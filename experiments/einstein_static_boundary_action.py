"""Boundary polarization of the constrained static ADM bulk action."""

import sympy as sp

from einstein_collar_gluing import check as check_composition


def check():
    kappa, h, slope, dh, dslope = sp.symbols("kappa h s dh ds", real=True)
    # The first-derivative bulk action contributes kappa*s*dh at
    # an outward-oriented endpoint. The ADM total derivative is
    # -kappa*h*s/2. The slope is independent of h in the variation.
    raw = kappa * slope * dh - kappa * (slope * dh + h * dslope) / 2
    coefficient = sp.solve(sp.diff(raw, dslope) + kappa * h * sp.Symbol("c"),
                           sp.Symbol("c"))[0]
    assert coefficient == sp.Rational(1, 2)
    dirichlet = sp.expand(raw + coefficient * kappa * (slope * dh + h * dslope))
    assert dirichlet == kappa * slope * dh

    left, right, source = sp.symbols("s_left s_right J")
    # The two regions have opposite normals but the same radial derivative
    # convention. With a common varied trace, stationarity matches flux.
    seam = dirichlet.subs(slope, left) - dirichlet.subs(slope, right) - source * dh
    assert sp.expand(sp.diff(seam, dh) - kappa * (left - right) + source) == 0
    # The smooth collar contributes the same derivative coefficient on both faces.
    collar_coefficient = sp.Symbol("B")
    collar_flux = (dirichlet - collar_coefficient * dh)
    assert sp.expand(collar_flux.subs(slope, left) - collar_flux.subs(slope, right)
                     - kappa * (left - right) * dh) == 0
    print("Dirichlet completion: +kappa*h*s/2 per outward endpoint.")
    print("Shared trace variation: kappa*(s_left-s_right)-J.")
    for cells in (32, 64, 128, 256):
        check_composition(cells, .125, .3, intrinsic=True)


if __name__ == "__main__":
    check()
