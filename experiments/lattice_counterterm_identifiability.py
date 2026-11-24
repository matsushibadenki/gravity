"""Check why a first-order reduced Hessian cannot fix the action counterterm."""

import numpy as np

from reduced_clock_ball_seam import spectral_operators


def smooth_band_action(operator, times, weights):
    eigenvalues = np.linalg.eigvalsh(operator)
    return -0.5 * np.dot(weights / times, np.exp(-times[:, None] * eigenvalues).sum(axis=1))


def main():
    nodes, weights = np.polynomial.legendre.leggauss(32)
    times = 0.03 + 0.01 * nodes
    weights *= 0.01
    for size in (3, 5):
        spacing = 1.8 / size
        sites, gradients, laplacian, _ = spectral_operators(size, spacing)
        profile = np.cos(2 * np.pi * sites[:, 2] / size)
        gradient_squared = sum((gradient @ profile)**2 for gradient in gradients)
        reference = np.eye(len(sites)) - laplacian
        first = np.diag(profile)
        contact = np.diag(gradient_squared)
        step = 1e-3
        predictions = []
        comparisons = []
        for direction in (0, 1):
            plus = smooth_band_action(reference + step * first + step**2 * direction * contact,
                                      times, weights)
            minus = smooth_band_action(reference - step * first + step**2 * direction * contact,
                                       times, weights)
            baseline = smooth_band_action(reference, times, weights)
            predictions.append((plus - minus) / (2 * step))
            comparisons.append((plus - 2 * baseline + minus) / step**2)
        assert np.isclose(*predictions, atol=1e-7)
        values, modes = np.linalg.eigh(reference)
        contact_diagonal = np.diag(modes.T @ contact @ modes)
        expected = weights @ (np.exp(-times[:, None] * values) @ contact_diagonal)
        measured = comparisons[1] - comparisons[0]
        assert np.isclose(measured, expected, rtol=1e-6)
        print(f"a={spacing:.3f}: unchanged first variation, "
              f"smooth second variation shift={measured:.9f}")


if __name__ == "__main__":
    main()
