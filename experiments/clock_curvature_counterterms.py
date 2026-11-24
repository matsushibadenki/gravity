"""Check local curvature-squared entropy on the moving scalar-clock slice."""

from fractions import Fraction as F
from math import isclose, pi

from proper_distance_collar import AREA_COEFFICIENT, LOG_COEFFICIENT, profile_terms


def curvature_check():
    hubble = F(3, 10)
    hessians = (
        [[F(3), F(-2), F(0)], [F(-2), F(1), F(4)], [F(0), F(4), F(2)]],
        [[F(-2), F(0), F(0)], [F(0), F(-2), F(0)], [F(0), F(0), F(-2)]],
    )
    for hessian in hessians:
        laplacian = sum(hessian[i][i] for i in range(3))
        trace_free = [[value - (laplacian / 3 if i == j else 0)
                       for j, value in enumerate(row)] for i, row in enumerate(hessian)]
        spatial_ricci = [[-value for value in row] for row in trace_free]
        shear = [[value / hubble for value in row] for row in trace_free]
        electric_weyl = [[spatial_ricci[i][j] + hubble * shear[i][j]
                          for j in range(3)] for i in range(3)]
        assert all(value == 0 for row in electric_weyl for value in row)
        assert -4 * laplacian + 4 * hubble * (laplacian / hubble) == 0
    print("Nonzero intrinsic curvature and shear: zero electric Weyl perturbation.")


def response_check():
    wave_number, eta = 0.8, 2 * pi
    cases = (
        ("single", ((1, 1),), -wave_number**2 / 6, wave_number**4 / 120),
        ("quartic-free", ((1, 1), (-1 / 16, 2)), -wave_number**2 / 8, 0),
    )
    for label, modes, quadratic, quartic in cases:
        predicted = 16 * pi * eta * quadratic / 5 + 4 * LOG_COEFFICIENT * quartic / 7
        radius_squared = (-AREA_COEFFICIENT / 3 + 2 * LOG_COEFFICIENT / 5) * quadratic
        error = float("inf")
        for radius in (0.4, 0.2, 0.1, 0.05):
            terms = [(power, weight * value)
                     for weight, factor in modes
                     for power, value in profile_terms(radius, factor * wave_number)]
            mean_difference = sum(power * value / (power + 3) for power, value in terms)
            power_collar = AREA_COEFFICIENT / 12 * sum(
                power * (power - 4) * value for power, value in terms
            )
            entropy_variation = (eta * 8 * pi * radius**2 + LOG_COEFFICIENT) * mean_difference + power_collar
            coefficient = (entropy_variation - radius_squared * radius**2) / radius**4
            next_error = abs(predicted - coefficient)
            assert next_error < error
            error = next_error
        assert isclose(coefficient, predicted, rel_tol=0.001)
        print(f"{label}: finite r^4 coefficient={coefficient:+.9f}; prediction={predicted:+.9f}")


if __name__ == "__main__":
    curvature_check()
    response_check()
