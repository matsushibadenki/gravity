"""Check production transverse tails and an independent shorter proper-time band."""

import argparse
from pathlib import Path

import numpy as np
from scipy.integrate import romb, simpson

from curvature_band_matching import checkpointed_result, settled
from direct_curvature_insertion import mixed_insertion
from mixed_momentum_holdout import (
    CUTOFFS, FOURTH_LENGTH, LENGTHS, band_grids, polynomial_check, third_zero_projection,
)
from restored_short_cutoff import mixed_zero_projection
from short_mixed_quadrature import mixed_projections, orientation_check
from transverse_insertion_sum import response


NEW_CUTOFF = .015
LENGTH_SEQUENCE = (*LENGTHS, FOURTH_LENGTH)
NEW_GRIDS = ((25, 29), (33, 37), (37, 41), (45, 49))
CAPS = (12, 16)
CHECK_GRID = (49, 53)
HIGH_LEVERAGE_ROWS = {
    (.015, 2): ((41, 45), 8),
    (.024, 2): ((41, 41), 16),
    (.015, 3): (CHECK_GRID, 16),
}


def production_grids(index):
    coarse, fine = NEW_GRIDS[index]
    groups = {coarse: [NEW_CUTOFF], fine: [NEW_CUTOFF]}
    for cutoff in CUTOFFS:
        size = band_grids(cutoff)[index][0][-1] if index < len(LENGTHS) else fine
        groups.setdefault(size, []).append(cutoff)
    return groups


def production_traces(directory, axis, index, size, cutoffs, *, cached_only=False, intervals=8):
    length = LENGTH_SEQUENCE[index]
    times = np.array([np.linspace(s, 2 * s, intervals + 1) for s in cutoffs])
    key = ["mixed-uv", 1, axis, float(length), size, cutoffs, list(CAPS)]
    path = directory / f"mixed-uv-{index}-axis{axis}.json"
    if intervals != 8:
        key.append(intervals)
        path = directory / f"mixed-uv-{index}-axis{axis}-{intervals}.json"
    def compute():
        if cached_only:
            raise ValueError(f"Missing production checkpoint at Lx={length}, axis={axis}, N={size}")
        return {cap: trace.reshape(times.shape).tolist()
                for cap, trace in response(size, axis, times, length, caps=CAPS).items()}

    values = checkpointed_result(path, key, compute)
    return {int(cap): np.asarray(trace) for cap, trace in values.items()}


def integrate_trace(trace, times, method):
    if method == "romberg":
        return romb(trace / times, dx=(times[-1] - times[0]) / (len(times) - 1))
    return simpson(trace / times, x=times)


def romberg_zero_projection(directory, cutoff, length, intervals=8):
    times = np.linspace(cutoff, 2 * cutoff, intervals + 1)
    path = directory / "mixed-uv-romberg-zero.json"
    key = ["mixed-romberg-zero", 1, float(cutoff), float(length), intervals]

    def compute():
        integrals = []
        for axis in (0, 1):
            results = []
            for size in (9, 13):
                momentum = (0, 0, 0, 0)
                projected = mixed_insertion(size, momentum, times, axis, length_x=length)
                full = mixed_insertion(size, momentum, times, axis, True, length_x=length) / 2
                results.append(integrate_trace(projected - full, times, "romberg"))
            np.testing.assert_allclose(*results, rtol=0, atol=1e-10)
            integrals.append(results[-1])
        return list(mixed_projections(*integrals, length_x=length))

    return np.array(checkpointed_result(path, key, compute))


def band_row(directory, axis, index, cutoff, *, method="simpson"):
    length = LENGTH_SEQUENCE[index]
    groups = production_grids(index)
    if cutoff == NEW_CUTOFF:
        coarse, fine = NEW_GRIDS[index]
    elif index == len(LENGTHS):
        coarse, fine = NEW_GRIDS[index]
        prefix = f"mixed-fourth-36-{round(1000*cutoff):03d}"
    else:
        (coarse, fine), prefix = band_grids(cutoff)[index]

    def traces_at(size):
        bands = groups[size]
        data = production_traces(directory, axis, index, size, bands, cached_only=True)
        return (data[cap][bands.index(cutoff)] for cap in CAPS)

    tail_low, trace = traces_at(fine)
    times = np.linspace(cutoff, 2 * cutoff, 9)
    integral = integrate_trace(trace, times, method)
    tail = integral - integrate_trace(tail_low, times, method)
    quadrature = integral - integrate_trace(trace[::2], times[::2], method)
    if cutoff == NEW_CUTOFF:
        _, coarse_trace = traces_at(coarse)
        coarse_value = integrate_trace(coarse_trace, times, method)
        stable = settled(coarse_trace, trace) and settled(coarse_value, integral)
        longitudinal = integral - coarse_value
    else:
        old, old_changes, stable = orientation_check(
            axis, (coarse, fine), 8, directory / f"{prefix}-axis{axis}.json",
            cutoff, length, signed_refinement=True)
        np.testing.assert_allclose(old, integrate_trace(tail_low, times, "simpson"), rtol=0, atol=1e-10)
        longitudinal = old_changes[0]
    if not (stable and settled(tail_low, trace) and settled(integral, integral - quadrature)):
        raise ValueError(f"Unresolved refinement at Lx={length}, axis={axis}, cutoff={cutoff}")
    return integral, np.array([longitudinal, tail, quadrature])


def refined_band_row(directory, axis, index, cutoff, original):
    (coarse, fine), intervals = HIGH_LEVERAGE_ROWS[cutoff, index]
    groups = production_grids(index)
    stored = production_traces(directory, axis, index, coarse, groups[coarse], cached_only=True)
    baseline = stored[16][groups[coarse].index(cutoff)]
    times = np.linspace(cutoff, 2 * cutoff, intervals + 1)

    def read(size):
        return production_traces(directory, axis, index, size, [cutoff], intervals=intervals,
                                 cached_only=True)

    if intervals == 16:
        denser = read(coarse)[16][0]
        np.testing.assert_allclose(denser[::2], baseline, rtol=0, atol=1e-10)
    else:
        denser = baseline
    fine_traces = read(fine)
    trace, lower = (fine_traces[cap][0] for cap in (16, 12))
    value = integrate_trace(trace, times, "romberg")
    shifts = original[1].copy()
    if fine != coarse:
        if not settled(denser, trace):
            raise ValueError(f"Unresolved longitudinal refinement at index={index}, cutoff={cutoff}")
        shifts[0] = value - integrate_trace(denser, times, "romberg")
    shifts[1] = value - integrate_trace(lower, times, "romberg")
    shifts[2] = value - integrate_trace(trace[::2], times[::2], "romberg")
    if not (settled(lower, trace) and settled(value, value - shifts[2])):
        raise ValueError(f"Unresolved transverse or quadrature refinement at index={index}, cutoff={cutoff}")
    return value, shifts


def analyse(directory, method="simpson", *, refined=False):
    cutoffs = np.r_[CUTOFFS, NEW_CUTOFF]
    values, shifts = [], []
    for cutoff in cutoffs:
        band, directions = [], []
        for index, length in enumerate(LENGTH_SEQUENCE):
            rows = [band_row(directory, axis, index, cutoff, method=method) for axis in (0, 1)]
            use_refinement = refined and (cutoff, index) in HIGH_LEVERAGE_ROWS
            if use_refinement:
                new_rows = [refined_band_row(directory, axis, index, cutoff, original)
                            for axis, original in enumerate(rows)]
            else:
                new_rows = rows
            integrals, variation = zip(*new_rows)
            if method == "romberg":
                intervals = HIGH_LEVERAGE_ROWS[cutoff, index][1] if use_refinement else 8
                zero = romberg_zero_projection(directory, cutoff, length, intervals)
            elif cutoff == NEW_CUTOFF or index >= 2 or (cutoff == .024 and index == 1):
                zero = third_zero_projection(directory, cutoff, length)
            else:
                zero = mixed_zero_projection(directory, length, cutoff, band_grids(cutoff)[index][0][-1])
            band.append(np.array(mixed_projections(*integrals, length_x=length)) - zero)
            if use_refinement:
                previous = np.array(mixed_projections(*(row[0] for row in rows), length_x=length))
                previous -= romberg_zero_projection(directory, cutoff, length)
                print(f"Refined cutoff={cutoff:g}, Lx={length:g}: change={band[-1] - previous}")
            projected_shifts = np.array(mixed_projections(*variation, length_x=length))
            if use_refinement and intervals == 16:
                projected_shifts[:, 2] -= zero - romberg_zero_projection(directory, cutoff, length)
            directions.append(projected_shifts)
        values.append(band)
        shifts.append(directions)
        print(f"cutoff={cutoff}: restored={np.array(band)}; cap shifts={np.array(directions)[..., 1]}")
    values, shifts = np.array(values), np.array(shifts)
    observed = abs(shifts).sum(axis=-1)
    residual, variation, _, _ = polynomial_check(cutoffs, values, observed)
    print("Fourth-band residual and observed variation at fixed momenta:", residual, variation)

    square = (2 * np.pi / np.array(LENGTH_SEQUENCE))**2
    for count in (3, 4):
        design = np.vander(square[:count] / square[0], increasing=True)
        weights = np.linalg.inv(design)[0]
        fit = np.einsum("q,sqi->si", weights, values[:, :count])
        fit_directions = np.einsum("q,sqij->sij", weights, shifts[:, :count])
        fit_variation = np.einsum("q,sqi->si", abs(weights), observed[:, :count])
        residual, variation, cubic, cubic_variation = polynomial_check(cutoffs, fit, fit_variation)
        print(f"{count} waves: fourth-band residual={residual}; observed variation={variation}")
        for degree in (1, 2):
            for size in (3, 4):
                cutoff_weights = np.linalg.pinv(
                    np.vander(cutoffs[:size] / max(cutoffs), degree + 1, increasing=True))[0]
                simultaneous = np.einsum("s,sij->ij", cutoff_weights, fit_directions[:size])
                print(f"{count} waves, {size} bands, degree {degree}: intercept={cutoff_weights @ fit[:size]}; "
                      f"observed variation={abs(cutoff_weights) @ fit_variation[:size]}; "
                      f"simultaneous changes by direction={simultaneous}")
                if (count, size, degree) == (4, 4, 2):
                    print("Quadratic intercept l1 amplification (momentum, cutoff, combined):",
                          abs(weights).sum(), abs(cutoff_weights).sum(),
                          abs(weights).sum() * abs(cutoff_weights).sum())
                    impacts = abs(cutoff_weights[:, None, None] * weights[None, :, None]
                                  * shifts[:, :, 1, :])
                    order = np.argsort(impacts.sum(axis=-1), axis=None)[-3:][::-1]
                    for band, wave in zip(*np.unravel_index(order, impacts.shape[:2])):
                        print(f"Refinement priority: cutoff={cutoffs[band]:g}, Lx={LENGTH_SEQUENCE[wave]:g}, "
                              f"Ricci-clock changes by direction={impacts[band, wave]}")
        print(f"{count} waves, four-band cubic intercept={cubic}; observed variation={cubic_variation}")


def shortest_refinement(directory, axis):
    """Refine time and longitudinal resolution separately at the lowest wave."""
    index = len(LENGTH_SEQUENCE) - 1
    cutoff = NEW_CUTOFF
    if axis is not None:
        for size in CHECK_GRID:
            production_traces(directory, axis, index, size, [cutoff], intervals=16)
        return

    coarse = CHECK_GRID[0]
    times = np.linspace(cutoff, 2 * cutoff, 17)
    rows = []
    for direction in (0, 1):
        original_bands = production_grids(index)[coarse]
        original = production_traces(directory, direction, index, coarse, original_bands,
                                     cached_only=True)[16][original_bands.index(cutoff)]
        denser, finer = (production_traces(directory, direction, index, size, [cutoff],
                                          cached_only=True, intervals=16)[16][0]
                         for size in CHECK_GRID)
        np.testing.assert_allclose(denser[::2], original, rtol=0, atol=1e-10)
        if not settled(denser, finer):
            raise ValueError(f"Unresolved 49-to-53-point trace refinement in orientation {direction}")
        old_simpson = integrate_trace(original, times[::2], "simpson")
        old_romberg = integrate_trace(original, times[::2], "romberg")
        new_romberg, fine_romberg = (integrate_trace(trace, times, "romberg")
                                     for trace in (denser, finer))
        rows.append([old_simpson, old_romberg, new_romberg, fine_romberg])

    measured = np.array(mixed_projections(*np.array(rows), length_x=FOURTH_LENGTH)).T
    zero8, zero16 = (romberg_zero_projection(directory, cutoff, FOURTH_LENGTH, steps)
                     for steps in (8, 16))
    corrected = measured - [third_zero_projection(directory, cutoff, FOURTH_LENGTH), zero8, zero16, zero16]
    print("Restored [49x9 Simpson, 49x9 Romberg, 49x17 Romberg, 53x17 Romberg]:", corrected)
    print("Paired changes [rule at 9 nodes, extra time nodes, extra spatial sites]:", np.diff(corrected, axis=0))
    square = (2 * np.pi / np.array(LENGTH_SEQUENCE))**2
    wave_weight = np.linalg.inv(np.vander(square / square[0], increasing=True))[0, -1]
    cutoffs = np.r_[CUTOFFS, NEW_CUTOFF]
    for degree in (1, 2):
        band_weight = np.linalg.pinv(np.vander(cutoffs / max(cutoffs), degree + 1, increasing=True))[0, -1]
        print(f"Degree {degree} cutoff intercept shift from replacing this Romberg row:",
              wave_weight * band_weight * (corrected[-1] - corrected[1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument("--quadrature", choices=("simpson", "romberg"), default="simpson")
    refinement = parser.add_mutually_exclusive_group()
    refinement.add_argument("--refined-fit", action="store_true",
                           help="Use the independently refined Romberg rows.")
    refinement.add_argument("--refine-shortest", action="store_true",
                            help="Use 17 time nodes and two finer grids for the shortest band at the lowest momentum.")
    refinement.add_argument("--refine-leverage", action="store_true",
                            help="Generate the two high-leverage refinements at Lx=3.")
    task = parser.add_mutually_exclusive_group(required=True)
    task.add_argument("--axis", type=int, choices=(0, 1))
    task.add_argument("--analyse", action="store_true")
    args = parser.parse_args()
    if args.refined_fit and (not args.analyse or args.quadrature != "romberg"):
        parser.error("--refined-fit requires --analyse --quadrature romberg")
    if args.refine_leverage:
        if args.axis is None:
            parser.error("--refine-leverage requires --axis")
        for (cutoff, index), ((_, fine), intervals) in HIGH_LEVERAGE_ROWS.items():
            if index == 2:
                production_traces(args.checkpoint_dir, args.axis, index, fine, [cutoff], intervals=intervals)
        return
    if args.refine_shortest:
        shortest_refinement(args.checkpoint_dir, args.axis)
        return
    if args.analyse:
        analyse(args.checkpoint_dir, args.quadrature, refined=args.refined_fit)
        return
    for index, length in enumerate(LENGTH_SEQUENCE):
        for size, cutoffs in production_grids(index).items():
            values = production_traces(args.checkpoint_dir, args.axis, index, size, cutoffs)
            print(f"axis={args.axis} Lx={length:g} N={size}: bands={cutoffs}; "
                  f"max pointwise cap 12-to-16 changes={abs(values[16]-values[12]).max(axis=1)}", flush=True)


if __name__ == "__main__":
    main()
