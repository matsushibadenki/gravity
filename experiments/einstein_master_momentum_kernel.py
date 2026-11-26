"""Even-parity angular constraint and fixed-flux master-momentum kernel."""

import sympy as sp


def check():
    r = sp.symbols("r", positive=True)
    a, c, n = [sp.Function(name)(r) for name in ("a", "c", "N")]
    # Tangential momentum = c Y gamma_AB + d (D_A D_B Y)^TF.
    b = (r*sp.diff(a, r) + 2*a - 2*c)/6
    d = (r*sp.diff(b, r) + 3*b + c)/2
    assert sp.expand(sp.diff(b, r) + (3*b+c-2*d)/r) == 0
    master = sp.expand(sp.diff(r**3*a, r, 2) - sp.diff(r**2*(a+2*c), r)
                       +r*(-3*a+6*c))
    gauge_a = -2*sp.diff(n, r)/r + 6*n/r**2
    gauge_c = -sp.diff(n, r, 2) - sp.diff(n, r)/r + 3*n/r**2
    assert sp.expand(master.subs({a: gauge_a, c: gauge_c}).doit()) == 0
    assert sp.expand(b.subs({a: gauge_a, c: gauge_c}).doit()
                     - sp.diff(n, r)/r + n/r**2) == 0

    # Kernel equation reduced by the radial constraint.
    # P/r^2=(r*a')'+4*a'+(a+2*c)/r-2*c'.
    residual = sp.expand(master/r**2)
    assert sp.expand(residual - (r*sp.diff(a, r, 2) + 5*sp.diff(a, r)
                                + (a+2*c)/r - 2*sp.diff(c, r))) == 0
    # Reconstruct a lapse locally from gauge_a=a. Then c-gauge_c
    # solves e'=e/r. The homogeneous lapse N=t r^3 shifts gauge_c by -6 t r.
    homogeneous = gauge_c.subs(n, r**3).doit()
    assert sp.expand(homogeneous) == -6*r

    # Matching perturbations of both fluxes at one endpoint forces
    # both lapse traces to vanish. No free integration constant remains.
    trace_map = sp.Matrix([[6/r**2, -2/r], [-1/r**2, 1/r]])
    assert sp.simplify(trace_map.det()) == 4/r**3
    u, p = [sp.Function(name)(r) for name in ("u", "P")]
    inverse_b = (r*sp.diff(u, r) + u - p/(3*r))/4
    inverse_a = u - 2*inverse_b
    inverse_c = (r*sp.diff(inverse_a, r) + 2*inverse_a - 6*inverse_b)/2
    assert sp.expand(master.subs({a: inverse_a, c: inverse_c}).doit() - p) == 0
    assert sp.expand(gauge_a + 2*(sp.diff(n, r)/r-n/r**2) - 4*n/r**2) == 0
    print("Angular constraint solved; the master kernel is lapse-generated locally.")
    print("Two fixed fluxes imply zero lapse value and slope at each finite endpoint.")


if __name__ == "__main__":
    check()
