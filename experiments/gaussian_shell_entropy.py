"""Check the entropy of a massive quadratic shell under static forcing."""

from math import isclose, log, sqrt


def local_entropy(stiffnesses):
    # The two sites are equal-weight mixtures of the symmetric and
    # antisymmetric normal modes. Each mode has unit kinetic coefficient.
    position_variance = sum(1 / sqrt(value) for value in stiffnesses) / 4
    momentum_variance = sum(sqrt(value) for value in stiffnesses) / 4
    symplectic_eigenvalue = sqrt(position_variance * momentum_variance)
    occupation = symplectic_eigenvalue - 0.5
    return (occupation + 1) * log(occupation + 1) - occupation * log(occupation)


def main():
    even, odd = 3.0, 7.0
    ground_entropy = local_entropy((even, odd))
    for strength in (0.01, 0.1, 1.0):
        # The two force components are strength and -strength/2.
        even_mean, odd_mean = -strength / (2 * sqrt(2) * even), -3 * strength / (2 * sqrt(2) * odd)
        site_mean = (even_mean + odd_mean) / sqrt(2)
        other_mean = (even_mean - odd_mean) / sqrt(2)
        diagonal, off_diagonal = (even + odd) / 2, (even - odd) / 2
        assert isclose(diagonal * site_mean + off_diagonal * other_mean, -strength)
        assert isclose(off_diagonal * site_mean + diagonal * other_mean, strength / 2)
        # Noncentral position moments contain the displacement; the reduced
        # Gaussian entropy instead uses the centered covariance.
        centered_position = (1 / sqrt(even) + 1 / sqrt(odd)) / 4
        raw_second = centered_position + site_mean**2
        symplectic_eigenvalue = sqrt(
            (raw_second - site_mean**2) * (sqrt(even) + sqrt(odd)) / 4
        )
        n = symplectic_eigenvalue - 0.5
        entropy = (n + 1) * log(n + 1) - n * log(n)
        assert isclose(entropy, ground_entropy, abs_tol=1e-14)
        print(f"force={strength:.2f}  site mean={site_mean:+.8f}  entropy={entropy:.9f}")

    step = 1e-5
    derivative = (local_entropy((even, odd + step)) - local_entropy((even, odd - step))) / (2 * step)
    assert derivative > 0
    print(f"Changing the stiffness at zero mean gives dS/dK_odd={derivative:.9f}.")


if __name__ == "__main__":
    main()
