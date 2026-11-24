"""Sum pure metric heat derivatives over transverse Fourier modes."""

from itertools import product

import numpy as np

from direct_curvature_insertion import operator_jets, second_trace
from transverse_insertion_sum import WAVE


def sample_trace(size, shear, times, harmonic, length_x, momentum, project_zero=False):
    t, y, z = momentum
    jets = operator_jets(size, (t, 0, y, z), 0., shear=shear,
                         project_zero=project_zero, harmonic=harmonic, length_x=length_x)
    transverse = WAVE**2 * (t*t + y*y + z*z)
    for block in jets:
        block[0] -= transverse * np.eye(len(block[0]))
    boson, ghost = [second_trace(block, times) for block in jets]
    return (boson - 2 * ghost) / (1 if project_zero else 2)



def zero_projection_trace_shift(size, shear, times, harmonic, length_x):
    args = size, shear, times, harmonic, length_x, (0, 0, 0)
    delta = sample_trace(*args, project_zero=True) - sample_trace(*args)
    # The conformal volume subtraction itself loses the flat zero mode.
    return delta if shear else delta + 24


def response(size, shear, times, harmonic=1, length_x=1.8):
    nodes = [(0, 0, 0), (1, 0, 0), (2, 0, 0)]
    if shear:
        nodes.extend(((0, 1, 0), (0, 2, 0), (1, 1, 0), (0, 1, 1)))

    def monomials(momentum):
        squares = np.asarray(momentum)**2
        if not shear:
            total = squares.sum(axis=-1)
            return np.array([np.ones_like(total), total, total**2])
        # Swapping y and z reverses the shear amplitude, so its second
        # derivative is symmetric in the two squared momenta.
        time, y, z = np.moveaxis(squares, -1, 0)
        spatial = y + z
        return np.array([np.ones_like(time), time, time**2, spatial,
                         spatial**2, time * spatial, y * z])

    def sample(momentum, project_zero=False):
        return sample_trace(size, shear, times, harmonic, length_x, momentum, project_zero)

    coefficients = np.linalg.solve([monomials(p) for p in nodes], [sample(p) for p in nodes])
    check = (1, 2, 1) if shear else (3, 0, 0)
    np.testing.assert_allclose(monomials(check) @ coefficients, sample(check), atol=1e-7, rtol=1e-7)
    infrared = sample((0, 0, 0), True) - coefficients[0]
    result = {}
    for cap in (3, 5, 8):
        p = np.array(list(product(range(-cap, cap+1), repeat=3)))
        p2 = (p*p).sum(axis=1)
        heat = np.exp(-times[:, None] * WAVE**2 * p2)
        total = infrared + np.sum((heat @ monomials(p).T) * coefficients.T, axis=1)
        if not shear:
            longitudinal = np.fft.fftfreq(size) * size
            flat = heat.sum(axis=1) * np.exp(-times[:, None] * (2 * np.pi / length_x)**2 * longitudinal**2).sum(axis=1)
            # d²/db² of the conformal volume factor is 8.
            total -= 24 * (flat - 1)
        result[cap] = total
    return result


if __name__ == "__main__":
    times = np.array([0.07, 0.105, 0.14, 0.035, 0.0525])
    for n in (9, 13):
        for shear in (False, True):
            values = response(n, shear, times)
            np.testing.assert_allclose(values[5], values[8], rtol=1e-4)
            for cap in (3, 5, 8):
                print(f"N={n} shear={shear} cap={cap}: {values[cap]}", flush=True)
