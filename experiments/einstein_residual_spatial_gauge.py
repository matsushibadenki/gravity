"""Identify static proper spatial gauge histories in the open link kernel."""

import numpy as np
from numpy.polynomial import Polynomial
from scipy.linalg import orth


def classify(zero_modes, primary, steps, n, order, left_inverse, right_inverse):
    # W_i=f(r^2)(Qx)_i+g(r^2)Y x_i. Its symmetrized gradient is
    # expressed in the four original Cartesian tensor basis families.
    s = Polynomial([0, 1])
    generators = []
    for offset, inverse, clamp in ((0, left_inverse, 1-s),
                                   (2*n, right_inverse, (1-s)*(4-s))):
        for j in range(order+3-clamp.degree()):
            polynomial = clamp*s**j
            for f, g in ((polynomial, 0*s), (0*s, polynomial)):
                raw = np.zeros((order+3, 4))
                for col, component in enumerate((2*g, 2*f, 2*(f.deriv()+g), 4*g.deriv())):
                    raw[:len(component.coef), col] = component.coef
                variation = np.zeros(primary.shape[1])
                variation[offset:offset+n] = np.linalg.solve(inverse.T, raw.ravel())
                generators.append(variation)
    gauge = orth(np.column_stack(generators))
    conditions = primary@gauge
    _, singular, vt = np.linalg.svd(conditions, full_matrices=True)
    gauge = gauge@vt[np.count_nonzero(singular>1e-7):].T
    histories = np.tile(gauge, (steps+1, 1))/np.sqrt(steps+1)
    angles = np.linalg.svd(histories.T@zero_modes, compute_uv=False)
    qends = zero_modes.reshape(steps+1, primary.shape[1], -1)[[0,-1]]
    endpoints = qends[:, np.r_[0:n,2*n:3*n], :].reshape(-1, zero_modes.shape[1])
    assert np.linalg.matrix_rank(endpoints,tol=1e-7) == zero_modes.shape[1]
    print(f"Static proper gauge dimension={histories.shape[1]}, "
          f"intersection={sum(angles>1-1e-7)}, minimum overlap={angles.min():.9g}, "
          f"endpoint configuration rank={np.linalg.matrix_rank(endpoints,tol=1e-7)}")
    assert len(angles) == histories.shape[1] == zero_modes.shape[1]
    np.testing.assert_allclose(angles, 1, atol=1e-7, rtol=0)
