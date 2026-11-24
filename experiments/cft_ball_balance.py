"""Compare the CFT modular integral with fixed-volume area and shell entropy."""

from math import cos, isclose, pi, sin


def main():
    coupling = 0.2
    wave_number = 0.8
    density = 0.01
    mass, shell_speed, mixing, response = 2.0, 0.8, 0.3, 0.4
    k2 = wave_number**2
    potential = -4 * pi * coupling * density / k2
    shell = mixing * k2 * potential / (mass**2 + shell_speed**2 * k2)
    count = 20000

    for eta in (1 / (4 * coupling), 1.1 / (4 * coupling)):
        for radius in (0.5, 0.25, 0.125):
            x = wave_number * radius
            area = 8 * pi * potential * radius**2 * (
                3 * (sin(x) - x * cos(x)) / x**3 - sin(x) / x
            )
            modular_integral = 0.0
            shell_integral = 0.0
            for index in range(count):
                unit = (index + 0.5) / count
                argument = x * unit
                modular_integral += unit**2 * (1 - unit**2) * sin(argument) / argument
                shell_integral += (unit**2 - 1 / 3) * (-2 * sin(argument / 2)**2)
            matter = 4 * pi**2 * density * radius**4 * modular_integral / count
            residual = 4 * pi * radius**2 * response * shell * shell_integral / count
            total = eta * area + matter + residual
            predicted = (eta - 1 / (4 * coupling)) * area + residual
            assert isclose(matter, -area / (4 * coupling), rel_tol=1e-7)
            assert isclose(total, predicted, rel_tol=1e-6)
            assert residual > 0
            print(f"eta={eta:.3f}, r={radius:.3f}, total/r^4={total/radius**4:.9f}, "
                  f"shell/r^4={residual/radius**4:.9f}")


if __name__ == "__main__":
    main()
