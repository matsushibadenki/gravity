"""Compare width-dependent entropy after removing equal-area terms."""

from math import sqrt

from clock_tensor_slab import covariance_symbols, slab_entropy


def compare_widths(spacing, shape, stencil, coupling=0.45 * sqrt(3 / 2)):
    nx, ny, nz = shape
    position, momentum = covariance_symbols(
        shape, spacing, gap=2, coupling=coupling, stencil=stencil
    )
    widths = (nx // 4, nx // 2, 3 * nx // 4)
    totals = {(components, width): 0.0 for components in (5, 6) for width in widths}
    for ky in range(ny):
        for kz in range(nz):
            for (components, width) in totals:
                totals[components, width] += slab_entropy(
                    position[:, ky, kz], momentum[:, ky, kz], width, components
                )
    area = 2 * ny * nz * spacing**2
    results = []
    for components in (5, 6):
        narrow, wide, complement = (totals[components, width] for width in widths)
        # Symmetrization cancels the volume contribution even for a mixed
        # whole species. Both partitions have the same pair of interfaces.
        difference = (wide - (narrow + complement) / 2) / area
        results.append((wide / area, difference))
    return results


def main():
    for spacing, shape in ((0.3, (8, 4, 4)), (0.15, (16, 8, 8)), (0.075, (32, 16, 16))):
        differences = {}
        for stencil in ("centered", "improved"):
            (shell_raw, shell), (joint_raw, joint) = compare_widths(spacing, shape, stencil)
            differences[stencil] = (shell, joint)
            print(f"a={spacing:.3f} {stencil:8s} width difference/area "
                  f"shell={shell:.8f}, joint={joint:.8f}; "
                  f"raw half-slab/area shell={shell_raw:.7f}, joint={joint_raw:.7f}")
        assert all(value > 0 for pair in differences.values() for value in pair)
        if spacing == 0.075:
            (_, free_shell), (_, free_joint) = compare_widths(spacing, shape, "centered", coupling=0)
            print(f"uncoupled width difference/area: shell={free_shell:.8f}, joint={free_joint:.8f}")
            for stencil, (shell, joint) in differences.items():
                print(f"{stencil:8s} interaction contribution: "
                      f"shell={shell-free_shell:+.8f}, joint={joint-free_joint:+.8f}")


if __name__ == "__main__":
    main()
