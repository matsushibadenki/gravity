"""Check the fixed-volume constraint and modular balance of matched local curvature terms."""

import argparse
from math import log, pi
from pathlib import Path

import numpy as np

from pure_local_expansion import curvature_coefficients, local_actions


def ball_balance(einstein, ricci, radius, wave, density):
    # Solve the matched static constraint for a prescribed traceless Fourier source.
    # Phi = 2 Psi gives delta R = 0, and the static momentum constraint is zero.
    psi = density / (-4*einstein*wave**2 + 4*ricci*wave**4)
    phase = wave*radius
    nodes, weights = np.polynomial.legendre.leggauss(32)
    x, w = (nodes+1)/2, weights/2
    boundary = w @ np.cos(phase*x)
    interior = 3*(w @ (x**2 * np.sinc(phase*x/pi)))
    ricci_normal = w @ ((1+x**2)*np.cos(phase*x))
    area, volume = 4*pi*radius**2, 4*pi*radius**3/3

    # Wald curvature derivative and fixed-W displacement are computed separately.
    einstein_entropy = 4*pi*einstein * (-2*area*psi*(boundary-interior))
    ricci_wald = 4*pi*ricci*area*wave**2*psi*ricci_normal
    ricci_volume = 2*ricci*wave**2*psi*volume*interior/einstein
    volume_compensation = -8*pi*einstein*ricci_volume/radius
    ricci_entropy = ricci_wald + volume_compensation
    # Smooth-cone local completion: -2π D ∫ k^2. For the conformally
    # perturbed spatial sphere, δ∫ k^2 = (8/r)∫∂_n f with f=-Psi.
    delta_k_squared = 8/radius*area*psi*wave*(w @ (x*np.sin(phase*x)))
    cone_shift = -2*pi*ricci*delta_k_squared
    shifted_volume = ricci_volume + radius*cone_shift/(8*pi*einstein)
    cone_entropy = ricci_wald + cone_shift - 8*pi*einstein*shifted_volume/radius
    np.testing.assert_allclose(cone_entropy, ricci_entropy, atol=1e-13, rtol=0)
    # With the Euler term completed topologically, the equivalent Weyl
    # representative has zero delta W when delta R = 0.
    electric_amplitude = -1.5*psi*wave**2
    weyl_entropy = -16*pi*(ricci/2)*area*electric_amplitude * (
        w @ ((x**2 - 1/3)*np.cos(phase*x)))
    np.testing.assert_allclose(ricci_entropy, weyl_entropy, atol=1e-13, rtol=1e-9)
    # The vacuum CFT ball modular kernel is fixed before solving for the metric.
    modular_weight = 4*pi*radius**4/2 * (w @ (x**2*(1-x**2)*np.sinc(phase*x/pi)))
    modular = 2*pi*modular_weight*density
    ricci_modular = 2*pi*modular_weight*(4*ricci*psi*wave**4)
    np.testing.assert_allclose(ricci_entropy + ricci_modular, 0, rtol=0, atol=1e-13)
    residual = einstein_entropy + ricci_entropy + modular
    np.testing.assert_allclose(residual, 0, rtol=0, atol=1e-13)
    return np.array([ricci_entropy, modular, residual])/radius**4


def standing_wave_density(wave):
    """Improved-scalar cosine response, in units of inverse state-normalization volume."""
    # Subtract the vacuum-to-standing-wave mixtures with relative phases + and -.
    # Their canonical T00 cross terms cancel for opposite momenta of equal energy.
    # The remaining improved T00 is -Δ:phi^2:/6 with cosine amplitude 2/E.
    energy = wave/2
    return wave**2 * (2/energy) / 6


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    directory = parser.parse_args().checkpoint_dir
    a, b, d = curvature_coefficients(local_actions(directory))
    sigma = .015
    einstein, scalar, ricci = a/(2*sigma), b*log(2), d*log(2)
    print("Matched band coupling (Einstein, R^2, Ricci^2):", einstein, scalar, ricci)
    wave = .8
    density = standing_wave_density(wave)
    for radius in (.4, .2, .1, .05):
        boundary, modular, residual = ball_balance(einstein, ricci, radius, wave, density)
        print(f"r={radius:g}: fixed-W Ricci entropy/r^4={boundary:+.12g}; "
              f"total modular/r^4={modular:+.12g}; residual/r^4={residual:+.3g}")
    psi = density/(-4*einstein*wave**2 + 4*ricci*wave**4)
    prefactor = 8*pi**2/15
    r4 = prefactor * np.array([4*einstein*psi*wave**2, -4*ricci*psi*wave**4, density])
    np.testing.assert_allclose(r4.sum(), 0, rtol=0, atol=1e-13)
    print("Analytic r^4 coefficients [Einstein, fixed-W Ricci, modular]:", r4)


if __name__ == "__main__":
    main()
