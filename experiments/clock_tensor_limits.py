"""Check the order of the continuum and clock-gap limits for tensor mixing."""

from itertools import product
from math import isclose, pi, sin, sqrt
from statistics import mean

from relative_clock_entropy import matrix_function, mode_entropy


def species_entropy(momentum_squared, clock_gap, mixing):
    shell = 1 + momentum_squared
    clock = clock_gap**2 + momentum_squared
    off_diagonal = mixing * momentum_squared
    position = matrix_function(shell, clock, off_diagonal, lambda value: value**-0.5)
    momentum = matrix_function(shell, clock, off_diagonal, sqrt)
    return mode_entropy(sqrt(position[0][0] * momentum[0][0]) / 2)


def entropy_per_site(spacing, clock_gap, mixing, lattice_size=12):
    # Use the positive nearest-neighbor lattice symbol for |k|^2.
    momenta = [4 * sin(pi * index / lattice_size)**2 / spacing**2
               for index in range(lattice_size)]
    return mean(species_entropy(sum(vector), clock_gap, mixing)
                for vector in product(momenta, repeat=3))


def main():
    mixing = 0.45
    high, low = sqrt(1 + mixing), sqrt(1 - mixing)
    ultraviolet = mode_entropy(sqrt((high + low) * (1 / high + 1 / low)) / 4)
    assert ultraviolet > 0
    assert isclose(species_entropy(1e7, 2, mixing), ultraviolet, rel_tol=1e-6)
    assert entropy_per_site(0.1, 2, 0) < 1e-12
    print(f"Ultraviolet entropy per mixed mode: {ultraviolet:.9f} nats.")
    for spacing in (0.5, 0.1, 0.025):
        fixed_gap = entropy_per_site(spacing, 2, mixing)
        gap_above_cutoff = entropy_per_site(spacing, 100 / spacing, mixing)
        print(f"a={spacing:.3f}: fixed gap={fixed_gap:.9f}, "
              f"gap above cutoff={gap_above_cutoff:.3e} nats/site")
    expected_finite_sample = ultraviolet * (1 - 1 / 12**3)
    assert isclose(entropy_per_site(0.025, 2, mixing), expected_finite_sample, rel_tol=0.005)
    assert entropy_per_site(0.025, 400000, mixing) < 1e-8


if __name__ == "__main__":
    main()
