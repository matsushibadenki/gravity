"""Finite-radius ADM kinetic integral in a polynomial TT subspace."""

import sympy as sp

from einstein_even_bulk import I, Q, R2, X, XYZ, Y
from einstein_even_shell import integrate


def check():
    # Two regular quadrupolar TT momenta with independent radial profiles.
    mixed = X*(Q*X).T + (Q*X)*X.T
    profiles = [Q, -11*R2*Q + 6*mixed - 4*Y*I]
    for tensor in profiles:
        assert sp.expand(sp.trace(tensor)) == 0
        for i in range(3):
            assert sp.expand(sum(sp.diff(tensor[i, j], XYZ[j])
                                 for j in range(3))) == 0

    # Normal momentum paired with the radial shift Y*n at r=1.
    flux = sp.Matrix([[integrate(Y*X.dot(tensor*X), 0, 1, surface=True)
                       for tensor in profiles]])
    for inner, outer in ((0, 1), (1, 2)):
        # ADM kinetic density is 16 pi G times (pi_ij pi^ij - pi^2/2).
        # Use units 32 pi G Delta_tau=1 in the Gaussian exponent -p^T M p/2.
        mass = sp.Matrix([[integrate(sum(a*b for a, b in zip(left, right)), inner, outer)
                           for right in profiles] for left in profiles])
        assert mass.is_positive_definite
        b = sp.Integer(2)
        p = sp.symbols("p", real=True)
        point = sp.Matrix([(b-flux[1]*p)/flux[0], p])
        reduced = sp.expand((point.T*mass*point)[0])
        covariance = (flux*mass.inv()*flux.T)[0]
        direct = (sp.sqrt(2*sp.pi/reduced.coeff(p, 2))/abs(flux[0])
                  * sp.exp(-reduced.subs(p, -reduced.coeff(p, 1)
                                           / (2*reduced.coeff(p, 2)))/2))
        expected = (sp.sqrt(2*sp.pi/(mass.det()*covariance))
                    * sp.exp(-b*b/(2*covariance)))
        assert sp.simplify(direct-expected) == 0
        print(f"radii {inner},{outer}: fixed flux={b}, covariance={covariance}")


if __name__ == "__main__":
    check()
