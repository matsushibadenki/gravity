"""Evaluate the induced seam insertion of the clock kinetic form on a ball."""

from itertools import product

import numpy as np


def spectral_operators(size, spacing):
    sites = np.array(list(product(range(size), repeat=3)))
    frequencies = 2 * np.pi * np.fft.fftfreq(size, spacing)
    momenta = np.array(list(product(frequencies, repeat=3)))
    square = np.sum(momenta**2, axis=1)
    modes = np.exp(1j * spacing * sites @ momenta.T) / np.sqrt(len(sites))

    def matrix(symbol):
        return np.real_if_close((modes * symbol) @ modes.conj().T).real

    gradients = [matrix(1j * momenta[:, i]) for i in range(3)]
    laplacian = matrix(-square)
    inverse = np.divide(-1, square, out=np.zeros_like(square), where=square > 0)
    return sites, gradients, laplacian, matrix(inverse)


def kinetic_variation(profile, gradients, laplacian, inverse, hubble):
    count = len(profile)
    dimension = len(gradients)
    active = np.eye(count) - 1 / count
    f_gradient = [gradient @ profile for gradient in gradients]
    lap_f = laplacian @ profile
    shift = [3 * gradient @ inverse for gradient in gradients]
    contraction = sum(value[:, None] * operator for value, operator in zip(f_gradient, shift))
    trace_e1 = np.zeros_like(active)
    result = -4 * (active.T @ (lap_f[:, None] * active)) / hubble**2
    for i, j in product(range(dimension), repeat=2):
        derivative = gradients[i] @ shift[j]
        e0 = (active if i == j else 0) - derivative
        e1 = (
            2 * profile[:, None] * derivative + f_gradient[i][:, None] * shift[j]
            + f_gradient[j][:, None] * shift[i] - (contraction if i == j else 0)
        )
        if i == j:
            trace_e1 += e1
        f_hessian = gradients[i] @ f_gradient[j]
        result += 3 * e0.T @ (profile[:, None] * e0)
        result += 2 * e0.T @ e1
        result -= 2 * active.T @ (f_hessian[:, None] * e0) / hubble**2
    result += 4 * active.T @ trace_e1
    # Normalize against the homogeneous kinetic form, which is 6*I in A units.
    return (result + result.T) / 12


def time_operator(spatial, seam, steps, dt):
    count = len(spatial)
    operator = np.kron(np.eye(steps), spatial).astype(complex)
    link = np.zeros((count, steps * count), dtype=complex)
    for time in range(steps):
        successor = (time + 1) % steps
        difference = np.zeros_like(link)
        difference[:, time * count:(time + 1) * count] = -np.eye(count)
        difference[:, successor * count:(successor + 1) * count] = (
            seam if successor == 0 else np.eye(count)
        )
        operator += difference.conj().T @ difference / dt**2
        if successor == 0:
            link = difference
    return operator, link


def response(spatial, mass_derivative, inside, replicas, steps, dt, band):
    count = len(spatial)
    total = 0.0
    low, high = band
    for branch in range(replicas):
        phase = np.exp(2j * np.pi * branch / replicas)
        seam = np.diag(np.where(inside, phase, 1))
        delta = (mass_derivative @ seam - seam @ mass_derivative) / 2
        operator, link = time_operator(spatial, seam, steps, dt)
        insertion = np.zeros_like(link)
        insertion[:, :count] = delta
        variation = (link.conj().T @ insertion + insertion.conj().T @ link) / dt**2
        values, modes = np.linalg.eigh(operator)
        assert np.min(values) > 0
        diagonal = np.sum(modes.conj() * (variation @ modes), axis=0).real
        weights = np.exp(-low * values) * (-np.expm1(-(high - low) * values)) / values
        total += np.dot(weights, diagonal) / 2
    return total


def velocity_crosscheck():
    size = 9
    spacing = 2 * np.pi / size
    sites, gradients, laplacian, inverse = spectral_operators(size, spacing)
    x, z = (sites[:, axis] * spacing for axis in (0, 2))
    mass_derivative = kinetic_variation(np.cos(z), gradients, laplacian, inverse, 0.3)
    w = np.cos(x) * (1 + np.cos(z))
    result = 6 * w @ mass_derivative @ w / len(w)
    assert np.isclose(result, 31.75, atol=1e-8)
    print(f"Reduced kinetic Fourier cross-check: {result:.8f}")


def finite_difference(spatial, mass_derivative, inside, steps, dt, band, step=1e-5):
    # For n=2 the untwisted sector has no variation. The odd sector
    # can be transported with the exact mass square root independently.
    original_seam = np.diag(np.where(inside, -1, 1))
    points, weights = np.polynomial.legendre.leggauss(24)
    half_width = (band[1] - band[0]) / 2
    times = band[0] + half_width * (points + 1)
    actions = []
    for amplitude in (step, -step):
        values, vectors = np.linalg.eigh(np.eye(len(spatial)) + amplitude * mass_derivative)
        root = (vectors * np.sqrt(values)) @ vectors.T
        inverse = (vectors / np.sqrt(values)) @ vectors.T
        operator, _ = time_operator(spatial, root @ original_seam @ inverse, steps, dt)
        spectrum = np.linalg.eigvalsh(operator)
        heat = np.exp(-times[:, None] * spectrum).sum(axis=1)
        actions.append(-half_width * np.dot(weights, heat / times) / 2)
    return (actions[0] - actions[1]) / (2 * step)


def main():
    velocity_crosscheck()
    spacing = 0.25
    size = 5
    sites, gradients, laplacian, inverse = spectral_operators(size, spacing)
    distance = spacing * np.linalg.norm(sites - (size - 1) / 2, axis=1)
    # A radial clock profile at the sampled sites, with the cutoff to zero
    # placed outside both tested balls and inside the periodic box.
    taper = np.clip((0.62 - distance) / 0.14, 0, 1)
    taper = taper**3 * (10 + taper * (-15 + 6 * taper))
    profile = (np.sinc(0.8 * distance / np.pi) - 1) * taper
    mass_derivative = kinetic_variation(profile, gradients, laplacian, inverse, 0.3)
    # Regulate the homogeneous reference oscillator without changing the
    # spatially varying velocity block, which excludes the zero mode.
    spatial = -laplacian + np.ones_like(laplacian) / len(sites)
    band = (0.02, 0.04)
    for radius in (0.27, 0.38):
        inside = distance < radius
        data = [response(spatial, mass_derivative, inside, n, 4, 0.2, band) for n in (1, 2, 3)]
        heavy_spatial = -laplacian + 4 * np.eye(len(sites))
        heavy_local_measure = np.diag(3 * profile)
        heavy_seam = 5 * response(heavy_spatial, heavy_local_measure, inside, 2, 4, 0.2, band)
        assert abs(heavy_seam) < 1e-14
        assert abs(data[0]) < 1e-14
        assert all(abs(value) > 1e-8 for value in data[1:])
        alternative = finite_difference(spatial, mass_derivative, inside, 4, 0.2, band)
        assert np.isclose(data[1], alternative, rtol=1e-5, atol=1e-8)
        print(f"r={radius:.2f}, sites={sum(inside)}: n=1,2,3 seam responses={data}; heavy seam={heavy_seam:.1f}")


if __name__ == "__main__":
    main()
