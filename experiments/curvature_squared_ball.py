"""Check the R-squared entropy at fixed volume and generalized volume."""

from math import cos, isclose, pi, sin


def ball_mean_cosine(argument):
    return 3 * (sin(argument) - argument * cos(argument)) / argument**3


def main():
    area_coefficient, curvature_coefficient = 0.3, 0.07
    profile, wave_number = 0.15, 0.8
    previous_error = float("inf")
    for radius in (0.6, 0.3, 0.15, 0.075):
        area = 4 * pi * radius**2
        volume = area * radius / 3
        constant_entropy = 8 * pi * curvature_coefficient * area * profile
        volume_compensation = (
            4 * pi * area_coefficient * 2 / radius
            * 3 * curvature_coefficient / area_coefficient * volume * profile
        )
        assert isclose(constant_entropy, volume_compensation, rel_tol=1e-14)

        argument = wave_number * radius
        surface = area * profile * sin(argument) / argument
        interior = volume * profile * ball_mean_cosine(argument)
        residual = 8 * pi * curvature_coefficient * (surface - 3 * interior / radius)
        expected = -32 * pi**2 * curvature_coefficient * wave_number**2 * profile / 15
        error = abs(residual / radius**4 / expected - 1)
        assert error < previous_error
        previous_error = error

        # Independent modular integral of the R-squared term in the lapse equation.
        samples = 10000
        average = 0.0
        for index in range(samples):
            x = (index + 0.5) / samples
            phase = argument * x
            average += x**2 * (1 - x**2) * sin(phase) / phase
        modular = (16 * pi**2 * curvature_coefficient * wave_number**2
                   * profile * radius**4 * average / samples)
        assert isclose(modular, -residual, rel_tol=1e-7)
        print(f"r={radius:.3f}: fixed-volume term/r^2={constant_entropy/radius**2:.8f}, "
              f"fixed-generalized-volume term/r^4={residual/radius**4:+.8f}")
    assert previous_error < 0.001


if __name__ == "__main__":
    main()
