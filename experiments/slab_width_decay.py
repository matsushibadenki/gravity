"""Track finite slab entropy versus interface separation and box size."""

from math import sqrt

from clock_tensor_slab import covariance_symbols, slab_entropy


def width_curve(spacing, shape, widths, coupling):
    nx, ny, nz = shape
    position, momentum = covariance_symbols(shape, spacing, 2, coupling, "improved")
    sites = [round(width / spacing) for width in widths]
    selected = sorted({nx // 2, *sites, *(nx - n for n in sites)})
    totals = {(components, width): 0.0 for components in (5, 6) for width in selected}
    for ky in range(ny):
        for kz in range(nz):
            for components, width in totals:
                totals[components, width] += slab_entropy(
                    position[:, ky, kz], momentum[:, ky, kz], width, components
                )
    area = 2 * ny * nz * spacing**2
    return [
        [(totals[components, nx // 2]
          - (totals[components, n] + totals[components, nx - n]) / 2) / area
         for components in (5, 6)]
        for n in sites
    ]


def main():
    widths = (0.6, 1.2, 1.8)
    strength = 0.45 * sqrt(3 / 2)
    for spacing, length, transverse in ((0.3, 4.8, 1.2), (0.15, 4.8, 1.2),
                                        (0.15, 6.0, 1.2), (0.15, 4.8, 1.8)):
        shape = tuple(round(size / spacing) for size in (length, transverse, transverse))
        coupled = width_curve(spacing, shape, widths, strength)
        uncoupled = width_curve(spacing, shape, widths, 0)
        for sector in range(2):
            assert all(coupled[i][sector] > coupled[i + 1][sector] > 0
                       for i in range(len(widths) - 1))
        print(f"a={spacing:.2f}, Lx={length:.1f}, Lperp={transverse:.1f}", flush=True)
        for width, totals, baseline in zip(widths, coupled, uncoupled):
            print(f"  w={width:.1f} shell={totals[0]:.8f}, joint={totals[1]:.8f}, "
                  f"clock delta=({totals[0]-baseline[0]:+.8f}, {totals[1]-baseline[1]:+.8f})",
                  flush=True)


if __name__ == "__main__":
    main()
