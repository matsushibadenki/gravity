"""Derive the zero-frequency master normalization from the spatial ADM action."""

import sympy as sp


def check():
    r, width, newton = sp.symbols("r w G", positive=True)
    psi = sp.Function("Psi")(r)
    k = sp.diff(psi, r) + 3 * psi / r
    h = 6 * psi / r - 2 * k + r * sp.diff(k, r)
    # Radial Gauss identity: G_rr=(k_ext^2-tr(k_ext^2)-R_sphere)/2.
    g_rr = sp.diff(k, r) / r - h / r**2 - 2 * k / r**2
    # On C_h=0 the linearized Einstein tensor has zero spatial trace.
    contracted = sp.simplify(r**2 * (h - k) * g_rr)
    energy = sp.diff(psi, r)**2 + 6 * psi**2 / r**2
    assert sp.simplify(contracted - 6 * energy
                       + 6 * sp.diff(psi * sp.diff(psi, r), r)) == 0
    half_kappa = 6 * (4 * sp.pi / 5) / (32 * sp.pi * newton)
    kappa = 2 * half_kappa
    x = sp.symbols("x")
    rho_squared = (3 * (1 - x**2) / (4 * width))**2
    leading_contact = sp.integrate(16 * rho_squared * width / kappa, (x, -1, 1))
    assert leading_contact == 32 * newton / width
    print(f"Static ADM bulk normalization={kappa}, leading contact={leading_contact}")


if __name__ == "__main__":
    check()
