"""Compare complex-momentum branch points with distant-slab information."""

from cmath import asin, sqrt as complex_sqrt
from math import log, sqrt

import numpy as np
from numpy.polynomial import Polynomial

from clock_tensor_slab import covariance_symbols, tensor_basis
from infinite_slab_information import density
from transverse_slab_integral import focused_rule


def branch_scales(spacing, mixing, transverse=(0.0, 0.0)):
    u = Polynomial([0, 1])
    laplacian = 4 * u / spacing**2
    derivative_squared = laplacian * (1 - u) * (1 + 2 * u / 3)**2
    angles = np.asarray(transverse)
    total_laplacian = laplacian + np.sum(4 * np.sin(angles / 2)**2) / spacing**2
    total_derivative = derivative_squared + np.sum((np.sin(angles) * (4 - np.cos(angles)) / 3)**2) / spacing**2
    determinant = (1 + total_laplacian) * (4 + total_laplacian) - mixing**2 * total_derivative**2
    momenta = [2 * asin(complex_sqrt(complex(root))) / spacing for root in determinant.roots()]
    mixed = min(abs(momentum.imag) for momentum in momenta)
    transverse_laplacian = np.sum(4 * np.sin(angles / 2)**2) / spacing**2
    spectator = 2 * np.arcsinh(spacing * sqrt(1 + transverse_laplacian) / 2) / spacing
    return mixed, spectator


def covariance_check(spacing, mixing, kappa):
    angles = np.linspace(0, np.pi, 17)
    assert all(min(branch_scales(spacing, mixing, (y, z))) >= kappa - 1e-9
               for y in angles for z in angles)
    (normal, _), (weights, _) = focused_rule(240)
    position, _ = covariance_symbols(
        (len(normal), 1, 1), spacing, 2, mixing * sqrt(3 / 2), "improved",
        normal_angles=normal,
    )
    direction = sqrt(3 / 2) * tensor_basis()[:, 0, 0]
    longitudinal = np.einsum("i,kij,j->k", direction, position[:, 0, 0, :5, :5], direction)
    sites = np.arange(20, 81, 10)
    values = np.cos(sites[:, None] * normal) @ (weights * longitudinal)
    distances = sites * spacing
    corrected = values * np.sqrt(distances) * np.exp(kappa * distances)
    assert np.all(values > 0)
    print("Scaled zero-transverse-momentum covariance:",
          list(zip(distances, corrected)), flush=True)


def main():
    spacing, mixing = 0.15, 0.45
    kappa, spectator = branch_scales(spacing, mixing)
    assert 0 < kappa < spectator
    covariance_check(spacing, mixing, kappa)
    continuum = sqrt(8 / (5 + sqrt(9 + 16 * mixing**2)))
    print(f"continuum kappa={continuum:.8f}; lattice kappa={kappa:.8f}; "
          f"spectator kappa={spectator:.8f}; predicted rate={2*kappa:.8f}", flush=True)
    gaps = np.arange(4, 11) * 0.6
    results = []
    for normal, transverse in ((176, 40), (240, 56)):
        values = density(spacing, 0.6, gaps, normal, transverse, mixing * sqrt(3 / 2))
        assert np.all(values > 0) and np.all(np.diff(values, axis=0) < 0)
        results.append(values)
        print(f"quadrature=({normal},{transverse},{transverse})", flush=True)
        for distance, (shell, joint) in zip(gaps, values):
            print(f"  d={distance:.1f}: shell={shell:.11e}, joint={joint:.11e}", flush=True)
    refined = results[-1]
    change = np.max(np.abs(results[0] / refined - 1))
    print(f"maximum refinement change={change:.4%}", flush=True)
    assert change < 0.05
    for sector, label in enumerate(("shell", "joint")):
        raw = [log(a / b) / 0.6 for a, b in zip(refined[:-1, sector], refined[1:, sector])]
        corrected = [slope - 2 * log(right / left) / 0.6
                     for slope, left, right in zip(raw, gaps, gaps[1:])]
        print(f"{label} raw: {np.round(raw, 4)}", flush=True)
        print(f"{label} power-corrected: {np.round(corrected, 4)}", flush=True)


if __name__ == "__main__":
    main()
