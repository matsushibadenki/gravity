"""Exact ADM kinetic density in master momentum and fixed-flux traces."""

import sympy as sp


def check():
    r = sp.symbols("r", positive=True)
    p, u = [sp.Function(name)(r) for name in ("P", "u")]
    b = (r*sp.diff(u, r)+u-p/(3*r))/4
    a = u-2*b
    c = (r*sp.diff(a, r)+2*a-6*b)/2
    d = (r*sp.diff(b, r)+3*b+c)/2
    density = r**2*(a*a+12*b*b+2*c*c+12*d*d-(a+2*c)**2/2)
    endpoint = (-r**5*sp.diff(u, r)**2/8 + r**4*u*sp.diff(u, r)/4
                +5*r**3*u*u/8 + r**3*p*sp.diff(u, r)/12
                -r*r*p*u/12-r*p*p/72)
    assert sp.expand(density-p*p/12-sp.diff(endpoint, r)) == 0
    radial, angular = sp.symbols("a b")
    traces = {u: radial+2*angular,
              sp.diff(u, r): (2*angular-radial+p/(3*r))/r}
    assert sp.expand(endpoint.subs(traces, simultaneous=True)
                     - r**3*(radial**2+12*radial*angular+12*angular**2)/4) == 0

    # A regular master momentum can be represented at the origin with
    # u=0 and P=r^3 times an even radial series. Verify its Cartesian tensor.
    x, y, z = sp.symbols("x y z")
    position = sp.Matrix([x, y, z])
    radius_squared = position.dot(position)
    q = sp.diag(-sp.Rational(1, 2), -sp.Rational(1, 2), 1)
    harmonic = position.dot(q*position)/radius_squared
    normal = position/sp.sqrt(radius_squared)
    projector = sp.eye(3)-normal*normal.T
    gradient = 2*projector*q*normal
    shear = 2*projector*q*projector+harmonic*projector
    for power in (3, 5, 7):
        amplitudes = [sp.expand(item.subs({p: r**power, u: 0}).doit())
                      for item in (a, b, c, d)]
        tensor = sum((coefficient.subs(r, sp.sqrt(radius_squared))*basis
                      for coefficient, basis in zip(amplitudes, (
                          harmonic*normal*normal.T, normal*gradient.T+gradient*normal.T,
                          harmonic*projector, shear))), sp.zeros(3))
        for entry in tensor:
            sp.Poly(sp.cancel(entry), x, y, z)
        assert sp.limit(endpoint.subs({p: r**power, u: 0}).doit(), r, 0) == 0
    g = sp.symbols("G", positive=True)
    norm = 4*sp.pi/5
    kappa = 3/(10*g)
    assert sp.simplify(16*sp.pi*g/(12*norm) - 1/(2*kappa)) == 0
    print("Bulk kinetic density P^2/12. Endpoint depends only on both shift fluxes.")
    print("Regular Cartesian representatives checked for P=r^3,r^5,r^7.")


if __name__ == "__main__":
    check()
