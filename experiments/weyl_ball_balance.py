"""Check the Weyl entropy and its modular balance on a round reference ball."""

from math import cos, isclose, pi, sin


def main():
    # Taylor-compatible profiles: E_ij=e*(z_i*z_j-I_ij/3)*cos(kz)
    # and, in the separate mixed test, delta R = q*(cos(kz)-1).
    weyl_coefficient, scalar_coefficient = 0.05, 0.07
    electric_amplitude, scalar_amplitude, wave_number = 0.15, 0.2, 0.8
    samples = 20000
    nodes = [(index + 0.5) / samples for index in range(samples)]
    previous_weyl_error = float("inf")
    for radius in (0.6, 0.3, 0.15, 0.075):
        phase = wave_number * radius
        area, volume = 4 * pi * radius**2, 4 * pi * radius**3 / 3
        electric_boundary = area * electric_amplitude * sum(
            (mu**2 - 1 / 3) * (-2 * sin(phase * mu / 2)**2) for mu in nodes
        ) / samples
        modular_weight = 2 * pi * radius**4 * sum(
            x**2 * (1 - x**2) * sin(phase * x) / (phase * x) for x in nodes
        ) / samples
        weyl_entropy = -16 * pi * weyl_coefficient * electric_boundary
        weyl_matter = (2 * pi * 8 * weyl_coefficient
                       * (-2 / 3) * electric_amplitude * wave_number**2 * modular_weight)
        assert isclose(weyl_entropy, -weyl_matter, rel_tol=1e-7)
        wave_laplacian = -2 * electric_amplitude * wave_number**2 / 3
        analytic = -64 * pi**2 * weyl_coefficient * wave_laplacian / 15
        error = abs(weyl_entropy / radius**4 / analytic - 1)
        assert error < previous_weyl_error
        previous_weyl_error = error

        scalar_surface = area * scalar_amplitude * (sin(phase) / phase - 1)
        scalar_integral = volume * 3 * scalar_amplitude * sum(
            x**2 * (sin(phase * x) / (phase * x) - 1) for x in nodes
        ) / samples
        scalar_matter = 2 * pi * 4 * scalar_coefficient * scalar_amplitude * wave_number**2 * modular_weight
        fixed_volume = weyl_entropy + weyl_matter + 8 * pi * scalar_coefficient * scalar_surface + scalar_matter
        compensation = 24 * pi * scalar_coefficient * scalar_integral / radius
        assert isclose(fixed_volume, compensation, rel_tol=1e-7)
        print(f"r={radius:.3f}: Weyl entropy/r^4={weyl_entropy/radius**4:+.9f}, "
              f"mixed fixed V/r^4={fixed_volume/radius**4:+.9f}, "
              f"mixed fixed W/r^4={(fixed_volume-compensation)/radius**4:+.3e}")
    assert previous_weyl_error < 0.001


if __name__ == "__main__":
    main()
