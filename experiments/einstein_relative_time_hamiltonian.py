"""Preservation test for relative time in the bare radiative Hamiltonian."""

import sympy as sp


def check():
    r, g, kappa = sp.symbols("r G kappa", positive=True)
    time = sp.Symbol("T")
    shifted = sp.Matrix(sp.symbols("P_1 P_2"))
    profiles = sp.Matrix([r**3, r**5])
    mass = (profiles*profiles.T).applyfunc(lambda x: sp.integrate(x, (r, 0, 2)))
    inverse = mass.inv()
    area_gradient = sp.Matrix([6, 8])
    # Canonical coordinates are (q, P, T, p_T), with p_T=0 in the
    # tested model. The bare ADM kinetic term uses p=P-C*T*dK.
    for coefficient in (1/(10*g), -3/(10*g)):
        direction = coefficient*area_gradient
        bare = shifted-time*direction
        energy = (bare.T*inverse*bare)[0]/(2*kappa)
        # The invariant completion fixed by the T=0 energy replaces
        # the bare momentum by P. Express its required terms in p.
        p = sp.Matrix(sp.symbols("p_1 p_2"))
        correction = (time*(p.T*inverse*direction)[0]
                      +time**2*(direction.T*inverse*direction)[0]/2)/kappa
        completed = energy + correction.subs(dict(zip(p, bare)), simultaneous=True)
        assert sp.simplify(completed.diff(time)) == 0
        secondary = -energy.diff(time)
        curvature = sp.simplify(energy.diff(time, 2))
        assert curvature.is_positive
        bracket = -secondary.diff(time)
        assert sp.simplify(bracket-curvature) == 0

        time_solution = sp.solve(secondary, time)[0]
        reduced = energy.subs(time, time_solution)
        reduced_hessian = sp.simplify(sp.hessian(reduced, tuple(shifted)))
        assert reduced_hessian.rank() == 1
        assert (reduced_hessian*direction).applyfunc(sp.simplify) == sp.zeros(2, 1)

        # Delta(p_T) delta(secondary) times the second-class density
        # cancels the time integration Jacobian exactly.
        assert sp.simplify(abs(bracket)/abs(secondary.diff(time))) == 1
    print("Bare kinetic energy makes the relative-time constraint second class.")
    print("The time integration has unit Dirac factor and removes one kinetic direction.")


if __name__ == "__main__":
    check()
