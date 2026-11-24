"""Compare tensor perturbations of diffusion and boundary entropy."""

from math import cos, exp, isclose, pi, sin, sqrt
from statistics import mean


def sphere_samples(latitudes=400, azimuths=128):
    """Equal-weight midpoint quadrature in z and azimuth."""
    for latitude in range(latitudes):
        z = -1 + 2 * (latitude + 0.5) / latitudes
        radial = sqrt(1 - z * z)
        for azimuth in range(azimuths):
            angle = 2 * pi * (azimuth + 0.5) / azimuths
            yield radial * cos(angle), radial * sin(angle), z


def quadrupole(vector):
    x, y, _ = vector
    return x * x - y * y


def hexadecapole(z):
    return (35 * z**4 - 30 * z * z + 3) / 8


def main():
    directions = list(sphere_samples())
    # Q=diag(1,-1,0); the unperturbed diffusivity is normalized to identity.
    diffusion_x = 3 * mean(x * x * quadrupole((x, y, z)) for x, y, z in directions)
    entropy_x = 2 * mean(abs(x) * quadrupole((x, y, z)) for x, y, z in directions)
    residual = entropy_x - diffusion_x / 2
    assert isclose(diffusion_x, 2 / 5, abs_tol=2e-4)
    assert isclose(entropy_x, 1 / 4, abs_tol=2e-4)
    assert isclose(residual, 1 / 20, abs_tol=2e-4)
    print(f"quadrupole: diffusion={diffusion_x:.7f}, entropy={entropy_x:.7f}, residual={residual:.7f}")

    diffusion_z = 3 * mean(z * z * hexadecapole(z) for _, _, z in directions)
    entropy_z = 2 * mean(abs(z) * hexadecapole(z) for _, _, z in directions)
    assert isclose(diffusion_z, 0, abs_tol=3e-4)
    assert isclose(entropy_z, -1 / 24, abs_tol=2e-4)
    print(f"degree four: diffusion={diffusion_z:.7f}, entropy={entropy_z:.7f}")

    def integrated_quadrupole(shape):
        # Surface normal and area element under exp(shape*Q), determinant one.
        values = []
        for x, y, z in directions:
            normal = x * exp(-shape), y * exp(shape), z
            norm = sqrt(sum(component * component for component in normal))
            values.append(quadrupole(normal) / norm)
        return 4 * pi * mean(values)

    step = 1e-5
    ellipsoid_derivative = (integrated_quadrupole(step) - integrated_quadrupole(-step)) / (2 * step)
    assert isclose(ellipsoid_derivative, -64 * pi / 15, abs_tol=2e-4)
    print(f"volume-preserving ellipsoid: surface quadrupole derivative={ellipsoid_derivative:.7f}")


if __name__ == "__main__":
    main()
