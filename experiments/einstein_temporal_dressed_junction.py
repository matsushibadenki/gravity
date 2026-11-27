"""Rank of the time and boost trace block before and after sewing."""

import sympy as sp


def check():
    r = sp.symbols("r", positive=True)
    # Strip the common I_Y/(16 pi G) normalization.
    trace = sp.Matrix([[-3*r**2, -6*r**2], [r**3, 0]])
    lapse_value = sp.Matrix([6/r**2, -1/r**2])
    lapse_slope = sp.Matrix([-2/r, 1/r])
    jets = lapse_value.row_join(lapse_slope)
    # After integration by parts, the Green and area contributions
    # multiply metric trace variations in the same polarization.
    block = trace.row_join(trace*jets)
    dressed = sp.eye(2).row_join(jets)
    gauge = jets.col_join(-sp.eye(2))
    # The exact cancellation uses beta, not eta, as the variable
    # shifted by minus the slope. Check the alternative jet convention.
    geometric_gauge = gauge.copy()
    geometric_gauge[3, 0] = 1/r
    assert block*geometric_gauge == sp.Matrix([[0, 0], [-2*r, 0]])
    assert block == trace*dressed
    assert gauge.rank() == block.rank() == 2
    assert block*gauge == sp.zeros(2)

    # Independent frame histories lift the common dressed flux on each
    # face. Matching the metric traces then cancels the oriented block.
    shared = sp.eye(2).col_join(sp.eye(2))
    common_flux = sp.eye(2).col_join(sp.zeros(2))
    lift = common_flux.col_join(common_flux).row_join(sp.diag(gauge, gauge))
    assert lift.rank() == 6
    assert sp.diag(dressed, dressed)*lift == shared.row_join(sp.zeros(4))
    assert shared.T*sp.diag(block, -block)*lift == sp.zeros(2, 6)
    assert shared.T*sp.diag(trace, -trace)*shared == sp.zeros(2)

    # A matched flat isometric reference shifts E by -4 A_c/r.
    # In the metric-coordinate polarization the time column changes
    # by -4 dA_c/r. Its residual vanishes only for a common time shift
    # after matching, or upon restriction to fixed area.
    reference_column = sp.Matrix([0, -8*r])
    referenced = block + sp.zeros(2, 2).row_join(
        reference_column.row_join(sp.zeros(2, 1))
    )
    residual = referenced*gauge
    assert residual == sp.Matrix([[0, 0], [8*r, 0]])
    assert referenced*geometric_gauge == sp.Matrix([[0, 0], [6*r, 0]])
    oriented_residual = shared.T*sp.diag(residual, -residual)
    assert oriented_residual*shared == sp.zeros(2)
    assert oriented_residual.rank() == 1
    print("Both orders cancel the shared trace pairing with time and boost retained.")
    print("Flat reference term: rank-one residual for independent compensated time shifts.")


if __name__ == "__main__":
    check()
