"""Check the bulk clock-curvature basis on conformal and flat clock probes."""

from fractions import Fraction
from math import factorial

import numpy as np


def conformal_row(winding):
    """Normalize by the spatial average of the squared conformal gradient."""
    gradient = np.array([1, 0, 0, 0])
    dot = winding @ gradient
    clock_hessian = np.eye(4, dtype=int) * dot - np.outer(winding, gradient) - np.outer(gradient, winding)
    box_squared = np.trace(clock_hessian)**2
    hessian_squared = np.sum(clock_hessian**2)
    rx = -6 * (winding @ winding)
    ricci = 2 * (dot**2 - winding @ winding)
    assert ricci == box_squared - hessian_squared
    return [rx, ricci, box_squared, hessian_squared]


def flat_form_factor_coefficient(order):
    """Coefficient of s^(order-1) q^(2*order) in the continuum flat probe."""
    return (-1)**order * Fraction(
        2 * factorial(order) - factorial(order + 1), factorial(2 * order + 1))


def main():
    parallel, transverse = np.eye(4, dtype=int)[:2]
    curved = np.array([conformal_row(parallel), conformal_row(transverse)])
    # The flat clock wave is normalized by its integrated Box(T)^2.
    complete = np.vstack((curved, [0, 0, 1, 1]))
    np.testing.assert_array_equal(complete[:, 1], complete[:, 2] - complete[:, 3])
    bulk = complete[:, :3]
    np.testing.assert_array_equal(bulk[:2] @ [2, -6, 3], [0, 0])
    assert np.linalg.matrix_rank(bulk[:2]) == 2
    assert round(np.linalg.det(bulk)) == 12
    coefficients = [flat_form_factor_coefficient(order) for order in (1, 2, 3)]
    assert coefficients[:2] == [0, Fraction(-1, 60)]
    print("Rows for [RX, Ricci-clock, Box(T)^2, Hessian(T)^2]:\n", complete)
    print("Curved-only null direction in the independent bulk basis [RX,Ricci-clock,Box(T)^2]: [2,-6,3]")
    print("Flat-probe form factor coefficients at q^2, sq^4 and s^2q^6:",
          ", ".join(map(str, coefficients)))


if __name__ == "__main__":
    main()
