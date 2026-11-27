"""Strong ADM momentum regulator with independent master and flux coordinates."""

import sympy as sp

from einstein_projected_lapse_gauge import R, lapse_images, pair


def amplitudes(master, u):
    b = (R*u.diff(R)+u-master/(3*R))/4
    a = u-2*b
    c = (R*a.diff(R)+2*a-6*b)/2
    d = (R*b.diff(R)+3*b+c)/2
    return tuple(sp.expand(item) for item in (a, b, c, d))


def reconstruct(master, radial, angular, lo, hi):
    seam_u = radial+2*angular
    seam_slope = 2*angular-radial+master.subs(R, 1)/3
    if lo == 0:
        u = seam_u+seam_slope*(R**2-1)/2
    else:
        t = R-1
        u = seam_u*(1-3*t**2+2*t**3)+seam_slope*t*(1-t)**2
        # Zero outer flux. The selected master profiles vanish at r=2.
    _, images, harmonics = lapse_images(lo, 2)
    a, b, c, d = amplitudes(master, u)
    before = a+2*c
    gauge_gram = sp.Matrix([[pair(i, j, lo, hi) for j in images] for i in images])
    orbit = -gauge_gram.inv()*sp.Matrix([pair(i, before, lo, hi) for i in images])
    lapses, _, _ = lapse_images(lo, 2)
    u += 4*sum(k*lapse for k, lapse in zip(orbit, lapses))/R**2
    a, b, c, d = amplitudes(master, u)
    assert sp.expand(a.diff(R)+(2*a-2*c-6*b)/R) == 0
    assert sp.expand(b.diff(R)+(3*b+c-2*d)/R) == 0
    assert sp.expand(a.subs(R, 1)-radial) == sp.expand(b.subs(R, 1)-angular) == 0
    if lo:
        assert a.subs(R, 2) == b.subs(R, 2) == 0
    for harmonic in harmonics:
        assert pair(harmonic, a+2*c-before, lo, hi) == 0
    for image in images:
        assert pair(image, a+2*c, lo, hi) == 0
    reconstructed = (R**3*a).diff(R, 2)-(R**2*(a+2*c)).diff(R)+R*(-3*a+6*c)
    assert sp.expand(reconstructed-master) == 0
    kinetic = a*a+12*b*b+2*c*c+12*d*d-(a+2*c)**2/2
    return pair(1, kinetic, lo, hi), (a, c)


def check():
    p, q, s, t, a, b = sp.symbols("p q s t a b", real=True)
    ball = p*R**3+q*R**5
    shell = (2-R)*(s+t*(R-1))
    left, left_momentum = reconstruct(ball, a, b, 0, 1)
    right, right_momentum = reconstruct(shell, a, b, 1, 2)
    total = sp.expand(left+right)
    reference = (sp.integrate(ball**2, (R, 0, 1))+sp.integrate(shell**2, (R, 1, 2)))/12
    assert sp.expand(total-reference) == 0
    assert sp.hessian(total, (p, q, s, t)).is_positive_definite
    assert total.diff(a) == total.diff(b) == 0
    # Direct symplectic pairing with global regular metric profiles.
    # Their values and slopes agree at the seam, while the momenta can differ.
    for metric in (R**3*(4-R**2), R**5*(4-R**2)):
        k = metric.diff(R)+3*metric/R
        h = 6*metric/R-2*k+R*k.diff(R)
        pairing = 0
        expected = 0
        for (radial, tangent), master, lo, hi in (
            (left_momentum, ball, 0, 1), (right_momentum, shell, 1, 2),
        ):
            pairing += pair(1, radial*h+2*tangent*k, lo, hi)
            expected += sp.integrate(master*metric, (R, lo, hi))
        assert sp.expand(pairing-expected) == 0
    print("Direct ADM symplectic pairing matches the master pairing for two shared metric profiles.")
    print("Both strong constraints and projected gauge hold exactly.")
    print("Sewn kinetic form positive on four master modes, independent of both common fluxes.")
    print(total)


if __name__ == "__main__":
    check()
