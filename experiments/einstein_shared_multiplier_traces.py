"""Numerical ADM boundary jets with a common orientation and normalization."""

import numpy as np
from scipy.interpolate import BSpline
from scipy.linalg import block_diag, null_space

from einstein_matched_mesh_sewing import assemble, tests


def check(cells):
    edges = np.linspace(0,2,2*cells+1)
    lapse = tests(edges,2,2,clamp_seam=False)
    shifts = tests(edges,1,1,clamp_seam=False)

    # N=r^2 f Y, W=f_s Qx+g_s Y_cart x. Angular shifts are
    # parametrized by the coefficient of the angular gradient of Y.
    lapse_jets = np.vstack((lapse(1.),2*(lapse(1.)+lapse(1.,nu=1))))
    value = shifts(1.)
    shift_jets = np.vstack((np.r_[value,value],np.r_[value/2,np.zeros_like(value)]))
    jets = block_diag(lapse_jets,shift_jets)
    assert np.linalg.matrix_rank(jets) == 4
    lift = np.linalg.pinv(jets)
    np.testing.assert_allclose(jets@lift,np.eye(4),atol=1e-12)
    lapse_count, shift_count = lapse.c.shape[1], shifts.c.shape[1]
    # Compare the kernel with the directly clamped smearing space.
    assert null_space(jets).shape[1] == (
        tests(edges,2,2).c.shape[1]+2*tests(edges,1,1).c.shape[1])
    unit_lapse = BSpline(lapse.t,lapse.c@lift[:lapse_count,:2],4)

    charges, bulk, traces, inertias = [],[],[],[]
    for sign, side in ((1,edges[:cells+1]),(-1,edges[cells:])):
        face = assemble(side,shifts,lapse,tensor_continuity=0)
        fields, derivative = np.split(face[-1],2)
        a,b,c,d = fields
        da,db,_,_ = derivative
        radial = a+b+2*c+d
        mixed = (b+c)/2
        angular = a-b/2
        radial_angular = 2*(a+da-db/2)
        # Angular norm of the project's quadrupole relative to pi.
        # In the project's G=1 normalization, I_Y/(8*pi)=0.1.
        # Shift the bare bulk momentum by sigma*kappa*l*udot/2,
        # where l is the angular metric trace covector. The remaining
        # embedding coefficient follows by the partial Legendre transform.
        angular_trace = 2*angular
        kappa = .1
        kinetic = face[0]
        trace_compliance = angular_trace@kinetic@angular_trace
        inertias.append(-4*sign*kappa-kappa**2*trace_compliance/4)
        scalar = .8*sign*np.vstack((2*(radial-angular)-2*radial_angular-12*mixed,
                                     2*angular))
        vector = .8*sign*np.vstack((2*radial,12*mixed))
        surface = block_diag(scalar,vector)
        scalar_pairing = lift[:lapse_count,:2].T@face[3][:lapse_count]
        vector_pairing = lift[lapse_count:,2:].T@face[3][lapse_count:]
        # N*C = <h,Hess N - g Lap N> + Q_N.
        # -2 W*div p = <p,L_W g> - Q_W.
        bulk.append(block_diag(scalar_pairing,vector_pairing)
                    +block_diag(scalar,-vector))
        charges.append(surface)
        # Only c's derivative enters the lapse-value charge. C^0 tensors
        # have independent one-sided derivatives until this row is matched.
        traces.append(block_diag(np.vstack((radial,mixed,angular,radial_angular)),
                                 np.vstack((radial,mixed))))
        actual = assemble(side,shifts,unit_lapse,tensor_continuity=0)[3][:2]
        np.testing.assert_allclose(actual,scalar_pairing,atol=1e-8,rtol=1e-8)
    common = null_space(np.column_stack((traces[0],-traces[1])))
    total_charge = np.column_stack(charges)
    cancellation = np.linalg.norm(total_charge@common)/np.linalg.norm(total_charge)
    assert cancellation < 1e-10
    print(f"cells={cells}, jet rank=4, clamped dimension={null_space(jets).shape[1]}, "
          f"relative smooth charge defect={cancellation:.5g}, "
          f"two-face volume row rank={np.linalg.matrix_rank(np.column_stack(bulk))}, "
          f"bare embedding velocity coefficients={np.round(inertias,8)}")


if __name__ == "__main__":
    for cells in (2,4,8):
        check(cells)
