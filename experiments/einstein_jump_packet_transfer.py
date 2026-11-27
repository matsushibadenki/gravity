"""Keep independent one-sided traces at the initial and final time slices."""

import numpy as np
from scipy.linalg import block_diag

from einstein_annular_trace_brackets import pairing
from einstein_even_bulk import tensor_basis
from einstein_geometric_packet_transfer import (
    log_amplitudes, proper_distance_load, radial_spaces,
)
from einstein_geometric_shell_transfer import endpoint, integrate


def jump_integral(order, steps, geometric, frame_width=0., *, sharp=False,
                  shared_packet=None):
    n = order+2
    dt, sigma, kappa = 1/steps, .2, .3
    stiffness, mass, source = [], [], []
    for side, basis in enumerate(radial_spaces(order)):
        lo, hi = side, side+1
        matrix, weight = integrate(basis, lo, hi, geometric)
        if geometric:
            matrix += endpoint(basis, lo)-endpoint(basis, hi)
        stiffness.append(matrix)
        mass.append(weight)
        collar = (.875, 1) if side == 0 else (1, 1.125)
        source.append(proper_distance_load(basis, *collar, geometric))

    geometry_jump = np.zeros((2, 2*n))
    geometry_jump[:, n-2:n] = np.eye(2)
    geometry_jump[:, -2:] = -np.eye(2)
    source = np.concatenate(source)
    # Retain both faces at the temporal endpoints. At intermediate
    # slices the geometric and lapse-charge conditions identify both traces.
    common = np.zeros((2*n, 2*n-2))
    common[:n, :n] = np.eye(n)
    common[n:n+order, n:] = np.eye(order)
    common[-2:, n-2:n] = np.eye(2)
    np.testing.assert_array_equal(geometry_jump@common, 0)
    endpoint_space = common if sharp else np.eye(2*n)
    projection = block_diag(endpoint_space, *([common]*(steps-1)), endpoint_space)
    temporal = np.ones(steps+1)
    temporal[[0, -1]] = .5
    differences = np.diff(np.eye(steps+1), axis=0)
    action = kappa*(dt*np.kron(np.diag(temporal), block_diag(*stiffness))
                    + np.kron(differences.T@differences, block_diag(*mass))/dt)

    # Canonical momentum conjugate to the jump, derived from the ADM endpoint.
    momentum = (4*np.pi/5)*np.array([[-3., -6.], [1., 0.]])
    # The frame increments couple to (-Delta E, Delta A_c). A real
    # Gaussian of width tau gives exp(-tau^2 |charge jump|^2/2).
    # Both endpoints use the same prescription, with opposite phase signs.
    frame_charge = np.array([[.6, -.4], [0., .1]])
    frame_map = frame_charge @ geometry_jump
    phase = np.zeros(len(action), dtype=complex)
    for t, orientation in ((0, 1), (steps, -1)):
        segment = slice(2*n*t, 2*n*(t+1))
        action[segment, segment] += (2*sigma**2*geometry_jump.T@momentum@momentum.T@geometry_jump
                                     + frame_width**2*frame_map.T@frame_map)
        phase[segment] = 1j*orientation*geometry_jump.T@momentum@np.array([2., -3.])
    history = dt*temporal*(1+.2*np.cos(2*np.pi*np.arange(steps+1)/steps))
    drive = projection.T@np.kron(history, source)
    phase = projection.T@phase
    action = projection.T@action@projection
    if shared_packet is not None:
        if not sharp:
            raise ValueError("The shared packet requires the sharp junction.")
        packet = 2*sigma**2*shared_packet.T@shared_packet
        center = shared_packet.T@np.array([2., -3.])
        # The common projection stores the shared traces after the ball
        # interior coefficients, rather than as the last two entries.
        size = common.shape[1]
        for t, sign in ((0, 1), (steps, -1)):
            seam = slice(t*size+n-2, t*size+n)
            action[seam, seam] += packet
            phase[seam] += 1j*sign*center
    assert np.linalg.eigvalsh(action)[0] > 0
    logdet = np.linalg.slogdet(action)[1]
    solved = np.linalg.solve(action, np.column_stack((phase, drive)))
    normalization = np.log(2*sigma**2*abs(np.linalg.det(momentum))/np.pi)
    if shared_packet is not None:
        # Divide out the constant projected jump weight before normalizing
        # the independently prepared state on the shared geometry.
        normalization = np.log(2*sigma**2*abs(np.linalg.det(shared_packet))/np.pi)
    log_zero = normalization + (phase@solved[:, 0]-logdet)/2
    response = drive@solved[:, 1]

    return np.array([logdet, log_zero, phase@solved[:, 1], response])


def check(order, steps, inverse):
    geometric = jump_integral(order, steps, True)
    master = jump_integral(order, steps, False)
    np.testing.assert_allclose(geometric, master, atol=1e-8, rtol=0)
    log_zero, response = geometric[[1, 3]]
    print(f"same-packet logdet gap={abs(geometric[0]-master[0]):.3e}, "
          f"source gap={abs(geometric[3]-master[3]):.3e}")
    _, reference_log, _, reference_response = log_amplitudes(order, steps, False, inverse)
    gap = abs(response-reference_response)
    assert gap > 1e-6
    print(f"order={order} links={steps}: jump susceptibility={response:.9g}, "
          f"shared susceptibility={reference_response.real:.9g}, difference={gap:.6g}, "
          f"log amplitude difference={abs(log_zero-reference_log):.6g}")


if __name__ == "__main__":
    for order in (2, 3):
        tensors = tensor_basis(order)
        inverse = np.array(pairing(tensors, 0, 1).inv()-pairing(tensors, 1, 2).inv(),
                           dtype=float)[:, ::-1]
        for steps in (4, 8):
            check(order, steps, inverse)
