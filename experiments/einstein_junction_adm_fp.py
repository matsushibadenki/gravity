"""Seam normalization from the constrained ADM endpoint symplectic form."""

import sympy as sp

from einstein_geometric_junction import check as check_junction
from einstein_tangential_seam import check as check_embedding


def check():
    g = sp.symbols("G", positive=True)
    norm = 4*sp.pi/5
    # At r=1 the ADM endpoint potential is
    # norm * (a dK - (3a + 6b) dPsi). Coordinates are (Psi,K,a,b).
    flux_to_momentum = norm*sp.Matrix([[-3, -6], [1, 0]])
    identity, zero = sp.eye(2), sp.zeros(2)
    canonical = sp.BlockMatrix([[zero, identity], [-identity, zero]]).as_explicit()
    change = sp.diag(identity, flux_to_momentum)
    poisson = change.inv()*canonical*change.inv().T
    faces = sp.diag(poisson, -poisson)
    geometry = sp.Matrix([[0, 1], [-3/(5*g), 2/(5*g)]])
    face_charges = geometry.row_join(zero)
    match = face_charges.row_join(-face_charges)
    common_flux = zero.row_join(identity).row_join(zero).row_join(identity)/2
    assert match*faces*match.T == zero
    fp = common_flux*faces*match.T
    assert abs(fp.det()) == abs(geometry.det()/flux_to_momentum.det())

    # First use differences and averages, then integrate the charge
    # deltas and condition the common flux. The remaining relative flux
    # coordinates are reported in canonical momentum units.
    relative_flux = zero.row_join(identity).row_join(zero).row_join(-identity)
    common_metric = identity.row_join(zero).row_join(identity).row_join(zero)/2
    coordinates = match.col_join(common_flux).col_join(common_metric).col_join(relative_flux)
    jacobian = abs(coordinates.det())
    density = flux_to_momentum.det()**2
    canonical_conversion = abs(flux_to_momentum.det())
    assert sp.simplify(density*abs(fp.det())/(jacobian*canonical_conversion)) == 1
    prescribed = sp.Matrix([2, -3])
    point = coordinates.inv()*sp.zeros(2, 1).col_join(prescribed).col_join(sp.ones(4, 1))
    assert common_flux*point == prescribed and match*point == sp.zeros(2, 1)
    print(f"Charge Jacobian={abs(geometry.det())}, conditional symplectic density ratio=1.")


if __name__ == "__main__":
    check()
    check_embedding()
    for order in (2, 3, 4):
        for frequency in (0, 1, 2):
            check_junction(order, frequency)
