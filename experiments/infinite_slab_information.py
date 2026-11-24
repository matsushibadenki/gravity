"""Evaluate the normal covariance by Fourier integration on the infinite lattice."""

from math import log, sqrt
import sys

import numpy as np

from clock_tensor_slab import covariance_symbols, gaussian_entropy
from transverse_slab_integral import focused_rule


def covariance_matrix(kernel, sites, components):
    # For an infinite lattice, signed displacements are used without wrapping.
    offsets = sites[:, None] - sites[None, :] + len(kernel) // 2
    blocks = kernel[offsets, :components, :components]
    size = len(sites) * components
    return blocks.transpose(0, 2, 1, 3).reshape(size, size)


def density(spacing, width, gaps, normal_points, transverse_points, coupling):
    sites = np.arange(round(width / spacing))
    unions = [np.concatenate((sites, sites + len(sites) + round(gap / spacing)))
              for gap in gaps]
    lag = unions[-1][-1]
    (normal_angles, _), (normal_weights, _) = focused_rule(normal_points)
    transverse_angles, transverse_weights = focused_rule(transverse_points)
    transform = np.exp(1j * np.arange(-lag, lag + 1)[:, None] * normal_angles) * normal_weights
    values = np.zeros((len(gaps), 2))
    for ky, wy in zip(transverse_angles[0], transverse_weights[0]):
        shape = (normal_points, 1, transverse_points)
        symbols = covariance_symbols(shape, spacing, 2, coupling, "improved",
                                     (np.array([ky]), transverse_angles[1]), normal_angles)
        kernels = [np.einsum("lk,kzij->lzij", transform, symbol[:, 0], optimize=True)
                   for symbol in symbols]
        for kz, wz in enumerate(transverse_weights[1]):
            def entropy(region, components):
                return gaussian_entropy(*(covariance_matrix(kernel[:, kz], region, components)
                                          for kernel in kernels))

            for sector, components in enumerate((5, 6)):
                single = entropy(sites, components)
                for index, union in enumerate(unions):
                    values[index, sector] += wy * wz * (2 * single - entropy(union, components))
    return values / spacing**2


def main():
    spacing, width = 0.15, 0.6
    gaps = (0.6, 1.2, 1.8, 2.4, 3.0, 3.6)
    strength = 0.45 * sqrt(3 / 2)
    results = {}
    for normal, transverse in ((112, 32), (176, 32), (176, 40)):
        data = density(spacing, width, gaps, normal, transverse, strength)
        assert np.all(data > 0) and np.all(np.diff(data, axis=0) < 0)
        assert np.all(data[:, 1] >= data[:, 0])
        results[normal, transverse] = data
        print(f"points=({normal}, {transverse}, {transverse})\n{data}", flush=True)
    normal_change = np.max(np.abs(results[112, 32] / results[176, 32] - 1))
    transverse_change = np.max(np.abs(results[176, 32] / results[176, 40] - 1))
    print(f"Maximum refinement changes: normal={normal_change:.3%}, "
          f"transverse={transverse_change:.3%}", flush=True)
    assert normal_change < 0.02 and transverse_change < 0.05
    chosen = results[176, 40]
    baseline = density(spacing, width, gaps, 176, 40, 0)
    print("Matched baseline differences:\n", chosen - baseline, flush=True)
    print("Shell slopes:", [round(log(a / b) / 0.6, 4) for a, b in
                           zip(chosen[:-1, 0], chosen[1:, 0])], flush=True)


def cutoff_check():
    spacing, width = 0.1, 0.6
    gaps = (0.6, 1.2, 1.8, 2.4, 3.0, 3.6)
    coupling = 0.45 * sqrt(3 / 2)
    coarse = density(spacing, width, gaps, 176, 32, coupling)
    refined = density(spacing, width, gaps, 176, 40, coupling)
    print("Finer cutoff, coupled results:\n", refined, flush=True)
    difference = np.max(np.abs(coarse / refined - 1))
    print(f"Finer-cutoff transverse refinement change: {difference:.3%}", flush=True)
    assert difference < 0.05
    baseline = density(spacing, width, gaps, 176, 40, 0)
    print("Finer-cutoff matched baseline differences:\n", refined - baseline, flush=True)


if __name__ == "__main__":
    if "--refine-cutoff" in sys.argv:
        cutoff_check()
    else:
        main()
