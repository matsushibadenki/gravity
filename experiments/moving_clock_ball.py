"""Check the displacement and intrinsic area of a moving clock-aligned ball."""

from math import cos, exp, isclose, pi, sin


def profile(radius, wave_number):
    argument = radius * wave_number
    return sin(argument) / argument - 1 if argument else 0.0


def volume(coordinate_radius, amplitude, wave_number, samples=2048):
    step = coordinate_radius / samples
    curved_minus_flat = sum(
        radius**2 * (exp(3 * amplitude * profile(radius, wave_number)) - 1)
        for index in range(samples)
        for radius in ((index + 0.5) * step,)
    )
    return 4 * pi * (coordinate_radius**3 / 3 + step * curved_minus_flat)


def tracked_ball(radius, amplitude, wave_number):
    target = 4 * pi * radius**3 / 3
    lower, upper = radius * 0.99, radius * 1.01
    for _ in range(45):
        candidate = (lower + upper) / 2
        if volume(candidate, amplitude, wave_number) < target:
            lower = candidate
        else:
            upper = candidate
    coordinate_radius = (lower + upper) / 2
    area = 4 * pi * coordinate_radius**2 * exp(2 * amplitude * profile(coordinate_radius, wave_number))
    return coordinate_radius, area


def main():
    wave_number, hubble, mp_squared = 0.8, 0.3, 1.0
    center_laplacian = -wave_number**2
    center_curvature = -4 * center_laplacian
    center_expansion = center_laplacian / hubble
    assert isclose(center_curvature + 4 * hubble * center_expansion, 0, abs_tol=1e-14)
    area_limit = -8 * pi * wave_number**2 / 15
    amplitude = 1e-3
    previous_error = float("inf")
    for radius in (0.5, 0.25, 0.125, 0.0625):
        plus = tracked_ball(radius, amplitude, wave_number)
        minus = tracked_ball(radius, -amplitude, wave_number)
        moving_radius, area_change = ((left - right) / (2 * amplitude)
                                      for left, right in zip(plus, minus))
        argument = wave_number * radius
        surface_mean = profile(radius, wave_number)
        volume_mean = 3 * (sin(argument) - argument * cos(argument)) / argument**3 - 1
        assert isclose(moving_radius, -radius * volume_mean, rel_tol=1e-5)
        assert isclose(area_change, 8 * pi * radius**2 * (surface_mean - volume_mean), rel_tol=1e-5)
        error = abs(area_change / radius**4 - area_limit)
        assert error < previous_error
        previous_error = error

        # This is the expansion contribution to the intrinsic area identity.
        count = 12000
        weighted = sum(
            x**2 * (1 - x**2) * (profile(radius * x, wave_number) + 1)
            for index in range(count)
            for x in ((index + 0.5) / count,)
        )
        expansion_energy = 2 * mp_squared * center_laplacian * 4 * pi**2 * radius**4 * weighted / count
        area_entropy = 2 * pi * mp_squared * area_change
        assert isclose(area_entropy, expansion_energy, rel_tol=1e-5)
        print(f"r={radius:.4f}: coordinate shift/r^3={moving_radius/radius**3:+.8f}, "
              f"area shift/r^4={area_change/radius**4:+.8f}")
    assert previous_error < 0.001


if __name__ == "__main__":
    main()
