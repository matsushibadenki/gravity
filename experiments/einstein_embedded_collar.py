"""Quadrupole intrinsic collar source with a radially extended embedding."""

import sympy as sp

from einstein_even_bulk import Q, R2, X, XYZ, Y, shift_gradient


def curvature_row(tensor, r):
    """Return c+3d from the polar and equatorial tangential components."""
    x, y, z = XYZ
    c = ((tensor[0, 0]+tensor[1, 1])/2).subs({x: 0, y: 0, z: r})
    three_d = (tensor[2, 2]-tensor[1, 1]).subs({x: r, y: 0, z: 0})
    return c+three_d


def check():
    r = sp.Symbol("r", positive=True)
    x, y, z = XYZ
    rho = 6*(1-64*(r-1)**2)
    intervals = ((sp.Rational(7, 8), 1), (1, sp.Rational(9, 8)))
    # Allow radial dependence both in the gauge parameter and in the
    # embedding. These shifts vanish at the seam but act inside the collar.
    for cutoff, (lo, hi) in zip((1-R2, (1-R2)*(4-R2)), intervals):
        for shape in (Q*X, Y*X):
            shift = cutoff*shape
            radial = shift[2].subs({x: 0, y: 0, z: r})
            metric_variation = curvature_row(shift_gradient(shift), r)
            # Keep each sphere at a specified signed proper distance from
            # the seam. Linear variation gives zeta'=-H/2.
            radial_metric_variation = shift_gradient(shift)[2, 2].subs(
                {x: 0, y: 0, z: r})
            displacement = -sp.integrate(radial_metric_variation/2, (r, 1, r))
            assert sp.expand(displacement+radial) == 0
            embedding_variation = 2*displacement/r
            assert sp.expand(metric_variation+embedding_variation) == 0
            bare = sp.integrate(4*rho*metric_variation/r**2, (r, lo, hi))
            assert bare != 0
            dressed = sp.integrate(4*rho*(metric_variation+embedding_variation)/r**2,
                                   (r, lo, hi))
            assert dressed == 0
            print(f"interval={lo},{hi}: metric-only change={bare.evalf(9)}, dressed=0")

    # Normalize the source, and exhibit sensitivity to how the seam
    # displacement is extended away from the central sphere.
    assert sp.integrate(rho, (r, *intervals[0])) + sp.integrate(
        rho, (r, *intervals[1])) == 1
    difference = sum(sp.integrate(8*rho*(r-1)**2/r**3, (r, lo, hi))
                     for lo, hi in intervals)
    assert difference.evalf() > 0
    print(f"Equal seam displacement, different off-seam embedding: {difference.evalf(9)}")


if __name__ == "__main__":
    check()
