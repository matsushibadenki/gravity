"""Test the direct smooth-junction projection of a geometric jump packet."""

import sympy as sp

from einstein_temporal_frame_links import frame_charge


def check():
    sigma = sp.Rational(1, 5)
    q = sp.Matrix(sp.symbols("Psi K", real=True))
    jump = sp.Matrix(sp.symbols("dPsi dK", real=True))
    flux = sp.Matrix([2, -3])
    matrix = (4*sp.pi/5)*sp.Matrix([[-3, -6], [1, 0]])
    normalization = sp.sqrt(2*sigma**2*abs(matrix.det())/sp.pi)
    jump_packet = normalization*sp.exp(-sigma**2*(matrix.T*jump).dot(matrix.T*jump)
                                       +sp.I*jump.dot(matrix*flux))
    # A sharp smooth-junction projection integrates the jump against its
    # delta. It evaluates the packet at zero jump, rather than Fourier
    # transforming it into a packet of the shared metric.
    projected = jump_packet.subs(dict.fromkeys(jump, 0))
    assert projected == normalization
    assert all(sp.diff(projected, x) == 0 for x in q)
    inverse = sp.Matrix(2, 2, sp.symbols("B0:4", real=True))
    # The logarithmic modulus Hessian suffices to exclude equality up
    # to normalization for every real invertible Dirac flux map.
    dirac_log_modulus = -sigma**2*(inverse*q).dot(inverse*q)
    hessian = sp.hessian(dirac_log_modulus, tuple(q))
    assert sp.factor(hessian.det()) == 4*sigma**4*inverse.det()**2

    # Check the coupled tilted-frame slice condition with independent
    # boundary coordinates and charges before enforcing the slice.
    g = sp.symbols("G", positive=True)
    frames = [sp.Matrix(sp.symbols(f"{side}0:3")) for side in ("left", "right")]
    momenta = [sp.Matrix(sp.symbols(f"p{side}0:3")) for side in ("left", "right")]
    next_frames = [sp.Matrix(sp.symbols(f"next{side}0:3")) for side in ("left", "right")]
    charges = [frame_charge(q[1]+sign*jump[1]/2, q[0]+sign*jump[0]/2,
                            frame[0], frame[2], flux[1], g)
               for sign, frame in zip((1, -1), frames)]
    conditions = (momenta[0]-charges[0]).col_join(momenta[1]-charges[1])
    conditions = conditions.col_join(frames[0]-frames[1]).col_join((frames[0]+frames[1])/2)
    assert abs(conditions.jacobian(list(momenta[0])+list(momenta[1])
                                   +list(frames[0])+list(frames[1])).det()) == 1
    phase = (charges[0].dot(next_frames[0]-frames[0])
             - charges[1].dot(next_frames[1]-frames[1]))
    common = phase.subs(dict(zip(frames[1], frames[0]))).subs(
        dict(zip(next_frames[1], next_frames[0])))
    assert sp.expand(common.subs(dict.fromkeys(jump, 0))) == 0
    delta_t = next_frames[0][0]-frames[0][0]
    delta_eta = next_frames[0][2]-frames[0][2]
    expected = (6*jump[0]-4*jump[1])*delta_t/(10*g) + jump[1]*delta_eta/(10*g)
    assert sp.expand(common-expected) == 0
    print("Smooth endpoint projection gives a constant, not a shared-trace Gaussian.")
    print("Tilted-frame coordinate density is unity; phase cancels on fully matched links.")


if __name__ == "__main__":
    check()
