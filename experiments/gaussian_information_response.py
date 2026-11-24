"""Evaluate Gaussian slab information directly at quadratic order."""

from math import log, sqrt

import numpy as np

from clock_tensor_slab import gaussian_entropy, tensor_basis
from infinite_slab_information import covariance_matrix
from slab_decay_scale import branch_scales
from transverse_slab_integral import focused_rule


def derivative(z):
    root = np.sqrt(z)
    return np.arctanh(0.5 / root) / root


class QuadraticResponse:
    """Entropy Hessian at two identical, uncorrelated Gaussian marginals."""

    def __init__(self, position, momentum, minimum_margin=None):
        self.position, self.momentum = position, momentum
        eigenvalues, vectors = np.linalg.eigh(position)
        root = (vectors * np.sqrt(eigenvalues)) @ vectors.conj().T
        spectrum, modes = np.linalg.eigh(root @ momentum @ root)
        self.floor = float(np.min(spectrum - 0.25))
        if minimum_margin is not None:
            adjusted = np.maximum(spectrum, 0.25 + minimum_margin)
            if np.any(adjusted != spectrum):
                scaled_modes = np.linalg.solve(root, modes)
                self.momentum = momentum + (
                    scaled_modes * (adjusted - spectrum)
                ) @ scaled_modes.conj().T
                spectrum = adjusted
        elif self.floor <= 0:
            raise ArithmeticError(f"Marginal spectrum reached the pure-state boundary: {self.floor}")
        self.forward = root @ modes
        self.inverse = np.linalg.solve(self.forward, np.eye(len(position)))
        self.first = derivative(spectrum)
        delta = spectrum[:, None] - spectrum[None, :]
        close = np.abs(delta) < 1e-7 * np.minimum(
            spectrum[:, None] - 0.25, spectrum[None, :] - 0.25
        )
        mean = (spectrum[:, None] + spectrum[None, :]) / 2
        divided = np.empty_like(delta)
        np.divide(self.first[:, None] - self.first[None, :], delta,
                  out=divided, where=~close)
        divided[close] = -derivative(mean[close]) / (2 * mean[close]) - 1 / (
            mean[close] * (4 * mean[close] - 1)
        )
        self.divided = divided

    def information(self, x, p):
        adjoint = lambda matrix: matrix.conj().T
        upper = self.inverse @ (self.position @ p + x @ self.momentum) @ self.forward
        lower = self.inverse @ (self.position @ adjoint(p) + adjoint(x) @ self.momentum) @ self.forward
        diagonal = self.inverse @ (x @ adjoint(p) + adjoint(x) @ p) @ self.forward
        return float(-np.real(self.first @ np.diag(diagonal)
                              + np.sum(self.divided * upper * lower.T)))


def cross_block(kernel, sites, shift, components):
    offsets = sites[:, None] - sites[None, :] - shift + len(kernel) // 2
    blocks = kernel[offsets, :components, :components]
    size = len(sites) * components
    return blocks.transpose(0, 2, 1, 3).reshape(size, size)


def analytic_symbols(spacing, normal, ky, kz, coupling):
    angles = np.stack(np.meshgrid(normal, kz, indexing="ij"), axis=-1)
    angles = np.stack((angles[..., 0], np.full_like(angles[..., 0], ky), angles[..., 1]), axis=-1)
    laplacian = np.sum(4 * np.sin(angles / 2)**2, axis=-1) / spacing**2
    d = np.sin(angles) * (4 - np.cos(angles)) / (3 * spacing)
    mixing = coupling * np.einsum("...i,aij,...j->...a", d, tensor_basis(), d)
    mixed_square = np.sum(mixing**2, axis=-1)
    shell, clock = 1 + laplacian, 4 + laplacian
    determinant_root = np.sqrt(shell * clock - mixed_square)
    denominator = np.sqrt(shell + clock + 2 * determinant_root)
    mixed_outer = mixing[..., :, None] * mixing[..., None, :]
    symbols = []
    # Exact square root and inverse square root on the analytic 2x2 block.
    for free, entry, clock_entry, off in (
        (1 / np.sqrt(shell), (clock + determinant_root) / (determinant_root * denominator),
         (shell + determinant_root) / (determinant_root * denominator),
         -1 / (determinant_root * denominator)),
        (np.sqrt(shell), (shell + determinant_root) / denominator,
         (clock + determinant_root) / denominator, 1 / denominator),
    ):
        correction = np.divide(entry - free, mixed_square, out=np.zeros_like(entry),
                               where=np.abs(mixed_square) > 1e-24)
        symbol = np.zeros((*shell.shape, 6, 6), dtype=complex)
        symbol[..., :5, :5] = free[..., None, None] * np.eye(5) + correction[..., None, None] * mixed_outer
        symbol[..., 5, :5] = symbol[..., :5, 5] = off[..., None] * mixing
        symbol[..., 5, 5] = clock_entry
        symbols.append(symbol / 2)
    return symbols


def kernels_for(spacing, normal_points, lags, ky, kz, coupling, contour_height=0.8):
    # Evaluate positive lags on a horizontal contour inside the light-mode
    # strip. Negative lags are adjoints and need no second integration.
    normal = 2 * np.pi * np.fft.fftfreq(normal_points) + 1j * contour_height * spacing
    lags_positive = np.arange(lags + 1)
    transform = np.exp(1j * lags_positive[:, None] * normal) / normal_points
    kernels = [np.einsum("lk,kzij->lzij", transform, symbol, optimize=True)
               for symbol in analytic_symbols(spacing, normal, ky, kz, coupling)]
    return [np.concatenate((kernel[:0:-1].swapaxes(-1, -2).conj(), kernel))
            for kernel in kernels]


def response_for(kernels, sites, shifts, components, exact=False, minimum_margin=None):
    marginals = [covariance_matrix(kernel, sites, components) for kernel in kernels]
    response = QuadraticResponse(*marginals, minimum_margin=minimum_margin)
    values = []
    for shift in shifts:
        cross = [cross_block(kernel, sites, shift, components) for kernel in kernels]
        result = response.information(*cross)
        if exact:
            direct = np.nan
            if not values:
                joint = [np.block([[local, off], [off.conj().T, local]])
                         for local, off in zip(marginals, cross)]
                direct = 2 * gaussian_entropy(*marginals) - gaussian_entropy(*joint)
            result = (result, direct)
        values.append(result)
    return np.array(values), response.floor


def zero_transverse(spacing, gaps, normal_points=1024, contour_height=0.8):
    sites = np.arange(round(0.6 / spacing))
    shifts = len(sites) + np.rint(gaps / spacing).astype(int)
    kernels = [kernel[:, 0] for kernel in kernels_for(
        spacing, normal_points, shifts[-1] + len(sites) - 1, 0, np.array([0.0]),
        0.45 * sqrt(3 / 2), contour_height
    )]
    parallel = np.r_[sqrt(3 / 2) * tensor_basis()[:, 0, 0], 0]
    clock = np.eye(6)[5]
    spectator = np.eye(6)[4]

    def projected(directions):
        directions = np.array(directions)
        return [directions @ kernel @ directions.T for kernel in kernels]

    results = []
    for directions in ([parallel], [parallel, clock], [spectator]):
        values, _ = response_for(projected(directions), sites, shifts, len(directions), exact=True)
        results.append(values)
    return results


def integrated(spacing, gaps, normal_points, transverse_points, minimum_margin):
    sites = np.arange(round(0.6 / spacing))
    shifts = len(sites) + np.rint(gaps / spacing).astype(int)
    lags = shifts[-1] + len(sites) - 1
    (angles, _), (weights, _) = focused_rule(transverse_points)
    values = np.zeros((len(gaps), 2))
    floor = float("inf")
    # The quadrature is symmetric under simultaneous transverse reflection;
    # keep the full domain for a transparent comparison with the exact code.
    for ky, wy in zip(angles, weights):
        kernels = kernels_for(spacing, normal_points, lags, ky, angles, 0.45 * sqrt(3 / 2))
        for j, wz in enumerate(weights):
            for sector, components in enumerate((5, 6)):
                data, margin = response_for([kernel[:, j] for kernel in kernels],
                                            sites, shifts, components, minimum_margin=minimum_margin)
                values[:, sector] += wy * wz * data
                floor = min(floor, margin)
    assert np.all(values > 0)
    return values / spacing**2, floor


def integrated_spectators(spacing, gaps, normal_points, transverse_points):
    sites = np.arange(round(0.6 / spacing))
    shifts = len(sites) + np.rint(gaps / spacing).astype(int)
    lags = shifts[-1] + len(sites) - 1
    normal = 2 * np.pi * np.fft.fftfreq(normal_points) + 0.8j * spacing
    transform = np.exp(1j * np.arange(lags + 1)[:, None] * normal) / normal_points
    (angles, _), (weights, _) = focused_rule(transverse_points)
    normal_squared = 4 * np.sin(normal / 2)**2 / spacing**2
    transverse_squared = 4 * np.sin(angles / 2)**2 / spacing**2
    total = np.zeros(len(gaps))
    for i, wy in enumerate(weights):
        frequencies = np.sqrt(1 + normal_squared[:, None] + transverse_squared[i] + transverse_squared)
        positives = [transform @ symbol / 2 for symbol in (1 / frequencies, frequencies)]
        kernels = [np.concatenate((data[:0:-1].conj(), data)) for data in positives]
        for j, wz in enumerate(weights):
            data, _ = response_for([kernel[:, j, None, None] for kernel in kernels],
                                   sites, shifts, 1, minimum_margin=1e-12)
            total += wy * wz * data
    # For any transverse momentum, two fixed tensor directions are
    # orthogonal to the entire normal-momentum-dependent mixing span.
    return 2 * total / spacing**2


def rates(values, gaps, power):
    return (np.log(values[:-1] / values[1:]) - power * np.log(gaps[1:] / gaps[:-1])) / np.diff(gaps)


def main():
    gaps = np.arange(10, 61, 2) * 0.6
    for spacing in (0.15, 0.10):
        mixed, spectator = branch_scales(spacing, 0.45)
        print(f"a={spacing} predicted rates: mixed={2*mixed:.8f}, spectator={2*spectator:.8f}")
        data = zero_transverse(spacing, gaps)
        alternative = zero_transverse(spacing, gaps, contour_height=0.7)
        assert all(np.allclose(primary[:, 0] / other[:, 0], 1, rtol=1e-5)
                   for primary, other in zip(data, alternative))
        for label, entries in zip(("mixed shell", "mixed joint", "one spectator"), data):
            quadratic, exact = entries.T
            assert np.all(quadratic > 0)
            assert np.isclose(quadratic[0], exact[0], rtol=0.002)
            print(label, "rates (remove 1/d):", np.round(rates(quadratic, gaps, 1), 5))
        ratio = data[0][:, 0] / (4 * data[2][:, 0])
        print("mixed shell / four spectators:", np.round(ratio, 4), flush=True)

        sampled = np.array([3.6, 6.0, 9.6, 12.0, 18.0, 24.0, 30.0, 36.0])
        total, floor = integrated(spacing, sampled, 1024, 48, 1e-12)
        comparison, _ = integrated(spacing, sampled, 896, 40, 1e-10)
        relative = np.max(np.abs(total / comparison - 1))
        assert relative < 0.05
        print("integrated minimum symplectic-square margin:", floor)
        print("joint refinement and symplectic regularization sensitivity:", relative)
        print("integrated information per area:\n", total)
        passive = integrated_spectators(spacing, sampled, 1024, 48)
        active = total - passive[:, None]
        assert np.all(active > 0)
        print("integrated spectator information per area:", passive)
        print("active shell fraction:", active[:, 0] / total[:, 0])
        print("active shell rates (remove 1/d^2):", rates(active[:, 0], sampled, 2))
        print("spectator rates (remove 1/d^2):", rates(passive, sampled, 2))
        print("shell integrated rates (remove 1/d^2):", rates(total[:, 0], sampled, 2))
        print("joint integrated rates (remove 1/d^2):", rates(total[:, 1], sampled, 2), flush=True)



if __name__ == "__main__":
    main()
