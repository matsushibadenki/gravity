"""Check the first-variation filter on a nonuniform bond-entropy profile."""

from math import isclose, pi, sin


def cosine_profile_responses(radius, wave_number, samples=12000):
    """Return fixed-volume area variation and normalized entropy residual."""
    x = wave_number * radius
    # f(z) = cos(k*z) - 1, with the center at z=0. The angular average
    # uses cos(y)-1 = -2*sin(y/2)^2 to retain the small-ball signal.
    nodes = [(index + 0.5) / samples for index in range(samples)]
    surface_mean = sum(-2 * sin(x * mu / 2)**2 for mu in nodes) / samples
    volume_mean = 3 * sum(
        radial**2 * (sin(x * radial) / (x * radial) - 1) for radial in nodes
    ) / samples
    # Physical volume is kept fixed in h=(1-epsilon*f) I.
    reference_area = 4 * pi * radius**2
    area_variation = reference_area * (volume_mean - surface_mean)
    residual_over_eta = 2 * reference_area * surface_mean
    return area_variation, residual_over_eta


def main():
    wave_number = 0.8
    expected_area = 4 * pi * wave_number**2 / 15
    expected_residual = -4 * pi * wave_number**2 / 3
    differences = []
    for radius in (0.4, 0.2, 0.1, 0.05):
        area, residual = cosine_profile_responses(radius, wave_number)
        area_scale, residual_scale = area / radius**4, residual / radius**4
        differences.append(abs(residual / area + 5))
        print(f"r={radius:.2f}  area/r^4={area_scale:.9f}  "
              f"residual/(eta*r^4)={residual_scale:.9f}  ratio={residual/area:.9f}")
    assert all(right < left for left, right in zip(differences, differences[1:]))
    assert isclose(area_scale, expected_area, rel_tol=0.0002)
    assert isclose(residual_scale, expected_residual, rel_tol=0.0002)


if __name__ == "__main__":
    main()
