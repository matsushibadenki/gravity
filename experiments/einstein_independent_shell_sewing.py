"""Independent one-sided Galerkin integration of the constrained ADM action."""

import numpy as np
from numpy.polynomial import Polynomial

from einstein_collar_gluing import eliminate
from einstein_geometric_shell_transfer import endpoint, integrate, source


def check(order, mode):
    r = Polynomial([0, 1])
    inner = [r**3*(1-r*r)*r**(2*n) for n in range(order)] + [r**3]
    outer = [(r-1)*(2-r)*(r-1)**n for n in range(order)] + [2-r]
    omega2 = 256*np.sin(np.pi*mode/8)**2
    sides = []
    reference = np.zeros((2*order+1, 2*order+1))
    reference_load = np.zeros(len(reference))
    for index, (basis, lower, upper, collar) in enumerate((
        (inner, 0, 1, (.875, 1)), (outer, 1, 2, (1, 1.125))
    )):
        geometric, mass = integrate(basis, lower, upper, True)
        # Fixed master trace variational completion on each oriented face.
        geometric += endpoint(basis, lower)-endpoint(basis, upper)
        load = source(basis, *collar, True)
        sides.append(eliminate(.3*(geometric+omega2*mass), load))

        # Independently assemble the uncut weak form in the C0 space.
        # Only the two endpoint shape functions share a global coefficient.
        stiffness, mass = integrate(basis, lower, upper, False)
        indices = np.r_[np.arange(order)+index*order, 2*order]
        reference[np.ix_(indices, indices)] += .3*(stiffness+omega2*mass)
        reference_load[indices] += source(basis, *collar, False)

    stiffness, linear, constant, logdet = np.add(*sides)
    sewn_det = logdet + np.log(stiffness)
    sewn_source = constant + linear**2/stiffness
    ref_det = np.linalg.slogdet(reference)[1]
    ref_source = reference_load @ np.linalg.solve(reference, reference_load)
    np.testing.assert_allclose([sewn_det, sewn_source], [ref_det, ref_source],
                               atol=1e-8, rtol=0)
    print(f"order={order} frequency={mode}: logdet gap={sewn_det-ref_det:+.2e}, "
          f"source gap={sewn_source-ref_source:+.2e}")


if __name__ == "__main__":
    for size in (2, 3, 4):
        for frequency in (0, 1, 2):
            check(size, frequency)
