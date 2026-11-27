"""Open-time physical quadratic action with matched flux packets."""

import numpy as np
from numpy.polynomial import Polynomial
from scipy.linalg import block_diag, lu_factor, lu_solve

from einstein_annular_trace_brackets import pairing
from einstein_even_bulk import tensor_basis
from einstein_geometric_shell_transfer import endpoint, integrate, source


def proper_distance_load(basis, lower, upper, geometric):
    nodes, weights = np.polynomial.legendre.leggauss(24)
    radius = lower+(upper-lower)*(1+nodes)/2
    rho = 6*(1-64*(radius-1)**2)
    path = 1+(radius[:, None]-1)*(1+nodes)/2
    path_weights = (radius[:, None]-1)*weights/2
    load = source(basis, lower, upper, geometric)
    for index, field in enumerate(basis):
        if geometric:
            # Keep signed proper distance from the central sphere fixed.
            h = path*field.deriv(2)(path)+field.deriv()(path)-3*field(path)/path
            displacement = -np.sum(path_weights*h, axis=1)/2
        else:
            integrated = np.sum(path_weights*field(path)/path, axis=1)
            displacement = -(radius*field.deriv()(radius)-field.deriv()(1)
                             -3*integrated)/2
        load[index] += 4*(upper-lower)*(weights@(rho*displacement/radius**3))
    return load


def radial_spaces(order):
    r = Polynomial([0, 1])
    inner_k = r**3*(r*r-1)/2
    outer_k = (r-1)*(2-r)
    inside = [r**(3+2*n)*(r*r-1)**2 for n in range(order)] + [r**3-6*inner_k, inner_k]
    outside = [(r-1)**(2+n)*(2-r) for n in range(order)] + [2-r-2*outer_k, outer_k]
    return inside, outside


def assemble(order, geometric):
    inside, outside = radial_spaces(order)
    stiffness, mass, loads = [], [], []
    for basis, lo, hi, collar in ((inside, 0, 1, (.875, 1)),
                                 (outside, 1, 2, (1, 1.125))):
        spatial, temporal = integrate(basis, lo, hi, geometric)
        if geometric:
            spatial += endpoint(basis, lo)-endpoint(basis, hi)
        stiffness.append(spatial)
        mass.append(temporal)
        loads.append(proper_distance_load(basis, *collar, geometric))

    projection = np.zeros((2*(order+2), 2*(order+1)))
    projection[:order, :order] = np.eye(order)
    projection[order+2:2*order+2, order:2*order] = np.eye(order)
    projection[order:order+2, -2:] = projection[-2:, -2:] = np.eye(2)
    return (projection.T@block_diag(*stiffness)@projection,
            projection.T@block_diag(*mass)@projection,
            projection.T@np.concatenate(loads))


def integrate_spatial_embedding(action, phase, source, sites, steps):
    # Lift the central trace K by its radial displacement 2*X. The
    # RW master trace already has zero spatial gauge variation.
    size = len(action)
    count = steps+1
    lift = np.zeros((size, count))
    for t in range(steps+1):
        lift[(t+1)*sites-1, t] = 2.  # radial displacement of the unit sphere
    mixed = action@lift
    unit, zero = np.eye(count), np.zeros((count, count))
    empty = np.zeros((size, count))
    bordered = np.block([[action, mixed, empty],
                         [mixed.T, lift.T@mixed, unit],
                         [empty.T, unit, zero]])
    # A real bordered matrix evaluates the absolute Fourier-multiplier
    # determinant and the constrained inverse. Gauge FP is unity.
    lu = lu_factor(bordered)
    logdet = np.log(abs(np.diag(lu[0]))).sum()
    augmented_phase = np.concatenate((phase, lift.T@phase, np.zeros(count)))
    augmented_source = np.concatenate((source, lift.T@source, np.zeros(count)))
    solved_phase = lu_solve(lu, augmented_phase)
    solved_source = lu_solve(lu, augmented_source)
    return (logdet, augmented_phase@solved_phase,
            augmented_phase@solved_source, augmented_source@solved_source)


def log_amplitudes(order, steps, geometric, inverse):
    kappa, dt, sigma = .3, 1/steps, .2
    stiffness, mass, load = assemble(order, geometric)
    time_weights = np.ones(steps+1)
    time_weights[[0, -1]] = .5
    difference = np.diff(np.eye(steps+1), axis=0)
    action = kappa*(dt*np.kron(np.diag(time_weights), stiffness)
                    + np.kron(difference.T@difference, mass)/dt)
    packet = 2*sigma**2*inverse.T@inverse
    phase = np.zeros(len(action), dtype=complex)
    fixed = np.array([2., -3.])
    n = len(load)
    for time_index, orientation in ((0, 1), (steps, -1)):
        seam = slice((time_index+1)*n-2, (time_index+1)*n)
        action[seam, seam] += packet
        phase[seam] = 1j*orientation*inverse.T@fixed
    history = dt*time_weights*(1+.2*np.cos(2*np.pi*np.arange(steps+1)/steps))
    driving = np.kron(history, load)
    logdet = np.linalg.slogdet(action)[1]
    normalization = np.log(2*sigma**2*abs(np.linalg.det(inverse))/np.pi)
    log_zero = normalization + (phase@np.linalg.solve(action, phase)-logdet)/2
    response = driving@np.linalg.solve(action, driving)
    linear = phase@np.linalg.solve(action, driving)
    if geometric:
        lifted_det, lifted_phase, lifted_linear, lifted_response = integrate_spatial_embedding(
            action, phase, driving, n, steps)
        lifted_log = normalization+(lifted_phase-lifted_det)/2
        np.testing.assert_allclose([lifted_det, lifted_log, lifted_linear, lifted_response],
                                   [logdet, log_zero, linear, response], atol=1e-9, rtol=0)
        return np.array([lifted_det, lifted_log, lifted_linear, lifted_response])
    return np.array([logdet, log_zero, linear, response])


def main():
    for order in (2, 3):
        tensors = tensor_basis(order)
        # The trace bracket code orders (K,Psi); this basis orders (Psi,K).
        inverse = np.array(pairing(tensors, 0, 1).inv()-pairing(tensors, 1, 2).inv(),
                           dtype=float)[:, ::-1]
        for steps in (4, 8):
            gap = log_amplitudes(order, steps, True, inverse)-log_amplitudes(
                order, steps, False, inverse)
            np.testing.assert_allclose(gap, 0, atol=1e-8, rtol=0)
            print(f"order={order} links={steps}: logdet={abs(gap[0]):.3e}, "
                  f"log amplitude={abs(gap[1]):.3e}, source quadratic={abs(gap[3]):.3e}")


if __name__ == "__main__":
    main()
