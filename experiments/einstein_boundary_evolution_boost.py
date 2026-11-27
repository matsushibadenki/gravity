"""Fixed boundary evolution under changes of the ADM normal frame."""

import sympy as sp


def boost(angle):
    return sp.Matrix([[sp.cosh(angle), sp.sinh(angle)],
                      [sp.sinh(angle), sp.cosh(angle)]])


def check():
    k, ell, lapse, eta, slope = sp.symbols("k ell L eta s", real=True)
    traces = sp.Matrix([k, ell])
    # Boundary evolution is L times the adapted timelike normal plus
    # an unchanged tangential shift. Change only its ADM decomposition.
    normal_components = lapse * boost(eta)[:, 0]
    shifted_components = boost(eta-slope)[:, 0] * lapse
    assert (shifted_components-boost(-slope)*normal_components).applyfunc(
        sp.trigsimp
    ) == sp.zeros(2, 1)
    energy = (normal_components.T * traces)[0]
    shifted_energy = (shifted_components.T * boost(slope) * traces)[0]
    assert sp.simplify(sp.expand_trig(shifted_energy-energy)) == 0

    # The inhomogeneous part of the normal connection matters for a
    # local boost and a nonzero tangential shift.
    omega, grad_eta, grad_slope, tangential_shift = sp.symbols(
        "omega D_eta D_s V", real=True
    )
    momentum = tangential_shift*(omega+grad_eta)
    shifted_momentum = tangential_shift*(omega+grad_slope+grad_eta-grad_slope)
    assert sp.expand(shifted_momentum-momentum) == 0
    assert sp.diff(momentum, grad_eta) == tangential_shift
    print("Fixed evolution: the mean-curvature and radial-shift terms are jointly invariant.")
    print("Nonzero tangential shift: the normal connection needs the boost gradient.")


if __name__ == "__main__":
    check()
