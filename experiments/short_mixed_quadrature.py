"""Nested quadrature of the short, subtracted mixed heat response."""

import argparse
from pathlib import Path

import numpy as np
from scipy.integrate import simpson

from transverse_insertion_sum import response
from curvature_band_matching import checkpointed_result, settled


def check(axis, size, intervals, checkpoint=None, cutoff=0.035):
    times = np.linspace(cutoff, 2 * cutoff, intervals + 1)
    key = ["mixed", 1, axis, size, intervals, float(times[0]), float(times[-1])]
    traces = checkpointed_result(checkpoint, key,
                               lambda: {int(cap): trace.tolist() for cap, trace
                                        in response(size, axis, times).items()})
    traces = {int(cap): np.asarray(trace) for cap, trace in traces.items()}
    integrand = traces[12] / times
    levels = [simpson(integrand[::stride], x=times[::stride])
              for stride in (4, 2, 1)]
    transverse = simpson(traces[8] / times, x=times)
    print(f"axis={axis} N={size}: Simpson levels={levels}; "
          f"transverse change={levels[-1]-transverse:.6g}; "
          f"endpoints={traces[12][[0,-1]]}", flush=True)
    return levels, transverse, traces[12]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--axis", type=int, choices=(0, 1), required=True)
    parser.add_argument("--sizes", type=int, nargs="+", default=(17, 21))
    parser.add_argument("--intervals", type=int, choices=(8, 16, 32), default=8)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--cutoff", type=float, default=0.035, help="Lower proper time of the dyadic band.")
    args = parser.parse_args()
    if not np.isfinite(args.cutoff) or args.cutoff <= 0:
        parser.error("--cutoff must be positive and finite")
    if any(n < 5 or n % 2 == 0 for n in args.sizes) or list(args.sizes) != sorted(set(args.sizes)):
        parser.error("--sizes must contain strictly increasing odd grids of at least 5 points")
    values = [check(args.axis, size, args.intervals, args.checkpoint, args.cutoff) for size in args.sizes]
    levels, transverse, fine = values[-1]
    quadrature_ok = settled(levels[-2], levels[-1])
    transverse_ok = settled(transverse, levels[-1])
    longitudinal_ok = (len(values) > 1 and
                       settled(values[-2][0][-1], levels[-1]) and
                       settled(values[-2][2], fine))
    print(f"quadrature_ok={quadrature_ok}, transverse_ok={transverse_ok}, "
          f"longitudinal_ok={longitudinal_ok}", flush=True)


if __name__ == "__main__":
    main()
