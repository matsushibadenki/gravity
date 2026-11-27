"""Combine the sewn time–area term with the radiative symplectic form."""

import sympy as sp


def check():
    r, g = sp.symbols("r G", positive=True)
    # Two regular quadrupole profiles with independent induced traces
    # at the unit seam. Use dual canonical coordinates for their momenta.
    profiles = (r**3, r**5)
    area_gradient = sp.Matrix([
        (profile.diff(r)+3*profile/r).subs(r, 1) for profile in profiles
    ])
    assert area_gradient == sp.Matrix([6, 8])
    momentum = sp.Matrix(sp.symbols("p_1 p_2"))
    time, flux_a, flux_b = sp.symbols("Delta_T F_a F_b")
    for coefficient in (1/(10*g), -3/(10*g)):
        canonical_momentum = momentum + coefficient*time*area_gradient
        variables = (*momentum, time, flux_a, flux_b)
        mixed = canonical_momentum.jacobian(variables)
        null_time = (-coefficient*area_gradient).col_join(sp.Matrix([1, 0, 0]))
        assert mixed.rank() == 2
        assert mixed*null_time == sp.zeros(2, 1)
        assert mixed[:, 3:] == sp.zeros(2)
        # Both endpoint coordinates and the independent flux labels
        # are held fixed during this triangular momentum change.
        change = canonical_momentum.col_join(sp.Matrix([time, flux_a, flux_b]))
        assert change.jacobian(variables).det() == 1
    print("The time–area term shifts the radiative momentum in both reference prescriptions.")
    print("The mixed block has no extra canonical pair; both flux columns remain zero.")


if __name__ == "__main__":
    check()
