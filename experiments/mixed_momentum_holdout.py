"""Test the low-momentum clock response against box length and proper time."""

import argparse
from pathlib import Path

import numpy as np

from curvature_cutoff_extrapolation import intercept_weights
from matched_wave_comparison import mixed_wave
from mixed_cross_box import zero_sector_shift
from restored_short_cutoff import mixed_zero_projection
from short_mixed_quadrature import mixed_projections


CUTOFF = .018
LENGTHS = np.array([1.8, 2.4, 3.])
CUTOFFS = np.array([.018, .021, .024])
FOURTH_LENGTH = 3.6
REFERENCE_GRIDS = {
    .018: (((25, 29), "mixed-018"), ((33, 37), "mixed-long-24-018")),
    .021: (((21, 25), "mixed-021"), ((29, 33), "mixed-long-24")),
    .024: (((21, 25), "mixed-024"), ((29, 33), "mixed-long-24-024")),
}


def band_grids(cutoff):
    return (*REFERENCE_GRIDS[cutoff], ((37, 41), f"mixed-third-30-{round(1000*cutoff):03d}"))


def third_zero_projection(directory, cutoff=CUTOFF, length=3., harmonic=1):
    checkpoint = directory / f"mixed-zero-sector-third-{round(1000*cutoff):03d}.json"
    values = []
    for axis in (0, 1):
        coarse, fine = (zero_sector_shift(length, n, axis, cutoff, 8, checkpoint,
                                         harmonic=harmonic) for n in (9, 13))
        np.testing.assert_allclose(coarse, fine, rtol=0, atol=1e-10)
        values.append(fine)
    return np.array(mixed_projections(*values, length_x=length, harmonic=harmonic))


def momentum_check(square, responses, shifts):
    design = np.column_stack((np.ones(3), square))
    two_wave = np.linalg.inv(design[:2])
    predict = design[2] @ two_wave
    residual = responses[2] - predict @ responses[:2]
    observed = shifts[2] + abs(predict) @ shifts[:2]
    quadratic = np.linalg.inv(np.column_stack((design, square**2)))[0]
    return residual, observed, two_wave[0] @ responses[:2], quadratic @ responses, abs(quadratic) @ shifts


def compare_band(directory, cutoff):
    responses, shifts, paired_shifts = [], [], []
    for length, (sizes, prefix) in zip(LENGTHS, band_grids(cutoff)):
        projected, numerical, paired = mixed_wave(
            directory, float(length), 1, cutoff, sizes, prefix, paired=True)
        if length == 3. or (cutoff == .024 and length == 2.4):
            zero = third_zero_projection(directory, cutoff, length)
        else:
            zero = mixed_zero_projection(directory, float(length), cutoff, sizes[-1])
        responses.append(projected - zero)
        shifts.append(numerical)
        paired_shifts.append(paired)
        print(f"Lx={length:g}: restored={responses[-1]}; raw-grid shifts={numerical}; paired shifts={paired}")
    square = (2 * np.pi / LENGTHS)**2
    residual, observed, first, quadratic, uncertainty = momentum_check(
        square, np.array(responses), np.array(shifts))
    print("Third-momentum holdout residual and observed variation:", residual, observed)
    print("Linear two-momentum intercept:", first)
    print("Quadratic three-momentum intercept and observed variation:", quadratic, uncertainty)
    _, paired_holdout, _, _, paired_intercept = momentum_check(
        square, np.array(responses), np.array(paired_shifts))
    print("Paired numerical variation for holdout and quadratic intercept:",
          paired_holdout, paired_intercept)
    return np.array(responses), np.array(shifts), np.array(paired_shifts), np.stack((first, quadratic)), paired_intercept


def compare_box(directory, reference):
    np.testing.assert_allclose(2 * np.pi / 3, 2 * np.pi * 2 / 6)
    projected, numerical, paired = mixed_wave(directory, 6., 2, CUTOFF, (65, 73),
                                              "mixed-matched-60-018", paired=True)
    restored = projected - third_zero_projection(directory, CUTOFF, 6., 2)
    values, independent_shifts, paired_shifts, _, _ = reference
    print("Restored matched-wave projections at Lx=3 and Lx=6:", values[-1], restored)
    print("Matched q box difference (Lx=6 minus Lx=3):", restored - values[-1])
    print("Summed independent and paired variations:", numerical + independent_shifts[-1],
          paired + paired_shifts[-1])


def compare_fourth_box(directory):
    cutoff = .024
    length = FOURTH_LENGTH
    np.testing.assert_allclose(2 * np.pi / length, 2 * np.pi * 2 / (2 * length))
    results = []
    for box, harmonic, sizes, prefix in (
        (length, 1, (45, 49), "mixed-fourth-36-024"),
        (2 * length, 2, (65, 73), "mixed-fourth-matched-72-024"),
    ):
        values, independent, directions = mixed_wave(
            directory, box, harmonic, cutoff, sizes, prefix, signed=True)
        restored = values - third_zero_projection(directory, cutoff, box, harmonic)
        print(f"Lx={box:g}, harmonic={harmonic}: restored={restored}")
        results.append((restored, independent, directions))
    (small, small_independent, small_directions), (large, large_independent, large_directions) = results
    difference = large - small
    print("Matched fourth-wave box difference:", difference)
    paired = (abs(large_directions) + abs(small_directions)).sum(axis=1)
    print("Summed independent and orientation-paired variations:", large_independent + small_independent, paired)
    print("Simultaneous refinement differences by direction:", large_directions - small_directions)


def polynomial_check(points, responses, shifts):
    """Predict the final point and compare lower- and higher-degree intercepts."""
    degree = len(points) - 1
    design = np.vander(points / max(abs(points)), increasing=True)
    fit = np.linalg.inv(design[:-1, :degree])
    weights = design[-1, :degree] @ fit
    extended = np.linalg.inv(design)[0]
    return (responses[-1] - np.tensordot(weights, responses[:-1], axes=1),
            shifts[-1] + np.tensordot(abs(weights), shifts[:-1], axes=1),
            np.tensordot(extended, responses, axes=1),
            np.tensordot(abs(extended), shifts, axes=1))


def compare_fourth_wave(directory, cutoff, band):
    values, separate, paired, _, _ = band
    square = (2 * np.pi / np.r_[LENGTHS, FOURTH_LENGTH])**2
    projected, numerical, together = mixed_wave(
        directory, FOURTH_LENGTH, 1, cutoff, (45, 49),
        f"mixed-fourth-36-{round(1000*cutoff):03d}", paired=True)
    restored = projected - third_zero_projection(directory, cutoff, FOURTH_LENGTH)
    combined = np.vstack((values, restored))
    residual, observed, cubic, variation = polynomial_check(square, combined, np.vstack((paired, together)))
    _, separate_observed, _, _ = polynomial_check(square, combined, np.vstack((separate, numerical)))
    print(f"sigma={cutoff:g}, fourth-wave restored projections:", restored)
    print("Fourth-wave residual, paired and independent variations:", residual, observed, separate_observed)
    print("Four-wave cubic momentum intercept and paired variation:", cubic, variation)
    return cubic, variation


def compare_three_bands(directory, short, *, include_fourth):
    bands = [short, *(compare_band(directory, cutoff) for cutoff in CUTOFFS[1:])]
    by_wave = np.array([row[0] for row in bands])
    by_wave_shifts = np.array([row[2] for row in bands])
    residual, observed, _, _ = polynomial_check(CUTOFFS, by_wave, by_wave_shifts)
    print("Third-band holdout residual and paired variation by fixed momentum:")
    for length, change, variation in zip(LENGTHS, residual, observed):
        print(f"q={2 * np.pi / length:.9g}:", change, variation)
    fits = np.array([row[3][1] for row in bands])
    shifts = np.array([row[4] for row in bands])
    residual, observed, intercept, variation = polynomial_check(CUTOFFS, fits, shifts)
    linear_weights = intercept_weights(CUTOFFS[:2])
    print("Third-band holdout residual and paired variation:", residual, observed)
    print("Shortest-pair linear, all-band linear and quadratic cutoff intercepts:",
          linear_weights @ fits[:2], intercept_weights(CUTOFFS) @ fits, intercept)
    print("Quadratic cutoff intercept paired variation:", variation)
    if not include_fourth:
        return
    cubic_fits, cubic_shifts = map(np.array, zip(*[
        compare_fourth_wave(directory, cutoff, band) for cutoff, band in zip(CUTOFFS, bands)
    ]))
    residual, observed, intercept, variation = polynomial_check(
        CUTOFFS, cubic_fits, cubic_shifts)
    print("Four-wave third-band holdout residual and paired variation:", residual, observed)
    print("Four-wave all-band linear and quadratic cutoff intercepts:",
          intercept_weights(CUTOFFS) @ cubic_fits, intercept)
    print("Four-wave quadratic cutoff intercept paired variation:", variation)


def signed_fit_check(directory):
    """Propagate simultaneous numerical refinements through the entire fit."""
    lengths = np.r_[LENGTHS, FOURTH_LENGTH]
    shifts = []
    for cutoff in CUTOFFS:
        grids = (*band_grids(cutoff), ((45, 49), f"mixed-fourth-36-{round(1000*cutoff):03d}"))
        shifts.append([mixed_wave(directory, length, 1, cutoff, sizes, prefix, signed=True)[2]
                       for length, (sizes, prefix) in zip(lengths, grids)])
    shifts = np.array(shifts)
    square = (2 * np.pi / lengths)**2
    for count in (3, 4):
        weights = np.linalg.solve(np.vander(square[:count], increasing=True).T, np.eye(count)[0])
        for degree in (1, 2):
            fit = np.polynomial.polynomial.polyvander(CUTOFFS, degree)
            cutoff_weights = np.linalg.pinv(fit)[0]
            refit = np.einsum("s,q,sqij->ij", cutoff_weights, weights, shifts[:, :count])
            envelope = np.einsum("s,q,sqij->i", abs(cutoff_weights), abs(weights), abs(shifts[:, :count]))
            print(f"{count} waves, cutoff degree {degree}: simultaneous changes by direction {refit}; "
                  f"summed envelope {envelope}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--zero-only", action="store_true", help="Check only the zero-sector corrections.")
    mode.add_argument("--matched-box", action="store_true", help="Compare the third momentum in two boxes.")
    mode.add_argument("--two-bands", action="store_true", help="Compare the momentum fits across proper-time bands.")
    mode.add_argument("--three-bands", action="store_true", help="Hold out the third proper-time band.")
    mode.add_argument("--fourth-wave", action="store_true", help="Also hold out the fourth momentum in each band.")
    mode.add_argument("--fourth-box", action="store_true", help="Compare the fourth momentum in two boxes.")
    mode.add_argument("--signed-fit", action="store_true", help="Track simultaneous refinements across the fit.")
    args = parser.parse_args()
    directory = args.checkpoint_dir
    if args.zero_only:
        for cutoff, length, harmonic in ((.018, 3., 1), (.021, 3., 1), (.018, 6., 2)):
            print(cutoff, length, harmonic, third_zero_projection(directory, cutoff, length, harmonic))
        return
    if args.fourth_box:
        compare_fourth_box(directory)
        return
    if args.signed_fit:
        signed_fit_check(directory)
        return
    short = compare_band(directory, CUTOFF)
    if args.matched_box:
        compare_box(directory, short)
    if args.two_bands:
        long = compare_band(directory, .021)
        weights = intercept_weights(np.array([CUTOFF, .021]))
        fits = np.stack((short[3], long[3]))
        print("Cutoff intercepts for two- and three-momentum fits:", np.tensordot(weights, fits, axes=1))
        print("Summed paired variations for the three-momentum cutoff intercept:",
              abs(weights) @ np.stack((short[4], long[4])))
    if args.three_bands or args.fourth_wave:
        compare_three_bands(directory, short, include_fourth=args.fourth_wave)


if __name__ == "__main__":
    main()
