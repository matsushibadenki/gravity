"""Compare equal-band clock-curvature projections on two boxes."""

import argparse
from pathlib import Path

import numpy as np
from scipy.integrate import simpson

from curvature_band_matching import checkpointed_result
from direct_curvature_insertion import mixed_insertion
from short_mixed_quadrature import mixed_projections, orientation_check


def zero_sector_shift(length, size, axis, cutoff, intervals, checkpoint, *, harmonic=1):
    times = np.linspace(cutoff, 2 * cutoff, intervals + 1)
    key = ["mixed-zero-sector", 1, length, size, axis, cutoff, intervals]
    if harmonic != 1:
        key.extend(["harmonic", harmonic])

    def compute():
        momentum = (0, 0, 0, 0)
        projected = mixed_insertion(size, momentum, times, axis, length_x=length, harmonic=harmonic)
        full = mixed_insertion(size, momentum, times, axis, True, length_x=length, harmonic=harmonic) / 2
        return float(simpson((projected - full) / times, x=times))

    return checkpointed_result(checkpoint, key, compute)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument("--compare-zero-sector", action="store_true")
    args = parser.parse_args()
    for length, sizes, name in ((1.8, (21, 25), "mixed-021"), (2.4, (29, 33), "mixed-long-24")):
        results = [orientation_check(axis, sizes, 8,
                                     args.checkpoint_dir / f"{name}-axis{axis}.json",
                                     .021, length) for axis in (0, 1)]
        if not all(stable for _, _, stable in results):
            parser.exit(1, f"Unresolved refinement at Lx={length}\n")
        integrals, shifts, _ = zip(*results)
        finite = mixed_projections(*integrals, length_x=length)
        observed = np.abs(mixed_projections(shifts[0], -shifts[1], length_x=length))
        print(f"Lx={length}: finite band {finite}; observed shifts {observed}")
        if args.compare_zero_sector:
            path = args.checkpoint_dir / "mixed-zero-sector-021.json"
            removed = [zero_sector_shift(length, sizes[-1], axis, .021, 8, path) for axis in (0, 1)]
            estimate = mixed_projections(*(np.array(integrals) - removed), length_x=length)
            print(f"Lx={length}: unprojected diagnostic {estimate}; zero-sector shifts {removed}")


if __name__ == "__main__":
    main()
