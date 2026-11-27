"""Compare the boosted sphere energy with the ADM kinetic completion."""

import sympy as sp


def check():
    r, g = sp.symbols("r G", positive=True)
    epsilon, a, b, eta, k1, y = sp.symbols("eps a b eta k1 Y", real=True)
    # k and l are the traces along the outward spacelike and future
    # timelike normals. In the ADM convention l = -a Y at first order.
    k = 2/r + epsilon*k1
    l = -epsilon*a*y
    rapidity = epsilon*eta*y
    boosted_k = sp.cosh(rapidity)*k + sp.sinh(rapidity)*l
    second_order = sp.expand(sp.diff(boosted_k-k, epsilon, 2).subs(epsilon, 0)/2)
    assert sp.expand(second_order-y**2*(-a*eta+eta**2/r)) == 0

    # Unit boundary lapse and zero boundary shift. Hold the intrinsic
    # two-metric and any intrinsic reference subtraction fixed.
    harmonic_norm = 4*sp.pi/5
    adm_factor = harmonic_norm/(16*sp.pi*g)
    energy_shift = -r**2*harmonic_norm/(8*sp.pi*g) * second_order.coeff(y, 2)
    bare = r**3*(a**2+12*a*b+12*b**2)/4
    dressed = bare.subs({a: a-2*eta/r, b: b+eta/r}, simultaneous=True)
    assert sp.expand(energy_shift/adm_factor-(dressed-bare)) == 0
    print("Boosted mean-curvature energy reproduces both ADM kinetic completion coefficients.")


if __name__ == "__main__":
    check()
