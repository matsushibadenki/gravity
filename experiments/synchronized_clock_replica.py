"""Verify clock synchronization and the conditional replica wiring."""

from fractions import Fraction as F
from itertools import product


def check_clock_reduction():
    sites = 4
    # Constraint rows act on T or P respectively. Their Poisson brackets
    # reduce to dot products of these rows.
    synchronization = [
        tuple(int(index == site) - int(index == 0) for index in range(sites))
        for site in range(1, sites)
    ]
    total_momentum = (1,) * sites
    for row in synchronization:
        assert sum(a * b for a, b in zip(row, total_momentum)) == 0

    # Gauge conditions P_x=0 for x>0 pair with the synchronization constraints.
    assert [row[1:] for row in synchronization] == [
        tuple(int(i == j) for i in range(sites - 1)) for j in range(sites - 1)
    ]
    print("Clock constraints preserve total momentum and remove all relative pairs.")


def check_conditional_gluing():
    # Normalized state on two sites, with nonzero entanglement across the cut.
    amplitude = ((F(1, 3), F(2, 3)), (F(2, 3), F(0)))
    marginal = tuple(tuple(sum(amplitude[i][k] * amplitude[j][k] for k in range(2))
                           for j in range(2)) for i in range(2))
    for replicas in range(1, 6):
        regional_trace = sum(
            multiply(marginal[sites[i]][sites[(i + 1) % replicas]] for i in range(replicas))
            for sites in product(range(2), repeat=replicas)
        )
        cyclic_gluing = sum(
            multiply(amplitude[sites[i]][outside[i]]
                     * amplitude[sites[(i + 1) % replicas]][outside[i]]
                     for i in range(replicas))
            for sites in product(range(2), repeat=replicas)
            for outside in product(range(2), repeat=replicas)
        )
        assert regional_trace == cyclic_gluing
        print(f"n={replicas}: regional trace = cyclic gluing = {regional_trace}")


def multiply(values):
    result = F(1)
    for value in values:
        result *= value
    return result


if __name__ == "__main__":
    check_clock_reduction()
    check_conditional_gluing()
