"""Two independent ADM shift fluxes in a finite-radius TT kinetic block."""

import sympy as sp

from einstein_even_bulk import I, Q, R2, X, XYZ, Y
from einstein_even_shell import integrate


def check():
    mixed = X*(Q*X).T + (Q*X)*X.T
    candidates = [R2**2*Q, R2*mixed, R2*Y*I, Y*X*X.T]
    coefficients = sp.symbols("a:4")
    trial = sum((a*t for a, t in zip(coefficients, candidates)), sp.zeros(3))
    expressions = [sp.trace(trial)] + [
        sum(sp.diff(trial[i, j], XYZ[j]) for j in range(3)) for i in range(3)]
    equations = [c for expression in expressions
                 for c in sp.Poly(expression, *XYZ).coeffs()]
    matrix, _ = sp.linear_eq_to_matrix(equations, coefficients)
    profile = matrix.nullspace()[0]
    tensors = [Q, -11*R2*Q + 6*mixed - 4*Y*I,
               sum((a*t for a, t in zip(profile, candidates)), sp.zeros(3))]
    # Gradient of the unit-sphere harmonic and the common outward direction.
    angular = 2*(Q*X-Y*X)
    flux = sp.Matrix([[integrate(v.dot(tensor*X), 0, 1, surface=True)
                       for tensor in tensors] for v in (Y*X, angular)])
    assert flux[:, :2].det() != 0

    b = sp.Matrix([2, -3])
    p = sp.symbols("p", real=True)
    point = (flux[:, :2].inv()*(b - flux[:, 2]*p)).col_join(sp.Matrix([p]))
    for inner, outer in ((0, 1), (1, 2)):
        mass = sp.Matrix([[integrate(sum(a*b for a, b in zip(left, right)), inner, outer)
                           for right in tensors] for left in tensors])
        covariance = flux*mass.inv()*flux.T
        exponent = sp.expand((point.T*mass*point)[0])
        curvature = exponent.coeff(p, 2)
        minimum = exponent.subs(p, -exponent.coeff(p, 1)/(2*curvature))
        assert sp.simplify(minimum - (b.T*covariance.inv()*b)[0]) == 0
        assert sp.simplify(curvature*flux[:, :2].det()**2
                           - mass.det()*covariance.det()) == 0
        print(f"radii {inner},{outer}: rank={flux.rank()}, covariance determinant={covariance.det()}")


if __name__ == "__main__":
    check()
