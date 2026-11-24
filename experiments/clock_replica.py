"""Verify the clock winding and the anisotropic Gaussian shell coefficients."""

from cmath import exp, phase
from fractions import Fraction
from math import isclose, pi


def sampled_winding(replica_index, samples=256):
    # In the cap frame, the polar basis rotates by theta, while the
    # components of the copied Cartesian clock rotate by -n*theta.
    directions = [exp(1j * (pi / 2 + (1 - replica_index) * 2 * pi * i / samples))
                  for i in range(samples + 1)]
    return sum(phase(right / left) for left, right in zip(directions, directions[1:])) / (2 * pi)


def main():
    for replica_index in (1, 2, 3, 4, 6):
        winding = sampled_winding(replica_index)
        assert isclose(winding, 1 - replica_index, abs_tol=1e-12)
        print(f"replicas={replica_index}, clock winding={winding:+.0f}")

    components = 3 * (3 + 1) // 2 - 1
    for speed in (Fraction(1, 2), Fraction(1), Fraction(2)):
        # Coefficients in units of I/(48*pi). The surface coefficient follows
        # from rescaling the two tangential lengths. The smooth coefficient
        # is 4*pi times the coefficient of minus the integrated slice curvature.
        canonical_area = components / speed**2
        ultrastatic_projection = components / speed
        assert canonical_area / ultrastatic_projection == 1 / speed
        print(f"v={speed}: canonical area coefficient={canonical_area}, "
              f"ultrastatic curvature projection={ultrastatic_projection}")


if __name__ == "__main__":
    main()
