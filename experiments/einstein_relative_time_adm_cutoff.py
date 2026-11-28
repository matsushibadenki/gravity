"""Compare the strong ADM bulk kinetic link with the required time completion."""

import sympy as sp

from einstein_sharp_time_cutoff import trace_norm


def surface_coefficient():
    r = sp.symbols("r", positive=True)
    radial, angular, time = sp.symbols("F_a F_b T")

    def surface(a, b):
        return r**3*(a**2+12*a*b+12*b**2)/4

    # Match geometrically dressed fluxes. Use zero average time and
    # zero boost representatives. The two faces have opposite orientation.
    def face(displacement):
        return surface(radial-6*displacement/r**2,
                       angular+displacement/r**2)

    sewn = sp.expand(face(time/2)-face(-time/2))
    assert sewn == -12*angular*r*time
    assert sewn.diff(time, 2) == 0
    return sewn.diff(time)


def check():
    linear_flux_term = surface_coefficient()
    print(f"Oriented ADM kinetic surface term per unit relative time: {linear_flux_term}")

    # In either reference prescription, write the energy in the momentum
    # P=p+T v and hold the dressed fluxes fixed during this link test.
    time, projection, linear, base = sp.symbols(
        "T projection linear base", real=True
    )
    curvature = sp.Symbol("curvature", positive=True)
    energy = base+time*(linear-projection)+time**2*curvature/2
    secondary = -energy.diff(time)
    bracket = -secondary.diff(time)
    assert bracket == curvature
    assert bracket/abs(secondary.diff(time)) == 1
    on_constraint = energy.subs(time, sp.solve(secondary, time)[0])
    assert sp.expand(on_constraint-base+(linear-projection)**2/(2*curvature)) == 0
    for order in (2, 4, 8, 12, 16):
        norm = trace_norm(order)
        # In units C^2/kappa the pure T Hessian missing from the
        # Hamiltonian in bare p coordinates is exactly the trace norm.
        assert norm > 0
        print(f"N={order:2d}: bulk T Hessian at fixed bare p=0, "
              f"required Hessian in C^2/kappa units={norm.evalf(12)}, "
              "conditional Dirac ratio=1")


if __name__ == "__main__":
    check()
