"""Consistency and Lorentzian time links with a free relative clock."""

import numpy as np
from scipy.linalg import lu_factor, lu_solve, null_space
from numpy.polynomial import Polynomial

from einstein_joint_adm_time_control import compare_fresnel


def diagnose(primary, poisson, hessian, time_row, source, steps, order, n, left_inverse, right_inverse):
    bracket = primary @ poisson @ primary.T
    kernel = null_space(bracket, rcond=1e-11)
    assert kernel.shape[1] == 1
    direction = (poisson @ primary.T @ kernel).ravel()
    direction /= time_row @ direction
    force = direction @ hessian
    curvature = force @ direction
    # Evaluate the mixed row on the entire primary tangent at fixed
    # relative time. This includes bulk momentum as well as frame data.
    fixed = null_space(np.vstack((primary, time_row)))
    print(f"N={order}: clock curvature={curvature:.9g}, "
          f"fixed-clock mixed row norm={np.linalg.norm(force@fixed):.9g}")
    # Smooth transverse-traceless momentum, with both fluxes zero at
    # the seam and outer boundary. Its master momentum is nonzero.
    r = Polynomial([0, 1])
    a = (1-r**2)**2*(4-r**2)**2
    c = -a/2
    b = (r*a.deriv()+3*a)/6
    d = (r*b.deriv()+3*b+c)/2
    master = (r**3*a).deriv(2)-(r**2*(a+2*c)).deriv()+r*(-3*a+6*c)
    assert abs(master(1)) > 1e-8
    np.testing.assert_allclose([a(1), b(1), a(2), b(2)], 0, atol=1e-11)
    # Invert the four component rows of tensor_basis.
    def divide(poly, power):
        quotient, remainder = divmod(poly, r**power)
        assert np.max(np.abs(remainder.coef)) < 1e-12
        return quotient
    raw = np.zeros((order+3, 4))
    for j, poly in enumerate((divide(c+d, 2), 2*d,
                              divide(2*(b-d), 2), divide(a-c+d-4*b, 4))):
        raw[:len(poly.coef[::2]), j] = poly.coef[::2]
    raw = raw.ravel()
    probe = np.zeros_like(direction)
    for start, inverse in ((n, left_inverse), (3*n, right_inverse)):
        probe[start:start+n] = np.linalg.solve(inverse.T, raw)
    np.testing.assert_allclose(primary@probe, 0, atol=1e-7)
    assert abs(time_row@probe) < 1e-12
    print(f"Mixed coefficient for the fixed TT profile={force@probe:.10g}, "
          f"master momentum at seam={master(1):.9g}")
    # Integrate all homogeneous constrained momenta at fixed configuration.
    # Completing the indefinite Lorentzian square is valid when this
    # momentum block is invertible. It tests cancellation independently
    # of the relative-time normalization used for the primary null lift.
    momentum_indices = np.r_[np.arange(n, 2*n), np.arange(3*n, 4*n),
                             np.arange(4*n+3, 4*n+6), np.arange(4*n+9, 4*n+12)]
    allowed_p = null_space(primary[:, momentum_indices])
    kinetic = allowed_p.T@hessian[np.ix_(momentum_indices, momentum_indices)]@allowed_p
    mixed_p = force[momentum_indices]@allowed_p
    relaxation = np.linalg.solve(kinetic, mixed_p)
    exchange = mixed_p@relaxation
    relaxed = direction.copy()
    relaxed[momentum_indices] -= allowed_p@relaxation
    np.testing.assert_allclose(relaxed@hessian@relaxed, curvature-exchange,
                               atol=1e-8, rtol=0)
    np.testing.assert_allclose(time_row@relaxed, 1, atol=1e-10)
    assert np.linalg.norm(allowed_p.T @ (hessian@relaxed)[momentum_indices]) < 1e-8
    print(f"Momentum Schur correction={exchange:.10g}, "
          f"remaining time Hessian={curvature-exchange:.10g}")
    assert abs(curvature) > 1e-9
    constraints = np.vstack((primary, force))
    bracket = constraints @ poisson @ constraints.T
    tangent = null_space(constraints)
    assert np.linalg.matrix_rank(bracket) == len(constraints)
    # Check that the relative-time lift enforces the secondary row.
    corrected = fixed - np.outer(direction, force@fixed)/curvature
    np.testing.assert_allclose(constraints@corrected, 0, atol=1e-7)

    dt = 1/steps
    action = dt*np.kron(np.eye(steps+1), hessian)
    potential = np.zeros_like(poisson)
    for start, width, sign in ((0, n, 1), (2*n, n, -1),
                               (4*n, 3, 1), (4*n+6, 3, -1)):
        potential[start:start+width, start+width:start+2*width] = sign*np.eye(width)
    derivative = np.diff(np.eye(steps+1), axis=0)
    links = np.kron(derivative.T@np.eye(steps, steps+1), potential)
    action -= links+links.T
    joint = np.kron(np.eye(steps+1), constraints)
    subspace = np.kron(np.eye(steps+1), tangent)
    from einstein_uncut_endpoint_response import compare_fixed_endpoints
    configuration = np.r_[0:n, 2*n:3*n, 4*n:4*n+3, 4*n+6:4*n+9]
    compare_fixed_endpoints(order, steps, tangent, configuration, action, source)
    spectrum, modes = np.linalg.eigh(subspace.T@action@subspace)
    drive = np.kron(dt*np.sin(np.pi*np.arange(steps+1)/steps), source)
    assert abs(direction@source) < 1e-8
    projected_drive = modes.T@(subspace.T@drive)
    print(f"Collar drive projection onto near-zero modes="
          f"{np.linalg.norm(projected_drive[abs(spectrum)<1e-8]):.8g}")
    zero = np.count_nonzero(abs(spectrum) < 1e-8)
    from einstein_residual_spatial_gauge import classify
    classify(subspace @ modes[:, abs(spectrum)<1e-8], primary, steps, n,
             order, left_inverse, right_inverse)
    print(f"constraint rank={np.linalg.matrix_rank(bracket)}, "
          f"link zero modes at 1e-8={zero}, min |eigenvalue|={min(abs(spectrum)):.3g}")
    print(f"log Dirac density/slice={np.linalg.slogdet(bracket)[1]/2:.8f}, "
          f"source along primary null={direction@source:.4g}")
    # Inertia of a saddle with independent constraints adds one positive
    # and one negative eigenvalue for each row, including at singularity.
    bordered = np.block([[action, joint.T], [joint, np.zeros((len(joint), len(joint)))]])
    full_spectrum = np.linalg.eigvalsh(bordered)
    # Check threshold stability. A full absolute scalar requires a
    # treatment of any zero directions and their boundary conditions.
    for tol in (1e-8, 1e-7):
        def inertia(values):
            return np.array([sum(values > tol), sum(values < -tol),
                             sum(abs(values) <= tol)])
        reduced_inertia = inertia(spectrum)
        assert np.array_equal(inertia(full_spectrum),
                              reduced_inertia+np.array([len(joint), len(joint), 0]))
    print(f"Reduced link inertia={reduced_inertia.tolist()}, "
          f"nonzero-sector phase/pi={-(reduced_inertia[0]-reduced_inertia[1])/4}")
    # Abel damping in the ambient canonical coordinates. Fourier
    # multipliers impose the constraints exactly. Check their normalized
    # absolute integral even when the undamped kernel is singular.
    density = (steps+1)*np.linalg.slogdet(bracket)[1]
    measure = (steps+1)*np.linalg.slogdet(tangent.T@np.linalg.solve(poisson, tangent))[1]
    for epsilon in (1e-3, 1e-5):
        gaussian = epsilon*np.eye(len(action))+1j*action
        bordered_gaussian = np.block([[gaussian, joint.T],
                                      [joint, np.zeros((len(joint), len(joint)))]])
        lu = lu_factor(bordered_gaussian)
        full = (density-np.log(abs(np.diag(lu[0]))).sum())/2
        extended_drive = np.pad(drive, (0, len(joint)))
        response = extended_drive@lu_solve(lu, extended_drive)
        direct_response = np.sum(projected_drive**2/(epsilon+1j*spectrum))
        np.testing.assert_allclose(response, direct_response, rtol=1e-5, atol=1e-5)
        direct = (measure-np.log(np.abs(epsilon+1j*spectrum)).sum())/2
        np.testing.assert_allclose(full, direct, atol=1e-4, rtol=0)
        print(f"Abel epsilon={epsilon:g}: normalized log modulus={full:.8g}, "
              f"pullback gap={abs(full-direct):.3g}")
    if zero == 0:
        measure = measure/(steps+1)
        compare_fresnel(action, joint, subspace, drive,
                        (steps+1)*np.linalg.slogdet(bracket)[1], (steps+1)*measure)


if __name__ == "__main__":
    from einstein_joint_adm_time_control import check
    for cutoff in (2, 3):
        check(projected_gauge=True, order=cutoff, open_time=True)
