"""Gaussian-regulated integral of the temporal and boost endpoint phases."""

import numpy as np
from numpy.polynomial.hermite import hermgauss

from einstein_annular_trace_brackets import pairing
from einstein_even_bulk import tensor_basis
from einstein_geometric_packet_transfer import log_amplitudes
from einstein_jump_packet_transfer import jump_integral


def check_fourier_factor():
    nodes, weights = hermgauss(24)
    width = 2.
    jump = [.2, -.3]
    charge = np.array([[.6, -.4], [0., .1]]) @ jump
    for sign in (-1, 1):
        factors = weights @ np.exp(1j*sign*np.sqrt(2)*width*nodes[:, None]*charge)
        np.testing.assert_allclose(np.prod(factors)/np.pi,
                                   np.exp(-width**2*charge@charge/2), atol=1e-14)


def main():
    check_fourier_factor()
    order, steps = 2, 8
    tensors = tensor_basis(order)
    inverse = np.array(pairing(tensors, 0, 1).inv()-pairing(tensors, 1, 2).inv(),
                       dtype=float)[:, ::-1]
    shared = log_amplitudes(order, steps, False, inverse)[3].real
    response = []
    for width in (0., 2., 8., 32., 128.):
        geometric = jump_integral(order, steps, True, width)
        master = jump_integral(order, steps, False, width)
        np.testing.assert_allclose(geometric, master, atol=1e-7, rtol=0)
        response.append(geometric[3].real)
        print(f"frame width={width:g}: response={response[-1]:.9f}, "
              f"Dirac packet={shared:.9f}, logdet gap={abs(geometric[0]-master[0]):.3e}, "
              f"source gap={abs(geometric[3]-master[3]):.3e}")
    assert all(a > b for a, b in zip(response, response[1:]))
    assert abs(response[-1]-shared) > 1e-3


if __name__ == "__main__":
    main()
