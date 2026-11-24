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

### CFT modular response and the full first variation in the comparison model

🟢 [Done] Evaluated the vacuum-subtracted CFT state contribution for a static conserved density mode. It cancels the area term at the matched Einstein coupling and leaves the massive-shell entropy residual. Reproduce the quadrature with [cft_ball_balance.py](experiments/cft_ball_balance.py).

Use a free massless Weyl fermion in 3+1 dimensions. In a large infrared box take two positive-energy one-particle modes of the same helicity and momenta $\mathbf p_\pm=(p_\perp,0,\pm k/2)$, with $p_\perp>0$. Their energies are equal, $E=\sqrt{p_\perp^2+k^2/4}$. Form the equal-weight sum and difference of the two one-particle states, choosing their relative phase so that the spinor overlap is real. Each superposition is stationary. For unit-normalized spinors the overlap magnitude is $p_\perp/E$, so the energy-density interference is nonzero. For each state form a positive statistical mixture of the vacuum and that excitation and differentiate the two mixture paths at zero admixture. Their difference removes the common homogeneous stress tensor and selects $\delta\langle T_{00}\rangle=\rho_k\cos(kz)$. Averaging the prepared mixtures over rotations about the wave axis projects onto the scalar sector. Conservation of the free stress tensor ensures that the nonzero Fourier mode satisfies $k\,\delta T^{z\nu}=0$. Transverse stresses need not vanish and can affect the lapse equation, but do not enter the Hamiltonian constraint or the vacuum ball's state modular response. The box is a normalization regulator for the stationary Fourier mode. The modular kernel used below is the infinite-flat-space vacuum kernel, and the comparison is made per unit Fourier amplitude in that limit.

For the reference sphere of radius $r$, the CFT entanglement first law on the fixed flat background gives

$$
\delta S_{\rm matter}
=2\pi\int_{B_r}w\,\delta\langle T_{00}\rangle\,d^3x,
\qquad
w=\frac{r^2-|x|^2}{2r}.
$$

This is the state variation of vacuum-subtracted matter entropy, with the usual ball modular Hamiltonian for the fermionic CFT. A shift of the surface acting on this already first-order matter integrand contributes only at second order. Geometry-dependent vacuum terms belong to the assumed UV/geometry response in this comparison. [Casini, Huerta, and Myers, spherical vacuum modular flow](https://arxiv.org/abs/1102.0440) · [Jacobson, state and geometry variations](https://arxiv.org/abs/1505.04753)

Use $\nabla^2\Psi=4\pi G_0\,\delta\langle T_{00}\rangle$. At the boundary $w=0$ and $\partial_nw=-1$, while $\nabla^2w=-3/r$ in the bulk. Integration by parts gives

$$
\delta S_{\rm matter}
=\frac{1}{2G_0}\left(\int_{\partial B_r}\Psi\,dA_0-\frac{3}{r}\int_{B_r}\Psi\,dV_0\right)
=-\frac{\delta A|_V}{4G_0}.
$$

The last identity uses the fixed-volume area formula in the preceding section. It holds to first order for smooth scalar profiles in this comparison, without expanding in $kr$. Denote the integrated massive-shell term from the preceding section by $\delta S_b$. The modeled total entropy variation is

$$
\delta S_{\rm gen}|_V
=\left(\eta_0-\frac{1}{4G_0}\right)\delta A|_V+\delta S_b.
$$

At $4\eta_0G_0=1$, the entire area contribution cancels at linear order and the residual for the cosine mode is

$$
\delta S_{\rm gen}|_V
=\frac{32\pi^2\beta g G_0}{45(M^2+v^2k^2)}\,k^2\rho_k r^4+O(r^6).
$$

It is nonzero for generic nonzero $\beta g k^2\rho_k$. In the small-ball coefficient, a constant change of $\eta_0$ can compensate it at one chosen wave number, but cannot compensate the different $k$ dependence across the source family. The result is for the assumed entropy functional $\eta_0 A+S_b+S_{\rm matter}$. It does not determine additional geometry-dependent vacuum or regulator terms of a microscopic model. The numerical check independently integrates the modular weight and the shell angular profile, and tests both matched and mismatched area coefficients.

### Curvature compensation across static wavelengths

🟢 [Done] Derived the curvature term that cancels the leading long-wavelength residual, and determined the obstruction to exact matching with a finite local curvature expansion. Reproduce the coefficient checks with [curvature_compensation.py](experiments/curvature_compensation.py).

Keep the matched normalization $4\eta_0G_0=1$. On the specified static slice let $\mathcal R_{ij}$ be the trace-free linearized spatial Ricci tensor. A boundary term proportional to $n^i n^j\mathcal R_{ij}$ is well defined at first order on the tracked sphere. The background curvature is zero, so the first-order integrand may be evaluated on the reference sphere. The massive-shell equation is $(M^2-v^2\nabla^2)b_{ij}=-g\mathcal R_{ij}$. Hence for a single source wave number the remaining entropy, after the matter-area cancellation, is

$$
\delta S_b=-\frac{\beta g}{M^2+v^2 k^2}\, I_{\mathcal R},
\qquad
I_{\mathcal R}=\int_{\partial B_r}n^i n^j\mathcal R_{ij}\,dA_0.
$$

For the cosine density mode, $I_{\mathcal R}$ is of order $k^2\rho_k r^4$ at fixed $k$ and small $kr$. Add a candidate geometric entropy term $\alpha I_{\mathcal R}$. A unique constant $\alpha=\beta g/M^2$ cancels the leading long-wavelength coefficient when $\beta g\ne0$. The remaining response is

$$
\delta S_{\rm gen}|_V
=\frac{\beta g\,v^2 k^2}{M^2(M^2+v^2 k^2)}\,I_{\mathcal R}.
$$

It is of order $k^4\rho_k r^4$ at long wavelength. It remains at order $r^4$ if the small-ball limit is taken at fixed nonzero $k$. A second geometric term proportional to the spatial Laplacian of $\mathcal R_{ij}$ can remove the next power of $k^2$. These are distinct derivative and small-ball expansions.

Within the static metric-only class of boundary terms obtained by applying a finite polynomial $P(-\nabla^2)$ to this trace-free Ricci tensor before contraction with the normal, exact matching on a continuum of wave numbers requires $(M^2+v^2 k^2)P(k^2)=\beta g$. For $v\ne0$ and $\beta g\ne0$ no finite polynomial satisfies this identity. Exact cancellation in this channel instead has kernel $\beta g(M^2-v^2\nabla^2)^{-1}$, with the same spatial boundary conditions as the massive field. This static metric response can be represented using a local expression while retaining the massive field explicitly. It corresponds on shell to a contribution $-\beta\int n^i n^j b_{ij}\,dA_0$. The calculation specifies the required contribution but gives no microscopic reason for its coefficient. It does not classify all independent boundary invariants or all possible microscopic entropy functionals.

### Wald curvature test for two action completions

🟢 [Done] Computed the binormal curvature response of two covariant interactions. The one that preserves the previous static response gives zero explicit Wald correction. The one with a nonzero correction changes the static equations. Reproduce the contractions with [wald_shell_response.py](experiments/wald_shell_response.py).

Introduce a scalar clock with timelike gradient and unit slice normal $u$. Take $b^{\mu\nu}$ to be spatial and trace free. The intrinsic interaction is $-g b^{ij} R^{(3)}_{ij}$ in the action, with the intrinsic Ricci tensor of the clock slice. It reproduces the static energy mixing $+g b^{ij}R^{(1)}_{ij}[h]$ of the comparison model.

In an orthonormal frame with $u=e_0$ and outward normal $n=e_1$, vary $t=R_{0101}$ and its symmetry-related components while keeping the other independent components and fields fixed. The explicit Wald density of a curvature-dependent Lagrangian scalar is $-2\pi\,\partial\mathcal L/\partial t$ in these conventions. The Einstein term gives $4\pi A_E=1/(4G_0)$ because $\partial R/\partial t=-2$. The intrinsic Ricci interaction gives zero: its Gauss expression projects the Riemann tensor entirely into the slice, and its extrinsic-curvature terms contribute nothing to this explicit curvature derivative. This interaction therefore supplies no term $-\beta b_{nn}$ through the tested curvature derivative. [Wald, Noether-charge entropy](https://arxiv.org/abs/gr-qc/9307038)

Replacing the interaction by $-g b^{\mu\nu}R_{\mu\nu}$ with the spacetime Ricci tensor produces a nonzero result. The curvature variation gives $\partial R_{00}/\partial t=1$ and $\partial R_{11}/\partial t=-1$. Since $b$ is spatial, the Wald density becomes $-2\pi g b_{nn}$. Its coefficient equals the previously required $-\beta$ precisely if $\beta=2\pi g$. Neither covariance nor the area matching fixes this equality.

The replacement also changes the static shell source because $R^{(1)}_{ij}=R^{(3,1)}_{ij}-\partial_i\partial_j\Phi$. The shell now responds to the trace-free Hessian of $\Psi-\Phi$ instead of that of $\Psi$. The lapse dependence adds a term proportional to $\partial_i\partial_j b^{ij}$ to the Hamiltonian constraint. The previous CFT matter-area cancellation used the original constraint and cannot be carried over. In the two-operator interpolation between intrinsic and spacetime Ricci, retaining the original off-shell static interaction for arbitrary $\Phi,\Psi,b$ requires the coefficient of the spacetime term to vanish. Its explicit Wald correction then vanishes as well.

This calculation isolates the explicit curvature derivative. A preferred clock need not be regular and invariant at a bifurcation surface, and a fixed-volume ball is not such a horizon. Clock, boundary, replica, and generalized-volume contributions are outside this test. [Bueno et al., generalized volume in causal-diamond equilibrium](https://arxiv.org/abs/1612.04374)

### Static equilibrium with spacetime Ricci mixing

🟢 [Done] Recomputed the static equations and the fixed-volume CFT entropy balance with the same spacetime-Ricci interaction. The explicit Wald contribution cancels the change in the matter-area balance produced by that interaction. An independent shell entropy remains. Run [spacetime_ricci_balance.py](experiments/spacetime_ricci_balance.py) to check the field equations and the sphere integrals.

Use the static scalar sector on the clock slice with $g_{00}=-1-2\Phi$, $h_{ij}=-2\Psi\delta_{ij}$, and the action interaction $-g b^{ij}R_{ij}^{(1)}$. The shell is spatial and traceless, has static stiffness $M^2-v^2\nabla^2$, and vanishes on the reference background. Let $A_E=1/(16\pi G_0)$ and denote the spatial stress trace by $P=\delta\langle T^i{}_i\rangle$. Varying lapse and spatial trace, respectively, gives

$$
4A_E\nabla^2\Psi+g\,\partial_i\partial_j b^{ij}=\rho,\qquad
4A_E\nabla^2(\Phi-\Psi)-g\,\partial_i\partial_j b^{ij}=P.
$$

The first equation contains the lapse term missing from the intrinsic-Ricci comparison. Their sum gives $4A_E\nabla^2\Phi=\rho+P$. For the static Weyl state in the previous test, the stress tensor is traceless at this order, so $P_k=\rho_k$. The coefficient of $\rho+P$ is the usual Einstein coefficient. Inferring a force coupling from $\rho$ alone for this relativistic source would introduce a factor of two from its pressure. A pressureless external perturbation has $P=0$, $\Phi=\Psi$, and no induced shell in this sector.

For the cosine scalar mode, write $b_{ij}=b_k(\hat z_i\hat z_j-\delta_{ij}/3)\cos(kz)$, $D=M^2+v^2k^2$, and $\sigma_k=\Phi_k-\Psi_k$. The static shell equation and the trace equation give

$$
b_k=-\frac{g k^2\sigma_k}{D},\qquad
\sigma_k=-\frac{P_k}{4A_E k^2+2g^2 k^4/(3D)}.
$$

Fix the physical volume of the ball in the matter metric $g_{\mu\nu}$. Use the same vacuum-subtracted CFT state contribution and the same boundary tracking as before. With $w=(r^2-|x|^2)/(2r)$ and $I_b=\int_{\partial B_r} n_i n_j b^{ij}dA_0$, integration by parts gives

$$
\int_{B_r} w\,\partial_i\partial_j b^{ij}dV_0=I_b.
$$

Here $w=0$ and $\partial_n w=-1$ on the sphere, and the bulk Hessian of $w$ is pure trace, so its contraction with $b$ vanishes. Applying the modified lapse constraint to the modular response yields the exact first-order identity

$$
\delta S_{\rm matter}=-4\pi A_E\,\delta A|_V+2\pi g I_b.
$$

The explicit Wald entropy from this same action is $-2\pi g I_b$. In the comparison functional with area coefficient $\eta_0$, matter entropy, explicit Wald entropy, and independent shell contribution $\beta I_b$, the balance is therefore

$$
\delta S_{\rm gen}|_V=(\eta_0-4\pi A_E)\,\delta A|_V+\beta I_b.
$$

The cancellation holds before the small-ball expansion and for any smooth $b$ in this static scalar calculation. Choosing $\beta=2\pi g$ does not remove the full residual when the equations of motion and Wald entropy are changed together. At $\eta_0=4\pi A_E$, nonzero $\beta g P_k k^2$ gives a remaining small-ball term $-(8\pi/45)\beta b_k k^2r^4+O(r^6)$. The numerical experiment checks the scalar equations exactly and integrates the entropy terms at three wave numbers.

A separate check follows from the linear metric shift $h^{E}_{ij}=h_{ij}+(g/A_E)b_{ij}$. The first variation of the Einstein action generates $-g b^{ij}R_{ij}^{(1)}$ with this shift, up to boundary terms and terms quadratic in $b$ needed in the transformed shell action. The volume shift vanishes at first order by tracelessness. The area shift is $-(g/2A_E)I_b$, so the Einstein area density evaluated on the shifted metric gives precisely the explicit Wald correction. This check does not change the metric to which the matter CFT is coupled.

The result applies to the stipulated linear static sector and entropy functional. It does not calculate possible additional clock, boundary, or regulator contributions on the sphere, and $\beta$ is still independent of the action coefficients.

### Microscopic entropy of a linearly driven Gaussian shell

🟢 [Done] Quantized the massive sector with a spatial oscillator regulator and evaluated its independent state entropy. For a positive quadratic Hamiltonian with a linear static drive, its boundary entropy has no source-dependent contribution. Separately checked that the classical curvature term survives shell elimination once. Run [gaussian_shell_entropy.py](experiments/gaussian_shell_entropy.py).

Use independent spatially local canonical variables for the massive shell on a fixed clock slice. At fixed background metric and cut, regulate the theory as a tensor product of oscillator Hilbert spaces. On this regulated space the stable Hamiltonian is

$$
H[J]=\tfrac12 p^{\mathsf T}p+\tfrac12 b^{\mathsf T}K b+J^{\mathsf T}b,
\qquad K>0.
$$

The static force represents the curvature source, and the mean is $\bar b=-K^{-1}J$. Completing the square, the ground state is $|\Omega_J\rangle=D(\bar b)|\Omega_0\rangle$, with $D(\bar b)=\exp(-i\bar b^{\mathsf T}p)$. Since the generator is a sum of local momenta on disjoint oscillator sites, $D=D_B\otimes D_{\bar B}$ for every regulated region $B$. This factorization holds even when the stiffness couples across the cut and $K^{-1}J$ has support on both sides. Partial trace then gives

$$
\rho_B(J)=D_B\rho_B(0)D_B^\dagger,\qquad S_B(J)=S_B(0).
$$

The equality holds at finite regulator and to all orders in the linear force for a fixed stiffness and cut. Consequently the coefficient of an independent state-entropy term $\beta\int_{\partial B}n_i n_j\bar b^{ij}dA$ is zero in this microscopic realization of the shell sector. The same source-only result holds if the background or cut is varied in both the forced and unforced comparisons using the same geometry and stiffness at each step. It leaves the vacuum entropy variation due to changing the geometry, stiffness, or cut undetermined. [Katsinis et al., entanglement in harmonic coherent states](https://arxiv.org/abs/2206.05781)

The two-site verification has nonzero vacuum entanglement because the symmetric and antisymmetric normal modes have different stiffnesses. It checks that the entropy is constant for three different means. Varying a stiffness at zero mean gives a nonzero entropy derivative in the same regulator. Thus a covariance-changing response can carry independent entropy that cannot be inferred from the mean alone. The earlier bond-qubit perturbation changes Schmidt coefficients and is outside the displacement calculation. Imposing a gravitational constraint that changes the regional algebra is also outside this proof.

For the action comparison, eliminate the shell at its classical stationary point, keeping the metric and any prescribed linear source as independent variables before variation. In a presentation where the shell operator is $K$ and its linear source is $J$, the saddle action contains the quadratic response in $J$ obtained by completing the square. The chain rule at the saddle gives $\partial_t S_{\rm eff}=(\partial_t S)|_{\bar b}$ for an independent variation of the normal-plane curvature $t$, since the shell equation removes the term proportional to $\partial_t\bar b$. Applied to the explicit spacetime-Ricci vertex of the preceding section, this reproduces the same $-2\pi g\bar b_{nn}$ curvature contribution, with $\bar b$ now expressed using its Green function. This is a check on that vertex, not a local Wald formula for a nonlocal action. It also follows from the preceding linear metric shift. Adding both versions of the vertex contribution would count it twice. The Gaussian fluctuation determinant and changes in the vacuum entropy with geometry require their own calculation.

With $\beta=0$ for the source-dependent shell entropy in this regulator and $\eta_0=4\pi A_E$, the previously calculated matter, area, and explicit curvature terms cancel at first order in the static comparison. This does not derive $\eta_0=4\pi A_E$ from the same microscopic vacuum. Nor does it settle the geometry-dependent contribution or the definition of regions in the coupled constrained system.

### One-loop vacuum entropy and Newton coupling in the same regulator

🟢 [Done] Matched the leading vacuum area term and the Einstein-action renormalization for a massive Gaussian scalar in four dimensions. This is a regulator benchmark for the shell calculation. Reproduce the coefficient and quadrature checks with [heat_kernel_matching.py](experiments/heat_kernel_matching.py).

Use a real scalar with Euclidean operator $\mathcal D=-\nabla^2+M^2+\xi R$ and the same proper-time lower bound $\epsilon^2$ in the smooth determinant and replica calculations. Define

$$
I(M,\epsilon)=\int_{\epsilon^2}^{\infty}\frac{ds}{s^2}e^{-M^2s}.
$$

On a smooth background the heat trace has the linear curvature coefficient $(1/6-\xi)sR$ multiplying $(4\pi s)^{-2}$ and the mass factor. In the one-loop effective action $W=-\frac12\int ds\,\operatorname{Tr}(e^{-s\mathcal D})/s$, this gives
$-\frac{1/6-\xi}{32\pi^2}I\int\sqrt g\,R$. The Einstein action in Euclidean signature is $-(16\pi G)^{-1}\int\sqrt g\,R$ in these conventions. Therefore,

$$
\Delta(1/G)=\frac{1-6\xi}{12\pi}I(M,\epsilon).
$$

For minimal coupling, use the planar replica cone of opening angle $2\pi n$ times the flat surface. The portion of the heat trace beyond $n$ copies of the smooth trace is $(n^{-1}-n)A e^{-M^2s}/(48\pi s)$. Applying $(n\partial_n-1)W_n$ at $n=1$ gives

$$
S_{\rm plane}=\frac{A}{48\pi}I(M,\epsilon)
=\frac{A}{4}\Delta(1/G)\quad(\xi=0).
$$

The area term is local, so its variation for a tracked smooth surface at fixed proper cutoff and mass is $I\,\delta A/(48\pi)$. A locally planar short-distance expansion suffices for this term. Curvature-dependent logarithms and finite entropy terms on a ball are separate. In the generalized entropy one may use the bare Einstein area coefficient and include the scalar contribution explicitly, or absorb this same area term into the renormalized coefficient. The equality also holds for any common finite proper-time band, by linearity in $I$. [Solodukhin, conical heat kernel and entropy renormalization](https://arxiv.org/abs/1104.3712)

Nonminimal coupling is a diagnostic for the regional prescription. The flat-space canonical plane entropy is unchanged because $R=0$ in the unreplicated Hamiltonian. A regulated geometric cone that includes the curvature at its tip instead adds
$S_{\rm contact}=-2\pi\xi A\langle\phi^2\rangle_\epsilon$, where the flat coincident function is $\langle\phi^2\rangle_\epsilon=I/(16\pi^2)$. With that addition, $S_{\rm plane}+S_{\rm contact}=A\Delta(1/G)/4$ also for $\xi\ne0$. For example, at $\xi=1/6$ the smooth Einstein coefficient has zero shift in this regulator even though the canonical plane entropy is positive. The contact term is part of the gravitational replica response; it is not a change of the flat reduced density matrix. [Solodukhin, nonminimal one-loop renormalization](https://arxiv.org/abs/hep-th/9504022)

The shell in the earlier model is a spatial traceless tensor with a preferred clock, not a minimally coupled covariant scalar. This benchmark does not justify multiplying the scalar result by five. It also does not fix the finite Einstein coefficient or predict $G_0$. Its operational consequence is that the shell comparison must use the same quadratic operator and regularization on smooth and replicated geometries, with any contact terms included once.

### Clock regularity and the planar tensor replica

🟢 [Done] Identified an obstruction to smoothing the replicated clock in the normal plane. Computed the flat canonical Rényi trace and the smooth ultrastatic curvature coefficient for a specified spatial tensor operator. Run [clock_replica.py](experiments/clock_replica.py) for the winding and normalization checks.

On the flat slice take a real unconstrained spatial symmetric traceless tensor with five components. For an ultrastatic Euclidean metric $d\tau^2+h_{ij}dx^idx^j$ and clock $T=\tau$, use the positive quadratic operator
$\mathcal D_b=-\partial_\tau^2+v^2\nabla_h^*\nabla_h+M^2$ on the spatial symmetric traceless bundle. Here $\nabla_h^*\nabla_h$ is the nonnegative Bochner Laplacian and $v>0$. There is no curvature endomorphism in this comparison. The regional algebra on the flat slice is the tensor product of the five oscillator components at each regulated site. This specifies the massive shell sector, with no gravitational constraint or fluctuating clock included in its regional algebra.

For the canonical replica trace, cyclically glue the flat components across the cut in their original Cartesian frame. With $x'=x/v$ this is five scalar Gaussian planar replicas. The physical surface has area $A$ and the rescaled surface area is $A/v^2$. Using the same operator proper-time bound $\epsilon^2$ as in the smooth determinant, the area coefficient is

$$
\frac{S_{\rm can}}{A}=\frac{5}{48\pi v^2}\,I(M,\epsilon).
$$

This canonical gluing computes the specified regional trace without constructing a smooth geometric replica of the clock. The smooth ultrastatic heat trace has volume prefactor $v^{-3}(4\pi s)^{-2}$ and curvature term $5s v^2R[h]/6$ inside that prefactor. The one-loop curvature term in the Euclidean action is

$$
W_R=-\frac{5I(M,\epsilon)}{192\pi^2 v}\int d\tau\,d^3x\,\sqrt h\,R[h].
$$

An ultrastatic calculation only fixes the displayed combination: the spacetime and spatial Ricci scalars agree there. Treating this coefficient as an Einstein coefficient of the original metric would yield an area density $5I/(48\pi v)$, which differs from the canonical density when $v\ne1$. This comparison does not identify a Newton coupling. Both factors are consistent with the effective metric $d\tau^2+v^{-2}h_{ij}dx^idx^j$ on this background: its integrated curvature is $v^{-1}$ times the displayed integral and its area is $A/v^2$. The comparison at $v=1$ alone cannot distinguish geometric completions.

To test the missing geometric replica, use a transverse cap disk with smooth polar angle $\theta$ of period $2\pi$. On its outer circle the angular coordinate of the copied plane is $n\theta$ for integer replica index $n$. Take the pullback of the same flat Euclidean Cartesian clock direction on every sheet, and require the clock to stay in the normal two-plane. Relative to a Cartesian frame on the cap, the polar basis rotates by $\theta$ while the copied clock components in that basis have angle $\pi/2-n\theta$. The clock winding is $1-n$. A continuous nowhere-zero planar vector on a disk restricts to a degree-zero boundary map into the circle. Hence this clock cannot extend smoothly with nonzero norm for $n>1$ under the stated boundary condition.

A second proof for an invariant clock scalar is local. At the fixed surface, the replica group rotates the normal plane by $2\pi/n$. Invariance forces the normal components of $dT$ to vanish there. If the clock also preserves translations along the planar surface, its tangential derivatives vanish too. The projector built from $u=dT/|dT|$ is then undefined at the tip. This proof assumes a real Euclidean clock and the stated replica and tangential symmetries. A clock that tilts along the surface and breaks that symmetry, or an extension whose norm may vanish, is outside the obstruction and needs its own operator and measure. [Lewkowycz and Maldacena, smooth replica covers](https://arxiv.org/abs/1304.4926)

### Punctured cone and the canonical tip condition

🟢 [Done] Matched the punctured-cone boundary to the finite-energy canonical gluing and exhibited an alternative tip prescription with a surviving entropy shift. Reproduce the most slowly converging radial sector with [punctured_cone.py](experiments/punctured_cone.py).

Use the five Cartesian components of the flat shell and rescale spatial coordinates as in the preceding section. The effective cone metric is $dr^2+r^2d\varphi^2$ with period $2\pi n$ for $\varphi$. Remove the disk $r<a$ in these rescaled coordinates. For a Fourier mode $e^{im\varphi/n}$ let $\nu=|m|/n$. For fixed tangential momentum and positive resolvent parameter, write $p>0$ for the resulting radial mass parameter. Homogeneous radial solutions are $I_\nu(pr)$ and $K_\nu(pr)$.

Canonical gluing has no added tip interaction. Its domain is the finite-gradient-energy (Friedrichs) domain: retain the regular $r^\nu$ branch for $\nu>0$ and exclude the logarithmic branch for $\nu=0$. The singular branches have infinite gradient energy even in angular sectors where they are square integrable. On the punctured exterior the exact regular-interior Dirichlet-to-Neumann condition for this resolvent is

$$
a f_m'(a)=pa\,\frac{I_\nu'(pa)}{I_\nu(pa)}f_m(a),
$$

where the derivative points toward increasing $r$. Eliminating the interior in the Gaussian path integral also produces its fixed-boundary determinant. The boundary map alone matches the exterior Green function, and the determinant must be included for a finite-radius partition function. With both factors, this construction is the canonical cone calculation cut at an arbitrary radius. Its tip heat-trace term per rescaled area is the usual $(n^{-1}-n)/(48\pi s)$ times the mass factor per component. It reproduces the canonical entropy density $5I/(48\pi v^2)$ per physical area. [Solodukhin, conical heat kernel](https://arxiv.org/abs/1104.3712)

For comparison, write an exterior radial solution as $I_\nu(pr)+c_aK_\nu(pr)$. At fixed $p$ and $n$, both Dirichlet and Neumann holes suppress $c_a$ as $a\to0$. For $\nu>0$ the suppression is $O((pa)^{2\nu})$. In the zero mode it is only $O(1/|\log(pa)|)$ for Dirichlet and $O((pa)^2)$ for Neumann. This is convergence of individual resolvent modes, rather than an estimate uniform in ultraviolet momenta or replica index. The determinant matching above sets the canonical entropy without an interchange of the hole-radius and proper-time limits.

A tuned Robin condition can retain a different tip. In the zero mode impose $a f'(a)=f(a)/\log(a/\ell)$ at small $a$ for a fixed length $\ell>0$. The limiting domain permits $f(r)\propto\log(r/\ell)$ and has a nonzero resolvent admixture

$$
c_a\longrightarrow \frac{1}{\log(p/\kappa)},\qquad
\kappa=2e^{-\gamma_{\rm E}}/\ell.
$$

The pole is the transverse bound state with eigenvalue $-\kappa^2$. If this extension is used for the massive shell, $M>\kappa$ keeps the full operator positive when the other angular sectors are regular. It changes the spectrum even after the hole has disappeared. A fixed noncanonical extension for every $n$, including one, would already change the unreplicated flat theory, so its determinant is not the canonical entropy. [Kay and Studer, logarithmic core boundary conditions](https://arxiv.org/abs/gr-qc/9510058) · [Kirsten, Loya, and Park, conic self-adjoint extensions](https://arxiv.org/abs/math-ph/0511002)

To test entropy dependence while keeping the unreplicated operator fixed, consider a separate regulated replica prescription. Add a nonnegative tip potential for $n\ge1$ with integral $(n-1)\lambda$ in the transverse plane, spread on a shrinking annulus, where $\lambda\ge0$. Take the replica derivative at one at fixed proper-time cutoff before shrinking the annulus. It contributes $\frac{\lambda}{2}$ times the flat regulated coincident Green function integrated over the surface for each component. Thus the added entropy density per physical area is $5\lambda I/(32\pi^2v^2)$. The one-sheet operator is unchanged, but the replica trace is changed by design. This regulated first-derivative example does not assert the existence of a fixed nonzero point potential in the unregulated continuum. It isolates why agreement of flat operators alone does not fix the tip entropy. The canonical cyclic gluing fixes this freedom by setting the added defect to zero.

### Synchronized microscopic clock and replica gluing

🟢 [Done] Defined a clock on the regulated spatial lattice and derived the canonical replica trace from its physical Hilbert space. Exact synchronization and conditioning give ordinary cyclic gluing without an extra clock-induced tip interaction. Reproduce the constraint and replica-wiring checks with [synchronized_clock_replica.py](experiments/synchronized_clock_replica.py).

Put an ideal canonical clock pair $(T_x,P_x)$ at each site of a finite lattice, with $T_x$ acting by multiplication and $P_x=-i\partial_{T_x}$ on $L^2(\mathbb R)$. Let $H_b$ be the positive finite-lattice oscillator Hamiltonian of the five shell components, independent of these clock coordinates. Choose a reference site $0$ and impose

$$
D_x=T_x-T_0=0\quad(x\ne0),\qquad
C=\sum_x P_x+H_b=0.
$$

All constraint brackets vanish. In particular, the clock momentum sum translates every reading by the same amount, leaving every $D_x$ unchanged. The independent $D_x$ constraints generate shifts of the relative momenta. The gauge $P_x=0$ for $x\ne0$ has an identity bracket matrix with the $D_x$. Equivalently, the canonical one-form on the synchronized slice is $\sum_x P_x\,dT_x=(\sum_x P_x)\,dT$. Reduction leaves one ideal clock $(T,P_T)$ and the constraint $P_T+H_b=0$. The unitary solution is $\psi(t)=e^{-itH_b}\psi(0)$, with the physical norm evaluated on any common clock reading. The remaining gauge condition $T=t$ has unit bracket with $C$. This is a synchronized realization of relational time; exact synchronization and the preferred spatial lattice are inputs. [Page and Wootters, relational clock time](https://doi.org/10.1103/PhysRevD.27.2885)

Define the region algebra after reduction, at the chosen common reading. It acts on the shell oscillators at the sites in $B$. For the reduced state $\rho$ on the full shell lattice the identity

$$
\operatorname{Tr}_B\!\left[(\operatorname{Tr}_{\bar B}\rho)^n\right]
=\operatorname{Tr}\!\left[\rho^{\otimes n}\mathsf{Cycle}_B\right]
$$

holds at integer $n$, where the cyclic permutation acts on the shell sites in $B$ and as the identity elsewhere. The left side is already the normalized conditional trace. Synchronization and the common time fix the clock on each copy; there are no relative clock states to sew at the branch surface and no relative clock Jacobian there. The ground-state Euclidean transfer representation of the reduced shell gives ordinary cyclic gluing. In the flat continuum limit of the specified free shell this selects the finite-energy tip prescription of the preceding section. No extra interaction of the form $(n-1)\lambda b^2$ supported at the tip occurs in this derived conditional trace. The standard cone entropy remains. The numerical check enumerates the two traces through five replicas for an entangled finite-dimensional example. The constraint and trace identities apply to the oscillator model independently of this example.

This microscopic clock is a synchronized reference system. It leaves no propagating local clock fluctuations and does not define a smooth Euclidean unit clock on the replica cap. All relabeling occurs on the regulated time slice, so the winding obstruction for a geometric clock is not used in constructing this trace. The result fixes the canonical entropy for this regional algebra and does not fix the relation between that entropy and a geometric determinant in a dynamical clock theory. A different choice that includes physical clocks in the regional algebra would require a new trace calculation.

### Physical relative clocks at finite synchronization strength

🟢 [Done] Retained physical clock offsets, coupled them to a shell oscillator, and compared two regional algebras under the same reference-clock conditioning. Run [relative_clock_entropy.py](experiments/relative_clock_entropy.py).

Use one ideal reference clock with constraint $P_T+H=0$. At each regulated site, define its local reading as $T+\chi_x$, where $\chi_x$ is a physical oscillator offset with its own conjugate momentum. Condition only on $T=t$, as in the common-reference construction. No measurement of the offsets is made. For one shell component $b$ the comparison Hamiltonian is

$$
H=\tfrac12(p_b^{\mathsf T}p_b+p_\chi^{\mathsf T}p_\chi)
+\tfrac12 b^{\mathsf T}K_b b
+\tfrac12\chi^{\mathsf T}(\Omega^2 I+K_\chi)\chi
+g b^{\mathsf T}\chi.
$$

Take $K_b>0$, $K_\chi\ge0$ and $\Omega>0$. The full stiffness $K$ is positive if $K_b-g^2(\Omega^2 I+K_\chi)^{-1}>0$. This is a regulated one-component model with a chosen shell polarization. It does not assume a rotationally invariant linear coupling between a scalar clock and the full trace-free tensor.

On the ground state of this positive quadratic model, the centered position and momentum covariances are $X=K^{-1/2}/2$ and $P=K^{1/2}/2$. For each regional algebra, restrict $X,P$ to its variables and use the square roots of the eigenvalues of $XP$ as symplectic eigenvalues. The two-site experiment uses symmetric and antisymmetric shell stiffnesses $3,7$ and clock stiffnesses $\Omega^2,\Omega^2+2$. Both tested algebras use one of the two sites:

- For the shell-only algebra, trace all clocks and the shell outside the region. In replicas, sew only the regional shell variables cyclically. The clock fields close on the same sheet everywhere.
- For the joint algebra, sew both clock and shell variables inside the region cyclically. The corresponding entropy is $S_{b\chi}=S_b+S_\chi-I(b:\chi)$ in that region, so treating clock and shell entropy as additive would count their correlations incorrectly.

At zero coupling, $S_b$ agrees with the synchronized shell benchmark, and the joint entropy is additive. At $g=1$ and $\Omega=2$, the shell-only entropy exceeds the benchmark by about $0.019637$ nats at the tested cut, and the clock-shell mutual information is about $0.032382$ nats. At $\Omega=32$ the corresponding values are about $0.0000364$ and $0.0000575$ nats. Reversing the sign of $g$ is a local clock parity transformation and leaves the regional entropies invariant, as checked numerically.

Integrating out the clock on a fixed replica geometry gives a clock determinant and the shell operator $\mathcal D_b-g^2\mathcal D_\chi^{-1}$ with the clock Green function taken in the prescribed sewing domain. In the shell-only trace, the clock determinant is a product of one-sheet determinants and cancels against trace normalization. The shell term persists because the regional shell is sewn differently. In the joint trace the clock determinant itself uses the sewn geometry and need not cancel. These operations follow from the density matrix with no independently added tip potential. A localized continuum contribution could still emerge from the induced kernel; the finite-lattice calculation does not establish one.

At fixed lattice and fixed $g$, letting $\Omega\to\infty$ decouples the clock covariance from the shell and recovers the synchronized shell entropy. This follows directly from the positive stiffness blocks, and the two-site calculation verifies convergence. The result does not justify taking the continuum limit first, since the lattice frequencies can grow with the cutoff.

### Rotationally invariant coupling and noncommuting synchronization limits

🟢 [Done] Built a rotationally invariant Gaussian clock-tensor interaction. Found cutoff-dependent whole-shell entropy before introducing any spatial cut, and established that the continuum and infinite-clock-gap limits of its entropy per site do not commute. Run [clock_tensor_limits.py](experiments/clock_tensor_limits.py).

For a scalar clock offset $\chi$ and spatial symmetric traceless tensor $b_{ij}$, take the local potential mixing

$$
g\int d^3x\,b^{ij}\left(\partial_i\partial_j-\tfrac13\delta_{ij}\nabla^2\right)\chi .
$$

Use unit kinetic terms and diagonal stiffnesses $m_b^2+v_b^2 k^2$ and $\Omega^2+v_\chi^2 k^2$. Only the normalized tensor component along $\sqrt{3/2}(\hat k_i\hat k_j-\delta_{ij}/3)$ couples to the clock at nonzero momentum. Its mixed stiffness has off-diagonal magnitude $|\gamma| k^2$, where $|\gamma|=\sqrt{2/3}|g|$. The condition $\gamma^2<v_b^2v_\chi^2$, with positive masses and speeds, guarantees a positive stiffness. The other four components do not contribute to the whole-species trace. The mixed component belongs to the massive shell field.

At fixed momentum the clock decouples as $\Omega\to\infty$. At fixed $\Omega$ the mixing is of the same order as the diagonal gradient terms at arbitrarily high momentum. For $v_b=v_\chi=1$ and $0<|\gamma|<1$, the two frequencies approach $|k|c_\pm$ with $c_\pm=\sqrt{1\pm|\gamma|}$. The shell-only symplectic eigenvalue of the mixed mode tends to

$$
\nu_\infty=\tfrac14\sqrt{(c_++c_-)(c_+^{-1}+c_-^{-1})}>\tfrac12 .
$$

Thus the oscillator entropy $f(\nu_\infty)$ is strictly positive. This trace retains the shell on the whole periodic lattice and traces every clock, with no spatial boundary. The joint ground state is pure, so this entropy measures correlations with the clocks. For lattice spacing $a$, the entropy per site tends to $f(\nu_\infty)$ if the continuum limit is taken at fixed $\Omega$. Bounded convergence applies to the stable lattice symbol, since almost every dimensionless lattice momentum corresponds to diverging physical momentum. The entropy per physical volume then grows as $a^{-3}$. Taking $\Omega\to\infty$ first at fixed lattice instead gives zero entropy per site.

The experiment uses the nearest-neighbor symbol for $k^2$ in the reduced mixed block. It checks the whole-species entropy and the limiting eigenvalue, while a spatial cut requires the full local tensor variables. For $|\gamma|=0.45$ the limiting entropy is $0.077075$ nats per mixed mode. The numerical lattice at $a=0.025$ gives $0.076977$ nats per site at fixed gap. Taking the gap far above the lattice band suppresses the site value. A fixed ratio of gap to cutoff does not by itself demonstrate that entropy per physical volume vanishes.

The whole-species trace supplies a bulk reference before extracting an entropy associated with the spatial cut. The calculation leaves the area coefficient and its comparison with a renormalized gravity coupling open.

### Spatial slabs after whole-species subtraction

🟢 [Done] Implemented shell-only and joint slab traces with all local tensor components. The finite-lattice results show a nonzero difference between the two regional algebras after the bulk subtraction, consistent with a regulator-dependent area divergence. Run [clock_tensor_slab.py](experiments/clock_tensor_slab.py) with Python and NumPy.

Use a periodic cubic lattice with five components in a local real orthonormal traceless tensor basis $E^A_{ij}$ and one clock offset per site. Use the nearest-neighbor Laplacian $\widehat k^2=4\sum_i\sin^2(k_i a/2)/a^2$ in the diagonal stiffness and set $d_i=\sin(k_i a)/a$. The mixing with component $A$ is $g E^A_{ij}d_i d_j$, the symbol of a local centered-difference Hessian followed by trace removal. Since $|d|^2\le\widehat k^2$, the same sufficient stability bound applies. This local discretization differs near the lattice band edge from the simplified longitudinal symbol used for the previous whole-species experiment. The bulk subtraction here is recomputed with the actual slab regulator.

Fourier transform only the two directions along the cut. Invert the remaining one-dimensional Fourier transform in each block to obtain the slab covariance in the local tensor components, then take the symplectic spectrum. The region $B$ is half the periodic box, so there are two planar interfaces. Translation symmetry gives equal entropies for the two halves. The exact bulk-subtracted shell quantity is

$$
S_b(B)-\tfrac12 S_b(\mathrm{all})
=\tfrac12 I(b_B:b_{\bar B}).
$$

For the joint algebra the analogous quantity is simply $S_{b\chi}(B)$ since the full joint state is pure. It equals half the joint mutual information across the cut and is at least as large as the shell-only quantity by data processing. This gives a regulator-level interpretation of the subtraction and a consistency check independent of a fitted volume coefficient.

In a fixed physical box of size $3.2\times1.6\times1.6$ and fixed clock gap $\Omega=2$, with $\sqrt{2/3}|g|=0.45$, the experiment gives:

| Spacing $a$ | Shell excess per interface site | Joint entropy per interface site |
|---:|---:|---:|
| 0.40 | 0.123045 | 0.146787 |
| 0.20 | 0.119249 | 0.150005 |
| 0.10 | 0.119559 | 0.153384 |

The physical area per interface site is $a^2$. From $a=0.20$ to $a=0.10$, the corresponding entropy densities per physical area grow by factors of approximately $4.01$ and $4.09$. These refinements are consistent with a leading area divergence. At fixed spacing, additional boxes show measurable finite-size effects, so the table does not establish a precise asymptotic coefficient. In the tested finite lattices with $\Omega=100/a$, the shell excess is within $6\times10^{-7}$ nats per interface site of the uncoupled shell. This comparison concerns the shell area observable, not the physical volume density of traced-clock entropy.

The difference between the two traces shows that the spatial-cut response depends on which physical variables are retained. The calculated difference includes ordinary correlations across the cut. It does not identify an extra fundamental tip interaction or a finite universal surface term.

### Equal-area subtraction across stencils and slab widths

🟢 [Done] Compared two spatial derivative stencils at fixed physical box size and three slab widths. An equal-area subtraction leaves a nonzero width-dependent signal consistent across the two regulators at the tested resolutions. Run [slab_finite_entropy.py](experiments/slab_finite_entropy.py) with Python and NumPy.

Keep the diagonal nearest-neighbor Laplacian and vary the derivative used in the mixed Hessian. The centered stencil has $d_i=\sin(k_i a)/a$. The improved stencil multiplies it by $(4-\cos(k_i a))/3$, preserving the same continuum coupling and changing its ultraviolet behavior. Both calculations use all five local shell components. Their stiffness matrices are positive at every sampled momentum. In fact the improved derivative satisfies $|d|^2\le(250/243)\widehat k^2$, so the mixing strength used here remains below the stability bound throughout the lattice band.

In a periodic box of fixed physical size $2.4\times1.2\times1.2$, compare slabs of widths $L_x/4,L_x/2,3L_x/4$. Each slab has the same two parallel boundaries, of total area $A=2L_yL_z$. For either regional algebra define

$$
F(a)=\frac{1}{A}\left[S(L_x/2)-\tfrac12\{S(L_x/4)+S(3L_x/4)\}\right].
$$

A volume term cancels because the mean of the quarter and three-quarter widths equals the half width. Every local term independent of slab width, including the regulator-dependent planar area term, cancels because all interfaces have the same area and orientation. Equivalently $F$ is the difference of the two spatial mutual informations divided by $2A$. This definition leaves the width-dependent correlation contribution, while also canceling any width-independent finite surface term.

With fixed clock gap $\Omega=2$ and mixing $\sqrt{2/3}|g|=0.45$:

| Spacing $a$ | Shell-only centered | Shell-only improved | Joint centered | Joint improved |
|---:|---:|---:|---:|---:|
| 0.300 | 0.06080700 | 0.06350775 | 0.06555267 | 0.06835596 |
| 0.150 | 0.06069788 | 0.06199385 | 0.06331661 | 0.06359865 |
| 0.075 | 0.05971476 | 0.05991272 | 0.06292929 | 0.06301482 |

The entries are nats per unit physical area. The differences between stencils at the finest resolution are about $0.000198$ for the shell-only algebra and $0.000086$ for the joint algebra, while their raw half-slab entropy densities differ by about $23.69$ and $2.20$, respectively. The three refinements provide numerical evidence for a nonzero finite width-dependent term. They do not prove continuum convergence or determine an absolute finite entropy of an isolated boundary.

The uncoupled reference at the finest resolution gives $0.05906079$ for the shell-only algebra and $0.06220620$ for the joint algebra. The interaction-dependent changes are positive in both stencil calculations, but their stencil differences are appreciable relative to those changes. Additional refinement is needed before assigning a continuum value to the interaction-only difference.

### Width dependence and periodic-box effects

🟢 [Done] Varied slab width, normal box length, and transverse box size independently. Recomputed the uncoupled baseline at each configuration. Run [slab_width_decay.py](experiments/slab_width_decay.py) with Python and NumPy.

Use the improved Hessian stencil and the same shell and joint traces. For an axial length $L_x$ and slab width $w$, define the equal-area comparison

$$
F(w,L_x)=\frac{S(L_x/2)-[S(w)+S(L_x-w)]/2}{2L_yL_z}.
$$

The half slab is a reference within each box. This comparison cancels the volume term and every width-independent local contribution. Varying $L_x$ changes the reference width, so it helps diagnose periodic-box effects but does not by itself yield an isolated-interface decay law.

At spacing $a=0.15$, clock gap $\Omega=2$, $\sqrt{2/3}|g|=0.45$, and $L_x=4.8$, $L_y=L_z=1.2$:

| Physical width $w$ | Shell-only $F$ | Joint $F$ | Coupled minus uncoupled shell | Coupled minus uncoupled joint |
|---:|---:|---:|---:|---:|
| 0.6 | 0.08042905 | 0.08206923 | 0.00304353 | 0.00131363 |
| 1.2 | 0.01523118 | 0.01546753 | 0.00010237 | 0.00013118 |
| 1.8 | 0.00246901 | 0.00248994 | 0.00003086 | 0.00003791 |

All entries are nats per unit physical area. The shell and joint differences decrease strictly with width in all four box and lattice configurations tested. Increasing $L_x$ from $4.8$ to $6.0$ at fixed transverse size changes the shell value by about $0.2\%$ at $w=0.6$, and by about $51\%$ at $w=1.8$. Increasing the transverse size from $1.2$ to $1.8$ instead gives shell values $0.042125$, $0.006998$, and $0.001109$ at the three widths. Thus the transverse momentum sampling and the distance to the complementary interface matter for quantitative decay rates.

At fixed physical box size, halving the spacing from $0.30$ to $0.15$ changes the total equal-area differences by roughly $2\%$ to $6\%$. The interaction-only differences are positive in the tested configurations but are more sensitive to this refinement. For instance, at $w=1.2$ and $L_x=4.8$, the shell interaction difference changes from $0.000461$ to $0.000102$. The measurements support a decreasing width-dependent contribution and do not yet determine a continuum interaction-only amplitude or a decay exponent.

### Mutual information of disjoint slabs

🟢 [Done] Computed disjoint-slab mutual information at fixed widths and varying separation. Checked two lattice spacings, two Hessian stencils, and independent changes of the normal and transverse box sizes. Run [disjoint_slab_information.py](experiments/disjoint_slab_information.py) with Python and NumPy.

Use two slabs $B_1,B_2$ of physical width $w=0.6$ with gaps $d$ and $L_x-2w-d$ along the periodic normal direction. All measurements take $d$ to be the shorter gap. For either algebra calculate $I(B_1:B_2)=S(B_1)+S(B_2)-S(B_1\cup B_2)$ directly from the local oscillator covariance of each region. The union uses a noncontiguous set of normal lattice sites. Both local surface and extensive terms cancel, without a half-box entropy reference. Divide by the transverse cross-sectional area $L_yL_z$. This normalization counts one cross section and does not divide out the contribution of the longer periodic gap.

For $a=0.15$, $L_x=9.6$, $L_y=L_z=1.2$, and the improved stencil:

| Shorter gap $d$ | Shell-only mutual information | Joint mutual information | Coupled minus uncoupled shell | Coupled minus uncoupled joint |
|---:|---:|---:|---:|---:|
| 0.6 | 0.12509867 | 0.13665624 | -0.00303628 | +0.00237081 |
| 1.2 | 0.02335848 | 0.02474608 | -0.00084252 | +0.00019703 |
| 1.8 | 0.00531886 | 0.00561929 | -0.00017221 | +0.00010414 |
| 2.4 | 0.00132036 | 0.00139527 | -0.00003401 | +0.00003912 |

All entries are nats per unit cross-sectional area. The total mutual information is positive and decreases with gap in all five configurations. The joint mutual information is at least the shell-only value, as required by data processing. Relative to matched uncoupled baselines, the interaction lowers shell-only mutual information and raises joint mutual information in the sampled configurations. This trend refers to separated slabs; the earlier equal-area differences compared distinct partitions and need not have the same interaction sign.

For the improved stencil at $a=0.15$, increasing the normal box length from $7.2$ to $9.6$ changes the shell result by about $0.36\%$ at $d=0.6$ and $26\%$ at $d=2.4$. At fixed normal length $7.2$, increasing both transverse lengths from $1.2$ to $1.8$ changes the shell density from $0.125546$ to $0.063531$ at $d=0.6$. These comparisons show that the decay rate is not yet controlled by a converged large-box calculation. In particular, the last adjacent-gap logarithmic slope for the shell changes from $1.951$ to $2.322$ when increasing the normal length. These slopes summarize the sampled data and do not identify an asymptotic exponent.

### Highest-priority follow-up

🟠 [Next] Control the transverse-volume limit using direct transverse-momentum integration or larger transverse tori at fixed physical cutoff and gap. Increase the second periodic gap independently before fitting any decay exponent. Keep the shell-only and joint baseline subtractions matched at every regulator. The disjoint-slab observable does not fix a width-independent surface counterterm for the gravitational action.

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
