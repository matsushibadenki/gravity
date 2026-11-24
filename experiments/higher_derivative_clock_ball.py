"""Check the order-reduced four-derivative constraints and ball entropy."""

from fractions import Fraction as F
from math import exp, isclose, pi

from proper_distance_collar import AREA_COEFFICIENT, LOG_COEFFICIENT, profile_terms


def heat_integral(mass, lower, upper, power, count=12000):
    step = (upper - lower) / count
    times = (lower + (index + 0.5) * step for index in range(count))
    return step * sum(exp(-mass**2 * time) / time**power for time in times)


def constraints(einstein, curvature, weyl):
    # Evaluate independent constraint terms as functions of the profile's Laplacian.
    hubble, laplacian = F(3, 10), F(-16, 25)
    background_r = -6 * hubble**2
    background_r_dot = -6 * hubble * background_r
    expansion0 = laplacian / hubble
    scalar_normal_derivative = -2 * background_r * expansion0
    rr_nn = 2 * expansion0 * background_r_dot + 6 * hubble * scalar_normal_derivative
    rr_ni = -2 * scalar_normal_derivative  # Strip off the spatial gradient.
    weyl_ni = -8 * hubble * laplacian
    assert rr_nn == -24 * background_r * laplacian

    lapse = (12 * curvature + 4 * weyl) * laplacian / einstein
    shift_laplacian = -laplacian / hubble * (1 + 12 * curvature * background_r / einstein)
    expansion = -3 * hubble * lapse - shift_laplacian
    density = -12 * einstein * hubble**2 * lapse
    momentum_residual = 4 * einstein * hubble * lapse + 2 * curvature * rr_ni + 2 * weyl * weyl_ni
    lapse_residual = -4 * einstein * laplacian + 4 * einstein * hubble * expansion + 2 * curvature * rr_nn - density
    assert momentum_residual == 0
    assert lapse_residual == 0
    assert lapse != 0 and density != 0
    print(f"corrected lapse={float(lapse):+.8e}; clock density={float(density):+.8e}")
    print(f"corrected expansion={float(expansion):+.9f}; both constraints have zero residual")
    return background_r


def ball_entropy(eta):
    wave_number = 0.8
    quadratic = -wave_number**2 / 8
    expected = -2 * pi * eta * wave_number**2 / 5
    leading = (-AREA_COEFFICIENT / 3 + 2 * LOG_COEFFICIENT / 5) * quadratic
    for radius in (0.4, 0.2, 0.1, 0.05):
        terms = list(profile_terms(radius, wave_number))
        terms.extend((power, -value / 16) for power, value in profile_terms(radius, 2 * wave_number))
        surface_minus_ball = sum(power * value / (power + 3) for power, value in terms)
        area = 8 * pi * radius**2 * surface_minus_ball
        collar = LOG_COEFFICIENT * surface_minus_ball + AREA_COEFFICIENT / 12 * sum(
            power * (power - 4) * value for power, value in terms
        )
        coefficient = (eta * area + collar - leading * radius**2) / radius**4
        print(f"r={radius:.2f}: retained response/r^4={coefficient:+.8f}")
    assert isclose(coefficient, expected, rel_tol=1e-5)
    return coefficient


def main():
    mass, lower, upper = 100, 1e-6, 2e-6
    i1 = heat_integral(mass, lower, upper, 2)
    i2 = heat_integral(mass, lower, upper, 1)
    induced = 5 * i1 / (192 * pi**2)
    einstein = F(500 + induced).limit_denominator(10**10)
    curvature = F(5 * i2 / (2304 * pi**2)).limit_denominator(10**10)
    weyl = F(5 * i2 / (3840 * pi**2)).limit_denominator(10**10)
    background_r = constraints(einstein, curvature, weyl)
    eta = 4 * pi * float(einstein + 2 * curvature * background_r)
    assert eta > 0
    coefficient = ball_entropy(eta)
    assert coefficient < 0
    print(f"shared band: induced Einstein={induced:.8f}, B_R={float(curvature):.8e}, "
          f"B_C={float(weyl):.8e}")


if __name__ == "__main__":
    main()
