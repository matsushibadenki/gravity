"""Joint constrained endpoint and tilted frame determinant in the linear model."""

import sympy as sp


def check(temporal_graph=False):
    g = sp.symbols("G", positive=True)
    unit = sp.eye(5)
    zero = sp.zeros(5)
    canonical = sp.BlockMatrix([[zero, unit], [-unit, zero]]).as_explicit()
    oriented = sp.diag(canonical, -canonical)
    # (Psi, K, T, X, eta; conjugate momenta) on each face.
    m = (4*sp.pi/5)*sp.Matrix([[-3, -6], [1, 0]])
    flux = sp.zeros(2, 5).row_join(m.inv().row_join(sp.zeros(2, 3)))
    charge = sp.Matrix([[0, 1], [-3/(5*g), 2/(5*g)]]).row_join(sp.zeros(2, 8))
    frame = sp.Matrix([
        [-3/(5*g), 2/(5*g), 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, -3/(5*g), 0, 0, 0, 1, 0],
        [0, -1/(10*g), 0, 0, 0, 0, 0, 0, 0, 1],
    ])
    if temporal_graph:
        frame[1, 2] = 3/(5*g)
    frame_bracket = frame*canonical*frame.T
    if temporal_graph:
        assert frame_bracket[0, 1] == -3/(5*g)
    position = unit[2:, :].row_join(sp.zeros(3, 5))
    conditions = sp.diag(frame, frame)
    conditions = conditions.col_join(position.row_join(-position))
    conditions = conditions.col_join(position.row_join(position)/2)
    conditions = conditions.col_join(charge.row_join(-charge))
    conditions = conditions.col_join(flux.row_join(flux)/2)
    bracket = conditions*oriented*conditions.T
    # Physical flux conditioning mixes with frame momentum definitions.
    mixed = bracket[:6, -2:]
    assert mixed.rank() == 2
    assert bracket.rank() == 16
    factor = sp.sqrt(sp.factor(bracket.det()))
    expected = sp.simplify(charge[:, :2].det()/m.det())
    assert sp.simplify(factor-expected) == 0

    # Retain shared metric and relative canonical momentum. The affine
    # values of the two flux conditions need not vanish.
    q = unit[:2, :].row_join(sp.zeros(2, 5))
    p = sp.zeros(2, 5).row_join(unit[:2, :])
    retained = (q.row_join(q)/2).col_join(p.row_join(-p))
    coordinates = conditions.col_join(retained)
    assert sp.simplify(factor/abs(coordinates.det())) == 1
    dirac = oriented - oriented*conditions.T*bracket.inv()*conditions*oriented
    expected_poisson = sp.BlockMatrix([
        [sp.zeros(2), sp.eye(2)], [-sp.eye(2), sp.zeros(2)]]).as_explicit()
    assert (retained*dirac*retained.T).applyfunc(sp.simplify) == expected_poisson
    rhs = sp.zeros(20, 1)
    rhs[14:16, 0] = sp.Matrix([2, -3])
    point = coordinates.inv()*rhs
    assert conditions[-2:, :]*point == sp.Matrix([2, -3])
    print(f"mixed rank={mixed.rank()}, full rank={bracket.rank()}, density={factor}, ratio=1")


if __name__ == "__main__":
    check()
    check(temporal_graph=True)
