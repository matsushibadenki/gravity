"""Cut versus global weak ADM response with flat metric endpoint values."""

import numpy as np
from scipy.linalg import block_diag, null_space

from einstein_even_bulk import tensor_basis
from einstein_joint_adm_time_control import region


def response(tangent, endpoint_coordinates, action, source, steps, *, return_history=False, affine_history=None):
    # Enforce the same flat configuration eigenstate at both ends. The
    # characteristic function Z[j]/Z[0] cancels its distributional norm.
    fixed = tangent@null_space(tangent[endpoint_coordinates], rcond=1e-10)
    lift = block_diag(fixed, *([tangent]*(steps-1)), fixed)
    projected = lift.T@action@lift
    spectrum, modes = np.linalg.eigh(projected)
    drive = np.kron(np.sin(np.pi*np.arange(steps+1)/steps)/steps, source)
    constant = 0
    if affine_history is not None:
        shift = np.asarray(affine_history).ravel()
        constant = 2*drive@shift-shift@action@shift
        drive = drive-action@shift
    load = modes.T@(lift.T@drive)
    near = abs(spectrum)<1e-8
    if affine_history is not None:
        print("Affine endpoint near eigenvalues and source components:",
              spectrum[near],load[near])
        near = abs(spectrum)<1e-11
        if np.linalg.norm(load[near]) >= 1e-7:
            active = lift@(modes[:,near]@load[near])
            slices = np.linalg.norm(active.reshape(steps+1,-1),axis=1)
            print("Source-coupled null history slice norms:",
                  np.round(slices/np.linalg.norm(slices),8))
            return np.nan, np.count_nonzero(near)
    assert np.linalg.norm(load[near]) < 1e-7
    susceptibility = constant+np.sum(load[~near]**2/spectrum[~near])
    if return_history:
        history = lift@(modes[:,~near]@(load[~near]/spectrum[~near]))
        return susceptibility, np.count_nonzero(near), history.reshape(steps+1,-1)
    return susceptibility, np.count_nonzero(near)


def compare_fixed_endpoints(order, steps, tangent, configuration, cut_action, cut_source):
    tensors = tensor_basis(order)
    n = len(tensors)
    _, constraints, _, source, kinetic, spatial, _ = region(
        tensors, 0, 2, 1, projected_gauge=True, spatial_order=order, whole=True
    )
    # Single Cartesian field over [0,2], without an internal frame or
    # jump rows. Proper generators preserve the marked probe sphere.
    hessian = block_diag(spatial,32*kinetic)
    canonical = np.zeros_like(hessian)
    canonical[:n,n:] = np.eye(n)
    diff = np.diff(np.eye(steps+1),axis=0)
    links = np.kron(diff.T@np.eye(steps,steps+1),canonical)
    action = np.kron(np.eye(steps+1),hessian)/steps-links-links.T
    direct, direct_zero = response(null_space(constraints),np.arange(n),action,source,steps)
    sewn, sewn_zero = response(tangent,configuration,cut_action,cut_source,steps)
    ratio = np.exp(.5j*.1**2*(sewn-direct))
    print(f"Flat endpoints: cut susceptibility={sewn:.10g}, uncut={direct:.10g}, "
          f"|normalized ratio at j=0.1 minus one|={abs(ratio-1):.9g}, "
          f"remaining nullities={sewn_zero},{direct_zero}")
