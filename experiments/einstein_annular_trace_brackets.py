"""Compare oriented ball and annulus brackets in a common tensor regulator."""

import sympy as sp

from einstein_adm_trace_brackets import trace_rows
from einstein_even_bulk import Q, R2, X, Y, lapse_gradient, shift_gradient, tensor_basis
from einstein_even_shell import integrate


def region_rows(tensors, lower, upper, cutoff=None):
    def dot(left, right):
        integrand = sum(a*b for a, b in zip(left, right))
        return integrate(integrand, lower, upper)/sp.pi

    gram = sp.Matrix([[dot(a, b) for b in tensors] for a in tensors])
    inverse = gram.inv()
    traces = trace_rows(tensors)
    geometry, flux = traces[:2, :], traces[2:, :]
    if cutoff is None:
        cutoff = (1-R2)*(4-R2) if lower else 1-R2
    lapse = lapse_gradient(Y*cutoff**2)
    shifts = [shift_gradient(cutoff*v) for v in (Q*X, Y*X)]
    lapse_row = sp.Matrix([[dot(lapse, a)] for a in tensors])
    shift_rows = sp.Matrix([[dot(shift, a) for shift in shifts] for a in tensors])
    assert geometry*inverse*shift_rows == sp.zeros(2)
    assert flux*inverse*lapse_row == sp.zeros(2, 1)
    return gram, geometry, flux, lapse_row.T, shift_rows.T


def pairing(tensors, lower, upper):
    gram, geometry, flux, _, _ = region_rows(tensors, lower, upper)
    return geometry*gram.inv()*flux.T


def check(order):
    tensors = tensor_basis(order)
    inside = pairing(tensors, 0, 1)
    outside = pairing(tensors, 1, 2)
    difference = inside-outside
    assert inside.rank() == outside.rank() == difference.rank() == 2
    bracket = sp.BlockMatrix([[sp.zeros(2), difference],
                              [-difference.T, sp.zeros(2)]]).as_explicit()
    assert bracket.rank() == 4
    assert sp.factor(bracket.det()-difference.det()**2) == 0
    print(f"order={order}: geometry–flux jump bracket=\n{difference.evalf(7)}")
    print(f"rank={bracket.rank()}, second-class density={abs(difference.det()).evalf(7)}")


if __name__ == "__main__":
    for order in (2, 3):
        check(order)
