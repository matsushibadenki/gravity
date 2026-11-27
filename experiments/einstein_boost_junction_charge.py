"""Oriented ADM lapse-slope charge and its extended corner pairing."""

import sympy as sp


def check():
    r, newton = sp.symbols("r G", positive=True)
    trace_left, trace_right = sp.symbols("h_L h_R")
    slope_left, slope_right = sp.symbols("s_L s_R")
    boost_left, boost_right = sp.symbols("eta_L eta_R")
    # h is the coefficient of the full induced trace h_A^A = h Y.
    # The trace includes metric and displacement contributions on the seam.
    area_factor = r**2 * (4*sp.pi/5) / (16*sp.pi*newton)
    traces = sp.Matrix([trace_left, trace_right])
    slopes = sp.Matrix([slope_left, slope_right])
    boosts = sp.Matrix([boost_left, boost_right])
    orientation = sp.diag(1, -1)
    common_and_jump = sp.Matrix([[1, sp.Rational(1, 2)],
                                 [1, -sp.Rational(1, 2)]])
    trace_average, trace_jump = sp.symbols("h_bar Delta_h")
    slope_average, slope_jump = sp.symbols("s_bar Delta_s")
    bulk_charge = area_factor * (slopes.T * orientation * traces)[0]
    charge = bulk_charge.subs(dict(zip(
        [*traces, *slopes],
        [*(common_and_jump * sp.Matrix([trace_average, trace_jump])),
         *(common_and_jump * sp.Matrix([slope_average, slope_jump]))],
    )))
    assert sp.expand(
        charge - area_factor * (slope_average*trace_jump + slope_jump*trace_average)
    ) == 0
    assert charge.subs(trace_jump, 0).diff(slope_average) == 0
    assert charge.subs(trace_jump, 0).diff(slope_jump) == area_factor*trace_average

    # With Omega = delta Theta and contraction in the first slot,
    # Theta_corner = -sum orientation * area_charge * delta eta.
    # This uses eta in the reference convention with delta eta = -s.
    corner_mixed = -area_factor * orientation
    corner_contraction = corner_mixed * slopes
    assert corner_contraction + sp.Matrix([bulk_charge.diff(t) for t in traces]) == sp.zeros(2, 1)
    corner_potential = (traces.T * corner_mixed * boosts)[0]
    relative_boost = sp.symbols("Delta_eta")
    assert sp.expand(corner_potential.subs({
        trace_right: trace_left, boost_left: boost_right + relative_boost,
    }) + area_factor*trace_left*relative_boost) == 0
    print("At matched area: common slope charge vanishes; slope jump pairs with shared area.")
    print("With compensating corner boosts: both one-sided slope contractions cancel.")


if __name__ == "__main__":
    check()
