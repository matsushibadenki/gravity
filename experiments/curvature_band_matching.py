"""Check integrated pure-curvature responses and their momentum separation."""

import argparse
import json
from pathlib import Path

import numpy as np

from pure_transverse_insertion_sum import response, zero_projection_trace_shift


LENGTH = 1.8
TOLERANCE = 1e-3


def band_response(size, shear, cutoff, harmonic, length_x=LENGTH, caps=(3, 5, 8)):
    quadratures = [np.polynomial.legendre.leggauss(order) for order in (8, 16)]
    times = np.concatenate([cutoff * (nodes + 3) / 2 for nodes, _ in quadratures])
    traces = response(size, shear, times, harmonic, length_x, caps)
    integrated = {}
    for cap, trace in traces.items():
        integrated[cap] = [
            -cutoff * (weights @ (part / (cutoff * (nodes + 3) / 2))) / (8 * LENGTH**3 * length_x)
            for (nodes, weights), part in zip(quadratures, np.split(trace, [8]))
        ]
    return integrated


def settled(first, second):
    return np.allclose(first, second, rtol=TOLERANCE, atol=1e-8)


def checkpointed_result(path, key, compute):
    if path is None:
        return compute()
    cache = json.loads(path.read_text()) if path.exists() else {}
    encoded = json.dumps(key)
    if encoded not in cache:
        cache[encoded] = compute()
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(cache, indent=2) + "\n")
        temporary.replace(path)
    return cache[encoded]


def checkpointed_band(path, length_x, cutoff, harmonic, shear, size, caps=(3, 5, 8)):
    key = [1, length_x, cutoff, harmonic, shear, size]
    if caps != (3, 5, 8):
        key.append(caps)
    cache = checkpointed_result(path, key, lambda: band_response(size, shear, cutoff, harmonic, length_x, caps))
    return {int(cap): pair for cap, pair in cache.items()}


def band_refinement_directions(values, lower, upper):
    """Signed changes from longitudinal, transverse, and quadrature refinement."""
    coarse, fine = values[-2:]
    return np.array([fine[upper][1] - coarse[upper][1],
                     fine[upper][1] - fine[lower][1],
                     fine[upper][1] - fine[upper][0]])


def band_resolution(values, lower, upper):
    """Sum the magnitudes of the three observed refinement shifts."""
    return np.abs(band_refinement_directions(values, lower, upper)).sum()


def common_volume_shift(length_x):
    # The stored conformal bands subtract 24 times the primed flat trace.
    # Restoring its missing unit lowers that trace derivative by 24.
    return 6 * np.log(2) / (LENGTH**3 * length_x)


def momentum_projections(conformal, shear, square):
    einstein, quartic = np.linalg.solve(
        np.column_stack((3 * square, square**2)), conformal)
    ricci = (shear + einstein * square) / square**2
    return einstein, (quartic - 6 * ricci) / 18, ricci


def zero_projection_band_shift(size, shear, cutoff, harmonic, length_x):
    nodes, weights = np.polynomial.legendre.leggauss(16)
    times = cutoff * (nodes + 3) / 2
    delta = zero_projection_trace_shift(size, shear, times, harmonic, length_x)
    return float(-cutoff * (weights @ (delta / times)) / (8 * LENGTH**3 * length_x))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cutoff", type=float, default=0.035,
                        help="Lower proper time for the band [cutoff, 2*cutoff].")
    parser.add_argument("--length-x", type=float, default=LENGTH)
    parser.add_argument("--sizes", type=int, nargs="+", default=(13, 17, 21))
    parser.add_argument("--compare-zero-projection", action="store_true",
                        help="Diagnose the change caused by dropping the zero-mode projection.")
    parser.add_argument("--checkpoint", type=Path, help="Save each completed band and resume from it.")
    parser.add_argument("--transverse-bounds", type=int, nargs=2, default=(5, 8))
    args = parser.parse_args()
    lower, upper = args.transverse_bounds
    if not 0 < lower < upper:
        parser.error("--transverse-bounds requires increasing positive limits")
    caps = (3, 5, 8) if (lower, upper) == (5, 8) else (lower, upper)
    if not np.isfinite(args.length_x) or args.length_x <= 0:
        parser.error("--length-x must be positive and finite")
    if not np.isfinite(args.cutoff) or args.cutoff <= 0:
        parser.error("--cutoff must be positive and finite")
    if len(args.sizes) < 2 or sorted(set(args.sizes)) != list(args.sizes):
        parser.error("--sizes needs at least two strictly increasing grid sizes")
    if any(n < 5 or n % 2 == 0 for n in args.sizes):
        parser.error("--sizes must contain odd grid sizes of at least 5 points")
    cutoff, sizes = args.cutoff, args.sizes
    responses = {}
    resolution = {}
    for shear in (True, False):
        for harmonic in (1, 2):
            values = []
            for n in sizes:
                value = checkpointed_band(args.checkpoint, args.length_x, cutoff, harmonic, shear, n, caps)
                values.append(value)
                print(f"Lx={args.length_x:g}, harmonic={harmonic}, shear={shear}, "
                      f"N={n}: band={value[upper][1]:.12g}", flush=True)
            stable = (settled(values[-2][upper][1], values[-1][upper][1])
                      and settled(values[-1][lower][1], values[-1][upper][1])
                      and settled(*values[-1][upper]))
            responses[harmonic, shear] = values[-1][upper][1], stable
            resolution[harmonic, shear] = band_resolution(values, lower, upper)
            print(f"s={cutoff:g}, harmonic={harmonic}, shear={shear}: "
                  f"longitudinal={[v[upper][1] for v in values]}, "
                  f"transverse={values[-1][lower][1]:.10g}, "
                  f"quadrature={values[-1][upper][0]:.10g}, {stable=}", flush=True)
    if not all(stable for _, stable in responses.values()):
        print("Resolution gate failed. Keeping the same lower proper-time cutoff.", flush=True)
        return
    stored_conformal = np.array([responses[harmonic, False][0] for harmonic in (1, 2)])
    volume_shift = common_volume_shift(args.length_x)
    conformal = stored_conformal + volume_shift
    print(f"Common flat volume subtraction shifts both conformal bands by {volume_shift:.12g}",
          flush=True)
    square = (2 * np.pi / args.length_x)**2 * np.array([1, 4])
    shear = np.array([responses[harmonic, True][0] for harmonic in (1, 2)])
    quartic = (conformal + 3 * shear) / square**2
    shifts = np.array([resolution[h, False] + 3 * resolution[h, True] for h in (1, 2)]) / square**2
    print("Einstein-free quartic projections:", quartic, flush=True)
    print("Observed refinement shifts propagated to those projections:", shifts, flush=True)
    einstein, scalar_square, ricci_square = momentum_projections(conformal, shear, square)
    print(f"Finite-band two-momentum projections: {einstein=}, {scalar_square=}, "
          f"{ricci_square=}", flush=True)
    if args.compare_zero_projection:
        shifts = []
        for is_shear in (False, True):
            row = []
            for harmonic in (1, 2):
                key = ["zero-projection", 1, args.length_x, cutoff, harmonic, is_shear, sizes[-1]]
                row.append(checkpointed_result(args.checkpoint, key, lambda: zero_projection_band_shift(
                    sizes[-1], is_shear, cutoff, harmonic, args.length_x)))
            shifts.append(np.array(row))
        conformal_full, shear_full = stored_conformal - shifts[0], shear - shifts[1]
        print("Unprojected Einstein-free quartic projections:",
              (conformal_full + 3 * shear_full) / square**2, flush=True)
        print("Unprojected projections (Einstein, scalar squared, Ricci squared):",
              momentum_projections(conformal_full, shear_full, square), flush=True)
    if not settled(*ricci_square):
        print("Momentum derivative expansion gate failed. Keeping the cutoff.", flush=True)
        return


if __name__ == "__main__":
    main()
