"""Positive reduced momentum contour with nonzero matched sphere fluxes."""

import sympy as sp

from einstein_projected_lapse_gauge import R


def kinetic(master, u):
    b = (R*u.diff(R)+u-master/(3*R))/4
    a = u-2*b
    c = (R*a.diff(R)+2*a-6*b)/2
    d = (R*b.diff(R)+3*b+c)/2
    return a, b, sp.expand(R**2*(a*a+12*b*b+2*c*c+12*d*d-(a+2*c)**2/2))


def check():
    p, q = sp.symbols("p q", real=True)
    inside = p*R**3
    outside = q*(2-R)
    # Match a=2,b=-3 at r=1 and set outer flux to zero. Give u a
    # regular even polynomial on the ball and a Hermite interpolant outside.
    seam = -4
    slope_inside, slope_outside = -8+p/3, -8+q/3
    inside_u = seam+slope_inside*(R**2-1)/2
    outside_u = sp.interpolate([(1, seam), (2, 0)], R)
    b0, b1 = sp.symbols("b0 b1")
    outside_u += (R-1)*(2-R)*(b0+b1*(R-1))
    outside_u = outside_u.subs(sp.solve([outside_u.diff(R).subs(R, 1)-slope_outside,
                                         outside_u.diff(R).subs(R, 2)], (b0, b1)))
    total, reference = 0, 0
    for master, u, lo, hi in ((inside, inside_u, 0, 1), (outside, outside_u, 1, 2)):
        a, b, density = kinetic(master, u)
        assert sp.simplify(a.subs(R, 1)-2) == 0
        assert sp.simplify(b.subs(R, 1)+3) == 0
        total += sp.integrate(density, (R, lo, hi))
        reference += sp.integrate(master**2/12, (R, lo, hi))
    assert sp.expand(total-reference) == 0
    assert sp.hessian(total, (p, q)).is_positive_definite
    print(f"Two-sided kinetic action with matched nonzero flux: {sp.expand(total)}")


if __name__ == "__main__":
    check()
