"""Same normalized endpoint state for a sewn and uncut radiative kernel."""

import numpy as np
from scipy.linalg import block_diag

from einstein_annular_trace_brackets import pairing
from einstein_even_bulk import tensor_basis
from einstein_geometric_packet_transfer import assemble, proper_distance_load, radial_spaces
from einstein_geometric_shell_transfer import endpoint, integrate


def logdet(matrix):
    # Analytic branch from positive damping on the Lorentzian Gaussian.
    eig = np.linalg.eigvals(matrix)
    assert np.min(eig.real) > -1e-9
    return np.log(eig).sum()


def condense(matrix, load, shared):
    private = np.setdiff1d(np.arange(len(load)), shared)
    a = matrix[np.ix_(private, private)]
    b = matrix[np.ix_(private, shared)]
    solution = np.linalg.solve(a, np.column_stack((b, load[private])))
    return (matrix[np.ix_(shared, shared)]-b.T@solution[:, :-1],
            load[shared]-b.T@solution[:, -1],
            load[private]@solution[:, -1], logdet(a))


def kernel(k, mass, drive, steps, j):
    dt = 1/steps
    weights = np.ones(steps+1)
    weights[[0, -1]] = .5
    diff = np.diff(np.eye(steps+1), axis=0)
    action = -.3j*(np.kron(diff.T@diff, mass)/dt-dt*np.kron(np.diag(weights), k))
    load = 1j*j*np.kron(dt*weights*(1+.2*np.cos(2*np.pi*np.arange(steps+1)/steps)), drive)
    return action, load


def add_packet(action, load, precision, center):
    sites = len(center)
    for offset, sign in ((0, 1), (len(load)-sites, -1)):
        face = slice(offset, offset+sites)
        action[face, face] += precision
        load[face] += 1j*sign*center


def check(order, steps):
    tensors = tensor_basis(order)
    inverse = np.array(pairing(tensors, 0, 1).inv()-pairing(tensors, 1, 2).inv(),
                       dtype=float)[:, ::-1]
    shared_width = 2*.2**2*inverse.T@inverse
    shared_center = inverse.T@np.array([2., -3.])
    k, mass, drive = assemble(order, False)
    sites = len(drive)
    width = block_diag(np.eye(sites-2), shared_width)
    center = np.r_[np.zeros(sites-2), shared_center]
    # One normalized real Gaussian envelope at each endpoint, in dq.
    packet_log = (np.linalg.slogdet(width)[1]-sites*np.log(np.pi))/2
    # Integrating the link momenta gives the usual free real-time prefactor.
    def normalization(mass_log):
        return (packet_log+sites*np.log(2*np.pi)/2+
                steps*(mass_log+sites*(np.log(.3*steps)-1j*np.pi/2))/2)

    sides = []
    for basis, lo, hi, collar in zip(radial_spaces(order), (0,1), (1,2),
                                     ((.875,1), (1,1.125))):
        spatial, local_mass = integrate(basis, lo, hi, True)
        spatial += endpoint(basis, lo)-endpoint(basis, hi)
        sides.append((spatial, local_mass, proper_distance_load(basis,*collar,True)))

    mass_seam = [condense(m, np.zeros(len(m)), np.arange(order,order+2))
                 for _,m,_ in sides]
    mass_log = sum(s[3] for s in mass_seam)+logdet(sum(s[0] for s in mass_seam))
    for j in (0., .1, -.1):
        action, load = kernel(k, mass, drive, steps, j)
        add_packet(action, load, width, center)
        direct = normalization(np.linalg.slogdet(mass)[1]) + (
            load@np.linalg.solve(action, load)-logdet(action))/2
        pieces = []
        for spatial, local_mass, local_drive in sides:
            action, load = kernel(spatial, local_mass, local_drive, steps, j)
            add_packet(action, load, np.diag(np.r_[np.ones(order),0.,0.]),
                       np.zeros(order+2))
            shared = np.arange(len(load)).reshape(steps+1,order+2)[:, -2:].ravel()
            pieces.append(condense(action, load, shared))
        seam, linear, constant, log_private = map(sum, zip(*pieces))
        add_packet(seam, linear, shared_width, shared_center)
        sewn = normalization(mass_log)+(constant+linear@np.linalg.solve(seam,linear)
                                        -log_private-logdet(seam))/2
        difference = np.expm1(sewn-direct)
        assert abs(difference) < 5e-8
        print(f"N={order}, links={steps}, j={j:+g}: "
              f"|sewn/uncut-1|={abs(difference):.3g}, uncut log modulus={direct.real:.8g}")


if __name__ == "__main__":
    for cutoff in (2,3,4):
        check(cutoff, 3)
