"""Check the velocity block of the inhomogeneous reduced clock Hessian."""

import numpy as np


def velocity_form(background_amplitude, hubble, f, gradient, hessian, w, shift, shift_derivative):
    """ADM velocity form, with auxiliaries substituted at homogeneous order."""
    eps = background_amplitude
    scale = np.exp(-2 * eps * f)
    identity = np.eye(3)
    lap_f = np.trace(hessian, axis1=-2, axis2=-1)
    gradient_sq = np.sum(gradient**2, axis=-1)
    grad_shift = np.sum(gradient * shift, axis=-1)
    connection = (
        gradient[..., :, None] * shift[..., None, :]
        + shift[..., :, None] * gradient[..., None, :]
        - grad_shift[..., None, None] * identity
    )
    e = w[..., None, None] * identity - scale[..., None, None] * (shift_derivative - eps * connection)
    trace_e = np.trace(e, axis1=-2, axis2=-1)
    # The background shift is -eps*df/H. Terms nonlinear in eps do not
    # affect the first derivative but retain the spatial covariant form.
    f_connection = 2 * gradient[..., :, None] * gradient[..., None, :] - gradient_sq[..., None, None] * identity
    expansion = hubble * identity + eps / hubble * scale[..., None, None] * (hessian - eps * f_connection)
    expansion -= np.trace(expansion, axis1=-2, axis2=-1)[..., None, None] * identity
    intrinsic = scale * (-4 * eps * lap_f - 2 * eps**2 * gradient_sq)
    lapse = w / hubble
    terms = intrinsic * lapse**2 - 2 * lapse * np.sum(expansion * e, axis=(-1, -2))
    terms += np.sum(e * e, axis=(-1, -2)) - trace_e**2
    return np.mean(np.exp(3 * eps * f) * terms)


def kinetic_check():
    angle = np.arange(32) * (2 * np.pi / 32)
    x, z = np.meshgrid(angle, angle, indexing="ij")
    f = np.cos(z)
    gradient = np.stack((np.zeros_like(x), np.zeros_like(x), -np.sin(z)), axis=-1)
    hessian = np.zeros((*x.shape, 3, 3))
    hessian[..., 2, 2] = -np.cos(z)
    w = np.cos(x) * (1 + np.cos(z))
    # s_i = 3*d_i*inverse_Laplacian(w) at a=1 in the stiff background.
    shift = np.stack((3 * np.sin(x) * (1 + np.cos(z) / 2),
                      np.zeros_like(x), 1.5 * np.cos(x) * np.sin(z)), axis=-1)
    derivative = np.zeros_like(hessian)
    derivative[..., 0, 0] = 3 * np.cos(x) * (1 + np.cos(z) / 2)
    derivative[..., 0, 2] = derivative[..., 2, 0] = -1.5 * np.sin(x) * np.sin(z)
    derivative[..., 2, 2] = 1.5 * np.cos(x) * np.cos(z)
    arguments = (0.3, f, gradient, hessian, w, shift, derivative)
    assert np.isclose(velocity_form(0, *arguments), 6 * np.mean(w**2))

    first = (velocity_form(1e-5, *arguments) - velocity_form(-1e-5, *arguments)) / 2e-5
    second = (velocity_form(1e-6, *arguments) - velocity_form(-1e-6, *arguments)) / 2e-6
    minimal = 18 * np.mean(f * w**2)
    assert np.isclose(first, second, rtol=1e-7)
    assert not np.isclose(first, minimal)
    print(f"ADM kinetic response: {first:.9f}; minimal scalar response: {minimal:.9f}.")


def measure_check():
    # The time-discretized configuration action has inverse-mass Gaussian
    # momentum integration; the normalized determinant retains its factor.
    mass = np.array([[2.0, 0.3], [0.3, 1.5]])
    stiffness = np.array([[5.0, 0.6], [0.6, 4.0]])
    values, vectors = np.linalg.eigh(mass)
    inverse_root = (vectors / np.sqrt(values)) @ vectors.T
    normalized = inverse_root @ stiffness @ inverse_root
    assert np.isclose(np.linalg.det(normalized),
                      np.linalg.det(stiffness) / np.linalg.det(mass))
    print("Canonical Gaussian measure: det(D) = det(O) / det(M).")


if __name__ == "__main__":
    kinetic_check()
    measure_check()
