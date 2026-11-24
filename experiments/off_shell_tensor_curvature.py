"""Measure the heavy tensor's base-metric Einstein term with independent sources."""

from math import pi

import numpy as np

from time_dependent_uv_match import match


def mixed_curvature(size, length, cutoff, mass=2):
    """Euclidean coefficient per component from the static lapse-metric cross response."""
    wave = 2 * pi * np.fft.fftfreq(size, length / size)
    square = wave**2
    shifted = np.roll(wave, -1)
    q = 2 * pi / length
    difference = shifted - wave
    metric_vertex = wave * shifted - 1.5 * (square + shifted**2)
    mixed_insertion = (1.25 * square + 0.375 * (shifted**2 + np.roll(square, 1))
                       - wave * (shifted + np.roll(wave, 1)))
    nodes, weights = np.polynomial.legendre.leggauss(24)
    response = []
    for s in cutoff * (3 + nodes) / 2:
        heat = np.exp(-s * square) / length
        flat = heat.sum()
        transverse_moment = 2 * flat * (heat @ square)
        transverse_flat = flat**2
        pair_heat = np.exp(-s * (square[None, :] + (1 + nodes[:, None]) / 2
                                * (shifted**2 - square))) / length
        metric = transverse_flat * metric_vertex - 2 * transverse_moment
        lapse = -1 / s - difference**2 / 2
        pair = (weights / 2) @ (pair_heat @ (lapse * metric))
        zero_momentum = (2 / s) * (transverse_flat * (heat @ square)
                                   + transverse_moment * flat)
        curvature_trace = (-s * transverse_flat * (heat @ mixed_insertion)
                           + s**2 * (pair - zero_momentum) / 2)
        response.append(np.exp(-s * mass**2) / np.sqrt(4 * pi * s) * curvature_trace / s)
    return -cutoff * (weights @ response) / (8 * q**2)


def main():
    for cutoff in (0.02, 0.005, 0.00125):
        for size in (25, 49, 97):
            spatial = mixed_curvature(size, 1.8, cutoff)
            temporal, _, _ = match(size, 1.8, cutoff)
            print(f"s={cutoff:g} N={size}: s*c_static={cutoff * spatial:+.9e}"
                  f" s*c_time={cutoff * temporal:+.9e}")
    assert np.isclose(spatial, temporal, rtol=0.01)


if __name__ == "__main__":
    main()
