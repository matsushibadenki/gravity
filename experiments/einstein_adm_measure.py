"""Measure of one nonzero real Fourier pair in linearized vacuum ADM gravity."""

import numpy as np


def constraints(momentum):
    """Use canonical symmetric-tensor components in an orthonormal basis."""
    unit = np.eye(3)
    basis = np.array([
        np.outer(unit[i], unit[i]) for i in range(3)
    ] + [
        (np.outer(unit[i], unit[j]) + np.outer(unit[j], unit[i])) / np.sqrt(2)
        for i, j in ((0, 1), (0, 2), (1, 2))
    ])
    scalar = (
        momentum @ momentum * np.trace(basis, axis1=1, axis2=2)
        - np.einsum("i,aij,j->a", momentum, basis, momentum)
    )
    # The Fourier derivative exchanges sine and cosine. Absorb its sign
    # into the real shift multipliers for the momentum constraints.
    vector = 2 * np.einsum("aij,j->ia", basis, momentum)
    rows = np.zeros((4, 12))
    rows[0, :6] = scalar
    rows[1:, 6:] = vector
    return rows


def check(momentum):
    identity = np.eye(6)
    zero = np.zeros_like(identity)
    symplectic = np.block([[zero, identity], [-identity, zero]])
    constraint = constraints(momentum)
    np.testing.assert_allclose(constraint @ symplectic @ constraint.T, 0, atol=1e-12)

    # These four gauge coordinates are conjugate to the constraints.
    gauge = constraint @ symplectic
    _, _, vt = np.linalg.svd(np.vstack((constraint, gauge)), full_matrices=True)
    physical = vt[8:].T
    np.testing.assert_allclose(
        (physical.T @ symplectic @ physical).T @ (physical.T @ symplectic @ physical),
        np.eye(4), atol=1e-12,
    )
    # Mix the gauge slice with physical boundary data and rescale its
    # coordinates. A correct FP-weighted measure is invariant under both.
    mixing = np.triu(np.ones((4, 4))) + np.diag([1., 2., 3., 4.])
    tilted_gauge = mixing @ gauge + 0.3 * physical.T
    for conditions in (gauge, tilted_gauge):
        fp = conditions @ symplectic @ constraint.T
        coordinates = np.vstack((constraint, conditions, physical.T))
        log_fp = np.linalg.slogdet(fp)[1]
        log_jacobian = -np.linalg.slogdet(coordinates)[1]
        np.testing.assert_allclose(log_fp + log_jacobian, 0, atol=1e-12)
        # A source along the physical subspace can be evaluated directly
        # on the constrained gauge slice or in the reduced coordinates.
        reduced = np.array([.2, -.1, .3, .4])
        lifted = np.linalg.solve(coordinates, np.r_[np.zeros(8), reduced])
        source = physical @ np.array([.5, .1, -.2, .6])
        np.testing.assert_allclose(source @ lifted, source @ physical @ reduced, atol=1e-12)
        print(f"k={momentum}: log FP={log_fp:+.6f}, log measure={log_fp + log_jacobian:+.3e}")


if __name__ == "__main__":
    # The constant mode has no linearized constraints of this form.
    assert not constraints(np.zeros(3)).any()
    for wave in ([0., 0., 1.], [1., 2., 3.], [-.5, .2, .8]):
        check(np.array(wave))
