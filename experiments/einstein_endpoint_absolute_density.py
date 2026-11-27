"""Canonical charge and gauge normalization for the isolated ADM endpoint."""

import sympy as sp


def check():
    g = sp.symbols("G", positive=True)
    unit, zero = sp.eye(2), sp.zeros(2)
    # (geometric jump, common flux). The endpoint potential is
    # (M f)^T d(jump). Retain the shared trace and relative flux outside
    # this block.
    m = (4*sp.pi/5)*sp.Matrix([[-3, -6], [1, 0]])
    a = sp.Matrix([[6, -4], [0, 1]])/(10*g)
    to_canonical = sp.diag(unit, m)
    canonical = sp.BlockMatrix([[zero, unit], [-unit, zero]]).as_explicit()
    poisson = to_canonical.inv()*canonical*to_canonical.inv().T
    constraints = a.row_join(zero)
    assert constraints*poisson*constraints.T == zero

    for gauge_basis in (unit, sp.Matrix([[2, 1], [1, 3]])):
        gauge = zero.row_join(gauge_basis)
        fp = abs((gauge*poisson*constraints.T).det())
        coordinates = constraints.col_join(gauge)
        liouville = abs(m.det())
        assert sp.simplify(liouville*fp/abs(coordinates.det())) == 1
    fp_in_flux_units = abs((zero.row_join(unit)*poisson*constraints.T).det())
    assert sp.simplify(fp_in_flux_units - 1/(64*sp.pi**2*g**2)) == 0

    # Group averaging a jump packet evaluates it at zero jump. The two
    # endpoint normalization constants multiply, without constraining the
    # surviving shared geometry or generating a source quadratic term.
    sigma = sp.symbols("sigma", positive=True)
    jump = sp.Matrix(sp.symbols("dPsi dK", real=True))
    mean_flux = sp.Matrix([2, -3])
    packet = sp.sqrt(2*sigma**2*abs(m.det())/sp.pi)*sp.exp(
        -sigma**2*(m.T*jump).dot(m.T*jump)+sp.I*jump.dot(m*mean_flux))
    weight = packet.subs(dict.fromkeys(jump, 0))
    assert sp.simplify(weight**2-2*sigma**2*abs(m.det())/sp.pi) == 0
    print(f"raw Fourier Jacobian={1/a.det()}, FP={fp_in_flux_units}, "
          f"Liouville density={m.det()}, net density=1")
    print(f"Two projected packet factors at sigma=0.2: {weight.subs(sigma, sp.Rational(1, 5))**2}")


if __name__ == "__main__":
    check()
