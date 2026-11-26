"""Inspect the restored mixed heat kernel before proper-time quadrature."""

import argparse
from pathlib import Path

import numpy as np

from curvature_band_matching import checkpointed_result
from direct_curvature_insertion import mixed_insertion
from mixed_uv_refinement import (
    CUTOFFS, HIGH_LEVERAGE_ROWS, LENGTH_SEQUENCE, NEW_CUTOFF, integrate_trace,
    production_grids, production_traces, romberg_zero_projection,
)
from short_mixed_quadrature import mixed_projections
from transverse_insertion_sum import mixed_samples, sum_transverse


def zero_trace(directory, length, axis, cutoff, times):
    key = ["mixed-zero-trace", 1, float(length), axis, float(cutoff), len(times)]

    def compute():
        def correction(size):
            momentum = (0, 0, 0, 0)
            projected = mixed_insertion(size, momentum, times, axis, length_x=length)
            full = mixed_insertion(size, momentum, times, axis, True, length_x=length) / 2
            return projected - full

        small, large = map(correction, (9, 13))
        np.testing.assert_allclose(small, large, rtol=0, atol=1e-10)
        return large.tolist()

    return np.asarray(checkpointed_result(directory / "mixed-kernel-zero-trace.json", key, compute))


def read_band(directory, index, cutoff, *, refined):
    length = LENGTH_SEQUENCE[index]
    if refined and (cutoff, index) in HIGH_LEVERAGE_ROWS:
        (_, size), intervals = HIGH_LEVERAGE_ROWS[cutoff, index]
        bands = [cutoff]
    else:
        groups = production_grids(index)
        size, bands = max((size, bands) for size, bands in groups.items() if cutoff in bands)
        intervals = 8
    times = np.linspace(cutoff, 2 * cutoff, intervals + 1)
    traces = []
    zeros = []
    for axis in (0, 1):
        stored = production_traces(directory, axis, index, size, bands,
                                   cached_only=True, intervals=intervals)[16][bands.index(cutoff)]
        correction = zero_trace(directory, length, axis, cutoff, times)
        traces.append(stored - correction)
        zeros.append(integrate_trace(correction, times, "romberg"))
    np.testing.assert_allclose(mixed_projections(*zeros, length_x=length),
                               romberg_zero_projection(directory, cutoff, length, intervals),
                               atol=1e-12, rtol=0)
    return times, np.array(mixed_projections(*traces, length_x=length)).T, size


def analyse(directory):
    cutoffs = np.r_[NEW_CUTOFF, CUTOFFS]
    square = (2 * np.pi / np.array(LENGTH_SEQUENCE))**2
    weights = [np.linalg.inv(np.vander(square[:n] / square[0], increasing=True))[0] for n in (3, 4)]
    for index, length in enumerate(LENGTH_SEQUENCE):
        shared = {}
        cross_grid = np.zeros(2)
        same_grid_count = 0
        for cutoff in cutoffs:
            times, rows, size = read_band(directory, index, cutoff, refined=True)
            for time, row in zip(times, rows):
                key = round(float(time), 12)
                if key in shared:
                    previous, old_size = shared[key]
                    if old_size == size:
                        np.testing.assert_allclose(row, previous, atol=1e-11, rtol=0)
                        same_grid_count += 1
                    else:
                        cross_grid = np.maximum(cross_grid, abs(row - previous))
                shared[key] = (row, size)
        print(f"Lx={length:g}: {len(shared)} distinct proper times; {same_grid_count} repeated same-grid nodes "
              f"agree; maximum shared-node cross-grid changes={cross_grid}.", flush=True)

    for cutoff in cutoffs:
        rows = np.array([read_band(directory, i, cutoff, refined=True)[1][[0, -1]]
                         for i in range(len(LENGTH_SEQUENCE))])
        standard = np.array([read_band(directory, i, cutoff, refined=False)[1][[0, -1]]
                             for i in range(len(LENGTH_SEQUENCE))])
        endpoints = [weight @ rows[:len(weight), :, 1] for weight in weights]
        variations = abs(weights[-1]) @ abs(rows[:, :, 1] - standard[:, :, 1])
        print(f"sigma={cutoff:g}: Ricci-clock endpoints by wave={rows[:, :, 1]}; "
              f"three- and four-wave endpoints={endpoints}; "
              f"four-wave endpoint change bound={variations}")
        print("dB/dlog(sigma) by wave and at q=0 (three/four waves):",
              np.diff(rows[:, :, 1], axis=1).ravel(), *(end - start for start, end in endpoints))
        print("Lower endpoint k/(s q^2) by wave:", rows[:, 0, 1] / (cutoff * square))


def transverse_period_check(directory):
    """Change all three transverse periods at fixed longitudinal probe and grid."""
    length, size = 3., 41
    times = np.array([[.015, .030], [.024, .048]])
    periods = (1.8, 2.4)
    caps = ((16, 20), (22, 27))
    traces = []
    for axis in (0, 1):
        key = ["mixed-transverse-period", 1, length, size, axis, times.tolist(), periods, caps]

        def compute():
            samples = mixed_samples(size, axis, times, length)
            return [[result.tolist() for result in sum_transverse(
                samples, size, axis, times, length, caps=pair, period=period).values()]
                for period, pair in zip(periods, caps)]

        values = np.array(checkpointed_result(directory / "mixed-transverse-period.json", key, compute))
        for row, cutoff in enumerate((.015, .024)):
            flat = np.linspace(cutoff, 2 * cutoff, 9)
            correction = zero_trace(directory, length, axis, cutoff, flat)[[0, -1]]
            values[:, :, 2*row:2*row+2] -= correction
        traces.append(values)

    projections = []
    for index, period in enumerate(periods):
        projection = np.array(mixed_projections(*(v[index] for v in traces), length_x=length, period=period))
        projections.append(projection)
        print(f"Transverse period={period:g}: endpoints={projection[:, -1]}; "
              f"cap changes={projection[:, -1]-projection[:, 0]}")
    reference = np.concatenate([read_band(directory, 2, cutoff, refined=False)[1][[0, -1]]
                                for cutoff in (.015, .024)]).T
    np.testing.assert_allclose(projections[0][:, -1], reference, atol=1e-11, rtol=0)
    print("Transverse period change [RX, Ricci-clock]:", projections[1][:, -1] - projections[0][:, -1])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument("--transverse-period", action="store_true")
    args = parser.parse_args()
    (transverse_period_check if args.transverse_period else analyse)(args.checkpoint_dir)


if __name__ == "__main__":
    main()
