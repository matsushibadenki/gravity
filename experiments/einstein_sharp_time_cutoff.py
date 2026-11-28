"""Track the sharp area trace in nested regular radiative spaces."""

import sympy as sp


def trace_norm(order):
    # Reference seam r=1, outer radius r=2. Modes are regular at the
    # origin and vanish at the outer boundary.
    r = sp.symbols("r", positive=True)
    modes = [r**(3+2*j)*(4-r**2) for j in range(order)]
    moments = []
    for j in range(2*order-1):
        power = 6+2*j
        # Integral of r^power (4-r^2)^2 on [0, 2].
        moment = sum(sp.Rational(coefficient*2**(power+offset+1), power+offset+1)
                     for offset, coefficient in ((0, 16), (2, -8), (4, 1)))
        moments.append(moment)
    gram = sp.Matrix(order, order, lambda i, j: moments[i+j])
    trace = sp.Matrix([
        (mode.diff(r)+3*mode/r).subs(r, 1) for mode in modes
    ])
    representer = gram.inv()*trace
    norm = (trace.T*representer)[0]
    assert gram*representer == trace
    return norm


def check():
    previous = 0
    for order in (2, 4, 8, 12, 16):
        norm = trace_norm(order)
        assert norm > previous
        previous = norm
        print(f"order={order:2d}  sharp trace norm squared={norm.evalf(12)}")


if __name__ == "__main__":
    check()
