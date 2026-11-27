"""Physical polynomial phase-space transfer with endpoint flux packets."""

import numpy as np
import sympy as sp
from scipy.linalg import block_diag

from einstein_annular_trace_brackets import pairing
from einstein_even_bulk import tensor_basis
from einstein_compatible_momentum_basis import reconstruct
from einstein_geometric_packet_transfer import (
    assemble, integrate_spatial_embedding, log_amplitudes, radial_spaces,
)
from einstein_projected_lapse_gauge import R, lapse_images, pair


def temporal_gauge(order):
    gram, coupling = [], []
    for side, basis in enumerate(radial_spaces(order)):
        _, images, _ = lapse_images(side, order)
        gram.append(np.array([[pair(a, b, side, side+1) for b in images]
                              for a in images], dtype=float))
        rows = np.zeros((order, 2*order+2))
        for j, field in enumerate(basis):
            profile = sum(sp.Rational(float(c))*R**k for k, c in enumerate(field.coef))
            # Trace of the inverse ADM momentum map in the u=0 section.
            trace = (profile.diff(R)+5*profile/R)/6
            column = j+side*order if j < order else j+order
            rows[:, column] = [float(pair(image, trace, side, side+1)) for image in images]
        coupling.append(rows)
    return block_diag(*gram), np.vstack(coupling)


def tensor_forms(order):
    coefficients = sp.symbols(f"p:{2*order+2}")
    radial_flux, angular_flux = sp.symbols("a b")
    total = 0
    pairing = sp.zeros(len(coefficients), 1)
    for side, shapes in enumerate(radial_spaces(order)):
        indices = list(range(side*order, (side+1)*order))+[2*order, 2*order+1]
        polynomials = [sum(sp.Rational(float(c))*R**k
                          for k, c in enumerate(shape.coef)) for shape in shapes]
        master = sum(coefficients[i]*shape for i, shape in zip(indices, polynomials))
        kinetic, (radial, tangential) = reconstruct(master, radial_flux, angular_flux,
                                                    side, side+1)
        total += kinetic
        for i, psi in zip(indices, polynomials):
            k = psi.diff(R)+3*psi/R
            h = 6*psi/R-2*k+R*k.diff(R)
            pairing[i] += pair(1, radial*h+2*tangential*k, side, side+1)
    assert sp.expand(total).diff(radial_flux) == sp.expand(total).diff(angular_flux) == 0
    assert not (any(pairing.diff(radial_flux)) or any(pairing.diff(angular_flux)))
    kinetic_matrix = np.array(6*sp.hessian(total, coefficients), dtype=float)
    link_matrix = np.array(pairing.jacobian(coefficients), dtype=float)
    return kinetic_matrix, link_matrix


def add_frame_links(action, phase, drive, sites, steps, inverse, pairing_form):
    """Attach independent two-face frame coordinates and momenta to each link."""
    # Per face: coordinate at every slice, charge momentum on every link.
    coordinates = 3*(steps+1)
    momenta = 3*steps
    size = len(action)
    width = 2*(coordinates+momenta)
    enlarged = block_diag(action, np.zeros((width, width), dtype=complex))
    constraints = np.zeros((width, size+width))
    row = 0
    for side, orientation in ((0, 1), (1, -1)):
        start = size+side*(coordinates+momenta)
        for t in range(steps):
            frame = np.arange(start+3*t, start+3*t+3)
            charge = np.arange(start+coordinates+3*t, start+coordinates+3*t+3)
            enlarged[np.ix_(frame, charge)] += 1j*orientation*np.eye(3)
            enlarged[np.ix_(frame+3, charge)] -= 1j*orientation*np.eye(3)
            constraints[row:row+3, charge] = np.eye(3)
            # Match the linear ADM charge definitions while keeping T,X,eta free.
            seam = (t+1)*sites-2
            constraints[row, seam:seam+2] = [-.6, .4]
            constraints[row+1, frame] = [.6, 0., -.6]
            constraints[row+2, seam+1] = -.1
            # In the declared trace polarization f=B^T p. The last
            # two canonical momenta are obtained using the pairing matrix.
            physical = slice((steps+1+t)*sites, (steps+2+t)*sites)
            constraints[row+1, physical] = -np.linalg.solve(
                inverse.T, pairing_form[-2:, :])[1]
            row += 3
    enlarged = enlarged + enlarged.T
    enlarged[:size, :size] = action
    for t in range(steps+1):
        left = np.arange(size+3*t, size+3*t+3)
        right = left+coordinates+momenta
        constraints[row:row+3, left] = np.eye(3)
        constraints[row:row+3, right] = -np.eye(3)
        constraints[row+3:row+6, left] = np.eye(3)/2
        constraints[row+3:row+6, right] = np.eye(3)/2
        row += 6
    assert row == width
    assert np.isclose(np.linalg.slogdet(constraints[:, size:])[1], 0, atol=1e-12)
    bordered = np.block([[enlarged, constraints.T],
                         [constraints, np.zeros((width, width))]])
    return bordered, np.pad(phase, (0, 2*width)), np.pad(drive, (0, 2*width))


def integrate_phase(order, steps, inverse, tensors):
    kappa, sigma, dt = .3, .2, 1/steps
    stiffness, mass, load = assemble(order, geometric=True)
    sites = len(load)
    time_weights = np.ones(steps+1)
    time_weights[[0, -1]] = .5
    difference = np.diff(np.eye(steps+1), axis=0)
    spatial = dt*kappa*np.kron(np.diag(time_weights), stiffness)

    # Momentum is expanded in the same polynomial space, in dual units
    # given by the ADM pullback pairing. The oriented fixed-flux energy
    # cancels on the seam. The bulk form is the positive master form
    # obtained from the DeWitt density.
    kinetic_form, pairing_form = tensors
    np.testing.assert_allclose(kinetic_form, mass, atol=1e-12, rtol=0)
    np.testing.assert_allclose(pairing_form, mass, atol=1e-12, rtol=0)
    kinetic = dt/kappa*np.kron(np.eye(steps), kinetic_form)
    canonical = np.kron(difference, pairing_form)
    phase_source = np.zeros(len(spatial), dtype=complex)
    packet = 2*sigma**2*inverse.T@inverse
    mean_momentum = inverse.T@np.array([2., -3.])
    for t, sign in ((0, 1), (steps, -1)):
        trace = slice((t+1)*sites-2, (t+1)*sites)
        spatial[trace, trace] += packet
        phase_source[trace] = 1j*sign*mean_momentum
    history = dt*time_weights*(1+.2*np.cos(2*np.pi*np.arange(steps+1)/steps))
    drive = np.kron(history, load)

    action = np.block([[spatial, -1j*canonical.T], [-1j*canonical, kinetic]])
    fp, trace_rows = temporal_gauge(order)
    assert np.linalg.norm(trace_rows) > 0
    fp_links = np.kron(np.eye(steps), fp)
    mixing = np.pad(np.kron(np.eye(steps), trace_rows), ((0, 0), (len(spatial), 0)))
    gauge = np.column_stack((mixing, fp_links))
    zero = np.zeros_like(fp_links)
    action = np.block([[block_diag(action, zero), gauge.T], [gauge, zero]])
    phase_source = np.r_[phase_source, np.zeros(len(kinetic)+2*len(fp_links))]
    drive = np.r_[drive, np.zeros(len(kinetic)+2*len(fp_links))]
    action, phase_source, drive = add_frame_links(
        action, phase_source, drive, sites, steps, inverse, pairing_form)
    bordered_log, phase_square, linear, quadratic = integrate_spatial_embedding(
        action, phase_source, drive, sites, steps)
    # Include the normalized Euclidean momentum-link measure and FP density.
    logdet = (bordered_log - np.linalg.slogdet(kinetic)[1]
              - 2*np.linalg.slogdet(fp_links)[1])
    normalization = np.log(2*sigma**2*abs(np.linalg.det(inverse))/np.pi)
    return np.array([logdet, normalization+(phase_square-logdet)/2, linear, quadratic])



def main():
    for order in (2, 3):
        tensors = tensor_basis(order)
        inverse = np.array(pairing(tensors, 0, 1).inv()-pairing(tensors, 1, 2).inv(),
                           dtype=float)[:, ::-1]
        forms = tensor_forms(order)
        for steps in (4, 8):
            phase = integrate_phase(order, steps, inverse, forms)
            reference = log_amplitudes(order, steps, False, inverse)
            gaps = abs(phase-reference)
            np.testing.assert_allclose(gaps, 0, atol=1e-8, rtol=0)
            print(f"order={order}, links={steps}: logdet gap={gaps[0]:.3e}, "
                  f"source quadratic gap={gaps[3]:.3e}")


if __name__ == "__main__":
    main()
