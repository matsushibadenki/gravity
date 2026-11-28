"""First-order time link of the isolated moving-tube boundary block."""

import sympy as sp


def check():
    radius, dt = sp.symbols("a dt", positive=True)
    left, right, momentum, lapse, lapse_r, beta_r, beta_t = sp.symbols(
        "u_left u_right P n n_r beta_r beta_t")
    angular_rate, metric_potential, source, strength = sp.symbols(
        "trace_rate V_h F j")
    orientation = sp.symbols("sigma", nonzero=True)
    # beta_t multiplies D_A Y in the tangential shift. Its divergence
    # in the quadrupole convention is -6 beta_t/a^2.
    velocity_coefficient = -angular_rate/2-2*beta_r/radius-6*beta_t/radius**2
    midpoint = (left+right)/2
    velocity = (right-left)/dt
    potential = (6*midpoint**2/radius+midpoint*(
        8*lapse/radius**2+2*lapse_r/radius+metric_potential))
    hamiltonian = (-(momentum-orientation*velocity_coefficient)**2
                   /(8*orientation*radius)-orientation*potential)
    link = momentum*(right-left)-dt*hamiltonian+dt*strength*source*midpoint
    recovered_momentum = orientation*(velocity_coefficient-4*radius*velocity)
    assert sp.simplify(sp.diff(link,momentum).subs(momentum,recovered_momentum)) == 0
    second_order = dt*(orientation*(-2*radius*velocity**2
                                    +velocity_coefficient*velocity+potential)
                       +strength*source*midpoint)
    assert sp.simplify(link.subs(momentum,recovered_momentum)-second_order) == 0

    # In the complete system these terms add to the bulk and frame rows.
    responses = [8*midpoint/radius**2,2*midpoint/radius,
                 -2*velocity/radius,-6*velocity/radius**2]
    for multiplier, response in zip((lapse,lapse_r,beta_r,beta_t),responses):
        stationarity = sp.diff(link,multiplier).subs(momentum,recovered_momentum)
        assert sp.simplify(stationarity-dt*orientation*response) == 0
    print("Moving-tube link Legendre transform and four multiplier contributions verified.")
    print("P = sigma * (B - 4*a*Delta u/dt).")
    print("Lapse and lapse-jet rows involve midpoint u; both shift rows involve Delta u/dt.")


if __name__ == "__main__":
    check()
