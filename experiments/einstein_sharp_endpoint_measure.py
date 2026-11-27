"""Sharp canonical endpoint projection and a separately prepared shared packet."""

import numpy as np
import sympy as sp

from einstein_annular_trace_brackets import pairing
from einstein_even_bulk import tensor_basis
from einstein_geometric_packet_transfer import log_amplitudes
from einstein_jump_packet_transfer import jump_integral


def check_measure():
    g = sp.symbols("G", positive=True)
    charge = sp.Matrix([[6, -4], [0, 1]])/(10*g)
    jacobian = charge.det()
    # Fourier integrating the increments gives delta(charge @ jump).
    # The density for the geometric jump is its inverse determinant.
    assert jacobian == 3/(50*g*g)
    return 1/jacobian


def main():
    print(f"Flat Fourier multiplier density in geometric jump units: {check_measure()}")
    order, steps = 2, 8
    basis = tensor_basis(order)
    inverse = np.array(pairing(basis, 0, 1).inv()-pairing(basis, 1, 2).inv(),
                       dtype=float)[:, ::-1]
    prescribed = log_amplitudes(order, steps, False, inverse)
    sharp = jump_integral(order, steps, True, sharp=True)
    assert abs(sharp[3]-prescribed[3]) > 1
    print(f"Sharp projection susceptibility={sharp[3].real:.9f}, Dirac={prescribed[3].real:.9f}")
    prepared = jump_integral(order, steps, True, sharp=True, shared_packet=inverse)
    gaps = abs(prepared-prescribed)
    np.testing.assert_allclose(gaps, 0, atol=1e-8, rtol=0)
    print(f"Separate shared packet: logdet gap={gaps[0]:.3e}, source gap={gaps[3]:.3e}")


if __name__ == "__main__":
    main()
