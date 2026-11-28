"""Check the temporal multiplier block of a tilted ADM junction."""

import sympy as sp

from einstein_sharp_time_cutoff import trace_norm


def check():
    k, ell, rapidity, lapse = sp.symbols("k ell eta L", real=True)
    # The normal components of a fixed evolution vector are ADM lapse
    # and radial shift. The temporal charge is their contraction with
    # the spacelike and timelike mean-curvature traces.
    normal_charge = lapse*(sp.cosh(rapidity)*k+sp.sinh(rapidity)*ell)
    assert normal_charge.diff(lapse).subs(rapidity, 0) == k

    newton = sp.symbols("G", positive=True)
    psi, area = sp.symbols("Psi K")
    energy = (4*area-6*psi)/(10*newton)
    # Independent time embeddings and momenta, prior to matching.
    left_time, right_time, left_p, right_p = sp.symbols("T_L T_R pi_L pi_R")
    next_left, next_right, step = sp.symbols("T_L_next T_R_next dt")
    energy_left, energy_right = sp.symbols("E_L E_R")
    phase = left_p*(next_left-left_time)-right_p*(next_right-right_time)
    link = phase-step*lapse*(energy_left-energy_right)
    assert -link.diff(lapse)/step == energy_left-energy_right
    matched_phase = phase.subs({left_p: -energy, right_p: -energy})
    assert sp.expand(matched_phase+energy*(next_left-next_right-left_time+right_time)) == 0
    poisson = sp.Matrix([[0, 0, 1, 0], [0, 0, 0, -1],
                         [-1, 0, 0, 0], [0, 1, 0, 0]])
    coordinates = (left_time, right_time, left_p, right_p)
    # Conditional test with a smooth shared cut and a fixed common clock.
    # These two clock rows are supplied as conditions in this block.
    constraints = sp.Matrix([left_p+energy, right_p+energy,
                             left_time-right_time, (left_time+right_time)/2])
    rows = constraints.jacobian(coordinates)
    bracket = rows*poisson*rows.T
    assert bracket.det() == 1
    assert abs(rows.det()) == 1

    # On independent geometrical traces the common boundary lapse
    # constrains the oriented energy jump. After imposing both trace
    # matches its row is redundant. Do not count it twice.
    delta_psi, delta_area = sp.symbols("Delta_Psi Delta_K")
    jump = energy.subs({psi: delta_psi, area: delta_area})
    geometric_rows = sp.Matrix([delta_area, jump]).jacobian((delta_psi, delta_area))
    assert geometric_rows.det() == 3/(5*newton)
    duplicated_rows = geometric_rows.col_join(sp.Matrix([[1, 0]]))
    assert len(duplicated_rows.T.nullspace()) == 1
    print("Conditional temporal bracket determinant and coordinate Jacobian: 1.")
    print("Common lapse charge row is redundant if both metric traces are matched.")

    # No explicit radiative momentum occurs in this charge definition.
    # These are direct Hessian entries at fixed traces and multipliers,
    # before eliminating any lapse, shift or embedding constraint.
    radiative_p = sp.Symbol("p")
    assert energy.diff(left_time, radiative_p) == energy.diff(left_time, 2) == 0
    for order in (2, 4, 8, 12, 16):
        print(f"N={order:2d}: required time Hessian / (C^2/kappa) = "
              f"{trace_norm(order).evalf(12)}")


if __name__ == "__main__":
    check()
