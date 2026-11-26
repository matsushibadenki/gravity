"""Sum mixed heat derivatives using their transverse Gaussian and polynomial."""

from itertools import product
from math import comb, gamma, pi

import numpy as np

from direct_curvature_insertion import mixed_insertion


WAVE = 2 * pi / 1.8


def mixed_samples(size, axis, times, length_x=1.8, harmonic=1, *, project_zero=True):
    """Identify the transverse polynomial and, if requested, its global-mode correction."""
    powers = [(i, j) for i, j in product(range(4), repeat=2)
              if i + j <= 3 and (axis == 0 or j == 0)]

    def monomials(time_square, spatial_square):
        return np.array([time_square**i * spatial_square**j for i, j in powers])

    samples = [mixed_insertion(size, (i, 0, j, 0), times, axis, factor_transverse=True, length_x=length_x, harmonic=harmonic) / 2
               for i, j in powers]
    design = [monomials(i*i, j*j) for i, j in powers]
    polynomial = np.linalg.solve(design, samples)
    probe = (1, 0, 2, 1)
    expected = mixed_insertion(size, probe, times, axis, factor_transverse=True, length_x=length_x, harmonic=harmonic) / 2
    arguments = (6, 0) if axis == 1 else (1, 5)
    np.testing.assert_allclose(monomials(*arguments) @ polynomial, expected, rtol=2e-7, atol=1e-7)
    infrared = 0
    if project_zero:
        projected = mixed_insertion(size, (0, 0, 0, 0), times, axis, length_x=length_x, harmonic=harmonic)
        infrared = projected - polynomial[0]
    return powers, polynomial, infrared


def transverse_moments(times, cap, period=1.8):
    """Gaussian moments for one, two, and three equal transverse directions."""
    square = (np.arange(-cap, cap + 1) * (1.8 / period))**2
    weight = np.exp(-times[:, None] * WAVE**2 * square)
    one = weight @ square[:, None]**np.arange(4)

    return product_moments(one)


def continuum_moments(times):
    """Integrate over real momenta in units of WAVE, per reference volume."""
    orders = np.arange(4) + .5
    one = np.array([gamma(order) for order in orders]) / (times[:, None] * WAVE**2)**orders
    return product_moments(one)


def radial_continuum_trace(size, axis, times, length_x, harmonic):
    """Integrate the angular average of a trace quadratic in clock winding."""
    radii = np.arange(4)

    def at(radius, direction):
        t, y, z = radius * direction
        return mixed_insertion(size, (t, 0., y, z), times, axis, True, length_x, harmonic) / 2

    # In the transverse plane the winding response has a scalar and a
    # rank-two part. Its angular mean is attained when p_t^2 = |p|^2/3.
    diagonal = np.ones(3) / np.sqrt(3)
    samples = [at(radius, diagonal) for radius in radii]
    coefficients = np.linalg.solve(np.vander(radii**2, increasing=True), samples)
    check_radius = 1.5
    if axis == 0:
        check = (at(check_radius, np.array([1., 0., 0.]))
                 + 2 * at(check_radius, np.array([0., 1., 0.]))) / 3
    else:
        check = at(check_radius, np.array([1., 0., 0.]))
    np.testing.assert_allclose(np.polynomial.polynomial.polyval(check_radius**2, coefficients),
                               check, rtol=2e-7, atol=1e-7)
    powers = [(order, 0) for order in range(4)]
    return integrate_transverse((powers, coefficients, 0), size, 1, times, length_x)


def product_moments(one):
    def append_direction(previous):
        return np.column_stack([
            sum(comb(order, i) * previous[:, i] * one[:, order - i] for i in range(order + 1))
            for order in range(4)
        ])

    two = append_direction(one)
    return one, two, append_direction(two)


def response(size, axis, times, length_x=1.8, harmonic=1, *, caps=(3, 5, 8, 12)):
    samples = mixed_samples(size, axis, times, length_x, harmonic)
    return sum_transverse(samples, size, axis, times, length_x, caps=caps)


def sum_transverse(samples, size, axis, times, length_x, *, caps, period=1.8):
    """Sum in units of the momentum used to identify the sample polynomial."""
    times = np.asarray(times).ravel()
    return {cap: trace_from_moments(samples, size, axis, times, length_x,
                                    transverse_moments(times, cap, period)) for cap in caps}


def integrate_transverse(samples, size, axis, times, length_x):
    """Return the restored continuum trace scaled by the reference transverse volume."""
    times = np.asarray(times).ravel()
    powers, coefficients, _ = samples
    return trace_from_moments((powers, coefficients, 0), size, axis, times, length_x,
                              continuum_moments(times))


def trace_from_moments(samples, size, axis, times, length_x, gaussian):
    powers, coefficients, infrared = samples
    longitudinal_k2 = (2 * pi * np.fft.fftfreq(size, d=length_x / size))**2
    long_heat = np.exp(-times[:, None] * longitudinal_k2)
    one, two, three = gaussian
    if axis == 1:
        moments = np.column_stack([three[:, i] for i, _ in powers])
    else:
        moments = np.column_stack([one[:, i] * two[:, j] for i, j in powers])
    raw = infrared + np.sum(moments * coefficients.T, axis=1)
    norm = (WAVE**2 * three[:, 1] * long_heat.sum(axis=1)
            + three[:, 0] * (long_heat @ longitudinal_k2))
    return raw - 4 * times**2 * norm


def main():
    times = np.array([0.07, 0.105, 0.14, 0.035, 0.0525])
    previous = {}
    for n in (9, 13):
        for axis in (0, 1):
            values = response(n, axis, times)
            np.testing.assert_allclose(values[8], values[12], rtol=1e-8, atol=1e-8)
            for cap in (3, 5, 12):
                print(f"N={n} axis={axis} cap={cap}: {values[cap]}", flush=True)
            if axis in previous:
                print(f"N={n} axis={axis} longitudinal difference: "
                      f"{values[12] - previous[axis]}", flush=True)
            previous[axis] = values[12]


if __name__ == "__main__":
    main()
