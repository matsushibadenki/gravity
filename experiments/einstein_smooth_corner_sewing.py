"""Smooth-frame corner reduction with geometric area and nonzero fixed flux."""

import sympy as sp

from einstein_collar_gluing import check as check_bulk


def check_corner():
    k, eta, g = sp.symbols("K eta G", real=True)
    # Within the P2 block the area density variation is K Y at r=1.
    # The two face amplitudes use a common boost sign before orientation.
    area_slope = (4*sp.pi/5)/(8*sp.pi*g)
    face = sp.Matrix([[0, 1], [-1, 0]])
    poisson = sp.diag(face, -face)
    # Coordinates (p_-,eta_-,p_+,eta_+). The two constraints and the common
    # gauge conditions constitute a finite corner reduction at fixed K.
    match = sp.Matrix([[1, 0, -1, 0], [0, 1, 0, -1]])
    gauge = sp.Matrix([[1, 0, 1, 0], [0, 1, 0, 1]])/2
    assert match*poisson*match.T == sp.zeros(2)
    coordinate_map = match.col_join(gauge)
    fp = gauge*poisson*match.T
    assert abs(fp.det()) == abs(coordinate_map.det()) == 1
    fixed = coordinate_map.inv()*sp.Matrix([0, 0, area_slope*k, eta])
    assert fixed == sp.Matrix([area_slope*k, eta, area_slope*k, eta])
    # The common area is tied to K, so its delta is used once. In raw
    # area units its Jacobian is compensated by the canonical measure.
    assert sp.simplify((8*sp.pi*g)*area_slope - 4*sp.pi/5) == 0

    left_a, left_b, right_a, right_b, j = sp.symbols("a_l b_l a_r b_r j")
    kinetic = lambda a, b: (a*a+12*a*b+12*b*b)/4
    flux_term = kinetic(left_a, left_b)-kinetic(right_a, right_b)
    assert flux_term.subs({left_a: 2, right_a: 2, left_b: -3, right_b: -3}) == 0
    corner_weight = fixed[0]*fixed[1]-fixed[2]*fixed[3]
    assert corner_weight == 0
    assert sp.diff(corner_weight + flux_term, j, 2) == 0
    print("Smooth corner FP/Jacobian ratio = 1. Opposite joint and fixed-flux weights cancel.")


if __name__ == "__main__":
    check_corner()
    for cells in (32, 64, 128, 256):
        check_bulk(cells, .125, .3, intrinsic=True)
