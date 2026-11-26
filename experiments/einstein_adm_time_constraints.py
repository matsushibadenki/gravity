"""Time-link determinant through ADM multiplier and gauge blocks in the ball."""

import numpy as np
import sympy as sp
from scipy.linalg import block_diag, lu_factor, lu_solve

from einstein_even_bulk import XYZ, assemble, inner, tensor_basis


def check(steps):
    gram, scalar, vector = (np.array(x, dtype=float) for x in assemble(1))
    tensors = tensor_basis(1)
    traces = [sp.Matrix([sp.trace(tensor)]) for tensor in tensors]
    trace_gram = np.array([[inner(a, b)/sp.pi for b in traces]
                           for a in traces], dtype=float)
    chol = np.linalg.cholesky(gram)
    inverse = np.linalg.inv(chol)
    count = len(gram)
    unit, zero = np.eye(count), np.zeros_like(gram)
    momentum = unit - inverse @ trace_gram @ inverse.T / 2
    scalar, vector = scalar @ inverse.T, vector @ inverse.T
    constraints = block_diag(scalar, vector)
    poisson = np.block([[zero, unit], [-unit, zero]])
    gauge = constraints @ poisson
    fp = gauge @ poisson @ constraints.T
    conditions = np.vstack((constraints, gauge))
    _, _, basis = np.linalg.svd(conditions, full_matrices=True)
    reduced = basis[len(conditions):].T
    np.testing.assert_allclose(conditions @ reduced, 0, atol=1e-11)

    # A positive auxiliary quadratic regulator allows an ordinary Euclidean
    # integral on this truncated basis. This is a measure control, not the
    # physical spatial ADM Hessian.
    dt = 1 / steps
    action = np.kron(np.eye(steps), dt*block_diag(unit, momentum + unit))
    difference = np.roll(np.eye(steps), -1, axis=0) - np.eye(steps)
    link = np.block([[zero, unit], [zero, zero]])
    mixed = np.kron(difference.T, link)
    action = action - 1j*(mixed + mixed.T)
    constraint_links = np.kron(np.eye(steps), conditions)
    embedding = np.kron(np.eye(steps), reduced)
    source_time = 1 + .2*np.cos(2*np.pi*np.arange(steps)/steps)
    # On the ball face use the inner half of the intrinsic collar.
    nodes, weights = np.polynomial.legendre.leggauss(12)
    width = .125
    radii = 1 + width*(nodes-1)/2
    collar = 3*(1-((radii-1)/width)**2)/(4*width)
    r = sp.Symbol("r")
    x, y, z = XYZ
    source_components = []
    for tensor in tensors:
        c = ((tensor[0, 0]+tensor[1, 1])/2).subs({x: 0, y: 0, z: r})
        three_d = (tensor[2, 2]-tensor[1, 1]).subs({x: r, y: 0, z: 0})
        profile = sp.lambdify(r, 4*(c+three_d)/r**2, "numpy")
        source_components.append(width/2 * (weights @ (collar*profile(radii))))
    source = np.kron(source_time*dt, np.r_[inverse@source_components, np.zeros(count)])

    # Fourier multipliers for both constraints and gauges. The bordered
    # determinant includes their delta-function Jacobians.
    multipliers = np.zeros((len(constraint_links), len(constraint_links)))
    bordered = np.block([[action, 1j*constraint_links.T],
                         [1j*constraint_links, multipliers]])
    effective = embedding.T @ action @ embedding
    full_lu = lu_factor(bordered)
    reduced_lu = lu_factor(effective)
    log_full = np.log(abs(np.diag(full_lu[0]))).sum() - 2*steps*np.linalg.slogdet(fp)[1]
    log_reduced = np.log(abs(np.diag(reduced_lu[0]))).sum()
    full_source = np.r_[source, np.zeros(len(constraint_links))]
    projected_source = embedding.T @ source
    response_full = full_source @ lu_solve(full_lu, full_source)
    response_reduced = projected_source @ lu_solve(reduced_lu, projected_source)
    np.testing.assert_allclose([log_full, response_full], [log_reduced, response_reduced],
                               atol=1e-9, rtol=0)
    print(f"steps={steps}: logdet gap={abs(log_full-log_reduced):.3e}, "
          f"source gap={abs(response_full-response_reduced):.3e}")


if __name__ == "__main__":
    for steps in (3, 5, 8):
        check(steps)
