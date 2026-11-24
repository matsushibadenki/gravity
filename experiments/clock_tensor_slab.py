"""Compute shell-only and joint slab entropies for a local tensor lattice."""

import numpy as np


def tensor_basis():
    basis = np.zeros((5, 3, 3))
    basis[0] = np.diag([1, -1, 0]) / np.sqrt(2)
    basis[1] = np.diag([1, 1, -2]) / np.sqrt(6)
    for index, (i, j) in enumerate(((0, 1), (0, 2), (1, 2)), start=2):
        basis[index, i, j] = basis[index, j, i] = 1 / np.sqrt(2)
    return basis


def covariance_symbols(shape, spacing, gap, coupling, stencil="centered"):
    angles = np.stack(np.meshgrid(*(2 * np.pi * np.fft.fftfreq(n) for n in shape),
                                  indexing="ij"), axis=-1)
    laplacian = np.sum(4 * np.sin(angles / 2)**2, axis=-1) / spacing**2
    derivative = np.sin(angles) / spacing
    if stencil == "improved":
        derivative *= (4 - np.cos(angles)) / 3
    elif stencil != "centered":
        raise ValueError(f"Unknown derivative stencil: {stencil}")
    mixing = coupling * np.einsum("...i,aij,...j->...a", derivative, tensor_basis(), derivative)
    stiffness = np.zeros((*shape, 6, 6))
    stiffness[..., :5, :5] = (1 + laplacian)[..., None, None] * np.eye(5)
    stiffness[..., 5, 5] = gap**2 + laplacian
    stiffness[..., :5, 5] = stiffness[..., 5, :5] = mixing
    values, vectors = np.linalg.eigh(stiffness)
    assert np.min(values) > 0
    frequencies = np.sqrt(values)
    position = (vectors / (2 * frequencies[..., None, :])) @ vectors.swapaxes(-1, -2)
    momentum = (vectors * (frequencies[..., None, :] / 2)) @ vectors.swapaxes(-1, -2)
    return position, momentum


def oscillator_entropy(symplectic):
    assert np.min(symplectic) > 0.5 - 1e-8
    occupation = np.maximum(symplectic - 0.5, 0)
    active = occupation[occupation > 1e-14]
    return np.sum((active + 1) * np.log1p(active) - active * np.log(active))


def regional_covariance(symbol, sites, components):
    kernel = np.fft.ifft(symbol[:, :components, :components], axis=0)
    blocks = kernel[(sites[:, None] - sites[None, :]) % len(kernel)]
    size = len(sites) * components
    return blocks.transpose(0, 2, 1, 3).reshape(size, size)


def regional_entropy(position, momentum, sites, components):
    position = regional_covariance(position, sites, components)
    momentum = regional_covariance(momentum, sites, components)
    values, vectors = np.linalg.eigh(position)
    root = (vectors * np.sqrt(values)) @ vectors.conj().T
    return oscillator_entropy(np.sqrt(np.linalg.eigvalsh(root @ momentum @ root)))


def slab_entropy(position, momentum, width, components):
    return regional_entropy(position, momentum, np.arange(width), components)


def measure(shape, spacing, gap, coupling):
    nx, ny, nz = shape
    position, momentum = covariance_symbols(shape, spacing, gap, coupling)
    whole_shell = oscillator_entropy(
        np.sqrt(np.sum(position[..., :5, 5] * -momentum[..., :5, 5], axis=-1) + 0.25)
    )
    shell = joint = 0.0
    for ky in range(ny):
        for kz in range(nz):
            x, p = position[:, ky, kz], momentum[:, ky, kz]
            shell += slab_entropy(x, p, nx // 2, 5)
            joint += slab_entropy(x, p, nx // 2, 6)
    interface_sites = 2 * ny * nz
    return (shell - whole_shell / 2) / interface_sites, joint / interface_sites, whole_shell


def main():
    coupling = 0.45 * np.sqrt(3 / 2)
    for spacing in (0.4, 0.2, 0.1):
        shape = (16, 8, 8)
        fixed = measure(shape, spacing, 2, coupling)
        high = measure(shape, spacing, 100 / spacing, coupling)
        reference = measure(shape, spacing, 100 / spacing, 0)
        assert fixed[1] >= fixed[0] > 0
        assert abs(high[0] - reference[0]) < 1e-3
        print(f"a={spacing:.2f}: fixed shell={fixed[0]:.7f}, fixed joint={fixed[1]:.7f}, "
              f"large gap shell={high[0]:.7f}, uncoupled shell={reference[0]:.7f}")
    for spacing, shape in ((0.4, (8, 4, 4)), (0.2, (16, 8, 8)), (0.1, (32, 16, 16))):
        shell, joint, _ = measure(shape, spacing, 2, coupling)
        print(f"fixed physical box a={spacing:.2f}: shell={shell:.7f}, joint={joint:.7f}, "
              f"shell/physical area={shell/spacing**2:.5f}, joint/physical area={joint/spacing**2:.5f}")
    for shape in ((16, 6, 6), (24, 8, 8), (24, 10, 10)):
        shell, joint, bulk = measure(shape, 0.2, 2, coupling)
        print(f"shape={shape}: shell/interface site={shell:.7f}, "
              f"joint/interface site={joint:.7f}, shell bulk/site={bulk/np.prod(shape):.7f}")


if __name__ == "__main__":
    main()
