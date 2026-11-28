"""Frame and junction rows on a common tensor mesh, in canonical face coordinates."""

import numpy as np
from scipy.linalg import block_diag, null_space

from einstein_uncut_endpoint_response import response


def frame_checks(sides, steps, conforming_response, radial_generators=None):
    left, right = sides
    sizes = [len(face[0]) for face in sides]
    bulk_size = sum(sizes)
    total = 2*bulk_size+12
    eye = np.eye(total)
    configuration = eye[:bulk_size]
    momentum = eye[bulk_size:2*bulk_size]
    frame_q = eye[-12:-6]
    frame_p = eye[-6:]
    poisson = np.zeros((total,total))
    poisson[:bulk_size,bulk_size:2*bulk_size] = np.eye(bulk_size)
    poisson[-12:-6,-6:] = np.eye(6)
    poisson -= poisson.T.copy()
    qtests = np.column_stack((left[3],right[3]))
    ptests = np.column_stack((left[4],right[4]))
    proper = np.vstack((qtests@configuration,ptests@momentum))
    seam = np.column_stack((left[-1],-right[-1]))
    continuity = np.vstack((seam@configuration,seam@momentum))

    coordinates = [configuration[:sizes[0]],configuration[sizes[0]:]]
    momenta = [momentum[:sizes[0]],momentum[sizes[0]:]]
    charges, geometry, fluxes = [], [], []
    for i, face in enumerate(sides):
        value = face[-1][:4]
        ds = face[-1][4:]
        a = value[0]+value[1]+2*value[2]+value[3]
        b = (value[1]+value[2])/2
        k = value[0]+value[1]
        rc = 2*value[0]+2*ds[0]-ds[1]
        psi = (k-3*b+(a-rc)/2)/3
        energy = (.4*k-.6*psi)@coordinates[i]
        area = .1*k@coordinates[i]
        t, x, eta = frame_q[3*i:3*i+3]
        signed = 1-2*i
        charges.extend(frame_p[3*i:3*i+3]-signed*np.array([
            -energy,9.6*b@momenta[i]+.6*(eta-t),area]))
        geometry.append([k@coordinates[i],energy])
        fluxes.append([a@momenta[i]+(6*t-2*eta)/16,
                       b@momenta[i]+(-t+eta)/16])
    dressed = np.subtract(*fluxes)
    jump = frame_q[:3]-frame_q[3:]
    average = (frame_q[:3]+frame_q[3:])/2
    # In the C1 control the K and energy jumps are already in continuity.
    # The dressed flux rows still act on relative time and boost.
    frames = np.vstack((charges,dressed,jump[1],average))
    bulk = np.vstack((proper,continuity))
    basis = np.linalg.qr(bulk.T, mode="reduced")[0].T
    combined = np.vstack((basis,frames))
    def log_density(rows):
        sign, value = np.linalg.slogdet(rows@poisson@rows.T)
        assert sign == 1 and np.isfinite(value)
        return value/2
    delta = log_density(combined)-log_density(basis)
    jacobian = np.linalg.slogdet(frames[:,-12:])[1]
    np.testing.assert_allclose(delta,jacobian,atol=2e-8,rtol=0)
    print(f"Frame log Dirac increment={delta:.9g}, frame log delta Jacobian={jacobian:.9g}")

    # Keep only geometric junction conditions, on the same broken elements.
    # The relative clock is allowed to vary. Its consistency fixes the
    # secondary row as in the previous open-time experiment.
    hessian = block_diag(left[1],right[1],left[0],right[0],np.zeros((12,12)))

    def geometric_rows(frame_section):
        primary = np.vstack((proper,np.subtract(*geometry),frames[:-3],
                             frame_section,jump[2]))
        primary = primary/np.linalg.norm(primary,axis=1)[:,None]
        assert np.linalg.matrix_rank(primary) == len(primary)
        primary = np.linalg.qr(primary.T, mode="reduced")[0].T
        bracket = primary@poisson@primary.T
        kernel = null_space(bracket,rcond=1e-10)
        assert kernel.shape[1] == 1
        direction = (poisson@primary.T@kernel).ravel()
        assert abs(jump[0]@direction) > 1e-8
        direction /= jump[0]@direction
        np.testing.assert_allclose(jump[2]@direction,0,atol=1e-8)
        bare_flux = (seam@momentum@direction)[:4]@np.array([[1,0],[1,.5],[2,.5],[1,0]])
        np.testing.assert_allclose(bare_flux,[-6/16,1/16],atol=1e-8)
        assert np.linalg.norm(continuity@direction) > 1e-7
        secondary = direction@hessian
        assert np.linalg.norm(secondary) > 1e-12
        return np.vstack((primary,secondary/np.linalg.norm(secondary)))

    rows = geometric_rows(average)
    tangent = null_space(rows)
    pair_difference = (len(combined)-len(rows))//2
    assert len(combined)-len(rows) == 12
    conforming = null_space(combined)
    # Measure the actual intersection before attributing the difference
    # in dimension to an independent symplectic sector.
    overlap = rows@conforming
    mismatch = np.linalg.svd(overlap, compute_uv=False)
    rank = np.count_nonzero(mismatch > 1e-8)
    common = conforming@null_space(overlap, rcond=1e-8)
    assert np.linalg.norm(rows@common) < 1e-7
    extra = tangent@null_space(common.T@tangent)
    print(f"Conforming directions excluded by geometric rows={rank}, "
          f"geometric directions outside intersection={extra.shape[1]}")
    print("Primary mismatch norm and secondary mismatch norm:",
          np.linalg.norm(overlap[:-1]), np.linalg.norm(overlap[-1]))
    canonical = np.triu(poisson,1)
    diff = np.diff(np.eye(steps+1),axis=0)
    # Trapezoidal potential weights and one momentum for each forward link.
    # For fixed flat endpoints the last momentum may be integrated as an
    # independent zero-source Gaussian and drops out of Z[j]/Z[0].
    weights = np.ones(steps+1)
    weights[[0,-1]] = .5
    energy = np.kron(np.diag(weights), hessian)
    pblock = hessian.copy()
    pblock[:bulk_size,:] = 0
    pblock[:,:bulk_size] = 0
    energy += np.kron(np.diag(1-weights),pblock)
    links = np.kron(diff.T@np.eye(steps,steps+1),canonical)
    action = energy/steps-links-links.T
    source = np.r_[left[2],right[2],np.zeros(bulk_size+12)]
    trace = np.vstack((seam@configuration,seam@momentum,jump[0]))
    # Normalize trace covectors by their ambient Gram norms before
    # projecting the directly sourced direction onto named traces.
    trace /= np.linalg.norm(trace,axis=1)[:,None]
    trace_rank = np.linalg.matrix_rank(trace@extra, tol=1e-8)
    assert np.linalg.norm(trace@common) < 1e-7
    print(f"Metric, momentum and relative-time trace rank={trace_rank}")
    direct_load = extra@(extra.T@source)
    excluded = conforming@null_space(common.T@conforming)
    print(f"Extra direct source norm={np.linalg.norm(direct_load):.8g}, "
          f"excluded conforming source norm={np.linalg.norm(excluded.T@source):.8g}")
    print("Direct source direction traces (Cartesian coefficient jumps q, dq/ds, p, dp/ds, relative T):",
          np.round(trace@direct_load,8))
    endpoint = np.r_[0:bulk_size,2*bulk_size:2*bulk_size+6]
    # Use the identical slice assembly for both junction prescriptions.
    # This also checks the sign and endpoint conventions of the independent
    # three-momentum-link calculation against the four-slice integral.
    control, control_nullity = response(conforming,endpoint,action,source,steps)
    np.testing.assert_allclose(control, conforming_response, atol=2e-6, rtol=0)
    assert control_nullity == 0
    value, nullity, history = response(
        tangent,endpoint,action,source,steps,return_history=True)
    alternate_rows = geometric_rows(frame_q[:3])
    alternate = null_space(alternate_rows)
    # The density on Euclidean tangent coordinates is the Dirac bracket
    # determinant divided by the coarea determinant of the delta rows.
    def check_measure(constraints, lift):
        density = log_density(constraints)-np.linalg.slogdet(constraints@constraints.T)[1]/2
        symplectic = np.linalg.slogdet(lift.T@poisson@lift)[1]/2
        np.testing.assert_allclose(density,symplectic,atol=1e-7,rtol=0)
        return density

    density = check_measure(rows,tangent)
    alternate_density = check_measure(alternate_rows,alternate)
    # A common translation puts the inner frame at zero. The time and
    # boost shifts induce equal and opposite changes of tangential charge.
    translation = (frame_q[:3]+frame_q[3:]).T.copy()
    translation[:,0] -= .6*(frame_p[1]-frame_p[4])
    translation[:,2] += .6*(frame_p[1]-frame_p[4])
    moved = tangent-translation@(frame_q[:3]@tangent)
    np.testing.assert_allclose(alternate_rows@moved,0,atol=1e-7,rtol=0)
    coordinate_map = alternate.T@moved
    jacobian = np.linalg.slogdet(coordinate_map)[1]
    np.testing.assert_allclose(density,alternate_density+jacobian,atol=1e-7,rtol=0)
    np.testing.assert_allclose(tangent.T@poisson@tangent,moved.T@poisson@moved,
                               atol=1e-8,rtol=0)
    np.testing.assert_allclose(tangent.T@canonical@tangent,moved.T@canonical@moved,
                               atol=1e-8,rtol=0)
    np.testing.assert_allclose(source@moved,source@tangent,atol=1e-8,rtol=0)
    endpoint_lift = tangent@null_space(tangent[endpoint],rcond=1e-10)
    np.testing.assert_allclose(frame_q[:3]@endpoint_lift,0,atol=1e-9,rtol=0)
    other_value, other_nullity = response(alternate,endpoint,action,source,steps)
    assert other_nullity == nullity
    np.testing.assert_allclose(other_value,value,atol=2e-6,rtol=0)
    print(f"Common-frame gauge comparison: log density={density:.8g}, "
          f"transported={alternate_density+jacobian:.8g}, "
          f"susceptibility gap={abs(other_value-value):.8g}")
    if radial_generators is not None:
        from einstein_radial_embedding_control import check_radial_embedding
        volume_values = []
        for frame_rows, reference in ((rows,value),(alternate_rows,other_value)):
            volume_values.append(check_radial_embedding(
                sides, radial_generators, frame_rows, canonical, hessian,
                source, endpoint, steps, reference))
        (first, first_lift, first_density), (second, second_lift, second_density) = volume_values
        shifted = first_lift-translation@(frame_q[:3]@first_lift)
        reduced_map = second_lift.T@shifted
        np.testing.assert_allclose(second_lift@reduced_map,shifted,atol=1e-7,rtol=0)
        measure_gap = abs(first_density-second_density-np.linalg.slogdet(reduced_map)[1])
        assert measure_gap < 1e-6
        print(f"Volume time-link transported log-density gap={measure_gap:.8g}")
        if np.all(np.isfinite([first,second])):
            np.testing.assert_allclose(first,second,atol=2e-5,rtol=0)
        else:
            assert np.isnan(first) and np.isnan(second)
            print("Both frame sections have a source-coupled endpoint null mode.")
    # Split the driven solution in the same Gram metric as the source
    # projection. The orthogonal boundary component has zero direct source.
    boundary_history = history@extra@extra.T
    sourced_axis = direct_load/np.linalg.norm(direct_load)
    indirect = boundary_history - np.outer(boundary_history@sourced_axis,sourced_axis)
    np.testing.assert_allclose(indirect@source,0,atol=1e-7)
    print("Peak driven normalized traces (q jets, p jets, relative time):",
          [np.max(np.linalg.norm(history@group.T,axis=1))
           for group in (trace[:8],trace[8:16],trace[16:])])
    print(f"Driven boundary history indirect fraction="
          f"{np.linalg.norm(indirect)/np.linalg.norm(boundary_history):.8g}")
    print(f"Geometric-only junction: flat susceptibility={value:.10g}, "
          f"endpoint kernel nullity={nullity}, additional canonical pairs={pair_difference}")
    return value
