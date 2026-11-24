"""Sum mixed heat derivatives using their transverse Gaussian and polynomial."""

from itertools import product
from math import pi

import numpy as np

from direct_curvature_insertion import mixed_insertion


WAVE = 2 * pi / 1.8


def mixed_samples(size, axis, times):
    powers = [(i, j) for i, j in product(range(4), repeat=2)
              if i + j <= 3 and (axis == 0 or j == 0)]

    def monomials(time_square, spatial_square):
        return np.array([time_square**i * spatial_square**j for i, j in powers])

    samples = [mixed_insertion(size, (i, 0, j, 0), times, axis, factor_transverse=True) / 2
               for i, j in powers]
    design = [monomials(i*i, j*j) for i, j in powers]
    polynomial = np.linalg.solve(design, samples)
    probe = (1, 0, 2, 1)
    expected = mixed_insertion(size, probe, times, axis, factor_transverse=True) / 2
    arguments = (6, 0) if axis == 1 else (1, 5)
    np.testing.assert_allclose(monomials(*arguments) @ polynomial, expected, rtol=2e-7, atol=1e-7)
    projected = mixed_insertion(size, (0, 0, 0, 0), times, axis)
    infrared = projected - polynomial[0]
    return powers, polynomial, infrared


def response(size, axis, times):
    powers, coefficients, infrared = mixed_samples(size, axis, times)
    longitudinal = np.fft.fftfreq(size) * size
    result = {}
    for cap in (3, 5, 8, 12):
        p = np.array(list(product(range(-cap, cap+1), repeat=3)))
        p2 = (p*p).sum(axis=1)
        temporal, spatial = (p2, np.zeros_like(p2)) if axis == 1 else (p[:, 0]**2, p2-p[:, 0]**2)
        moment = np.array([temporal**i * spatial**j for i, j in powers])
        weight = np.exp(-times[:, None] * WAVE**2 * p2)
        raw = infrared + np.sum((weight @ moment.T) * coefficients.T, axis=1)
        long_heat = np.exp(-times[:, None] * WAVE**2 * longitudinal**2)
        norm = (weight * p2).sum(axis=1) * long_heat.sum(axis=1)
        norm += weight.sum(axis=1) * (long_heat @ longitudinal**2)
        result[cap] = raw - 4 * times**2 * WAVE**2 * norm
    return result


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
