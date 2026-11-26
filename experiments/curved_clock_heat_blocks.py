"""Resolve the curved Gaussian contour in selected transverse Fourier sectors."""

import numpy as np
import torch
from torch.func import hessian, jacfwd

from collections import Counter
from itertools import product

from curved_clock_ward_4d import FourDimensionalWard
from clock_gradient_heat import vertices


class FourierBlock(FourDimensionalWard):
    def __init__(self, size, momentum, length=1.8, length_x=None):
        super().__init__(size, length if length_x is None else length_x)
        self.momentum = torch.tensor(momentum) * (2 * torch.pi / length)

    def derivative(self, field, axis):
        if axis == 1:
            return super().derivative(field, axis)
        if field.shape[0] == 1:
            return torch.zeros_like(field)
        wave = torch.tensor([0., 1., -1.]).reshape((3,) + (1,) * (field.ndim - 1))
        return torch.fft.ifft(1j * self.momentum[axis] * wave
                              * torch.fft.fft(field, dim=0), dim=0).real


def operators(size, momentum, amplitude, velocity, clock_axis=0, shear=False,
              project_zero=True, harmonic=1, clock_correction_only=False, length_x=None,
              *, include_ghost=True):
    model = FourierBlock(size, momentum, length_x=length_x)
    zero_sector = not any(momentum) and project_zero
    phase = torch.arange(1 if zero_sector else 3) * (2 * torch.pi / 3)
    phase_basis = (torch.ones((1, 1)) if zero_sector else
                   2**0.5 * torch.stack((phase.cos(), phase.sin()), dim=1))
    x = 2 * torch.pi * torch.arange(size) / size
    warp = amplitude * (harmonic * x).cos()[None, :, None, None]
    shape = (len(phase), size, 1, 1)
    exponents = warp[..., None] * (torch.tensor([0., 0., 1., -1.]) if shear else torch.ones(4))
    volume_half = (exponents.sum(dim=-1) / 2).exp()
    metric = torch.diag_embed((2 * exponents).exp()).expand(*shape, 4, 4)
    tensor_scale = (exponents[..., :, None] + exponents[..., None, :]).exp() / volume_half[..., None, None]
    vector_scale = (-exponents).exp() / volume_half[..., None]
    background = torch.cat((metric.flatten(-2), torch.zeros((*shape, 1))), dim=-1)
    winding = torch.eye(4)[clock_axis] * velocity
    gauge, inverse, density = model.de_donder(background)
    site_basis = torch.eye(size)
    ghost_basis = site_basis[..., None].expand(size, size, 4)
    if zero_sector:
        ghost_low = vector_scale.reciprocal().reshape(size, 4)
        direction = ghost_low.T / torch.linalg.vector_norm(ghost_low.T, dim=1, keepdim=True)
        direction = direction + torch.eye(size)[0]
        reflection = (torch.eye(size) - 2 * direction[..., :, None] * direction[..., None, :]
                      / direction.square().sum(dim=-1)[:, None, None])
        ghost_basis = reflection[..., 1:].permute(1, 2, 0)
        site_basis = torch.linalg.qr(torch.ones((size, 1)), mode="complete").Q[:, 1:]
    channels = torch.as_tensor(vertices()[0].reshape(10, 16))
    trace = torch.as_tensor(vertices()[1]) / 2
    nphase, nsite = len(phase_basis.T), len(site_basis.T)

    def interpolate(coefficients, basis=site_basis):
        field = torch.einsum("ap,xq,pqc->axc", phase_basis, basis, coefficients)
        return field[:, :, None, None]

    def boson_action(coefficients):
        field = interpolate(coefficients.reshape(nphase, nsite, 11))
        metric_fluctuation = ((2**0.5 * field[..., :10]) @ channels).unflatten(-1, (4, 4))
        metric_fluctuation = (tensor_scale * metric_fluctuation).flatten(-2)
        clock = field[..., 10] / volume_half
        perturbation = torch.cat((metric_fluctuation, clock[..., None]), dim=-1)
        if clock_correction_only:
            frame = (-exponents).exp()
            h = metric_fluctuation.unflatten(-1, (4, 4)) * frame[..., :, None] * frame[..., None, :]
            tr = h.diagonal(dim1=-2, dim2=-1).sum(dim=-1)
            background_clock = frame * winding
            clock_change = frame * model.gradient(clock)
            h_clock = torch.einsum("...ab,...b->...a", h, background_clock)
            density_term = background_clock.square().sum(dim=-1) * (
                tr.square() / 16 - h.square().sum(dim=(-1, -2)) / 8)
            clock_term = h_clock.square().sum(dim=-1) / 2
            clock_term -= tr * (h_clock * background_clock).sum(dim=-1) / 4
            mixed_term = ((tr[..., None] * background_clock / 2 - h_clock) * clock_change).sum(dim=-1)
            return size * (density * (density_term + clock_term + mixed_term)).mean()
        condition = gauge(perturbation)
        fixing = torch.einsum("...a,...ab,...b->...", condition, inverse, condition)
        return size * (model.action(background + perturbation, winding)
                       + (density * fixing).mean() / 2)

    def ghost_apply(coefficients):
        data = coefficients.reshape(nphase, nsite, 4)
        normalized = torch.einsum("ap,xqc,pqc->axc", phase_basis, ghost_basis, data)
        vector = vector_scale * normalized[:, :, None, None]
        covector = -gauge(model.orbit(background, vector, winding))
        vector_image = torch.einsum("...ab,...b->...a", inverse, covector)
        image = vector_image / vector_scale
        return (torch.einsum("ap,xqc,axc->pqc", phase_basis, ghost_basis,
                             image[:, :, 0, 0]) / len(phase)).flatten()

    boson = hessian(boson_action)(torch.zeros(nphase * nsite * 11))
    local_rotation = torch.eye(11, dtype=torch.complex128)
    local_rotation[:10, :10] += (1j - 1) * torch.outer(trace, trace)
    blocks = boson.to(torch.complex128).reshape(nphase * nsite, 11, nphase * nsite, 11)
    rotated = torch.einsum("ab,pbqc,cd->paqd", local_rotation.T, blocks, local_rotation).reshape(boson.shape)
    if clock_correction_only or not include_ghost:
        return rotated, torch.zeros((0, 0))
    ghost = jacfwd(ghost_apply)(torch.zeros(nphase * nsite * 4))
    return rotated, ghost


def spectra(size, momentum, amplitude, velocity, clock_axis=0, shear=False):
    rotated, ghost = (matrix.numpy() for matrix in
                      operators(size, momentum, amplitude, velocity, clock_axis, shear))
    assert np.linalg.eigvalsh(rotated.real).min() > 0
    modes = np.linalg.eigvals(rotated), np.linalg.eigvals(ghost)
    assert min(modes[1].real) > 0
    return modes


def heat_trace(modes, times):
    traces = np.array([np.exp(-times[:, None] * values).sum(axis=1) for values in modes])
    assert np.max(np.abs(traces.imag)) < 1e-9
    return traces.real


def main():
    times = np.array([0.025, 0.0375, 0.05])
    for momentum in ((0, 0, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0)):
        flat = heat_trace(spectra(9, momentum, 0, 0), times)
        wave = 2 * np.pi * np.fft.fftfreq(9, 1.8 / 9)
        if not any(momentum):
            wave = wave[1:]
        k2 = wave**2 + sum(component**2 for component in momentum) * (2 * np.pi / 1.8)**2
        expected = np.exp(-times[:, None] * k2).sum(axis=1) * (2 if any(momentum) else 1)
        np.testing.assert_allclose(flat, np.outer([11, 4], expected), atol=1e-8)
        for velocity in (0, 0.1):
            traces = []
            for size in (5, 9, 13, 17):
                trace = heat_trace(spectra(size, momentum, 0.015, velocity), times)
                traces.append(trace)
                print(f"p={momentum}, v={velocity:g}, N={size}: "
                      f"boson={trace[0, 1]:.9f}, ghost={trace[1, 1]:.9f}", flush=True)
            np.testing.assert_allclose(traces[-2], traces[-1], rtol=2e-5)


def summed_trace(size, transverse_cap, velocity, times, clock_axis=0, amplitude=0.015):
    indices = range(-transverse_cap, transverse_cap + 1)
    absolute = ((abs(t), abs(y), abs(z)) for t, y, z in product(indices, repeat=3))
    if clock_axis == 1:
        momenta = Counter(tuple(sorted(momentum)) for momentum in absolute)
    else:
        momenta = Counter((t, *sorted((y, z))) for t, y, z in absolute)
    total = np.zeros((2, len(times)))
    inner = np.zeros_like(total)
    for (t, y, z), count in momenta.items():
        momentum = (t, 0, y, z)
        modes = spectra(size, momentum, amplitude, velocity, clock_axis)
        contribution = count * heat_trace(modes, times) / (2 if any(momentum) else 1)
        total += contribution
        if max(t, y, z) < transverse_cap:
            inner += contribution
    return total, inner


def sum_check():
    times = np.array([0.07, 0.085, 0.10])
    for velocity in (0., 0.1):
        coarse, _ = summed_trace(9, 3, velocity, times)
        fine, inner = summed_trace(13, 3, velocity, times)
        np.testing.assert_allclose(coarse, fine, rtol=2e-5)
        np.testing.assert_allclose(fine, inner, rtol=0.008)
        print(f"Summed v={velocity:g}: boson={fine[0, 1]:.9f}, ghost={fine[1, 1]:.9f}, "
              f"x refinement={np.max(np.abs(coarse/fine-1)):.3e}, "
              f"last transverse shell={np.max(np.abs(inner/fine-1)):.3e}", flush=True)


if __name__ == "__main__":
    main()
    sum_check()
