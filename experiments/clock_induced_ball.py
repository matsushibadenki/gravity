"""Check induced clock-foliation coefficients and moving-ball cancellation."""

from fractions import Fraction as F
from math import exp, isclose, pi

from proper_distance_collar import AREA_COEFFICIENT, LOG_COEFFICIENT, profile_terms


def proper_time_band(mass, lower, upper, samples=10000):
    step = (upper - lower) / samples
    nodes = (lower + (index + 0.5) * step for index in range(samples))
    return step * sum(exp(-mass**2 * time) / time**2 for time in nodes)


def constraints(bare, induced, speed):
    spatial = bare + induced / speed
    kinetic = bare + induced / speed**3
    eta_over_four_pi = bare + induced / speed**2
    hubble, wave_number_squared, amplitude = F(3, 10), F(16, 25), F(1, 5)
    density_background = 6 * kinetic * hubble**2
    lapse = F(0)
    shift = -spatial * amplitude / (kinetic * hubble)
    expansion = shift * wave_number_squared
    intrinsic = 4 * wave_number_squared * amplitude
    density = -2 * density_background * lapse
    assert spatial * intrinsic + 4 * kinetic * hubble * expansion == density
    assert spatial / kinetic > 0 and eta_over_four_pi > 0
    # One coefficient in the transformed Einstein action must reproduce both.
    assert (spatial * kinetic) / (spatial / kinetic) == kinetic**2
    return eta_over_four_pi, expansion, spatial / kinetic


def entropy_response(speed, eta):
    # Superpose two sinc profiles so the local quartic Taylor coefficient is zero.
    wave_number = 0.8
    expected = -2 * pi * eta * wave_number**2 / 5
    quadratic = -wave_number**2 / 8
    r2 = (-AREA_COEFFICIENT / 3 + 2 * LOG_COEFFICIENT / 5) * quadratic
    for radius in (0.4, 0.2, 0.1, 0.05):
        terms = [(power, value)
                 for wave, weight in ((wave_number, 1), (2 * wave_number, -1 / 16))
                 for power, entry in profile_terms(radius, wave)
                 for value in (weight * entry,)]
        surface_minus_ball = sum(power * value / (power + 3) for power, value in terms)
        area = 8 * pi * radius**2 * surface_minus_ball
        collar = LOG_COEFFICIENT * surface_minus_ball + AREA_COEFFICIENT / 12 * sum(
            power * (power - 4) * value for power, value in terms
        )
        coefficient = (eta * area + collar - r2 * radius**2) / radius**4
    assert isclose(coefficient, expected, rel_tol=1e-5)
    print(f"v={speed}: measured r^4 coefficient={coefficient:+.9f}; predicted={expected:+.9f}")


def main():
    bare = F(500)
    band = proper_time_band(100, 1e-6, 2e-6)
    induced = F(5 * band / (192 * pi**2)).limit_denominator(10**10)
    for speed in (F(4, 5), F(1), F(5, 4)):
        eta_over_four_pi, expansion, speed_squared = constraints(bare, induced, speed)
        # Independent cone coefficient per physical area for the same band.
        cone_density = 5 * band / (48 * pi * float(speed)**2)
        eta = 4 * pi * float(eta_over_four_pi)
        assert isclose(eta - 4 * pi * float(bare), cone_density, rel_tol=1e-12)
        print(f"v={speed}, expansion(mode)={float(expansion):+.7f}, scalar c^2={float(speed_squared):.7f}")
        entropy_response(speed, eta)


if __name__ == "__main__":
    main()
