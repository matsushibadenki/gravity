"""Check all flat Einstein-clock and ghost channels on a four-torus."""

from itertools import product
from math import log, pi

import numpy as np


def ward_check():
    """Verify the de Donder identity before the Euclidean trace rotation."""
    pairs = [(mu, nu) for mu in range(4) for nu in range(mu, 4)]
    metric = np.zeros((10, 4, 4))
    for basis, (mu, nu) in zip(metric, pairs):
        basis[mu, nu] = basis[nu, mu] = 1 if mu == nu else 1 / np.sqrt(2)
    traces = np.trace(metric, axis1=1, axis2=2)
    trace_reverse = np.eye(10) - np.outer(traces, traces) / 2
    np.testing.assert_allclose(np.linalg.eigvalsh(trace_reverse), [-1] + [1] * 9)
    for k in (np.array(mode) for mode in product(range(-2, 3), repeat=4)):
        k2 = k @ k
        gauge_fix = np.einsum("aij,j->ia", metric, k) - np.outer(k, traces) / 2
        orbit = 2 * np.einsum("aij,j->ai", metric, k)
        ghost = gauge_fix @ orbit
        hessian_fixed = k2 * trace_reverse
        hessian_bare = hessian_fixed - 2 * gauge_fix.T @ gauge_fix
        np.testing.assert_allclose(ghost, k2 * np.eye(4), atol=1e-13)
        np.testing.assert_allclose(hessian_bare @ orbit, 0, atol=1e-13)
        np.testing.assert_allclose(hessian_fixed @ orbit, 2 * gauge_fix.T @ ghost, atol=1e-13)
    print("Flat four-dimensional Ward identity verified on 625 Fourier modes.")


def shell(size, length, cutoff):
    """Absolute Gaussian heat action per four-volume with constant modes fixed."""
    wave = 2 * pi * np.fft.fftfreq(size, length / size)
    nodes, weights = np.polynomial.legendre.leggauss(32)
    times = cutoff * (3 + nodes) / 2
    scalar_trace = (np.exp(-times[:, None] * wave**2).sum(axis=1)**4 - 1) / length**4
    metric_trace, clock_trace, ghost_trace = 10 * scalar_trace, scalar_trace, 4 * scalar_trace
    weighted_trace = metric_trace + clock_trace - 2 * ghost_trace
    action = -cutoff / 4 * (weights @ (weighted_trace / times))
    return action, weighted_trace


def main():
    ward_check()
    length = 1.8
    target = -9 / (256 * pi**2)
    for cutoff in (0.02, 0.005, 0.00125):
        values = []
        for size in (17, 33, 65, 129):
            action, trace = shell(size, length, cutoff)
            values.append((action, trace))
            print(f"s={cutoff:g} N={size:3d}: s^2 * action={cutoff**2 * action:+.11f}")
        np.testing.assert_allclose(values[-2][1], values[-1][1], rtol=2e-6)
        corrected = cutoff**2 * (values[-1][0] - 3 * log(2) / (2 * length**4))
        assert np.isclose(corrected, target, rtol=2e-6)


if __name__ == "__main__":
    main()
