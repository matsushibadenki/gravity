"""Cut and uncut Lorentzian ADM integrals on one conforming radial mesh."""

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import BSpline
from scipy.linalg import block_diag, null_space, solve_triangular


def splines(edges, continuity):
    # Piecewise quartics in r^2. The central sphere is a mesh node.
    knots = np.r_[np.repeat(edges[0]**2, 5), np.repeat(edges[1:-1]**2, 4-continuity),
                  np.repeat(edges[-1]**2, 5)]
    return BSpline(knots, np.eye(len(knots)-5), 4)


def tests(edges, continuity, jets, *, clamp_seam=True):
    shape = splines(edges, continuity)
    traces = np.vstack([shape(r*r, nu=j) for r in ((1,2) if clamp_seam else (2,)) for j in range(jets)])
    return BSpline(shape.t, null_space(traces), 4)


def tensor_rows(shape, r):
    s = r*r
    p = shape(s)
    derivative = shape(s, nu=1)
    def row(coeff, ds):
        value = np.outer(p, coeff).ravel()
        radial = 2*s*(np.outer(derivative, coeff)+np.outer(p, ds)).ravel()
        return value, radial
    h, _ = row([s,1,2*s,s*s],[1,0,2,2*s])
    b, _ = row([0,.5,s/2,0],[0,0,.5,0])
    c, rc = row([s,-.5,0,0],[1,0,0,0])
    d, rd = row([0,.5,0,0],[0,0,0,0])
    return np.array([h,b,c,d]), rc, rd


def collar_anchor_coefficient(lower=.875, upper=1.125):
    """Derivative of the curvature collar source with respect to its anchor."""
    nodes, weights = leggauss(20)
    radius = (lower+upper+(upper-lower)*nodes)/2
    return (upper-lower)/2*np.dot(weights,48*(1-64*(radius-1)**2)/radius**3)


def assemble(edges, vector, lapse, *, trace_radius=1., tensor_continuity=1, verify_generators=False, sample_regions=None):
    shape = splines(edges, tensor_continuity)
    n = len(shape.c)*4
    samples = []
    generators = []
    sample_radii = []
    kinetic, spatial = np.zeros((2,n,n))
    shift = np.zeros((2*vector.c.shape[1],n))
    scalar = np.zeros((lapse.c.shape[1],n))
    trace_gauge = np.zeros_like(scalar)
    source = np.zeros(n)
    nodes, weights = leggauss(20)
    for lo, hi in zip(edges[:-1], edges[1:]):
        for r, w in zip((lo+hi+(hi-lo)*nodes)/2, (hi-lo)*weights/2):
            sample_radii.extend([r]*4)
            components = tensor_rows(shape,r)[0]
            samples.append(np.sqrt(w*.8*r*r)*np.sqrt([1,12,2,12])[:,None]*components)
    root = np.linalg.qr(np.vstack(samples), mode="r").T
    def white(rows):
        return solve_triangular(root, rows.T, lower=True).T

    for lo, hi in zip(edges[:-1], edges[1:]):
        for r, w in zip((lo+hi+(hi-lo)*nodes)/2, (hi-lo)*weights/2):
            s = r*r
            components, rc, rd = tensor_rows(shape, r)
            components = white(components)
            h,b,c,d = components
            rc, rd = white(np.array([rc,rd]))
            def angular(amplitudes):
                return (amplitudes*np.array([1,12,2,12]))@components
            mass = components.T@(np.array([1,12,2,12])[:,None]*components)
            factor = w*.8*s
            kinetic += 32*factor*(mass-np.outer(h+2*c,h+2*c)/2)
            spatial_form = (np.outer(rc-h,rc-h)/2+6*np.outer(rc-h,b)-3*np.outer(rd,rd)
                            +12*np.outer(rd,b-d)+2*np.outer(h,c+3*d)
                            +6*np.outer(b,b)-6*np.outer(d,d))
            spatial -= w*.8*(spatial_form+spatial_form.T)/16
            # Same test functions evaluated independently on each region.
            v, vs = vector(s), vector(s,nu=1)
            zero = np.zeros_like(v)
            f_shift = np.column_stack([2*v+4*s*vs,v+s*vs,-v,v])
            g_shift = np.column_stack([6*s*v+4*s*s*vs,s*v,2*s*v,zero])
            shift += factor*angular(np.vstack([f_shift,g_shift]))
            f, fs, fss = lapse(s), lapse(s,nu=1), lapse(s,nu=2)
            lap = s*(14*fs+4*s*fss)
            # Hessian of f(r^2) Y_cart minus the Cartesian trace.
            amps = np.column_stack([2*f+10*s*fs+4*s*s*fss-lap,
                                    f+2*s*fs,2*s*fs-f-lap,f])
            if verify_generators:
                generators.append(np.sqrt(factor*np.array([1,12,2,12]))[:,None]
                                  *np.vstack((amps,f_shift,g_shift)).T)
            scalar += factor*angular(amps)
            trace_gauge += factor*np.outer(-2*lap,h+2*c)
        # Proper-distance source with zeta(1)=0. Its support can cross
        # integration elements. Integrate the radial primitive piecewise.
        lower, upper = max(.875,lo), min(1.125,hi)
        if upper > lower:
            for r,w in zip((upper+lower+(upper-lower)*nodes)/2,(upper-lower)*weights/2):
                components, _, _ = tensor_rows(shape,r)
                path = np.r_[min(r,1), edges[(edges>min(r,1)) & (edges<max(r,1))], max(r,1)]
                primitive = np.zeros(n)
                for a,e in zip(path[:-1],path[1:]):
                    for x,vw in zip((e+a+(e-a)*nodes)/2,(e-a)*weights/2):
                        primitive += vw*tensor_rows(shape,x)[0][0]
                source += w*24*(1-64*(r-1)**2)/r**2*(
                    components[2]+3*components[3]-np.sign(r-1)*primitive/r)
    if verify_generators:
        targets = np.vstack(generators)
        coefficients = solve_triangular(root.T,np.vstack((scalar,shift)).T)
        defects = np.linalg.norm(np.vstack(samples)@coefficients-targets,axis=0)
        relative = max(defects/np.linalg.norm(targets,axis=0))
        assert relative < 1e-8
        print(f"Maximum generator representation defect={relative:.6g}")
    if sample_regions is not None:
        radii = np.asarray(sample_radii)
        values = np.vstack(samples)
        for mask in (radii < .875, (radii >= .875)&(radii <= 1.125), radii > 1.125):
            sample_regions.append(white(values[mask]))
    seam = np.vstack([np.kron(shape(trace_radius**2,nu=j),np.eye(4)) for j in (0,1)])
    return kinetic, spatial, white(source), np.vstack([scalar,shift]), np.vstack([trace_gauge,shift]), white(seam)


def chart(kinetic, spatial, drive, qrows, prows, steps=3, *, spatial_only=False):
    # Pair proper shifts with metric gauges, proper lapses with the
    # projected trace gauge. Include seam delta rows before reduction.
    def normalized(rows):
        # Orthonormal row conventions carry their multiplier Jacobians
        # into the delta functions and Poisson determinant together.
        rows = rows/np.linalg.norm(rows,axis=1)[:,None]
        basis, upper = np.linalg.qr(rows.T, mode="reduced")
        assert np.linalg.matrix_rank(upper) == len(rows)
        return basis.T
    qrows, prows = normalized(qrows), normalized(prows)
    q, p = null_space(qrows), null_space(prows)
    pairing = q.T@p
    def log_volume(rows):
        return np.linalg.slogdet(rows@rows.T)[1]/2
    dirac = np.linalg.slogdet(qrows@prows.T)[1]-log_volume(qrows)-log_volume(prows)
    np.testing.assert_allclose(dirac,np.linalg.slogdet(pairing)[1],atol=2e-7,rtol=0)
    # Change to the canonical p conjugate to the orthonormal q. The
    # induced Dirac density cancels the Jacobian. Retain one real
    # momentum on each link in the first-order Fresnel integral.
    canon = np.linalg.solve(pairing.T,p.T).T
    d = canon.T@kinetic@canon
    d = (d+d.T)/2
    stiffness = q.T@spatial@q
    if spatial_only:
        return stiffness, d, q.T@drive, q, canon
    dt = 1/steps
    diff = np.diff(np.eye(steps+1),axis=0)
    weights = np.ones(steps+1)
    weights[[0,-1]] = .5
    canonical = np.kron(diff,np.eye(len(d)))
    action = np.block([[-dt*np.kron(np.diag(weights),stiffness),canonical.T],
                       [canonical,-dt*np.kron(np.eye(steps),d)]])
    source = np.r_[np.kron(dt*np.sin(np.pi*np.arange(steps+1)/steps),q.T@drive),
                   np.zeros(steps*len(d))]
    return action, source, len(d), dirac


def amplitudes(chart_data, steps=3):
    action, drive, n, dirac = chart_data
    # Keep p on every link. This avoids inversion of the indefinite
    # DeWitt Hessian before evaluating the configuration kernel.
    end = np.r_[0:n,steps*n:(steps+1)*n]
    middle = np.setdiff1d(np.arange(len(drive)),end)
    restricted = action[np.ix_(middle,middle)]
    eig = np.linalg.eigvalsh(restricted)
    assert min(abs(eig)) > 1e-10
    flat = (-n*np.log(2*np.pi)/2-np.linalg.slogdet(restricted)[1]/2
            +1j*np.pi*np.sign(eig).sum()/4)
    flat_response = drive[middle]@np.linalg.solve(restricted,drive[middle])
    # A single L2 metric Gaussian on each physical endpoint, normalized
    # in dq. Eliminate the interior before including the wavefunctions.
    b = action[middle,:][:,end]
    seam = action[np.ix_(end,end)]-b.T@np.linalg.solve(restricted,b)
    endpoint_drive = drive[end]-b.T@np.linalg.solve(restricted,drive[middle])
    eig = np.linalg.eigvalsh(seam)
    packet = flat+n*np.log(2*np.pi)-n*np.log(np.pi)/2-np.log(1-1j*eig).sum()/2
    load = np.linalg.solve(np.eye(len(end))-1j*seam,endpoint_drive)
    return np.array([flat, flat-.005j*flat_response, packet,
                     packet-.005j*flat_response-.005*endpoint_drive@load])


def check(cells, steps=3, *, uncut_only=False, radial_embedding=False):
    edges = np.linspace(0,2,2*cells+1)
    shift = tests(edges,2,1)
    lapse = tests(edges,3,2)
    full = assemble(edges,shift,lapse)
    scalar_count = lapse.c.shape[1]
    shifts = full[3][scalar_count:]
    # For metric gauge S q=0 the shift FP is S S^T. In the same
    # field metric this cancels the orbit integral with delta(S q).
    # QR of S^T evaluates det(S S^T) without squaring the condition number.
    orth_shifts, shift_factor = np.linalg.qr(shifts.T,mode="reduced")
    fp_log = 2*np.log(abs(np.diag(shift_factor))).sum()
    singular = np.linalg.svd(shifts,compute_uv=False)
    assert singular[-1] > 1e-12*singular[0]
    np.testing.assert_allclose(fp_log,2*np.log(singular).sum(),atol=1e-7)
    assert np.linalg.norm(orth_shifts.T@full[2]) < 1e-7*np.linalg.norm(full[2])
    print(f"Proper shift directions={len(shifts)}, log shift FP={fp_log:.9g}")
    direct = chart(*full[:-1], steps=steps)
    if uncut_only:
        flat = amplitudes(direct,steps)
        print(f"cells/side={cells}, steps={steps}, uncut susceptibility="
              f"{(flat[1]-flat[0]).imag/.005:.12g}")
        return
    sides = [assemble(e,shift,lapse) for e in (edges[:cells+1],edges[cells:])]
    left,right = sides
    jump = np.column_stack((left[-1],-right[-1]))
    def sewn_rows(i):
        return np.vstack((np.column_stack((left[i],right[i])),jump))
    sewn = chart(block_diag(left[0],right[0]),block_diag(left[1],right[1]),
                 np.r_[left[2],right[2]],sewn_rows(3),sewn_rows(4),steps=steps)
    a,b = amplitudes(direct,steps),amplitudes(sewn,steps)
    gap = abs(np.expm1(b-a))
    normalized = abs(np.expm1((b[1]-b[0])-(a[1]-a[0])))
    print(f"cells/side={cells}, steps={steps}, canonical pairs={direct[2]}, "
          f"log measure (uncut,cut)=({direct[3]:.7g},{sewn[3]:.7g}), "
          f"flat gaps={gap[:2]}, packet gaps={gap[2:]}, normalized gap={normalized:.3g}")
    from einstein_matched_mesh_frames import frame_checks
    direct_response = (a[1]-a[0]).imag/.005
    radial_generators = None
    if radial_embedding:
        from scipy.interpolate import make_interp_spline
        # W=(4-r^2)Y_cart x/3 has unit normal value at the sphere.
        # It is regular at the center and vanishes at the outer wall.
        radial = make_interp_spline([0.,4.],np.array([[4/3],[0.]]),k=1)
        independent = make_interp_spline([0.,1.,4.],np.array([[16/9],[1.],[0.]]),k=2)
        radial_generators = [
            (assemble(e,radial,lapse)[3][-2:],assemble(e,independent,lapse)[3][-2:])
            for e in (edges[:cells+1],edges[cells:])
        ]
    geometric = frame_checks(sides, steps, direct_response, radial_generators)
    print(f"Uncut flat susceptibility={direct_response:.10g}")
    ratio = np.expm1(.005j*(geometric-direct_response))
    print(f"Geometric-only normalized gap={abs(ratio):.9g}")
    assert direct[2] == sewn[2]
    np.testing.assert_allclose(gap,0,atol=2e-6,rtol=0)
    assert normalized < 1e-9


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", type=int, nargs="+", default=[1,2,4,8])
    parser.add_argument("--steps", type=int, nargs="+", default=[3])
    parser.add_argument("--uncut-only", action="store_true")
    parser.add_argument("--radial-embedding", action="store_true")
    args = parser.parse_args()
    for cells in args.cells:
        for steps in args.steps:
            check(cells, steps, uncut_only=args.uncut_only, radial_embedding=args.radial_embedding)
