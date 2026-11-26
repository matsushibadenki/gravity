"""Match mixed heat traces to the transverse continuum at fixed physical momentum."""

import argparse
from pathlib import Path

import numpy as np

from curvature_band_matching import checkpointed_result, settled
from mixed_kernel_endpoints import read_band
from mixed_uv_refinement import CUTOFFS, LENGTH_SEQUENCE, NEW_CUTOFF, integrate_trace, polynomial_check
from short_mixed_quadrature import mixed_projections
from transverse_insertion_sum import (
    integrate_transverse, mixed_samples, radial_continuum_trace, sum_transverse,
)


BANDS = np.r_[CUTOFFS, NEW_CUTOFF]
GRIDS = ((25, 29), (33, 37), (41, 45), (49, 53))
MATCHED_GRIDS = {3: (73, 81), 0: (49, 57)}
LOWEST_REFINEMENT = (89, (0, 3))
SHORTEST_REFINEMENT = (97, 3)
PERIODS = (1.8, 2.4, 3.6, 4.8)
CAPS = tuple((int(np.ceil(16 * p / 1.8)), int(np.ceil(20 * p / 1.8))) for p in PERIODS)
TIMES = np.array([np.linspace(sigma, 2 * sigma, 17) for sigma in BANDS])


def trace_rows(directory, index, size, axis, *, cached_only=False, harmonic=1):
    length = harmonic * LENGTH_SEQUENCE[index]
    path = directory / f"mixed-transverse-continuum-{index}-axis{axis}.json"
    key = ["mixed-transverse-continuum", 1, size, axis, float(length), TIMES.tolist(), PERIODS, CAPS]
    if harmonic != 1:
        key.append(harmonic)

    def compute():
        if cached_only:
            raise FileNotFoundError(f"Missing transverse-continuum checkpoint at Lx={length:g}, N={size}, axis={axis}")
        samples = mixed_samples(size, axis, TIMES, length, harmonic, project_zero=False)
        continuous = integrate_transverse(samples, size, axis, TIMES, length)
        periodic = [
            [(trace * (1.8 / period)**3).reshape(TIMES.shape).tolist()
             for trace in sum_transverse(samples, size, axis, TIMES, length, caps=caps, period=period).values()]
            for period, caps in zip(PERIODS, CAPS)
        ]
        return {"continuous": continuous.reshape(TIMES.shape).tolist(), "periodic": periodic}

    rows = checkpointed_result(path, key, compute)
    return np.asarray(rows["continuous"]), np.asarray(rows["periodic"])


def integrals(traces, *, stride=1, times=TIMES):
    return np.array([integrate_trace(trace[::stride], nodes[::stride], "romberg")
                     for trace, nodes in zip(traces, times)])


def matched_trace(directory, index, size, axis, *, cached_only=False, bands=None):
    if bands is None:
        try:
            return trace_rows(directory, index, size, axis, cached_only=True, harmonic=2)[0]
        except FileNotFoundError:
            pass
    length = 2 * LENGTH_SEQUENCE[index]
    times = TIMES if bands is None else TIMES[list(bands)]
    key = ["mixed-matched-radial", 1, size, axis, float(length), times.tolist()]
    path = directory / f"mixed-matched-radial-{index}-axis{axis}.json"

    def compute():
        if cached_only:
            raise FileNotFoundError(f"Missing matched trace at Lx={length:g}, N={size}, axis={axis}")
        return radial_continuum_trace(size, axis, times, length, 2).reshape(times.shape).tolist()

    return np.asarray(checkpointed_result(path, key, compute))


def refined_integrals(previous, trace, length, axis, *, require_all=True, times=TIMES):
    final = integrals(trace, times=times)
    previous_grid = integrals(previous, times=times)
    fewer_nodes = integrals(trace, stride=2, times=times)
    resolved = np.array([settled(coarse, fine) and settled(old, new) and settled(fewer, new)
                         for coarse, fine, old, new, fewer in
                         zip(previous, trace, previous_grid, final, fewer_nodes)])
    if require_all and not resolved.all():
        raise ValueError(f"Unresolved longitudinal or time refinement at Lx={length:g}, axis={axis}")
    return final, np.stack((final - previous_grid, final - fewer_nodes), axis=-1), resolved


def analyse(directory):
    values, shifts, finite_values, continuum_endpoints, finite_endpoints = [], [], [], [], []
    for index, (length, (coarse, fine)) in enumerate(zip(LENGTH_SEQUENCE, GRIDS)):
        fine_rows, coarse_rows, directions, periodic_channels = [], [], [], []
        for axis in (0, 1):
            previous, _ = trace_rows(directory, index, coarse, axis, cached_only=True)
            trace, periodic = trace_rows(directory, index, fine, axis, cached_only=True)
            np.testing.assert_allclose(periodic[:, 0], periodic[:, 1], rtol=0, atol=1e-10)
            np.testing.assert_allclose(periodic[-2:, 1], np.broadcast_to(trace, (2, *trace.shape)),
                                       rtol=0, atol=1e-10)
            _, changes, _ = refined_integrals(previous, trace, length, axis)
            directions.append(changes)
            fine_rows.append(trace)
            coarse_rows.append(previous)
            periodic_channels.append(periodic[:, 1])

        projected = np.array(mixed_projections(*fine_rows, length_x=length))
        periodic = np.array(mixed_projections(*periodic_channels, length_x=length))
        for band, cutoff in enumerate(BANDS):
            nodes, reference, size = read_band(directory, index, cutoff, refined=True)
            if size == fine:
                stride = (len(TIMES[band]) - 1) // (len(nodes) - 1)
                np.testing.assert_allclose(periodic[:, 0, band, ::stride], reference.T, rtol=0, atol=1e-11)
        changes = abs(periodic - projected[:, None]).max(axis=(2, 3))
        print(f"Lx={length:g}: maximum pointwise period effects in (RX, Ricci-clock) order:\n{changes}")
        print("Largest paired longitudinal pointwise changes:",
              abs(projected - np.array(mixed_projections(*coarse_rows, length_x=length))).max(axis=(1, 2)))
        values.append([integrals(channel) for channel in projected])
        finite_values.append([integrals(channel[0]) for channel in periodic])
        shifts.append(mixed_projections(*directions, length_x=length))
        continuum_endpoints.append(np.take(projected, [0, -1], axis=-1))
        finite_endpoints.append(np.take(periodic[:, 0], [0, -1], axis=-1))

    values, finite_values = map(lambda x: np.array(x).transpose(2, 0, 1), (values, finite_values))
    shifts = np.array(shifts).transpose(2, 0, 1, 3)
    square = (2 * np.pi / np.array(LENGTH_SEQUENCE))**2
    momentum = np.linalg.inv(np.vander(square / square[0], increasing=True))[0]
    print("Largest finite-to-continuum band changes at (RX, Ricci-clock):",
          abs(values - finite_values).max(axis=(0, 1)))
    for label, endpoints in (("finite", finite_endpoints), ("transverse continuum", continuum_endpoints)):
        projected = np.einsum("q,qisb->isb", momentum, np.array(endpoints))
        print(f"{label} four-wave Ricci-clock endpoint running:", np.diff(projected[1], axis=-1).ravel())

    for count in (3, 4):
        weight = np.linalg.inv(np.vander(square[:count] / square[0], increasing=True))[0]
        fit = np.einsum("q,sqi->si", weight, values[:, :count])
        finite_fit = np.einsum("q,sqi->si", weight, finite_values[:, :count])
        grid_variation = np.einsum("q,sqi->si", abs(weight), abs(shifts[:, :count]).sum(axis=-1))
        residual, observed, _, _ = polynomial_check(BANDS, fit, grid_variation)
        print(f"{count} waves: continuum fourth-band holdout residual={residual}; variation={observed}")
        for degree in (1, 2, 3):
            cutoff = np.linalg.pinv(np.vander(BANDS / max(BANDS), degree + 1, increasing=True))[0]
            print(f"{count} waves, cutoff degree {degree}: finite={cutoff @ finite_fit}; "
                  f"transverse continuum={cutoff @ fit}; observed variation={abs(cutoff) @ grid_variation}")
    return values, shifts


def analyse_matched(directory, indices):
    values, shifts = analyse(directory)
    replacements, replacement_shifts = values.copy(), shifts.copy()
    for index in indices:
        coarse, fine = MATCHED_GRIDS[index]
        length = LENGTH_SEQUENCE[index]
        np.testing.assert_allclose(2 * np.pi / length, 2 * np.pi * 2 / (2 * length), rtol=1e-15)
        rows, long_traces, short_traces = [], [], []
        refined_size, refined_bands = LOWEST_REFINEMENT
        targeted = None
        if index == 3:
            try:
                targeted = [matched_trace(directory, index, refined_size, axis, cached_only=True,
                                          bands=refined_bands) for axis in (0, 1)]
            except FileNotFoundError:
                pass
        for axis in (0, 1):
            previous, trace = (matched_trace(directory, index, size, axis, cached_only=True)
                               for size in (coarse, fine))
            final, changes, resolved = refined_integrals(previous, trace, 2 * length, axis, require_all=False)
            if targeted is not None:
                take = list(refined_bands)
                denser, fine_changes, fine_resolved = refined_integrals(
                    trace[take], targeted[axis], 2 * length, axis, require_all=False, times=TIMES[take])
                trace = trace.copy()
                trace[take] = targeted[axis]
                final[take], changes[take], resolved[take] = denser, fine_changes, fine_resolved
            rows.append((final, changes, resolved))
            long_traces.append(trace)
            short_traces.append(trace_rows(directory, index, GRIDS[index][-1], axis, cached_only=True)[0])
        deep_size, deep_band = SHORTEST_REFINEMENT
        if targeted is not None and index == 3:
            try:
                deeper = [matched_trace(directory, index, deep_size, axis, cached_only=True,
                                        bands=(deep_band,)) for axis in (0, 1)]
            except FileNotFoundError:
                deeper = None
            if deeper is not None:
                band = slice(deep_band, deep_band + 1)
                for axis, ((final, changes, resolved), trace, denser) in enumerate(zip(rows, long_traces, deeper)):
                    final[band], changes[band], resolved[band] = refined_integrals(
                        trace[band], denser, 2 * length, axis, require_all=False, times=TIMES[band])
                    long_traces[axis] = trace.copy()
                    long_traces[axis][band] = denser
                print(f"Additional shortest-band grid pair ({refined_size}, {deep_size}).")
        integrals_by_axis, directions_by_axis, resolved_by_axis = zip(*rows)
        resolved = np.all(resolved_by_axis, axis=0)
        candidate = np.array(mixed_projections(*integrals_by_axis, length_x=2 * length, harmonic=2)).T
        candidate_shifts = np.array(mixed_projections(*directions_by_axis, length_x=2 * length,
                                                      harmonic=2)).transpose(1, 0, 2)
        replacements[resolved, index] = candidate[resolved]
        replacement_shifts[resolved, index] = candidate_shifts[resolved]
        difference = candidate - values[:, index]
        separate = (abs(shifts[:, index]) + abs(candidate_shifts)).sum(axis=-1)
        simultaneous = abs(candidate_shifts - shifts[:, index]).sum(axis=-1)
        print(f"Matched q={2*np.pi/length:.9g}, Lx={length:g}->{2*length:g}: band differences:\n{difference}")
        if targeted is not None:
            print(f"Targeted grid pair ({fine}, {refined_size}) at bands {BANDS[list(refined_bands)]}.")
        print("Substituted bands:", BANDS[resolved], "; unresolved bands:", BANDS[~resolved])
        print(f"Separate-box refinement variations:\n{separate}\nSimultaneous changes:\n{simultaneous}")
        long_kernel = np.array(mixed_projections(*long_traces, length_x=2 * length, harmonic=2))
        short_kernel = np.array(mixed_projections(*short_traces, length_x=length))
        print("Matched pointwise maximum by channel:", abs(long_kernel - short_kernel).max(axis=(1, 2)))

    square = (2 * np.pi / np.array(LENGTH_SEQUENCE))**2
    weight = np.linalg.inv(np.vander(square / square[0], increasing=True))[0]
    original = np.einsum("q,sqi->si", weight, values)
    substituted = np.einsum("q,sqi->si", weight, replacements)
    variation = np.einsum("q,sqi->si", abs(weight), abs(replacement_shifts).sum(axis=-1))
    residual, observed, _, _ = polynomial_check(BANDS, substituted, variation)
    print("Matched-box substitution shortest-band holdout residual and variation:", residual, observed)
    for degree in (1, 2, 3):
        cutoff = np.linalg.pinv(np.vander(BANDS / max(BANDS), degree + 1, increasing=True))[0]
        by_wave = np.einsum("s,q,sqi->qi", cutoff, weight, replacements - values)
        print(f"Matched cutoff degree {degree}: original={cutoff @ original}; substituted={cutoff @ substituted}; "
              f"observed variation={abs(cutoff) @ variation}; per-wave differences={by_wave}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--axis", type=int, choices=(0, 1))
    mode.add_argument("--analyse", action="store_true")
    parser.add_argument("--matched", action="store_true", help="Use the matched second harmonics in doubled boxes.")
    parser.add_argument("--matched-wave", nargs="+", type=int, choices=(1, 4),
                        help="Select the first wave, fourth wave, or both for the matched comparison.")
    parser.add_argument("--refine-lowest", action="store_true",
                        help="Refine the short bands and repeat the shortest on the finest grid.")
    args = parser.parse_args()
    if args.matched_wave and not args.matched:
        parser.error("--matched-wave requires --matched")
    if args.refine_lowest:
        if not args.matched or args.axis is None:
            parser.error("--refine-lowest requires --matched and --axis")
        size, bands = LOWEST_REFINEMENT
        matched_trace(args.checkpoint_dir, 3, size, args.axis, bands=bands)
        size, shortest = SHORTEST_REFINEMENT
        matched_trace(args.checkpoint_dir, 3, size, args.axis, bands=(shortest,))
        return
    indices = tuple(dict.fromkeys(wave - 1 for wave in args.matched_wave)) if args.matched_wave else tuple(MATCHED_GRIDS)
    if args.analyse:
        if args.matched:
            analyse_matched(args.checkpoint_dir, indices)
        else:
            analyse(args.checkpoint_dir)
        return
    if args.matched:
        for index in indices:
            for size in MATCHED_GRIDS[index]:
                matched_trace(args.checkpoint_dir, index, size, args.axis)
                print(f"axis={args.axis}, Lx={2*LENGTH_SEQUENCE[index]:g}, N={size}: ready", flush=True)
        return
    for index, length in enumerate(LENGTH_SEQUENCE):
        for size in GRIDS[index]:
            continuous, periodic = trace_rows(args.checkpoint_dir, index, size, args.axis)
            print(f"axis={args.axis}, Lx={length:g}, N={size}: "
                  f"period changes={abs(periodic[:, -1] - continuous).max(axis=(1, 2))}", flush=True)


if __name__ == "__main__":
    main()
