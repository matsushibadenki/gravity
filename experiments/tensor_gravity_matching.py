"""Compare the two-derivative coefficients of an effective-metric tensor shell."""

from fractions import Fraction as F


def coefficients(speed, bare, induced):
    """Return spatial curvature, kinetic, and area coefficients in EH units."""
    spatial = bare + induced / speed
    kinetic = bare + induced / speed**3
    # Divide the entropy per area by 4*pi for direct comparison.
    area = bare + induced / speed**2
    return spatial, kinetic, area


def main():
    bare, induced = F(2), F(1, 3)
    for speed in (F(1, 2), F(1), F(2)):
        spatial, kinetic, area = coefficients(speed, bare, induced)
        assert spatial > 0 and kinetic > 0
        assert area - spatial == induced * (1 - speed) / speed**2
        assert spatial - kinetic == induced * (speed**2 - 1) / speed**3
        assert (spatial == kinetic == area) == (speed == 1)
        assert coefficients(speed, 0, induced)[0] / coefficients(speed, 0, induced)[1] == speed**2
        print(f"v={speed}: A_R={spatial}, A_K={kinetic}, "
              f"eta/(4*pi)={area}, c_T^2={spatial/kinetic}, 4*eta*G_static={area/spatial}")


if __name__ == "__main__":
    main()
