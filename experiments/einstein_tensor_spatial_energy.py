"""Flat-slice Einstein spatial Hessian with radial GHY endpoints."""

import numpy as np
from numpy.polynomial.legendre import leggauss


def spatial_hessian(order, lo, hi, inverse_cholesky):
    """Same whitened Cartesian tensor coordinates as the joint ADM control."""
    powers = np.arange(order+3)*2
    n = 4*len(powers)
    energy = np.zeros((n, n))
    # Gauss exactness for products of monomials through degree 4*order+16.
    nodes, weights = leggauss(2*order+10)
    for node, weight in zip(nodes, weights):
        r = lo+(hi-lo)*(node+1)/2
        common = r**powers
        # Components in the order Y I, Q, sym(x Qx), Y xx.
        def row(entries):
            return (common[:, None]*np.array(entries)).ravel()
        h = row([r*r, 1, 2*r*r, r**4])
        c = row([r*r, -.5, 0, 0])
        d = row([0, .5, 0, 0])
        b = row([0, .5, r*r/2, 0])
        rc = c*(np.repeat(powers, 4)+np.tile([2, 0, 2, 4], len(powers)))
        rd = d*np.repeat(powers, 4)
        # Angular integral of N sqrt(q) [R[q] + k^2 - k_AB k^AB]
        # at second order, divided by the norm of the quadrupole.
        rc, h, b, rd, d, c = (inverse_cholesky @ component
                              for component in (rc, h, b, rd, d, c))
        outer = np.outer
        form = (outer(rc-h, rc-h)/2 + 6*outer(rc-h, b)
                - 3*outer(rd, rd) + 12*outer(rd, b-d)
                + 2*outer(h, c+3*d) + 6*outer(b, b) - 6*outer(d, d))
        energy += weight*(form+form.T)/2
    energy *= (hi-lo)/2 * (4/5)  # radial Jacobian and I_Y/pi
    # G=1. The Einstein action prefactor for integrals divided by pi
    # is 1/16, and the Hessian is twice the quadratic coefficient.
    return -energy/8


def check_angular_expansion():
    """Re-expand the radial Einstein–GHY density before angular integration."""
    import sympy as sp
    x = sp.Symbol("cos_theta")
    h, c, b, d, rc, rd = sp.symbols("H K b d rKprime rdprime")
    y = (3*x*x-1)/2
    shear = 3*(1-x*x)/2
    # Diagonal angular metric perturbations and first-order radial
    # extrinsic numerator after subtracting the Lie derivative of the shift.
    a, e = c*y+d*shear, c*y-d*shear
    u = a+(rc*y+rd*shear)/2-b*(3-6*x*x)
    v = e+(rc*y-rd*shear)/2+3*b*x*x
    shift_connection = b*(3*x*(1-x*x)*(a-e).diff(x)/2+3*x*x*(e-a))
    shift_squared = 9*b*b*x*x*(1-x*x)
    intrinsic = -(h*y)**2/4-shift_squared+h*(6*c+12*d)*y*y/2
    extrinsic = 2*(u*v+shift_connection-(u+v)*(h*y+a+e)/2
                   +3*(h*y)**2/8+shift_squared/2
                   +3*(a*a+e*e)/8+a*e/4+h*y*(a+e)/4)
    integrated = 5*sp.integrate(sp.expand(intrinsic+extrinsic), (x, -1, 1))/2
    expected = ((rc-h)**2/2+6*(rc-h)*b-3*rd**2+12*rd*(b-d)
                +2*h*(c+3*d)+6*b**2-6*d**2)
    assert sp.expand(integrated-expected) == 0
    assert sp.expand(integrated.subs({d: 0, rd: 0, b: 0})
                     -(h-rc)**2/2-2*h*c) == 0


if __name__ == "__main__":
    check_angular_expansion()
