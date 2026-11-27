"""Rank of the geometric flux pairing before and after smooth matching."""

import sympy as sp


def check():
    # The ADM endpoint potential at r=1, in (Psi,K) and (a,b) units.
    harmonic_norm = 4*sp.pi/5
    momentum = harmonic_norm*sp.Matrix([[-3, -6], [1, 0]])
    identity = sp.eye(2)
    zero = sp.zeros(2)
    # Write q_L=q+delta_q/2, q_R=q-delta_q/2, and similarly for f.
    transform = sp.BlockMatrix([[identity, identity/2],
                                 [identity, -identity/2]]).as_explicit()
    oriented = sp.diag(momentum, -momentum)
    common_relative = transform.T*oriented*transform
    expected = sp.BlockMatrix([[zero, momentum], [momentum, zero]]).as_explicit()
    assert common_relative == expected
    assert common_relative.rank() == 4

    # Enforce metric matching only, and examine the surviving pairing.
    metric_match = sp.eye(4)[:, :2]
    restricted = metric_match.T*common_relative
    assert restricted.rank() == 2
    assert restricted[:, :2] == zero
    assert restricted[:, 2:] == momentum
    # Also match the flux. In these coordinates the endpoint contribution
    # then gives no symplectic density on (common metric, common flux).
    assert restricted*metric_match == zero

    # The common flux is paired to the geometric jump before matching.
    # Its fixed value changes a phase if the jump is present.
    psi, k = sp.symbols("deltaPsi deltaK")
    flux = sp.Matrix([2, -3])
    phase = (sp.Matrix([[psi, k]])*momentum*flux)[0]
    assert sp.expand(phase-harmonic_norm*(12*psi+2*k)) == 0
    # A normalized flux packet transforms to the jump polarization.
    # In canonical momentum units the density is dp=|det M| df.
    sigma = sp.symbols("sigma", positive=True)
    determinant = abs(momentum.det())
    amplitude_squared = 2*sigma**2*determinant/sp.pi
    inverse_covariance = 2*sigma**2*momentum*momentum.T
    gaussian_norm = sp.pi/sp.sqrt(inverse_covariance.det())
    assert sp.simplify(amplitude_squared*gaussian_norm) == 1
    assert determinant == 96*sp.pi**2/25
    print("Independent faces: rank 4. Metric matched: relative flux pairing rank 2.")
    print("Metric and flux matched: common endpoint pairing rank 0.")
    print(f"Common flux (2,-3) couples to the geometric jump as {sp.expand(phase)}.")


if __name__ == "__main__":
    check()
