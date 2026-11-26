"""Compare cached common-reference curvature projections along the cutoff sequence."""

import argparse
import json
from pathlib import Path

import numpy as np

from curvature_band_matching import band_resolution, common_volume_shift, momentum_projections, settled


def intercept_weights(points):
    """Linear intercept weights in the supplied independent variable."""
    design = np.column_stack((np.ones(len(points)), points))
    return np.linalg.pinv(design)[0]


def band_projection(cache, length, cutoff, sizes, caps):
    lower, upper = caps
    values = np.empty((2, 2))
    shifts = np.empty_like(values)
    for row, shear in enumerate((False, True)):
        for column, harmonic in enumerate((1, 2)):
            key = [1, length, cutoff, harmonic, shear]
            rows = []
            for size in sizes:
                grid_key = key + [size]
                if caps != (5, 8):
                    grid_key.append(caps)
                stored = cache.get(json.dumps(grid_key))
                if stored is None:
                    raise ValueError(f"Missing checkpoint row {grid_key}")
                rows.append({int(cap): band for cap, band in stored.items()})
            coarse, fine = rows
            if not (settled(coarse[upper][1], fine[upper][1])
                    and settled(fine[lower][1], fine[upper][1])
                    and settled(*fine[upper])):
                raise ValueError(f"Unresolved numerical refinement for {grid_key}")
            values[row, column] = fine[upper][1]
            shifts[row, column] = band_resolution(rows, lower, upper)
    values[0] += common_volume_shift(length)
    square = (2 * np.pi / length)**2 * np.array([1., 4.])
    momentum_weights = intercept_weights(square)

    def project(responses):
        einstein, scalar, ricci = momentum_projections(*responses, square)
        return np.array([cutoff * einstein, momentum_weights @ scalar,
                         momentum_weights @ ricci])

    # The projections are linear, so propagate test shifts by absolute weights.
    weights = np.column_stack([project(unit.reshape(2, 2)) for unit in np.eye(4)])
    return project(values), abs(weights) @ shifts.ravel()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, action="append", required=True)
    args = parser.parse_args()
    cache = {}
    for path in args.checkpoint:
        cache.update(json.loads(path.read_text()))
    sequence = ((3.6, 0.035, (25, 29), (5, 8)), (3.6, 0.028, (29, 33), (5, 8)),
                (4.2, 0.024, (33, 37), (8, 12)))
    bands, shifts = [], []
    for length, cutoff, sizes, caps in sequence:
        try:
            value, shift = band_projection(cache, length, cutoff, sizes, caps)
        except ValueError as error:
            print(error)
            return
        bands.append(value)
        shifts.append(shift)
        print(f"sigma={cutoff}: scaled Einstein, R^2, Ric^2 = {value}; "
              f"observed refinement shifts = {shift}")
    cutoffs = np.array([item[1] for item in sequence])
    weights = intercept_weights(cutoffs)
    extrapolated = weights @ bands
    two_band = intercept_weights(cutoffs[1:]) @ bands[1:]
    print(f"Three-band linear intercept: {extrapolated}")
    print(f"Two-shortest-band linear intercept: {two_band}")
    print(f"Observed refinement shifts propagated to three-band intercept: {abs(weights) @ shifts}")
    print("Diagnostics only. Two momenta cannot test omitted higher powers of momentum, "
          "and the shortest band changes the box length.")


if __name__ == "__main__":
    main()
