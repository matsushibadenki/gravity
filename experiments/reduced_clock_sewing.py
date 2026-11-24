"""Check how canonical sewing transforms under a nonlocal kinetic measure."""

import numpy as np


def replica_operator(amplitude, replicas, times, use_induced_seam):
    """Return the normalized finite transfer operator on a two-site region."""
    mass = np.array([[1.0, amplitude], [amplitude, 1.0]])
    stiffness = np.array([[3.0, -0.75], [-0.75, 2.0]])
    masses, vectors = np.linalg.eigh(mass)
    root = (vectors * np.sqrt(masses)) @ vectors.T
    inverse = (vectors / np.sqrt(masses)) @ vectors.T
    repeated_root = np.kron(np.eye(replicas), root)
    repeated_inverse = np.kron(np.eye(replicas), inverse)
    block_size = 2 * replicas
    permutation = np.eye(block_size)
    for sheet in range(replicas):
        permutation[2 * sheet, 2 * sheet] = 0
        permutation[2 * sheet, 2 * ((sheet + 1) % replicas)] = 1
    if replicas == 1:
        assert np.array_equal(permutation, np.eye(2))

    seam = repeated_root @ permutation @ repeated_inverse if use_induced_seam else permutation
    potential = np.kron(np.eye(replicas), inverse @ stiffness @ inverse)
    operator = np.kron(np.eye(times), potential)
    for time in range(times):
        successor = (time + 1) % times
        difference = np.zeros((block_size, times * block_size))
        difference[:, time * block_size:(time + 1) * block_size] = -np.eye(block_size)
        difference[:, successor * block_size:(successor + 1) * block_size] = (
            seam if successor == 0 else np.eye(block_size)
        )
        operator += difference.T @ difference
    return operator


def band_action(operator):
    points, weights = np.polynomial.legendre.leggauss(48)
    times = 0.2 + (points + 1) * 0.35
    spectrum = np.linalg.eigvalsh(operator)
    trace = np.exp(-times[:, None] * spectrum).sum(axis=1)
    return -0.175 * np.sum(weights * trace / times)


def response(replicas, induced, step):
    plus = band_action(replica_operator(step, replicas, 4, induced))
    minus = band_action(replica_operator(-step, replicas, 4, induced))
    return (plus - minus) / (2 * step)


if __name__ == "__main__":
    step = 1e-5
    assert np.isclose(response(1, True, step), response(1, False, step), atol=1e-9)
    for replicas in (2, 3):
        required = response(replicas, True, step)
        scalar_seam = response(replicas, False, step)
        assert abs(required - scalar_seam) > 1e-5
        assert np.isclose(required, response(replicas, True, step / 2), atol=1e-9)
        print(f"n={replicas}: transformed canonical response={required:+.9f}, "
              f"untransformed sewing={scalar_seam:+.9f}")
