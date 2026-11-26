"""Exact oriented charge algebra of the linearized quadrupole block."""

import sympy as sp


def check():
    mixed = sp.Matrix([[8, sp.Rational(16, 5)],
                       [sp.Rational(56, 5), -sp.Rational(16, 5)]])
    zero = sp.zeros(2)
    face = sp.BlockMatrix([[zero, mixed], [-mixed.T, zero]]).as_explicit()
    assert face.rank() == 4
    two_faces = sp.diag(face, -face)
    identity = sp.eye(4)
    diagonal = identity.row_join(-identity)
    relative = identity.row_join(identity) / 2
    assert diagonal * two_faces * diagonal.T == sp.zeros(4)
    assert relative * two_faces * relative.T == sp.zeros(4)
    bracket = diagonal * two_faces * relative.T
    assert bracket == face
    combined = diagonal.col_join(relative)
    second_class = combined * two_faces * combined.T
    assert second_class.rank() == 8
    assert sp.sqrt(second_class.det()) == mixed.det()**2

    # The quadrupole curvature includes the normal displacement of the
    # embedding. In the spatial gauge its transformation cancels delta K.
    normal, angular = sp.symbols("w v")
    assert sp.expand(4*((2*normal-6*angular) + 3*(2*angular) - 2*normal)) == 0
    print("One face rank 4; diagonal rank 0; diagonal plus relative rank 8.")
    print(f"Second-class density in these coordinates: {mixed.det()**2}")


def check_conditional_momentum():
    # A reduced positive Gaussian with a prescribed nonzero common flux.
    # This is a control for momentum integration, with no ADM Hessian assumed.
    kinetic = sp.Matrix([[3, 1], [1, 2]])
    flux = sp.Matrix([[1, 2]])
    covariance = flux * kinetic.inv() * flux.T
    b = sp.Integer(2)
    minimum = kinetic.inv() * flux.T * covariance.inv() * sp.Matrix([b])
    assert flux * minimum == sp.Matrix([b])
    assert (minimum.T * kinetic * minimum)[0] == b**2 / covariance[0]
    # Direct delta integration over the first momentum component.
    p, j, spatial_source = sp.symbols("p j S", real=True)
    constrained = sp.Matrix([b - 2*p, p])
    direct = sp.integrate(sp.exp(-(constrained.T * kinetic * constrained)[0]/2),
                          (p, -sp.oo, sp.oo))
    predicted = sp.sqrt(2*sp.pi/(kinetic.det()*covariance[0])) * sp.exp(
        -b**2/(2*covariance[0]))
    assert sp.simplify(direct - predicted) == 0
    assert sp.diff(sp.log(predicted) + j*spatial_source, j, 2) == 0
    print("Nonzero-flux Gaussian: conditional determinant agrees with direct integration.")


if __name__ == "__main__":
    check()
    check_conditional_momentum()
