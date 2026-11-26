"""Differentiate curved heat traces using exact lattice operator insertions."""

import numpy as np
import torch
from torch.func import jvp
from scipy.sparse import bmat, csr_matrix
from scipy.sparse.linalg import expm_multiply

from curved_clock_heat_blocks import operators, heat_trace, spectra


def operator_jets(size, momentum, velocity, clock_axis=0, shear=False, project_zero=True,
                  harmonic=1, clock_correction_only=False, length_x=None, *, include_ghost=True):
    zero, direction = torch.tensor(0.), torch.tensor(1.)

    def matrices(amplitude):
        boson, ghost = operators(size, momentum, amplitude, velocity, clock_axis, shear, project_zero,
                                 harmonic, clock_correction_only, length_x, include_ghost=include_ghost)
        return boson.real, boson.imag, ghost

    def first_jet(amplitude):
        return jvp(matrices, (amplitude,), (direction,))

    (base, first), (_, second) = jvp(first_jet, (zero,), (direction,))
    jets = (base, first, second)
    boson = [real.numpy() + 1j * imag.numpy() for real, imag, _ in jets]
    ghost = [matrix.numpy() for _, _, matrix in jets]
    return boson, ghost


def insertion(size, momentum, velocity, times, clock_axis=0, shear=False):
    jets = operator_jets(size, momentum, velocity, clock_axis, shear)
    return np.array([second_trace(block, times) for block in jets])


def mixed_operator_jets(size, momentum, clock_axis, project_zero, length_x, harmonic):
    # The Hessian is exactly quadratic in the clock winding. Evaluation at
    # 0 and ±1 extracts its polynomial coefficients, without a step limit.
    neutral = np.asarray(operator_jets(
        size, momentum, 0., clock_axis, project_zero=project_zero, length_x=length_x,
        harmonic=harmonic, include_ghost=False)[0])
    correction = np.asarray(operator_jets(
        size, momentum, 1., clock_axis, project_zero=project_zero,
        clock_correction_only=True, length_x=length_x, harmonic=harmonic)[0])
    parity = np.where(np.arange(neutral.shape[-1]) % 11 == 10, -1, 1)
    reflected = parity[:, None] * correction * parity
    jets = np.stack((neutral, (correction - reflected) / 2, (correction + reflected) / 2), axis=1)
    jets[2] /= 2
    return jets


def longitudinal_fourier(jets, size):
    dimension = jets.shape[-1]
    phase = dimension // (11 * size)
    jets = jets.reshape(3, 3, phase, size, 11, phase, size, 11)
    jets = np.fft.ifft(jets, axis=-5, norm="ortho")
    return np.fft.fft(jets, axis=-2, norm="ortho").reshape(3, 3, dimension, dimension)


def mixed_insertion(size, momentum, times, clock_axis, factor_transverse=False, length_x=1.8, harmonic=1):
    jets = mixed_operator_jets(size, momentum, clock_axis, not factor_transverse, length_x, harmonic)
    projected_zero = not factor_transverse and not any(momentum)
    if factor_transverse:
        transverse_k2 = sum(component**2 for component in momentum) * (2 * np.pi / 1.8)**2
        jets[0, 0] -= transverse_k2 * np.eye(jets.shape[-1])
        # Curvature order j shifts longitudinal Fourier indices by at most
        # j multiples of the probe harmonic. Drop roundoff beyond that support.
        dimension = jets.shape[-1]
        phase = dimension // (11 * size)
        jets = longitudinal_fourier(jets, size)
        index = np.tile(np.repeat(np.arange(size), 11), phase)
    elif projected_zero:
        # Use the same mean-zero site basis as operators(), then express it
        # in the nonzero Fourier modes. The global projector is diagonal here.
        site_basis = torch.linalg.qr(torch.ones((size, 1)), mode="complete").Q[:, 1:].numpy()
        waves = np.fft.fft(np.eye(size), norm="ortho")[:, 1:]
        transform = np.kron(site_basis.T @ waves, np.eye(11))
        jets = transform.conj().T @ jets @ transform
        index = np.repeat(np.arange(1, size), 11)
    if factor_transverse or projected_zero:
        difference = (index[:, None] - index) % size
        for order in range(3):
            allowed = (np.arange(-order, order + 1) * harmonic) % size
            excluded = ~np.isin(difference, allowed)
            np.testing.assert_allclose(jets[order][:, excluded], 0, atol=1e-9)
            jets[order][:, excluded] = 0
        # The trace closes in momentum. At curvature order two a closed
        # path visits only k and the two modes shifted by one probe harmonic.
        result = np.zeros(np.size(times), dtype=complex)
        flat_times = np.asarray(times).ravel()
        for k in np.unique(index):
            center = index == k
            keep = np.isin((index - k) % size, [0, harmonic, size - harmonic])
            neighborhood = jets[:, :, keep, :][:, :, :, keep]
            base = neighborhood[0, 0]
            diagonal = np.diag_indices_from(base)
            offset = max(0., base[diagonal].real.min())
            base[diagonal] -= offset
            result += np.exp(-flat_times * offset) * jet_exponential_trace(neighborhood, times, center[keep])
    else:
        result = jet_exponential_trace(jets, times, np.ones(jets.shape[-1], dtype=bool))
    np.testing.assert_allclose(result.imag, 0, atol=1e-8)
    return result.real


def jet_exponential_trace(jets, times, center):
    degrees = [(w, v) for w in range(3) for v in range(3)]
    blocks = [[csr_matrix(jets[w-i, v-j]) if i <= w and j <= v else None
               for i, j in degrees] for w, v in degrees]
    generator = bmat(blocks, format="csr")
    dimension = len(center)
    initial = np.zeros((9 * dimension, center.sum()), dtype=complex)
    initial[:dimension] = np.eye(dimension)[:, center]
    final_rows = np.flatnonzero(center) + 8 * dimension
    groups = np.asarray(times)
    if groups.ndim == 1:
        groups = groups[None, :]
    return np.concatenate([trace_time_grid(generator, initial, final_rows, group)
                           for group in groups])


def trace_time_grid(generator, initial, final_rows, times):
    times = np.asarray(times)
    distinct = np.unique(times)
    step = np.diff(distinct).min() if len(distinct) > 1 else 0
    offsets = (times - times.min()) / step if step else np.zeros_like(times)
    indices = np.rint(offsets).astype(int)
    if step and np.allclose(offsets, indices, atol=1e-10, rtol=0):
        evolved = expm_multiply(-generator, initial, start=times.min(), stop=times.max(),
                                num=indices.max() + 1)
        return 4 * np.trace(evolved[indices][:, final_rows], axis1=-2, axis2=-1)
    return 4 * np.array([np.trace(expm_multiply(-s * generator, initial)[final_rows])
                         for s in times])



def second_trace(block, times):
    base, first, second = block
    if np.allclose(base, base.conj().T, atol=1e-12):
        eigenvalues, modes = np.linalg.eigh(base)
        inverse = modes.conj().T
    else:
        eigenvalues, modes = np.linalg.eig(base)
        inverse = np.linalg.inv(modes)
    first = inverse @ first @ modes
    second = np.diag(inverse @ second @ modes)
    left, right = eigenvalues[:, None], eigenvalues[None, :]
    difference = left - right
    result = []
    for s in times:
        heat = np.exp(-s * eigenvalues)
        heat_left, heat_right = heat[:, None], heat[None, :]
        coalescent = np.abs(s * difference) < 1e-8
        divided = np.divide(heat_right - heat_left, s * difference,
                            out=(heat_left + heat_right) / 2, where=~coalescent)
        result.append(-s * (heat @ second) + s**2 * np.sum(divided * first * first.T))
    result = np.asarray(result)
    np.testing.assert_allclose(result.imag, 0, atol=1e-8)
    return result.real


def main():
    times = np.array([0.035, 0.07, 0.14])
    for shear, clock_axis, velocity in ((False, 0, 0.), (True, 0, 0.),
                                         (False, 0, 0.3), (False, 1, 0.3)):
        curves = []
        for n in (9, 13, 17):
            derivative = insertion(n, (0, 0, 0, 0), velocity, times, clock_axis, shear)
            curves.append(derivative)
            print(f"N={n} shear={shear} axis={clock_axis} v={velocity}: {derivative[:, 1]}", flush=True)
        np.testing.assert_allclose(curves[-2], curves[-1], rtol=0.02, atol=2e-4)
        amplitude = 2e-4
        samples = [heat_trace(spectra(9, (0, 0, 0, 0), b, velocity, clock_axis, shear), times)
                   for b in (-amplitude, 0, amplitude)]
        np.testing.assert_allclose((samples[0] + samples[2] - 2 * samples[1]) / amplitude**2,
                                   curves[0], rtol=2e-5, atol=2e-5)


def mixed_resolution():
    # A sine/cosine pair already counts the two signs of a transverse mode.
    times = np.array([0.035, 0.07])
    for axis in (0, 1):
        for n in (5, 9, 13):
            value = mixed_insertion(n, (0, 0, 0, 0), times, axis)
            print(f"Mixed axis={axis} N={n}: {value}", flush=True)
        temporal = mixed_insertion(9, (1, 0, 0, 0), times, axis)
        spatial = temporal if axis == 1 else mixed_insertion(9, (0, 0, 1, 0), times, axis)
        print(f"Mixed axis={axis} first axial transverse shell: {temporal + 2 * spatial}",
              flush=True)


if __name__ == "__main__":
    main()
    mixed_resolution()
