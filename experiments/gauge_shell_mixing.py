"""Check linearized Ricci gauge invariance and the massive-shell response."""

from fractions import Fraction
from math import isclose, sqrt


def spatial_ricci(symbol, field):
    """Linearized spatial Ricci tensor, with Fourier derivatives i*k."""
    size = sum(component**2 for component in symbol)
    trace = sum(field[i][i] for i in range(3))
    return [
        [
            (size * field[i][j] + symbol[i] * symbol[j] * trace
             - sum(symbol[l] * (symbol[i] * field[j][l] + symbol[j] * field[i][l])
                   for l in range(3))) / 2
            for j in range(3)
        ]
        for i in range(3)
    ]


def check_ricci():
    wave_vector = (Fraction(1), Fraction(2), Fraction(-3))
    for axis in range(3):
        gauge_shift = [
            [wave_vector[i] * (j == axis) + wave_vector[j] * (i == axis)
             for j in range(3)]
            for i in range(3)
        ]
        assert all(value == 0 for row in spatial_ricci(wave_vector, gauge_shift) for value in row)

    polarization = [[Fraction(1), 0, 0], [0, Fraction(-1), 0], [0, 0, 0]]
    assert spatial_ricci((0, 0, Fraction(2)), polarization) == [
        [2 * value for value in row] for row in polarization
    ]
    print("Linearized spatial Ricci: three gauge shifts vanish; TT response is k^2/2.")


def check_mixing():
    light_speed, shell_speed, mass, coupling = 1.0, 0.8, 2.0, 0.3
    ratios = []
    for wave_number in (0.1, 0.05, 0.025):
        k2 = wave_number**2
        light = light_speed**2 * k2
        massive = mass**2 + shell_speed**2 * k2
        mixing = coupling * k2
        determinant = light * massive - mixing**2
        assert determinant > 0
        upper = (light + massive + sqrt((massive - light)**2 + 4 * mixing**2)) / 2
        lower = determinant / upper
        shell_ratio = -mixing / (massive - lower)
        assert isclose(light + mixing * shell_ratio, lower, abs_tol=1e-14)
        misfit = -(lower - light) / k2**2
        assert isclose(misfit, coupling**2 / mass**2, rel_tol=1e-3)
        assert isclose(shell_ratio / k2, -coupling / mass**2, rel_tol=1e-3)
        ratios.append(abs(shell_ratio))
        print(f"k={wave_number:.3f}  omega/k={sqrt(lower)/wave_number:.8f}  massive/light={shell_ratio:.9f}")
    assert all(isclose(left / right, 4, rel_tol=1e-3) for left, right in zip(ratios, ratios[1:]))


if __name__ == "__main__":
    check_ricci()
    check_mixing()
