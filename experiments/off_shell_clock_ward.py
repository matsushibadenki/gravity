"""Test the classical off-shell Einstein-clock Ward identity with spectral derivatives."""

from math import pi

import torch
from torch.func import grad, jvp

torch.set_default_dtype(torch.float64)
torch.set_num_threads(1)


class SpectralWard:
    def __init__(self, size, length=1.8):
        self.size = size
        self.wave = 2 * pi * torch.fft.fftfreq(size, length / size)

    def derivative(self, field, axis):
        shape = [1] * field.ndim
        shape[axis] = self.size
        return torch.fft.ifft(
            1j * self.wave.reshape(shape) * torch.fft.fft(field, dim=axis), dim=axis
        ).real

    def low_modes(self, field):
        modes = torch.fft.fftfreq(self.size) * self.size
        keep = (modes.abs() <= 4.01)
        mask = (keep[:, None] & keep[None, :])[..., None]
        return torch.fft.ifft2(mask * torch.fft.fft2(field, dim=(0, 1)), dim=(0, 1)).real

    def gradient(self, field):
        return torch.stack([self.derivative(field, axis) for axis in (0, 1)], dim=2)

    def unpack(self, fields):
        metric = fields[..., :4].reshape(self.size, self.size, 2, 2)
        metric = (metric + metric.transpose(-2, -1)) / 2
        warp, clock = fields[..., 4], fields[..., 5]
        return metric, warp, clock

    def action(self, fields, sector):
        metric, warp, clock = self.unpack(fields)
        inverse = torch.linalg.inv(metric)
        density = torch.sqrt(-torch.linalg.det(metric)) * torch.exp(2 * warp)
        if sector == "clock":
            clock_gradient = self.gradient(clock) + torch.tensor([1., 0.])
            return (-0.5 * density * torch.einsum("...ab,...a,...b->...", inverse,
                                                clock_gradient, clock_gradient)).mean()
        partial = self.gradient(metric)
        christoffel = 0.5 * torch.einsum("...ad,...bcd->...abc", inverse,
            partial + partial.transpose(-3, -2) - partial.permute(0, 1, 3, 4, 2))
        connection_gradient = self.gradient(christoffel)
        ricci = (torch.einsum("...aabc->...bc", connection_gradient)
                 - torch.einsum("...caba->...bc", connection_gradient)
                 + torch.einsum("...aad,...dbc->...bc", christoffel, christoffel)
                 - torch.einsum("...acd,...dba->...bc", christoffel, christoffel))
        warp_gradient = self.gradient(warp)
        curvature = torch.einsum("...ab,...ab->...", inverse, ricci)
        warp_term = 2 * torch.einsum("...ab,...a,...b->...", inverse, warp_gradient, warp_gradient)
        return (density * (curvature + warp_term)).mean()

    def gauge(self, fields, vector):
        metric, warp, clock = self.unpack(fields)
        vector_gradient = self.gradient(vector)
        index_term = torch.einsum("...ab,...ca->...cb", metric, vector_gradient)
        metric_change = (torch.einsum("...c,...cab->...ab", vector, self.gradient(metric))
                         + index_term + index_term.transpose(-2, -1))
        warp_change = (vector * self.gradient(warp)).sum(dim=-1)
        clock_change = (vector * self.gradient(clock)).sum(dim=-1) + vector[..., 0]
        return torch.cat((metric_change.flatten(2), warp_change[..., None],
                          clock_change[..., None]), dim=-1)


def gauge_fixed_check(model, fields, gauge_direction, action, bulk):
    # A linear background gauge on the two retained diffeomorphisms.
    # F=(clock perturbation, spatial divergence of the metric perturbation).
    def gauge_fix(fluctuation):
        metric, _, clock = model.unpack(fluctuation)
        return torch.stack((clock, model.derivative(metric[..., 1, 1], 1)), dim=-1)

    def fixed_action(data):
        field = gauge_fix(data - fields)
        return action(data) + field.square().sum() / 2

    fixed_bulk = jvp(grad(fixed_action), (fields,), (gauge_direction,))[1]
    ghost = gauge_fix(gauge_direction)
    adjoint_ghost = grad(lambda fluctuation: (gauge_fix(fluctuation) * ghost).sum())(fields)
    difference = fixed_bulk - adjoint_ghost - bulk
    assert difference.norm() < 1e-11 * fixed_bulk.norm()
    assert ghost.norm() > 0


def check(size, harmonic=1):
    model = SpectralWard(size)
    phase = 2 * pi * torch.arange(size) / size
    t, x = torch.meshgrid(phase, phase, indexing="ij")
    lapse = torch.exp(0.16 * torch.cos(t + harmonic * x))
    shift = 0.12 * torch.sin(t - harmonic * x)
    space = torch.exp(0.24 * torch.cos(2 * t + harmonic * x))
    fields = torch.stack((-lapse**2 + space * shift**2, space * shift, space * shift, space,
                          0.12 * torch.cos(t - harmonic * x), 0.08 * torch.sin(t + 2 * harmonic * x)), dim=-1)
    vector = torch.stack((torch.cos(t - harmonic * x), torch.sin(2 * t + harmonic * x)), dim=-1)
    gauge = lambda data: model.gauge(data, vector)
    gauge_direction = gauge(fields)
    errors = []
    for sector in ("gravity", "clock"):
        action_gradient = grad(lambda data: model.action(data, sector))
        source, bulk = jvp(action_gradient, (fields,), (gauge_direction,))
        source_term = grad(lambda data: (source.detach() * gauge(data)).sum())(fields)
        if sector == "gravity":
            gauge_fixed_check(model, fields, gauge_direction,
                              lambda data: model.action(data, sector), bulk)
        full_residual = (bulk + source_term).norm() / (bulk.norm() + source_term.norm())
        bulk, source_term = map(model.low_modes, (bulk, source_term))
        scale = bulk.norm() + source_term.norm()
        residual = ((bulk + source_term).norm() / scale).item()
        assert (source_term.norm() / scale).item() > 0.05
        errors.append(residual)
        print(f"N={size:2d} harmonic={harmonic:2d} {sector}: Ward residual={residual:.6e}, "
              f"full={full_residual:.6e}, omitting source term={bulk.norm()/scale:.6e}")
    return max(errors)


if __name__ == "__main__":
    errors = [check(size) for size in (9, 17, 33, 65)]
    assert errors[0] > errors[1] > errors[2]
    assert errors[-1] < 1e-8
    assert check(65, harmonic=15) > 0.1
