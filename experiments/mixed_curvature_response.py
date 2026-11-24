"""Finite-band mixed Einstein-clock heat response and curvature probe rank."""

from math import pi

import numpy as np

from curved_clock_heat_blocks import heat_trace, spectra, summed_trace


LENGTH = 1.8
WAVE = 2 * pi / LENGTH


def mixed_shells(size, cap, amplitude, velocity):
    nodes, weights = np.polynomial.legendre.leggauss(12)
    cutoffs = np.array([0.07, 0.035, 0.0175])
    times = (cutoffs[:, None] * (3 + nodes) / 2).ravel()

    def trace(warp, winding, axis=1):
        # The ghost is independent of the clock and cancels in the inner difference.
        return np.array([item[0] for item in summed_trace(
            size, cap, winding, times, clock_axis=axis, amplitude=warp)])

    curved_null = trace(amplitude, 0)
    flat_null = trace(0, 0)
    flat_clock = trace(0, velocity)
    grid = 2 * pi * np.arange(size) / size
    volume_factor = np.exp(2 * amplitude * np.cos(grid)).mean()
    result = []
    for axis in (1, 0):
        change = trace(amplitude, velocity, axis) - curved_null
        subtracted = change - volume_factor * (flat_clock - flat_null)
        integral = -(subtracted / times).reshape(2, -1, len(nodes)) @ weights
        result.append(integral * cutoffs / (4 * LENGTH**4 * amplitude**2 * velocity**2))
    temporal, spatial = result
    # Integrated RX and Ric(dT,dT) coefficients at order amplitude^2 velocity^2.
    return -temporal / (3 * WAVE**2), (temporal - spatial) / WAVE**2


def curvature_rank():
    """Separate the local curvature-square invariants modulo Euler on a torus."""
    # Metric variations are 2 cos(qx) I and 2 cos(qx) diag(0,0,1,-1).
    # The rows are averages of linearized R^2 and Ric^2 divided by q^4.
    symbol = np.diag([0., -1., 0., 0.])
    rows = []
    for h in (2 * np.eye(4), 2 * np.diag([0., 0., 1., -1.])):
        ricci = (symbol @ h + h @ symbol - np.trace(symbol) * h - np.trace(h) * symbol) / 2
        rows.append([np.trace(ricci)**2 / 2, np.sum(ricci**2) / 2])
    np.testing.assert_array_equal(rows, [[18, 6], [0, 1]])
    print("Pure curvature R^2, Ric^2 probe matrix:", rows, flush=True)


def main():
    curvature_rank()
    times = np.array([0.035, 0.07, 0.14])
    traces = [heat_trace(spectra(n, (0, 0, 0, 0), 0.025, 0, shear=True), times)
              for n in (13, 17)]
    np.testing.assert_allclose(*traces, rtol=2e-5)
    print(f"Shear zero transverse sector traces at s=0.07: {traces[-1][:, 1]}", flush=True)
    for size, cap, amplitude in ((9, 2, 0.025), (9, 3, 0.025), (13, 3, 0.025),
                                 (9, 2, 0.0125)):
        rx, ric = mixed_shells(size, cap, amplitude, 0.3)
        print(f"N={size} cap={cap} amplitude={amplitude}: "
              f"RX total={rx[0]} inner={rx[1]}, RicTT total={ric[0]} inner={ric[1]}", flush=True)


if __name__ == "__main__":
    main()
