"""Compute the kinetic norm of a collar-averaged induced trace."""

import sympy as sp


def check():
    x = sp.symbols("x", real=True)
    radius, width = sp.symbols("R h", positive=True)
    shape = 3*(1-x**2)/4
    radial_position = radius+width*x
    weight = shape/width
    derivative = shape.diff(x)/width**2
    representative = -derivative+3*weight/radial_position

    # Integration by parts converts the cross term in the squared norm.
    difference = representative**2-derivative**2-6*weight**2/radial_position**2
    assert sp.simplify(width*difference+3*(weight**2/radial_position).diff(x)) == 0
    assert all(weight.subs(x, end) == 0 for end in (-1, 1))

    derivative_norm = sp.integrate(width*derivative**2, (x, -1, 1))
    assert derivative_norm == 3/(2*width**3)
    # Use the same unit reference radius and half-width as the curvature
    # source experiment. This defines a control for an averaged trace.
    fixed = {radius: 1, width: sp.Rational(1, 8)}
    area_term = sp.integrate(
        (6*width*weight**2/radial_position**2).subs(fixed), (x, -1, 1)
    )
    norm = sp.simplify(derivative_norm.subs(fixed)+area_term)
    assert 768 < norm.evalf() < 800
    # Averaging the whole thin-sphere potential instead retains its
    # geometric radius factor C(r) proportional to r.
    geometric_representative = -radial_position*derivative+2*weight
    geometric_norm = sp.integrate(width*geometric_representative**2, (x, -1, 1))
    assert sp.simplify(geometric_norm-3*radius**2/(2*width**3)
                       -9/(2*width)) == 0
    assert geometric_norm.subs(fixed) == 804
    print("Radius-weighted thin-sphere average: squared kinetic norm = 804.")
    print(f"R=1, h=1/8: squared kinetic norm = {norm.evalf(12)}")
    print("Relative-time kinetic curvature is this norm times C^2/kappa.")


if __name__ == "__main__":
    check()
