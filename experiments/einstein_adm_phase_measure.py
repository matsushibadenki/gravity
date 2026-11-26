"""Check proper ADM phase-space reduction in the even quadrupole ball."""

import numpy as np

from einstein_even_bulk import assemble


def check(order):
    gram, scalar, vector = (np.array(item, dtype=float) for item in assemble(order))
    factor = np.linalg.cholesky(gram)
    # Change both canonical coordinates and momenta to dual orthonormal bases.
    scalar = np.linalg.solve(factor, scalar.T).T
    vector = np.linalg.solve(factor, vector.T).T
    count = len(gram)
    identity, zero = np.eye(count), np.zeros_like(gram)
    poisson = np.block([[zero, identity], [-identity, zero]])
    constraints = np.block([[scalar, np.zeros_like(scalar)],
                            [np.zeros_like(vector), vector]])
    gauge = constraints @ poisson
    np.testing.assert_allclose(constraints @ poisson @ constraints.T, 0, atol=1e-10)
    _, _, basis = np.linalg.svd(np.vstack((constraints, gauge)), full_matrices=True)
    reduced = basis[2 * len(constraints):]
    for conditions in (gauge, 2 * gauge + .1 * reduced[:len(gauge)]):
        fp = conditions @ poisson @ constraints.T
        change = np.vstack((constraints, conditions, reduced))
        log_ratio = np.linalg.slogdet(fp)[1] - np.linalg.slogdet(change)[1]
        np.testing.assert_allclose(log_ratio, 0, atol=1e-10)
        projector = reduced @ poisson @ reduced.T
        np.testing.assert_allclose(projector.T @ projector, np.eye(len(reduced)), atol=1e-10)
        print(f"order={order}: phase dimension={len(reduced)}, log ratio={log_ratio:+.3e}")


if __name__ == "__main__":
    for size in (1, 2, 3):
        check(size)
