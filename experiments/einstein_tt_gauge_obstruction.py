"""A proper lapse cannot remove all trace momentum at fixed sphere charges."""

import sympy as sp

from einstein_even_bulk import Q, R2, X, XYZ, Y, lapse_gradient
from einstein_even_shell import integrate


def check():
    r = sp.symbols("r", positive=True)
    # Delta in the ell=2 sector. A proper lapse satisfies N=N'=0.
    lapse = sp.Function("N")(r)
    operator = sp.diff(lapse, r, 2)+2*sp.diff(lapse, r)/r-6*lapse/r**2
    for harmonic in (r**2, r**-3):
        green_flux = r*r*(harmonic*sp.diff(lapse, r)-sp.diff(harmonic, r)*lapse)
        assert sp.expand(r*r*harmonic*operator-sp.diff(green_flux, r)) == 0

    # This momentum satisfies the strong divergence constraint everywhere.
    # Its trace has a nonzero quadrupole harmonic moment.
    momentum = lapse_gradient(R2*Y)
    trace = sp.trace(momentum)
    assert sp.expand(trace+28*Y) == 0
    for i in range(3):
        assert sp.expand(sum(sp.diff(momentum[i, j], XYZ[j]) for j in range(3))) == 0

    # Add TT tensors to impose nonzero flux without modifying the obstruction.
    cross = X*(Q*X).T+(Q*X)*X.T
    tt = (Q, -11*R2*Q+6*cross-4*Y*sp.eye(3))
    angular = 2*(Q*X-Y*X)

    def flux(tensor):
        return sp.Matrix([integrate(direction.dot(tensor*X), 0, 1, surface=True)
                          for direction in (Y*X, angular)])

    flux_basis = sp.Matrix.hstack(*(flux(tensor) for tensor in tt))
    target = sp.Matrix([2, -3])
    coefficients = flux_basis.inv()*(target-flux(momentum))
    momentum += sum((a*t for a, t in zip(coefficients, tt)), sp.zeros(3))
    assert (flux(momentum)-target).applyfunc(sp.simplify) == sp.zeros(2, 1)
    for inner, outer in ((0, 1), (1, 2)):
        moment = integrate(Y*sp.trace(momentum), inner, outer)
        assert moment != 0
        print(f"radii={inner},{outer}: flux=(2,-3), obstructing harmonic moment={moment}")

    # Explicit lapse solving the trace equation cannot obey both traces.
    # Delta(r^4)=14 r^2 in the ell=2 sector.
    a = sp.symbols("a")
    regular = -r**4+a*r*r
    assert sp.expand(operator.subs(lapse, regular).doit()+14*r*r) == 0
    dirichlet = regular.subs(a, 1)
    assert dirichlet.subs(r, 1) == 0 and dirichlet.diff(r).subs(r, 1) == -2
    print("Trace-removing Dirichlet lapse has nonzero normal slope at the seam.")


if __name__ == "__main__":
    check()
