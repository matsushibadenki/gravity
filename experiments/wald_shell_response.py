"""Check binormal curvature contractions for two shell interactions."""

from fractions import Fraction as F
from itertools import product


def normal_plane_curvature(a, b, c, d):
    """Derivative of R_abcd with respect to the component R_0101."""
    oriented_pair = {(0, 1): 1, (1, 0): -1}
    return oriented_pair.get((a, b), 0) * oriented_pair.get((c, d), 0)


def main():
    signature = (-1, 1, 1, 1)
    ricci = [
        sum(signature[a] * normal_plane_curvature(a, b, a, b) for a in range(4))
        for b in range(4)
    ]
    assert ricci == [1, -1, 0, 0]
    spatial_projection = sum(
        normal_plane_curvature(i, j, i, j) for i, j in product(range(1, 4), repeat=2)
    )
    assert spatial_projection == 0

    # The Wald entropy density divided by -2*pi equals dL/dR_0101.
    einstein_coefficient = F(2, 7)
    mixing = F(3, 10)
    shell = [F(0), F(2, 3), F(-1, 3), F(-1, 3)]
    einstein_derivative = einstein_coefficient * sum(
        sign * component for sign, component in zip(signature, ricci)
    )
    spacetime_mixing_derivative = -mixing * sum(
        field * component for field, component in zip(shell, ricci)
    )
    assert einstein_derivative == -2 * einstein_coefficient
    assert spacetime_mixing_derivative == mixing * shell[1]
    print("Wald density: Einstein = 4*pi*A_E; intrinsic spatial mixing = 0.")
    print("Wald density: spacetime Ricci mixing = -2*pi*g*b_nn.")


if __name__ == "__main__":
    main()
