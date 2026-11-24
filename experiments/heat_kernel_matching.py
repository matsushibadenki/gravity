"""Check proper-time matching of scalar area entropy and Newton renormalization."""

from math import exp, isclose, pi


def proper_time_integral(mass, cutoff, samples=40000):
    # Substitute y=cutoff**2/s to integrate on a bounded interval.
    scaled_mass = (mass * cutoff)**2
    return sum(exp(-scaled_mass / ((index + 0.5) / samples))
               for index in range(samples)) / (samples * cutoff**2)


def main():
    def cone_factor(replica_index):
        return (1 / replica_index - replica_index) / 12

    step = 1e-5
    cone_slope = (cone_factor(1 + step) - cone_factor(1 - step)) / (2 * step)
    assert isclose(cone_slope, -1 / 6, rel_tol=1e-9)
    for mass, cutoff in ((0.0, 0.2), (0.7, 0.2), (1.4, 0.1)):
        integral = proper_time_integral(mass, cutoff)
        entropy_density = -cone_slope * integral / (8 * pi)
        for coupling in (0.0, 1 / 12, 1 / 6):
            delta_newton_inverse = (1 / 6 - coupling) * integral / (2 * pi)
            coincidence = integral / (16 * pi**2)
            contact = -2 * pi * coupling * coincidence
            assert isclose(entropy_density + contact, delta_newton_inverse / 4,
                           rel_tol=1e-9, abs_tol=1e-10)
        print(f"M={mass:.1f}, cutoff={cutoff:.1f}: minimal area density={entropy_density:.9f}")
    print("The nonminimal contact term restores the same-regulator equality.")


if __name__ == "__main__":
    main()
