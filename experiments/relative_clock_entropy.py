"""Compare regional entropy with and without physical clock fluctuations."""

from math import hypot, isclose, log, sqrt


def matrix_function(shell, clock, coupling, function):
    midpoint = (shell + clock) / 2
    radius = hypot((shell - clock) / 2, coupling)
    if midpoint <= radius:
        raise ValueError("The stiffness must be positive.")
    if not radius:
        value = function(midpoint)
        return ((value, 0.0), (0.0, value))
    upper, lower = function(midpoint + radius), function(midpoint - radius)
    average, slope = (upper + lower) / 2, (upper - lower) / (2 * radius)
    diagonal = slope * (shell - clock) / 2
    return ((average + diagonal, slope * coupling),
            (slope * coupling, average - diagonal))


def determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def mode_entropy(eigenvalue):
    occupation = max(0.0, eigenvalue - 0.5)
    return ((occupation + 1) * log(occupation + 1) - occupation * log(occupation)
            if occupation else 0.0)


def entropies(clock_gap, coupling):
    # The symmetric and antisymmetric spatial modes form independent pairs.
    modes = ((3.0, clock_gap**2), (7.0, clock_gap**2 + 2))
    mode_positions = [matrix_function(b, c, coupling, lambda x: 1 / sqrt(x)) for b, c in modes]
    mode_momenta = [matrix_function(b, c, coupling, sqrt) for b, c in modes]
    position, momentum = (
        [[sum(mode[i][j] for mode in block) / 4 for j in range(2)] for i in range(2)]
        for block in (mode_positions, mode_momenta)
    )
    shell = mode_entropy(sqrt(position[0][0] * momentum[0][0]))
    clock = mode_entropy(sqrt(position[1][1] * momentum[1][1]))
    trace = sum(position[i][j] * momentum[j][i] for i in range(2) for j in range(2))
    product = determinant(position) * determinant(momentum)
    large = (trace + sqrt(max(0.0, trace**2 - 4 * product))) / 2
    joint = mode_entropy(sqrt(large)) + mode_entropy(sqrt(product / large))
    return shell, clock, joint


def main():
    reference, free_clock, uncoupled_joint = entropies(2.0, 0.0)
    assert isclose(uncoupled_joint, reference + free_clock, abs_tol=1e-12)
    deviations = []
    for gap in (2.0, 4.0, 8.0, 16.0, 32.0):
        shell, clock, joint = entropies(gap, 1.0)
        assert all(isclose(left, right, abs_tol=1e-12)
                   for left, right in zip((shell, clock, joint), entropies(gap, -1.0)))
        mutual_information = shell + clock - joint
        assert mutual_information > 0
        deviations.append(abs(shell - reference))
        print(f"clock gap={gap:>4.1f}  shell-reference={shell-reference:+.9f}  "
              f"clock={clock:.9f}  mutual information={mutual_information:.9f}")
    assert all(right < left for left, right in zip(deviations, deviations[1:]))
    assert deviations[-1] < 1e-4


if __name__ == "__main__":
    main()
