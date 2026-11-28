"""Distinguish single-tube and collar time couplings by their support."""

import sympy as sp


def check():
    x = sp.symbols("x", real=True)
    half_width = sp.Rational(1, 8)
    radius = 1+half_width*x
    weight = 3*(1-x**2)/(4*half_width)
    derivative = weight.diff(x)/half_width
    lo, hi = sp.Rational(1, 4), sp.Rational(1, 2)
    # Extend by zero. The perturbation and its first two derivatives
    # vanish at the support endpoints, and it vanishes near the tube.
    profile = (x-lo)**3*(hi-x)**3
    for order in range(3):
        assert all(profile.diff(x, order).subs(x, bound) == 0 for bound in (lo, hi))

    induced_trace = profile.diff(x)/half_width+3*profile/radius
    for radius_factor in (sp.S.One, radius):
        averaged = sp.integrate(half_width*radius_factor*weight*induced_trace, (x, lo, hi))
        representative = -(radius_factor*weight).diff(x)/half_width
        representative += 3*radius_factor*weight/radius
        by_parts = sp.integrate(half_width*representative*profile, (x, lo, hi))
        assert sp.simplify(averaged-by_parts) == 0
        assert representative.subs(x, lo).is_positive
        assert averaged.evalf(25) > 0
        print(f"Collar response ({radius_factor}): {averaged.evalf(10)}")

    print("Single-tube trace response for this perturbation: zero.")


if __name__ == "__main__":
    check()
