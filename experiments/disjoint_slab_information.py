"""Measure mutual information between disjoint slabs of fixed width."""

from math import log, sqrt

import numpy as np

from clock_tensor_slab import covariance_symbols, regional_entropy


def mutual_information(spacing, shape, width, separations, coupling, stencil, transverse_rule=None):
    _, ny, nz = shape
    angles, weights = transverse_rule if transverse_rule is not None else (None, None)
    position, momentum = covariance_symbols(shape, spacing, 2, coupling, stencil, angles)
    sites = np.arange(round(width / spacing))
    unions = [
        np.concatenate((sites, sites + len(sites) + round(separation / spacing)))
        for separation in separations
    ]
    information = np.zeros((len(separations), 2))
    for ky in range(ny):
        for kz in range(nz):
            x, p = position[:, ky, kz], momentum[:, ky, kz]
            weight = weights[0][ky] * weights[1][kz] if weights is not None else 1 / (ny * nz)
            for sector, components in enumerate((5, 6)):
                single = regional_entropy(x, p, sites, components)
                for index, union in enumerate(unions):
                    information[index, sector] += weight * (2 * single - regional_entropy(x, p, union, components))
    return information / spacing**2


def main():
    width = 0.6
    separations = (0.6, 1.2, 1.8, 2.4)
    coupling = 0.45 * sqrt(3 / 2)
    cases = (
        (0.3, 7.2, 1.2, "improved"),
        (0.15, 7.2, 1.2, "improved"),
        (0.15, 9.6, 1.2, "improved"),
        (0.15, 7.2, 1.8, "improved"),
        (0.15, 7.2, 1.2, "centered"),
    )
    for spacing, length, transverse, stencil in cases:
        shape = tuple(round(size / spacing) for size in (length, transverse, transverse))
        assert length - 2 * width > 2 * max(separations)
        coupled = mutual_information(spacing, shape, width, separations, coupling, stencil)
        baseline = mutual_information(spacing, shape, width, separations, 0, stencil)
        assert np.all(coupled > 0)
        assert np.all(coupled[:, 1] >= coupled[:, 0])
        assert np.all(np.diff(coupled, axis=0) < 0)
        print(f"a={spacing:.2f}, Lx={length:.1f}, Lperp={transverse:.1f}, {stencil}", flush=True)
        for separation, values, change in zip(separations, coupled, coupled - baseline):
            print(f"  gap={separation:.1f}: shell={values[0]:.8f}, joint={values[1]:.8f}, "
                  f"coupling delta=({change[0]:+.8f}, {change[1]:+.8f})", flush=True)
        slopes = [log(a / b) / (right - left) for a, b, left, right in
                  zip(coupled[:-1, 0], coupled[1:, 0], separations[:-1], separations[1:])]
        print("  shell effective slopes:", " ".join(f"{slope:.3f}" for slope in slopes), flush=True)


if __name__ == "__main__":
    main()
