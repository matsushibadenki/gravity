"""Joint ADM/tube Legendre identities with shared lapse and shift slots."""

import sympy as sp


def check():
    radius, dt = sp.symbols("a dt", positive=True)
    mass, orientation = sp.symbols("m sigma", nonzero=True)
    metric_left, metric_right, u_left, u_right = sp.symbols("q0 q1 u0 u1")
    lapse, lapse_jet, radial_shift, tangent_shift = sp.symbols("n nr br bt")
    lapse_bulk, jet_bulk, spatial_force, source, strength = sp.symbols(
        "C_n C_nr V_q F j")
    metric_p, embedding_p = sp.symbols("p P")

    # q denotes the angular trace in this symbolic projection. The
    # ADM shift changes its velocity by the trace of the Lie derivative.
    trace_shift = 4*radial_shift/radius-12*tangent_shift/radius**2
    tube_shift = -2*radial_shift/radius-6*tangent_shift/radius**2
    u = (u_left+u_right)/2
    qdot, udot = sp.symbols("qdot udot")
    velocities = sp.Matrix([qdot,udot])
    kinetic = (mass*(qdot-trace_shift)**2/2
               +orientation*(-2*radius*udot**2-qdot*udot/2+tube_shift*udot))
    potential = (lapse*lapse_bulk+lapse_jet*jet_bulk
                 +orientation*(6*u*u/radius+u*(8*lapse/radius**2
                                                +2*lapse_jet/radius+spatial_force)))
    momenta = sp.Matrix([metric_p,embedding_p])
    matrix = sp.hessian(kinetic,velocities)
    shift_covector = sp.Matrix([sp.diff(kinetic,x).subs({qdot:0,udot:0})
                                for x in velocities])
    stationary_velocity = matrix.inv()@(momenta-shift_covector)
    hamiltonian = ((momenta-shift_covector).T@stationary_velocity)[0]/2
    hamiltonian -= kinetic.subs({qdot:0,udot:0})+potential
    increments = sp.Matrix([metric_right-metric_left,u_right-u_left])
    link = (momenta.T@increments)[0]-dt*hamiltonian+dt*strength*source*u
    substitution = dict(zip(momenta,matrix@increments/dt+shift_covector))
    expected = dt*(kinetic.subs(dict(zip(velocities,increments/dt)))
                   +potential+strength*source*u)
    assert sp.simplify(link.subs(substitution)-expected) == 0

    # Differentiate in the common multipliers before substituting the
    # link momentum equation. The bulk shift term must use the new p.
    changes = [lapse_bulk+orientation*8*u/radius**2,
               jet_bulk+orientation*2*u/radius,
               -4*metric_p/radius-4*orientation*udot/radius,
               12*metric_p/radius**2]
    momentum_equations = {
        metric_p: sp.diff(kinetic,qdot), embedding_p: sp.diff(kinetic,udot)}
    for multiplier, change in zip((lapse,lapse_jet,radial_shift,tangent_shift),changes):
        left = sp.diff(link,multiplier).subs(substitution)/dt
        right = change.subs(momentum_equations).subs(dict(zip(velocities,increments/dt)))
        assert sp.simplify(left-right) == 0
    shift_hessian = sp.simplify(sp.hessian(hamiltonian,(radial_shift,tangent_shift)))
    assert shift_hessian[0,0] != 0
    assert shift_hessian[:,1] == sp.zeros(2,1)
    # Verify elimination before forming secondary constraints. Other ADM
    # slots can contribute to this radial shift coefficient.
    beta_value = sp.solve(sp.diff(hamiltonian,radial_shift),radial_shift)[0]
    eliminated = sp.simplify(hamiltonian.subs(radial_shift,beta_value))
    linear = sp.diff(hamiltonian,radial_shift).subs(radial_shift,0)
    schur = hamiltonian.subs(radial_shift,0)-linear**2/(2*shift_hessian[0,0])
    assert sp.simplify(eliminated-schur) == 0
    print("The trace-projected Hamiltonian has a radial shift quadratic term of rank one.")
    print("Shared lapse and shift link identities verified in the angular-trace projection.")
    print("The corrected metric momentum contains -sigma*u_dot/2.")
    print("The explicit tangential velocity term cancels after replacing the bulk momentum.")


if __name__ == "__main__":
    check()
