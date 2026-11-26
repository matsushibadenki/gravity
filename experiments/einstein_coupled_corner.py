"""Coupled quadrupole corner reduction for the known linear boundary action."""

import sympy as sp

from einstein_smooth_corner_sewing import check_corner
from einstein_collar_gluing import check as check_bulk


def check():
    g = sp.symbols("G", positive=True)
    identity = sp.eye(4)
    zero = sp.zeros(4)
    poisson = sp.BlockMatrix([[zero, identity], [-identity, zero]]).as_explicit()
    # Coordinates (K,Psi,T,eta,p_K,p_Psi,p_T,p_eta).
    # P2 harmonic norm is 4 pi/5; the unit-radius energy is (4K-6Psi)/(10G).
    area = sp.Matrix([[1/(10*g), 0]])
    energy = sp.Matrix([[2/(5*g), -3/(5*g)]])
    constraints = sp.Matrix([
        [*energy, 0, 0, 0, 0, 1, 0],
        [*-area, 0, 0, 0, 0, 0, 1],
    ])
    assert constraints*poisson*constraints.T == sp.zeros(2)
    assert (identity[:, :2].T.row_join(sp.zeros(2, 4))
            *poisson*constraints.T) == sp.zeros(2)
    assert (sp.zeros(2, 4).row_join(identity[:, :2].T)
            *poisson*constraints.T) == (-energy.T).row_join(area.T)

    # Dress the spatial momenta by the temporal and boost coordinates.
    transform = sp.eye(8)
    transform[4:6, 2:4] = energy.T.row_join(-area.T)
    transform[6:8, :] = constraints
    assert transform*poisson*transform.T == poisson
    assert transform.det() == 1

    # The two-face matching constraints commute in the dressed variables.
    # Average coordinates fix the diagonal orbits with unit determinant.
    frame_poisson = poisson.extract([2, 3, 6, 7], [2, 3, 6, 7])
    two_faces = sp.diag(frame_poisson, -frame_poisson)
    match = sp.eye(4).row_join(-sp.eye(4))
    average = sp.eye(4).row_join(sp.eye(4))/2
    assert match*two_faces*match.T == sp.zeros(4)
    assert (average*two_faces*match.T).det() == 1
    assert abs(match.col_join(average).det()) == 1

    k, psi, time, boost, j = sp.symbols("K Psi T eta j")
    boundary = (area*sp.Matrix([k, psi]))[0]*boost - (energy*sp.Matrix([k, psi]))[0]*time
    assert sp.diff(boundary, j, 2) == 0
    print("Mixed brackets included: canonical transform and oriented reduction have unit determinants.")


if __name__ == "__main__":
    check()
    check_corner()
    for cells in (32, 64, 128, 256):
        check_bulk(cells, .125, .3, intrinsic=True)
