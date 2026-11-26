"""Measure finite-box shifts while keeping the external physical momentum fixed."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import simpson

from curvature_band_matching import (LENGTH, band_refinement_directions, band_resolution, checkpointed_result,
                                     common_volume_shift, momentum_projections, settled,
                                     zero_projection_band_shift)
from pure_transverse_insertion_sum import zero_projection_trace_shift
from direct_curvature_insertion import mixed_insertion
from short_mixed_quadrature import mixed_projections, orientation_check
from curvature_cutoff_extrapolation import band_projection, intercept_weights
from curvature_momentum_validation import (REFERENCE, fixed_box_comparison,
                                           wave_rows)


def pure_wave(cache, length, cutoff, harmonic, sizes, *, signed_refinement=False):
    responses, shifts = [], []
    for shear in (False, True):
        grids = []
        for n in sizes:
            key = json.dumps([1, length, cutoff, harmonic, shear, n, [8, 12]])
            if key not in cache:
                raise ValueError(f"Missing checkpoint row {key}")
            grids.append({int(cap): band for cap, band in cache[key].items()})
        coarse, fine = grids
        if not (settled(coarse[12][1], fine[12][1])
                and settled(fine[8][1], fine[12][1])
                and settled(*fine[12])):
            raise ValueError(f"Unresolved grid at Lx={length}, sigma={cutoff}, shear={shear}")
        responses.append(fine[12][1])
        refinement = band_refinement_directions if signed_refinement else band_resolution
        shifts.append(refinement(grids, 8, 12))
    responses[0] += common_volume_shift(length)
    return np.array(responses), np.array(shifts)


def calculate_pure_zero(directory):
    bands = (.024, .021)
    nodes, weights = np.polynomial.legendre.leggauss(16)
    times = np.array([sigma * (nodes + 3) / 2 for sigma in bands])
    for suffix, short, long in (("", (37, 41), (53, 53)), ("-coarse", (33, 37), (49, 49))):
        path = directory / f"pure-matched-zero-sector{suffix}.json"
        for length, harmonic, sizes in ((4.2, 3, short), (5.6, 4, long)):
            for shear in (False, True):
                for size in dict.fromkeys(sizes):
                    indices = [i for i, n in enumerate(sizes) if n == size]
                    key = ["pure-zero-matched", 1, length, harmonic, shear, size,
                           [bands[i] for i in indices]]

                    def compute():
                        traces = zero_projection_trace_shift(
                            size, shear, times[indices].ravel(), harmonic, length)
                        return [float(-bands[i] * (weights @ (trace / times[i]))
                                      / (8 * LENGTH**3 * length))
                                for i, trace in zip(indices, traces.reshape(-1, 16))]

                    result = checkpointed_result(path, key, compute)
                    print(length, harmonic, shear, size, result, flush=True)


def restore_pure_zero_sector(cache, response, length, harmonic, n, sigma):
    bands = [.024, .021] if length == 5.6 else [sigma]
    shifts = np.array([
        cache[json.dumps(["pure-zero-matched", 1, length, harmonic, shear, n, bands])][bands.index(sigma)]
        for shear in (False, True)
    ])
    # The checkpoint shift compares the legacy primed subtraction with
    # the unprojected subtraction. The input uses the common subtraction.
    shifts[0] += common_volume_shift(length)
    return response - shifts


def show_pure(directory, restore_zero=False):
    cache = {}
    for name in ("curvature-third-wave", "curvature-fixed-box", "curvature-low-wave",
                 "curvature-matched-56"):
        cache.update(json.loads((directory / f"{name}.json").read_text()))
    if restore_zero:
        sector = json.loads((directory / "pure-matched-zero-sector.json").read_text())
        sector_coarse = json.loads((directory / "pure-matched-zero-sector-coarse.json").read_text())
    wave = 2 * np.pi * 3 / 4.2
    np.testing.assert_allclose(wave, 2 * np.pi * 4 / 5.6)
    for sigma, sizes in ((.024, (33, 37)), (.021, (37, 41))):
        a, ae = pure_wave(cache, 4.2, sigma, 3, sizes)
        b, be = pure_wave(cache, 5.6, sigma, 4, (49, 53))
        weights = np.array([1, 3]) / wave**4
        print(f"Pure sigma={sigma}, q={wave}: Lx=4.2 {a}, Lx=5.6 {b}")
        print(f"Einstein-free difference={weights @ (b-a):.12g}; "
              f"observed shift={weights @ (be+ae):.12g}")

        if restore_zero:
            a_full = restore_pure_zero_sector(sector, a, 4.2, 3, sizes[-1], sigma)
            b_full = restore_pure_zero_sector(sector, b, 5.6, 4, 53, sigma)
            def coarse_response(length, harmonic, size):
                raw = [cache[json.dumps([1, length, sigma, harmonic, shear, size, [8, 12]])]["12"][1]
                       for shear in (False, True)]
                raw[0] += common_volume_shift(length)
                return restore_pure_zero_sector(sector_coarse, np.array(raw), length, harmonic, size, sigma)

            a_coarse = coarse_response(4.2, 3, sizes[0])
            b_coarse = coarse_response(5.6, 4, 49)
            variation = weights @ (abs(a_full-a_coarse) + abs(b_full-b_coarse))
            print(f"Unprojected diagnostic: Lx=4.2 {a_full}, Lx=5.6 {b_full}; "
                  f"Einstein-free difference={weights @ (b_full-a_full):.12g}; "
                  f"observed longitudinal shift={variation:.12g}")


def mixed_wave(directory, length, harmonic, sigma, sizes, prefix, *, paired=False, signed=False):
    """Return band projections and optionally the paired shifts by direction."""
    rows = [orientation_check(axis, sizes, 8, directory / f"{prefix}-axis{axis}.json",
                              sigma, length, harmonic, signed_refinement=True) for axis in (0, 1)]
    if not all(stable for _, _, stable in rows):
        raise ValueError(f"Unresolved mixed refinement at Lx={length}, sigma={sigma}")
    integrals, shifts, _ = zip(*rows)
    projections = np.array(mixed_projections(*integrals, length_x=length, harmonic=harmonic))
    spatial, temporal = np.abs(shifts).sum(axis=1)
    observed = np.abs(mixed_projections(spatial, -temporal, length_x=length,
                                       harmonic=harmonic))
    if paired or signed:
        directions = np.array(mixed_projections(*shifts, length_x=length, harmonic=harmonic))
        return projections, observed, directions if signed else abs(directions).sum(axis=1)
    return projections, observed


def mixed_zero_shifts(directory, length, harmonic, size, axis):
    cutoffs = (.024, .021)
    times = np.array([np.linspace(sigma, 2 * sigma, 9) for sigma in cutoffs])
    key = ["mixed-matched-zero", 1, length, harmonic, size, axis, list(cutoffs)]

    def compute():
        momentum = (0, 0, 0, 0)
        steps = times.ravel()
        projected = mixed_insertion(size, momentum, steps, axis, length_x=length,
                                    harmonic=harmonic)
        full = mixed_insertion(size, momentum, steps, axis, True, length, harmonic) / 2
        delta = (projected - full).reshape(times.shape)
        return [float(simpson(row / nodes, x=nodes)) for row, nodes in zip(delta, times)]

    return checkpointed_result(directory / "mixed-matched-zero-sector.json", key, compute)


def calculate_mixed_zero(directory):
    for length, harmonic, size in ((1.8, 1, 25), (3.6, 2, 45)):
        for axis in (0, 1):
            print(length, harmonic, size, axis,
                  mixed_zero_shifts(directory, length, harmonic, size, axis), flush=True)


def show_mixed(directory, restore_zero=False):
    short_values, long_values = [], []
    short_restored, long_restored = [], []
    cutoffs = np.array([.024, .021])
    for i, sigma in enumerate(cutoffs):
        a, ae = mixed_wave(directory, 1.8, 1, sigma, (21, 25), f"mixed-{int(round(1000*sigma)):03d}")
        b, be = mixed_wave(directory, 3.6, 2, sigma, (41, 45), "mixed-matched-36")
        print(f"Mixed sigma={sigma}, q={2*np.pi/1.8}: Lx=1.8 {a}, Lx=3.6 {b}")
        print(f"Matched-wave difference={b-a}; observed shifts={ae+be}")
        if restore_zero:
            def zero_change(length, harmonic, size):
                shifts = [mixed_zero_shifts(directory, length, harmonic, size, axis)[i]
                          for axis in (0, 1)]
                return np.array(mixed_projections(*shifts, length_x=length, harmonic=harmonic))

            a_full = a - zero_change(1.8, 1, 25)
            b_full = b - zero_change(3.6, 2, 45)
            short_restored.append(a_full)
            long_restored.append(b_full)
            print(f"Unprojected mixed diagnostic: Lx=1.8 {a_full}, Lx=3.6 {b_full}; "
                  f"matched-wave difference={b_full-a_full}")
        short_values.append(a)
        long_values.append(b)
    weights = intercept_weights(cutoffs)
    print(f"Two-band linear intercepts: Lx=1.8 {weights @ short_values}; "
          f"Lx=3.6 {weights @ long_values}")
    if restore_zero:
        print(f"Restored two-band intercepts: Lx=1.8 {weights @ short_restored}; "
              f"Lx=3.6 {weights @ long_restored}")
    fine, error = mixed_wave(directory, 1.8, 1, .018, (25, 29), "mixed-018")
    print(f"Mixed Lx=1.8 sigma=0.018: {fine}; observed shifts={error}")
    print(f"Fixed-box cutoff difference (0.018 minus 0.021): {fine-short_values[-1]}")


def show_cutoff(directory):
    reference = {}
    for name in ("curvature-fixed-box", "curvature-low-wave"):
        reference.update(json.loads((directory / f"{name}.json").read_text()))
    coarse, fine, coarse_shift, fine_shift, _, _ = fixed_box_comparison(reference)
    shortest, shortest_shift = band_projection(reference, 4.2, .021, (37, 41), (8, 12))

    longer = {}
    for name in ("curvature-long-56", "curvature-long-56-028"):
        longer.update(json.loads((directory / f"{name}.json").read_text()))
    cutoffs = np.array([.028, .024, .021])
    long_values, long_shifts = zip(*[
        band_projection(longer, 5.6, cutoff, pair, (8, 12))
        for cutoff, pair in zip(cutoffs, ((41, 45), (49, 53), (49, 53)))
    ])
    for length, values, shifts in ((4.2, [coarse, fine, shortest],
                                   [coarse_shift, fine_shift, shortest_shift]),
                                  (5.6, long_values, long_shifts)):
        for start in (0, 1):
            weights = intercept_weights(cutoffs[start:])
            print(f"Lx={length}, cutoffs={cutoffs[start:]}: "
                  f"intercept={weights @ values[start:]}; "
                  f"observed shifts={abs(weights) @ shifts[start:]}")
    print("Two-wave momentum fits; the intercept comparison is a cutoff diagnostic.")


def show_restored_cutoff(directory):
    cache = {}
    for name in ("curvature-fixed-box", "curvature-low-wave", "curvature-long-56"):
        cache.update(json.loads((directory / f"{name}.json").read_text()))
    path = directory / "pure-low-wave-zero-sector.json"
    cutoffs = (.024, .021)
    for length in (4.2, 5.6):
        projected, full = [], []
        q2 = (2 * np.pi / length)**2 * np.array([1, 4])
        momentum_weights = intercept_weights(q2)
        for sigma in cutoffs:
            if length == 4.2 and sigma == .024:
                responses = REFERENCE.copy()
                sizes = (37, 37)
            elif length == 4.2:
                responses = np.column_stack([wave_rows(cache, sigma, h, (37, 41))[0]
                                             for h in (1, 2)])
                sizes = (41, 41)
            else:
                responses = np.column_stack([pure_wave(cache, length, sigma, h, (49, 53))[0]
                                             for h in (1, 2)])
                responses[0] -= common_volume_shift(length)
                sizes = (53, 53)
            primed = responses.copy()
            primed[0] += common_volume_shift(length)
            unprimed = responses.copy()
            for row, shear in enumerate((False, True)):
                for h, size in enumerate(sizes, 1):
                    key = ["pure-low-wave-zero", 1, length, sigma, h, shear, size]
                    shift = checkpointed_result(path, key, lambda: zero_projection_band_shift(
                        size, shear, sigma, h, length))
                    unprimed[row, h-1] -= shift
            for data, collection in ((primed, projected), (unprimed, full)):
                einstein, scalar, ricci = momentum_projections(*data, q2)
                collection.append([sigma * einstein, momentum_weights @ scalar,
                                   momentum_weights @ ricci])
            print(f"Lx={length} sigma={sigma}: projected={projected[-1]}, full={full[-1]}",
                  flush=True)
        weights = intercept_weights(np.array(cutoffs))
        print(f"Cutoff intercept, Lx={length}: projected={weights @ projected}, "
              f"unprojected={weights @ full}", flush=True)
    print("Two-wave, two-band diagnostic with a common flat volume reference.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument("--part", choices=("pure", "mixed", "cutoff", "zero", "mixed-zero", "restored-cutoff"), required=True)
    parser.add_argument("--restore-zero", action="store_true", help="Compare with the corresponding global zero sector restored.")
    args = parser.parse_args()
    try:
        if args.part == "pure":
            show_pure(args.checkpoint_dir, args.restore_zero)
        elif args.part == "mixed":
            show_mixed(args.checkpoint_dir, args.restore_zero)
        else:
            {"cutoff": show_cutoff, "zero": calculate_pure_zero,
             "mixed-zero": calculate_mixed_zero, "restored-cutoff": show_restored_cutoff}[args.part](args.checkpoint_dir)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
