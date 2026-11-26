"""Nested quadrature of the short, subtracted mixed heat response."""

import argparse
from pathlib import Path

import numpy as np
from scipy.integrate import simpson

from transverse_insertion_sum import response
from curvature_band_matching import LENGTH, checkpointed_result, settled


def check(axis, size, intervals, checkpoint=None, cutoff=0.035, length_x=LENGTH, harmonic=1,
          *, caps=(8, 12)):
    times = np.linspace(cutoff, 2 * cutoff, intervals + 1)
    key = ["mixed", 1, axis, size, intervals, float(times[0]), float(times[-1])]
    if length_x != LENGTH:
        key.append(length_x)
    if harmonic != 1:
        key.extend(["harmonic", harmonic])
    default_caps = caps == (8, 12)
    if not default_caps:
        key.extend(["caps", list(caps)])
    stored_caps = (3, 5, *caps) if default_caps else caps
    traces = checkpointed_result(checkpoint, key,
                               lambda: {int(cap): trace.tolist() for cap, trace
                                        in response(size, axis, times, length_x, harmonic,
                                                    caps=stored_caps).items()})
    traces = {int(cap): np.asarray(trace) for cap, trace in traces.items()}
    lower, upper = caps
    integrand = traces[upper] / times
    levels = [simpson(integrand[::stride], x=times[::stride])
              for stride in (4, 2, 1)]
    transverse = simpson(traces[lower] / times, x=times)
    print(f"axis={axis} N={size}: Simpson levels={levels}; "
          f"transverse change={levels[-1]-transverse:.6g}; "
          f"endpoints={traces[upper][[0,-1]]}", flush=True)
    return levels, transverse, traces[upper]


def mixed_projections(spatial_integral, temporal_integral, length_x=LENGTH, harmonic=1, *, period=LENGTH):
    # The fourth derivative contributes 2! * 2! times the action coefficient.
    spatial, temporal = -np.array([spatial_integral, temporal_integral]) / (8 * period**3 * length_x)
    q2 = (2 * np.pi * harmonic / length_x)**2
    return -temporal / (3 * q2), (temporal - spatial) / q2


def orientation_check(axis, sizes, intervals, checkpoint, cutoff, length_x=LENGTH, harmonic=1,
                      *, signed_refinement=False, caps=(8, 12)):
    values = [check(axis, size, intervals, checkpoint, cutoff, length_x, harmonic, caps=caps)
              for size in sizes]
    levels, transverse, fine = values[-1]
    quadrature_ok = settled(levels[-2], levels[-1])
    transverse_ok = settled(transverse, levels[-1])
    longitudinal_ok = (len(values) > 1 and
                       settled(values[-2][0][-1], levels[-1]) and
                       settled(values[-2][2], fine))
    print(f"quadrature_ok={quadrature_ok}, transverse_ok={transverse_ok}, "
          f"longitudinal_ok={longitudinal_ok}", flush=True)
    changes = np.array([levels[-1] - values[-2][0][-1] if len(values) > 1 else np.inf,
                        levels[-1] - transverse, levels[-1] - levels[-2]])
    observed = changes if signed_refinement else abs(changes).sum()
    return levels[-1], observed, quadrature_ok and transverse_ok and longitudinal_ok


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    orientation = parser.add_mutually_exclusive_group(required=True)
    orientation.add_argument("--axis", type=int, choices=(0, 1))
    orientation.add_argument("--match", action="store_true",
                             help="Check both orientations and compare the mixed band coefficients.")
    parser.add_argument("--sizes", type=int, nargs="+", default=(17, 21))
    parser.add_argument("--intervals", type=int, choices=(8, 16, 32), default=8)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--cutoff", type=float, default=0.035, help="Lower proper time of the dyadic band.")
    parser.add_argument("--length-x", type=float, default=LENGTH)
    parser.add_argument("--harmonic", type=int, default=1)
    parser.add_argument("--caps", type=int, nargs=2, metavar=("LOWER", "UPPER"), default=(8, 12))
    args = parser.parse_args()
    if not 0 < args.caps[0] < args.caps[1]:
        parser.error("--caps must be positive and increasing")
    if args.harmonic < 1 or any(4 * args.harmonic >= n for n in args.sizes):
        parser.error("harmonic must be positive and grids must resolve twice the harmonic")
    if not np.isfinite(args.length_x) or args.length_x <= 0:
        parser.error("--length-x must be positive and finite")
    if not np.isfinite(args.cutoff) or args.cutoff <= 0:
        parser.error("--cutoff must be positive and finite")
    if any(n < 5 or n % 2 == 0 for n in args.sizes) or list(args.sizes) != sorted(set(args.sizes)):
        parser.error("--sizes must contain strictly increasing odd grids of at least 5 points")
    axes = (0, 1) if args.match else (args.axis,)
    bands = [orientation_check(axis, args.sizes, args.intervals, args.checkpoint, args.cutoff,
                               args.length_x, args.harmonic, caps=tuple(args.caps))
             for axis in axes]
    if args.match and all(stable for _, _, stable in bands):
        rx, ricci_clock = mixed_projections(
            *(integral for integral, _, _ in bands), length_x=args.length_x, harmonic=args.harmonic)
        spatial_shift, temporal_shift = [shift for _, shift, _ in bands]
        # Opposite signs maximize the change in the Ricci projection, which is a difference.
        rx_shift, ricci_shift = mixed_projections(
            spatial_shift, -temporal_shift, length_x=args.length_x, harmonic=args.harmonic)
        print(f"Finite-band mixed projections: RX={rx:.12g}, RicTT={ricci_clock:.12g}")
        print(f"Propagated observed refinement shifts: RX={abs(rx_shift):.4g}, "
              f"RicTT={abs(ricci_shift):.4g}")


if __name__ == "__main__":
    main()
