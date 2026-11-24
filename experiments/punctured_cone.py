"""Check the punctured replica cone's most slowly converging angular mode."""

from math import exp, isclose, log

EULER_GAMMA = 0.5772156649015329


def radial_zero_mode(x):
    """Return I0, K0 and their derivatives using convergent small-x series."""
    i0 = 1.0
    xi0_prime = 0.0
    series = xseries_prime = harmonic = 0.0
    term = 1.0
    for order in range(1, 20):
        term *= (x / 2)**2 / order**2
        harmonic += 1 / order
        i0 += term
        xi0_prime += 2 * order * term
        series += harmonic * term
        xseries_prime += 2 * order * harmonic * term
    factor = log(x / 2) + EULER_GAMMA
    return i0, -factor * i0 + series, xi0_prime, -i0 - factor * xi0_prime + xseries_prime


def main():
    momentum = 3.0
    tip_length = 1.0
    pole = 2 * exp(-EULER_GAMMA) / tip_length
    expected = 1 / log(momentum / pole)
    samples = []
    for radius in (1e-2, 1e-4, 1e-6):
        i0, k0, di0, dk0 = radial_zero_mode(momentum * radius)
        dirichlet = -i0 / k0
        neumann = -di0 / dk0
        robin = 1 / log(radius / tip_length)
        retained = (robin * i0 - di0) / (dk0 - robin * k0)
        samples.append((abs(dirichlet), abs(neumann), abs(retained - expected)))
        print(f"a={radius:.0e}: Dirichlet={dirichlet:+.8f}, "
              f"Neumann={neumann:+.3e}, retained tip={retained:+.8f}")
    assert all(later < earlier for earlier, later in zip(samples[0], samples[-1]))
    assert isclose(retained, expected, rel_tol=1e-8)
    assert pole < momentum
    print(f"Noncanonical tip pole: {pole:.8f}; surviving resolvent coefficient: {expected:.8f}.")


if __name__ == "__main__":
    main()
