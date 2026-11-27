"""Compare time and boost polarizations of the quadrupole corner."""

import sympy as sp


def check():
    r, g = sp.symbols("r G", positive=True)
    psi, trace, time, eta, adapted = sp.symbols("Psi K T eta beta")
    area_charge = r**2*trace/(10*g)
    green_energy = (-12*psi+6*r*trace)/(20*g)
    curvature_energy = (-12*psi+8*r*trace)/(20*g)
    assert sp.simplify(curvature_energy-green_energy-area_charge/r) == 0

    # Use the convention p_T=-E, p_eta=A_c and hold the reference
    # radius fixed. The change of frame is the same eta-T/r as in omega.
    frame_map = sp.Matrix([time, adapted+time/r])
    jacobian = frame_map.jacobian((time, adapted))
    old_coefficients = sp.Matrix([-curvature_energy, area_charge])
    new_coefficients = sp.Matrix([-green_energy, area_charge])
    assert jacobian.det() == 1
    assert (jacobian.T*old_coefficients-new_coefficients).applyfunc(
        sp.simplify
    ) == sp.zeros(2, 1)

    # A flat reference embedding matched to the conformal quadrupole
    # has normal displacement r K Y/2. For l=2, delta k0=(6-2) f/r^2.
    reference_displacement = r*trace/2
    reference_curvature = (6-2)*reference_displacement/r**2
    reference_energy = 2*r**2*(reference_curvature+2*trace/r)/(20*g)
    subtracted_energy = sp.simplify(curvature_energy-reference_energy)
    assert subtracted_energy == -3*psi/(5*g)
    assert sp.simplify(subtracted_energy-green_energy+3*area_charge/r) == 0
    print("Unsubtracted corner potentials agree under beta = eta - T/r with unit Jacobian.")
    print("The matched flat isometric subtraction gives E_refsub = -3 Psi/(5 G).")


if __name__ == "__main__":
    check()
