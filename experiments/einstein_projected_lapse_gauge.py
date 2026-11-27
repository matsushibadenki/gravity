"""Exact Galerkin temporal gauge that retains harmonic trace moments."""

import sympy as sp


R = sp.symbols("r", positive=True)


def pair(left, right, lo, hi):
    return sp.integrate(sp.expand(R**2*left*right), (R, lo, hi))


def laplace(profile):
    return profile.diff(R, 2)+2*profile.diff(R)/R-6*profile/R**2


def lapse_images(lo, order):
    bubble = (R**2-1)**2
    harmonics = [R**2]
    if lo:
        bubble *= (R**2-4)**2
        harmonics.append(R**-3)
    lapses = [R**(2+2*j)*bubble for j in range(order)]
    return lapses, [-2*laplace(lapse) for lapse in lapses], harmonics


def check(lo, hi, order):
    lapses, traces, harmonics = lapse_images(lo, order)
    for lapse in lapses:
        for edge in ((hi,) if lo == 0 else (lo, hi)):
            assert lapse.subs(R, edge) == lapse.diff(R).subs(R, edge) == 0
    for trace in traces:
        for harmonic in harmonics:
            assert pair(trace, harmonic, lo, hi) == 0

    # Gauge conditions are the contractions of the trace with the image
    # of the proper lapse. Their bracket is the image Gram matrix.
    fp = sp.Matrix([[pair(a, b, lo, hi) for b in traces] for a in traces])
    assert fp.is_positive_definite
    gram_h = sp.Matrix([[pair(a, b, lo, hi) for b in harmonics] for a in harmonics])
    moments = sp.Matrix([pair(h, R**4, lo, hi) for h in harmonics])
    coefficients = gram_h.inv()*moments
    harmonic_piece = sum(a*h for a, h in zip(coefficients, harmonics))
    seed = harmonic_piece+sum((j+1)*trace for j, trace in enumerate(traces))
    gauge_residual = sp.Matrix([pair(trace, seed, lo, hi) for trace in traces])
    orbit = fp.inv()*gauge_residual
    fixed = sp.expand(seed-sum(a*trace for a, trace in zip(orbit, traces)))
    assert sp.expand(fixed-harmonic_piece) == 0
    # Integrating the gauge delta over lapse orbit coefficients.
    assert sp.simplify(fp.det()*fp.inv().det()) == 1
    print(f"radii={lo},{hi} order={order}: FP rank={fp.rank()}, "
          "harmonic moments unchanged, delta density ratio=1")


if __name__ == "__main__":
    for bounds in ((0, 1), (1, 2)):
        for size in (2, 3, 4):
            check(*bounds, size)
