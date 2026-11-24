"""Check the clock-projected curvature and modular cost of clock energy."""

from fractions import Fraction as F
from itertools import product
from math import isclose, pi, sin


def riemann(wave, metric, a, b, c, d):
    # Four derivatives of a Fourier amplitude, with both derivative signs included.
    return (-wave[b] * wave[c] * metric[a][d] - wave[a] * wave[d] * metric[b][c]
            + wave[a] * wave[c] * metric[b][d] + wave[b] * wave[d] * metric[a][c]) / 2


def check_clock_projection():
    wave = (F(7, 10), F(1, 5), F(0), F(4, 5))
    lapse = [[F(int(i == j == 0)) for j in range(4)] for i in range(4)]
    for a, b in product(range(4), repeat=2):
        for i, j in product(range(1, 4), repeat=2):
            assert riemann(wave, lapse, a, b, i, j) == 0
    metric = [[F(int(i == j == 1)) for j in range(4)] for i in range(4)]
    assert riemann(wave, metric, 0, 1, 1, 3) != 0
    print("The projected curvature is lapse independent and retains time derivatives.")
    # In an observer frame tilted relative to the clock, an internal
    # spatial basis vector has a nonzero observer-time component.
    tilted_spatial_axis = (F(3, 4), F(5, 4), F(0), F(0))
    observer_lapse_curvature = sum(
        component * riemann(wave, lapse, 0, 3, index, 3)
        for index, component in enumerate(tilted_spatial_axis)
    )
    assert observer_lapse_curvature == F(6, 25)
    print(f"Tilted observer: projected lapse-curvature component={observer_lapse_curvature}.")


def check_clock_modular_deficit():
    amplitude, wave_number = 0.2, 0.8
    count = 20000
    previous_error = float("inf")
    for radius in (0.6, 0.3, 0.15, 0.075):
        phase = wave_number * radius
        weighted = 0.0
        for index in range(count):
            x = (index + 0.5) / count
            weighted += x**2 * (1 - x**2) * sin(phase * x) / (phase * x)
        residual = -4 * pi**2 * amplitude * radius**4 * weighted / count
        prediction = -8 * pi**2 * amplitude / 15
        error = abs(residual / radius**4 / prediction - 1)
        assert error < previous_error
        previous_error = error
        print(f"r={radius:.3f}: matter-only residual/r^4={residual/radius**4:+.9f}")
    assert isclose(residual / radius**4, prediction, rel_tol=0.001)


if __name__ == "__main__":
    check_clock_projection()
    check_clock_modular_deficit()
