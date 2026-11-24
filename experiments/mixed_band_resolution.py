"""Gate mixed heat-response bands on independent lattice and quadrature checks."""

import numpy as np
from scipy.integrate import simpson, trapezoid

from transverse_insertion_sum import response


def main():
    times = np.linspace(0.035, 0.14, 7)
    for axis in (0, 1):
        previous = None
        for size in (13, 17, 21):
            traces = response(size, axis, times)
            for start, stop in ((2, 7), (0, 3)):
                sample = slice(start, stop)
                nodes = times[sample]
                integrand = traces[12][sample] / nodes
                integral = simpson(integrand, x=nodes)
                quadrature = trapezoid(integrand, x=nodes)
                transverse = simpson(traces[8][sample] / nodes, x=nodes)
                longitudinal = (np.nan if previous is None else
                                np.max(abs(traces[12][sample] - previous[sample])))
                scale = np.max(abs(traces[12][sample]))
                stable = (abs(integral - quadrature) <= 1e-3 * abs(integral)
                          and abs(integral - transverse) <= 1e-3 * abs(integral)
                          and longitudinal <= 1e-3 * scale)
                print(f"axis={axis}, N={size}, band={nodes[0]:g}–{nodes[-1]:g}: "
                      f"integral={integral:.10g}, quadrature difference={integral-quadrature:.4g}, "
                      f"transverse difference={integral-transverse:.4g}, "
                      f"max pointwise longitudinal change="
                      f"{longitudinal:.4g}, {stable=}",
                      flush=True)
            previous = traces[12]


if __name__ == "__main__":
    main()
