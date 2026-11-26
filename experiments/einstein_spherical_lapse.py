"""Quadrupolar lapse constraint and boundary trace matrices on the unit ball."""

import numpy as np
from numpy.polynomial.legendre import leggauss


def check(size):
    # Both the lapse and conformal metric probes use r^2 P_2 times a
    # polynomial in y=2r^2-1. The P_2 angular norm is 4 pi/5.
    from numpy.polynomial.legendre import Legendre

    nodes, weights = leggauss(2 * size + 4)
    r = (nodes + 1) / 2
    y = 2 * r**2 - 1
    polynomials = [Legendre.basis(i) for i in range(size)]
    value = np.array([p(y) for p in polynomials]).T * r[:, None]**2
    laplace = np.array([
        28 * r**2 * p.deriv()(y) + 16 * r**4 * p.deriv(2)(y)
        for p in polynomials
    ]).T
    volume = weights * r**2 * (2 * np.pi / 5)
    constraint = -2 * value.T @ (volume[:, None] * laplace)
    trace = np.array([[p(1) for p in polynomials],
                      [2 * p(1) + 4 * p.deriv()(1) for p in polynomials]])
    orientation = np.array([[0., -1.], [1., 0.]])
    flux = (8 * np.pi / 5) * trace.T @ orientation @ trace
    np.testing.assert_allclose(constraint - constraint.T, flux, atol=5e-10)

    _, _, vt = np.linalg.svd(trace, full_matrices=True)
    proper = vt[2:].T
    np.testing.assert_allclose(proper.T @ flux, 0., atol=1e-11)
    assert np.linalg.matrix_rank(flux, tol=1e-9) == 2
    generator = proper.T @ constraint
    assert np.linalg.matrix_rank(generator) == size - 2

    # For the restricted canonical model the constraints generate momentum shifts.
    # Gauge-fix the proper orbits using their orthonormal right singular vectors.
    _, _, gauge_basis = np.linalg.svd(generator, full_matrices=True)
    fp = gauge_basis[:size-2] @ generator.T
    coordinates = np.vstack((generator, gauge_basis[size-2:]))
    error = np.linalg.slogdet(fp)[1] - np.linalg.slogdet(coordinates)[1]
    np.testing.assert_allclose(error, 0., atol=1e-11)
    print(f"basis={size}: proper rank={size-2}, boundary rank=2, log measure error={error:+.2e}")


if __name__ == "__main__":
    for order in (4, 6, 8, 10):
        check(order)
