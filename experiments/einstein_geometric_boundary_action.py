"""Static Euclidean Einstein–GHY action in the spatial induced metric gauge."""

import sympy as sp


def check():
    r, epsilon, y = sp.symbols("r epsilon Y", real=True)
    h, k, derivative = sp.symbols("H K K_prime", real=True)
    radial_lapse = sp.sqrt(1 + epsilon * h * y)
    sphere_factor = 1 + epsilon * k * y

    # sqrt(q) R[q] = 2 - Delta log(1 + epsilon K Y), up to the
    # unit-sphere measure. Only its linear part couples to the lapse
    # perturbation. The unweighted angular Laplacian integrates to zero.
    intrinsic = radial_lapse * (2 + 6 * epsilon * k * y)
    extrinsic = (2 * sphere_factor / radial_lapse
                 * (1 + r * epsilon * derivative * y / (2 * sphere_factor))**2)
    quadratic = sp.expand(sp.series(intrinsic + extrinsic, epsilon, 0, 3)
                          .removeO()).coeff(epsilon, 2).coeff(y, 2)
    assert sp.expand(quadratic - ((h-r*derivative)**2/2 + 2*h*k)) == 0

    psi = sp.Function("Psi")(r)
    trace = sp.diff(psi, r) + 3*psi/r
    constrained = quadratic.subs({h: 6*psi/r - 2*trace + r*sp.diff(trace, r),
                                   k: trace, derivative: sp.diff(trace, r)})
    bulk = 3*(sp.diff(psi, r)**2 + 6*psi**2/r**2)
    endpoint = 9*psi**2/r - r*trace**2
    # The Euclidean Einstein action has the overall minus sign.
    assert sp.simplify(-constrained - bulk - sp.diff(endpoint, r)) == 0
    print("Static ADM–GHY endpoint term: kappa/6 * (9 Psi^2/r - r K^2).")

    field, fixed, radius, kappa, source_flux = sp.symbols("psi K r kappa B")
    geometric = kappa/6 * (9*field**2/radius - radius*fixed**2)
    generating = -kappa*field*fixed + 3*kappa*field**2/(2*radius) + source_flux*field
    difference = sp.expand(geometric - generating)
    assert sp.diff(difference, field) == kappa*fixed - source_flux
    print("Difference from the reduced fixed-K completion has slope kappa*K - B.")


if __name__ == "__main__":
    check()
