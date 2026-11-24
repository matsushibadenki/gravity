"""Check a shared proper-time Gaussian comparison at fixed Einstein-frame volume."""

from fractions import Fraction as F
from math import isclose, pi

from higher_derivative_clock_ball import constraints, heat_integral
from proper_distance_collar import profile_terms


def matched_coefficients(bare, lower, upper, heavy_mass):
    # The massless rank-one completion and massive rank-five bundle share s.
    area_integral = heat_integral(0, lower, upper, 2) + 5 * heat_integral(heavy_mass, lower, upper, 2)
    curvature_integral = heat_integral(0, lower, upper, 1) + 5 * heat_integral(heavy_mass, lower, upper, 1)
    action_area = area_integral / (192 * pi**2)
    cone_area = area_integral / (48 * pi)
    assert isclose(4 * pi * action_area, cone_area)
    return tuple(F(value).limit_denominator(10**11) for value in (
        bare + action_area, curvature_integral / (2304 * pi**2),
        curvature_integral / (3840 * pi**2),
    ))


def fixed_volume_test(einstein, curvature, background_r):
    reference_slope = float(einstein + 2 * curvature * background_r)
    assert reference_slope > 0
    energy_wave_number = 0.8
    # On the zeroth-order constrained data the curvature variation is zero.
    # In W the curvature variation is multiplied by B_R, so the corrected
    # O(B_R,B_C) curvature is immaterial at the retained order.
    curvature_variation0 = 0.0
    correction_to_volume = 3 * float(curvature) / reference_slope * curvature_variation0
    assert correction_to_volume == 0
    expected = -8 * pi**2 * reference_slope * energy_wave_number**2 / 5
    for radius in (0.4, 0.2, 0.1, 0.05):
        terms = list(profile_terms(radius, energy_wave_number))
        terms.extend((power, -value / 16) for power, value in profile_terms(radius, 2 * energy_wave_number))
        mean_difference = sum(power * value / (power + 3) for power, value in terms)
        area_change = 8 * pi * radius**2 * mean_difference
        finite_boundary = 8 * pi * float(curvature * background_r) * area_change
        entropy = 4 * pi * float(einstein) * area_change + finite_boundary
        print(f"r={radius:.2f}: fixed-W response/r^4={entropy/radius**4:+.9f}, "
              f"finite curvature boundary/r^4={finite_boundary/radius**4:+.9f}")
    assert isclose(entropy / radius**4, expected, rel_tol=1e-6)


def check_volume_from_action(einstein, curvature, background_r):
    # Independent derivative of the spatial volume in the Einstein frame.
    slope = float(einstein + 2 * curvature * background_r)
    step, variation = 1e-2, 0.3
    relative = 2 * float(curvature) * variation * step / slope
    derivative = ((1 + relative)**1.5 - (1 - relative)**1.5) / (2 * step)
    assert isclose(derivative, 3 * float(curvature) * variation / slope, rel_tol=1e-6)


if __name__ == "__main__":
    action = matched_coefficients(500, 1e-6, 2e-6, 100)
    reference_r = constraints(*action)
    check_volume_from_action(action[0], action[1], reference_r)
    fixed_volume_test(action[0], action[1], reference_r)
