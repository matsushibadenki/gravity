"""Distinguish clock stress from a coherent-reference modular response."""

from fractions import Fraction as F
from math import isclose, log, sqrt

from relative_clock_entropy import mode_entropy


def gaussian_check():
    # Two coupled oscillators, so the clock's regional state is mixed.
    frequencies = (sqrt(3), sqrt(7))
    position = sum(1 / value for value in frequencies) / 4
    momentum = sum(frequencies) / 4
    nu = sqrt(position * momentum)
    entropy = mode_entropy(nu)
    modular_frequency = log((nu + 0.5) / (nu - 0.5))
    reference_momentum = 0.7
    for step in (0.1, 0.01, 0.001):
        displaced = reference_momentum + step
        raw_second_moment = momentum + displaced**2
        centered = raw_second_moment - displaced**2
        assert isclose(mode_entropy(sqrt(position * centered)), entropy, abs_tol=1e-14)
        physical_change = (displaced**2 - reference_momentum**2) / 2
        modular_change = modular_frequency * nu * step**2 / (2 * momentum)
        assert isclose(physical_change / step - step / 2, reference_momentum)
        assert isclose(modular_change / step**2, modular_frequency * nu / (2 * momentum))
        print(f"epsilon={step:.3f}: energy change/epsilon={physical_change/step:.6f}, "
              f"modular change/epsilon={modular_change/step:.6f}, entropy={entropy:.9f}")


def observer_check():
    # Linear stress of a coherent momentum displacement: delta T = diag(s,s,s,s).
    aligned = F(7, 10)
    gamma, gamma_velocity = F(5, 4), F(3, 4)
    assert gamma**2 - gamma_velocity**2 == 1
    tilted = aligned * (gamma**2 + gamma_velocity**2)
    assert tilted / aligned == F(17, 8)
    print(f"Tilted scalar-clock energy variation factor: {tilted/aligned}.")


if __name__ == "__main__":
    gaussian_check()
    observer_check()
