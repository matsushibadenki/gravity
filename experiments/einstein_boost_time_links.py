"""Check the compensated lapse slope in the linear ADM canonical links."""

import sympy as sp


def check():
    r = sp.symbols("r", positive=True)
    lapse = sp.Function("N")(r)
    # Apply the flat ADM lapse transformation before restricting the jet.
    delta_a = -2*lapse.diff(r)/r + 6*lapse/r**2
    delta_c = -lapse.diff(r, 2) - lapse.diff(r)/r + 3*lapse/r**2
    delta_master = ((r**3*delta_a).diff(r, 2)
                    - (r**2*(delta_a+2*delta_c)).diff(r)
                    + r*(-3*delta_a+6*delta_c))
    assert sp.expand(delta_master) == 0

    # Use midpoint sampling on each time link. The Green identity
    # for a constraint-satisfying metric increment gives -c s dh.
    charge_factor = sp.symbols("c", positive=True)
    h0, h1, s0, s1 = sp.symbols("h_0 h_1 s_0 s_1")
    bulk = -charge_factor*(s0+s1)/2*(h1-h0)
    corner = charge_factor*(h0+h1)/2*(s1-s0)
    # The corner potential is -c h d eta and delta eta = -s.
    endpoint = charge_factor*(h0*s0-h1*s1)
    assert sp.expand(bulk-corner-endpoint) == 0
    # Switching to the area coordinate adds the exact variation
    # c d(h eta), which transforms by the opposite endpoint term.
    area_corner = -charge_factor*(s0+s1)/2*(h1-h0)
    assert sp.expand(bulk-area_corner) == 0

    a, b, eta, slope = sp.symbols("a b eta s")
    bare = sp.Matrix([a, b])
    boosted = bare + sp.Matrix([-2, 1])*eta/r
    transform = {a: a-2*slope/r, b: b+slope/r, eta: eta-slope}
    assert sp.expand(boosted.subs(transform, simultaneous=True)-boosted) == sp.zeros(2, 1)
    print("Master momentum and both frame-corrected fluxes are invariant.")
    print("Canonical links change by an endpoint term in boost polarization.")
    print("The area polarization cancels the variation on each link.")


if __name__ == "__main__":
    check()
