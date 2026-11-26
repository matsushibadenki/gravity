"""One-sheet composition of a static radiative Einstein master mode."""

from math import exp

import numpy as np


def radial_block(grid, ell):
    """Assemble the open interval action, including half endpoint weights."""
    step = grid[1] - grid[0]
    matrix = np.zeros((len(grid), len(grid)))
    for i, pair in enumerate(zip(grid[:-1], grid[1:])):
        potential = [ell * (ell + 1) / r**2 if r else 0 for r in pair]
        matrix[i:i+2, i:i+2] += (
            np.array([[1., -1.], [-1., 1.]]) / step
            + step * np.diag(potential) / 2
        )
    return matrix


def endpoint_action(matrix):
    """Integrate the bulk nodes with measure du/sqrt(2*pi) per node."""
    bulk = matrix[:-1, :-1]
    coupling = matrix[:-1, -1]
    return (
        matrix[-1, -1] - coupling @ np.linalg.solve(bulk, coupling),
        np.linalg.slogdet(bulk)[1],
    )


def compare(cells, ell, source):
    grid = np.linspace(0, 2, 2 * cells + 1)
    # Assemble the full interval independently and impose u(0)=u(2)=0.
    full = radial_block(grid, ell)[1:-1, 1:-1]
    seam = cells - 1
    unit = np.eye(len(full))[:, seam]
    variance = np.linalg.solve(full, unit)[seam]
    direct = -np.linalg.slogdet(full)[1] / 2 + source**2 * variance / 2

    inner = radial_block(grid[:cells+1], ell)[1:, 1:]
    outer = radial_block(grid[cells:], ell)[:-1, :-1][::-1, ::-1]
    left, log_left = endpoint_action(inner)
    right, log_right = endpoint_action(outer)
    stiffness = left + right
    glued = -(log_left + log_right + np.log(stiffness)) / 2 + source**2 / (2 * stiffness)
    return glued - direct, source / stiffness - source * variance, variance


def main():
    # At zero frequency the two ODE solutions are r^(ell+1) and r^(-ell).
    ell = 2
    exact = (1 - 2.**(-2 * ell - 1)) / (2 * ell + 1)
    errors = []
    for cells in (16, 32, 64, 128):
        zero, _, _ = compare(cells, ell, 0.)
        finite, response, variance = compare(cells, ell, .2)
        error = abs(variance - exact)
        errors.append(error)
        print(f"N={cells:3} ratio={exp(zero):.12f} "
              f"log ratio at source={finite:+.3e} "
              f"response difference={response:+.3e} Green error={error:.3e}")
        np.testing.assert_allclose([zero, finite, response], 0, atol=2e-11)
    assert all(new < old / 3 for old, new in zip(errors, errors[1:]))


if __name__ == "__main__":
    main()
