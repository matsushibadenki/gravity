"""Check contour admissibility of the physical ADM momentum on the joint regulator."""

import numpy as np
import sympy as sp
from scipy.linalg import block_diag, null_space

from einstein_even_bulk import XYZ, tensor_basis
from einstein_annular_trace_brackets import region_rows
from einstein_joint_adm_time_control import region


def check(projected_gauge=False):
    tensors = tensor_basis(2)
    ball, shell = (region(tensors, 0, 1, 1, projected_gauge),
                   region(tensors, 1, 2, -1, projected_gauge))
    n = len(tensors)
    # Keep the original tensor momenta, impose the proper shift constraint,
    # its temporal gauge complement and the equality of both interface fluxes.
    momentum_rows = []
    for side in (ball, shell):
        rows = side[1][:, n:]
        momentum_rows.append(rows[np.linalg.norm(rows, axis=1) > 0])
    proper = block_diag(*momentum_rows)
    flux = np.column_stack((ball[2][2:, n:], -shell[2][2:, n:]))
    conditions = np.vstack((proper, flux))
    reduced = null_space(conditions)
    kinetic = block_diag(ball[4], shell[4])
    eigenvalues = np.linalg.eigvalsh(reduced.T@kinetic@reduced)
    negative = eigenvalues[eigenvalues < -1e-9]
    assert len(negative) > 0
    print(f"Momentum dimension={len(eigenvalues)}, negative eigenvalues={negative}")

    # For fixed affine conditions, convergence is decided by the same
    # quadratic form on homogeneous variations, not by the packet mean.
    common_flux = np.column_stack((ball[2][2:, n:], np.zeros((2, n))))
    affine = np.vstack((conditions, common_flux))
    values = np.r_[np.zeros(len(conditions)), 2., -3.]
    solution = np.linalg.lstsq(affine, values, rcond=None)[0]
    np.testing.assert_allclose(affine@solution, values, atol=1e-11)
    fixed = null_space(affine)
    fixed_eigenvalues = np.linalg.eigvalsh(fixed.T@kinetic@fixed)
    assert np.min(fixed_eigenvalues) < 0
    print(f"At fixed nonzero flux, minimum kinetic eigenvalue={min(fixed_eigenvalues):.9f}")


def strong_momentum_check():
    tensors = tensor_basis(2)
    components = sp.symbols(f"p:{len(tensors)}")
    tensor = sum((p*field for p, field in zip(components, tensors)), sp.zeros(3))
    expressions = [tensor.trace()] + [
        sum(sp.diff(tensor[i, j], XYZ[j]) for j in range(3)) for i in range(3)]
    coefficients = [c for expression in expressions
                    for c in sp.Poly(expression, *XYZ).coeffs()]
    equations, _ = sp.linear_eq_to_matrix(coefficients, components)
    basis = sp.Matrix.hstack(*equations.nullspace())
    for lo, hi in ((0, 1), (1, 2)):
        gram, _, flux, _, _ = region_rows(tensors, lo, hi)
        kinetic = basis.T*gram*basis
        projected_flux = flux*basis
        assert kinetic.is_positive_definite
        assert projected_flux.rank() == 2
        fixed = np.asarray(projected_flux, dtype=float)
        point = np.linalg.lstsq(fixed, [2., -3.], rcond=None)[0]
        np.testing.assert_allclose(fixed@point, [2., -3.], atol=1e-11)
        print(f"radii={lo},{hi}: strong TT rank={basis.cols}, both nonzero fluxes attainable")


if __name__ == "__main__":
    check(projected_gauge=True)
    strong_momentum_check()
