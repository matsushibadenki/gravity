"""Direct Dirac reduction and auxiliary conversion of the raw ADM trace jumps."""

import sympy as sp

from einstein_annular_trace_brackets import pairing
from einstein_even_bulk import tensor_basis


def poisson(mixed):
    size = mixed.rows
    return sp.BlockMatrix([[sp.zeros(size), mixed],
                           [-mixed.T, sp.zeros(size)]]).as_explicit()


def check(order):
    tensors = tensor_basis(order)
    ball = pairing(tensors, 0, 1)
    shell = pairing(tensors, 1, 2)
    separate = sp.diag(poisson(ball), -poisson(shell))
    identity = sp.eye(4)
    jump = identity.row_join(-identity)
    shared = identity.row_join(identity)/2
    charge = jump*separate*jump.T
    dirac = separate-separate*jump.T*charge.inv()*jump*separate
    assert jump*dirac == sp.zeros(4, 8)

    # Pull back the oriented symplectic form instead of using a Dirac bracket.
    pullback = identity.col_join(identity)
    form = pullback.T*separate.inv()*pullback
    shared_poisson = shared*dirac*shared.T
    assert shared_poisson == form.inv()

    density = sp.sqrt(charge.det())
    original_density = 1/sp.sqrt(separate.det())
    reduced_density = 1/sp.sqrt(shared_poisson.det())
    assert sp.simplify(original_density*density-reduced_density) == 0

    # A constant-bracket conversion with an auxiliary opposite symplectic
    # block. Gauge xi=0 recovers the original jump delta and its density.
    extended = sp.diag(separate, -charge)
    converted = jump.row_join(identity)
    gauge = sp.zeros(4, 8).row_join(identity)
    assert converted*extended*converted.T == sp.zeros(4)
    fp = gauge*extended*converted.T
    auxiliary_density = 1/sp.sqrt(charge.det())
    assert sp.simplify(abs(fp.det())*auxiliary_density-density) == 0
    print(f"order={order}: direct density={reduced_density.evalf(9)}, "
          "independent symplectic pullback and auxiliary conversion agree")
    print("Shared metric–flux bracket:")
    print(shared_poisson[:2, 2:].evalf(7))


if __name__ == "__main__":
    for order in (2, 3):
        check(order)
