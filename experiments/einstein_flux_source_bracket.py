"""Exact collar-source bracket with the matched ADM trace fluxes."""

import sympy as sp

from einstein_adm_trace_brackets import trace_rows
from einstein_even_bulk import XYZ, tensor_basis
from einstein_even_shell import integrate
from einstein_trace_dirac_sewing import poisson


def rows(tensors, lower, upper, lo, hi):
    gram = sp.Matrix([[integrate(sum(a*b for a, b in zip(left, right)),
                                    lower, upper)/sp.pi
                       for right in tensors] for left in tensors])
    r = sp.Symbol("r", positive=True)
    x, y, z = XYZ
    rho = 6*(1-64*(r-1)**2)
    source = []
    for tensor in tensors:
        c = ((tensor[0, 0]+tensor[1, 1])/2).subs({x: 0, y: 0, z: r})
        three_d = (tensor[2, 2]-tensor[1, 1]).subs({x: r, y: 0, z: 0})
        source.append(sp.integrate(sp.expand(4*rho*(c+three_d)/r**2),
                                   (r, lo, hi)))
    count = len(tensors)
    trace = trace_rows(tensors)
    trace = sp.diag(trace[:2, :], trace[2:, :])
    source_row = sp.Matrix([source+[0]*count])
    return poisson(gram.inv()), trace, source_row


def check(order):
    basis = tensor_basis(order)
    inner, left, load_left = rows(basis, 0, 1, sp.Rational(7, 8), 1)
    outer, right, load_right = rows(basis, 1, 2, 1, sp.Rational(9, 8))
    # Common-radial orientation on trace phase space; the source adds.
    symplectic = sp.diag(inner, -outer)
    jump = left.row_join(-right)
    average = left.row_join(right)/2
    bracket = jump*symplectic*jump.T
    cross = symplectic*jump.T
    load = load_left.row_join(load_right)
    response = symplectic*load.T + cross*(bracket.inv()*(cross.T*load.T))
    source_bracket = (average[2:, :]*response).applyfunc(sp.expand)
    assert source_bracket != sp.zeros(2, 1)
    assert (jump*response).applyfunc(sp.expand) == sp.zeros(4, 1)
    print(f"order={order}: {{common flux, collar source}}={source_bracket.evalf(9).T}")


if __name__ == "__main__":
    for order in (2, 3):
        check(order)
