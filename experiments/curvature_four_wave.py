"""Compare q^6 and q^8 curvature projections on fixed-box checkpoint data."""

import argparse
import json
from pathlib import Path

import numpy as np

from curvature_cutoff_extrapolation import intercept_weights
from curvature_momentum_validation import (
    CUTOFF, LENGTH_X, REFERENCE, REFERENCE_SHIFTS, common_volume_shift,
    refine_fundamental, wave_rows,
)


def action_projections(responses, shifts, cutoff, length=LENGTH_X):
    count = responses.shape[1]
    square = (2 * np.pi / length)**2 * np.arange(1, count + 1)**2
    design = np.column_stack([square**power for power in range(1, count + 1)])
    inverse = np.linalg.inv(design)

    def project(data):
        conformal, shear = data @ inverse.T
        return np.array([cutoff * (conformal[0] / 3 - shear[0]) / 2,
                         (conformal[1] - 6 * shear[1]) / 18, shear[1]])

    mapping = np.column_stack([project(unit.reshape(responses.shape))
                               for unit in np.eye(responses.size)])
    adjusted = responses.copy()
    adjusted[0] += common_volume_shift(length)
    return project(adjusted), abs(mapping) @ shifts.ravel()


def fourth_holdout(responses, shifts):
    square = (2 * np.pi / LENGTH_X)**2 * np.arange(1, 5)**2
    quartic = (responses[0] + common_volume_shift(LENGTH_X) + 3 * responses[1]) / square**2
    observed = (shifts[0] + 3 * shifts[1]) / square**2
    # Fit a q^8 response using three waves, with the fourth left out.
    nodes = np.column_stack((np.ones(4), square, square**2))
    weight = np.linalg.solve(nodes[:3].T, nodes[3])
    return quartic[3] - weight @ quartic[:3], observed[3] + abs(weight) @ observed[:3]


def collect(cache, cutoff, fourth_sizes):
    if cutoff == CUTOFF:
        first, first_shift = refine_fundamental(cache, cutoff, REFERENCE[:, 0])
        third, third_shift = wave_rows(cache, cutoff, 3, (33, 37))
        waves = [(first, first_shift), (REFERENCE[:, 1], REFERENCE_SHIFTS[:, 1]), (third, third_shift)]
    else:
        waves = [wave_rows(cache, cutoff, h, (37, 41) if h == 1 or cutoff == .021 else (33, 37))
                 for h in (1, 2, 3)]
    waves.append(wave_rows(cache, cutoff, 4, fourth_sizes))
    return np.column_stack([v for v, _ in waves]), np.column_stack([s for _, s in waves])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, action="append", required=True)
    parser.add_argument("--fourth-sizes", type=int, nargs=2, default=(37, 41))
    args = parser.parse_args()
    cache = {}
    for path in args.checkpoint:
        cache.update(json.loads(path.read_text()))
    bands = []
    for cutoff in (.035, .028, .024, .021):
        try:
            responses, shifts = collect(cache, cutoff, tuple(args.fourth_sizes))
        except ValueError as error:
            print(error)
            continue
        sixth, sixth_shift = action_projections(responses[:, :3], shifts[:, :3], cutoff)
        eighth, eighth_shift = action_projections(responses, shifts, cutoff)
        residual, observed = fourth_holdout(responses, shifts)
        print(f"sigma={cutoff}: q^6 coefficients={sixth}; shifts={sixth_shift}")
        print(f"sigma={cutoff}: q^8 coefficients={eighth}; shifts={eighth_shift}")
        print(f"sigma={cutoff}: fourth-wave holdout={residual:.10g}; shifts={observed:.10g}")
        bands.append((cutoff, sixth, eighth, eighth_shift))
    for subset in (bands, bands[-2:]):
        if len(subset) < 2:
            continue
        cutoffs, sixth, eighth, shifts = zip(*subset)
        weights = intercept_weights(np.array(cutoffs))
        print(f"Linear cutoff intercept for {cutoffs}: q^6={weights @ sixth}; "
              f"q^8={weights @ eighth}; q^8 shifts={abs(weights) @ shifts}")


if __name__ == "__main__":
    main()
