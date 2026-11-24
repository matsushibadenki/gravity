# Quantum Information Emergent Gravity (QIEG) Research Roadmap

Updated 24 November 2026

## Research objective and current scope

QIEG studies whether entropy and spacetime geometry emerge from the same quantum information structure. The microscopic inputs are a subsystem structure, a quantum state, and a self-adjoint Hamiltonian or constraint. The goal is to derive spatial geometry, causal dynamics, and a gravitational response with the same independently calculated coupling in one model.

At low energies, a smooth Lorentzian metric, a local conformal vacuum, an orientation-independent area coefficient, and fixed-volume entanglement equilibrium give the linearized semiclassical Einstein equation. In natural units, the matching is $G_{\mathrm N}=1/(4\eta)$. Its covariant two-derivative completion is $G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G_{\mathrm N}\langle T_{\mu\nu}\rangle$. The completion uses the additional assumption of a two-derivative metric effective theory. Microscopic equilibrium and the values of $\eta$ and $\Lambda$ remain open. [Jacobson, *Entanglement Equilibrium and the Einstein Equation*](https://arxiv.org/abs/1505.04753) · [Casini, Huerta, and Myers, spherical modular flow](https://arxiv.org/abs/1102.0440)

## Status

- 🟢 [Done] Implemented in the current workspace
- 🟠 [Next] High-priority unfinished work
- 🔴 [Later] Planned work after the nearest milestones
- ⭕️ [Pending] On hold because it cannot be tested in the development environment

## Established results

| Test | Result |
|---|---|
| Nearest-neighbor Bell pairs | The diffusion window has spectral dimension three. Shortest paths converge locally to Manhattan distance. The diffusion metric is Euclidean, and the pullback of the BKM metric from single-vertex states is degenerate because those states are identical. |
| Dynamics of a fixed vacuum | A sum of bond projectors and a hopping Hamiltonian can share the same unique vacuum while producing different propagation. At critical positive hopping, the dispersive branch closes quadratically and the vacuum becomes degenerate. |
| Linearized gravity benchmark | First-class constraints leave two positive-energy transverse-traceless (TT) polarizations. The Hamiltonian constraint with a conserved matter source controls the static Newtonian response. A periodic Poisson problem requires a mean-zero density perturbation. An isolated positive mass uses asymptotically flat boundary conditions. |
| Planar entropy | The nearest-neighbor area density is proportional to $\lVert n\rVert_1$ and varies by a factor of $\sqrt3$ with the unit normal $n$. An asymptotically uniform distribution of bond directions makes the planar entropy density and long-wavelength diffusion isotropic. The baseline coefficient is set by the chosen bond entanglement. |

## 1. Curved boundaries in the flat reference model

🟢 [Done] Established the area law and controlled the lattice and bond-length errors for spheres and ellipsoids. Reproduce the checks with `python3 experiments/area_response.py`.

For a region $E$ and bond displacement $v$, the starting points of crossing bonds lie in $E\triangle(E-v)$. Averaging over the lattice origin in a unit cell makes the crossing count times $a^3$ exactly equal to the volume of this symmetric difference. At a fixed origin, any counting discrepancy lies within $O(a)$ of one of the two boundaries. For spheres and ellipsoids of size $r$ and fixed axis ratios, the volume error is $O(ar^2)$, uniformly in the origin.

For $E=T B_1$, an ellipsoid obtained from the unit ball, and $d=|T^{-1}v|\le2$,

$$
|E\triangle(E-v)|
=2\pi |\det T|\,d(1-d^2/12).
$$

With isotropic bond directions of length $L$, $m_a$ directions, and entropy $s_a=2\eta_0 a^3/(m_a L)$ per bond, the leading entropy is $\eta_0 A(E)$. This follows from the transformed area element $|\det T|\,|T^{-\mathsf T}u|d\Omega$. The exact sphere ratio in the origin-averaged, equal-length model is $S/(\eta_0 A)=1-L^2/(12r^2)$. Relative errors are $O(a/L)$, $O((L/r)^2)$, and the error from approximating the angular distribution and bond lengths. At the finest tested lattice, the maximum crossing-volume error over the two tested origins was 0.044% for the sphere and 0.082% for the ellipsoid.

🟠 [Next] Extend the result to a nonuniform reconstructed metric for a dynamically admissible perturbation. Resolve the $r^4$ curvature signal against the errors in the leading $r^2$ area term. Record the order of the continuum limit, the small-ball limit, and the first variation.

## 2. First variations of entropy and the diffusion metric

### Uniform entanglement perturbation

🟢 [Done] Found a fixed-volume counterexample and determined its excitation energy in the regular positive-hopping model. Reproduce the checks with `python3 experiments/area_response.py` and `python3 experiments/uniform_mode.py`.

Uniformly scaling the bond entropies by $\lambda$ scales the unnormalized diffusion generator by $\lambda$. With the diffusion-time normalization fixed at the reference state, $h_\lambda=\lambda^{-1}h_1$. A ball of fixed physical radius $r$ therefore has coordinate radius $\sqrt\lambda r$. Its physical area is constant, while its leading entropy is $S_\lambda=\eta_0\lambda^2 A_h$. In the origin-averaged finite-length sphere calculation this becomes $S_\lambda=\eta_0 A_h[\lambda^2-\lambda L^2/(12r^2)]$. The entropy variation is already nonzero at order $r^2$. At a fixed origin on a finite lattice, crossing counts vary in steps, so differentiation is performed on the averaged formula or its continuum limit.

For a bond vacuum $\cos\theta|00\rangle+\sin\theta|11\rangle$, with $0<\theta<\pi/4$, the entropy derivative with respect to $\theta$ is nonzero. Its uniform tangent is the equal superposition of one orthogonal bond excitation. On a regular hopping graph of degree $z$, this is the bottom of the excitation band, with energy $m=\Delta-zJ$, where $\Delta$ is the local excitation cost and $J\ge0$ is the hopping strength. The operator bound $H\ge m\sum_e Q_e$, with $Q_e$ the projector onto the complement of the bond vacuum, proves that $m>0$ gaps every excitation. At $m=0$ the tangent is an exact zero mode, and for $m<0$ the bond vacuum is unstable. For a uniform bond rotation by $\epsilon$, the variational energy is $M[m\sin^2\epsilon+zJ\sin^4\epsilon]$ for $M$ bonds. At criticality this energy starts at fourth order even though the tangent is an exact zero mode.

### Traceless tensor perturbation

🟢 [Done] Tested whether excluding the uniform entropy perturbation is sufficient for local area matching. It is insufficient for equal-length independent bonds. Reproduce the angular and ellipsoidal checks with `python3 experiments/tensor_response.py`.

Let $Q$ be a real symmetric traceless matrix, and vary the bond entropies on the isotropic shell by the factor $1+\epsilon\,u^{\mathsf T}Qu$, where $u$ is the unit bond direction. This family is realized by varying the Schmidt coefficients of the pure bonds for sufficiently small $\epsilon$. Its angular mean variation vanishes. Normalize the baseline diffusivity to $I$ and keep that normalization fixed. The fourth spherical moment gives $\delta h^{-1}=(2/5)Q$, where $\delta\$ denotes differentiation in $\epsilon$ at zero. For a fixed coordinate plane with unit normal $n$, the induced metric area changes by $\delta dA_h/dA=(1/5)n^{\mathsf T}Qn$. Meanwhile, the bond-crossing entropy per coordinate area changes by

$$
\frac{\delta(dS/dA)}{\eta_0}
=2\langle |u\cdot n|u^{\mathsf T}Qu\rangle_{S^2}
=\frac14n^{\mathsf T}Qn.
$$

For $n$ along the polar axis, the normalized averages of $|u\cdot n|u_z^2$ and $|u\cdot n|u_x^2$ are $1/4$ and $1/8$. Tracelessness gives the result for any orientation. The local difference is therefore $\eta_0 n^{\mathsf T}Qn/20$. A sphere averages this difference to zero at first order. A volume-preserving ellipsoid can retain it. For $Q=\operatorname{diag}(1,-1,0)$ and the unit sphere deformed by $\exp(tQ)$, the derivative at $t=0$ of $\int n^{\mathsf T}Qn\,dA$ is $-64\pi/15$. The metric perturbation itself preserves volume at first order because $\operatorname{tr}Q=0$. This is a counterexample to local matching and to matching on general fixed-volume regions. Spherical entanglement equilibrium and the realization of a physical TT excitation remain separate tests.

A degree-four angular perturbation $P_4(u_z)$ also has zero diffusivity variation, by orthogonality to all polynomial angular components of degree at most two. For a plane normal to the polar axis its fractional entropy response is $2\int_0^1 zP_4(z)\,dz=-1/24$. Thus the second moment that defines the diffusion metric does not determine the full first variation of boundary entropy.

### Two-shell matching and the tensor polarization test

🟢 [Done] Constructed an exactly matched two-shell direction and tested whether rotational symmetry protects it or reduces it to two propagating modes. Reproduce the exact coefficient and quadratic-kernel checks with `python3 experiments/two_shell_response.py`.

Take two isotropic bond populations at lengths $L$ and $2L$, with the same number of directions and the same reference entropy per bond. Let $q_1$ and $q_2$ be their relative quadrupolar amplitudes, multiplying the same traceless tensor $Q$. The entropy weights are proportional to $sL$, and the diffusion weights to $sL^2$. The two coefficients of $n^{mathsf T}Qn$, after dividing the entropy response by $eta_0$, are

$$
C_{
m entropy}=rac{q_1+2q_2}{12},qquad
C_{
m metric}=rac{q_1+4q_2}{25},qquad
C_{
m entropy}-C_{
m metric}=rac{13q_1+2q_2}{300}.
$$

Thus $q=(-2,13)$ gives $C_{
m entropy}=C_{
m metric}=2$. The opposite signs are essential for this choice of reference shell populations and lengths. The microscopic bond entropies remain positive for sufficiently small perturbations. The matching fixes a relative amplitude in the response sector. It does not set the baseline gravitational coupling.

To test dynamical mode selection at quadratic order, introduce canonical traceless tensor coordinates in each shell, with their linear normalization chosen so that they represent the two relative quadrupolar amplitudes. Write $hat f=(-2,13)/sqrt{173}$ and $hat g=(13,2)/sqrt{173}$. For each tensor component, choose a unit kinetic term and the squared-frequency kernel

$$
K(mathbf k)=c_T^2|mathbf k|^2 I_2+M^2hat ghat g^{mathsf T},qquad M>0.
$$

It is positive semidefinite. The matched combination $hat f$ has $omega=c_T|mathbf k|$ and the orthogonal combination $hat g$ has $omega^2=M^2+c_T^2|mathbf k|^2$. This is a quadratic comparison model, and its kernel deliberately uses the amplitude ratio derived from area matching. The shell variables are independent of the scalar and degree-four sectors at this order if rotations are exact. A separate microscopic construction must establish those sectors and control their responses. The two shell copies transform in the same tensor representation, so rotations permit arbitrary real symmetric shell mixing. Even while retaining one zero eigenvalue, a rotation of the soft shell eigenvector away from $hat f$ generically produces a nonzero local area residual.

**Polarization obstruction.** Each soft shell combination contains five unconstrained components of a traceless symmetric spatial tensor. In an unconstrained quadratic model with a positive nonsingular kinetic matrix, an analytic spatial kernel, and exact rotational symmetry of the zero-momentum kernel, a gapless tensor eigenspace at zero momentum contains a full spin-two multiplet. Indeed, rotations act irreducibly on its five components, and the zero-momentum kernel acts as the identity in those tensor indices times a matrix acting on the shell indices. Continuity then gives at least five branches with energies tending to zero as momentum tends to zero. A finite gradient penalty for the divergence changes dispersions but leaves this counting intact. Leaving only two physical polarizations requires a mechanism outside these hypotheses, such as a gauge constraint that removes canonical degrees of freedom for nonzero momentum. The quadratic model above therefore passes the area test in its selected direction and fails the polarization test.

### Local constraint and dispersion test

🟢 [Done] Built a first-class constrained comparison model with two tensor polarizations and identified an obstruction to linear dispersion in its local traceless sector. Reproduce the constraint and dispersion checks with python3 experiments/tensor_constraint.py.

Use the matched shell combination as a traceless symmetric canonical field $q_{ij}$ with traceless momentum $p_{ij}$. Keep the orthogonal shell combination massive and decoupled. In the matched sector impose $C_i=-\partial_j p_{ij}=0$. The constraints commute and generate $\delta q_{ij}=\operatorname{ST}(\partial_i\xi_j)$, where $\operatorname{ST}$ symmetrizes and removes the trace. The gauge map has rank three at nonzero momentum, so five canonical pairs reduce to two. The spatially constant sector is excluded from this finite periodic comparison.

Take an isotropic, parity-even local quadratic Hamiltonian with ordinary positive kinetic term $p_{ij}p_{ij}/2$, no momentum-coordinate mixing, and a symmetric potential kernel on traceless tensors. Gauge invariance requires the kernel to annihilate the gauge shifts and ensures conservation of $C_i$. At order $|k|^2$, rotational covariance gives

$$
(K_2Q)_{ij}=a|k|^2Q_{ij}+b\,\operatorname{ST}(k_iQ_{j\ell}k_\ell).
$$

For momentum along the third axis, the two vector gauge directions have eigenvalue $|k|^2(a+b/2)$. The scalar gauge direction has eigenvalue $|k|^2(a+2b/3)$. Both must vanish, forcing $a=b=0$. A constant rotationally invariant kernel also vanishes if it annihilates the gauge shifts. The obstruction concerns this field content, constraint, and kinetic term.

A positive local kernel is $K_4=\kappa |k|^4\Pi^{\rm TT}(k)$ with $\kappa>0$. The factor $|k|^4$ cancels the projector denominators and makes the symbol polynomial. It annihilates the same gauge directions and gives $\omega=\sqrt{\kappa}|k|^2$ for each of the two physical modes. A kernel $c_T^2|k|^2\Pi^{\rm TT}$ would give linear dispersion but contains a spatial inverse Laplacian in the traceless variables. This comparison establishes two local constrained modes with quadratic dispersion.

The shell ratio is fixed by construction. The local algebraic area residual vanishes along the selected shell direction. Establishing entropy matching for a physical region still requires a prescription for its boundary under gauge transformations. The model also leaves the microscopic vacuum and the matter source constraint open.

### Local linear dispersion and gauge-allowed shell mixing

🟢 [Done] Restored the spatial trace in a local constrained comparison model, defined its area response for a tracked boundary, and tested a gauge-invariant coupling to the massive shell. Reproduce the checks with [gauge_shell_mixing.py](experiments/gauge_shell_mixing.py).

Take the full symmetric spatial metric perturbation $h_{ij}$ with conjugate momentum $\pi^{ij}$ and use the vacuum linearized Einstein Hamiltonian. Lapse and shift impose $C=\partial_i\partial_jh_{ij}-\nabla^2h_{ii}=0$ and $C_i=-2\partial_j\pi^{ij}=0$. These four linear first-class constraints leave two canonical pairs at nonzero spatial momentum. With the standard sign of the Einstein action the reduced vacuum Hamiltonian has positive kinetic and gradient energy and $\omega=c_T|k|$. The trace is part of the constrained field; it adds no propagating scalar in this benchmark. The construction assumes flat reference geometry and the linearized Einstein Hamiltonian.

For a specified surface, let $\zeta^i$ be its embedding displacement from a reference embedding and let $P^{ij}$ project onto the tangent plane. On a specified reference time slice its linear area variation is

$$
\delta A=\frac12\int dA_0\,P^{ij}
\left(h_{ij}+\partial_i\zeta_j+\partial_j\zeta_i\right).
$$

The tangential derivatives of $\zeta$ in this formula depend only on the boundary displacement. Under a spatial gauge transformation $h_{ij}\mapsto h_{ij}+2\partial_{(i}\xi_{j)}$ and $\zeta^i\mapsto\zeta^i-\xi^i$, the geometric result is unchanged. This verifies covariance after specifying which surface is tracked. A microscopic prescription for selecting that surface and defining its entropy remains necessary.

Now include a gauge-inert massive traceless tensor $b_{ij}$ representing the independent shell combination with a nonzero area residual. Use the reconstructed spatial metric as $h$ and take the leading residual to be $\beta n^i n^j b_{ij}$, with $\beta\ne0$ set by the shell normalization. A symmetry-allowed local interaction is proportional to $b^{ij}R^{(1)}_{ij}[h]$, with $R^{(1)}_{ij}$ the linearized spatial Ricci tensor. It commutes with the momentum constraints because $R^{(1)}_{ij}$ is invariant under the linear spatial gauge shift on flat space. It commutes with the Hamiltonian constraint because both depend only on coordinates. Thus the extra interaction preserves the linear constraint evolution.

On each TT component $R^{(1)}_{ij}=|k|^2 h_{ij}/2$. Absorb the factor of two and the field normalizations into the real mixing coefficient $\gamma$. With unit reduced kinetic terms the squared-frequency matrix in the TT sector is

$$
K(k)=
\begin{pmatrix}
c_T^2|k|^2 & \gamma|k|^2\\
\gamma|k|^2 & M^2+v^2|k|^2
\end{pmatrix}.
$$

For $M>0$, $c_T>0$, $v>0$, and $\gamma^2<c_T^2v^2$, this matrix is positive for nonzero $k$. The non-TT massive components decouple from the reduced vacuum TT modes at quadratic order by rotations about $k$. The light branch has

$$
\omega_-^2=c_T^2|k|^2-\frac{\gamma^2}{M^2}|k|^4+O(|k|^6),
\qquad
\frac{b^{\rm TT}}{h^{\rm TT}}=-\frac{\gamma}{M^2}|k|^2+O(|k|^4).
$$

The two light polarizations retain their linear limiting speed. Gauge symmetry permits a local area residual starting at two spatial derivatives, even though the derivative-free matching survives. The residual above is local; its integral on a specific boundary may cancel. In particular, a spherical angular average for a single transverse plane wave can vanish by rotational symmetry. The calculation therefore does not establish failure of spherical entanglement equilibrium. It shows that the two-derivative response must be tested separately from the leading area density. The model imports the metric constraints and selects the entropy observable by construction, so it is a comparison model for microscopic candidates.

### Static conserved source and a fixed-volume ball

🟢 [Done] Tested the static coupling and integrated the local entropy residual on a fixed-volume ball. The calculation is linear in a prescribed conserved source in the comparison model. Reproduce the checks with [static_ball.py](experiments/static_ball.py).

Use $T_{00}=\rho_k\cos(kz)$, $T_{0i}=T_{ij}=0$ on flat background. This source obeys linear conservation and has zero mean in a periodic box. It represents a density perturbation or an external probe. Use $g_{00}=-1-2\Phi$ and $h_{ij}=-2\Psi\delta_{ij}$ in static scalar gauge. Write $A_E=1/(16\pi G_0)$ for the independently specified Einstein-action coefficient and take the static energy mixing to be $g\,b^{ij}R^{(1)}_{ij}$ with unit-normalized massive-shell energy. The symbol $g$ here denotes the coupling, with its sign fixed by the static energy, and its normalization need not equal the reduced TT matrix element in the preceding section.

The lapse constraint gives $\nabla^2\Psi=4\pi G_0\rho$, unchanged by the mixing because the added interaction is lapse independent at this order. The trace-free spatial Ricci tensor is $(\partial_i\partial_j-\delta_{ij}\nabla^2/3)\Psi$. For $D=M^2+v^2 k^2$ and $Q_{ij}=\hat z_i\hat z_j-\delta_{ij}/3$, eliminating the massive static field gives

$$
\Psi_k=-\frac{4\pi G_0}{k^2}\rho_k,\qquad
b_{ij}=\frac{g k^2\Psi_k}{D}Q_{ij}\cos(kz).
$$

The trace spatial equation in this normalization is $4A_E\nabla^2(\Phi-\Psi)=g\partial_i\partial_j b_{ij}$. Its Fourier solution gives the coupling measured by the nonrelativistic potential,

$$
-\frac{k^2\Phi_k}{4\pi\rho_k}
=G_0\!\left[1+\frac{g^2 k^2}{6A_E D}\right].
$$

Thus the static curvature coupling is exactly $G_0$ at this order, and the force coupling tends to $G_0$ as $k\to0$ with a finite-wavelength correction. The entropy-area prescription gives $G_\eta=1/(4\eta_0)$ independently. Equality in the long-wavelength limit holds precisely if $4\eta_0G_0=1$. The two coefficients are separate inputs in this model, and the computation only tests their matching. No independent microscopic prediction of either coefficient is assumed.

Center the ball at the crest $z=0$ and fix its physical volume to the flat reference volume $4\pi r^3/3$. The area change from the metric and boundary displacement is $\delta A|_V=2A_0(\langle\Psi\rangle_{\rm ball}-\langle\Psi\rangle_{\rm surface})$, where $A_0=4\pi r^2$. This follows by imposing the volume constraint on the mean boundary displacement. The flat sphere is stationary against volume-preserving shape changes, so the first-order area result also applies to the corresponding geodesic ball. For $kr\ll1$, $\delta A|_V=-(32\pi^2/15)G_0\rho_k r^4+O(r^6)$ at fixed $k$.

For the independent local entropy residual $\beta n^i n^j b_{ij}$, the field $b$ is already linear in the source, so the first-order integral uses the unperturbed sphere. The constant angular term vanishes. The first surviving term follows from $\int_{S^2}(\mu^2-1/3)\cos(kr\mu)\,d\Omega=-(8\pi/45)(kr)^2+O((kr)^4)$. The resulting fixed-volume residual is

$$
\left.\delta S_{\rm UV}\right|_V-\left.\eta_0\delta A\right|_V
=\frac{32\pi^2\beta gG_0}{45D}\,k^2\rho_k r^4+O(r^6).
$$

At fixed nonzero $k$ this survives at the small-ball curvature order. Relative to $\eta_0\delta A|_V$ its leading coefficient is $-\beta g k^2/(3\eta_0D)$. The term vanishes in the long-wavelength source limit at fixed amplitude in the linear response coefficient, or when $\beta g=0$. A single constant tidal tensor on the reference sphere would miss this term. The numerical probe uses $\eta_0$ chosen to match $G_0$ at zero momentum and verifies both the finite-wavelength force correction and the $r^4$ residual scaling. The prescribed density mode does not itself provide a conformal matter state or its modular entropy. The calculation establishes a mismatch in the modeled UV response, while the full generalized entropy balance remains open.

### Highest-priority follow-up

🟠 [Next] Test whether a microscopic entropy functional or the fixed geometric quantity contributes the compensating two-derivative term. Use multiple conserved source profiles, a matter state with an independently known modular response, and the same coupling normalization. Require independent derivations of $\eta_0$ and $G_0$ before interpreting agreement of their values as a prediction.

## 3. Joint gravitational response in a single model

🟠 [Next] After the entropy-response filter, build a candidate and check its vacuum, self-adjoint generator, clock convention, and preservation of the dynamical constraints.

1. Check for exactly two gapless TT polarizations with positive energy and linear dispersion. Compare their limiting speed with that of matter in the same reconstructed geometry.
2. Define the matter stress tensor independently and verify conservation. Compute the static density response and infer $G_{\mathrm N}$ from the Poisson coefficient.
3. Compute the entropy area coefficient from the same vacuum. Test $4\eta G_{\mathrm N}=1$ and the fixed-volume entropy balance for multiple excitations and observer directions with the same normalization.
4. Record where any mismatch occurs and revise the dependent conclusions. A model passes when the radiative, static, and entropy responses agree.

## Later and pending work

- 🔴 [Later] Determine when dynamics selects a stable $3+1$-dimensional phase without a prescribed spatial lattice or dimension.
- 🔴 [Later] Analyze nonconformal modular response, nonlinear constraint closure, and higher-curvature corrections. Higher derivatives can require changes to the entropy functional and the geometric quantity held fixed. [Bueno et al., *Entanglement equilibrium for higher order gravity*](https://arxiv.org/abs/1612.04374)
- 🔴 [Later] Predict the area coefficient and effective action couplings from microscopic parameters, then calculate an observable deviation from general relativity.
- ⭕️ [Pending] Observational or experimental testing of a quantitative QIEG-specific prediction.

## Consistency checks for every stage

Record the input geometry, symmetries, and fitted parameters. Check signs, units, and boundary conditions. For dimensionless entropy $[\eta]=L^{-2}$ and $G_{\mathrm N}=c^3/(4\hbar\eta)$ in SI units. State how the thermodynamic, continuum, small-ball, and variation limits are ordered. Recheck dependent conclusions after finding a contradiction. Preserve the nearest-neighbor anisotropy, the quadratic critical dispersion, and the TT and static linearized responses as reference cases.
