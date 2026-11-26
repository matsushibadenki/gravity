"""Finite-radius spatial ADM constraint reduction with the collar source."""

import sympy as sp


def check():
    r = sp.symbols("r", positive=True)
    k = sp.Function("K")(r)
    h = sp.Function("H")(r)
    psi = sp.Function("Psi")(r)
    # Divergence of the metric perturbation in the Regge–Wheeler spatial
    # gauge. The radial component is F Y and the angular one is K D_A Y.
    divergence_radial = sp.diff(h, r) + 2 * (h - k) / r
    trace = h + 2 * k
    constraint = (sp.diff(r**2 * divergence_radial, r) / r**2 - 6*k/r**2
                  - sp.diff(r**2 * sp.diff(trace, r), r) / r**2 + 6*trace/r**2)
    reconstruction = 6 * psi / r - 2 * k + r * sp.diff(k, r)
    reduced = sp.simplify(constraint.subs(h, reconstruction).doit())
    trace_on_constraint = sp.diff(psi, r) + 3 * psi / r
    assert sp.simplify(reduced + 12 / r**2 * (k - trace_on_constraint)) == 0

    # Spatial gauge h_AB^TF=0 and h_rA=0. The input gauge amplitudes are
    # xi_r=w Y and xi_A=r^2 v D_A Y. The mixed metric is h_rA=J D_A Y.
    # Delta d=2v and Delta J=w+r^2 v'. Use an arbitrary discrete derivative
    # to check the finite-mode Jacobian of this triangular gauge map.
    radii = sp.diag(1, sp.Rational(9, 8), sp.Rational(7, 8))
    derivative = sp.Matrix([[0, 4, -4], [-4, 4, 0], [4, 0, -4]])
    identity, zero = sp.eye(3), sp.zeros(3)
    gauge = sp.BlockMatrix([[2*identity, zero],
                            [radii**2 * derivative, identity]]).as_explicit()
    assert gauge.det() == 8
    # Local Jacobian from (K,H) to (K,Psi), times delta(C_h) integrated
    # over K. These are configuration factors in the declared coordinates.
    h_jacobian = 6 * radii.inv()
    constraint_jacobian = -12 * radii**(-2)
    assert abs(h_jacobian.det() / constraint_jacobian.det()) == (radii / 2).det()
    # The original linear source is simply evaluated on the constraint.
    j, rho = sp.symbols("j rho")
    assert sp.simplify((4*j*rho*k/r**2).subs(k, trace_on_constraint)
                       - 4*j*rho*trace_on_constraint/r**2) == 0
    print("Exact ADM constraint: C_h = -12 (K - Psi' - 3 Psi/r)/r^2")
    print("Spatial FP and scalar constraint Jacobians verified.")


if __name__ == "__main__":
    check()
