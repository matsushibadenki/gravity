"""Intrinsic-curvature source in the static even-parity vacuum solution."""

import sympy as sp

from einstein_radial_gluing import compare


def curvature(trace, shear, displacement):
    # Unit sphere, ell=2, h_AB=c Y gamma_AB+d (D_A D_B Y)^TF.
    return 4 * (trace + 3 * shear + 2 * displacement)


def check():
    c, d, displacement, radial, angular = sp.symbols("c d displacement radial angular")
    assert sp.expand(curvature(c + 2 * radial - 6 * angular, d + 2 * angular,
                               displacement - radial)
                     - curvature(c, d, displacement)) == 0

    radius, j = sp.symbols("r j", positive=True)
    # Static scalar-potential sector with h_ij=-2 Phi delta_ij and fixed
    # relational embedding in this gauge. Set u=r Phi in unit normalization.
    # A source j delta R_Sigma couples as -8 j u at r=1.
    regular, exterior = sp.symbols("regular exterior")
    inner = regular * radius**3
    outer = exterior * (radius**-2 - radius**3 / 32)
    seam_source = j * curvature(-2, 0, 0)
    solution = sp.solve([
        inner.subs(radius, 1) - outer.subs(radius, 1),
        sp.diff(inner - outer, radius).subs(radius, 1) - seam_source,
    ], (regular, exterior))
    direct_response = -8 * inner.subs(solution).subs(radius, 1)

    inner = radius**3
    outer = (radius**-2 - radius**3 / 32) * sp.Rational(32, 31)
    # Independent on-shell actions of the two intervals with unit seam value.
    stiffness = sp.diff(inner - outer, radius).subs(radius, 1)
    glued_response = sp.diff(seam_source, j) * seam_source / stiffness
    assert direct_response == glued_response == sp.Rational(62, 5) * j
    for cells in (16, 32, 64, 128):
        log_difference, source_difference, variance = compare(cells, 2, -8 * .1)
        assert abs(log_difference) < 2e-11
        assert abs(-8 * source_difference) < 2e-11
        error = abs(64 * .1 * variance - float(direct_response.subs(j, .1)))
        print(f"cells per side={cells}: geometric response error={error:.3e}")
    print(f"Geometric source response: {direct_response}, seam stiffness: {stiffness}")


if __name__ == "__main__":
    check()
