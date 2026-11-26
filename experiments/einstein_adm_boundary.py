"""Green identity and oriented corner charges for the linearized ADM constraints."""

import numpy as np
from numpy.polynomial.legendre import leggauss


def check(nodes):
    mu, weight = leggauss(nodes)
    t, radial_weight = (mu + 1) / 2, weight / 2
    weight = 2 * np.pi * weight
    # Axisymmetric quadrupole H = r^2 P_2(cos(theta)), with Laplacian zero.
    p2 = (3 * mu**2 - 1) / 2

    def scalar_flux(radius, orientation):
        h = radius**2 * p2
        dh = 2 * radius * p2
        lapse = (radius**2 - 1) * h
        dlapse = 2 * radius * h + (radius**2 - 1) * dh
        return orientation * radius**2 * (weight @ (2 * h * dlapse - 2 * lapse * dh))

    def shift_flux(radius, orientation):
        # pi = H delta and W = x H, so their normal contraction is r H^2.
        return orientation * 2 * radius**7 * (weight @ p2**2)

    for inner, outer in ((0., 1.), (1., 2.), (0., 2.)):
        r = inner + (outer - inner) * t
        # N=(r^2-1)H has Laplacian 14H. For h_ij=H delta_ij the
        # lapse volume difference is 2 H Delta N. The shift integrand
        # is 2 div(pi W)=14 H^2 for this probe.
        integral = (outer - inner) * (radial_weight @ r**6) * (weight @ p2**2)
        np.testing.assert_allclose(
            [scalar_flux(outer, 1) + scalar_flux(inner, -1),
             shift_flux(outer, 1) + shift_flux(inner, -1)],
            [28 * integral, 14 * integral], rtol=1e-13,
        )

    # At r=1, N=0 and its outward slope is 2 P_2. The tangent
    # trace of the metric variation is 2 P_2 on the same sphere.
    boost = scalar_flux(1., 1)
    area_moment = weight @ (2 * p2**2)
    np.testing.assert_allclose(boost, 2 * area_moment, rtol=1e-13)
    assert abs(boost) > 1 and abs(shift_flux(1., 1)) > 1
    for flux in (scalar_flux, shift_flux):
        np.testing.assert_allclose(flux(1., 1) + flux(1., -1), 0., atol=1e-13)
    print(f"nodes={nodes}: oriented scalar={boost:.10f}, "
          f"shift={shift_flux(1., 1):.10f}, both internal sums zero")


if __name__ == "__main__":
    for count in (4, 8, 16):
        check(count)
