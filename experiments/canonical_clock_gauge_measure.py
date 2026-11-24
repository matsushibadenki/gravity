"""Check the homogeneous linear ADM gauge measure on the spectral lattice."""

import numpy as np
import torch

from quartic_clock_reduction import ADMReduction


def check(size):
    spacing = 1.8 / size
    model = ADMReduction(size, spacing)
    count = model.count
    eigenvalues, eigenvectors = np.linalg.eigh(-model.laplacian.numpy())
    modes = eigenvectors[:, eigenvalues > 1e-9]
    k2 = eigenvalues[eigenvalues > 1e-9]
    velocity = np.sqrt(12) * model.hubble

    # In an orthonormal basis the spatial gauge operator has two transverse
    # eigenvalues -k^2 and one longitudinal eigenvalue -4 k^2 / 3.
    gauge_logdet = np.log(velocity) + np.log(4 / 3) + 3 * np.log(k2)
    # Each gauge constraint delta function removes its orbit coordinate.
    orbit_log_jacobian = -np.log(velocity) - 2 * np.log(k2) - np.log(4 * k2 / 3)
    assert np.allclose(gauge_logdet + orbit_log_jacobian, 0, atol=1e-13)

    hessian = torch.func.hessian(
        lambda q, auxiliary: model.action(q, auxiliary, 2), argnums=(0, 1)
    )(torch.zeros(2 * count), torch.zeros(4 * count))
    field, mixed = (block.numpy() for block in hessian[0])
    auxiliary = hessian[1][1].numpy()
    basis = np.kron(np.eye(4), modes)
    projected = basis.T @ auxiliary @ basis
    velocity_block = field[count:, count:]
    coupling = mixed[count:] @ basis
    schur = velocity_block - coupling @ np.linalg.solve(projected, coupling.T)
    normalized_mass = (modes.T @ schur @ modes) / model.cell
    assert np.allclose(normalized_mass, 12 * np.eye(len(k2)), atol=1e-9)
    # The auxiliary configuration Gaussian is not the orbit Jacobian.
    log_auxiliary = -np.linalg.slogdet(projected / model.cell)[1] / 2
    print(f"N={size}: modes={len(k2)}, mass/cell={np.trace(normalized_mass)/len(k2):.9f}, "
          f"auxiliary log-weight={log_auxiliary:+.6f}, "
          f"cancelled FP log-weight={gauge_logdet.sum():+.6f}")


if __name__ == "__main__":
    for size in (3, 5, 7):
        check(size)
