"""Joint two-sided ADM tensor and frame time-link measure control."""

import numpy as np
from scipy.linalg import block_diag, lu_factor, lu_solve, null_space
from sympy import Rational, pi

from einstein_annular_trace_brackets import region_rows
from einstein_even_bulk import R2, Y, lapse_gradient, tensor_basis
from einstein_flux_source_bracket import rows as collar_rows
from einstein_even_shell import integrate


def region(tensors, lo, hi, sign, projected_gauge=False):
    gram, q, f, lapse, shift = region_rows(tensors, lo, hi)
    gram, q, f, lapse, shift = map(lambda value: np.array(value, dtype=float),
                                   (gram, q, f, lapse, shift))
    inverse = np.linalg.inv(np.linalg.cholesky(gram))
    n = len(gram)
    unit, zero = np.eye(n), np.zeros((n, n))
    poisson = np.block([[zero, unit], [-unit, zero]])
    proper = block_diag(lapse @ inverse.T, shift @ inverse.T)
    gauge = proper @ poisson
    if projected_gauge:
        cutoff = (1-R2) * ((4-R2) if lo else 1)
        image = lapse_gradient(Y*cutoff**2).trace()
        trace_row = np.array([integrate(image*tensor.trace(), lo, hi)/pi
                              for tensor in tensors], dtype=float)
        # The lapse-image test removes a trace component orthogonal to
        # the harmonic moments. The original scalar constraint remains.
        gauge[0, n:] = trace_row @ inverse.T
        assert abs((gauge @ poisson @ proper.T)[0, 0]) > 0
    traces = block_diag(q @ inverse.T, f @ inverse.T)
    bounds = (Rational(7, 8), 1) if lo == 0 else (1, Rational(9, 8))
    _, _, load = collar_rows(tensors, lo, hi, *bounds)
    source = block_diag(inverse, inverse) @ np.array(load, dtype=float).ravel()
    trace_gram = np.array([[integrate(a*b, lo, hi)/pi for b in
                                [tensor.trace() for tensor in tensors]]
                           for a in [tensor.trace() for tensor in tensors]], dtype=float)
    kinetic = unit-inverse@trace_gram@inverse.T/2
    return sign*poisson, np.vstack((proper, gauge)), traces, source, kinetic


def check(steps=3, projected_gauge=False):
    tensors = tensor_basis(2)
    left, right = (region(tensors, 0, 1, 1, projected_gauge),
                   region(tensors, 1, 2, -1, projected_gauge))
    n = len(tensors)
    frame_unit = np.eye(3)
    frame_poisson = np.block([[np.zeros((3, 3)), frame_unit],
                              [-frame_unit, np.zeros((3, 3))]])
    poisson = block_diag(left[0], right[0], frame_poisson, -frame_poisson)
    size = len(poisson)
    proper = np.pad(block_diag(left[1], right[1]), ((0, 0), (0, 12)))
    traces = np.pad(block_diag(left[2], right[2]), ((0, 0), (0, 12)))
    jump = traces[:4]-traces[4:]
    average = (traces[:4]+traces[4:])/2
    positions = np.eye(size)[[4*n, 4*n+1, 4*n+2, 4*n+6, 4*n+7, 4*n+8]]
    momenta = np.eye(size)[[4*n+3, 4*n+4, 4*n+5, 4*n+9, 4*n+10, 4*n+11]]
    frame = momenta.copy()
    for side in (0, 1):
        t, x, eta = positions[3*side:3*side+3]
        k, psi, _, f = traces[4*side:4*side+4]
        frame[3*side] += .4*k-.6*psi
        frame[3*side+1] -= f+.6*(eta-t)
        frame[3*side+2] -= .1*k
    gauge_rows = np.vstack((positions[:3]-positions[3:],
                            (positions[:3]+positions[3:])/2))
    constraints = np.vstack((proper, jump, frame, gauge_rows))
    bracket = constraints@poisson@constraints.T
    assert np.linalg.matrix_rank(bracket) == len(bracket)
    assert np.linalg.norm(frame@poisson@jump.T) > 0
    reduced = null_space(constraints)

    # Positive tensor Gaussian for the measure test. The original geometric
    # spatial Hessian is not used in this control.
    dt = 1/steps
    quadratic = block_diag(np.eye(n), left[4]+np.eye(n),
                           np.eye(n), right[4]+np.eye(n), np.zeros((12, 12)))
    action = dt*np.kron(np.eye(steps+1), quadratic)
    links = np.diff(np.eye(steps+1), axis=0)
    link_matrix = np.zeros((size, size))
    for offset, length, sign in ((0, n, 1), (2*n, n, -1),
                                  (4*n, 3, 1), (4*n+6, 3, -1)):
        link_matrix[offset:offset+length, offset+length:offset+2*length] = sign*np.eye(length)
    canonical = np.kron(links.T, link_matrix)
    # Momentum at the earlier endpoint of each time link.
    canonical = canonical @ np.kron(np.eye(steps, steps+1), np.eye(size))
    action = action-1j*(canonical+canonical.T)

    joint = np.kron(np.eye(steps+1), constraints)
    subspace = np.kron(np.eye(steps+1), reduced)
    raw = np.r_[left[3], right[3], np.zeros(12)]
    source = np.kron(dt*np.sin(np.pi*np.arange(steps+1)/steps), raw)
    charge = jump@poisson@jump.T
    cross = poisson@jump.T
    trace_poisson = average@(poisson+cross@np.linalg.solve(charge, cross.T))@average.T
    inverse = np.linalg.inv(trace_poisson[:2, 2:])
    sigma = .2
    packet = 2*sigma**2*average[:2].T@inverse.T@inverse@average[:2]
    phase = np.zeros(len(source), dtype=complex)
    momentum = inverse.T@np.array([2., -3.])
    for index, sign in ((0, 1), (steps, -1)):
        segment = slice(index*size, (index+1)*size)
        action[segment, segment] += packet
        phase[segment] = sign*1j*average[:2].T@momentum

    bordered = np.block([[action, joint.T],
                         [joint, np.zeros((len(joint), len(joint)))]])
    full_lu, reduced_lu = lu_factor(bordered), lu_factor(subspace.T@action@subspace)
    def logdet(lu):
        return np.log(abs(np.diag(lu[0]))).sum()
    # Liouville density of the orthonormal projected subspace.
    pulled_form = reduced.T@np.linalg.inv(poisson)@reduced
    full_log = logdet(full_lu)-(steps+1)*np.linalg.slogdet(bracket)[1]
    expected_log = logdet(reduced_lu)-(steps+1)*np.linalg.slogdet(pulled_form)[1]
    np.testing.assert_allclose(full_log, expected_log, atol=1e-8, rtol=0)
    normalization = np.log(2*sigma**2*abs(np.linalg.det(inverse))/np.pi)
    max_gap = 0.
    for j in (0., .1, -.1):
        load = phase+j*source
        extended = np.r_[load, np.zeros(len(joint))]
        projected = subspace.T@load
        full_amp = normalization+(extended@lu_solve(full_lu, extended)-full_log)/2
        reduced_amp = normalization+(projected@lu_solve(reduced_lu, projected)-expected_log)/2
        np.testing.assert_allclose(full_amp, reduced_amp, atol=1e-8, rtol=0)
        max_gap = max(max_gap, abs(full_amp-reduced_amp))
    print(f"links={steps}: rank={len(bracket)}, log determinant gap={abs(full_log-expected_log):.3e}")
    print(f"Maximum log amplitude gap at j=0 and j=±0.1: {max_gap:.3e}")


if __name__ == "__main__":
    check(projected_gauge=True)
