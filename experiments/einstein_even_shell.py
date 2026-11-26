"""Charged even-parity constraint pairing on both sides of a spherical cut."""

import sympy as sp

from einstein_even_bulk import (
    I, Q, X, XYZ, Y, R2, lapse_gradient, moment, shift_gradient,
)


def integrate(polynomial, inner, outer, surface=False):
    result = 0
    for powers, coefficient in sp.Poly(polynomial, *XYZ).terms():
        degree = sum(powers)
        if surface:
            factor = (degree + 3) * outer**(degree + 2)
        else:
            factor = outer**(degree + 3) - inner**(degree + 3)
        result += coefficient * moment(powers) * factor
    return result


def boundary_flux(lapse, metric, radius):
    trace = sp.trace(metric)
    gradient = sp.Matrix([sp.diff(lapse, x) for x in XYZ])
    divergence = sp.Matrix([
        sum(sp.diff(metric[i, j], XYZ[j]) for j in range(3))
        for i in range(3)
    ])
    trace_gradient = sp.Matrix([sp.diff(trace, x) for x in XYZ])
    normal = X / radius
    flux = normal.dot(lapse * (divergence - trace_gradient)
                      - metric * gradient + trace * gradient)
    return integrate(flux, 0, radius, surface=True)


def check():
    # Spans both lapse traces and both even-parity shift traces at r=1.
    lapses = [Y, R2 * Y, (1 - R2)**2 * Y]
    shifts = [Q * X, Y * X, (1 - R2) * Q * X, (1 - R2) * Y * X]
    inner_rows, outer_rows = [], []
    for lapse in lapses:
        inner_row, outer_row = [], []
        for shift in shifts:
            metric = shift_gradient(shift)
            adjoint = lapse_gradient(lapse)
            polynomial = sum(a * b for a, b in zip(metric, adjoint))
            at_cut = boundary_flux(lapse, metric, sp.Integer(1))
            at_outer = boundary_flux(lapse, metric, sp.Integer(2))
            inner = integrate(polynomial, 0, 1)
            shell = integrate(polynomial, 1, 2)
            # A pure spatial gauge variation has identically zero C_h.
            assert sp.simplify(inner + at_cut) == 0
            assert sp.simplify(shell + at_outer - at_cut) == 0
            inner_row.append(inner / sp.pi)
            outer_row.append((shell + at_outer) / sp.pi)
        inner_rows.append(inner_row)
        outer_rows.append(outer_row)
    inner, outer = map(sp.Matrix, (inner_rows, outer_rows))
    assert inner + outer == sp.zeros(3, 4)
    assert inner[2, :] == sp.zeros(1, 4)
    assert inner.rank() == 2
    print("Inner mixed pairing divided by pi:", inner)
    print("Shell cut pairing cancels it exactly after removing the outer flux.")


if __name__ == "__main__":
    check()
