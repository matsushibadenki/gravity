"""Four-dimensional off-shell Einstein-clock Hessian and ghost Ward checks."""

import torch
from torch.func import grad, jvp

from off_shell_clock_ward import SpectralWard


class FourDimensionalWard(SpectralWard):
    def gradient(self, field):
        return torch.stack([self.derivative(field, axis) for axis in range(4)], dim=4)

    @staticmethod
    def metric(fields):
        raw = fields[..., :16].unflatten(-1, (4, 4))
        return (raw + raw.mT) / 2

    def connection(self, metric, inverse):
        partial = self.gradient(metric)
        return 0.5 * torch.einsum("...ad,...bcd->...abc", inverse,
            partial + partial.transpose(-3, -2) - partial.movedim(-3, -1))

    def clock_gradient(self, fields, winding):
        return self.gradient(fields[..., 16]) + winding

    def action(self, fields, winding):
        metric = self.metric(fields)
        inverse = torch.linalg.inv(metric)
        connection = self.connection(metric, inverse)
        # Einstein density up to the periodic boundary term.
        ricci_product = (torch.einsum("...rus,...svr->...uv", connection, connection)
                         - torch.einsum("...ruv,...srs->...uv", connection, connection))
        clock = self.clock_gradient(fields, winding)
        density = torch.linalg.cholesky(metric).diagonal(dim1=-2, dim2=-1).prod(dim=-1)
        return (density * torch.einsum("...ab,...ab->...", inverse,
                                       clock[..., :, None] * clock[..., None, :] / 2
                                       - ricci_product)).mean()

    def orbit(self, fields, vector, winding):
        metric = self.metric(fields)
        index_term = self.gradient(vector) @ metric
        change = (torch.einsum("...a,...aij->...ij", vector, self.gradient(metric))
                  + index_term + index_term.mT)
        clock_change = (vector * self.clock_gradient(fields, winding)).sum(dim=-1)
        return torch.cat((change.flatten(-2), clock_change[..., None]), dim=-1)

    def de_donder(self, background):
        metric = self.metric(background)
        inverse = torch.linalg.inv(metric)
        connection = self.connection(metric, inverse)
        density = torch.linalg.cholesky(metric).diagonal(dim1=-2, dim2=-1).prod(dim=-1)

        def gauge_fix(fluctuation):
            h = self.metric(fluctuation)
            index_term = torch.einsum("...dab,...dc->...abc", connection, h)
            covariant = self.gradient(h) - index_term - index_term.transpose(-2, -1)
            return (torch.einsum("...ab,...abc->...c", inverse, covariant)
                    - torch.einsum("...ab,...cab->...c", inverse, covariant) / 2)

        return gauge_fix, inverse, density


def check(size, velocity):
    model = FourDimensionalWard(size)
    phase = 2 * torch.pi * torch.arange(size) / size
    t, x, y, z = torch.meshgrid(phase, phase, phase, phase, indexing="ij")
    warp = 0.08 * torch.cos(x + t) + 0.025 * torch.cos(y - z)
    metric = torch.exp(2 * warp)[..., None, None] * torch.eye(4)
    clock = velocity * 0.015 * torch.sin(t - x + y)
    fields = torch.cat((metric.flatten(-2), clock[..., None]), dim=-1)
    winding = torch.tensor([velocity, 0., 0., 0.])
    vector = torch.stack((torch.sin(x + t), torch.cos(t - y),
                          torch.sin(x + z), torch.cos(y + z)), dim=-1)
    orbit = lambda data: model.orbit(data, vector, winding)
    direction = orbit(fields)
    action = lambda data: model.action(data, winding)
    tadpole, image = jvp(grad(action), (fields,), (direction,))
    source = grad(lambda data: (tadpole.detach() * orbit(data)).sum())(fields)
    defect = (image + source).norm() / (image.norm() + source.norm())

    gauge_fix, inverse, density = model.de_donder(fields)
    ghost = -gauge_fix(direction)

    def pairing(left, right):
        return (density * torch.einsum("...ab,...a,...b->...", inverse, left, right)).mean()

    def fixed_action(data):
        condition = gauge_fix(data - fields)
        return action(data) + pairing(condition, condition) / 2

    fixed_image = jvp(grad(fixed_action), (fields,), (direction,))[1]
    ghost_adjoint = grad(lambda data: pairing(gauge_fix(data), ghost))(fields)
    assert (fixed_image - image + ghost_adjoint).norm() < 1e-10 * fixed_image.norm()
    print(f"N={size} velocity={velocity:.2f}: Ward defect={defect:.6e}")
    return defect.item()


if __name__ == "__main__":
    for velocity in (0., 0.35):
        errors = [check(size, velocity) for size in (5, 7, 9, 11)]
        assert all(left > right for left, right in zip(errors, errors[1:]))
        assert errors[-1] < 1e-3
