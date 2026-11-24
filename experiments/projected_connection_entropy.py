"""Check the spin-two trace and the linear replica response of a bundle connection."""

from math import isclose

import numpy as np

from clock_tensor_slab import tensor_basis


def connection_generator(rotation):
    # An infinitesimal spatial rotation acts on a symmetric tensor by [J, Q].
    basis = tensor_basis()
    return np.einsum("aij,bij->ab", basis, rotation @ basis - basis @ rotation)


def replica_operator(replicas, generator, amplitude):
    """A small Gaussian graph with a cut, two time slices, and spatial flux."""
    spaces, times, rank = 3, 2, len(generator)
    nodes = replicas * spaces * times
    operator = np.eye(nodes * rank)
    derivative = np.zeros_like(operator)
    eigenvalues, vectors = np.linalg.eigh(1j * generator)
    active = np.real_if_close((vectors * np.exp(-1j * amplitude * eigenvalues)) @ vectors.conj().T)

    def block(sheet, time, site):
        start = rank * (spaces * (times * sheet + time) + site)
        return slice(start, start + rank)

    def link(left, right, rotation=None):
        identity = np.eye(rank)
        connection = identity if rotation is None else rotation
        operator[left, left] += identity
        operator[right, right] += identity
        operator[left, right] -= connection
        operator[right, left] -= connection.T
        if rotation is not None:
            derivative[left, right] -= generator
            derivative[right, left] += generator

    for sheet in range(replicas):
        for time in range(times):
            for site in range(spaces):
                following = (site + 1) % spaces
                link(block(sheet, time, site), block(sheet, time, following),
                     active if site == 0 else None)
        for site in range(spaces):
            link(block(sheet, 0, site), block(sheet, 1, site))
            # Only one spatial site belongs to the replicated region.
            next_sheet = (sheet + 1) % replicas if site == 0 else sheet
            link(block(sheet, 1, site), block(next_sheet, 0, site))
    return operator, derivative


def effective_action(operator, time_points, weights):
    spectrum = np.linalg.eigvalsh(operator)
    heat_trace = np.exp(-time_points[:, None] * spectrum).sum(axis=1)
    return -0.5 * np.sum(weights * heat_trace / time_points)


def main():
    rotation = np.array([[0., -1., 0.], [1., 0., 0.], [0., 0., 0.]])
    generator = connection_generator(rotation)
    assert np.allclose(generator, -generator.T)
    assert isclose(np.trace(generator @ generator), 5 * np.trace(rotation @ rotation))
    assert isclose(np.trace(generator @ generator), -10)

    nodes, weights = np.polynomial.legendre.leggauss(24)
    times = 0.25 + (nodes + 1) * 0.375
    weights *= 0.375
    step = 1e-3
    for n in (1, 2, 3, 4):
        operator, perturbation = replica_operator(n, generator, 0)
        assert np.max(np.abs(np.trace(perturbation.reshape(-1, 5, len(operator) // 5, 5),
                                      axis1=1, axis2=3))) < 1e-14
        values, modes = np.linalg.eigh(operator)
        spectral_diagonal = np.diag(modes.T @ perturbation @ modes)
        heat_response = np.exp(-times[:, None] * values) @ spectral_diagonal
        assert np.max(np.abs(heat_response)) < 1e-12
        plus = effective_action(replica_operator(n, generator, step)[0], times, weights)
        minus = effective_action(replica_operator(n, generator, -step)[0], times, weights)
        neutral = effective_action(operator, times, weights)
        assert isclose(plus, minus, abs_tol=1e-12)
        assert abs(plus - neutral) > 1e-11
        print(f"replicas={n}: maximum linear heat response={max(abs(heat_response)):.3e}; "
              f"finite deformation={plus-neutral:+.3e}")


if __name__ == "__main__":
    main()
