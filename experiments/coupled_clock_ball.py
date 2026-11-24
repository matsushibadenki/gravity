"""Check linear GR-scalar constraints and the reduced clock modular response."""

from fractions import Fraction as F
from itertools import product
from math import isclose, pi, sin

import numpy as np

from clock_tensor_slab import oscillator_entropy


def constraints():
    mp2, hubble, epsilon_h = F(1), F(3, 10), F(3)
    scale_factor, wave_number_sq, zeta_dot = F(1), F(16, 25), F(-7, 100)
    lapse = zeta_dot / hubble
    shift = -scale_factor**2 * epsilon_h * zeta_dot / wave_number_sq
    delta_k = 3 * (zeta_dot - hubble * lapse) + wave_number_sq * shift / scale_factor**2
    density = -2 * mp2 * hubble**2 * epsilon_h * lapse
    assert zeta_dot - hubble * lapse == 0
    assert 4 * hubble * delta_k == 2 * density / mp2
    assert density != 0
    print(f"delta rho={density}, delta K={delta_k}; intrinsic curvature variation=0")
    return float(density), float(2 * mp2 * hubble * delta_k)


def modular_coefficient():
    # Positive Dirichlet box regulator, retaining a local oscillator algebra.
    size = 5
    spacing = 0.2
    coordinates = np.array(list(product(range(size), repeat=3)))
    distances = np.abs(coordinates[:, None, :] - coordinates[None, :, :]).sum(axis=-1)
    stiffness = (6 * np.eye(len(coordinates)) - (distances == 1)) / spacing**2
    values, modes = np.linalg.eigh(stiffness)
    assert min(values) > 0
    frequency = np.sqrt(values)
    mass = 6 * spacing**3  # 2*a_FLRW^3*M_pl^2*epsilon_H times the cell volume.
    x = (modes / (2 * mass * frequency)) @ modes.T
    p = (modes * (mass * frequency / 2)) @ modes.T
    center = (size - 1) / 2
    region = np.where(((coordinates - center)**2).sum(axis=1) <= 2)[0]
    x, p = (covariance[np.ix_(region, region)] for covariance in (x, p))
    spectrum, basis = np.linalg.eigh(x)
    root = (basis * np.sqrt(spectrum)) @ basis.T
    covariance_values, modes = np.linalg.eigh(root @ p @ root)
    nu = np.sqrt(covariance_values)
    assert min(nu) > 0.5
    modular_frequency = np.log1p(1 / (nu - 0.5))
    transform = root @ modes
    modular_pp = (transform * (modular_frequency / nu)) @ transform.T
    # A nonzero momentum displacement of the reduced scalar, with no spatial
    # metric displacement, leaves both the covariance and the cut identical.
    displacement = -0.07 * mass * np.cos(0.8 * spacing * (coordinates[region, 2] - center))
    coefficient = displacement @ modular_pp @ displacement / 2
    reference_entropy = oscillator_entropy(nu)
    assert coefficient > 0 and reference_entropy > 0
    for amplitude in (0.1, 0.01, 0.001):
        mean = amplitude * displacement
        raw_momentum = p + np.outer(mean, mean)
        entropy = oscillator_entropy(np.sqrt(np.linalg.eigvalsh(
            root @ (raw_momentum - np.outer(mean, mean)) @ root
        )))
        assert isclose(entropy, reference_entropy, abs_tol=1e-12)
        modular = mean @ modular_pp @ mean / 2
        assert isclose(modular / amplitude**2, coefficient)
        print(f"epsilon={amplitude:.3f}: modular change/epsilon={modular/amplitude:.8f}, "
              f"regional entropy={entropy:.8f}")


def ball_energy(density, extrinsic_density):
    sample_count = 20000
    for radius in (0.5, 0.25, 0.125, 0.0625):
        argument = 0.8 * radius
        average = 0.0
        for index in range(sample_count):
            x = (index + 0.5) / sample_count
            phase = argument * x
            average += x**2 * (1 - x**2) * sin(phase) / phase
        apparent = 4 * pi**2 * radius**4 * density * average / sample_count
        extrinsic = -4 * pi**2 * radius**4 * extrinsic_density * average / sample_count
        assert isclose(apparent + extrinsic, 0, abs_tol=1e-15)
        print(f"r={radius:.4f}: energy moment/r^4={apparent/radius**4:+.9f}, "
              f"extrinsic correction/r^4={extrinsic/radius**4:+.9f}")


if __name__ == "__main__":
    clock_density, extrinsic_density = constraints()
    modular_coefficient()
    ball_energy(clock_density, extrinsic_density)
