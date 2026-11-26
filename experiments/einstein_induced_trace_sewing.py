"""Reduced boundary change of polarization and exact Gaussian sewing."""

import numpy as np
import sympy as sp

from einstein_collar_gluing import eliminate, radial_block, source_vector


def check_variation():
    h, k, dh, dk, radius, kappa, b = sp.symbols("h K dh dK r kappa B")
    boundary_term = -kappa*h*k + 3*kappa*h**2/(2*radius) + b*h
    master_flux = (kappa*(k - 3*h/radius) - b)*dh
    assert sp.expand(master_flux + sp.diff(boundary_term, h)*dh
                     + sp.diff(boundary_term, k)*dk) == -kappa*h*dk


def check_overlap(cells, j):
    width, kappa = .125, .3
    grid = np.linspace(0, 2, 2*cells + 1)
    inside, outside = grid[:cells+1], grid[cells:]
    left = eliminate(kappa*radial_block(inside, 2)[1:, 1:],
                     source_vector(inside, width, intrinsic=True)[1:])
    right = eliminate(kappa*radial_block(outside, 2)[:-1, :-1][::-1, ::-1],
                      source_vector(outside, width, intrinsic=True)[:-1][::-1])
    a, linear, constant, logdet = np.array([left, right]).T
    f = j*linear
    trace_log = (j*j*constant.sum() - logdet.sum() - np.log(a.sum())
                 + f.sum()**2/a.sum())/2

    # Unitary change of polarization of the reduced boundary wavefunctions.
    # Both wavefunctions use the same phase because one enters as its adjoint.
    curvature_phase = 3*kappa
    b = 3*j/width  # 4*j*rho_w(1), at seam radius one
    quadratic = a - 1j*curvature_phase
    quadratic[1] = quadratic[1].conjugate()
    inverse = 1/quadratic
    total_inverse = inverse.sum()
    signs = np.array([-1j, 1j])
    frequency_linear = np.sum(signs*f*inverse)
    # Integrate in the shifted Fourier coordinate t=kappa*K-b.
    # Its Jacobian cancels the two sqrt(kappa) Fourier prefactors.
    induced_log = ((j*j*constant.sum() - logdet.sum())/2
                   - (np.log(quadratic).sum() + np.log(total_inverse))/2
                   + np.sum(f*f*inverse)/2 + frequency_linear**2/(2*total_inverse))
    np.testing.assert_allclose(induced_log, trace_log, rtol=0, atol=1e-11)
    assert np.isfinite(b)
    print(f"N={cells}, j={j:g}: log overlap difference={abs(induced_log-trace_log):.3e}")


if __name__ == "__main__":
    check_variation()
    for size in (32, 64, 128, 256):
        for source in (0., .1):
            check_overlap(size, source)
