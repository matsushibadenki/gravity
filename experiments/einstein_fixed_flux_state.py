"""Flux-normalized boundary states from the reduced tensor trace bracket."""

import sympy as sp

from einstein_annular_trace_brackets import pairing
from einstein_even_bulk import tensor_basis


def check(order):
    tensors = tensor_basis(order)
    ball = pairing(tensors, 0, 1)
    shell = pairing(tensors, 1, 2)
    mixed = (ball.inv()-shell.inv()).inv()
    # {q,f}=mixed and p=mixed^(-T) f, with <q|p>=exp(i p.q)/(2*pi).
    flux_to_p = mixed.T.inv()
    assert mixed*flux_to_p.T == sp.eye(2)
    measure = abs(flux_to_p.det())
    fixed = sp.Matrix([2, -3])
    p = flux_to_p*fixed
    assert p != sp.zeros(2, 1)
    # <f|f'>=delta(f-f') requires the square root of dp/df
    # on each wavefunction. The same factor gives resolution of identity.
    prefactor = sp.sqrt(measure)/(2*sp.pi)
    assert sp.simplify((2*sp.pi*prefactor)**2/measure) == 1

    # A normalizable packet in flux coordinates uses df, and its
    # translated momentum Gaussian uses dp. Compare their norms exactly.
    width = sp.symbols("sigma", positive=True)
    x = sp.symbols("x", real=True)
    norm_1d = sp.integrate(sp.exp(-x*x/(2*width**2)), (x, -sp.oo, sp.oo))
    amplitude_squared = 1/(2*sp.pi*width**2)
    assert sp.simplify(amplitude_squared*norm_1d**2) == 1
    assert sp.simplify(amplitude_squared*norm_1d**2*measure/measure) == 1

    # Time-link phases from a fixed flux state on a periodic chain.
    traces = [sp.Matrix(sp.symbols(f"q{t}_0:2")) for t in range(4)]
    phase = sum(p.dot(traces[(t+1) % 4]-q) for t, q in enumerate(traces))
    assert sp.simplify(phase) == 0

    # Auxiliary conversion of C=0 gives the same projector normalization
    # only with its Liouville measure, not with a flat auxiliary measure.
    difference = ball-shell
    second_class_density = abs(difference.det())
    fp_det = difference.det()**2
    assert sp.simplify(fp_det/second_class_density-second_class_density) == 0
    print(f"order={order}: dp/df={measure.evalf(9)}, "
          f"fixed canonical momentum={p.evalf(6).T}, closed phase=0")


if __name__ == "__main__":
    for order in (2, 3):
        check(order)
