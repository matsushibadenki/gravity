"""Pull back the strong trace form with the fixed-tube lapse jet."""

import sympy as sp


def check():
    r, g = sp.symbols("r G", positive=True)
    normalization = 1/(20*g)
    trace_map = sp.Matrix([[-3*r**2, -6*r**2], [r**3, 0]])
    value = sp.Matrix([6/r**2, -1/r**2])
    slope = sp.Matrix([-2/r, 1/r])
    # In the original boost coordinate the geometric dressed trace is
    # f + value*T + slope*eta. The Green potential uses beta=eta-T/r.
    for reference_shift, coefficient in ((0, 2*r), (-8*r, -6*r)):
        extra_time = -trace_map*slope/r + sp.Matrix([0, reference_shift])
        assert extra_time == sp.Matrix([0, coefficient])
        original = trace_map.row_join(
            (trace_map*value+extra_time).row_join(trace_map*slope)
        )

        # Columns are common dressed fluxes, common/relative time,
        # and two independent boosts. Solve the dressed match for f.
        time_left = sp.Matrix([[0, 0, 1, sp.Rational(1, 2), 0, 0]])
        time_right = sp.Matrix([[0, 0, 1, -sp.Rational(1, 2), 0, 0]])
        shared_flux = sp.eye(2).row_join(sp.zeros(2, 4))
        faces = []
        for time, index in ((time_left, 4), (time_right, 5)):
            eta = sp.eye(6)[index, :]
            bare_flux = shared_flux-value*time-slope*eta
            faces.append(original*bare_flux.col_join(time).col_join(eta))
        sewn = normalization*(faces[0]-faces[1])
        expected = sp.zeros(2, 6)
        expected[1, 3] = normalization*coefficient
        assert sewn == expected
        assert sewn.rank() == 1
        print(f"Reference shift {reference_shift}: p_K = ({normalization*coefficient}) Delta T")


if __name__ == "__main__":
    check()
