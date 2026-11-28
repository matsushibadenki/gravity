"""Radial coordinate extension of the finite ADM junction integral."""

import numpy as np
from scipy.linalg import block_diag, null_space

from einstein_matched_mesh_sewing import collar_anchor_coefficient
from einstein_uncut_endpoint_response import response


def check_radial_embedding(sides, generators, rows, canonical, hessian,
                           source, endpoint, steps, reference):
    size = len(source)
    bulk = sum(family.shape[1] for family,_ in generators)
    radial = block_diag(*(family[-1,:,None] for family,_ in generators))
    lift = np.eye(size+4)
    # Coordinates are dressed bulk/frame variables, R, P_dressed.
    # Bare q=q_dressed+gR and P_bare=P_dressed-g^T p.
    lift[:bulk,size:size+2] = radial
    lift[size+2:,bulk:2*bulk] = -radial.T
    inverse = np.linalg.inv(lift)
    extended_link = np.pad(canonical,((0,4),(0,4)))
    extended_link[size:size+2,size+2:] = np.eye(2)
    poisson = extended_link-extended_link.T
    np.testing.assert_allclose(lift.T@extended_link@lift,extended_link,atol=1e-12)
    completed_source = np.r_[source,-collar_anchor_coefficient(.875,1),
                            -collar_anchor_coefficient(1,1.125),0,0]
    np.testing.assert_allclose(lift.T@completed_source,np.r_[source,np.zeros(4)],atol=1e-9)
    pullback = inverse[:size]
    energy = pullback.T@hessian@pullback
    padded_rows = np.pad(rows,((0,0),(0,4)))
    # On the strong momentum constraint the differentiable generator
    # is its surface term. Test that identity on the weak finite chart.
    allowed_momenta = null_space(rows)[bulk:2*bulk]
    surface = block_diag(*(sign*1.6*(face[-1][0]+face[-1][1]+2*face[-1][2]+face[-1][3])
                           for sign,face in zip((1,-1),sides)))
    tangent_flux = block_diag(*(sign*4.8*(face[-1][1]+face[-1][2])/2
                                for sign,face in zip((1,-1),sides)))
    flux_rows = np.vstack((surface,tangent_flux))
    # Qx has the same normal boundary value as Y_cart x and half a
    # tangential gradient. Subtract the latter shift to isolate it.
    weak = np.vstack((radial.T,block_diag(*(family[0]-family[1]
                                           for family,_ in generators))))
    heldout = np.vstack((block_diag(*(family[1] for _,family in generators)),
                        block_diag(*(family[0]-family[1] for _,family in generators))))
    constraint = (weak-flux_rows)@allowed_momenta
    refined = allowed_momenta@null_space(constraint)
    before, after = flux_rows@allowed_momenta, flux_rows@refined
    rank = np.linalg.matrix_rank(before)
    assert np.linalg.matrix_rank(after) == rank
    denominator = np.linalg.norm(surface@refined)
    assert denominator > 1e-10
    old = np.linalg.norm((radial.T-surface)@allowed_momenta)/np.linalg.norm(surface@allowed_momenta)
    new = np.linalg.norm((radial.T-surface)@refined)/denominator
    diagnostic = heldout-flux_rows
    # Compare the independent volume strains on the same full flux norm.
    print(f"Radial generator bulk-defect/flux norm={old:.8g} -> {new:.8g}, "
          f"joint flux rank={rank}, held-out defect="
          f"{np.linalg.norm(diagnostic@allowed_momenta)/np.linalg.norm(before):.8g} -> "
          f"{np.linalg.norm(diagnostic@refined)/np.linalg.norm(after):.8g}")
    volume_rows = np.zeros((len(flux_rows),size))
    volume_rows[:,bulk:2*bulk] = weak-flux_rows
    base = null_space(rows)
    reduced_form = base.T@(canonical-canonical.T)@base
    reduced_volume = volume_rows@base
    directions = base@np.linalg.solve(reduced_form,reduced_volume.T)
    volume_bracket = volume_rows@directions
    secondary = directions.T@hessian
    completed = np.vstack((rows,volume_rows,secondary))
    row_scales = np.linalg.norm(completed,axis=1)
    completed /= row_scales[:,None]
    bracket_norm = np.linalg.norm(volume_bracket,ord=2)
    bracket_spectrum = np.linalg.svd(completed@(canonical-canonical.T)@completed.T,
                                    compute_uv=False)
    drive_defect = np.linalg.norm(directions.T@source)
    augmented = null_space(completed)
    augmented_flux = np.linalg.matrix_rank(flux_rows@augmented[bulk:2*bulk])
    print(f"Volume bracket norm={bracket_norm:.6g}, completed bracket minimum="
          f"{bracket_spectrum[-1]:.6g}, secondary source norm={drive_defect:.6g}, "
          f"completed flux rank={augmented_flux}")
    eye = np.eye(size+4)
    # The second section gives a field-dependent displacement, vanishing
    # at the same flat temporal endpoints.
    section = np.zeros((2,size+4))
    section[0,0], section[1,generators[0][0].shape[1]] = .2,-.2
    endpoint_rows = np.vstack((pullback[endpoint],eye[size:size+2]))
    weights = np.ones(steps+1)
    weights[[0,-1]] = .5
    position_count = np.r_[0:bulk,2*bulk:size-6,size:size+2]
    momentum_energy = energy.copy()
    momentum_energy[position_count,:] = 0
    momentum_energy[:,position_count] = 0
    time_difference = np.diff(np.eye(steps+1),axis=0)
    links = np.kron(time_difference.T@np.eye(steps,steps+1),extended_link)
    action = (np.kron(np.diag(weights),energy)
              +np.kron(np.diag(1-weights),momentum_energy))/steps-links-links.T

    assert bracket_norm < 1e-8 and bracket_spectrum[-1] > 1e-10
    # Preservation is source dependent. Carry the affine displacement
    # on every slice, including its contribution to the Gaussian phase.
    target = np.r_[np.zeros(len(rows)+len(flux_rows)),directions.T@source]/row_scales
    particular = np.linalg.lstsq(completed,target,rcond=None)[0]
    np.testing.assert_allclose(completed@particular,target,atol=1e-9,rtol=0)
    time_shape = np.sin(np.pi*np.arange(steps+1)/steps)
    time_shape[[0,-1]] = 0
    indices = np.arange((steps+1)*(size+4)).reshape(steps+1,size+4)[:,:size].ravel()
    volume_value, volume_nullity = response(
        augmented,endpoint,action[np.ix_(indices,indices)],source,steps,
        affine_history=np.outer(time_shape,particular))
    direct_density = np.linalg.slogdet(augmented.T@(canonical-canonical.T)@augmented)[1]/2
    coarea_density = np.log(bracket_spectrum).sum()/2-np.linalg.slogdet(completed@completed.T)[1]/2
    np.testing.assert_allclose(direct_density,coarea_density,atol=1e-6,rtol=0)
    print(f"Volume time-link susceptibility={volume_value:.11g}, log density={direct_density:.9g}, "
          f"nullity={volume_nullity}")

    endpoint_rank = np.linalg.matrix_rank(endpoint_rows)
    endpoint_basis = np.linalg.svd(endpoint_rows,full_matrices=False)[2][:endpoint_rank]
    rotation = np.vstack((endpoint_basis,null_space(endpoint_basis).T))
    temporal_rotation = np.kron(np.eye(steps+1),rotation)
    for gauge in (np.zeros_like(section),section):
        constraints = np.vstack((padded_rows,eye[size+2:],eye[size:size+2]-gauge))@inverse
        tangent = null_space(constraints)
        sign, log_bracket = np.linalg.slogdet(constraints@poisson@constraints.T)
        assert sign == 1 and np.isfinite(log_bracket)
        log_density = log_bracket/2
        log_coarea = np.linalg.slogdet(constraints@constraints.T)[1]/2
        induced = np.linalg.slogdet(tangent.T@poisson@tangent)[1]/2
        np.testing.assert_allclose(log_density-log_coarea,induced,atol=1e-8,rtol=0)
        # At the endpoints R=0 in both sections once dressed q=0.
        # Rotate the endpoint row space to coordinate axes for the Gaussian.
        actual, nullity = response(rotation@tangent,np.arange(endpoint_rank),
                                   temporal_rotation@action@temporal_rotation.T,
                                   rotation@completed_source,steps)
        np.testing.assert_allclose(actual,reference,atol=2e-7,rtol=0)
        print(f"Radial section: susceptibility gap={abs(actual-reference):.8g}, "
              f"endpoint nullity={nullity}, Dirac density={induced:.8g}")

    return volume_value, augmented, direct_density
