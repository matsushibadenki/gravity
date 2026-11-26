"""Reuse curvature operator samples across dyadic proper-time bands."""

import argparse
import json
from pathlib import Path

import numpy as np

from curvature_band_matching import LENGTH, checkpointed_result
from pure_transverse_insertion_sum import response


def band_batch(size, shear, cutoffs, harmonic, length, caps):
    quadratures = [np.polynomial.legendre.leggauss(order) for order in (8, 16)]
    times = [cutoff * (nodes + 3) / 2 for cutoff in cutoffs for nodes, _ in quadratures]
    splits = np.cumsum([len(nodes) for nodes in times])[:-1]
    traces = response(size, shear, np.concatenate(times), harmonic, length, caps)
    bands = [{} for _ in cutoffs]
    for cap, trace in traces.items():
        parts = np.split(trace, splits)
        for i, (cutoff, band) in enumerate(zip(cutoffs, bands)):
            band[cap] = [
                -cutoff * (weights @ (parts[index] / times[index])) / (8 * LENGTH**3 * length)
                for index, (_, weights) in zip((2 * i, 2 * i + 1), quadratures)
            ]
    return bands


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--sizes", type=int, nargs="+", default=(33, 37))
    parser.add_argument("--cutoffs", type=float, nargs="+", default=(0.035, 0.028, 0.021))
    parser.add_argument("--harmonics", type=int, nargs="+", choices=(1, 2, 3, 4), default=(1, 2, 3))
    parser.add_argument("--length-x", type=float, default=4.2)
    args = parser.parse_args()
    if not np.isfinite(args.length_x) or args.length_x <= 0:
        parser.error("length-x must be positive and finite")
    if len(set(args.cutoffs)) != len(args.cutoffs) or any(
            not np.isfinite(s) or s <= 0 for s in args.cutoffs):
        parser.error("cutoffs must be distinct, positive and finite")
    if any(n < 7 or n % 2 == 0 for n in args.sizes):
        parser.error("sizes must be odd and at least 7")
    length, caps = args.length_x, (8, 12)
    for harmonic in args.harmonics:
        for shear in (False, True):
            for size in args.sizes:
                cache = json.loads(args.checkpoint.read_text()) if args.checkpoint.exists() else {}
                keys = [[1, length, s, harmonic, shear, size, caps] for s in args.cutoffs]
                missing = [key for key in keys if json.dumps(key) not in cache]
                if missing:
                    bands = band_batch(size, shear, [key[2] for key in missing], harmonic, length, caps)
                    for key, band in zip(missing, bands):
                        checkpointed_result(args.checkpoint, key, lambda band=band: band)
                print(f"harmonic={harmonic} shear={shear} N={size}: "
                      f"saved {len(missing)} bands", flush=True)


if __name__ == "__main__":
    main()
