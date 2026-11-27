"""Second-class density with independent tilted frames on both faces."""

import numpy as np
import sympy as sp

from einstein_annular_trace_brackets import pairing
from einstein_even_bulk import tensor_basis
from einstein_geometric_packet_transfer import log_amplitudes
from einstein_jump_packet_transfer import jump_integral
from einstein_trace_dirac_sewing import poisson


def check(order):
    basis = tensor_basis(order)
    ball, shell = pairing(basis, 0, 1), pairing(basis, 1, 2)
    bulk = sp.diag(poisson(ball), -poisson(shell))
    eye, zero = sp.eye(3), sp.zeros(3)
    canonical = sp.BlockMatrix([[zero, eye], [-eye, zero]]).as_explicit()
    phase_poisson = sp.diag(bulk, canonical, -canonical)
    jump = sp.eye(4).row_join(-sp.eye(4))
    shared = sp.eye(4).row_join(sp.eye(4))/2
    raw = jump*bulk*jump.T
    pos = eye.row_join(zero)
    mom = zero.row_join(eye)
    charge = sp.Matrix([[sp.Rational(-2, 5), sp.Rational(3, 5), 0, 0],
                        [0, 0, 0, 1], [sp.Rational(1, 10), 0, 0, 0]])
    correction = sp.zeros(3)
    correction[1, 0] = -sp.Rational(3, 5)
    correction[1, 2] = sp.Rational(3, 5)
    definition = mom-correction*pos
    frame_difference = pos.row_join(-pos)
    frame_average = pos.row_join(pos)/2
    frame_rows = sp.diag(definition, definition).col_join(
        frame_difference).col_join(frame_average)
    trace_rows = (-sp.diag(charge, charge)).col_join(sp.zeros(6, 8))
    conditions = jump.row_join(sp.zeros(4, 12)).col_join(trace_rows.row_join(frame_rows))
    bracket = conditions*phase_poisson*conditions.T
    assert bracket[:4, 4:10].rank() > 0
    assert bracket[4:7, 4:7].rank() > 0
    assert bracket.rank() == 16
    assert sp.factor(bracket.det()-raw.det()) == 0
    coordinates = conditions.col_join(shared.row_join(sp.zeros(4, 12)))
    assert abs(coordinates.det()) == 1
    density = sp.sqrt(bracket.det()/phase_poisson.det())
    retained = shared.row_join(sp.zeros(4, 12))
    reduced = phase_poisson-phase_poisson*conditions.T*bracket.inv()*conditions*phase_poisson
    physical = retained*reduced*retained.T
    assert sp.simplify(density-1/sp.sqrt(physical.det())) == 0
    inverse = np.array(physical.inv()[2:, :2], dtype=float)[:, ::-1]
    print(f"order={order}: independent frame block factor=1, "
          f"shared density={density.evalf(9)}, rank={bracket.rank()}")
    geometric = jump_integral(order, 4, True, sharp=True, shared_packet=inverse)
    master = log_amplitudes(order, 4, False, inverse)
    gaps = abs(geometric-master)
    np.testing.assert_allclose(gaps, 0, atol=1e-8, rtol=0)
    print(f"same-packet log determinant gap={gaps[0]:.3e}, source gap={gaps[3]:.3e}")


if __name__ == "__main__":
    for order in (2, 3):
        check(order)
