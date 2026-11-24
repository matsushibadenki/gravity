"""Matched Gaussian initial data and a common center average of the moving cut."""

from itertools import product
from math import pi

import numpy as np

from evolving_clock_transfer import (
    background_at_times, heavy_blocks, light_blocks, phase_hamiltonian, scalar_cubic_hessian,
)
from reduced_clock_ball_seam import spectral_operators
from reduced_clock_transfer import covariance, entropy, regional_spectrum, replica_action, symplectic_form


def matrix_roots(matrix):
    values, vectors = np.linalg.eigh(matrix)
    assert min(values) > 0
    return ((vectors * np.sqrt(values)) @ vectors.T,
            (vectors / np.sqrt(values)) @ vectors.T)


def adiabatic_state(energies, derivative_step):
    before, central, after = energies
    base = covariance(central, beta=np.inf)
    derivative = (covariance(after, beta=np.inf) - covariance(before, beta=np.inf)) / (2 * derivative_step)
    root, inverse = matrix_roots(central)
    form = symplectic_form(len(base) // 2)
    frequencies, modes = np.linalg.eigh(1j * root @ form @ root)
    derivative_modes = modes.conj().T @ root @ derivative @ root @ modes
    opposite = frequencies[:, None] * frequencies[None, :] < 0
    differences = frequencies[:, None] - frequencies[None, :]
    response = np.divide(1j * derivative_modes, differences, where=opposite,
                         out=np.zeros_like(derivative_modes))
    correction = (inverse @ modes @ response @ modes.conj().T @ inverse).real
    candidate = base + correction
    candidate_root, _ = matrix_roots(candidate)
    values, vectors = np.linalg.eigh(1j * candidate_root @ form @ candidate_root)
    pure = (candidate_root @ (vectors / np.abs(values)) @ vectors.conj().T @ candidate_root).real / 2
    assert np.max(np.abs(pure @ form @ pure - form / 4)) < 1e-9
    # At first adiabatic order the opposite-sign frequency block solves
    # Vdot_0 = J H V_1 + V_1 (J H)^T before purification.
    equation = (-1j * differences) * response
    assert np.allclose(equation[opposite], derivative_modes[opposite])
    return pure


def trajectory(initial_blocks, time_blocks, dt, amplitude, derivative_step):
    def energy(block):
        reference, variation = block
        return phase_hamiltonian(*(a + amplitude * b for a, b in zip(reference, variation)))

    state = adiabatic_state([energy(block) for block in initial_blocks], derivative_step)
    form = symplectic_form(len(state) // 2)
    identity = np.eye(len(state))
    for block in time_blocks:
        generator = dt / 2 * form @ energy(block)
        transfer = np.linalg.solve(identity - generator, identity + generator)
        state = transfer @ state @ transfer.T
    assert np.max(np.abs(state @ form @ state - form / 4)) < 1e-8
    return state


def periodic_offset(lattice, center, box):
    return (lattice - center + box / 2) % box - box / 2


def entropy_of(state, sites):
    return entropy(regional_spectrum(state, sites)) if len(sites) else 0


class MovingBall:
    def __init__(self, lattice, profile, spacing, size, radius):
        self.lattice, self.spacing, self.box, self.radius = lattice, spacing, size * spacing, radius
        frequencies = 2 * pi * np.fft.fftfreq(size, spacing)
        self.wave = np.array(list(product(frequencies, repeat=3)))
        self.coefficients = np.fft.fftn(profile.reshape((size,) * 3)).ravel() / len(profile)
        length = np.linalg.norm(self.wave, axis=1) * radius
        body = np.ones_like(length)
        valid = length > 1e-8
        body[valid] = 3 * (np.sin(length[valid]) - length[valid] * np.cos(length[valid])) / length[valid]**3
        nodes, weights = np.polynomial.legendre.leggauss(24)
        line_average = (weights / 2) @ np.sinc((nodes[:, None] + 1) * length[None, :] / (2 * pi))
        self.fixed_volume = radius * (line_average - body)

    def displacement(self, center, normal):
        phase = np.exp(1j * self.wave @ center)
        along = self.radius * self.wave @ normal
        line = self.radius * np.exp(0.5j * along) * np.sinc(along / (2 * pi))
        return float(np.real(np.dot(self.coefficients * phase, self.fixed_volume - line)))

    def state_change(self, plus, minus, epsilon, order):
        nodes = ((np.arange(order) + 0.5) / order - 0.5) * self.spacing
        value = 0.0
        cache = {}
        for center in product(nodes, repeat=3):
            offset = periodic_offset(self.lattice, center, self.box)
            sites = np.flatnonzero(np.sum(offset**2, axis=1) < self.radius**2)
            key = tuple(sites)
            if key not in cache:
                cache[key] = (entropy_of(plus, sites) - entropy_of(minus, sites)) / (2 * epsilon)
            value += cache[key]
        return value / order**3

    def shape_change(self, reference, order):
        nodes, weights = np.polynomial.legendre.leggauss(order)
        cache = {}
        integral = 0.0
        for z, weight in zip((nodes + 1) / 2, weights / 2):
            radial = np.sqrt(1 - z**2)
            for i in range(2 * order):
                phi = (i + 0.5) * pi / (4 * order)
                normal = np.array([radial * np.cos(phi), radial * np.sin(phi), z])
                unwrapped_center = -self.radius * normal
                center = (unwrapped_center + self.spacing / 2) % self.spacing - self.spacing / 2
                offsets = periodic_offset(self.lattice, unwrapped_center, self.box)
                inside = np.sum(offsets**2, axis=1) < self.radius**2 - 1e-13
                inside[0] = False
                sites = np.flatnonzero(inside)
                key = tuple(sites)
                if key not in cache:
                    cache[key] = entropy_of(reference, np.r_[0, sites]) - entropy_of(reference, sites)
                integral += weight * cache[key] * self.displacement(center, normal) / (2 * order)
        return 4 * pi * self.radius**2 * integral / self.spacing**3


def run(size):
    box, final, initial = 1.8, 1.0, 0.9
    spacing, time_steps, derivative_step = box / size, 8, 1e-4
    sites, gradients, laplacian, inverse = spectral_operators(size, spacing)
    lattice = (sites * spacing + box / 2) % box - box / 2
    distance = np.linalg.norm(lattice, axis=1)
    taper = np.clip((0.89 - distance) / 0.18, 0, 1)
    taper = taper**3 * (10 + taper * (-15 + 6 * taper))
    profile = (np.sinc(0.8 * distance / pi) - 1) * taper
    profile -= profile.mean()
    times = np.linspace(initial, final, 2 * time_steps + 1)
    initial_times = [initial - derivative_step, initial, initial + derivative_step]
    backgrounds = background_at_times(laplacian, profile, sorted(set(times) | set(initial_times)))
    cell = spacing**3

    def blocks(time, heavy):
        f, df = backgrounds[time]
        if heavy:
            return heavy_blocks(time, cell, f, df, gradients, laplacian, inverse)
        correction = scalar_cubic_hessian(f, df, time**(1 / 3), 1 / (3 * time),
                                          gradients, laplacian, inverse, cell)
        return light_blocks(time, cell, laplacian, correction)

    epsilon = 1e-5
    for name, rank, heavy in (("light", 1, False), ("heavy", 5, True)):
        initial_blocks = [blocks(time, heavy) for time in initial_times]
        time_blocks = [blocks(time, heavy) for time in times[1:-1:2]]
        minus, reference, plus = (trajectory(initial_blocks, time_blocks, 0.1 / time_steps, eps,
                                            derivative_step) for eps in (-epsilon, 0, epsilon))
        for radius in (0.46, 0.67):
            ball = MovingBall(lattice, profile, spacing, size, radius)
            centered = np.flatnonzero(distance < radius)
            occupations = regional_spectrum(reference, centered)
            from_replica = (replica_action(occupations, 1.00001)
                            - replica_action(occupations, 0.99999)) / 0.00002
            assert np.isclose(from_replica, entropy(occupations), rtol=1e-7)
            values = []
            for state_order, angular_order in ((4, 6), (6, 10)):
                state = rank * ball.state_change(plus, minus, epsilon, state_order)
                shape = rank * ball.shape_change(reference, angular_order)
                values.append((state, shape))
            print(f"a={spacing:.3f} {name}, r={radius:.2f}: "
                  f"(state, shape) at two quadratures {values}; sum={sum(values[-1]):+.9f}",
                  flush=True)


if __name__ == "__main__":
    for size in (3, 5, 7):
        run(size)
