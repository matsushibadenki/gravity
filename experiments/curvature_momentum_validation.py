"""Hold out the third harmonic from the local curvature and q^6 fits."""

import argparse
import json
from pathlib import Path

import numpy as np

from curvature_band_matching import band_resolution, common_volume_shift, momentum_projections, settled
from curvature_cutoff_extrapolation import band_projection, intercept_weights


LENGTH_X = 4.2
CUTOFF = 0.024
SIZES = (33, 37)
CAPS = (8, 12)

# Last resolved grid and observed refinement shifts, from the preceding
# checkpoint run recorded in the roadmap. The conformal values are raw bands.
REFERENCE = np.array([[3.10789702129868, 12.339423110294524],
                      [-1.1166259766947637, -4.545833001234427]])
REFERENCE_SHIFTS = np.array([[0.0005296158537, 0.002308785162],
                             [0.000227895851, 0.001229052763]])


def wave_rows(cache, cutoff, harmonic, sizes=SIZES):
    values, shifts = [], []
    lower, upper = CAPS
    for shear in (False, True):
        grids = []
        for size in sizes:
            key = json.dumps([1, LENGTH_X, cutoff, harmonic, shear, size, CAPS])
            if key not in cache:
                raise ValueError(f"Missing checkpoint row {key}")
            grids.append({int(cap): estimates for cap, estimates in cache[key].items()})
        coarse, fine = grids
        if not (settled(coarse[upper][1], fine[upper][1])
                and settled(fine[lower][1], fine[upper][1])
                and settled(*fine[upper])):
            raise ValueError(f"Refinement failed for sigma={cutoff}, harmonic={harmonic}, shear={shear}")
        values.append(fine[upper][1])
        shifts.append(band_resolution(grids, lower, upper))
    return np.array(values), np.array(shifts)


def quartic_holdout(responses, shifts, length_x):
    square = (2 * np.pi / length_x)**2 * np.arange(1, 4)**2
    conformal, shear = responses
    conformal_shift, shear_shift = shifts
    projection = (conformal + common_volume_shift(length_x) + 3 * shear) / square**2
    numerical = (conformal_shift + 3 * shear_shift) / square**2
    # A q^6 term in the response gives a q^2 term in the projection.
    fraction = (square[2] - square[0]) / (square[1] - square[0])
    weights = np.array([1 - fraction, fraction])
    return (projection, projection[2] - weights @ projection[:2],
            numerical[2] + abs(weights) @ numerical[:2])


def independent_einstein(responses, shifts, length_x):
    square = (2 * np.pi / length_x)**2 * np.arange(1, 4)**2
    # Divide out q^2 before fitting the local intercept to each family.
    weight = np.linalg.inv(np.column_stack((np.ones(3), square, square**2)))[0] / square
    conformal, shear = responses
    values = np.array([weight @ (conformal + common_volume_shift(length_x)) / 3,
                       -weight @ shear])
    observed = np.array([abs(weight) @ shifts[0] / 3, abs(weight) @ shifts[1]])
    return values, observed


def fixed_box_comparison(cache):
    longer_band = 0.028
    coarse, coarse_shift = band_projection(cache, LENGTH_X, longer_band, SIZES, CAPS)
    square = (2 * np.pi / LENGTH_X)**2 * np.array([1, 4])
    weights = intercept_weights(square)

    def reference_projection(responses):
        einstein, scalar, ricci = momentum_projections(*responses, square)
        return np.array([CUTOFF * einstein, weights @ scalar, weights @ ricci])

    reference = REFERENCE.copy()
    reference[0] += common_volume_shift(LENGTH_X)
    fine = reference_projection(reference)
    response_weights = np.column_stack([
        reference_projection(unit.reshape(2, 2)) for unit in np.eye(4)])
    fine_shift = abs(response_weights) @ REFERENCE_SHIFTS.ravel()
    cutoff_weights = intercept_weights(np.array([longer_band, CUTOFF]))
    return coarse, fine, coarse_shift, fine_shift, cutoff_weights @ [coarse, fine], (
        abs(cutoff_weights) @ [coarse_shift, fine_shift])


def three_wave_coefficients(responses, shifts, length_x, cutoff):
    square = (2 * np.pi / length_x)**2 * np.arange(1, 4)**2
    weights = np.linalg.inv(np.column_stack((square, square**2, square**3)))
    correction = np.array([[common_volume_shift(length_x)] * 3, [0.] * 3])

    def project(data):
        conformal, shear = data @ weights.T
        einstein = cutoff * (conformal[0] / 3 - shear[0]) / 2
        ricci = shear[1]
        return np.array([einstein, (conformal[1] - 6 * ricci) / 18, ricci])

    mapping = np.column_stack([project(unit.reshape(2, 3)) for unit in np.eye(6)])
    return project(responses + correction), abs(mapping) @ shifts.ravel()


def refine_fundamental(cache, cutoff, coarse):
    values, shifts = [], []
    lower, upper = CAPS
    for value, shear in zip(coarse, (False, True)):
        key = json.dumps([1, LENGTH_X, cutoff, 1, shear, 41, CAPS])
        if key not in cache:
            raise ValueError(f"Missing fundamental refinement {key}")
        fine = {int(cap): estimates for cap, estimates in cache[key].items()}
        if not (settled(value, fine[upper][1])
                and settled(fine[lower][1], fine[upper][1])
                and settled(*fine[upper])):
            raise ValueError(f"Fundamental refinement failed for sigma={cutoff}, shear={shear}")
        values.append(fine[upper][1])
        shifts.append(band_resolution([{upper: [value, value]}, fine], lower, upper))
    return np.array(values), np.array(shifts)


def cutoff_sweep(cache, reference_cache, sizes=SIZES, low_wave_cache=None):
    bands = []
    for cutoff in (0.035, 0.028, 0.024, 0.021):
        try:
            if cutoff == CUTOFF:
                third, third_shift = wave_rows(reference_cache, cutoff, 3)
                responses = np.column_stack((REFERENCE, third))
                shifts = np.column_stack((REFERENCE_SHIFTS, third_shift))
            else:
                merged = cache | (low_wave_cache or {})
                waves = []
                for h in (1, 2, 3):
                    refined = all(json.dumps([1, LENGTH_X, cutoff, h, shear, 41, CAPS]) in merged
                                  for shear in (False, True))
                    pair = (sizes[-1], 41) if refined else sizes
                    waves.append(wave_rows(merged, cutoff, h, pair))
                    if refined:
                        print(f"sigma={cutoff}: harmonic {h} passes the {pair[0]}-to-41-point check")
                responses = np.column_stack([wave[0] for wave in waves])
                shifts = np.column_stack([wave[1] for wave in waves])
        except ValueError as error:
            print(error)
            continue
        if low_wave_cache and cutoff == CUTOFF:
            try:
                refined, refined_shift = refine_fundamental(low_wave_cache, cutoff, responses[:, 0])
            except ValueError as error:
                print(error)
                continue
            print(f"sigma={cutoff}: fundamental change at 41 points={refined - responses[:, 0]}")
            responses[:, 0], shifts[:, 0] = refined, refined_shift
        quartic, residual, change = quartic_holdout(responses, shifts, LENGTH_X)
        einstein, einstein_change = independent_einstein(responses, shifts, LENGTH_X)
        print(f"sigma={cutoff}: quartic={quartic}; third-wave residual={residual:.8g}; "
              f"observed shift={change:.8g}; Einstein={einstein}; shifts={einstein_change}")
        values, variation = three_wave_coefficients(responses, shifts, LENGTH_X, cutoff)
        print("Three-wave band projections:", values, "observed shifts:", variation)
        bands.append((cutoff, values, variation))
    for subset in (bands, bands[-2:]):
        if len(subset) < 2:
            continue
        cutoffs, values, changes = zip(*subset)
        weights = intercept_weights(np.array(cutoffs))
        print(f"Linear cutoff intercept for {cutoffs}: {weights @ values}; "
              f"observed shifts={abs(weights) @ changes}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, help="Third-harmonic checkpoint.")
    parser.add_argument("--fixed-box-checkpoint", type=Path,
                        help="Checkpoint for the 0.028 band at the same box length.")
    parser.add_argument("--sweep-checkpoint", type=Path, help="Fixed-box multi-band checkpoint.")
    parser.add_argument("--sweep-sizes", type=int, nargs=2, default=SIZES)
    parser.add_argument("--low-wave-checkpoint", type=Path, help="Optional 41-point fundamental.")
    args = parser.parse_args()
    if args.checkpoint is None and args.fixed_box_checkpoint is None and args.sweep_checkpoint is None:
        parser.error("provide at least one checkpoint")
    if args.checkpoint is not None:
        try:
            values, shifts = wave_rows(json.loads(args.checkpoint.read_text()), CUTOFF, 3)
        except ValueError as error:
            parser.exit(1, f"{error}\n")
        responses = np.column_stack((REFERENCE, values))
        refinements = np.column_stack((REFERENCE_SHIFTS, shifts))
        projections, residual, observed_shifts = quartic_holdout(responses, refinements, LENGTH_X)
        print("Einstein-free quartic projections:", projections)
        print("Third-wave residual after fitting a q^6 response to the first two waves:", residual)
        print("Observed numerical shifts propagated to the residual:", observed_shifts)
        einstein, einstein_shift = independent_einstein(responses, refinements, LENGTH_X)
        print("Independent three-wave Einstein projections (conformal, shear):", einstein)
        print("Observed numerical shifts propagated to the Einstein projections:", einstein_shift)
    if args.fixed_box_checkpoint is not None:
        try:
            coarse, fine, cs, fs, limit, ls = fixed_box_comparison(
                json.loads(args.fixed_box_checkpoint.read_text()))
        except ValueError as error:
            parser.exit(1, f"{error}\n")
        print("Scaled Einstein, scalar squared, Ricci squared at sigma=0.028:", coarse, "shifts:", cs)
        print("Same projections at sigma=0.024:", fine, "shifts:", fs)
        print("Two-band linear intercept:", limit, "propagated shifts:", ls)
    if args.sweep_checkpoint is not None:
        cutoff_sweep(json.loads(args.sweep_checkpoint.read_text()),
                     json.loads(args.checkpoint.read_text()) if args.checkpoint else {},
                     tuple(args.sweep_sizes),
                     json.loads(args.low_wave_checkpoint.read_text()) if args.low_wave_checkpoint else None)
    print("Diagnostic only. The geometry and volume reference are fixed.")


if __name__ == "__main__":
    main()
