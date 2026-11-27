"""Express proper-lapse trace invariants in master momentum and seam fluxes."""

import sympy as sp


def check():
    r = sp.symbols("r", positive=True)
    a, b = (sp.Function(name)(r) for name in ("a", "b"))
    c = (r*a.diff(r)+2*a-6*b)/2
    master = (r**3*a).diff(r, 2)-(r**2*(a+2*c)).diff(r)+r*(-3*a+6*c)
    u = a+2*b
    for harmonic, expected_kernel in ((r**2, r**3/6), (r**-3, r**-2)):
        auxiliary = r**2*(r*harmonic.diff(r)-3*harmonic)/2
        endpoint = r**3*harmonic*a+r*auxiliary*u
        kernel = -auxiliary/(3*r)
        assert sp.factor(kernel-expected_kernel) == 0
        assert sp.expand(r**2*harmonic*(a+2*c)-endpoint.diff(r)-kernel*master) == 0

        # Nonzero equal seam flux is permitted. The moment can still
        # vary through P, without any variation of the two flux traces.
        radius_one = endpoint.subs(r, 1).subs({a.subs(r, 1): 2, b.subs(r, 1): -3})
        print(f"harmonic={harmonic}: seam contribution={radius_one}, master kernel={kernel}")

    # Regular centre: a and b finite, regular harmonic endpoint vanishes.
    regular = r**5*(a/2-b)
    assert sp.limit(regular.subs({a: 2, b: -3}), r, 0) == 0
    # Linear temporal gauge: subtract the harmonic-moment representative
    # from the trace. The remaining source admits zero value and slope.
    # Example regular profile with zero r^2 harmonic moment on [0,1].
    trace = r**4-sp.Rational(7, 9)*r**2
    assert sp.integrate(r**4*trace, (r, 0, 1)) == 0
    lapse = -r**6/72+r**4/36-r**2/72
    laplace = lapse.diff(r, 2)+2*lapse.diff(r)/r-6*lapse/r**2
    assert sp.expand(trace+2*laplace) == 0
    assert lapse.subs(r, 1) == lapse.diff(r).subs(r, 1) == 0
    print("Zero-moment ball example admits trace removal with both proper lapse conditions.")


if __name__ == "__main__":
    check()
