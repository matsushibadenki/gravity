# Quantum Information Emergent Gravity (QIEG) Research

QIEG studies whether entropy and spacetime geometry emerge from the same quantum information structure. The microscopic inputs are a subsystem structure, a quantum state, and a self-adjoint Hamiltonian or constraint. The goal is to derive spatial geometry, causal dynamics, and a gravitational response with the same independently calculated coupling in one model.

## What we learned

- Mutual-information distances, diffusion metrics, and dynamical propagation can disagree for the same vacuum. The nearest-neighbor Bell-pair grid has isotropic diffusion and an orientation-dependent entropy density.
- Increasing the number of bond directions can make the flat-space area law isotropic and extend it to spheres and ellipsoids. Matching the reference area density leaves the response to physical perturbations to be tested.
- A linear force changes a Gaussian shell's mean while preserving its regional entanglement. Changes in covariance can change that entropy. The shell's classical curvature contribution appears once in the effective action.
- Clock conditioning and the regional algebra affect replica sewing. Exact synchronization gives canonical sewing. Tracing physical clocks can change the shell entropy and produce a volume term even without a spatial cut.
- Separated slabs retain a distance-dependent information signal after local area subtraction. Complex-momentum branch points explain the distinct decay scales measured in the mixed and unmixed Gaussian sectors.
- Moving a clock-defined ball can change its vacuum entropy even when the state perturbation preserves the entanglement on each fixed cut.

## Established results and their scope

- **Conditional Einstein response.** Vacuum ball modular flow, fixed-volume stationarity, and an orientation-independent area coefficient give linearized semiclassical Einstein response with $G_{\rm N}=1/(4\eta)$ under the stated low-energy assumptions.
- **Low-energy counterexample.** The positive-hopping bond Hamiltonian admits a low-energy tangent whose fixed-volume entropy mismatch remains at order $r^4$. This candidate fails the area-response filter.
- **Linear gravity benchmark.** Solved linearized metric constraints leave two positive-energy tensor polarizations and yield the static Poisson response. The comparison models show that linear dispersion and polarization counting require separate checks.
- **Curved balls in local effective theories.** The Weyl boundary contribution cancels its matter modular term in the tested linear metric theory. The isolated $R^2$ term uses the generalized volume derived from its action. Under identity gluing, the projected connection has zero first-order canonical entropy about the flat reference.
- **Coupled clock.** In the expanding Einstein-scalar comparison, a momentum displacement with unchanged intrinsic metric changes clock density and extrinsic curvature by equal constraint contributions. The apparent clock-energy residual is absent for this perturbation.
- **Moving-ball collar.** A symmetric proper-distance collar gives a finite shape response from the reduced vacuum area and logarithmic terms. In the Einstein area subtraction matched to that collar, the calculated $r^4$ response remains. This result uses a specified local renormalization condition. The smooth gravitational determinant has yet to be matched microscopically to the collar.

- **Local curvature terms on the moving ball.** Evaluated on the solved Einstein-scalar initial data, ordinary metric curvature-squared entropy terms add an area-density shift and no independent first-order shape term. A second profile removes the collar logarithm at order $r^4$ while retaining the area response. Corrected higher-derivative dynamics and clock-dependent terms remain open.

- **Induced clock-foliation terms.** A specified heavy-field proper-time band gives distinct intrinsic-curvature, expansion, and area coefficients. Solving the modified two-derivative constraints leaves a nonzero fixed-volume $r^4$ response in the retained entropy comparison. Higher-derivative and finite clock entropy terms are still open.

- **Four-derivative moving-ball test.** In the luminal member, the same heavy proper-time band induces scalar-curvature, Weyl, and projected-connection terms. The corrected constraints change the clock density, while the retained one-loop boundary entropy leaves a nonzero fixed-volume $r^4$ coefficient. Finite microscopic boundary matching remains open.

- **Shared-regulator volume benchmark.** A common proper-time band for an explicitly chosen light Gaussian completion and the heavy tensor gives matching local cone and action coefficients. The action's Einstein-frame volume leaves a nonzero $r^4$ response for the tested data. The true reduced light operator on the inhomogeneous clock background has yet to be derived.

- **Inhomogeneous light operator.** Constraint substitution gives a scalar bulk Hessian and its canonical configuration measure. A noncollinear Fourier test distinguishes its kinetic response from the minimal scalar completion. On a regulated spherical set of sites, the ADM kinetic block gives a nonzero transported seam response in integer replicas. The complete replica derivative and finite ball coefficient remain open.

- **Reduced clock transfer.** The frozen-reading transfer includes the time, space, and mixed quadratic terms. Its normalized canonical replica derivative can be computed directly, and a separate shared-band integer calculation subtracts the one-sheet trace. These finite tests leave the continuum moved-cut and band-matched entropy coefficient open.

- **Time-dependent transfer.** Both sectors evolve on a common spatial lattice and admit direct canonical replica derivatives at one. Averaging over the lattice cell resolves the reference shape derivative, but the centered state response varies strongly between grid spacings. No continuum fixed-volume cancellation has been established.

- **Adiabatic moving-cut average.** Light and heavy initial covariances now include a first adiabatic correction on the inhomogeneous lattice. The same center average is used for state and boundary motion. The bare responses still do not converge across the tested cutoffs, and the smooth curvature subtraction requires a second background variation of the reduced operator.

- **Quartic light-clock reduction.** The projected second-order lapse and shift give the second background variation of the reduced scalar Hessian and canonical measure. The same spatial lattice gives a smooth finite-band determinant response independent of the moving-ball entropy calculation. The quartic insertion changes the response substantially, and backgrounds with identical intrinsic curvature give different results. Independent curvature counterterms and the continuum fixed-generalized-volume coefficient remain open.

- **Time-dependent ultraviolet control.** A minimal scalar independently reproduces the local curvature and potential coefficients on refined spectral lattices. The curvature coefficient cancels the local continuum cone area term at fixed Einstein-order volume. The full clock and tensor counterterms and the coupled moving-ball coefficient remain open.

## Open problems

- Derive the allowed low-energy states, physical regional algebra, and regulator matching in a single microscopic model that passes the entropy-response filter.
- Match the smooth gravitational determinant and geometric boundary terms to the proper-distance collar. Determine the finite curvature and clock contributions independently and repeat the moving-ball test across perturbation profiles.
- Derive a common causal cone, two gapless tensor polarizations, and the same Newton coupling from vacuum entropy and static response.
- Extend the coupled-clock test to higher-derivative generalized volumes and tilted observers, with a controlled order of limits.
- Establish the integrated long-distance information exponent with independent error controls and a continuum extrapolation. A local gravitational area coefficient requires a separate renormalization condition.

## Research and reproduction

The [research roadmap](roadmap.md) records assumptions, derivations, numerical results, and the entropy-response filter. The [experiments](experiments/) directory contains reproducible Python checks. The Gaussian matrix calculations require NumPy.

Run the latest moving-ball test with:

    python3 -B experiments/proper_distance_collar.py
