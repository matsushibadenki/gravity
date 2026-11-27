"""Test common flux as a gauge slice of the ADM tensor trace junction."""

import sympy as sp

from einstein_annular_trace_brackets import pairing
from einstein_even_bulk import tensor_basis
from einstein_trace_dirac_sewing import poisson


def check(order):
    tensors = tensor_basis(order)
    left, right = pairing(tensors, 0, 1), pairing(tensors, 1, 2)
    full = sp.diag(poisson(left), -poisson(right))
    identity, zero = sp.eye(2), sp.zeros(2)
    q = identity.row_join(zero)
    flux = zero.row_join(identity)
    geometry_jump = q.row_join(-q)
    flux_jump = flux.row_join(-flux)
    common_flux = flux.row_join(flux)/2
    complement = geometry_jump*full*common_flux.T
    violation = geometry_jump*full*flux_jump.T
    assert complement == (left+right)/2
    assert violation == left-right
    assert complement.rank() == violation.rank() == 2
    conditions = geometry_jump.col_join(flux_jump)
    bracket = conditions*full*conditions.T

    # Include canonical frame positions and charge momenta. On a fixed
    # common-frame slice the pullback of p_frame d(frame) vanishes, even
    # when the momenta depend on traces and on the other frame variables.
    frame_unit, frame_zero = sp.eye(3), sp.zeros(3)
    frame_form = sp.BlockMatrix([[frame_zero, -frame_unit],
                                 [frame_unit, frame_zero]]).as_explicit()
    # Linearized energy, tangential charge, and area on each face.
    charge = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(2, 5), 0, 0],
                        [0, 0, 0, 1], [0, sp.Rational(1, 10), 0, 0]])
    # trace ordering in pairing() is K, Psi, a, b
    charge = charge[:, [1, 0, 2, 3]]
    frame_pullback = sp.zeros(3, 8).col_join(charge.row_join(sp.zeros(3, 4)))
    frame_pullback = frame_pullback.col_join(
        sp.zeros(3, 8).col_join(sp.zeros(3, 4).row_join(charge)))
    extended = sp.diag(full.inv(), frame_form, -frame_form)
    lift = sp.eye(8).col_join(frame_pullback)
    assert lift.T*extended*lift == full.inv()

    dirac = full-full*conditions.T*bracket.inv()*conditions*full
    assert conditions*dirac == sp.zeros(4, 8)
    shared_geometry = q.row_join(q)/2
    physical = shared_geometry*dirac*common_flux.T
    assert physical.rank() == 2
    print(f"order={order}: trial FP rank={complement.rank()}, "
          f"flux-jump violation rank={violation.rank()}, "
          f"reduced geometry–flux rank={physical.rank()}")


if __name__ == "__main__":
    for order in (2, 3):
        check(order)
