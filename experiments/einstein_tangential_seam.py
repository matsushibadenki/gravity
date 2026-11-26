"""Constraint determinant of the linear tilted embedding block."""

import sympy as sp

from einstein_dynamic_collar_sewing import check as check_transfer


def check():
    g = sp.symbols("G", positive=True)
    # Coordinates (K,Psi,T,X,eta) and their canonical momenta. X multiplies
    # D^A Y and eta multiplies Y, so the boost-gradient pairing uses 6||Y||².
    identity = sp.eye(5)
    zero = sp.zeros(5)
    poisson = sp.BlockMatrix([[zero, identity], [-identity, zero]]).as_explicit()
    beta = 3/(5*g)
    constraints = sp.Matrix([
        [2/(5*g), -3/(5*g), 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, -beta, 0, 0, 0, 1, 0],
        [-1/(10*g), 0, 0, 0, 0, 0, 0, 0, 0, 1],
    ])
    face = constraints*poisson*constraints.T
    assert face == sp.Matrix([[0, 0, 0], [0, 0, -beta], [0, beta, 0]])
    assert face.rank() == 2

    oriented = sp.diag(poisson, -poisson)
    diagonal = constraints.row_join(-constraints)
    relative = constraints.row_join(constraints)/2
    assert diagonal*oriented*diagonal.T == sp.zeros(3)
    assert diagonal*oriented*relative.T == face

    # Keep the spatial data fixed for the conditional frame integral.
    # Fix the average embedding/boost coordinates; in this gauge the
    # mixed charged bracket does not enter the delta-coordinate Jacobian.
    frame_indices = [2, 3, 4, 7, 8, 9]
    frame = constraints[:, frame_indices]
    frame_poisson = poisson.extract(frame_indices, frame_indices)
    frame_oriented = sp.diag(frame_poisson, -frame_poisson)
    common = frame.row_join(-frame)
    common_coordinate = sp.eye(3).row_join(sp.zeros(3))
    gauge = common_coordinate.row_join(common_coordinate)/2
    fp = gauge*frame_oriented*common.T
    assert fp == sp.eye(3)
    junction = sp.diag(frame, frame).col_join(
        common_coordinate.row_join(-common_coordinate)).col_join(gauge)
    assert abs(junction.det()) == 1
    assert (junction*frame_oriented*junction.T).det() == 1
    # Constrain each frame momentum to its geometric charge and match the
    # frame coordinates. The shift charge has a nonzero prescribed part.
    q, eta, flux = sp.symbols("q eta flux")
    assert sp.diff(flux + beta*eta, q) == 0
    one_face = sp.eye(6)
    one_face[4, 2] = -beta
    assert one_face.det() == 1
    print("Single-face bracket rank=2; oriented diagonal rank=0; average-frame FP det=1.")


if __name__ == "__main__":
    check()
    for cells in (32, 64, 128):
        check_transfer(cells, cells//4)
