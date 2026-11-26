"""Fixed-collar Gaussian composition with the geometric curvature source."""

import numpy as np
from numpy.polynomial.legendre import leggauss

from einstein_master_collar import response
from einstein_radial_gluing import radial_block


def source_vector(grid, width, intrinsic=False):
    nodes, weights = leggauss(8)
    source = np.zeros(len(grid))
    for i, (left, right) in enumerate(zip(grid[:-1], grid[1:])):
        lo, hi = max(left, 1 - width), min(right, 1 + width)
        if hi <= lo:
            continue
        r = lo + (hi - lo) * (nodes + 1) / 2
        rho = 3 * (1 - ((r - 1) / width)**2) / (4 * width)
        if intrinsic:
            rho = rho / r**2
        step = right - left
        hats = np.array([right - r, r - left]) / step
        derivative = np.array([[-1.], [1.]]) / step
        source[i:i+2] += (derivative + 3 * hats / r) @ (2 * (hi - lo) * weights * rho)
    return source


def eliminate(matrix, source):
    bulk = matrix[:-1, :-1]
    coupling = matrix[:-1, -1]
    solved = np.linalg.solve(bulk, np.column_stack((coupling, source[:-1])))
    return (matrix[-1, -1] - coupling @ solved[:, 0],
            source[-1] - coupling @ solved[:, 1],
            source[:-1] @ solved[:, 1], np.linalg.slogdet(bulk)[1])


def check(cells, width, kappa, intrinsic=False):
    grid = np.linspace(0, 2, 2 * cells + 1)
    full = kappa * radial_block(grid, 2)[1:-1, 1:-1]
    source = source_vector(grid, width, intrinsic)[1:-1]
    direct = source @ np.linalg.solve(full, source)
    direct_logdet = np.linalg.slogdet(full)[1]

    inside, outside = grid[:cells+1], grid[cells:]
    left = eliminate(kappa * radial_block(inside, 2)[1:, 1:],
                     source_vector(inside, width, intrinsic)[1:])
    right = eliminate(kappa * radial_block(outside, 2)[:-1, :-1][::-1, ::-1],
                      source_vector(outside, width, intrinsic)[:-1][::-1])
    stiffness, linear, constant, logdet = np.add(left, right)
    sewn = constant + linear**2 / stiffness
    sewn_logdet = logdet + np.log(stiffness)
    np.testing.assert_allclose([sewn, sewn_logdet], [direct, direct_logdet],
                               atol=2e-11, rtol=0)
    for j in (0., .1):
        np.testing.assert_allclose(-sewn_logdet / 2 + j*j*sewn / 2,
                                   -direct_logdet / 2 + j*j*direct / 2,
                                   atol=2e-11, rtol=0)
    exact = response(width, 32, intrinsic)[0] / kappa
    print(f"N={cells}: log determinant gap={sewn_logdet-direct_logdet:+.2e}, "
          f"susceptibility gap={sewn-direct:+.2e}, continuum error={abs(direct-exact):.3e}")
    return abs(direct - exact)


if __name__ == "__main__":
    # Axisymmetric ell=2 master field, Newton constant set to one.
    mu, weights = leggauss(8)
    shear_norm = 2 * np.pi * (weights @ (2 * (1.5 * (1 - mu**2))**2))
    kappa = shear_norm / (32 * np.pi)
    np.testing.assert_allclose(kappa, .3, atol=1e-14)
    for intrinsic in (False, True):
        print(f"Intrinsic curvature on each collar sphere: {intrinsic}")
        errors = [check(n, .125, kappa, intrinsic) for n in (32, 64, 128, 256)]
        assert all(new < old / 3 for old, new in zip(errors, errors[1:]))
