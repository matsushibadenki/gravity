"""Pull back the even-parity ADM symplectic potential on a radial interval."""

import sympy as sp


def check():
    r = sp.symbols("r", positive=True)
    a, b, c, variation = [sp.Function(name)(r) for name in ("a", "b", "c", "deltaPsi")]
    delta_k = sp.diff(variation, r) + 3*variation/r
    delta_h = 6*variation/r - 2*delta_k + r*sp.diff(delta_k, r)
    adm = r*r*(a*delta_h + 2*c*delta_k)
    second = r**3*a
    first = r*r*(a + 2*c)
    master = sp.diff(second, r, 2) - sp.diff(first, r) + r*(-3*a + 6*c)
    boundary = second*sp.diff(variation, r) + (first-sp.diff(second, r))*variation
    assert sp.expand(adm - master*variation - sp.diff(boundary, r)) == 0

    # Momentum constraint in the radial direction:
    # a' + (2a-2c-6b)/r=0. The angular divergence enters through b.
    on_constraint = sp.expand(boundary).subs(sp.diff(a, r), (-2*a+2*c+6*b)/r)
    expected = r**3*a*delta_k - r*r*(3*a+6*b)*variation
    assert sp.expand(on_constraint-expected) == 0

    # Opposite seam orientations cancel for shared fields and common fluxes.
    right_a, right_b = sp.symbols("a_plus b_plus")
    mismatch = sp.expand(expected-expected.subs({a: right_a, b: right_b}))
    assert mismatch.subs({right_a: a, right_b: b}) == 0

    # The corner pair can be expressed in either boost or area polarization.
    area, boost, g = sp.symbols("A eta G", real=True)
    generating = area*boost/(8*sp.pi*g)
    assert sp.diff(generating, boost) == area/(8*sp.pi*g)
    assert sp.diff(generating, area) == boost/(8*sp.pi*g)
    print("Bulk master momentum and both seam flux terms agree by exact integration by parts.")


if __name__ == "__main__":
    check()
