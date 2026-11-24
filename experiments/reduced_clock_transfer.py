"""Frozen-reading reduced clock transfer matrix and its canonical replica derivative."""

from itertools import product

import numpy as np

from reduced_clock_ball_seam import kinetic_variation, spectral_operators


def cubic_density(q, dq, hubble, gradients, laplacian, inverse):
    """Cubic ADM density in units of A on the a=1 stiff-clock slice."""
    u = dq / hubble
    psi = -q / hubble + 3 * inverse @ dq
    grad_q = np.array([derivative @ q for derivative in gradients]).T
    grad_psi = np.array([derivative @ psi for derivative in gradients]).T
    hessian_psi = np.stack(
        [left @ right @ psi for left, right in product(gradients, repeat=2)], axis=-1
    ).reshape(-1, 3, 3)
    contraction = np.sum(grad_q * grad_psi, axis=-1)
    connection = (grad_q[..., :, None] * grad_psi[..., None, :]
                  + grad_psi[..., :, None] * grad_q[..., None, :]
                  - contraction[..., None, None] * np.eye(3))
    tr_hessian = np.trace(hessian_psi, axis1=-2, axis2=-1)
    tr_connection = np.trace(connection, axis1=-2, axis2=-1)
    curvature = -4 * (laplacian @ q) * (q**2 / 2 + q * u)
    curvature -= 2 * np.sum(grad_q**2, axis=-1) * (q + u)
    clock = hubble**2 * (-54 * u * q**2 + 18 * u**2 * q - 6 * u**3)
    shift_linear = 4 * hubble * (q**2 * tr_hessian / 2 - q * tr_connection)
    shift_quadratic = -(q + u) * (np.sum(hessian_psi**2, axis=(-1, -2)) - tr_hessian**2)
    shift_quadratic -= 2 * (np.sum(hessian_psi * connection, axis=(-1, -2))
                            - tr_hessian * tr_connection)
    return curvature + clock + shift_linear + shift_quadratic


def hessian(spacing, sites, profile, gradients, laplacian, inverse):
    count = len(sites)
    hubble = 0.3
    project = np.eye(count) - 1 / count
    zero = np.zeros(count)
    derivatives = [np.array(gradients), laplacian, inverse]

    def cubic(q, dq):
        return np.sum(cubic_density(q, dq, hubble, *derivatives)) * spacing**3

    base = cubic(profile, zero)

    def form(vector):
        q, dq = np.split(vector, 2)
        q, dq = project @ q, project @ dq
        return (cubic(profile + q, dq) + cubic(profile - q, -dq) - 2 * base) / 2

    basis = np.eye(2 * count)
    diagonal = np.array([form(vector) for vector in basis])
    output = np.diag(2 * diagonal)
    for i, j in zip(*np.triu_indices(2 * count, 1)):
        output[i, j] = output[j, i] = form(basis[i] + basis[j]) - diagonal[i] - diagonal[j]
    return output


def hamiltonian(laplacian, spacing, correction, amplitude):
    count = len(laplacian)
    normalization = 12 * spacing**3
    # Retain local canonical sites and regulate the separate homogeneous oscillator.
    potential = normalization * (-laplacian + np.ones_like(laplacian) / count)
    mass = normalization * np.eye(count)
    mixing = amplitude * correction[count:, :count]
    mass += amplitude * correction[count:, count:]
    potential -= amplitude * correction[:count, :count]
    inverse_mass = np.linalg.solve(mass, np.eye(count))
    matrix = np.block([
        [potential + mixing.T @ inverse_mass @ mixing, -mixing.T @ inverse_mass],
        [-inverse_mass @ mixing, inverse_mass],
    ])
    return mass, matrix


def symplectic_form(count):
    identity = np.eye(count)
    zero = np.zeros_like(identity)
    return np.block([[zero, identity], [-identity, zero]])


def covariance(energy, beta):
    values, modes = np.linalg.eigh(energy)
    assert min(values) > 0
    root = (modes * np.sqrt(values)) @ modes.T
    inverse = (modes / np.sqrt(values)) @ modes.T
    frequency, basis = np.linalg.eigh(1j * root @ symplectic_form(len(energy) // 2) @ root)
    positive = np.abs(frequency)
    thermal = positive if np.isinf(beta) else positive / np.tanh(beta * positive / 2)
    return (inverse @ (basis * thermal) @ basis.conj().T @ inverse).real / 2


def regional_spectrum(whole, selected):
    count = len(whole) // 2
    indices = np.r_[selected, selected + count]
    restricted = whole[np.ix_(indices, indices)]
    values, modes = np.linalg.eigh(restricted)
    root = (modes * np.sqrt(values)) @ modes.T
    spectrum = np.linalg.eigvalsh(1j * root @ symplectic_form(len(selected)) @ root)
    assert min(spectrum[len(selected):]) > 0.5 - 1e-9
    return np.maximum(spectrum[len(selected):] - 0.5, 0)


def replica_action(occupation, replicas):
    return np.sum(np.log((1 + occupation)**replicas - occupation**replicas))


def entropy(occupation):
    active = occupation[occupation > 1e-13]
    return np.sum((1 + active) * np.log1p(active) - active * np.log(active))



def band_variation(spatial, mass_change, potential_change, mixing_change,
                   selected, replicas, band, steps=4, dt=0.2):
    """First variation of a midpoint time-transfer heat determinant."""
    count = len(spatial)
    result = 0.0
    inside = np.zeros(count, dtype=bool)
    inside[selected] = True
    for branch in range(replicas):
        phase = np.exp(2j * np.pi * branch / replicas)
        seam = np.diag(np.where(inside, phase, 1))
        seam_change = (mass_change @ seam - seam @ mass_change) / 2
        baseline = np.zeros((steps * count, steps * count), dtype=complex)
        variation = np.zeros_like(baseline)
        for time in range(steps):
            following = (time + 1) % steps
            current = slice(time * count, (time + 1) * count)
            successor = slice(following * count, (following + 1) * count)
            d = np.zeros((count, steps * count), dtype=complex)
            q = np.zeros_like(d)
            d[:, current], q[:, current] = -np.eye(count), np.eye(count) / 2
            endpoint = seam if following == 0 else np.eye(count)
            d[:, successor], q[:, successor] = endpoint, endpoint / 2
            dd = np.zeros_like(d)
            if following == 0:
                dd[:, successor] = seam_change
            dq = dd / 2
            baseline += d.conj().T @ d / dt**2 + q.conj().T @ spatial @ q
            variation += (dd.conj().T @ d + d.conj().T @ dd) / dt**2
            variation += dq.conj().T @ spatial @ q + q.conj().T @ spatial @ dq
            variation += q.conj().T @ potential_change @ q
            mixed = d.conj().T @ mixing_change @ q
            variation -= 1j * (mixed + mixed.conj().T) / dt

        values, vectors = np.linalg.eigh(baseline)
        assert min(values) > 0
        lower, upper = band
        weights = np.exp(-lower * values) * (-np.expm1(-(upper - lower) * values)) / values
        diagonal = np.sum(vectors.conj() * (variation @ vectors), axis=0)
        result += weights @ diagonal / 2
    assert abs(result.imag) < 1e-9
    return result.real


def shared_band_check(spacing, profile, gradients, laplacian, correction, selected):
    count = len(profile)
    normalization = 12 * spacing**3
    clock_spatial = -laplacian + np.ones_like(laplacian) / count
    clock_mass = correction[count:, count:] / normalization
    clock_potential = (-correction[:count, :count] / normalization
                       - (clock_mass @ clock_spatial + clock_spatial @ clock_mass) / 2)
    clock_mixing = correction[count:, :count] / normalization

    heavy_mass = np.diag(3 * profile)
    heavy_spatial = -laplacian + 4 * np.eye(count)
    heavy_potential = sum(derivative.T @ (profile[:, None] * derivative) for derivative in gradients)
    heavy_potential += 4 * heavy_mass - (heavy_mass @ heavy_spatial + heavy_spatial @ heavy_mass) / 2
    heavy_mixing = np.zeros_like(laplacian)
    band = (0.02, 0.04)
    for label, rank, fields in (
        ("clock", 1, (clock_spatial, clock_mass, clock_potential, clock_mixing)),
        ("heavy", 5, (heavy_spatial, heavy_mass, heavy_potential, heavy_mixing)),
    ):
        smooth = band_variation(*fields, selected, 1, band)
        values = [rank * (band_variation(*fields, selected, n, band) - n * smooth) for n in (2, 3)]
        print(f"  {label} smooth-subtracted band response (n=2,3): {values}")


def main():
    spacing = 0.25
    sites, gradients, laplacian, inverse = spectral_operators(3, spacing)
    distance = np.linalg.norm(spacing * (sites - 1), axis=1)
    profile = np.sinc(0.8 * distance / np.pi) - 1
    correction = hessian(spacing, sites, profile, gradients, laplacian, inverse)
    count = len(sites)
    expected_mass = kinetic_variation(profile, gradients, laplacian, inverse, 0.3)
    assert np.allclose(correction[count:, count:] / (12 * spacing**3), expected_mass)
    assert all(np.linalg.norm(block) > 0 for block in (
        correction[:count, :count], correction[count:, :count], correction[count:, count:]
    ))

    step = 1e-4
    ground = {}
    for amplitude in (-step, 0, step):
        mass, energy = hamiltonian(laplacian, spacing, correction, amplitude)
        assert np.linalg.slogdet(mass)[0] == 1
        ground[amplitude] = covariance(energy, beta=np.inf)
    thermal = covariance(energy, beta=30)
    assert np.allclose(thermal, ground[step], rtol=1e-8, atol=1e-8)
    for radius in (0.27, 0.38):
        selected = np.where(distance < radius)[0]
        occupations = {key: regional_spectrum(value, selected) for key, value in ground.items()}
        for occupation in occupations.values():
            derivative = (replica_action(occupation, 1 + 1e-5)
                          - replica_action(occupation, 1 - 1e-5)) / 2e-5
            assert np.isclose(derivative, entropy(occupation), rtol=1e-7)
            assert abs(replica_action(occupation, 1)) < 1e-14
        variation = (entropy(occupations[step]) - entropy(occupations[-step])) / (2 * step)
        print(f"r={radius:.2f}, sites={len(selected)}: canonical dS/d(background)={variation:+.9f}")
        shared_band_check(spacing, profile, gradients, laplacian, correction, selected)


if __name__ == "__main__":
    main()
