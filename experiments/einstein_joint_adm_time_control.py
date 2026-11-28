"""Joint two-sided ADM tensor and frame time-link measure control."""

import numpy as np
from scipy.linalg import block_diag, lu_factor, lu_solve, null_space
from sympy import Rational, pi

from einstein_annular_trace_brackets import region_rows
from einstein_even_bulk import R2, Y, lapse_gradient, tensor_basis
from einstein_flux_source_bracket import rows as collar_rows
from einstein_even_shell import integrate


def region(tensors, lo, hi, sign, projected_gauge=False, spatial_order=None, whole=False):
    gram, q, f, lapse, shift = region_rows(tensors, lo, hi, (1-R2)*(4-R2) if whole else None)
    gram, q, f, lapse, shift = map(lambda value: np.array(value, dtype=float),
                                   (gram, q, f, lapse, shift))
    inverse = np.linalg.inv(np.linalg.cholesky(gram))
    n = len(gram)
    unit, zero = np.eye(n), np.zeros((n, n))
    poisson = np.block([[zero, unit], [-unit, zero]])
    proper = block_diag(lapse @ inverse.T, shift @ inverse.T)
    gauge = proper @ poisson
    if projected_gauge:
        cutoff = (1-R2) * ((4-R2) if lo or whole else 1)
        image = lapse_gradient(Y*cutoff**2).trace()
        trace_row = np.array([integrate(image*tensor.trace(), lo, hi)/pi
                              for tensor in tensors], dtype=float)
        # The lapse-image test removes a trace component orthogonal to
        # the harmonic moments. The original scalar constraint remains.
        gauge[0, n:] = trace_row @ inverse.T
        assert abs((gauge @ poisson @ proper.T)[0, 0]) > 0
    traces = block_diag(q @ inverse.T, f @ inverse.T)
    bounds = (Rational(7, 8), 1) if lo == 0 else (1, Rational(9, 8))
    if whole:
        bounds = (Rational(7, 8), Rational(9, 8))
    _, _, load = collar_rows(tensors, lo, hi, *bounds, proper_distance=spatial_order is not None)
    source = block_diag(inverse, inverse) @ np.array(load, dtype=float).ravel()
    trace_gram = np.array([[integrate(a*b, lo, hi)/pi for b in
                                [tensor.trace() for tensor in tensors]]
                           for a in [tensor.trace() for tensor in tensors]], dtype=float)
    kinetic = unit-inverse@trace_gram@inverse.T/2
    result = sign*poisson, np.vstack((proper, gauge)), traces, source, kinetic
    if spatial_order is not None:
        from einstein_tensor_spatial_energy import spatial_hessian
        return (*result, spatial_hessian(spatial_order, lo, hi, inverse), inverse)
    return result


def compare_fresnel(action, joint, subspace, source, constraint_log, pullback_log):
    """Compare signed Gaussian factors in the bordered and reduced controls."""
    bordered = np.block([[action, joint.T],
                         [joint, np.zeros((len(joint), len(joint)))]])
    reduced = subspace.T @ action @ subspace

    def factor(matrix, density_log):
        spectrum = np.linalg.eigvalsh(matrix)
        assert np.min(abs(spectrum)) > 1e-10
        signature = np.sign(spectrum).sum()
        value = (density_log-np.log(abs(spectrum)).sum())/2
        return value-1j*np.pi*signature/4, int(signature)

    full, signature = factor(bordered, constraint_log)
    direct, direct_signature = factor(reduced, pullback_log)
    assert signature == direct_signature
    np.testing.assert_allclose(full, direct, atol=1e-8, rtol=0)

    bordered_source = np.pad(source, (0, len(joint)))
    projected_source = subspace.T @ source
    response = bordered_source @ np.linalg.solve(bordered, bordered_source)
    direct_response = projected_source @ np.linalg.solve(reduced, projected_source)
    np.testing.assert_allclose(response, direct_response, atol=1e-8, rtol=0)
    print(f"Lorentzian joint signature={signature}, "
          f"log factor gap={abs(full-direct):.3e}, "
          f"source quadratic gap={abs(response-direct_response):.3e}")


def check(steps=3, projected_gauge=False, order=2, charge_match=False, open_time=False):
    tensors = tensor_basis(order)
    spatial_order = order if open_time else None
    left, right = (region(tensors, 0, 1, 1, projected_gauge, spatial_order),
                   region(tensors, 1, 2, -1, projected_gauge, spatial_order))
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
    if open_time:
        # The common clock is fixed. Relative time is an independent
        # coordinate until consistency of the remaining rows is tested.
        from einstein_open_time_link import diagnose
        charge_rows = jump.copy()
        charge_rows[1] = .4*jump[0]-.6*jump[1]
        # Canonical momentum coefficients use the Cartesian Gram / pi.
        # Geometric momentum K_ij-g_ij K is 16 G times these coefficients.
        delta_t, _, delta_eta = positions[:3]-positions[3:]
        charge_rows[2] += (6*delta_t-2*delta_eta)/16
        charge_rows[3] += (-delta_t+delta_eta)/16
        for side in (0, 1):
            # 2 * l(l+1) * I_Y/pi multiplies b in the shift generator.
            frame[3*side+1] -= (9.6-1)*traces[4*side+3]
        primary = np.vstack((proper, charge_rows, frame, gauge_rows[1:]))
        hamiltonian = block_diag(left[5], 32*left[4], right[5], 32*right[4], np.zeros((12, 12)))
        # Only the symmetric part enters the quadratic action.
        hamiltonian = (hamiltonian+hamiltonian.T)/2
        diagnose(primary, poisson, hamiltonian, positions[0]-positions[3],
                 np.r_[left[3], right[3], np.zeros(12)], steps, order, n, left[6], right[6])
        return
    constraints = np.vstack((proper, jump, frame, gauge_rows))
    bracket = constraints@poisson@constraints.T
    assert np.linalg.matrix_rank(bracket) == len(bracket)
    assert np.linalg.norm(frame@poisson@jump.T) > 0
    if charge_match:
        # Replace the master jump with the lapse-charge jump at G=1.
        # Keep the raw geometric jump for the existing packet map.
        charge_basis = np.eye(len(constraints))
        index = len(proper) + 1
        charge_basis[index, index-1:index+1] = [.4, -.6]
        raw_log = np.linalg.slogdet(bracket)[1]
        constraints = charge_basis @ constraints
        bracket = constraints @ poisson @ constraints.T
        np.testing.assert_allclose(np.linalg.slogdet(bracket)[1]-raw_log,
                                   2*np.log(.6), atol=1e-9, rtol=0)
        # The source is linear. Check convergence of the original
        # momentum quadratic on homogeneous allowed directions.
        momentum_indices = np.r_[np.arange(n, 2*n), np.arange(3*n, 4*n),
                                 np.arange(4*n+3, 4*n+6), np.arange(4*n+9, 4*n+12)]
        allowed = null_space(constraints[:, momentum_indices])
        physical_kinetic = block_diag(left[4], right[4], np.zeros((6, 6)))
        eigenvalues = np.linalg.eigvalsh(allowed.T@physical_kinetic@allowed)
        negative = eigenvalues[eigenvalues < -1e-9]
        assert len(negative) > 0
        print(f"order={order}: rank={len(bracket)}, physical momentum "
              f"negative directions={len(negative)}, minimum={negative.min():.9g}")
        # Real Lorentzian momenta with e^{-i dt H}, regulated with
        # exp(-epsilon |p|^2/2). This checks the momentum subintegral.
        assert np.min(np.abs(eigenvalues)) > 1e-9
        signature = len(eigenvalues)-2*len(negative)
        scaled = eigenvalues/steps
        limiting_log = -0.5*np.log(abs(scaled)).sum()-1j*np.pi*signature/4
        for relative_epsilon in (1e-3, 1e-6, 1e-9):
            epsilon = relative_epsilon*np.min(abs(scaled))
            regulated_log = -0.5*np.log(epsilon+1j*scaled).sum()
            assert abs(regulated_log-limiting_log) < len(scaled)*relative_epsilon
        print(f"order={order}: momentum dimension={len(scaled)}, signature={signature}, "
              f"Fresnel log modulus={limiting_log.real:.9g}, "
              f"unwrapped phase/pi={limiting_log.imag/np.pi:.9g}")
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
    if charge_match:
        # Physical DeWitt momentum block and the existing control
        # configuration Hessian. Packet weights are excluded here.
        lorentzian_quadratic = block_diag(np.eye(n), left[4],
                                         np.eye(n), right[4], np.zeros((12, 12)))
        lorentzian = dt*np.kron(np.eye(steps+1), lorentzian_quadratic)
        lorentzian -= canonical+canonical.T
        pulled_form = reduced.T @ np.linalg.inv(poisson) @ reduced
        compare_fresnel(lorentzian, joint, subspace, source,
                        (steps+1)*np.linalg.slogdet(bracket)[1],
                        (steps+1)*np.linalg.slogdet(pulled_form)[1])
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
