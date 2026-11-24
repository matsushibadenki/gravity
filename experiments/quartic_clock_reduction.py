"""Reduce the scalar ADM action through fourth order on a periodic lattice."""

from math import factorial, pi

import numpy as np
import torch

from evolving_clock_transfer import scalar_cubic_hessian, phase_hamiltonian
from reduced_clock_ball_seam import spectral_operators
from reduced_clock_transfer import symplectic_form

torch.set_default_dtype(torch.float64)
torch.set_num_threads(1)


class ADMReduction:
    def __init__(self, size, spacing, hubble=0.3):
        sites, gradients, laplacian, inverse = spectral_operators(size, spacing)
        self.sites, self.spacing, self.hubble = sites, spacing, hubble
        self.cell, self.count = spacing**3, len(sites)
        self.gradients, self.laplacian, self.inverse = map(torch.as_tensor, (
            np.array(gradients), laplacian, inverse
        ))
        self.identity = torch.eye(3)
        self.projector = torch.eye(self.count) - 1 / self.count
        q = torch.zeros(2 * self.count)
        auxiliary = torch.zeros(4 * self.count)
        stiffness = torch.func.hessian(lambda b: self.action(q, b, 2))(auxiliary)
        spectrum, basis = torch.linalg.eigh(stiffness)
        keep = spectrum.abs() > 1e-8 * spectrum.abs().max()
        assert int(keep.sum()) == 4 * (self.count - 1)
        self.auxiliary_hessian = stiffness
        self.auxiliary_inverse = (basis[:, keep] / spectrum[keep]) @ basis[:, keep].T
        self.source = torch.func.grad(lambda q, b: self.action(q, b, 3), argnums=1)

    @staticmethod
    def prefactor(z, lapse, power, order):
        return sum((power * z)**j / factorial(j) * (-lapse)**(order-j) for j in range(order+1))

    def action(self, q, auxiliary, order):
        """Coefficient of perturbation degree 'order' before reduction, in A units."""
        z, dz = q.reshape(2, self.count)
        lapse, *shift = auxiliary.reshape(4, self.count)
        shift = torch.stack(shift, dim=1)
        gradient = (self.gradients @ z).T
        lap = self.laplacian @ z
        derivative = torch.einsum("ixy,yj->xij", self.gradients, shift)
        d = (derivative + derivative.transpose(-1, -2)) / 2
        connection = (gradient[:, :, None] * shift[:, None, :] + shift[:, :, None] * gradient[:, None, :]
                      - (gradient * shift).sum(dim=1)[:, None, None] * self.identity)
        d_tr = d.diagonal(dim1=-1, dim2=-2).sum(dim=-1)
        c_tr = connection.diagonal(dim1=-1, dim2=-2).sum(dim=-1)

        def conformal_factor(n):
            return z**n / factorial(n) + (lapse * z**(n-1) / factorial(n-1) if n else 0)

        curvature = -4 * lap * conformal_factor(order - 1)
        curvature -= 2 * gradient.square().sum(dim=1) * conformal_factor(order - 2)
        result = curvature
        groups = (
            (3, (-12 * self.hubble * dz, -6 * dz**2)),
            (1, (4 * self.hubble * d_tr, 4 * (dz * d_tr - self.hubble * c_tr), -4 * dz * c_tr)),
            (-1, (None, (d * d).sum(dim=(1, 2)) - d_tr**2,
                   -2 * ((d * connection).sum(dim=(1, 2)) - d_tr * c_tr),
                   connection.square().sum(dim=(1, 2)) - c_tr**2)),
        )
        for power, terms in groups:
            for degree, term in enumerate(terms, start=1):
                if term is not None and degree <= order:
                    result = result + term * self.prefactor(z, lapse, power, order - degree)
        return self.cell * result.sum()

    def first_auxiliary(self, q):
        z, dz = q.reshape(2, self.count)
        psi = -z / self.hubble + 3 * self.inverse @ dz
        return torch.cat((dz / self.hubble, (self.gradients @ psi).reshape(-1)))

    def projected_source(self, q, auxiliary):
        return (self.source(q, auxiliary).reshape(4, self.count) @ self.projector).flatten()

    def reduced(self, q, order):
        q = (q.reshape(2, self.count) @ self.projector).flatten()
        auxiliary = self.first_auxiliary(q)
        value = self.action(q, auxiliary, order)
        if order == 4:
            source = self.projected_source(q, auxiliary)
            value -= source @ self.auxiliary_inverse @ source / 2
        return value

    def constraint_check(self, field):
        aux1 = self.first_auxiliary(field)
        first = torch.func.grad(lambda b: self.action(field, b, 2))(aux1)
        assert torch.linalg.vector_norm((first.reshape(4, self.count) @ self.projector)) < 1e-10
        source = self.projected_source(field, aux1)
        aux2 = -self.auxiliary_inverse @ source
        assert torch.linalg.vector_norm(self.auxiliary_hessian @ aux2 + source) < 1e-10
        assert torch.linalg.vector_norm(aux2) > 0
        return torch.linalg.vector_norm(aux2).item()


def smooth_band(energy, lower=0.02, upper=0.04):
    values, modes = np.linalg.eigh(energy)
    assert min(values) > 0
    root = (modes * np.sqrt(values)) @ modes.T
    spectrum = np.linalg.eigvalsh(1j * root @ symplectic_form(len(energy) // 2) @ root)
    rank = len(spectrum) // 2
    nodes, weights = np.polynomial.legendre.leggauss(24)
    half = (upper - lower) / 2
    times = lower + (nodes + 1) * half
    trace = np.exp(-times[:, None] * spectrum[rank:]**2).sum(axis=1) / np.sqrt(4 * pi * times)
    return -0.5 * half * np.dot(weights, trace / times)


def run(size, direction=(0, 0, 1), fixed_expansion=False):
    spacing = 1.8 / size
    model = ADMReduction(size, spacing)
    n = model.count
    laplacian = model.laplacian.numpy()
    profile = np.cos(2 * pi * (model.sites @ np.array(direction)) / size)
    profile_dot = laplacian @ profile / (3 * model.hubble) if fixed_expansion else np.zeros(n)
    field = torch.as_tensor(np.r_[profile, profile_dot])
    if fixed_expansion:
        first_shift = -profile / model.hubble + 3 * model.inverse.numpy() @ profile_dot
        assert np.linalg.norm(first_shift) < 1e-10
        assert np.linalg.norm(laplacian @ profile) > 0
        print("Clock data: nonzero intrinsic curvature with zero linear extrinsic perturbation.", flush=True)
    print(f"a={spacing:.3f}, direction={direction}: quadratic constraint correction norm={model.constraint_check(field):.7f}", flush=True)
    first = torch.func.hessian(lambda q: model.reduced(q, 3))(field).numpy()
    second = 2 * torch.func.hessian(lambda q: model.reduced(q, 4))(field).numpy()
    expected = scalar_cubic_hessian(profile, profile_dot, 1, 0.3, model.gradients.numpy(),
                                     laplacian, model.inverse.numpy(), model.cell)
    assert np.allclose(first, expected, atol=1e-9)
    m0 = 12 * model.cell
    m1, m2 = first[n:, n:] / m0, second[n:, n:] / m0
    measure = np.trace(m2 - m1 @ m1) / 2
    step_measure = 1e-6
    log_determinants = [np.linalg.slogdet(np.eye(n) + sign * step_measure * m1
                          + step_measure**2 * m2 / 2)[1] for sign in (-1, 1)]
    assert np.isclose(sum(log_determinants) / (2 * step_measure**2), measure, rtol=1e-6)
    print(f"a={spacing:.3f}: d^2 log canonical measure={measure:+.9f}", flush=True)

    def action(amplitude, include_quartic):
        change = amplitude * first + (amplitude**2 * second / 2 if include_quartic else 0)
        mass = m0 * np.eye(n) + change[n:, n:]
        potential = m0 * (-laplacian + np.ones_like(laplacian) / n) - change[:n, :n]
        return smooth_band(phase_hamiltonian(mass, potential, change[n:, :n]))

    step = 1e-6 if fixed_expansion else 3e-6
    baseline = action(0, True)
    for include_quartic in (False, True):
        response = (action(step, include_quartic) + action(-step, include_quartic)
                    - 2 * baseline) / step**2
        half = step / 2
        refined = (action(half, include_quartic) + action(-half, include_quartic)
                   - 2 * baseline) / half**2
        assert np.isclose(response, refined, rtol=1e-4), (response, refined)
        print(f"  quartic={include_quartic}: smooth second action variation={response:+.9f}", flush=True)


if __name__ == "__main__":
    run(3)
    run(5)
    run(5, (0, 1, 1))
    run(5, fixed_expansion=True)
