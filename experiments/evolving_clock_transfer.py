"""Evolve both Gaussian sectors on a common spatial regulator."""

from math import pi, cos, sin

import numpy as np

from reduced_clock_ball_seam import spectral_operators
from reduced_clock_transfer import covariance, entropy, hessian, regional_spectrum, replica_action, symplectic_form


def scalar_cubic_hessian(profile, profile_dot, scale, hubble, gradients, laplacian, inverse, cell):
    """Second variation of the reduced ADM cubic density in units of A."""
    count = len(profile)
    project = np.eye(count) - 1 / count
    zero = np.zeros_like(project)
    q = np.concatenate((project, zero), axis=1)
    rate = np.concatenate((zero, project), axis=1)
    u = rate / hubble
    psi = -q / hubble + 3 * scale**2 * (inverse @ rate)
    d_q = [gradient @ q for gradient in gradients]
    d_psi = [gradient @ psi for gradient in gradients]
    dd_psi = [[gradient @ term for term in d_psi] for gradient in gradients]
    tr_psi = sum(dd_psi[i][i] for i in range(3))
    background = np.r_[profile, profile_dot]
    # Configuration and fluctuation maps use the same infrared
    # convention. Constant offsets in f have no role in this test.
    result = np.zeros((2 * count, 2 * count))

    def add(coefficient, left, middle, right):
        # The Hessian of a product of three linear functions.
        for first, second, third in ((left, middle, right), (middle, right, left),
                                    (right, left, middle)):
            result[:] += coefficient * (second.T @ ((first @ background)[:, None] * third))

    lap_q = laplacian @ q
    add(-2 * scale, lap_q, q, q)
    add(-4 * scale, lap_q, q, u)
    for item in d_q:
        add(-2 * scale, item, item, q + u)
    add(-54 * scale**3 * hubble**2, u, q, q)
    add(18 * scale**3 * hubble**2, u, u, q)
    add(-6 * scale**3 * hubble**2, u, u, u)
    add(2 * scale * hubble, q, q, tr_psi)
    for i in range(3):
        add(4 * scale * hubble, q, d_q[i], d_psi[i])
    add(1 / scale, q + u, tr_psi, tr_psi)
    for i in range(3):
        for j in range(3):
            term = dd_psi[i][j]
            add(-1 / scale, q + u, term, term)
            add(-2 / scale, term, d_q[i], d_psi[j])
            add(-2 / scale, term, d_q[j], d_psi[i])
    # In 3d tr(C)=-grad(q).grad(psi); its contribution cancels the
    # delta_ij part of -2*D:C. No integrations by parts are used here.
    return (result + result.T) * cell


def background_at_times(laplacian, profile, times):
    """Integrate the leading constrained scalar profile backwards from f-dot=0."""
    values, basis = np.linalg.eigh(laplacian)
    fields = {times[-1]: (profile, np.zeros_like(profile))}
    state = np.stack((basis.T @ profile, np.zeros(len(profile))))

    def motion(time, data):
        scale = time**(1 / 3)
        return np.stack((data[1], values * data[0] / scale**2 - data[1] / time))

    for right, left in zip(times[:0:-1], times[-2::-1]):
        step = left - right
        k1 = motion(right, state)
        k2 = motion(right + step / 2, state + step * k1 / 2)
        k3 = motion(right + step / 2, state + step * k2 / 2)
        k4 = motion(left, state + step * k3)
        state += step * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        fields[left] = tuple(basis @ value for value in state)
    return fields


def phase_hamiltonian(mass, position, mixing):
    inverse = np.linalg.solve(mass, np.eye(len(mass)))
    return np.block([[position + mixing.T @ inverse @ mixing, -mixing.T @ inverse],
                     [-inverse @ mixing, inverse]])


def light_blocks(time, cell, laplacian, hessian):
    count = len(laplacian)
    scale = time**(1 / 3)
    infrared = np.ones_like(laplacian) / count
    main = (12 * scale**3 * cell * np.eye(count), 12 * scale * cell * (-laplacian + infrared),
            np.zeros_like(laplacian))
    change = hessian[count:, count:], -hessian[:count, :count], hessian[count:, :count]
    return main, change


def heavy_blocks(time, cell, profile, profile_dot, gradients, laplacian, inverse):
    scale, hubble, heavy_mass = time**(1 / 3), 1 / (3 * time), 2
    count = len(profile)
    lapse = profile_dot / hubble
    shift = -profile / hubble + 3 * scale**2 * inverse @ profile_dot
    main = (cell * scale**3 * np.eye(count),
            cell * (-scale * laplacian + scale**3 * heavy_mass**2 * np.eye(count)),
            np.zeros_like(laplacian))
    mass = cell * scale**3 * np.diag(3 * profile - lapse)
    potential = cell * scale * sum(g.T @ ((profile + lapse)[:, None] * g) for g in gradients)
    potential += cell * scale**3 * heavy_mass**2 * np.diag(3 * profile + lapse)
    mixed = -cell * scale * sum((g @ shift)[:, None] * g for g in gradients)
    return main, (mass, potential, mixed)


def evolve(initial, blocks, amplitudes, dt):
    # Use the same Gaussian initial-state convention for each sector and
    # displacement. The inhomogeneous background enters the evolution.
    reference = covariance(phase_hamiltonian(*initial), beta=np.inf)
    states = {epsilon: reference.copy() for epsilon in amplitudes}
    form = symplectic_form(len(reference) // 2)
    identity = np.eye(len(reference))
    for main, change in blocks:
        for epsilon, previous in states.items():
            energy = phase_hamiltonian(*(a + epsilon * b for a, b in zip(main, change)))
            generator = form @ energy * dt / 2
            transfer = np.linalg.solve(identity - generator, identity + generator)
            assert np.max(np.abs(transfer.T @ form @ transfer - form)) < 1e-10
            states[epsilon] = transfer @ previous @ transfer.T
    return states


def averaged_shape_response(state, sites, spacing, radius, radius_change, angular_order):
    # Translating the center uniformly over one cell turns the boundary
    # crossings into a sphere integral of the entropy increment of one site.
    # The translationally invariant reference lets that site be the origin.
    box = spacing * (sites.max() + 1)
    lattice = spacing * sites
    nodes, weights = np.polynomial.legendre.leggauss(angular_order)
    cache = {}
    integral = 0.0
    for node, weight in zip((nodes + 1) / 2, weights / 2):
        xy = np.sqrt(1 - node**2)
        for i in range(2 * angular_order):
            phi = (i + 0.5) * pi / (4 * angular_order)
            center = radius * np.array([xy * np.cos(phi), xy * np.sin(phi), node])
            offset = (lattice - center + box / 2) % box - box / 2
            inside = np.sum(offset**2, axis=1) < radius**2 - 1e-13
            inside[0] = False
            key = tuple(np.flatnonzero(inside))
            if key not in cache:
                without = entropy(regional_spectrum(state, np.array(key, dtype=int))) if key else 0.0
                with_site = entropy(regional_spectrum(state, np.array((0,) + key, dtype=int)))
                cache[key] = with_site - without
            integral += weight * cache[key] / (2 * angular_order)
    return 4 * pi * radius**2 / spacing**3 * radius_change * integral


def run(size, time_steps=4, show=True):
    box = 1.8
    spacing = box / size
    sites, gradients, laplacian, inverse = spectral_operators(size, spacing)
    distance = spacing * np.linalg.norm(sites - (size - 1) / 2, axis=1)
    taper = np.clip((0.89 - distance) / 0.18, 0, 1)
    taper = taper**3 * (10 + taper * (-15 + 6 * taper))
    profile = (np.sinc(0.8 * distance / pi) - 1) * taper
    mean = profile.mean()
    profile -= mean
    if size == 3:
        new = scalar_cubic_hessian(profile, np.zeros_like(profile), 1, 0.3,
                                   gradients, laplacian, inverse, spacing**3)
        old = hessian(spacing, sites, profile, gradients, laplacian, inverse)
        assert np.allclose(new, old, atol=1e-10)
    times = np.linspace(0.9, 1.0, 2 * time_steps + 1)
    backgrounds = background_at_times(laplacian, profile, times)
    cell = spacing**3
    light, heavy = [], []
    for time in times[1:-1:2]:
        f, df = backgrounds[time]
        cubic = scalar_cubic_hessian(f, df, time**(1 / 3), 1 / (3 * time),
                                     gradients, laplacian, inverse, cell)
        light.append(light_blocks(time, cell, laplacian, cubic))
        heavy.append(heavy_blocks(time, cell, f, df, gradients, laplacian, inverse))

    step = 1e-4
    radii = (0.46, 0.67)
    cuts = {}
    radius_derivatives = {}
    for radius in radii:
        argument = 0.8 * radius
        volume_mean = 3 * (sin(argument) - argument * cos(argument)) / argument**3 - 1 - mean
        derivative = -radius * volume_mean
        radius_derivatives[radius] = derivative
        cuts[radius] = {epsilon: np.where(distance < radius + epsilon * derivative)[0]
                        for epsilon in (-step, step)}
        assert np.array_equal(cuts[radius][-step], cuts[radius][step])
        if show:
            print(f"a={spacing:.3f}, r={radius:.2f}: fixed-W radius variation={derivative:+.9f}; "
                  "no lattice site crosses the cut", flush=True)
    results = []
    initial_light, _ = light_blocks(times[0], cell, laplacian, np.zeros((2*len(sites), 2*len(sites))))
    f0, df0 = backgrounds[times[0]]
    initial_heavy, _ = heavy_blocks(times[0], cell, f0, df0, gradients, laplacian, inverse)
    for label, rank, block, initial in (("light", 1, light, initial_light),
                                       ("heavy", 5, heavy, initial_heavy)):
        amplitudes = (-step, 0, step) if show else (-step, step)
        states = evolve(initial, block, amplitudes, 0.1 / time_steps)
        for radius in radii:
            selected = cuts[radius][step]
            occupations = {epsilon: regional_spectrum(states[epsilon], cuts[radius][epsilon])
                           for epsilon in (-step, step)}
            for spectrum in occupations.values():
                derivative = (replica_action(spectrum, 1 + 1e-5)
                              - replica_action(spectrum, 1 - 1e-5)) / 2e-5
                assert np.isclose(derivative, entropy(spectrum), rtol=1e-7)
            change = rank * (entropy(occupations[step]) - entropy(occupations[-step])) / (2 * step)
            results.append(change)
            if show:
                print(f"a={spacing:.3f} {label}, r={radius:.2f}, sites={len(selected)}: "
                      f"canonical entropy variation={change:+.9f}", flush=True)
                orders = (6, 10) if size <= 5 else (6,)
                shape = [rank * averaged_shape_response(
                    states[0], sites, spacing, radius, radius_derivatives[radius], order
                ) for order in orders]
                print(f"  separate reference shape responses (orders {orders}): {shape}", flush=True)
    return np.array(results)


if __name__ == "__main__":
    run(3, time_steps=8)
    coarse = run(5, time_steps=8)
    fine_time = run(5, time_steps=16, show=False)
    print("a=0.36: time-step refinements", fine_time - coarse, flush=True)
    assert np.max(np.abs(fine_time - coarse) / np.maximum(1, np.abs(fine_time))) < 0.05
    run(7, time_steps=8)
