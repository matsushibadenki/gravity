"""Compare the ADM lapse Green term and quasilocal energy gradients."""

import sympy as sp


def check():
    r, newton = sp.symbols("r G", positive=True)
    psi, trace, trace_prime = sp.symbols("Psi K K_r")
    radial_metric = 6*psi/r-2*trace+r*trace_prime
    mean_curvature = trace_prime-radial_metric/r
    norm = (4*sp.pi/5)/(16*sp.pi*newton)
    # Metric canonical potential against the lapse-generated momentum.
    trace_pairing = sp.Matrix([[-3*r**2, -6*r**2], [r**3, 0]])
    lapse_value = sp.Matrix([6/r**2, -1/r**2])
    green_coefficient = norm * trace_pairing*lapse_value
    green_term = norm*r**2*(2*mean_curvature+2*trace/r)
    assert (green_coefficient-sp.Matrix([green_term.diff(psi), green_term.diff(trace)])
            ).applyfunc(sp.simplify) == sp.zeros(2, 1)

    # Include the perturbation K of the sphere area element in the
    # quasilocal term, with sign chosen to compare the gradient of E
    # in the existing p_T = -E charge convention.
    energy = norm * 2*r**2*(mean_curvature+2*trace/r)
    difference = sp.simplify(energy-green_term)
    assert difference == r*trace/(10*newton)
    assert difference.diff(psi) == 0
    print("The lapse-value columns agree on the master trace.")
    print("Their difference is r K/(10 G), entirely in the area trace.")


if __name__ == "__main__":
    check()
