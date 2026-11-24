"""Reproduce the curved-boundary and fixed-volume QIEG checks."""

from itertools import product
from math import ceil, cos, floor, pi, sin, sqrt
from statistics import mean


def symmetric_difference(axes, shift):
    """Volume of the symmetric difference of two translated ellipsoids."""
    distance = sqrt(sum((delta / axis) ** 2 for axis, delta in zip(axes, shift)))
    determinant = axes[0] * axes[1] * axes[2]
    if distance >= 2:
        return determinant * 8 * pi / 3
    return determinant * 2 * pi * distance * (1 - distance**2 / 12)


def grid_volume(axes, step, displacement, origin):
    """Count crossing edges whose endpoints are on the shifted cubic grid."""
    ranges = []
    for axis, offset, jump in zip(axes, origin, displacement):
        bound = ceil(axis / step) + abs(jump) + 1
        ranges.append(range(-bound, bound + 1))
    terms = [
        {index: ((index + offset) * step / axis) ** 2 for index in indices}
        for axis, offset, indices in zip(axes, origin, ranges)
    ]

    def inside(point):
        return sum(table[index] for table, index in zip(terms, point)) < 1

    # Endpoints outside the counting box are also outside the ellipsoid.
    count = 0
    for point in product(*ranges):
        endpoint = tuple(index + jump for index, jump in zip(point, displacement))
        endpoint_inside = all(index in table for table, index in zip(terms, endpoint))
        if inside(point) != (endpoint_inside and inside(endpoint)):
            count += 1
    return count * step**3


def sphere_directions(count):
    for index in range(count):
        z = 1 - 2 * (index + 0.5) / count
        azimuth = pi * (3 - sqrt(5)) * index
        radial = sqrt(1 - z * z)
        yield radial * cos(azimuth), radial * sin(azimuth), z


def check_curved_boundaries():
    for axes in ((1, 1, 1), (1.2, 1.0, 0.7)):
        length = 0.2
        exact = symmetric_difference(axes, (length, length, 0))
        for resolution in (15, 30):
            step = 1 / resolution
            jump = floor(length * resolution + 0.5)
            estimates = [
                grid_volume(axes, step, (jump, jump, 0), origin)
                for origin in ((0.13, 0.37, 0.71), (0.63, 0.87, 0.21))
            ]
            error = max(abs(value - exact) / exact for value in estimates)
            print(f"{axes} a={step:.5f} crossing-volume error <= {error:.3%}")
            assert error < 0.02

    axes = (1.2, 1.0, 0.7)
    directions = list(sphere_directions(8192))
    determinant = axes[0] * axes[1] * axes[2]
    # Independent surface-area integral using the transformed area element.
    area = 4 * pi * determinant * mean(
        sqrt(sum((component / axis) ** 2 for component, axis in zip(direction, axes)))
        for direction in directions
    )
    for length in (0.2, 0.1):
        entropy = 2 * mean(
            symmetric_difference(axes, tuple(length * component for component in direction))
            for direction in directions
        ) / length
        print(f"Ellipsoid L={length:.2f} entropy/area={entropy / area:.8f}")
        assert 0 < 1 - entropy / area < (length / min(axes))**2 / 12


def check_fixed_volume():
    eta = 1.0
    radius = 1.0
    length = 0.2
    area = 4 * pi * radius**2

    def entropy(scale):
        coordinate_radius = radius * sqrt(scale)
        return 2 * eta * scale * symmetric_difference(
            (coordinate_radius,) * 3, (length, 0, 0)
        ) / length

    epsilon = 1e-5
    derivative = (entropy(1 + epsilon) - entropy(1 - epsilon)) / (2 * epsilon)
    expected = 2 * eta * area - pi * eta * length**2 / 3
    assert abs(derivative - expected) < 1e-8
    print(f"Fixed-volume derivative / (eta * area) = {derivative / (eta * area):.8f}")


if __name__ == "__main__":
    check_curved_boundaries()
    check_fixed_volume()
