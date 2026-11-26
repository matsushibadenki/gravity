"""Symplectic reduction of the charged quadrupole block at a shared sphere."""

import sympy as sp


def check():
    # Mixed volume pairing in the polynomial smearing basis, in units of pi.
    pairing = sp.Matrix([[8, sp.Rational(16, 5)],
                         [sp.Rational(56, 5), -sp.Rational(16, 5)]])
    # Lie derivatives along Qx and Yx give (c,d)=(-1,1) and (2,0),
    # where h_AB=c Y gamma_AB+d (D_A D_B Y)^TF.
    induced = sp.Matrix([[-1, 2], [1, 0]])
    # If h = induced * b for shift b, conjugate momentum in h coordinates
    # is induced^(-T) * pairing.T * a for lapse a.
    momentum = induced.T.inv() * pairing.T
    assert momentum.T * induced == pairing

    identity = sp.eye(2)
    zero = sp.zeros(2)
    canonical = sp.BlockMatrix([[zero, identity], [-identity, zero]]).as_explicit()
    two_faces = sp.diag(canonical, -canonical)
    match = identity.row_join(zero).row_join(-identity).row_join(zero)
    assert match * two_faces * match.T == zero
    orbit = two_faces * match.T
    assert orbit[:4, :] == orbit[4:, :]

    # x=(h+,p+,h-,p-). Matching identifies h. The relative momentum
    # survives, whereas the average momentum is a gauge coordinate.
    for gauge_rescaling in (identity, sp.Matrix([[2, 1], [1, 3]])):
        average_gauge = (zero.row_join(gauge_rescaling)
                         .row_join(zero).row_join(gauge_rescaling)) / 2
        shared = identity.row_join(zero).row_join(identity).row_join(zero) / 2
        relative = zero.row_join(identity).row_join(zero).row_join(-identity)
        transform = match.col_join(average_gauge).col_join(shared).col_join(relative)
        fp = average_gauge * orbit
        assert abs(fp.det()) == abs(transform.det())
        reduced = shared.col_join(relative)
        assert reduced * two_faces * reduced.T == canonical
    print("Exact charged block: matching is first class, gauge and Jacobian cancel.")
    print("Reduced canonical coordinates: shared induced metric, relative momentum.")


if __name__ == "__main__":
    check()
