"""Check the fixed-volume sphere residual and static gravitational response."""

from math import cos, isclose, pi, sin


def main():
    gravitational_coupling, eta = 0.2, 1.25
    mixing, response, mass, shell_speed = 0.3, 0.4, 2.0, 0.8
    wave_number, density = 0.2, 0.01
    k2 = wave_number**2
    einstein_coefficient = 1 / (16 * pi * gravitational_coupling)
    denominator = mass**2 + shell_speed**2 * k2
    psi = -4 * pi * gravitational_coupling * density / k2
    shell = mixing * k2 * psi / denominator
    phi = psi * (1 + mixing**2 * k2 / (6 * einstein_coefficient * denominator))
    assert isclose(-k2 * psi, 4 * pi * gravitational_coupling * density)
    assert isclose(
        4 * einstein_coefficient * (-k2) * (phi - psi),
        mixing * (-k2) * (2 / 3) * shell,
    )

    print(f"G_eta={1 / (4 * eta):.8f}, G_Psi={-k2 * psi / (4 * pi * density):.8f}")
    print(f"G_Phi(k={wave_number:g})={-k2 * phi / (4 * pi * density):.8f}")
    count = 10000
    for radius in (0.5, 0.25, 0.125):
        x = wave_number * radius
        integral = 0
        for index in range(count):
            mu = -1 + 2 * (index + 0.5) / count
            # Subtract the analytically vanishing constant angular term.
            integral += (mu**2 - 1 / 3) * (-2 * sin(x * mu / 2)**2)
        residual = 4 * pi * radius**2 * response * shell * integral / count
        leading = 32 * pi**2 * response * mixing * gravitational_coupling * k2 * density * radius**4 / (45 * denominator)
        assert residual > 0 and isclose(residual, leading, rel_tol=1e-3)

        # Exact first-order area at fixed physical volume in the conformal metric.
        delta_area = 8 * pi * psi * radius**2 * (3 * (sin(x) - x * cos(x)) / x**3 - sin(x) / x)
        leading_area = -32 * pi**2 * gravitational_coupling * density * radius**4 / 15
        assert isclose(delta_area, leading_area, rel_tol=1e-3)
        print(f"r={radius:.3f}  residual/r^4={residual/radius**4:.10f}  area_shift/r^4={delta_area/radius**4:.10f}")


if __name__ == "__main__":
    main()
