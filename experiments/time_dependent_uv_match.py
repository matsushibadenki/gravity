"""Match local smooth proper-time coefficients in a time-dependent scalar control."""

from math import pi

import numpy as np


def match(size, length, cutoff, mass=2):
    """Return dimension-two action coefficients per real scalar."""
    spacing = length / size
    wave = 2 * pi * np.fft.fftfreq(size, d=spacing)
    k2 = (wave[:, None, None] ** 2 + wave[None, :, None] ** 2
          + wave[None, None, :] ** 2).ravel()
    nodes, weights = np.polynomial.legendre.leggauss(24)
    # A dyadic shell has a known power divergence without an IR subtraction.
    times = (nodes + 3) * cutoff / 2
    heat = np.exp(-times[:, None] * k2) / length**3
    moment = times[:, None] * k2
    flat = heat.sum(axis=1)
    # Coefficient of nu^2 in the second background variation of the trace.
    metric = (-9 / 4) * flat
    metric += (heat * (3 * moment - moment**2 / 3)).sum(axis=1)
    measure = np.exp(-times * mass**2) / np.sqrt(4 * pi * times)
    # The integrated scalar curvature has second variation 6 nu^2.
    curvature = -cutoff / 4 * (weights @ (measure * metric)) / 6
    potential = cutoff / 4 * (weights @ (measure * flat))
    cone = cutoff / 24 * (weights @ (np.exp(-times * mass**2)
                                     / (4 * pi * times**2)))
    return curvature, potential, cone


def main():
    target = -1 / (384 * pi**2)
    previous_error = float("inf")
    for cutoff in (0.02, 0.005, 0.00125):
        print(f"lower proper time={cutoff:g}")
        for size in (25, 49, 97):
            curvature, potential, cone = match(size, 1.8, cutoff)
            # Euclidean effective action contains c_R R. Its replica entropy
            # is -4 pi c_R A. Apply the independent counterterm +4 pi c_R A.
            area_coefficient = cone + 4 * pi * curvature
            # Unit variation of spatial scalar curvature at fixed ball volume.
            residual = -4 * pi / 30 * area_coefficient
            print(f"  N={size:2d}  s*c_R={cutoff * curvature:+.8e}"
                  f"  s*c_X={cutoff * potential:+.8e}"
                  f"  local remainder/r^4={residual:+.8e}")
        assert np.isclose(potential, -6 * curvature, rtol=2e-4)
        assert abs(area_coefficient / cone) < 2e-4
        error = abs(cutoff * curvature - target)
        assert error < previous_error
        previous_error = error
    assert previous_error < 0.01 * abs(target)


if __name__ == "__main__":
    main()
