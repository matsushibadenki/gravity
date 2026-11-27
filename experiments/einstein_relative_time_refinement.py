"""Bound the time–area kinetic coefficient under radial refinement."""

import sympy as sp


def check():
    width, radius, kappa = sp.symbols("h R kappa", positive=True)
    coupling = sp.symbols("C", nonzero=True, real=True)
    x = sp.symbols("x", real=True)

    # psi = h*x*(1-x^2)^3 on |x| <= 1, with x=(r-R)/h.
    # Zero extension is C^2. For h<R it vanishes near the origin.
    shape = x*(1-x**2)**3
    assert shape.subs(x, 0) == 0 and shape.diff(x).subs(x, 0) == 1
    for order in range(3):
        assert all(shape.diff(x, order).subs(x, end) == 0 for end in (-1, 1))

    # The induced trace K=psi'+3 psi/R is one for this test direction.
    trace = shape.diff(x).subs(x, 0) + 3*width*shape.subs(x, 0)/radius
    norm_squared = width**3*sp.integrate(shape**2, (x, -1, 1))
    lower_bound = sp.factor(coupling**2*trace**2/(kappa*norm_squared))
    assert lower_bound == 45045*coupling**2/(2048*kappa*width**3)
    assert sp.simplify(lower_bound.subs(width, width/2)/lower_bound) == 8
    # A fixed-width averaged trace instead has an L2 representative.
    # Normalize a parabolic collar and compute its derivative norm.
    weight_shape = 3*(1-x**2)/4
    assert sp.integrate(weight_shape, (x, -1, 1)) == 1
    assert sp.integrate(weight_shape.diff(x)**2, (x, -1, 1)) == sp.Rational(3, 2)
    print("A fixed-width parabolic collar has finite derivative norm 3/(2 h^3).")
    print("Area-trace dual norm gives a kinetic curvature lower bound:")
    print(lower_bound)


if __name__ == "__main__":
    check()
