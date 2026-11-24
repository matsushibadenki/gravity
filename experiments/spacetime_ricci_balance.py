"""Check the fixed-volume entropy balance for spacetime-Ricci mixing."""

from fractions import Fraction as F
from math import cos, isclose, pi, sin


def main():
    einstein, mixing, beta = F(1, 5), F(3, 10), F(2, 5)
    mass2, speed2 = F(4), F(16, 25)
    density = F(1, 100)
    radius = 0.5
    count = 10000

    for wave_number in (F(1, 2), F(1, 4), F(1, 8)):
        k2 = wave_number**2
        denominator = mass2 + speed2 * k2
        pressure_trace = density  # Traceless stress tensor.
        slip = -pressure_trace / (4 * einstein * k2 + 2 * mixing**2 * k2**2 / (3 * denominator))
        shell = -mixing * k2 * slip / denominator
        phi = -(density + pressure_trace) / (4 * einstein * k2)
        psi = phi - slip
        double_divergence = -F(2, 3) * k2 * shell
        assert -4 * einstein * k2 * psi + mixing * double_divergence == density
        assert -4 * einstein * k2 * slip - mixing * double_divergence == pressure_trace
        assert denominator * shell == mixing * k2 * (psi - phi)

        x = float(wave_number) * radius
        radial = angular = 0.0
        for index in range(count):
            unit = (index + 0.5) / count
            angle = x * unit
            radial += unit**2 * (1 - unit**2) * sin(angle) / angle
            angular += (unit**2 - 1 / 3) * (-2 * sin(angle / 2)**2)
        matter = 4 * pi**2 * float(density) * radius**4 * radial / count
        area = 8 * pi * float(psi) * radius**2 * (
            3 * (sin(x) - x * cos(x)) / x**3 - sin(x) / x
        )
        integral = 4 * pi * radius**2 * float(shell) * angular / count
        wald = -2 * pi * float(mixing) * integral
        independent_entropy = float(beta) * integral
        area_entropy = 4 * pi * float(einstein) * area
        assert isclose(area_entropy + matter, -wald, rel_tol=0.002)
        assert isclose(area_entropy + matter + wald + independent_entropy,
                       independent_entropy, rel_tol=0.002)
        print(f"k={float(wave_number):.3f}  area+matter={area_entropy + matter:+.9e}  "
              f"Wald={wald:+.9e}  independent shell entropy={independent_entropy:+.9e}")

    print("Both static constraints and the massive-shell equation agree exactly.")


if __name__ == "__main__":
    main()
