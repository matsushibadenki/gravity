"""Compare fitted long-box curvature responses at matched proper-time bands."""

import argparse
import json
from pathlib import Path

import numpy as np

from curvature_cutoff_extrapolation import band_projection, intercept_weights
from curvature_momentum_validation import fixed_box_comparison
from curvature_band_matching import band_resolution, common_volume_shift
from curvature_four_wave import collect


def independent_quartic(reference, long_box, cutoff):
    prior, prior_shifts = collect(reference, cutoff, (37, 41))
    long = np.empty((2, 2))
    long_shifts = np.empty_like(long)
    for row, shear in enumerate((False, True)):
        for col, harmonic in enumerate((1, 2)):
            rows = [{int(cap): pair for cap, pair in
                     long_box[json.dumps([1, 5.6, cutoff, harmonic, shear, size, [8, 12]])].items()}
                    for size in (49, 53)]
            long[row, col] = rows[-1][12][1]
            long_shifts[row, col] = band_resolution(rows, 8, 12)

    def quartic(data, length):
        q2 = (2 * np.pi / length)**2 * np.arange(1, data.shape[1] + 1)**2
        value = (data[0] + common_volume_shift(length) + 3 * data[1]) / q2**2
        return q2, value

    q2, baseline = quartic(prior[:, :3], 4.2)
    long_q2, observed = quartic(long, 5.6)
    nodes = np.column_stack((np.ones(3), q2))
    weights = np.column_stack((np.ones(2), long_q2)) @ np.linalg.pinv(nodes)
    prior_error = (prior_shifts[0, :3] + 3 * prior_shifts[1, :3]) / q2**2
    long_error = (long_shifts[0] + 3 * long_shifts[1]) / long_q2**2
    return long_q2, observed, weights @ baseline, long_error + abs(weights) @ prior_error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, action="append", required=True)
    parser.add_argument("--long-box", type=Path, required=True)
    args = parser.parse_args()
    reference = {}
    for path in args.reference:
        reference.update(json.loads(path.read_text()))
    try:
        long_box = json.loads(args.long_box.read_text())
        _, short_024, _, short_024_shift, _, _ = fixed_box_comparison(reference)
        # The shortest reference band has full 37/41 refinement, the longer box
        # is compared at identical time bounds and its own refinement pair.
        short_021, short_021_shift = band_projection(reference, 4.2, .021, (37, 41), (8, 12))
        values = []
        for cutoff, short, short_shift in (
            (.024, short_024, short_024_shift), (.021, short_021, short_021_shift)
        ):
            long, long_shift = band_projection(long_box, 5.6, cutoff, (49, 53), (8, 12))
            print(f"sigma={cutoff}: Lx=4.2 {short}, shifts={short_shift}")
            print(f"sigma={cutoff}: Lx=5.6 {long}, shifts={long_shift}")
            print(f"Changes at matched cutoff: {long-short}")
            q2, observed, predicted, shifts = independent_quartic(reference, long_box, cutoff)
            print(f"Long-box squared momenta: {q2}; Einstein-free response: {observed}")
            print(f"Short-box three-wave q^6 prediction at those momenta: {predicted}")
            print(f"Observed refinement shifts on the difference: {shifts}")
            values.append((short, long, short_shift, long_shift))
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")

    weights = intercept_weights(np.array([.024, .021]))
    first, second, first_shift, second_shift = (np.array(v) for v in zip(*values))
    print("Two-band intercept, Lx=4.2:", weights @ first, "shifts:", abs(weights) @ first_shift)
    print("Two-band intercept, Lx=5.6:", weights @ second, "shifts:", abs(weights) @ second_shift)
    print("At each box the fit uses two momenta, with no independent higher-power momentum check.")


if __name__ == "__main__":
    main()
