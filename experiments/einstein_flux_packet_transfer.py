"""Endpoint flux packets in a reduced Gaussian trace transfer control."""

import numpy as np
import sympy as sp
from scipy.linalg import lu_factor

from einstein_annular_trace_brackets import pairing
from einstein_even_bulk import tensor_basis


def check(order, steps):
    tensors = tensor_basis(order)
    ball, shell = pairing(tensors, 0, 1), pairing(tensors, 1, 2)
    mixed = np.array((ball.inv()-shell.inv()).inv(), dtype=float)
    fixed = np.array([2., -3.])
    sigma, dt = .2, 1/steps
    count = 2*(steps+1)
    # Test oscillator on the shared trace sector. Its Hamiltonian is an
    # auxiliary positive regulator, not the geometric ADM action.
    stiffness = np.diag([2., 3.])
    spatial = dt*np.kron(np.diag([.5]+[1.]*(steps-1)+[.5]), stiffness)
    difference = np.kron(np.diff(np.eye(steps+1), axis=0), np.eye(2))
    # Fourier transform of the unit packet in flux labels. In q space
    # its exponent is -sigma^2 |B^-1 q|^2 + i f0.B^-1 q.
    inverse = np.linalg.inv(mixed)
    packet = 2*sigma**2*inverse.T@inverse
    spatial[:2, :2] += packet
    spatial[-2:, -2:] += packet
    load_phase = np.zeros(count, dtype=complex)
    load_phase[:2] = 1j*np.linalg.solve(mixed.T, fixed)
    load_phase[-2:] = -load_phase[:2]

    # This source is a control in trace coordinates, with the fixed
    # parabolic collar integrated to one at half-width 1/8.
    nodes, weights = np.polynomial.legendre.leggauss(4)
    collar_norm = weights @ (3*(1-nodes**2)/4)
    load = dt*collar_norm*np.kron(np.sin(np.pi*np.arange(steps+1)/steps), [0., 4.])
    # Each link integrates its own flux. A fixed endpoint packet never
    # imposes a value on the interior momenta.
    flux_mass = dt*np.kron(np.eye(steps), inverse@inverse.T)
    canonical_link = np.kron(np.eye(steps), inverse) @ difference
    phase = np.block([[spatial, -1j*canonical_link.T],
                      [-1j*canonical_link, flux_mass]])
    configuration = spatial + difference.T@difference/dt
    flux_density = abs(np.linalg.det(inverse))
    log_phase = np.log(abs(np.diag(lu_factor(phase)[0]))).sum() - 2*steps*np.log(dt) - 2*steps*np.log(flux_density)
    packet_norm_squared = 2*sigma**2*flux_density/np.pi
    log_configuration = np.linalg.slogdet(configuration)[1]
    np.testing.assert_allclose(log_phase, log_configuration, atol=1e-10, rtol=0)
    for j in (0., .1):
        boundary_load = load_phase+j*load
        full = np.r_[boundary_load, np.zeros(2*steps)]
        phase_response = full@np.linalg.solve(phase, full)
        coordinate_response = boundary_load@np.linalg.solve(configuration, boundary_load)
        phase_log = np.log(packet_norm_squared) + (phase_response-log_phase)/2
        coordinate_log = np.log(packet_norm_squared) + (coordinate_response-log_configuration)/2
        np.testing.assert_allclose(phase_log, coordinate_log, atol=1e-10, rtol=0)
    assert np.linalg.norm(mixed.T @ np.array([0., 4.])) > 0
    print(f"order={order}, steps={steps}: log determinant gap={log_phase-log_configuration:+.3e}")


def embedding_check():
    # Under a spatial normal and gradient displacement the embedding
    # compensates the metric contribution to the local curvature.
    w, v = sp.symbols("w v")
    assert sp.expand(4*(2*w-6*v+3*2*v-2*w)) == 0


if __name__ == "__main__":
    embedding_check()
    for order in (2, 3):
        check(order, 8)
