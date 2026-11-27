"""Shared physical flux density from the two-face symplectic pullback."""

import numpy as np
import sympy as sp

from einstein_annular_trace_brackets import pairing
from einstein_even_bulk import tensor_basis
from einstein_geometric_packet_transfer import log_amplitudes
from einstein_jump_packet_transfer import jump_integral
from einstein_trace_dirac_sewing import poisson


def derive(order):
    basis = tensor_basis(order)
    left, right = pairing(basis, 0, 1), pairing(basis, 1, 2)
    bulk = sp.diag(poisson(left), -poisson(right))
    # Frame coordinates (T,X,eta) and their linear ADM charges on each face.
    # Retain the matched frame as a variable during the pullback.
    unit, zero = sp.eye(3), sp.zeros(3)
    frame_form = sp.BlockMatrix([[zero, -unit], [unit, zero]]).as_explicit()
    form = sp.diag(bulk.inv(), frame_form, -frame_form)
    q = sp.Matrix(sp.symbols("K Psi a b", real=True))
    frame = sp.Matrix(sp.symbols("T X eta", real=True))
    k, psi, _, b = q
    time, _, boost = frame
    charges = sp.Matrix([(.6*psi-.4*k), b+.6*(boost-time), .1*k]).applyfunc(
        lambda expr: sp.nsimplify(expr, rational=True))
    matched = q.col_join(q).col_join(frame).col_join(charges)
    matched = matched.col_join(frame).col_join(charges)
    lift = matched.jacobian(list(q)+list(frame))
    pulled = lift.T*form*lift
    assert pulled[4:, :] == sp.zeros(3, 7)
    assert pulled[:, 4:] == sp.zeros(7, 3)
    # Only the common frame is quotiented here. Both flux values remain
    # coordinates of the physical trace phase space.
    reduced = pulled[:4, :4]
    density = sp.sqrt(reduced.det())
    inverse = reduced[2:, :2]
    assert abs(inverse.det()) == density

    # Independent second-class formula in the original trace coordinates.
    jump = sp.eye(4).row_join(-sp.eye(4))
    average = sp.eye(4).row_join(sp.eye(4))/2
    bracket = jump*bulk*jump.T
    dirac = bulk-bulk*jump.T*bracket.inv()*jump*bulk
    assert average*dirac*average.T == reduced.inv()
    assert sp.simplify(density-sp.sqrt(bracket.det())/sp.sqrt(bulk.det())) == 0
    print(f"order={order}: physical endpoint density={density.evalf(9)}, common frame nullity=3")
    return np.array(inverse, dtype=float)[:, ::-1]


def main():
    for order in (2, 3):
        inverse = derive(order)
        steps = 4
        physical = jump_integral(order, steps, True, sharp=True, shared_packet=inverse)
        reference = log_amplitudes(order, steps, False, inverse)
        gaps = abs(physical-reference)
        np.testing.assert_allclose(gaps, 0, atol=1e-8, rtol=0)
        print(f"logdet gap={gaps[0]:.3e}, source quadratic gap={gaps[3]:.3e}")


if __name__ == "__main__":
    main()
