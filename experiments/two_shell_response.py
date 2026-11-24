"""Check area matching and shell-mode selection for two bond lengths."""

from fractions import Fraction
from math import isclose, sqrt


def area_responses(short, long):
    """Return the entropy and metric coefficients for equal shell populations."""
    entropy = Fraction(1, 4) * (short + 2 * long) / 3
    geometry = Fraction(1, 5) * (short + 4 * long) / 5
    return entropy, geometry


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def main():
    matched = (-2, 13)
    orthogonal = (13, 2)
    entropy, geometry = area_responses(*matched)
    assert entropy == geometry == 2
    assert dot(matched, orthogonal) == 0
    entropy, geometry = area_responses(*orthogonal)
    assert entropy - geometry == Fraction(173, 300)

    scale = sqrt(173)
    soft = tuple(component / scale for component in matched)
    massive = tuple(component / scale for component in orthogonal)
    gap = 2.0
    speed = 1.5
    for wave_number in (0.0, 0.01, 0.1):
        kernel = [
            [gap**2 * left * right + (speed * wave_number)**2 * (i == j)
             for j, right in enumerate(massive)]
            for i, left in enumerate(massive)
        ]
        for vector, expected in (
            (soft, (speed * wave_number)**2),
            (massive, gap**2 + (speed * wave_number)**2),
        ):
            assert all(isclose(dot(row, vector), expected * vector[i], abs_tol=1e-12)
                       for i, row in enumerate(kernel))
    print("Matched shell amplitudes (-2, 13): exact entropy and area coefficients = 2.")
    print("Orthogonal shell amplitudes (13, 2): exact area mismatch = 173/300.")
    print("Positive kernel: one soft and one massive shell combination per tensor component.")


if __name__ == "__main__":
    main()
