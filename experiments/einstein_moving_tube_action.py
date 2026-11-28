"""Lorentzian GHY action of a moving round tube in the flat reference."""

import sympy as sp


def check():
    t = sp.symbols("t", real=True)
    radius = sp.Function("R")(t)
    velocity = sp.diff(radius,t)
    gamma = 1/sp.sqrt(1-velocity**2)
    # n=(gamma*v,gamma) in the (t,r) plane. Along the tube, du/dtau
    # contributes gamma^3 * acceleration to the normal curvature.
    curvature = gamma**3*sp.diff(velocity,t)+2*gamma/radius
    density = sp.simplify(radius**2*curvature/gamma)
    angle = sp.atanh(velocity)
    # Subtract the endpoint joint difference R^2*angle.
    action = 2*radius-2*radius*velocity*angle
    assert sp.simplify(density-action-sp.diff(radius**2*angle,t)) == 0
    r, v = sp.symbols("r v", real=True)
    action = action.subs(velocity,v).subs(radius,r)
    momentum = sp.diff(action,v)
    hamiltonian = sp.simplify(v*momentum-action)
    assert sp.simplify(hamiltonian+2*r/(1-v*v)) == 0
    print("Outward face, in units 4*pi/(8*pi*G):")
    print("L =",sp.series(action,v,0,4))
    print("P =",sp.series(momentum,v,0,3))
    print("H =",sp.series(hamiltonian,v,0,4))
    print("Reversing the normal reverses all three expressions.")


def check_quadrupole():
    """Verify the quadratic term of the deformed tube and endpoint joint."""
    r, radius, t, z = sp.symbols("r a t z", real=True, positive=True)
    epsilon = sp.symbols("epsilon", real=True)
    harmonic = (3*z*z-1)/2
    amplitude = sp.Function("u")(t)
    displacement = amplitude*harmonic
    tube = radius+epsilon*displacement
    velocity = sp.diff(tube,t)
    gradient_squared = (1-z*z)*sp.diff(tube,z)**2
    # Expand the level-set unit normal before taking its divergence.
    inverse_norm = 1+(velocity**2-gradient_squared/r**2)/2
    normal_t = velocity
    normal_r = inverse_norm
    normal_z = -(1-z*z)*sp.diff(tube,z)/r**2
    curvature = (sp.diff(normal_t,t)+sp.diff(r*r*normal_r,r)/r**2
                 +sp.diff(normal_z,z))
    ghy_density = tube**2*curvature.subs(r,tube)*(2-inverse_norm.subs(r,tube))
    joint = sp.diff(tube**2*velocity,t)
    quadratic = sp.expand(sp.series(ghy_density-joint,epsilon,0,3).removeO()).coeff(epsilon,2)
    expected = ((1-z*z)*sp.diff(displacement,z)**2/radius
                -2*radius*sp.diff(displacement,t)**2)
    assert sp.simplify(quadratic-expected) == 0
    angular_integral = sp.integrate(quadratic,(z,-1,1))*2*sp.pi
    expected_integral = 4*sp.pi/5*(6*amplitude**2/radius-2*radius*sp.diff(amplitude,t)**2)
    assert sp.simplify(angular_integral-expected_integral) == 0
    print("Quadrupole tube L2/(angular norm) = 6*u^2/a - 2*a*(du/dt)^2.")


def check_mixed_boundary_variation():
    """Differentiate the boundary metric variation in the tube shape."""
    a, u = sp.symbols("a U", positive=True)
    tt, tx, ty, xx, xy, yy = sp.symbols("U_tt U_tx U_ty U_xx U_xy U_yy")
    metric = sp.diag(-1,1,1)
    curvature = sp.diag(0,1/a,1/a)
    shape_hessian = sp.Matrix([[tt,tx,ty],[tx,xx,xy],[ty,xy,yy]])
    delta_metric = 2*u*curvature
    delta_inverse = -metric*delta_metric*metric
    delta_curvature = -shape_hessian+u*curvature*metric*curvature
    trace = sp.trace(metric*curvature)
    delta_trace = sp.trace(delta_inverse*curvature+metric*delta_curvature)
    by = metric*curvature*metric-trace*metric
    delta_by = (delta_inverse*curvature*metric+metric*delta_curvature*metric
                +metric*curvature*delta_inverse-delta_trace*metric
                -trace*delta_inverse+u*trace*by)
    expected = sp.Matrix([[2*u/a**2-xx-yy,tx,ty],
                          [tx,-tt+yy+u/a**2,-xy],
                          [ty,-xy,-tt+xx+u/a**2]])
    assert sp.simplify(delta_by-expected) == sp.zeros(3)

    # A metric perturbation is pulled back to the moving tube. At this
    # order n and beta are the ADM lapse and covariant shift perturbations.
    lapse, lapse_r, beta_r, velocity = sp.symbols("n n_r beta_r U_t")
    pulled_tt = -2*u*lapse_r+2*beta_r*velocity
    lapse_shift_terms = -(-2*lapse*delta_by[0,0]+by[0,0]*pulled_tt)/2
    assert sp.expand(lapse_shift_terms-
                     (lapse*(2*u/a**2-xx-yy)+2*u*lapse_r/a
                      -2*beta_r*velocity/a)) == 0
    print("Mixed worldtube metric variation verified, including lapse and radial shift.")


if __name__ == "__main__":
    check()
    check_quadrupole()
    check_mixed_boundary_variation()
