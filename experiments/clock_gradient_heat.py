"""Match the flat, constant-gradient clock insertion in de Donder gauge."""

from math import pi

import numpy as np


def vertices():
    basis = []
    for a in range(4):
        for b in range(a, 4):
            h = np.zeros((4, 4))
            h[a, b] = h[b, a] = 1 if a == b else 1 / np.sqrt(2)
            basis.append(h)
    basis = np.array(basis)
    tr = np.trace(basis, axis1=1, axis2=2)
    t = np.eye(4)[0]
    ht = basis @ t
    ht_t = ht @ t
    # Clock action is sqrt(g) g^{ab} T_a T_b / 2, Einstein coupling A=1.
    metric = (np.outer(tr, tr) / 8 - np.eye(10) / 4
              - (np.outer(tr, ht_t) + np.outer(ht_t, tr)) / 4 + ht @ ht.T)
    mixing = np.outer(tr, t) / 2 - ht
    return basis, tr, t, metric, mixing


def ward_and_weights():
    basis, tr, t, metric, mixing = vertices()
    tadpole = np.eye(4) / 4 - np.outer(t, t) / 2
    reverse = np.eye(10) - np.outer(tr, tr) / 2
    for k in np.array([[1, 2, 3, 4], [2, -2, 0, 3], [0, 1, 0, 0]]):
        for xi in np.eye(4):
            orbit_metric = 2j * np.einsum("aij,i,j->a", basis, k, xi)
            orbit_clock = t @ xi
            b = mixing @ k
            metric_image = metric @ orbit_metric + 1j * b * orbit_clock
            clock_image = -1j * b @ orbit_metric + (k @ k) * orbit_clock
            variation = (- (k @ xi) * basis
                         + np.einsum("i,ajk,k->aij", k, basis, xi)
                         + np.einsum("j,aik,k->aij", k, basis, xi))
            source = 1j * np.einsum("ij,aij->a", tadpole, variation)
            np.testing.assert_allclose(metric_image + source, 0, atol=1e-13)
            np.testing.assert_allclose(clock_image, 0, atol=1e-13)
    # Rotating the conformal direction gives C C^T=2P in metric units.
    # Trace of the X vertex and trace of the square of the sqrt(X) vertex.
    return np.trace(2 * reverse @ metric), 4 * np.trace(mixing.T @ reverse @ mixing)


def shell(size, length, cutoff, metric_trace, mixed_trace):
    wave = 2 * pi * np.fft.fftfreq(size, length / size)
    nodes, weights = np.polynomial.legendre.leggauss(32)
    times = cutoff * (3 + nodes) / 2
    heat = np.exp(-times[:, None] * wave**2)
    flat = heat.sum(axis=1)
    moment = heat @ wave**2
    trace = (-times * metric_trace * (flat**4 - 1)
             + times**2 * mixed_trace * moment * flat**3 / 2) / length**4
    return -cutoff / 4 * (weights @ (trace / times)), trace


def main():
    metric, mixed = ward_and_weights()
    print(f"Ward identity verified; trace weights {metric=:.9f}, {mixed=:.9f}")
    target = (metric - mixed / 4) / (64 * pi**2)
    for cutoff in (0.02, 0.005, 0.00125):
        traces = []
        for size in (17, 33, 65, 129):
            value, trace = shell(size, 1.8, cutoff, metric, mixed)
            traces.append(trace)
            print(f"s={cutoff:g} N={size:3d}: s*c_X={cutoff * value:+.10e}")
        np.testing.assert_allclose(traces[-2], traces[-1], rtol=2e-6, atol=1e-10)
    corrected = cutoff * (value + metric * cutoff / (2 * 1.8**4))
    assert np.isclose(corrected, target, rtol=2e-6, atol=1e-10)


if __name__ == "__main__":
    main()
