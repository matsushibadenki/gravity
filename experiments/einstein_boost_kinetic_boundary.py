"""Test the ADM kinetic surface term under compensated lapse slopes."""

import sympy as sp


def check():
    radius = sp.symbols("r", positive=True)
    a, b, eta, slope = sp.symbols("a b eta s", real=True)

    def surface(radial, angular):
        return radius**3 * (radial**2 + 12*radial*angular + 12*angular**2)/4

    # The bulk P^2/12 term is invariant by the canonical-link check.
    # Here T is held fixed at zero since the surface lapse vanishes.
    transform = {a: a-2*slope/radius, b: b+slope/radius, eta: eta-slope}
    bare = surface(a, b)
    change = sp.expand(bare.subs(transform, simultaneous=True)-bare)
    assert change == 2*radius**2*a*slope-2*radius*slope**2

    dressed = surface(a-2*eta/radius, b+eta/radius)
    completion = sp.expand(dressed-bare)
    assert completion == 2*radius**2*a*eta-2*radius*eta**2
    assert sp.expand(dressed.subs(transform, simultaneous=True)-dressed) == 0

    left_slope, right_slope = sp.symbols("s_L s_R")
    sewn_change = sp.factor(change.subs(slope, left_slope)
                           - change.subs(slope, right_slope))
    assert sewn_change == 2*radius*(left_slope-right_slope)*(
        a*radius-left_slope-right_slope
    )
    assert sewn_change.subs(right_slope, left_slope) == 0

    print("Bare ADM surface energy changes for independent face slopes.")
    print("The common slope cancels for matched bare traces.")
    print("The frame completion cancels each face variation at T=0.")


if __name__ == "__main__":
    check()
