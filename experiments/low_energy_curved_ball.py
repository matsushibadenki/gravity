"""Check that an independent low-energy spectrum admits the curved-ball test."""

from math import cos, exp, isclose, log, log1p, pi, sin

from curved_ball_entropy_filter import cosine_profile_responses


def binary_entropy_at_log_probability(log_probability):
    probability = exp(log_probability)
    return -probability * log_probability - (1 - probability) * log1p(-probability)


def tangent_weight(entropy):
    """Return the squared angular derivative for s -> (1+epsilon)*s."""
    lower, upper = log(entropy) - 20, log(entropy)
    for _ in range(70):
        midpoint = (lower + upper) / 2
        if binary_entropy_at_log_probability(midpoint) < entropy:
            lower = midpoint
        else:
            upper = midpoint
    log_probability = (lower + upper) / 2
    probability = exp(log_probability)
    derivative = 2 * (probability * (1 - probability))**0.5 * (
        log1p(-probability) - log_probability
    )
    return (entropy / derivative)**2


def spectrum_check():
    mass, stiffness, wave_number, energy_cutoff = 0.25, 0.5, 0.8, 0.65
    for sites in (12, 24, 48):
        spacing = 2 * pi / (wave_number * sites)
        hopping = stiffness / spacing**2
        energies = [mass + 4 * hopping * sin(pi * index / sites)**2 for index in range(sites)]
        profile = [cos(2 * pi * index / sites) - 1 for index in range(sites)]
        # Apply the positive form of the three-dimensional Hamiltonian
        # to fields constant in the two transverse directions.
        image = [
            mass * value + hopping * (
                2 * value - profile[(index - 1) % sites] - profile[(index + 1) % sites]
            )
            for index, value in enumerate(profile)
        ]
        assert all(isclose(actual, energies[1] * cos(2 * pi * index / sites) - mass,
                           abs_tol=1e-12) for index, actual in enumerate(image))
        assert energies[0] < energies[1] < energy_cutoff
        print(f"sites={sites}: E(0)={energies[0]:.6f}, E(k)={energies[1]:.6f}")


def normalization_check():
    eta, reference_length = 1, 1
    target = eta / (6 * reference_length)
    errors = []
    for bond_length in (0.12, 0.08, 0.04, 0.02, 0.01):
        spacing = bond_length * exp(-reference_length / bond_length)
        directions = round((reference_length / bond_length)**2)
        entropy = 2 * eta * spacing**3 / (directions * bond_length)
        norm_density = directions * tangent_weight(entropy) / spacing**3
        errors.append(abs(norm_density - target))
        print(f"bond length={bond_length:.2f}: tangent norm density={norm_density:.8f}")
    assert all(right < left for left, right in zip(errors, errors[1:]))
    assert isclose(norm_density, target, rel_tol=0.1)


if __name__ == "__main__":
    spectrum_check()
    normalization_check()
    area, residual = cosine_profile_responses(0.05, 0.8)
    assert isclose(residual / area, -5, rel_tol=1e-4)
    print(f"Allowed profile: residual/(eta * area)={residual / area:.8f}")
