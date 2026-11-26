"""Independent traces sewn by geometric metric and lapse-charge conditions."""

import numpy as np
from numpy.polynomial import Polynomial
from scipy.linalg import block_diag

from einstein_geometric_shell_transfer import endpoint, integrate, source


def check(order, mode):
    r = Polynomial([0, 1])
    # Last two basis functions have unit (h,K) boundary traces respectively.
    ball_bubble = r**3*(r*r-1)**2
    ball_k = r**3*(r*r-1)/2
    ball = [ball_bubble*r**(2*n) for n in range(order)] + [r**3-6*ball_k, ball_k]
    shell_k = (r-1)*(2-r)
    shell = [(r-1)**2*(2-r)*(r-1)**n for n in range(order)] + [2-r-2*shell_k, shell_k]
    omega2 = 256*np.sin(np.pi*mode/8)**2
    geometric, master, loads, references = [], [], [], []
    for basis, lo, hi, bounds in (
        (ball, 0, 1, (.875, 1)), (shell, 1, 2, (1, 1.125))
    ):
        stiffness, mass = integrate(basis, lo, hi, True)
        stiffness += endpoint(basis, lo)-endpoint(basis, hi)
        geometric.append(.3*(stiffness+omega2*mass))
        stiffness, mass = integrate(basis, lo, hi, False)
        master.append(.3*(stiffness+omega2*mass))
        loads.append(source(basis, *bounds, True))
        references.append(source(basis, *bounds, False))

    n = order+2
    difference = np.zeros((2, 2*n))
    difference[:, n-2:n] = np.eye(2)
    difference[:, -2:] = -np.eye(2)
    # Constraint order: induced trace jump, Brown–York energy jump (G=1).
    charge_coordinates = np.array([[0., 1.], [-.6, .4]])
    conditions = charge_coordinates @ difference
    adm = block_diag(*geometric)
    bordered = np.block([[adm, conditions.T],
                         [conditions, np.zeros((2, 2))]])
    load = np.concatenate((*loads, np.zeros(2)))
    raw_logdet = np.linalg.slogdet(bordered)[1]
    # Declare the multiplier normalization in trace units. This is the
    # compensating Jacobian, not an independent geometric gauge determinant.
    logdet = raw_logdet - 2*np.linalg.slogdet(charge_coordinates)[1]
    susceptibility = load @ np.linalg.solve(bordered, load)

    # Independent master assembly, with shared value and derivative traces.
    projection = np.zeros((2*n, 2*order+2))
    projection[:order, :order] = np.eye(order)
    projection[n:n+order, order:2*order] = np.eye(order)
    projection[order:n, -2:] = projection[-2:, -2:] = np.eye(2)
    reference = projection.T @ block_diag(*master) @ projection
    reference_load = projection.T @ np.concatenate(references)
    gap = logdet-np.linalg.slogdet(reference)[1]
    response_gap = susceptibility-reference_load @ np.linalg.solve(reference, reference_load)
    np.testing.assert_allclose([gap, response_gap], 0, atol=1e-8, rtol=0)
    print(f"order={order} mode={mode}: logdet gap={abs(gap):.3e}, "
          f"source gap={abs(response_gap):.3e}")


if __name__ == "__main__":
    for order in (2, 3, 4):
        for mode in (0, 1, 2):
            check(order, mode)
