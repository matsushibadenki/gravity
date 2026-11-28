"""Source-weighted spectrum of the uncut flat-endpoint Lorentzian integral."""

import argparse

import numpy as np
from scipy.linalg import eigh, null_space, solve_triangular

from einstein_matched_mesh_sewing import assemble, chart, collar_anchor_coefficient, tests


def check(cells, steps, spatial_data, probes, wall, *, fix_wall=False, regions=()):
    stiffness, kinetic, source, metric_lift, momentum_lift = spatial_data
    dt = 1/steps
    restriction = null_space(wall@metric_lift) if fix_wall else np.eye(len(source))
    metric_count = restriction.shape[1]
    stiffness = restriction.T@stiffness@restriction
    # Keep all original constrained momenta in the Fresnel integral.
    momentum_count = len(source)
    if fix_wall:
        assert momentum_count-metric_count == len(wall)
        np.testing.assert_allclose(wall@metric_lift@restriction,0,atol=1e-12)
    source = restriction.T@source
    # The forward difference maps the Dirichlet sine to a link cosine.
    difference = 2*np.sin(np.pi/(2*steps))*restriction.T
    hessian = np.block([[dt*stiffness, -difference], [-difference.T, dt*kinetic]])
    drive = np.r_[np.sqrt(dt/2)*source,np.zeros(momentum_count)]
    eigenvalues, modes = eigh(hessian)
    overlaps = modes.T@drive
    assert np.min(abs(eigenvalues)) > 1e-12
    contributions = overlaps**2/eigenvalues
    bands = np.digitize(abs(eigenvalues), [1e-3,1e-2,1e-1,1,10])
    sums = np.bincount(bands, weights=contributions, minlength=6)
    print(f"cells={cells} links={steps} chi={sum(sums):.10f} bands={sums.round(6)}")
    dominant = np.argmax(abs(contributions))
    print(f"largest signed term={contributions[dominant]:.8g}, "
          f"eigenvalue={eigenvalues[dominant]:.8g}, "
          f"source overlap={abs(overlaps[dominant]):.8g}")
    if steps == 6:
        low = (abs(eigenvalues) >= 1e-3) & (abs(eigenvalues) < 1e-2)
        band_indices = np.flatnonzero(low)
        selected = [("dominant", dominant)]
        tiny = np.flatnonzero(abs(eigenvalues) < 1e-3)
        if regions and tiny.size:
            ranked = tiny[np.argsort(abs(contributions[tiny]))[::-1]]
            print(f"Tiny-band count={len(tiny)}, signed subtotal={sum(contributions[tiny]):.8g}")
            for index in ranked[:3]:
                q, p = np.split(modes[:,index],[metric_count])
                q, p = metric_lift@restriction@q, momentum_lift@p
                def fractions(field):
                    weights = [np.linalg.norm(region@field)**2/np.linalg.norm(field)**2
                               for region in regions]
                    np.testing.assert_allclose(sum(weights),1,atol=1e-9)
                    return np.round(weights,5).tolist()
                scalar, shift = probes
                print(f"Tiny mode lambda={eigenvalues[index]:.8g}, "
                      f"overlap={abs(overlaps[index]):.8g}, contribution={contributions[index]:.8g}, "
                      f"q/p fractions={fractions(q)}/{fractions(p)}, "
                      f"lapse/shift defects={np.linalg.norm(scalar@q)/np.linalg.norm(q):.6g}/"
                      f"{np.linalg.norm(shift@p)/np.linalg.norm(p):.6g}")
        if band_indices.size:
            selected.append(("low band", band_indices[np.argmax(abs(contributions[low]))]))
        for label, index in selected:
            q, p = np.split(modes[:,index],[metric_count])
            q, p = metric_lift@restriction@q, momentum_lift@p
            scalar, shift = probes
            print(f"{label} term={contributions[index]:.7g}, independent "
                  f"lapse/shift defects={np.linalg.norm(scalar@q)/np.linalg.norm(q):.5g},"
                  f"{np.linalg.norm(shift@p)/np.linalg.norm(p):.5g}, "
                  f"wall metric defect={np.linalg.norm(wall@q)/np.linalg.norm(q):.5g}")
    return sum(sums)


def transport_source(full, released_shift, anchor_variation, spatial_data):
    """Move the anchored metric to the released shift slice with its embedding."""
    stiffness, kinetic, source, metric_lift, momentum_lift = spatial_data
    gauge, upper = np.linalg.qr(released_shift.T,mode="reduced")
    coordinates = solve_triangular(upper,gauge.T@metric_lift)
    moved_metric = metric_lift - released_shift.T@coordinates
    moved_anchor = -anchor_variation@coordinates
    np.testing.assert_allclose(gauge.T@moved_metric,0,atol=1e-9)
    moved_source = moved_metric.T@full[2] + collar_anchor_coefficient()*moved_anchor
    np.testing.assert_allclose(moved_source,source,atol=1e-9,rtol=0)
    print(f"Transported completed source defect={np.linalg.norm(moved_source-source):.8g}")
    # The original anchored phase space is transported together with
    # its action. Re-solving with more bulk constraints is a different test.
    return stiffness, kinetic, moved_source, metric_lift, momentum_lift


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", type=int, nargs="+", default=[4,8,16,24,32])
    parser.add_argument("--steps", type=int, nargs="+", default=[6,12,24])
    parser.add_argument("--fix-wall", action="store_true")
    parser.add_argument("--enriched", action="store_true")
    parser.add_argument("--compatible", action="store_true",
                        help="Use continuous tensor quartics with enriched smearings.")
    parser.add_argument("--release-seam-tests", action="store_true")
    parser.add_argument("--radial-modes", action="store_true")
    parser.add_argument("--embedding-check", action="store_true")
    parser.add_argument("--transport-embedding", action="store_true")
    args = parser.parse_args()
    if args.transport_embedding and (not args.embedding_check or args.release_seam_tests):
        parser.error("--transport-embedding requires the anchored --embedding-check")
    if (args.release_seam_tests or args.embedding_check) and not args.compatible:
        parser.error("--release-seam-tests requires --compatible")
    if args.compatible and not (args.fix_wall and args.enriched):
        parser.error("--compatible requires --fix-wall and --enriched")
    if args.radial_modes and any(cells % 8 for cells in args.cells):
        parser.error("--radial-modes requires cell counts divisible by 8 to align the collar.")
    references = {4:40.4503057386,8:69.5459514131,16:113.263426461,
                  24:149.920900490,32:185.640791968}
    for cells in args.cells:
        edges = np.linspace(0,2,2*cells+1)
        shift_continuity, lapse_continuity = (1,2) if args.enriched else (2,3)
        continuity = 0 if args.compatible else 1
        clamp_seam = not args.release_seam_tests
        regions = [] if args.radial_modes else None
        lapse = tests(edges,lapse_continuity,2,clamp_seam=clamp_seam)
        vector = tests(edges,shift_continuity,1,clamp_seam=clamp_seam)
        full = assemble(edges,vector,lapse,trace_radius=2,
                        tensor_continuity=continuity,verify_generators=args.compatible,sample_regions=regions)
        # Angular components c=s*A-B/2 and d=B/2 at the wall.
        traces = full[-1][:4]
        wall = np.vstack((4*traces[0]-traces[1]/2,traces[1]/2))
        wall /= np.linalg.norm(wall,axis=1)[:,None]
        if args.compatible:
            scalar_count = lapse.c.shape[1]
            scalar, shift = np.split(full[3],[scalar_count])
            scalar_basis = np.linalg.qr(scalar.T,mode="reduced")[0]
            shift_basis = np.linalg.qr(shift.T,mode="reduced")[0]
            bracket = np.linalg.norm(scalar_basis.T@shift_basis,ord=2)
            wall_shift = np.linalg.norm(wall@shift_basis,ord=2)
            assert max(bracket,wall_shift) < 1e-7
            print(f"Relative source overlap with shift gauge="
                  f"{np.linalg.norm(shift_basis.T@full[2])/np.linalg.norm(full[2]):.8g}")
            if args.embedding_check:
                # Both Qx and Yx have the same radial harmonic at r=1.
                anchor_variation = -np.tile(vector(1.),2)
                coefficient = collar_anchor_coefficient()
                bulk_variation = shift@full[2]
                total_variation = bulk_variation + coefficient*anchor_variation
                scale = np.linalg.norm(shift,axis=1)*np.linalg.norm(full[2])
                residual = np.max(abs(total_variation)/scale)
                assert residual < 1e-8
                print(f"Embedding source coefficient={coefficient:.10g}, "
                      f"completed shift residual={residual:.6g}, "
                      f"independent embedded shift rows={shift_basis.shape[1]}")
            print(f"Scalar-shift bracket={bracket:.6g}, wall shift defect={wall_shift:.6g}")
        spatial_data = chart(*full[:-1],spatial_only=True)
        enriched_shift = tests(edges,shift_continuity-1,1,clamp_seam=clamp_seam)
        enriched_lapse = tests(edges,lapse_continuity-1,2,clamp_seam=clamp_seam)
        rows = assemble(edges,enriched_shift,enriched_lapse,tensor_continuity=continuity)[3]
        split = enriched_lapse.c.shape[1]
        # Orthonormal row-space coordinates make the defect independent
        # of the choice and normalization of the enriched test basis.
        probes = []
        for block in (rows[:split],rows[split:]):
            _, singular, vectors = np.linalg.svd(block,full_matrices=False)
            probes.append(vectors[singular > 1e-10*singular[0]])
        if args.embedding_check:
            print(f"Canonical pairs before wall restriction={len(spatial_data[2])}")
        if args.transport_embedding:
            released = tests(edges,shift_continuity,1,clamp_seam=False)
            release_rows = assemble(edges,released,lapse,tensor_continuity=continuity)[3]
            transported = transport_source(
                full,release_rows[lapse.c.shape[1]:],-np.tile(released(1.),2),spatial_data)
        for steps in args.steps:
            result = check(cells,steps,spatial_data,probes,wall,fix_wall=args.fix_wall,regions=regions)
            if args.transport_embedding:
                moved_result = check(cells,steps,transported,probes,wall,fix_wall=True)
                np.testing.assert_allclose(moved_result,result,atol=1e-6,rtol=0)
                print(f"Transported susceptibility gap={abs(moved_result-result):.8g}")
            if steps == 6 and cells in references and not (args.fix_wall or args.enriched):
                np.testing.assert_allclose(result,references[cells],atol=1e-6,rtol=0)
