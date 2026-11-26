"""Static quadrupole lapse junction and its conditional Gaussian measure."""

import sympy as sp

from einstein_collar_gluing import check as check_composition


def junction():
    r, newton = sp.symbols("r G", positive=True)
    k, derivative, psi = sp.symbols("K K_prime Psi", real=True)
    h = 6*psi/r - 2*k + r*derivative
    # First variation of the sphere mean curvature in a radial gauge.
    mean_curvature = sp.expand(derivative - h/r)
    assert mean_curvature == 2*k/r - 6*psi/r**2
    # The Hamiltonian boundary lapse couples to sqrt(q) times the
    # oriented mean curvature. Its extra area variation is shared.
    charge = sp.expand((4*sp.pi/5)/(8*sp.pi*newton)
                       * (r*r*mean_curvature + 2*r*k))
    slope = sp.diff(charge, psi)
    assert slope == -3/(5*newton)
    left, right, b, kappa = sp.symbols("Psi_left Psi_right B kappa")
    extra_weight = (kappa*k - b)*(left-right)
    assert extra_weight.subs(right, left) == 0
    jacobian = -1/slope
    assert sp.simplify(jacobian * (-slope)) == 1
    print(f"Lapse charge slope: {slope}; raw delta Jacobian: {jacobian}")
    for cells in (32, 64, 128, 256):
        check_composition(cells, .125, .3, intrinsic=True)


if __name__ == "__main__":
    junction()
