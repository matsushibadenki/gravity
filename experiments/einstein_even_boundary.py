"""Even-parity quadrupole boundary charge pairing on a unit sphere."""

import numpy as np
from numpy.polynomial.legendre import leggauss


def quadrature_matrix(nodes):
    mu, weight = leggauss(nodes)
    weight = 2 * np.pi * weight
    harmonic = (3 * mu**2 - 1) / 2
    gradient = -3 * mu * np.sqrt(1 - mu**2)
    scalar_norm = weight @ harmonic**2
    vector_norm = weight @ gradient**2

    # Columns: h_rr, h_rA, tangential trace/2, its radial derivative,
    # tangential trace-free h_AB, pi_rr, pi_rA, pi_AB trace and shear.
    # Rows: lapse value, lapse normal slope, radial and angular shifts.
    matrix = np.zeros((4, 9))
    matrix[0, :4] = [2 * scalar_norm, -2 * vector_norm,
                     -2 * scalar_norm, -2 * scalar_norm]
    matrix[1, 2] = 2 * scalar_norm
    matrix[2, 5] = 2 * scalar_norm
    matrix[3, 6] = 2 * vector_norm
    return matrix


def check(nodes):
    matrix = quadrature_matrix(nodes)
    expected = np.array([
        [2, -12, -2, -2, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 12, 0, 0],
    ]) * (4 * np.pi / 5)
    np.testing.assert_allclose(matrix, expected, atol=1e-12)
    _, singular, right = np.linalg.svd(matrix, full_matrices=True)
    assert singular[-1] > 1
    np.testing.assert_allclose(matrix @ right[4:].T, 0, atol=1e-12)

    # Allow different one-sided data with the same four charges.
    inner = np.arange(1., 10.) / 10
    outer = inner + right[4:].sum(axis=0)
    np.testing.assert_allclose(matrix @ inner - matrix @ outer, 0, atol=1e-12)
    # A jump in each charge is detected by its independent smearing.
    jumps = matrix @ np.linalg.pinv(matrix)
    np.testing.assert_allclose(jumps, np.eye(4), atol=1e-12)
    print(f"nodes={nodes}: charge rank=4, kernel dimension=5, "
          f"minimum singular value={singular[-1]:.8f}")


if __name__ == "__main__":
    for count in (4, 8, 16):
        check(count)
