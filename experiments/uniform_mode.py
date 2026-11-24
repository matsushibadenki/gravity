"""Check the uniform entanglement tangent and its excitation energy."""

from math import cos, isclose, log, sin, sqrt


def apply_hamiltonian(state, bonds, gap, hopping):
    result = [gap * index.bit_count() * amplitude for index, amplitude in enumerate(state)]
    for index, amplitude in enumerate(state):
        for left, right in bonds:
            if ((index >> left) ^ (index >> right)) & 1:
                target = index ^ (1 << left) ^ (1 << right)
                result[target] -= hopping * amplitude
    return result


def inner(left, right):
    return sum(a * b for a, b in zip(left, right))


def binary_entropy(probability):
    return -probability * log(probability) - (1 - probability) * log(1 - probability)


def main():
    # The ring is a small regular hopping graph. The proof applies at degree z.
    count = 6
    degree = 2
    bonds = [(site, (site + 1) % count) for site in range(count)]
    gap = 1.0
    uniform = [1 / sqrt(count) if index.bit_count() == 1 else 0 for index in range(1 << count)]
    angle = 0.07
    product_state = [
        sin(angle) ** index.bit_count() * cos(angle) ** (count - index.bit_count())
        for index in range(1 << count)
    ]
    occupation = sin(angle) ** 2

    for hopping in (0, 0.35, 0.5):
        tangent_energy = gap - degree * hopping
        actual = apply_hamiltonian(uniform, bonds, gap, hopping)
        assert all(isclose(value, tangent_energy * amplitude, abs_tol=1e-12)
                   for value, amplitude in zip(actual, uniform))
        energy = inner(product_state, apply_hamiltonian(product_state, bonds, gap, hopping))
        expected = count * (tangent_energy * occupation + degree * hopping * occupation**2)
        assert isclose(energy, expected, abs_tol=1e-12)
        print(f"J={hopping:.2f}  tangent energy={tangent_energy:.6f}  product energy={energy:.9f}")

    theta = 0.19
    probability = sin(theta) ** 2
    derivative = sin(2 * theta) * log((1 - probability) / probability)
    step = 1e-6
    numerical = (binary_entropy(sin(theta + step) ** 2)
                 - binary_entropy(sin(theta - step) ** 2)) / (2 * step)
    assert derivative > 0 and isclose(numerical, derivative, rel_tol=1e-9)
    print(f"Entanglement derivative dS_edge/dtheta={derivative:.9f}")


if __name__ == "__main__":
    main()
