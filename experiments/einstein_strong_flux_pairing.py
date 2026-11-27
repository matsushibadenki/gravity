"""Locate the common flux in the strong ADM symplectic form."""

import sympy as sp

from einstein_compatible_momentum_basis import reconstruct
from einstein_projected_lapse_gauge import R, pair


def check():
    radial, angular = sp.symbols("a b")
    flux_symbols = (radial, angular)
    # Isolate the pure flux variations at fixed master momentum. They
    # still solve both momentum constraints and the projected time gauge.
    left_energy, left = reconstruct(sp.S.Zero, radial, angular, 0, 1)
    right_energy, right = reconstruct(sp.S.Zero, radial, angular, 1, 2)
    assert sp.expand(left_energy+right_energy) == 0
    norm = 4*sp.pi/5
    expected = norm*sp.Matrix([[-3, -6], [1, 0]])
    # Use two independent interface lifts in each interval. The first
    # pair has value one and induced trace zero; the second the reverse.
    left_k = R**3*(R**2-1)/2
    right_k = (R-1)*(2-R)
    left_fields = (R**3-6*left_k, left_k)
    right_fields = (2-R-2*right_k, right_k)

    def pullback(momentum, fields, lo, hi):
        a, c = momentum
        coefficients = []
        for psi in fields:
            k = psi.diff(R)+3*psi/R
            h = 6*psi/R-2*k+R*k.diff(R)
            coefficients.append(norm*pair(1, a*h+2*c*k, lo, hi))
        return sp.Matrix(coefficients).jacobian(flux_symbols).applyfunc(sp.simplify)

    one_side = pullback(left, left_fields, 0, 1)
    other_side = pullback(right, right_fields, 1, 2)
    assert one_side == expected and other_side == -expected
    assert one_side.rank() == 2 and one_side + other_side == sp.zeros(2)

    # Pairing with compact interior metric tests vanishes as well.
    assert pullback(left, (R**3*(1-R**2)**2,), 0, 1) == sp.zeros(1, 2)
    assert pullback(right, ((R-1)**2*(2-R)**2,), 1, 2) == sp.zeros(1, 2)
    # The reduced trace prescription used previously cannot be deduced
    # just by identifying f with a function of the bulk master momenta.
    for value in ((2, -3), (0, 0)):
        assert sp.expand((left_energy+right_energy).subs(dict(zip(flux_symbols, value)))) == 0
    # The shift Green identity fixes the generator of independent
    # spatial displacements. For W=(w Y, v D^A Y) its surface term is
    # 2 I_Y(a w + 6 b v). A relative displacement supplies a separate
    # possible conjugate coordinate for the common flux.
    w, v = sp.symbols("delta_w delta_v")
    surface = 2*norm*(radial*w+6*angular*v)
    charge = sp.Matrix([surface.diff(w), surface.diff(v)])
    charge_map = charge.jacobian(flux_symbols)
    assert charge_map.det() == 384*sp.pi**2/25
    assert charge_map.rank() == 2
    print("Independent trace lifts: rank-two flux pairing on each face.")
    print("With both traces matched: pure common flux variations are null in the ADM bulk pullback.")
    print(f"Spatial displacement charge map determinant: {charge_map.det()}")


if __name__ == "__main__":
    check()
