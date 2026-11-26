"""Canonical multiplier normalization in a finite charged interface block."""

import numpy as np
import sympy as sp


def check_boundary():
    g = sp.symbols("G", positive=True)
    # One lapse charge and two even-parity shift charges. In local canonical
    # coordinates take their matched differences to be q_+ - q_-.
    # A nonsingular rescaling models their charge normalization.
    scale = sp.diag(3/(5*g), 2, 12)
    identity, zero = sp.eye(3), sp.zeros(3)
    canonical = sp.BlockMatrix([[zero, identity], [-identity, zero]]).as_explicit()
    poisson = sp.diag(canonical, -canonical)
    match = scale.row_join(zero).row_join(-scale).row_join(zero)
    gauge = zero.row_join(identity).row_join(zero).row_join(identity)/2
    shared = identity.row_join(zero).row_join(identity).row_join(zero)/2
    relative = zero.row_join(identity).row_join(zero).row_join(-identity)
    coordinates = match.col_join(gauge).col_join(shared).col_join(relative)
    assert match * poisson * match.T == zero
    assert abs((gauge * poisson * match.T).det()) == abs(coordinates.det())
    # Matching a flux imposes equality, and permits a nonzero common flux.
    shared_values = sp.Matrix([0, 2, -3])
    point = coordinates.inv() * sp.zeros(6, 1).col_join(shared_values).col_join(sp.ones(3, 1))
    assert match * point == sp.zeros(3, 1)
    assert shared * point == shared_values
    print("Finite canonical block: lapse and shift charge scale cancels against FP.")


def check_euclidean():
    # A Lorentzian multiplier Fourier integral defines delta(C). Its
    # Euclidean representation has an imaginary multiplier, with dn/(2 pi i).
    # A real Gaussian regulator on the Fourier parameter yields a delta sequence.
    for sigma in (.25, .125, .0625):
        charge_scale, center = .6, .3
        weighted = (np.exp(-center**2 / (2*(1 + sigma**2/charge_scale**2)))
                    / np.sqrt(1 + sigma**2/charge_scale**2))
        assert abs(weighted - np.exp(-center**2/2)) < 2*sigma**2

    p, step, mass, delta = sp.symbols("p step mass delta", positive=True)
    # Euclidean phase-space kernel: keep physical momentum real.
    kernel = sp.integrate(sp.exp(-step*p**2/(2*mass) + sp.I*p*delta),
                          (p, -sp.oo, sp.oo))/ (2*sp.pi)
    expected = sp.sqrt(mass/(2*sp.pi*step))*sp.exp(-mass*delta**2/(2*step))
    assert sp.simplify(kernel - expected) == 0
    print("Fourier multiplier delta sequence and physical momentum kernel verified.")


if __name__ == "__main__":
    check_boundary()
    check_euclidean()
