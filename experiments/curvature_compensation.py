"""Verify shell-entropy compensation within the static comparison model."""

from fractions import Fraction as F


def check_compensation():
    mass_squared = F(4)
    speed_squared = F(16, 25)
    shell_entropy_coupling = F(3, 25)

    # Coefficients multiply the same integrated normal-normal Ricci response.
    local_coefficient = shell_entropy_coupling / mass_squared
    for wave_number in (F(1, 2), F(1, 4), F(1, 8)):
        k2 = wave_number**2
        denominator = mass_squared + speed_squared * k2
        shell = -shell_entropy_coupling / denominator
        constant_residual = shell + local_coefficient
        assert constant_residual == (
            shell_entropy_coupling * speed_squared * k2 / (mass_squared * denominator)
        )
        derivative_coefficient = -shell_entropy_coupling * speed_squared / mass_squared**2
        two_term_residual = constant_residual + derivative_coefficient * k2
        assert two_term_residual == (
            -shell_entropy_coupling * speed_squared**2 * k2**2
            / (mass_squared**2 * denominator)
        )
        exact_response = shell_entropy_coupling / denominator
        assert shell + exact_response == 0
        print(f"k={float(wave_number):.3f}  local residual={float(constant_residual):.9f}  "
              f"two-term residual={float(two_term_residual):.9f}")

    # For a polynomial P, a nonzero leading coefficient cannot cancel after
    # multiplication by the massive denominator, whose degree is one in k^2.
    for coefficients in ([F(3, 100)], [F(3, 100), F(-3, 625)]):
        leading_product = speed_squared * coefficients[-1]
        assert leading_product != 0
    print("The full massive response cancels exactly; finite local truncations leave a residual.")


if __name__ == "__main__":
    check_compensation()
