"""Time-domain phase-space sewing from the constrained ADM quadratic action."""

import numpy as np
from scipy.linalg import lu_factor, lu_solve

from einstein_collar_gluing import radial_block, source_vector
from einstein_dynamic_collar_sewing import check as master_check


def assemble(grid, steps, global_left, global_right):
    dt = 1 / steps
    spacing = grid[1] - grid[0]
    kappa = .3
    indices = slice(int(global_left), len(grid)-int(global_right))
    radial = radial_block(grid, 2)[indices, indices]
    weights = np.ones(len(grid))
    weights[[0, -1]] = .5
    weights = weights[indices]
    sites = len(weights)
    difference = np.roll(np.eye(steps), -1, axis=0)-np.eye(steps)
    spatial = dt*kappa*np.kron(np.eye(steps), radial)
    momentum = np.diag(np.tile(dt/(kappa*spacing*weights), steps))
    cross = -1j*np.kron(difference.T, np.eye(sites))
    phase = np.block([[spatial, cross], [cross.T, momentum]])
    time = np.arange(steps)*dt
    profile = 1 + .2*np.cos(2*np.pi*time) + .3*np.sin(4*np.pi*time)
    source = dt*np.kron(profile, source_vector(grid, .125, intrinsic=True)[indices])
    return phase, np.r_[source, np.zeros_like(source)], momentum, sites


def eliminate(matrix, source, kept):
    bulk = np.setdiff1d(np.arange(len(source)), kept)
    block = matrix[np.ix_(bulk, bulk)]
    coupling = matrix[np.ix_(bulk, kept)]
    lu, pivots = lu_factor(block)
    solved = lu_solve((lu, pivots), np.column_stack((coupling, source[bulk])))
    diagonal = np.diag(lu)
    logdet = np.log(abs(diagonal)).sum()
    parity = np.count_nonzero(pivots != np.arange(len(pivots)))
    np.testing.assert_allclose((-1)**parity*np.prod(diagonal/abs(diagonal)), 1, atol=1e-10)
    return (matrix[np.ix_(kept, kept)]-coupling.T@solved[:, :-1],
            source[kept]-coupling.T@solved[:, -1],
            source[bulk]@solved[:, -1], logdet)


def check(cells, steps):
    grid = np.linspace(0, 2, 2*cells+1)
    phase, source, momentum, _ = assemble(grid, steps, True, True)
    empty = np.array([], dtype=int)
    _, _, direct, direct_det = eliminate(phase, source, empty)
    direct_det -= np.linalg.slogdet(momentum)[1]
    # The oriented ADM kinetic boundary weight is nonzero on each face.
    a, b = 2, -3
    flux_action = 16*np.pi*(4*np.pi/5)*(a*a+12*a*b+12*b*b)/4
    sides = []
    for inside, interval in ((True, grid[:cells+1]), (False, grid[cells:])):
        phase, source, momentum, sites = assemble(interval, steps, inside, not inside)
        kept = np.arange(steps)*sites + (sites-1 if inside else 0)
        matrix, linear, constant, logdet = eliminate(phase, source, kept)
        sides.append((matrix, linear, constant, logdet-np.linalg.slogdet(momentum)[1]))
    matrix, linear, constant, logdet = (a+b for a, b in zip(*sides))
    _, _, contribution, seam_det = eliminate(matrix, linear, empty)
    glued, glued_det = constant+contribution, logdet+seam_det
    glued_log = (-glued_det/2-flux_action)+(.005*glued+flux_action)
    master_log, master_source = master_check(cells, steps)
    np.testing.assert_allclose([glued_det, glued], [direct_det, direct], atol=1e-9, rtol=0)
    np.testing.assert_allclose([glued_log, glued],
                               [master_log, master_source], atol=1e-9, rtol=0)
    print(f"ADM phase cells={cells}, time={steps}: determinant gap={abs(glued_det-direct_det):.3e}, "
          f"source quadratic gap={abs(glued-direct):.3e}")


if __name__ == "__main__":
    for cells, steps in ((8, 6), (16, 8), (32, 12)):
        check(cells, steps)
