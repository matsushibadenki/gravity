"""Strong ADM trace pairing at fixed time embedding and master momentum."""

import sympy as sp


def check():
    # Unit reference radius. The common angular and Newton normalization
    # multiplies both the bulk endpoint and the area-polarized corner.
    trace_map = sp.Matrix([[-3, -6], [1, 0]])
    slope_direction = sp.Matrix([-2, 1])
    corner_column = sp.Matrix([0, -2])
    assert trace_map*slope_direction == corner_column
    one_face = trace_map.row_join(corner_column)
    gauge = slope_direction.col_join(sp.Matrix([-1]))
    assert one_face*gauge == sp.zeros(2, 1)
    assert one_face.nullspace() == [-gauge]

    # Coordinates are (Psi, K) on each face, and the momentum-like data
    # are (a, b, eta). Eliminate the boost redundancy before sewing.
    dressed = sp.eye(2).row_join(slope_direction)
    assert one_face == trace_map*dressed
    assert trace_map.det() == 6
    oriented = sp.diag(trace_map, -trace_map)
    shared = sp.eye(2).col_join(sp.eye(2))
    assert (shared.T*oriented).rank() == 2
    assert shared.T*oriented*shared == sp.zeros(2)

    # Equivalently impose the dressed junction first and pull back the
    # original form, allowing independent eta on the two faces.
    boost_lift = (-slope_direction).row_join(sp.zeros(2, 1)).col_join(
        sp.Matrix([[1, 0]])
    )
    right_boost_lift = boost_lift[:, ::-1]
    dressed_lift = dressed[:, :2].col_join(sp.zeros(1, 2))
    junction_lift = dressed_lift.row_join(boost_lift).col_join(
        dressed_lift.row_join(right_boost_lift)
    )
    assert sp.diag(dressed, dressed)*junction_lift == shared.row_join(sp.zeros(4, 2))
    assert junction_lift.rank() == 4
    assert shared.T*sp.diag(one_face, -one_face)*junction_lift == sp.zeros(2, 4)
    print("One-face dressed trace pairing has rank two.")
    print("Both orders give zero shared trace–flux pairing in this sector.")


if __name__ == "__main__":
    check()
