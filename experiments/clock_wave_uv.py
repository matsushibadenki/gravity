"""Evaluate the flat clock-wave form factor and a temporal curvature trace."""

from math import pi

import numpy as np

from clock_gradient_heat import vertices
from curved_clock_heat_blocks import spectra, heat_trace, summed_trace


def wave_shell(size, length, cutoff):
    """Return the band coefficient per integrated (box T)^2 after the X subtraction."""
    _, trace, _, _, mixed = vertices()
    reverse = np.eye(10) - np.outer(trace, trace) / 2
    np.testing.assert_allclose(2 * mixed.T @ reverse @ mixed, np.eye(4))
    momenta = 2 * pi * np.fft.fftfreq(size, length / size)
    square = momenta**2
    pair_mask = (square > 0) & (np.roll(square, -1) > 0)
    q2 = (2 * pi / length)**2
    nodes, weights = np.polynomial.legendre.leggauss(32)
    response = []
    for s in cutoff * (3 + nodes) / 2:
        heat = np.exp(-s * square)
        flat, moment = heat.sum(), heat @ square
        pair = np.exp(-s * (square + (nodes[:, None] + 1) / 2
                            * (np.roll(square, -1) - square)))
        pair_sum = pair @ (flat**3 * square + 3 * flat**2 * moment)
        # In the fixed-moduli prescription neither end of a mixed vertex
        # can be the global zero mode. Only zero transverse momentum needs removal.
        pair_sum -= pair @ np.where(pair_mask, 0, square)
        zero = 4 * flat**3 * moment
        response.append(s * ((weights / 2) @ pair_sum - zero) / (length**4 * q2))
    return -cutoff * (weights @ response) / 4


def main():
    errors = []
    for cutoff in (0.02, 0.005, 0.00125):
        values = [wave_shell(size, 1.8, cutoff) for size in (17, 33, 65, 129)]
        assert np.isclose(values[-1], values[-2], rtol=2e-4, atol=1e-9)
        errors.append(abs(values[-1]))
        print(f"s={cutoff:g}: derivative clock-wave shell coefficients {values}")
    assert errors[0] > errors[1] > errors[2]

    times = np.array([0.07, 0.085, 0.10])
    coarse, _ = summed_trace(9, 3, 0.1, times, clock_axis=1)
    fine, inner = summed_trace(13, 3, 0.1, times, clock_axis=1)
    np.testing.assert_allclose(coarse, fine, rtol=2e-5)
    np.testing.assert_allclose(inner, fine, rtol=0.002)
    print(f"Temporal curve: traces {fine[:, 1]}, grid change "
          f"{np.max(abs(coarse / fine - 1)):.3e}, shell change "
          f"{np.max(abs(inner / fine - 1)):.3e}", flush=True)
    for clock_axis in (0, 1):
        traces = [heat_trace(spectra(n, (0, 0, 0, 0), 0.015, 0.1, clock_axis), times)
                  for n in (9, 13)]
        np.testing.assert_allclose(*traces, rtol=2e-5)
        print(f"clock axis={clock_axis}: zero transverse block at s=0.085 {traces[-1][:, 1]}")


if __name__ == "__main__":
    main()
