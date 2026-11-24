"""Match the projected bundle connection and audit the reduced clock sources."""

from math import pi

import numpy as np

from projected_connection_entropy import connection_generator
from reduced_clock_ball_seam import spectral_operators


def constraint_rank(size, length):
    sites, gradients, laplacian, inverse = spectral_operators(size, length / size)
    hubble = 0.3
    columns = []
    for direction in ((0, 0, 1), (0, 1, 1)):
        profile = np.cos(2 * pi * (sites @ direction) / size)
        for velocity in (np.zeros_like(profile), profile, laplacian @ profile / (3 * hubble)):
            lapse = velocity / hubble
            shift = -profile / hubble + 3 * inverse @ velocity
            expansion = -sum(gradient @ (gradient @ shift) for gradient in gradients)
            columns.append(np.column_stack((-4 * laplacian @ profile, 4 * hubble * expansion,
                                            12 * hubble**2 * lapse)))
    design = np.concatenate(columns)
    assert np.linalg.matrix_rank(design, tol=1e-9) == 2
    assert np.max(np.abs(design.sum(axis=1))) < 1e-10
    r, k, clock = design.T
    quadratic = np.column_stack((r*r, r*k, r*clock, k*k, k*clock, clock*clock))
    assert np.linalg.matrix_rank(quadratic, tol=1e-8) == 3
    print(f"Clock N={size}: linear rank 2/3, quadratic rank 3/6")


def connection_coefficients(size, length, cutoff, mass=2):
    """Return coefficients of tr(Omega_ab Omega_ab), including both ab orders."""
    wave = 2 * pi * np.fft.fftfreq(size, length / size)
    square = wave**2
    momentum = 2 * pi / length
    nodes, weights = np.polynomial.legendre.leggauss(24)
    times = cutoff * (3 + nodes) / 2
    fractions = (1 + nodes) / 2
    heat = np.exp(-times[:, None] * square)
    flat = heat.sum(axis=1) / length
    moment = (heat @ square) / length
    time_heat = np.exp(-times * mass**2) / np.sqrt(4 * pi * times)
    # Temporal probe at zero frequency slope; spatial probe at the box fundamental.
    temporal = -(cutoff / 24) * (weights @ (times**2 * time_heat * moment * flat**2))
    shifted = square[None, :] + fractions[:, None] * (np.roll(square, -1) - square)
    spatial_heat = (np.exp(-times[:, None, None] * shifted) @ np.ones(size)) @ (weights / 2)
    spatial_deficit = flat - spatial_heat / length
    spatial = -(cutoff / 4) * (weights @ (times * time_heat * moment * flat * spatial_deficit)) / momentum**2
    return temporal, spatial


def main():
    for size in (3, 5, 7):
        constraint_rank(size, 1.8)

    rotation = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    generator = connection_generator(rotation)
    assert np.allclose(generator.T, -generator)
    assert np.isclose(np.trace(generator @ generator), -10)

    target = -np.log(2) / (384 * pi**2)
    for cutoff in (0.02, 0.005, 0.00125):
        for size in (25, 49, 97):
            temporal, spatial = connection_coefficients(size, 1.8, cutoff)
            print(f"s={cutoff:g} N={size}: temporal={temporal:+.9e} spatial={spatial:+.9e}")
    assert np.isclose(temporal, target, rtol=0.01)
    assert np.isclose(spatial, temporal, rtol=0.01)


if __name__ == "__main__":
    main()
