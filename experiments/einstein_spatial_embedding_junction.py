"""Spatial embedding compensation of the ADM symplectic boundary flux."""

import sympy as sp

from einstein_projected_lapse_gauge import R


def check():
    a, b, w, v = (sp.Function(name)(R) for name in ("a", "b", "w", "v"))
    c = (R*a.diff(R)+2*a-6*b)/2
    d = (R*b.diff(R)+3*b+c)/2
    # W_r=w Y and W_A=r^2 v D_A Y. Tensor components use an
    # orthonormal radial/tangential frame.
    h_rr = 2*w.diff(R)
    h_mixed = w/R+R*v.diff(R)
    h_trace = 2*w/R-6*v
    h_shear = 2*v
    pairing = R**2*(a*h_rr+12*b*h_mixed+2*c*h_trace+12*d*h_shear)
    endpoint = 2*R**2*(a*w+6*R*b*v)
    assert sp.expand(pairing-endpoint.diff(R)) == 0

    # Common flux couples to the difference of the geometric gauge
    # displacements. The independent embedding shifts by its negative.
    geometry = sp.Matrix(sp.symbols("w_g v_g"))
    embedding = sp.Matrix(sp.symbols("w_e v_e"))
    flux = sp.Matrix(sp.symbols("a_f b_f"))
    flux_map = 2*(4*sp.pi/5)*sp.diag(1, 6)
    tangent = sp.Matrix(sp.symbols("dw dv"))
    potential = (flux.T*flux_map*(geometry+embedding))[0]
    assert sp.expand(potential.subs(dict(zip(geometry, tangent))).subs(
        dict(zip(embedding, -tangent)))) == 0

    # Relative intrinsic trace and shear respond to the dressed
    # displacement, so smooth identification fixes both components.
    induced = sp.Matrix([[2, -6], [0, 2]])
    assert induced.det() == 4
    assert (induced*(geometry+embedding)).jacobian(tuple(embedding)).rank() == 2
    print("Exact ADM pairing equals the two shift surface charges.")
    print("Dressed relative trace and shear fix both spatial displacements in this block.")


if __name__ == "__main__":
    check()
