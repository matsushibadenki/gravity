"""Physical static ADM–GHY Hessian on a common ball and annulus basis."""

import numpy as np
from numpy.polynomial import Polynomial
from numpy.polynomial.legendre import leggauss


def integrate(basis, lower, upper, geometric):
    x, w = leggauss(24)
    r = lower + (upper-lower)*(1+x)/2
    weight = w*(upper-lower)/2
    psi = np.array([p(r) for p in basis]).T
    derivative = np.array([p.deriv()(r) for p in basis]).T
    second = np.array([p.deriv(2)(r) for p in basis]).T
    k = derivative + 3*psi/r[:, None]
    dk = second + 3*derivative/r[:, None] - 3*psi/r[:, None]**2
    h = 6*psi/r[:, None] - 2*k + r[:, None]*dk

    def pair(a, b):
        return a.T @ (weight[:, None]*b)

    if geometric:
        difference = h-r[:, None]*dk
        stiffness = -(pair(difference, difference)/2+pair(h, k)+pair(k, h))/3
    else:
        stiffness = pair(derivative, derivative)+pair(psi/r[:, None], psi/r[:, None])*6
    return stiffness, pair(psi, psi)


def endpoint(basis, r):
    if r == 0:
        return np.zeros((len(basis), len(basis)))
    psi = np.array([p(r) for p in basis])
    k = np.array([p.deriv()(r) for p in basis]) + 3*psi/r
    return (9*np.outer(psi, psi)/r-r*np.outer(k, k))/3


def source(basis, lower, upper, geometric):
    x, w = leggauss(24)
    r = lower + (upper-lower)*(1+x)/2
    weight = w*(upper-lower)/2
    rho = 3*(1-((r-1)/.125)**2)/(4*.125)
    psi = np.array([p(r) for p in basis])
    derivative = np.array([p.deriv()(r) for p in basis])
    intrinsic = (4*(derivative+3*psi/r)/r**2 if geometric
                 else 4*derivative/r**2+12*psi/r**3)
    return intrinsic @ (weight*rho)


def check(order):
    r = Polynomial([0, 1])
    basis = [r**3*(1-r*r/4)*(r*r/4)**n for n in range(order)]
    ball, ball_mass = integrate(basis, 0, 1, True)
    shell, shell_mass = integrate(basis, 1, 2, True)
    master, master_mass = integrate(basis, 0, 2, False)
    # Separate geometric endpoint terms and compare each region independently.
    for a, b, geometric in ((0, 1, ball), (1, 2, shell)):
        reference, _ = integrate(basis, a, b, False)
        np.testing.assert_allclose(geometric-endpoint(basis, b)+endpoint(basis, a),
                                   reference, atol=2e-12, rtol=0)
    stiffness = ball + shell - endpoint(basis, 2)
    np.testing.assert_allclose(stiffness, master, atol=2e-12, rtol=0)
    load = source(basis, .875, 1, True)+source(basis, 1, 1.125, True)
    master_load = source(basis, .875, 1.125, False)
    for mode in (0, 1, 2):
        omega2 = 64*4*np.sin(np.pi*mode/8)**2
        adm = .3*(stiffness + omega2*(ball_mass+shell_mass))
        reference = .3*(master + omega2*master_mass)
        log_gap = np.linalg.slogdet(adm)[1]-np.linalg.slogdet(reference)[1]
        source_gap = load@np.linalg.solve(adm, load)-master_load@np.linalg.solve(
            reference, master_load)
        np.testing.assert_allclose([log_gap, source_gap], 0, atol=2e-6)
        print(f"order={order}, frequency={mode}: logdet gap={log_gap:+.2e}, "
              f"source gap={source_gap:+.2e}")


if __name__ == "__main__":
    for size in (3, 4, 5):
        check(size)
