"""Check the analytic collar response of the reduced scalar reference vacuum."""

from math import factorial, isclose, pi


AREA_COEFFICIENT = 4 * pi * 0.0055351600
LOG_COEFFICIENT = -1 / 90


def profile_terms(radius, wave_number):
    for order in range(1, 11):
        power = 2 * order
        value = (-1)**order * (wave_number * radius)**power / factorial(power + 1)
        yield power, value


def profile(radius, wave_number):
    return sum(value for _, value in profile_terms(radius, wave_number))


def response(radius, wave_number):
    terms = list(profile_terms(radius, wave_number))
    bulk_mean = sum(3 * value / (power + 3) for power, value in terms)
    geometric_scale = profile(radius, wave_number) - bulk_mean
    collar_term = AREA_COEFFICIENT / 12 * sum(
        power * (power - 4) * value for power, value in terms
    )
    logarithmic = LOG_COEFFICIENT * geometric_scale
    return -radius * bulk_mean, geometric_scale, collar_term + logarithmic


def integrate_profile(radius, offset, wave_number, samples=256):
    step = offset / samples
    return step * sum(profile(radius + (index + 0.5) * step, wave_number)
                      for index in range(samples))


def collar_check():
    radius, wave_number = 0.6, 0.8
    center_shift, geometric_scale, finite = response(radius, wave_number)
    errors = []
    for thickness in (0.12, 0.06, 0.03, 0.015):
        inner = center_shift - integrate_profile(radius, -thickness / 2, wave_number)
        outer = center_shift - integrate_profile(radius, thickness / 2, wave_number)
        log_change = (outer + inner) / (2 * radius) - (outer - inner) / thickness
        unsubtracted = (2 * AREA_COEFFICIENT * (radius / thickness)**2 + LOG_COEFFICIENT) * log_change
        area_subtraction = 2 * AREA_COEFFICIENT * (radius / thickness)**2 * geometric_scale
        remainder = unsubtracted - area_subtraction
        errors.append(abs(remainder - finite))
        print(f"collar={thickness:.3f}: area-subtracted first variation={remainder:+.10f}")
    assert all(right < left for left, right in zip(errors, errors[1:]))
    assert isclose(remainder, finite, rel_tol=0.001)


def small_ball_check():
    wave_number, planck_mass_squared = 0.8, 1.0
    radius_squared_coefficient = wave_number**2 * (AREA_COEFFICIENT / 18 + 1 / 1350)
    expected = -16 * pi**2 * planck_mass_squared * wave_number**2 / 15 - wave_number**4 / 18900
    for radius in (0.4, 0.2, 0.1, 0.05):
        _, geometric_scale, vacuum = response(radius, wave_number)
        einstein = 2 * pi * planck_mass_squared * 8 * pi * radius**2 * geometric_scale
        r4 = (einstein + vacuum - radius_squared_coefficient * radius**2) / radius**4
        print(f"r={radius:.2f}: residual r^4 coefficient={r4:+.9f}")
    assert isclose(r4, expected, rel_tol=0.001)


if __name__ == "__main__":
    collar_check()
    small_ball_check()
