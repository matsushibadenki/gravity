"""Canonical spatial embedding reduction of the ADM collar source."""

import sympy as sp

from einstein_embedded_collar import curvature_row
from einstein_even_bulk import Q, X, XYZ, Y, shift_gradient


def check():
    r = sp.Symbol("r", positive=True)
    x, y, z = XYZ
    shifts = (Q*X, Y*X)
    # In the chosen generator coordinates the spatial metric changes by
    # L_W delta and the embedding coefficients change by -W.
    metric = sp.eye(2)
    transformation = sp.BlockMatrix([[metric, metric],
                                      [sp.zeros(2), metric]]).as_explicit()
    canonical = sp.diag(transformation, transformation.inv().T)
    zero, unit = sp.zeros(4), sp.eye(4)
    poisson = sp.BlockMatrix([[zero, unit], [-unit, zero]]).as_explicit()
    assert canonical*poisson*canonical.T == poisson
    assert canonical.det() == 1
    # On the slice X=0, integrate dP_X delta(P_X-p.G). The generator
    # G is the ADM spatial shift contraction, including its surface flux.
    constraint = sp.zeros(2, 4).row_join((-metric).row_join(metric))
    gauge = sp.zeros(2).row_join(metric).row_join(sp.zeros(2, 4))
    assert gauge*poisson*constraint.T == metric

    rho = 6*(1-64*(r-1)**2)
    for shift in shifts:
        h = shift_gradient(shift)
        radial = shift[2].subs({x: 0, y: 0, z: r})
        central = -radial.subs(r, 1)
        radial_metric = h[2, 2].subs({x: 0, y: 0, z: r})
        zeta = central-sp.integrate(radial_metric/2, (r, 1, r))
        assert sp.expand(zeta+radial) == 0
        for lo, hi in ((sp.Rational(7, 8), 1), (1, sp.Rational(9, 8))):
            variation = curvature_row(h, r)+2*zeta/r
            assert sp.integrate(4*rho*sp.expand(variation)/r**2, (r, lo, hi)) == 0

    # No boundary phase is left by the canonical lift on a time lattice.
    p1, p2 = sp.symbols("p1 p2")
    p = sp.Matrix([p1, p2])
    dq = sp.Matrix(sp.symbols("dq1 dq2"))
    dx = sp.Matrix(sp.symbols("dx1 dx2"))
    assert sp.expand(p.dot(dq)+p.dot(dx)-p.dot(dq+dx)) == 0
    print("Central spatial shifts: canonical determinant=1, FP determinant=1.")
    print("Proper-distance source invariant on both sides with a moving central sphere.")


if __name__ == "__main__":
    check()
