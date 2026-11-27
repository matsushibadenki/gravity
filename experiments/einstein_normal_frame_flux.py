"""Linear quadrupole fluxes in a displaced and boosted sphere frame."""

import sympy as sp


def check():
    r = sp.symbols("r", positive=True)
    lapse, slope, time, boost = sp.symbols("N N_r T eta")
    a, b = sp.symbols("a b")
    # In the ADM convention of the master kernel, K_A^A = -a Y.
    # A time graph contributes Delta_S T to K_A^A, and a boost of
    # the future normal toward the radial normal adds 2 eta/r.
    # The normal connection acquires D_A(eta - T/r).
    bare = sp.Matrix([a, b])
    frame = sp.Matrix([time, boost])
    jet_map = sp.Matrix([[6/r**2, -2/r], [-1/r**2, 1/r]])
    dressed = bare + jet_map * frame
    jet = sp.Matrix([lapse, slope])
    assert sp.simplify(jet_map.det()) == 4/r**3
    variation = dressed.jacobian(bare) * jet_map * jet - dressed.jacobian(frame) * jet
    assert variation == sp.zeros(2, 1)

    # For a surface-fixed lapse the slope still acts on both bare fluxes
    # when boosts are included in the gauge transformation.
    slope_response = jet_map[:, 1]
    assert slope_response.rank() == 1
    boost_invariant = sp.Matrix([[1, 2]])
    assert boost_invariant * slope_response == sp.zeros(1, 1)
    assert sp.simplify((boost_invariant * dressed)[0]
                       - (a + 2*b + 4*time/r**2)) == 0

    # Use the same radial reference direction on both faces. Reversing
    # the outward normal reverses the connection component.
    left, right = sp.Matrix(sp.symbols("T_L eta_L")), sp.Matrix(sp.symbols("T_R eta_R"))
    flux_jump = sp.Matrix(sp.symbols("delta_a delta_b"))
    junction = flux_jump + jet_map * (left - right)
    assert junction.jacobian(tuple(left)).rank() == 2
    assert sp.simplify(junction.subs(dict(zip(flux_jump, sp.zeros(2, 1))))
                       - jet_map * (left-right)) == sp.zeros(2, 1)
    print("Dressed flux jet map: rank 2, determinant 4/r^3.")
    print("Surface-fixed lapse: one boost-independent bare combination, a + 2 b.")
    print("Dressed junction: equal bare fluxes fix the relative time and boost in this block.")


if __name__ == "__main__":
    check()
