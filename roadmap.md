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

🟠 [Next] Extend the result to a nonuniform reconstructed metric for a dynamically admissible perturbation. Resolve the $r^4$ curvature signal against the errors in the leading $r^2$ area term using the protocol below.

### Order of limits for a curvature measurement

Use $L_{\rm box}$ for the box size, $L_{\rm bond}$ for the interaction length, $a$ for the lattice spacing, $r$ for the physical radius of the reference ball, and $\epsilon$ for the dimensionless perturbation amplitude. Fix a macroscopic length $R_*$, set by the perturbation or curvature scales, independently of $r$. Fix the physical clock gap $\Omega$, the renormalization prescription, and the definition of the region before taking these limits.

For a matched observable $\mathcal O$ such as $S_{\rm UV}-\eta_0 A_h$, let $\Delta_\epsilon\mathcal O(r)$ be its difference from the reference vacuum. The two regions in this difference have the same physical volume. Take the limits in the following order, from innermost to outermost:

$$
\mathcal C_{\mathcal O}
=\lim_{r/R_*\to0}
\frac{R_*^2}{\eta_0 r^4}
\lim_{\epsilon\to0}
\frac{1}{\epsilon}
\lim_{\substack{L_{\rm bond}\to0\\a/L_{\rm bond}\to0}}
\lim_{L_{\rm box}\to\infty}
\Delta_\epsilon\mathcal O(r).
$$

First take the thermodynamic limit at fixed lattice and physical ball. Then take the continuum limit at fixed $r>0$ and $\epsilon$, with $a/L_{\rm bond}\to0$ along a declared regulator family. Form the first variation at fixed $r$ in that continuum theory, then take the small-ball limit. Match divergent coefficients and subtractions in the same regulator before the continuum limit. This ordering also avoids differentiating lattice boundary membership, which can change in steps at a fixed origin. A derivative taken first on an averaged or smoothly defined lattice region can replace this ordering only with a uniform estimate that justifies exchanging the derivative and continuum limit.

For a finite numerical sequence, set $t=r/R_*\to0$. With a finite positive area coefficient $\eta_0$, the curvature signal in the first variation has scale $\eta_0 r^4/R_*^2$. If an error multiplies the leading $\eta_0 r^2$ term, its dimensionless size must be $o(t^2)$. In particular, where the Section 1 estimates apply, require

$$
\frac{a}{L_{\rm bond}}=o(t^2),\qquad
\left(\frac{L_{\rm bond}}r\right)^2=o(t^2),\qquad
E_{\rm angular}+E_{\rm box}=o(t^2).
$$

Here $E_{\rm angular}$ includes angular quadrature and bond-length approximation errors, and $E_{\rm box}$ is the residual finite-volume error relative to the leading area scale. One sufficient schedule for these particular lattice and bond-length errors is $L_{\rm bond}/R_*=t^{2+\delta}$ and $a/L_{\rm bond}=t^{2+\delta}$ with $\delta>0$. This schedule supplements the hierarchy $a\ll L_{\rm bond}\ll r\ll R_*$. For a nonuniform metric, derive the error bounds for the actual reconstruction and include any additional terms. Bound the errors for the first variation itself. If the available error estimates bound only the two raw entropy values, the resulting error after division by $|\epsilon|$ must still be $o(t^2)$ on the normalized area scale. Control finite-difference bias separately. In particular, geometry and reference-state subtraction must be recomputed for each perturbation amplitude.

An infinite-clock-gap study is a separate limit. Record explicitly whether $\Omega\to\infty$ is taken at fixed $a$ before the continuum, after the continuum at fixed physical $\Omega$, or along a specified joint scaling $\Omega(a)$. Section 2 demonstrates that the first two orders need not agree.

### Nonuniform fixed-volume ball test

🟢 [Done] Isolated a curvature-order counterexample in the isotropic bond response with the leading uniform response removed at the ball center. Run [curved_ball_entropy_filter.py](experiments/curved_ball_entropy_filter.py).

In the equal-length isotropic bond family, multiply the reference entropy of each bond by $\lambda(x)=1+\epsilon f(x)$ at its midpoint. For bounded smooth $f$ and sufficiently small $\epsilon$, each change is realized by varying the Schmidt coefficients of the bond. Take the continuum limit at fixed ball size and perturbation amplitude according to the preceding protocol. The weighted bond midpoint approaches the crossing point as the bond length tends to zero, so the leading entropy in the reference coordinates is $\eta_0\int_{\partial B}\lambda\,dA_{\rm flat}$. This uses the isotropic direction distribution and the same origin-averaged counting prescription or its controlled fixed-origin limit. The limit here is sequential; the calculation does not assume the flat finite-bond $O((L_{\rm bond}/r)^2)$ error estimate for a general nonuniform reconstructed metric.

The diffusion principal symbol is $\lambda(x)\delta^{ij}$ with the reference diffusion-time normalization, so $h_{ij}=\lambda^{-1}\delta_{ij}$. The first derivatives of $\lambda$ also affect the drift, which does not enter the principal symbol. The induced area element in three spatial dimensions is $\lambda^{-1}dA_{\rm flat}$. Hence the entropy per unit physical area is $\eta_0\lambda^2$ in this continuum model. For the ball tracked at fixed physical volume, the reference integrand of $S_{\rm UV}-\eta_0 A_h$ vanishes pointwise. The boundary displacement therefore produces no term in the first variation of this difference:

$$
R_{\rm UV}(r)=2\eta_0 \int_{\partial B_r^{(0)}} f(x)\,dA_0.
$$

Choose $f(x)=\cos(kz)-1$ and center at $z=0$. This has $f(0)=0$ and $\Delta f(0)=-k^2$. It removes the $r^2$ term in the residual while the spatial scalar curvature changes by $\delta R^{(3)}=2\Delta f$. The exact spherical mean of $f$ is $\sin(kr)/(kr)-1$. Thus

$$
\delta A_h|_V=\frac{4\pi}{15}k^2r^4+O(k^4r^6),\qquad
R_{\rm UV}(r)=-\frac{4\pi}{3}\eta_0 k^2r^4+O(\eta_0 k^4r^6).
$$

For the area check, a conformal perturbation $h=(1-\epsilon f)I$ gives $\delta A_h|_V=A_0(\langle f\rangle_{\rm ball}-\langle f\rangle_{\rm surface})$, where $A_0=4\pi r^2$. This includes the boundary displacement needed to hold the physical volume fixed. At first order the same result applies to the geodesic ball because the round reference sphere is stationary for volume-preserving shape changes. Independent numerical angular and radial integrals over four radii give $R_{\rm UV}/(\eta_0\delta A_h|_V)\to-5$.

With $R_*=1/|k|$, the normalized curvature residual tends to $-4\pi/3$. A constant area coefficient fails on this state family if its tangent is admitted as a physical perturbation. The construction establishes a valid microscopic state variation and a nonzero geometric response. It does not show that a particular stable low-energy Hamiltonian admits the spatial profile in its physical sector. Accordingly, the dynamical candidate remains inconclusive unless its allowed perturbations are specified independently. In particular, removing only a homogeneous mode does not itself prove the required local entropy response on the remaining admissible profiles.

### Dynamical admissibility of the nonuniform bond perturbation

🟢 [Done] Constructed a positive local bond Hamiltonian, specified its low-energy window before the entropy test, and checked that the nonuniform tangent is admissible. The $r^4$ mismatch persists for this dynamical candidate. Run [low_energy_curved_ball.py](experiments/low_energy_curved_ball.py).

Use the isotropic bond-product reference states from the preceding test. Each unoriented displacement type has one bond anchored at each cubic lattice site. Write its reference state as $|\phi\rangle=\cos\theta_a|00\rangle+\sin\theta_a|11\rangle$ and choose the orthogonal excitation $|\chi\rangle=\partial_\theta|\phi\rangle$. For bond $e$, set $b_e^\dagger=|\chi\rangle_e\langle\phi|$ and $Q_e=I-|\phi\rangle_e\langle\phi|$. In each displacement type connect anchor sites that differ by one lattice step. The resulting independent hopping graphs have degree six. Their couplings have physical diameter of order $L_{\rm bond}+a$, which vanishes in the continuum limit. On a periodic box define

$$
H_a=(m+6J_a)\sum_eQ_e
-J_a\sum_{\langle e,e'\rangle}(b_e^\dagger b_{e'}+b_{e'}^\dagger b_e),
\qquad J_a=\mathcal D/a^2,\quad m,\mathcal D>0.
$$

The two-site hopping bound gives $H_a\ge m\sum_eQ_e$. The reference state is a unique zero-energy ground state at finite volume, and there is no zero-mode degeneracy. The $\chi$ one-excitation sector is exactly invariant. For every bond type its dispersion is

$$
E_a(\mathbf q)=m+4\mathcal D a^{-2}\sum_i\sin^2(q_i a/2)
\longrightarrow m+\mathcal D|\mathbf q|^2 .
$$

Define admissible first-order perturbations by the excited spectral subspace below a fixed physical energy $E_{\rm cut}$. Choose $E_{\rm cut}>m$ independently of the entropy calculation. The window may contain other excitations; the test tangent lies in the invariant one-excitation sector. Within this spectral window select $k$ so that $m+\mathcal D k^2<E_{\rm cut}$. Multiply the entropy at each bond midpoint by $1+\epsilon[\cos(kz)-1]$. The tangent is proportional to the sum of single $\chi$ excitations weighted by that profile. The bond midpoint only adds orientation-dependent phases to the two nonzero Fourier modes. The tangent therefore has spectral support exactly at $\mathbf q=0$ and $\mathbf q=\pm k\hat z$, below $E_{\rm cut}$ for all sufficiently fine lattices. This is an initial-state perturbation; it evolves under $H_a$ and is not a stationary source. A commensurate sequence of periodic boxes gives the thermodynamic limit of the profile. The spectral criterion is for the tangent of the state at the vacuum, the quantity used by the first-variation filter.

To verify that this perturbation need not become singular as the bond regulator is removed, choose the continuum path $a=L_{\rm bond}\exp(-\ell_*/L_{\rm bond})$ for a fixed physical length $\ell_*>0$ and grow the number of direction types $m_a$ polynomially in $\ell_*/L_{\rm bond}$. The reference entropy per bond is $s_a=2\eta_0a^3/(m_aL_{\rm bond})$. For the small Schmidt probability $p_a=\sin^2\theta_a$, one has $s_a\sim p_a\log(1/p_a)$ and the squared angular derivative with respect to the fractional entropy change is $\theta_a'^2\sim s_a/[4\log(1/p_a)]$. Since $L_{\rm bond}\log(1/p_a)\to3\ell_*$,

$$
\frac{m_a}{a^3}\theta_a'^2\ \longrightarrow\ \frac{\eta_0}{6\ell_*}.
$$

Thus the tangent norm per physical volume is finite and nonzero for a nonzero spatial mean of $f^2$. The quadratic energy per volume is finite as well, by the spectral bound. At fixed small amplitude the product states also have bounded energy density on this path. To see this, let $\alpha_e$ be the relative rotation of bond $e$, $u_e=\sin\alpha_e$, and $w_e=u_e\cos\alpha_e$. The energy equals $m\sum_e u_e^2+J_a\sum_{\langle e,e'\rangle}(w_e-w_{e'})^2+6J_a\sum_e u_e^4$. The first sum per volume is bounded by the squared angular derivative density, the second by smoothness of the midpoint profile and $J_a a^2=\mathcal D$, and the last vanishes as $a/m_a$ at fixed amplitude. This path is a chosen regulator family, not a dynamically predicted scale relation.

Take the continuum at fixed $r$ and small fixed $\epsilon$ and then take the first variation, as in the Section 1 protocol. For the matched physical ball centered at $z=0$, the previous area and entropy calculation applies because the Hamiltonian leaves the reference state and regional algebra unchanged. It yields

$$
\delta A_h|_V=\frac{4\pi}{15}k^2r^4+O(k^4r^6),\qquad
R_{\rm UV}=-\frac{4\pi}{3}\eta_0 k^2r^4+O(\eta_0k^4r^6).
$$

With the independent spectral window, the model therefore fails the Einstein entropy-response filter. This rules out the specified positive-hopping realization, not all possible bond dynamics. The numerical check uses $m=0.25$, $\mathcal D=0.5$, $k=0.8$, and $E_{\rm cut}=0.65$. The limiting energies of the uniform and nonuniform tangent components are $0.25$ and $0.57$. It verifies the Fourier action, the regulator scaling of the tangent, and the fixed-volume coefficient separately. The thermodynamic and continuum arguments are analytic.

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

### Tensor vacuum determinant on non-ultrastatic backgrounds

🟢 [Done] Specified a minimal smooth completion of the Gaussian tensor operator and extracted independent spatial-curvature and kinetic coefficients. Compared them with the canonical planar entropy from the same proper-time band and the same physical metric. Run [tensor_gravity_matching.py](experiments/tensor_gravity_matching.py).

Fix a smooth reference foliation and use a positive constant shell speed $v$ in units where the matter limiting speed is one. The physical Lorentzian metric has lapse $N$, shift $N^i$, and spatial metric $h_{ij}$. Choose the shell effective metric $\widetilde g$ with the same lapse and shift and spatial metric $\widetilde h_{ij}=v^{-2}h_{ij}$. On the Euclidean continuation use a metric-compatible connection on the rank-five spatial traceless tensor bundle and a pure Bochner Laplacian of $\widetilde g$, with mass $M$ and no curvature endomorphism. This is an explicit extension of the ultrastatic operator. The foliation is a prescribed background in this calculation, and other choices of endomorphism or clock couplings can change the result.

The smooth heat trace at linear curvature contains $5\widetilde R/6$. The connection curvature first affects higher heat coefficients in this minimal operator. The positive coefficient multiplying the induced Lorentzian Einstein term of $\widetilde g$ is therefore

$$
C=\frac{5}{192\pi^2}\int_{\epsilon^2}^{\infty}\frac{ds}{s^2}e^{-M^2s}.
$$

The same comparison can be made on a finite proper-time band. The zeroth-derivative term is assumed subtracted by matching the flat background. [Vassilevich, smooth Laplace-type heat coefficients](https://arxiv.org/abs/hep-th/0306138)

The spatial scalar curvature rescales as $\widetilde R^{(3)}=v^2R^{(3)}$, and $\sqrt{\widetilde h}=v^{-3}\sqrt h$. With $v$ constant, the mixed extrinsic curvature $\widetilde K^i{}_j$ equals $K^i{}_j$ because the lapse and shift are unchanged. Dropping the usual bulk total divergence in the ADM decomposition yields

$$
\Gamma_{\rm ind}^{(2)}
=C\int dt\,d^3x\,N\sqrt h\left[
v^{-1}R^{(3)}+v^{-3}(K_{ij}K^{ij}-K^2)\right].
$$

A curved ultrastatic background isolates the first coefficient. A spatially flat time-dependent background can isolate the second. This resolves the ambiguity in the earlier ultrastatic comparison for this chosen completion. [Arnowitt, Deser, and Misner, canonical Einstein action](https://arxiv.org/abs/gr-qc/0405109)

Add a bare two-derivative Einstein term for the matter metric with positive coefficient $A_0$. In the sector with a flat reference, no additional clock terms, and minimal matter coupling to that metric, define

$$
A_R=A_0+C/v,\qquad A_K=A_0+C/v^3,\qquad
\frac{\eta_{\rm can}}{4\pi}=A_0+C/v^2.
$$

The third expression combines the bare Einstein entropy with the canonical planar shell entropy evaluated using the physical area. In the static lapse equation, $K_{ij}=0$, so the linear spatial curvature response to a prescribed nonrelativistic source defines $G_{\rm static}=1/(16\pi A_R)$. The TT kinetic and gradient terms give $c_T^2=A_R/A_K$ relative to matter, and the entropy normalization predicts $4\eta_{\rm can}G_{\rm static}=(A_0+C/v^2)/(A_0+C/v)$. For $C>0$, both quantities equal one only at $v=1$ in this minimal completion. The pure induced limit gives $c_T=v$, as expected from the effective metric. The canonical area discrepancy is fixed in sign by $C(v^{-2}-v^{-1})$. If the only geometric entropy term kept is the area term, an additional area density $4\pi C(v^{-1}-v^{-2})$ would be required to match the static coefficient. The calculation does not derive such a term.

This is a smooth determinant and canonical planar comparison, with the same shell operator on the flat slice. It does not use a smooth clock replica at the cone tip or calculate all curvature-dependent entropy terms on a ball. No finite Einstein coefficient is predicted, and no counterterm is set by the static response. For $v\ne1$ it identifies two necessary mismatches in the specified minimal completion, before a full entropy-response gate is attempted. At $v=1$ the leading coefficients agree in this calculation, while the nonuniform ball, replica prescription in curved geometry, and constraint closure of a dynamical clock remain open.

### Curvature-squared benchmark for the luminal tensor completion

🟢 [Done] Isolated the curvature-squared response fixed by the rank part of the smooth tensor heat coefficient. Evaluated its spherical entropy at fixed physical volume and tested the generalized-volume cancellation in the corresponding local $f(R)$ theory. Run [curvature_squared_ball.py](experiments/curvature_squared_ball.py).

Set $v=1$ in the smooth minimal Bochner completion. In four dimensions the connection-independent part of the next heat coefficient, per component and up to a total derivative, is

$$
\frac{1}{180}(R_{\mu\nu\rho\sigma}^2-R_{\mu\nu}^2)+\frac{1}{72}R^2
=\frac{1}{120}C_{\mu\nu\rho\sigma}^2-\frac{1}{360}E_4+\frac{1}{72}R^2 ,
$$

where $C_{\mu\nu\rho\sigma}$ is the Weyl tensor and $E_4$ is the Euler density. The full bundle coefficient also includes $\operatorname{tr}(\Omega_{\mu\nu}\Omega^{\mu\nu})/12$ for the projected connection curvature $\Omega_{\mu\nu}$. Isolate the $R^2$ term of the rank contribution. For a shared proper-time band $s\in[s_1,s_2]$ its Lorentzian coefficient is

$$
B_R=\frac{5}{2304\pi^2}\int_{s_1}^{s_2}\frac{ds}{s}\,e^{-M^2s}.
$$

This is an induced local coefficient in the band. It is not the finite renormalized $R^2$ coupling of an unspecified microscopic theory. For a local short-distance entropy comparison the band satisfies $\sqrt{s_2}\ll r$ and the curvature varies slowly on this scale. A small-ball extrapolation at fixed band cannot extend through $r\sim\sqrt{s_2}$. [Vassilevich, smooth heat-kernel coefficients](https://arxiv.org/abs/hep-th/0306138)

Use first an ultrastatic reference perturbed by constant spatial sectional curvature $\mathcal K$. The full scalar curvature is $6\mathcal K$, the spacetime Weyl tensor vanishes, and the geodesic sphere in its spatial slice is umbilic. For the metric-curvature part of the usual squashed-cone geometric entropy, the Weyl surface term therefore vanishes and the Euler term has zero first change at fixed sphere topology. The $R^2$ interaction gives $8\pi B_R\int_{\partial B_r}R\,dA$. At fixed physical volume its first change is $8\pi B_RA_0\,\delta R$, where $A_0=4\pi r^2$, so it is proportional to $r^2\delta R$. The area shift is $\delta A|_V=-4\pi r^4\delta\mathcal K/5$. Hence the metric $R^2$ contribution by itself is of lower order in ball radius than the Einstein area response. This statement concerns the indicated geometric entropy term and does not identify the full canonical entropy of the clock-tensor replica. [Fursaev, Patrushev, and Solodukhin, quadratic invariants on squashed cones](https://arxiv.org/abs/1306.4000)

For a controlled comparison take the local action $A_E R+B_R R^2$ and a flat reference, with $A_E$ the matched Einstein coefficient. Its independently defined $f(R)$ generalized volume is $W=V+(3B_R/A_E)\int_B R\,dV$ to first order. At fixed $W$, the volume displacement changes the Einstein area entropy by $-(24\pi B_R/r)\int_B\delta R\,dV_0$. This removes the constant-curvature entropy term exactly and leaves

$$
8\pi B_R\left(\int_{\partial B_r}\delta R\,dA_0
-\frac3r\int_{B_r}\delta R\,dV_0\right)
=\frac{32\pi^2B_R}{15}r^4\Delta\delta R(0)+O(r^6)
$$

for a smooth profile. This is a change of the fixed geometric quantity in a specified higher-derivative model, not a correction obtained by fitting the original area test. [Bueno et al., generalized volume for $f(R)$, Appendix B](https://arxiv.org/abs/1612.04374)

For the isolated static scalar sector of this $f(R)$ comparison, the linear lapse equation is $2A_E\delta G_{00}-4B_R\Delta\delta R=\delta\langle T_{00}\rangle$. The same CFT modular weight $w=(r^2-|x|^2)/(2r)$ takes the $B_R$ part of the source to minus the displayed surface-minus-volume term, by integration by parts. Thus the curvature correction and its matter modular response cancel at fixed $W$ in this static comparison, including nonconstant $\delta R$. The numerical check uses a cosine curvature profile, tests the constant part separately, and reproduces the $r^4$ term at four radii.

The projected-connection test below supplies a canonical comparison on the same regulated cut. Testing the complete tensor determinant still requires the remaining base-metric response and a regional prescription for a dynamical clock.

### Projected connection entropy on the two ball prescriptions

🟢 [Done] Computed the smooth projected-connection coefficient and the first variation of its canonical replica contribution with the same proper-time band. Checked both fixed physical volume and the previously specified $f(R)$ generalized volume. Run [projected_connection_entropy.py](experiments/projected_connection_entropy.py) and [curvature_squared_ball.py](experiments/curvature_squared_ball.py).

Use the luminal minimal Bochner operator and compare it with the same base metric, cut, and regulator but a trivial connection on five internal components. The reference is a flat slice with a constant clock, trivial internal frame, and cyclic gluing by the identity on the fiber. The connection on an ultrastatic curved background is the spatial Levi-Civita connection acting on symmetric traceless tensors. For an orthonormal spatial rotation generator $J$ of unit angle, the generator $J_{(2)}$ on the five tensor components has weights $-2,-1,0,1,2$, and $\operatorname{tr}J_{(2)}^2=-10=5\operatorname{tr}J^2$. Rotational invariance fixes the trace of the product for arbitrary spatial generators. In particular, on an ultrastatic slice,

$$
\operatorname{tr}(\Omega_{\mu\nu}\Omega^{\mu\nu})
=-5\,R^{(3)}_{ijkl}R^{(3)ijkl}.
$$

The smooth one-loop coefficient of this spatial Riemann-square term in the Lorentzian effective action is $-5J/(384\pi^2)$, where $J=\int_{s_1}^{s_2}e^{-M^2s}\,ds/s$. This follows from the bundle heat coefficient $\operatorname{tr}\Omega^2/12$ in the same band as the preceding rank calculation. The term can affect the spatial field equations even though its contribution to the static linear lapse equation about flat space vanishes. On static slices with zero shift the spatial connection curvature is independent of the lapse, and the lapse multiplies an expression already quadratic in the perturbation. [Vassilevich, Laplace-type heat coefficients](https://arxiv.org/abs/hep-th/0306138)

For the canonical replica use the pulled-back spatial connection on every sheet and no separate rotation at the seam. At the flat reference the replicated operator is $D_{n,0}=D^{\rm scalar}_{n,0}\otimes I_5$. The variation due only to the connection is a sum of scalar differential operators times traceless internal generators. The fiber trace of each such term vanishes, so the first variation of the heat trace at each proper time is

$$
\delta_\Omega\operatorname{Tr}e^{-sD_n}
=-s\,\operatorname{Tr}\!\left(e^{-sD_{n,0}}\delta_\Omega D_n\right)=0.
$$

This holds before the proper-time integral, on each regulated replica, for an arbitrary cut and a smooth metric perturbation about the flat trivial connection. It can also be obtained directly for the von Neumann entropy: the reference state and the component-blind regional algebra are invariant under simultaneous constant internal rotations. The only first-order entropy functional of the connection perturbation is its group average, and the average of each rotation generator is zero. This check does not require analytic continuation of the integer identities alone. Variations of the base metric and displacement of the cut enter both comparison operators equally at first order; the response isolated here is their difference. A finite Gaussian replica graph verifies the linear cancellation for one through four sheets and exhibits a nonzero change at quadratic order.

For the same static sector the explicit geometric Wald test also gives zero for the projected-connection term. Its curvature derivative is fully spatial when the clock and its projections are held fixed, so contraction with the normal-plane binormal vanishes. Likewise its explicit contraction with $u_a u_d h_{bc}$ in the metric curvature generalized-volume formula vanishes. These are checks of the spatial operator, not a derivation of a full generalized volume for a dynamical clock. A geometric cap that rotates the fiber already on the flat replicas, or that changes the regional algebra, is a different prescription and is not covered by the canonical trace argument. [Wald, curvature entropy](https://arxiv.org/abs/gr-qc/9307038) · [Bueno et al., generalized volume](https://arxiv.org/abs/1612.04374)

The first-order difference due to the connection is consequently zero through $r^4$ at both fixed $V$ and the independently specified $f(R)$ fixed $W$ of the previous benchmark, because the identity holds cut by cut. For the sum of the isolated $R^2$ term and the projected-connection response, the fixed-volume entropy still has the $8\pi B_R A_0\delta R(0)$ term at $r^2$. With $W$ held fixed it loses that leading term and retains the $r^4\Delta\delta R$ term for a nonuniform profile. The latter cancels the matter modular contribution in the tested static $f(R)$ comparison; the projected connection adds no new term or linear lapse source to that check. Constant curvature gives no such term at fixed $W$. This comparison keeps a finite proper-time band within its local curvature regime.

🟠 [Next] Match any tip prescription beyond identity gluing on nonuniform curved backgrounds. The following section tests the Weyl term in the static metric-sector comparison. A covariant generalized volume for the complete clock theory and the full tensor entropy filter remain open.

### Weyl entropy and the nonuniform static ball balance

🟢 [Done] Computed the Weyl-squared entropy from the same finite proper-time band as the scalar curvature term. Tested the geometric and CFT modular terms against the lapse constraint on nonuniform balls. Run [weyl_ball_balance.py](experiments/weyl_ball_balance.py).

Keep the luminal minimal Bochner operator. For the rank part of the smooth heat coefficient, the $C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}$ term in the Lorentzian action has coefficient

$$
B_C=\frac{5}{3840\pi^2}\int_{s_1}^{s_2}\frac{ds}{s}\,e^{-M^2s}.
$$

The same band and scale separation $\sqrt{s_2}\ll r$ apply on the ball. Use the local comparison action $A_E R+B_R R^2+B_C C^2$ and keep the Euler term as a separate topological entropy constant for spheres, with its topological completion. The generalized volume below is the one for the displayed dynamical action. The previous identity-glued connection test gives no additional linear entropy term. This calculation isolates the metric-curvature sector and does not define an alternative clock-cap or tip prescription. [Vassilevich, heat coefficients](https://arxiv.org/abs/hep-th/0306138)

Let $E_{ij}=\delta C_{0i0j}$ in the orthonormal rest frame of the reference ball. It is symmetric and traceless. The metric squashed-cone entropy contains an extrinsic term quadratic in the trace-free extrinsic curvatures. Both trace-free parts vanish on a round sphere in the flat reference, so that term has no first variation even when the perturbed sphere is not umbilic. The first-order Weyl contribution is therefore the binormal curvature term

$$
\delta S_C=-16\pi B_C\int_{\partial B_r} n^i n^j E_{ij}\,dA_0.
$$

The normalization uses the Lorentzian binormal with squared norm $-2$. A spatially constant $E_{ij}$ averages to zero; odd angular terms also vanish. For a smooth nonuniform profile,

$$
\delta S_C=-\frac{64\pi^2B_C}{15}r^4\,\partial_i\partial_jE_{ij}(0)+O(r^6).
$$

The geometric sphere displacement gives no additional Weyl term at first order because the reference Weyl tensor is zero. [Fursaev, Patrushev, and Solodukhin, Weyl term on a squashed cone](https://arxiv.org/abs/1306.4000)

For a static scalar perturbation with $g_{00}=-1-2\Phi$ and $h_{ij}=-2\Psi\delta_{ij}$, one finds $E_{ij}=\tfrac12\operatorname{ST}(\partial_i\partial_j(\Phi+\Psi))$ and $\delta R=4\nabla^2\Psi-2\nabla^2\Phi$. Here $\operatorname{ST}$ removes the spatial trace. Take $\Psi=\psi_k\cos(kz)$ and $\Phi=2\Psi$. Then $\delta R=0$ and $E_{ij}$ is nonuniform and nonzero. The static linear stress tensor inferred from the covariant metric action is conserved and traceless in this scalar mode; its transverse pressures add to its density and its modulated longitudinal pressure vanishes. The previously constructed rotationally averaged Weyl-fermion density mode has this stress structure and may be normalized to the source amplitude.

Using the same action, the flat-reference linear lapse equation in this sector is

$$
2A_E\delta G_{00}-4B_R\nabla^2\delta R
  +8B_C\,\partial_i\partial_jE_{ij}
=\delta\langle T_{00}\rangle .
$$

For the CFT vacuum modular weight $w=(r^2-|x|^2)/(2r)$, two integrations by parts give
$\int_{B_r}w\,\partial_i\partial_jE_{ij}\,dV_0
=\int_{\partial B_r}n^i n^jE_{ij}\,dA_0$.
The interior term is zero because the Hessian of $w$ is pure trace. The Weyl part of $\delta S_{\rm matter}=2\pi\int w\,\delta\langle T_{00}\rangle$ cancels $\delta S_C$ exactly at this order, before the small-radius expansion. The Weyl term in the generalized volume vanishes since its curvature derivative is trace free and $h_{bc}=g_{bc}+u_bu_c$. Thus the pure-Weyl example has no residual at either fixed physical volume or fixed generalized volume. [Casini, Huerta, and Myers, ball modular flow](https://arxiv.org/abs/1102.0440) · [Bueno et al., generalized volume and linear constraints](https://arxiv.org/abs/1612.04374)

When the scalar-curvature sector is also varied, the constraint-level comparison gives

$$
\left.\delta S_{\rm gen}\right|_V=\frac{24\pi B_R}{r}\int_{B_r}\delta R\,dV_0,\qquad
\left.\delta S_{\rm gen}\right|_W=0,\quad
W=V+\frac{3B_R}{A_E}\int_B R\,dV .
$$

The formulas use the matched Einstein density $4\pi A_E$, the metric entropy of the displayed action, and the state modular response. At fixed $V$ there is generally an $r^2$ term. Even when $\delta R(0)=0$, a nonzero $\Delta\delta R(0)$ leaves $(16\pi^2 B_R/5)r^4\Delta\delta R(0)$ at fixed $V$. This residual is from $R^2$, while the Weyl contribution has already canceled. Holding $W$ removes the scalar term through the Einstein area change. The mixed numerical profile $\delta R=q(\cos(kz)-1)$ is a test of the lapse and entropy identities, not a claim that this scalar mode solves all field equations with a traceless CFT source. The numerical test integrates the surface terms and modular response separately at four radii.

🟠 [Next] The next section extends the linear constraint identity to time-dependent geometry for an aligned clock. A full regulated variational identity still requires the clock regional algebra and its boundary terms.

### Time-dependent metric response and clock energy on the ball

🟢 [Done] Extended the linear constraint comparison to time-dependent metric perturbations on a clock-aligned slice. Identified the missing modular term for a specified classical clock action and checked that the lapse argument depends on observer alignment. Run [clock_aligned_ball.py](experiments/clock_aligned_ball.py).

Let the clock scalar be $T=t+\chi$ around the flat reference. Take $u_\mu=-\partial_\mu T/\sqrt{-g^{\alpha\beta}\partial_\alpha T\partial_\beta T}$ and let $P$ project onto its spatial subspace. Extend the shell connection as the projected spacetime Levi-Civita connection on the spatial traceless tensor bundle. The curvature of the projected connection on the spatial vector bundle consists of the spacetime curvature projected on its two internal indices, plus a term quadratic in $\nabla P$. Since $R_{\mu\nu\rho\sigma}$ and $\nabla P$ are zero in the reference, the linear curvature is just the representation of $\delta R_{\mu\nu ij}$ with spatial internal indices in the unperturbed clock frame. A perturbation of the clock projector contributes only at higher order. This derivation uses the chosen projected connection and does not require a static metric.

Through quadratic order in the perturbations the connection-induced action is proportional to $\delta R_{\mu\nu ij}\delta R^{\mu\nu ij}$. It includes time derivatives of the spatial metric and shift, but no linearized lapse field $h_{00}$ appears in $\delta R_{\mu\nu ij}$. Consequently this term makes no contribution to the linear lapse constraint in the clock frame, even when the metric evolves. The same first-order component-trace argument as for the static canonical replica gives zero connection entropy for the clock-aligned cut with a trivial reference fiber frame and identity sewing. The numerical check evaluates all projected curvature components of a lapse perturbation and exhibits a nonzero time-dependent curvature component from a spatial metric perturbation.

On the clock-aligned round reference ball the linear Gauss relation is $\delta G_{uu}=\delta R^{(3)}/2$ because the reference extrinsic curvature is zero. In the metric part of the linear lapse equation the $R^2$ derivative term reduces to a spatial Laplacian and the Weyl term to the spatial double divergence of $\delta C_{uiuj}$. Antisymmetry removes temporal derivatives in the contracted Weyl term. Thus the previous integrations by parts apply at each reference time, with the same flat reference ball modular weight. At fixed $W=V+(3B_R/A_E)\int_B R\,dV$, the geometric entropy variation is

$$
\delta S_{\rm geom}|_W
=-2\pi\int_{B_r}w\,\delta\rho_{\rm total}\,dV_0,\qquad
w=\frac{r^2-|x|^2}{2r},
$$

when the aligned linear lapse constraint holds for the displayed effective metric theory. Here $\delta\rho_{\rm total}$ includes any independent clock stress in that constraint. This identity refers to each reference slice and does not assume time independence of the metric profiles. [Arnowitt, Deser, and Misner, constraint decomposition](https://arxiv.org/abs/gr-qc/0405109) · [Bueno et al., ball variational identity](https://arxiv.org/abs/1612.04374)

As an explicit classical clock convention, use an irrotational dust action
$S_T=\tfrac12\int\sqrt{-g}\,\lambda(X-1)$ with $X=-g^{\mu\nu}\partial_\mu T\partial_\nu T$. Its multiplier fixes $X=1$, and its stress tensor on that constraint is $\lambda\,\partial_\mu T\partial_\nu T$. Around $T=t$, $\lambda=0$, the clock energy variation is $\delta\rho_T=\delta\lambda$. The norm constraint gives $\dot\chi=\Phi$ for $h_{00}=-2\Phi$, and the linear clock equation gives $\partial_t\delta\lambda=0$. The clock can therefore carry a spatially varying density in the linear lapse constraint. This is a classical stress and synchronization prescription, not a quantum clock vacuum or regional algebra. [Husain and Pawlowski, dust time and the gravitational Hamiltonian](https://arxiv.org/abs/1108.1145)

If only the CFT modular response is included, the difference at fixed $W$ is

$$
\delta S_{\rm geom}|_W+\delta S_{\rm CFT}
=-2\pi\int_{B_r} w\,\delta\rho_T\,dV_0
=-\frac{8\pi^2}{15}\delta\rho_T(0)r^4+O(r^6).
$$

This is the response missing from a CFT-only entropy accounting, not a derivation of the dust entropy. A smooth static density Fourier component verifies the coefficient by direct quadrature. It may be treated as the modulated part of a nonnegative density profile if that restriction is imposed on the classical dust. Whether quantum clock entropy or a change in the physical regional prescription supplies the required contribution remains undecided.

The alignment restriction is essential to the lapse argument. In an observer frame tilted relative to the clock, a clock-spatial basis vector can have a nonzero observer-time component. A lapse perturbation of the tilted observer can then enter the projected curvature. The script gives an explicit nonzero component for such a boost. Therefore the aligned cancellation does not establish an observer-independent variational identity for this clock theory.

🟠 [Next] The next section tests the proposed clock-energy response in an independent quantum scalar probe. The coupled clock state and the tilted geometric response still require their own calculation before the full tensor gate can be applied.

### Quantum clock stress versus its modular response

🟢 [Done] Computed an exact clock-state modular response in a regulated quantum reference model and compared it with the local energy variation. Identified why it cannot supply a universal clock term in the ball identity. Run [quantum_clock_modular.py](experiments/quantum_clock_modular.py).

The preceding dust action does not select a clock vacuum by itself. Its quadratic clock-sector expansion about $T=t$ and $\lambda=0$ on a prescribed metric is $\int\delta\lambda(\dot\chi-\Phi)\,d^4x$. At fixed flat metric this has symplectic term $\delta\lambda\dot\chi$ and no restoring Hamiltonian. Thus it supplies a conjugate pair and the required stress variation but no distinguished Gaussian clock state or regional modular generator. Coupling it to the metric constraints could change the physical state space; this observation concerns the isolated quadratic clock sector. [Husain and Pawlowski, deparametrization with dust](https://arxiv.org/abs/1108.1145)

To test the proposed modular response independently, use a free minimally coupled real scalar clock $\varphi$ quantized with a spatial oscillator regulator, and remove any homogeneous oscillator zero mode by the infrared prescription. Use a local coherent background with $\partial_t\bar\varphi=q\ne0$ and $\nabla\bar\varphi=0$ on the test slice. Smooth finite-volume or compactly supported initial data can realize that profile on a ball. The scalar is an explicit quantum clock probe, with its normalization set by $q$. Its coherent background carries nonzero stress, so this test holds the geometry fixed and does not identify it with the zero-density flat dust solution. The regional algebra contains the scalar canonical variables on the chosen cut; it does not postselect on scalar field values.

Perturb the initial data by $\delta\langle\varphi\rangle=0$ and $\delta\langle\pi_\varphi\rangle=f(x)$, using a coherent displacement of amplitude $\epsilon$. In the locally homogeneous background the minimally coupled stress responses are $\delta T_{00}=q f$, $\delta T_{ij}=q f\delta_{ij}$, and $\delta T_{0i}=0$ on that slice. They are linear in $\epsilon$, with $\delta$ denoting the coefficient. The displacement is generated by local scalar coordinates and factorizes across the spatial cut. If $\rho_{B,0}$ is the regional coherent reference and $K_{B,0}=-\log\rho_{B,0}$, then

$$
\rho_{B,\epsilon}=D_B(\epsilon f)\rho_{B,0}D_B^\dagger(\epsilon f),
\qquad
S(\rho_{B,\epsilon})=S(\rho_{B,0}),\qquad
\left.\frac{d}{d\epsilon}\langle K_{B,0}\rangle_\epsilon\right|_0=0 .
$$

The reference modular operator is the undisplaced one conjugated by the reference displacement. Its quadratic form uses centered momenta, so its expectation begins at order $\epsilon^2$. In contrast, the physical scalar energy uses uncentered momenta and has a nonzero linear cross term with the clock background. This resolves the difference without invoking entropy from a replica-tip insertion. The exact two-site test uses an entangled Gaussian reference with nonzero regional entropy and checks the distinct orders in $\epsilon$. [Katsinis and Pastras, coherent-state Gaussian modular operators](https://arxiv.org/abs/2206.05781)

In a region with smooth $f$ and $f(0)\ne0$, the energy moment that the aligned ball comparison would require is
$2\pi\int_{B_r}w\,\delta T_{00}\,dV_0=(8\pi^2/15)qf(0)r^4+O(r^6)$.
The independent scalar-state entropy computed here supplies none of it. Substituting the vacuum CFT ball weight for the modular Hamiltonian of this clock reference would give a spurious linear response. This is a counterexample to that substitution, not an application of the flat-dust gravity identity to the stressed scalar background.

For an observer of four-velocity $v^\mu=(\gamma,\gamma\mathbf u)$ the local density variation in the same scalar probe is $\delta T_{\mu\nu}v^\mu v^\nu=(2\gamma^2-1)qf$ at the specified point. A fixed tilted flat slice also admits the free-field displacement test for its own regional canonical algebra. This compares the observer dependence of local stress with the probe's state-entropy variation. It does not compute the gravitational lapse, geometric entropy, or dynamical clock selection of that tilted boundary.

🟠 [Next] The following section tests an aligned physical clock state in a coupled Einstein-scalar background. The higher-derivative and tilted clock tests remain open.

### A coupled quantum clock on an expanding reference slice

🟢 [Done] Solved the linear Einstein and scalar-clock constraints on a backreacting background. Defined a regulated regional algebra of the reduced scalar mode and computed its modular response for a physical momentum perturbation. Run [coupled_clock_ball.py](experiments/coupled_clock_ball.py).

Use the two-derivative action $\int\sqrt{-g}[M_{\rm Pl}^2 R/2-(\partial\varphi)^2/2]$, with $M_{\rm Pl}^2=(8\pi G)^{-1}$ and no extra matter. The spatially flat expanding solution has $3M_{\rm Pl}^2H^2=\dot{\bar\varphi}^{\,2}/2$ and $\varepsilon_H=-\dot H/H^2=3$. The monotone scalar is the clock. The slice is defined by its value, and coordinates are fixed in comoving scalar gauge $\delta\varphi=0$ with the scalar spatial shear in $h_{ij}$ set to zero. Use the Einstein generalized volume, which equals the physical volume $W=V$ in this action. This is the leading two-derivative comparison, so the $R^2$ and Weyl generalized-volume terms of earlier sections are outside this calculation.

Write $h_{ij}=a_{\rm FLRW}^2(1+2\zeta)\delta_{ij}$, $N=1+\alpha$, and $N_i=\partial_i\psi$. The linear momentum and Hamiltonian constraints for nonhomogeneous scalar modes give

$$
\alpha=\frac{\dot\zeta}{H},\qquad
\psi=-\frac{\zeta}{H}+\sigma,\qquad
\Delta\sigma=a_{\rm FLRW}^2\varepsilon_H\dot\zeta .
$$

An infrared boundary convention fixes the homogeneous solutions of the elliptic equation. The reduced scalar quadratic action is
$M_{\rm Pl}^2\int a_{\rm FLRW}^3\varepsilon_H
[\dot\zeta^2-a_{\rm FLRW}^{-2}(\nabla\zeta)^2]\,dt\,d^3x$,
with canonical momentum $\pi_\zeta=2M_{\rm Pl}^2a_{\rm FLRW}^3\varepsilon_H\dot\zeta$. Both coefficients are positive on the specified background. The tensor perturbations are held in their reference state. [Maldacena, comoving-gauge constraints and scalar action](https://arxiv.org/abs/astro-ph/0210603)

Select a reference clock reading and a center on a marked integral curve of the clock normals. The physical region is the geodesic ball of fixed physical volume in its uniform-clock slice at that reading. In the regulated linear comparison, use the local canonical algebra of the reduced $\zeta,\pi_\zeta$ variables in the fixed spatial gauge anchored at the center and at the infrared boundary. Choose the Gaussian state of the instantaneous positive reduced Hamiltonian in a Dirichlet box, which removes the zero oscillator without deleting a local canonical variable. This is an initial-state prescription at the chosen clock reading. It does not assume an invariant vacuum throughout the expansion.

Displace only the reduced momentum, with $\delta\zeta=0$ and smooth $\delta\dot\zeta\ne0$, for instance a nonzero cosine mode in the infinite-volume test. The intrinsic spatial geometry and the ball boundary do not shift at this reading to first order. The displacement operator is the exponential of a sum of local $\zeta$ coordinates. It factorizes between the ball and the complement of the regulated reduced algebra. Hence the clock and scalar-geometry regional state is unitarily equivalent to its reference, with $\delta S_{\rm red}=0$ and $\delta\langle K_{B,0}\rangle=0$ at first order. The script obtains $K_{B,0}$ from the restricted covariance on a finite three-dimensional Dirichlet lattice. For a momentum displacement it finds a nonzero modular expectation at quadratic order and no linear term. The exact first-order statement follows from the factorized displacement, not from a fixed-site approximation to a changing cut. An exact nonlinear relational algebra and gravitational edge data are not fixed by this prescription.

The clock energy still changes. With $K=3H$ on the reference and the convention $K_{ij}=\mathcal L_u h_{ij}/2$, the solved initial data give

$$
\delta\rho_\varphi=-\dot{\bar\varphi}^{\,2}\alpha,\qquad
\delta K=-\varepsilon_H\dot\zeta,\qquad
\delta R^{(3)}=0 .
$$

The linear Hamiltonian constraint on the expanding slice is

$$
\delta R^{(3)}+4H\delta K=\frac{2}{M_{\rm Pl}^2}\,\delta\rho_\varphi.
$$

Thus $\delta\rho_\varphi=2 M_{\rm Pl}^2 H\delta K$ for the specified perturbation. In contrast to the earlier flat spacetime reference, the background extrinsic curvature here is nonzero. The variation seen by the intrinsic area formula is the energy combination $\delta\rho_\varphi-2M_{\rm Pl}^2H\delta K$, not the clock energy density alone. At the chosen reading the area at fixed $W=V$ and the reduced entropy are both unvaried. Applying the flat-background ball formula only to the clock density would have generated a spurious term. In the constraint rewritten in ball form, the two weighted moments

$$
2\pi\int_{B_r}w\,\delta\rho_\varphi\,dV_0,\qquad
-2\pi\int_{B_r}w\,2M_{\rm Pl}^2H\delta K\,dV_0
$$

cancel exactly. Each would separately scale as $r^4$ for a nonzero density at the center. The free clock-mode modular energy does not supply this cancellation. The numerical experiment solves the constraints with rational parameters for a mode and integrates the two moments at four radii.

🟠 [Next] Test a constrained perturbation with nonzero intrinsic curvature and a moving relational cut. Add the higher-derivative action and its independently derived fixed quantity only after modeling those responses on the expanding clock background. The present result is an aligned momentum test in the coupled Einstein-scalar model, not the full entropy gate for the clock-tensor candidate.

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

### Transverse momentum integration for separated slabs

🟢 [Done] Replaced the discrete transverse torus by direct integration over the transverse lattice Brillouin zone. Controlled the quadrature separately from the remaining periodic normal direction. Run [transverse_slab_integral.py](experiments/transverse_slab_integral.py) with Python and NumPy.

The slabs are infinite in the two transverse directions at this stage. At fixed spacing $a$, integrate each transverse covariance block against $d\theta_y\,d\theta_z/(2\pi a)^2$. The normal lattice remains periodic. An initial uniform midpoint rule severely under-resolved the low-momentum contribution at large gaps. The retained rule applies Gauss-Legendre quadrature on $x\in[-1,1]$ with $\theta=\pi x^3$ in each direction. The transformed weights for $d\theta/(2\pi)$ are the Gauss-Legendre weights times $3x^2/2$. The cubic map concentrates nodes near zero without changing the integration measure. The two weights in each block are multiplied before summing; the factor $a^{-2}$ converts to physical area density.

At $a=0.15$, width $0.6$, clock gap $2$, and the same improved stencil and coupling as before, the 32-point rule per transverse direction gives the following values on the longer normal lattice $L_x=14.4$:

| Gap $d$ | Shell-only information per area | Joint information per area |
|---:|---:|---:|
| 0.6 | 0.035332227 | 0.044693159 |
| 1.2 | 0.002853921 | 0.003404899 |
| 1.8 | 0.000401599 | 0.000464080 |
| 2.4 | 0.000070635 | 0.000080057 |
| 3.0 | 0.000014016 | 0.000015693 |
| 3.6 | 0.000003004 | 0.000003336 |

At $L_x=9.6$, changing from 24 to 32 points per transverse direction changes the shell result by at most about $1.59\%$ over all sampled gaps. The corresponding maximum change from 16 to 32 points is about $19.1\%$. These are numerical refinement estimates, not rigorous error bounds. At fixed quadrature, increasing $L_x$ from $9.6$ to $14.4$ alters the shell result by about $1.13\%$ at gap $2.4$ and $23.4\%$ at gap $3.6$. The effective shell logarithmic slopes over adjacent gaps in the longer box are $4.19,3.27,2.90,2.70,2.57$ in inverse length units. They still drift and do not establish an asymptotic exponent.

The uncoupled reference uses identical quadrature, normal box, stencil, and spacing. For example, at gap $1.2$ the coupled-minus-uncoupled result is about $-3.97\times10^{-5}$ for the shell-only algebra and $+4.34\times10^{-4}$ for the joint algebra. At gap $0.6$ the shell difference is positive, about $1.47\times10^{-4}$, in this integration, whereas the earlier small transverse tori gave a negative difference. The earlier sign observation is therefore limited to those boxes. Since these differences may be much smaller than the total mutual information, convergence of the total alone is insufficient to establish the interaction-only sign and amplitude throughout the range.

### Disjoint slabs on the infinite lattice

🟢 [Done] Replaced the normal periodic covariance by a direct Fourier integral, removing the periodic image from the disjoint-slab observable. Run [infinite_slab_information.py](experiments/infinite_slab_information.py) with Python and NumPy. The separate cutoff check uses the --refine-cutoff option.

For each transverse momentum, compute the normal covariances as Fourier coefficients of $K^{-1/2}/2$ and $K^{1/2}/2$ on the normal Brillouin zone. Use signed lattice separations in the Fourier phase, without modular reduction. The local tensor variables and the two regional algebras are the same as before. The focused Gauss-Legendre rule is used in all three directions. The normal integration is done on each transverse row to limit memory use. The entropy is still computed for finite widths and gaps in physical units, on an infinite ambient lattice.

At $a=0.15$, width $0.6$, clock gap $2$, and the improved stencil, the 176-point normal rule and 40-point transverse rule give:

| Gap $d$ | Shell-only information per area | Joint information per area |
|---:|---:|---:|
| 0.6 | 0.035332028 | 0.044692966 |
| 1.2 | 0.002853793 | 0.003404765 |
| 1.8 | 0.000401530 | 0.000464024 |
| 2.4 | 0.000070636 | 0.000080059 |
| 3.0 | 0.000014030 | 0.000015704 |
| 3.6 | 0.000003009 | 0.000003340 |

Changing the normal rule from 112 to 176 points changes any entry by less than $0.001\%$ at 32 transverse points. At 176 normal points, changing the transverse rule from 32 to 40 points changes any entry by at most $0.273\%$. These are refinement differences, not certified error bounds. The shell information is positive and below the joint value at every gap. The last effective shell logarithmic slope is $2.566$ in inverse length units; the preceding slopes are $4.194$, $3.269$, $2.896$, and $2.694$. The drift persists without periodic images, so a single exponential fit across these gaps would be misleading.

The matched uncoupled reference gives shell differences of approximately $+1.47\times10^{-4}$ at $d=0.6$ and $-3.97\times10^{-5}$ at $d=1.2$ in this model at $a=0.15$. At $d=3.6$ the shell interaction-only difference is of the same order as the transverse refinement difference in total information. Its sign is unresolved at that separation. The joint interaction increase is larger in these samples.

The separate cutoff check uses $a=0.10$ and keeps the width and gaps fixed. It gives shell information densities $0.03441430$, $0.00281090$, and $2.97755\times10^{-6}$ at gaps $0.6$, $1.2$, and $3.6$. The 32-to-40 transverse refinement changes any coupled result by at most $0.939\%$ at the finer spacing. Across the six gaps the shell total changes by at most $2.60\%$ between spacings. At gap $0.6$, the shell coupled-minus-uncoupled difference changes from $+1.47\times10^{-4}$ to $-9.53\times10^{-5}$. This sign is sensitive to the cutoff and requires refinement of the baseline as well as the coupled observable. No continuum sign is assigned.

### Complex-momentum correlation scale and distant-slab test

🟢 [Done] Derived the continuum branch-point scale, located its counterpart for the actual lattice stencil, and compared the resulting information-decay prediction with larger separations. Run [slab_decay_scale.py](experiments/slab_decay_scale.py) with Python and NumPy.

For equal bare propagation speeds, write $s=k_x^2+|k_\perp|^2$ and specialize to shell mass $1$, clock gap $2$, and normalized mixing $\gamma=0.45$. The longitudinal stiffness determinant is

$$
\det K_\parallel=(1+s)(4+s)-\gamma^2s^2.
$$

The lighter root is $s=-\kappa_0^2$, with $\kappa_0^2=8/(5+\sqrt{9+16\gamma^2})$ and $\kappa_0=0.97022405$. At fixed transverse momentum the branch is at $k_x=i\sqrt{\kappa_0^2+|k_\perp|^2}$. The four unmixed shell components start at mass $1$, and the other mixed root is farther away. The light mixed eigenvector has a nonzero shell component, so the branch is present in both the shell-only and joint observables.

For the lattice at $k_\perp=0$, let $u=\sin^2(k_xa/2)$. The improved stencil has $\widehat k_x^2=4u/a^2$ and $d_x^2=(4u/a^2)(1-u)(1+2u/3)^2$. Replace the continuum diagonal momenta by $\widehat k_x^2$ and the off-diagonal squared by $\gamma^2(d_x^2)^2$. Mapping the determinant roots back to complex $k_x$ gives the closest mixed branch at $\kappa_{\rm lat}=0.96946420$ for $a=0.15$. The unmixed scale is $2\,\mathrm{arsinh}(a/2)/a=0.99906487$. A transverse grid scan of the determinant roots found no smaller imaginary momentum. The continuum minimum is analytic; the lattice transverse scan is a numerical check rather than an exhaustive proof.

A simple zero eigenvalue of the stiffness gives an inverse-square-root singularity in $K^{-1/2}$. Its fixed-transverse-momentum Fourier transform gives the large-distance form $r^{-1/2}e^{-\kappa r}$ in the position covariance. The conjugate momentum covariance has a weaker square-root branch. The longitudinal position covariance at $k_\perp=0$, multiplied by $\sqrt r e^{\kappa_{\rm lat}r}$, varies from $0.02648$ at $r=3$ to $0.02766$ at $r=12$, consistent with the branch prediction.

For full-rank reduced Gaussian states at fixed transverse momentum in the regulated theory, mutual information is even in the off-diagonal covariance and starts at quadratic order for weak correlation, provided the quadratic response is nonzero. At a nondegenerate transverse minimum, the two-dimensional transverse integral adds a factor $d^{-1}$ to the $d^{-1}$ from squaring the normal covariance. These steps predict an eventual form $I/A\sim C d^{-2}e^{-2\kappa d}$ when the light branch dominates and the quadratic expansion is uniform in the relevant momenta. The continuum exponential rate is $1.94044810$, and the stencil prediction is $1.93892840$. The prediction is for separated slabs of fixed width.

For the infinite ambient lattice at $a=0.15$ and slab width $0.6$, increasing the quadrature from $(176,40,40)$ to $(240,56,56)$ changes the computed mutual informations by at most $0.108\%$:

| Gap $d$ | Shell-only information per area | Joint information per area |
|---:|---:|---:|
| 2.4 | $7.06375\times10^{-5}$ | $8.00610\times10^{-5}$ |
| 3.6 | $3.00920\times10^{-6}$ | $3.34069\times10^{-6}$ |
| 4.8 | $1.59988\times10^{-7}$ | $1.76009\times10^{-7}$ |
| 6.0 | $9.61293\times10^{-9}$ | $1.05358\times10^{-8}$ |

Over the final interval $d=5.4$ to $6.0$, the raw rates are $2.324$ and $2.326$ for shell-only and joint information, respectively. After removing the predicted $d^{-2}$ factor they are $1.972$ and $1.975$, compared with the lattice prediction $1.939$. The corrected shell rates span $1.950$ to $1.972$ over the tested intervals. This is approximate agreement with the predicted scale and power correction, not a measurement of the exact asymptotic exponent. In particular, the competing unmixed rate $1.998$ is close, and the measured corrected rates lie between the two predictions. The branch in the projected covariance can be distinguished more directly than its ultimate dominance in the information of all five components.

### Direct Gaussian information response and separated decay rates

🟢 [Done] Evaluated the quadratic information directly, separated the independent tensor sectors, and tested distances up to $36$ at two lattice spacings. Run [gaussian_information_response.py](experiments/gaussian_information_response.py) with Python and NumPy.

At fixed transverse momentum use position and momentum covariance blocks $X(t)=X_0+tX_1$ and $P(t)=P_0+tP_1$. Here $X_0,P_0$ are block diagonal in the two slabs and $X_1,P_1$ contain their actual cross-covariances. With $F(z)$ the oscillator entropy at symplectic eigenvalue $\sqrt z$, the joint entropy is $\operatorname{Tr}F(XP)$. Set $M_0=X_0P_0$, $M_1=X_0P_1+X_1P_0$, and $M_2=X_1P_1$. In the eigenbasis of $M_0$ with eigenvalues $z_i$, the coefficient of $t^2$ in the mutual information is

$$
I_2=-\sum_i F'(z_i)(M_2)_{ii}
-\frac12\sum_{ij} F'^{[1]}(z_i,z_j)(M_1)_{ij}(M_1)_{ji}.
$$

The divided difference $F'^{[1]}$ is evaluated by $F''$ for coincident eigenvalues. This formula includes both the change quadratic in $X_1,P_1$ and the entropy Hessian. The diagonalization of $M_0$ uses its similarity transform to a Hermitian matrix. At zero transverse momentum and gap $6$, the direct coefficient agrees with the full Gaussian entropy subtraction within the script's $0.2\%$ tolerance for each sector and spacing. It remains usable at larger gaps where the full entropy difference falls below double-precision resolution. The reported large-gap values are quadratic responses.

Normal covariance integrals are evaluated on a horizontal complex contour inside the light branch point to avoid cancellation of oscillatory integrals at large distances. Changing the contour from imaginary normal momentum $0.8$ to $0.7$ agrees within the numerical tolerance in the zero-transverse comparison. Some integrated marginal modes at $a=0.10$ are numerically saturated at symplectic eigenvalue $1/2$. The integrated calculation adds a small positive momentum-covariance correction only to those near-pure modes to floor the squared margin. The reported sensitivity jointly varies the floor from $10^{-12}$ to $10^{-10}$ and the quadrature from $(1024,48,48)$ to $(896,40,40)$. The maximum relative difference in total response is $2.74\%$ at $a=0.15$ and $4.03\%$ at $a=0.10$ over the sampled gaps. This is a sensitivity comparison rather than a rigorous error estimate.

At zero transverse momentum the longitudinal tensor and clock form an exact two-field block, and four tensor components are independent free spectators. This splitting is exact for the spatial regions because the tensor basis change is independent of normal momentum. The rates after removing the fixed-transverse $d^{-1}$ factor, for the final interval $34.8$ to $36$, are:

| Spacing | Mixed shell measured | Mixed predicted | One spectator measured | Spectator predicted |
|---:|---:|---:|---:|---:|
| 0.15 | 1.93826 | 1.93893 | 1.99752 | 1.99813 |
| 0.10 | 1.93911 | 1.93977 | 1.99856 | 1.99917 |

The mixed shell contribution at this momentum exceeds the combined four spectators between gaps $27.6$ and $28.8$ at both spacings. At $d=36$ the ratios are $1.63$ and $1.61$, respectively. The mixed joint rates are $1.93832$ and $1.93916$ at the same final interval.

For generic transverse momentum the Hessian tensor direction depends on normal momentum, so the zero-transverse four-spectator split cannot be applied directly inside the integral. Two spectator directions do remain exactly independent: choose the transverse vector orthogonal to the transverse derivative symbol and symmetrize its tensor product with the slab normal and with the transverse derivative direction. Both are trace free and orthogonal to the mixing tensor for all normal momenta. The remaining three shell directions form the active block with the clock, which need not be purely the light branch. Subtracting the two independent scalar information responses from the total gives this block's contribution. It accounts for about $82.6\%$ and $82.2\%$ of the shell-only information at $d=36$ at the two spacings.

After removing the transverse-integrated $d^{-2}$ factor, the final interval $30$ to $36$ gives:

| Spacing | Total shell | Active shell block | Two independent spectators | Total joint |
|---:|---:|---:|---:|---:|
| 0.15 | 1.9620 | 1.9532 | 1.9986 | 1.9591 |
| 0.10 | 1.9608 | 1.9519 | 1.9965 | 1.9575 |

The integrated shell information at $d=36$ is approximately $5.78\times10^{-36}$ and $5.58\times10^{-36}$ nats per unit area. The active rates are closer to the predicted light rates than the full integrated rates, while the exactly separated fixed-momentum rates approach their respective predictions to within $0.001$. The finite-distance and regulator uncertainties are still too large to claim an integrated continuum exponent at this precision.

### Highest-priority follow-up

🟠 [Next] Evaluate the branch amplitudes as functions of transverse momentum and compare a two-scale asymptotic expansion with the integrated active-block response. Refine the pure-mode treatment and vary the normal grid, transverse grid, and covariance floor independently. Use the asymptotic amplitudes to test the continuum extrapolation without interpreting disjoint-slab information as a local gravitational entropy coefficient.

## 3. Joint gravitational response in a single model

### Entropy-response filter

This filter tests whether a candidate's microscopic entropy can be matched to its independently reconstructed geometry at the accuracy needed to start the joint gravitational response tests. The default target is the Einstein area term. A higher-derivative candidate may use a different geometric entropy functional and fixed quantity if both are specified independently before the comparison.

1. **Fix the observables and region.** Specify the microscopic vacuum, the regional algebra and which clock and shell variables it contains, the conditioning and replica prescription, and any bulk subtraction or local counterterms. Define the region as a geodesic ball in the independently reconstructed spatial metric on a specified physical clock slice. In a spacetime model use the slice through the ball center associated with the chosen observer direction. Track the same physical center and keep the ball's physical volume fixed during each variation. A flat plane can calibrate the area coefficient and a slab can diagnose correlations, but the gate is evaluated on these balls.
2. **Fix the normalization and perturbations.** Obtain $\eta_0>0$ from the vacuum area coefficient or a matched action calculation in the same regulator, without fitting it to perturbed-ball data or to the static force law. Define allowed perturbations independently through the candidate's generator and constraints. Test a nonzero scalar curvature or density response, a tensor response when the candidate has that sector, and available control perturbations that test spurious uniform or angular entropy responses. Include multiple ball centers, radii, and perturbation profiles or wavelengths. When a Lorentzian metric and observer family are available, include several observer directions and test uniformity on a declared domain. State explicitly which perturbations and directions the candidate can realize.
3. **Measure the residual at fixed volume.** For the Einstein target, evaluate $R_{\rm UV}=\delta S_{\rm UV}|_V-\eta_0\,\delta A_h|_V$ under the Section 1 limit protocol. For a predeclared extension replace the area term and volume by the independently derived geometric entropy and fixed quantity. Report the signed residual, the coefficients of the $r^2$ and $r^4$ terms or bounds on them, and the numerical or analytic uncertainty. Require at least one independently computed nonzero geometric response at order $r^4$ so that a vanishing residual on symmetry-null tests cannot suffice.

**Pass.** For the declared model and perturbation class, show $R_{\rm UV}=o(\eta_0 r^4/R_*^2)$ in the stated limit, with a bound or convergence analysis that resolves the $r^4$ coefficient and includes a nonzero geometric test. The same normalization and regional prescription must work across the test family. Numerical work must report the probed class and resolutions. An extension beyond that class requires its own test.

**Fail.** A controlled nonzero $r^2$ or $r^4$ residual on an allowed perturbation rejects the candidate under the tested entropy functional and fixed-quantity prescription. A proposed change to that prescription requires independent justification and a new test across the same perturbation family.

**Inconclusive.** Leave the gate open if the uncertainty can hide an $r^4$ residual, the result depends on an unresolved order of limits or regulator choice, the regional algebra or subtraction is ambiguous, or only symmetry-null or planar tests are available. Missing tensor or observer tests also keep the full gate open if those sectors are part of the candidate's intended scope.

🟠 [Next] Extend the initial assessment to a candidate with independently specified dynamics and a controlled nonuniform entropy calculation. A pass advances the stated model and perturbation class to the joint response tests below. It does not establish the CFT modular balance, static coupling match, or massless TT dynamics; those checks remain part of Section 3.

### Initial filter assessment

| Candidate or comparison | Result under the stated prescription |
|---|---|
| Isotropic bond family with the Section 1 positive-hopping generator | **Fail**. The independently defined energy window contains the nonuniform tangent, and its fixed-volume response leaves a controlled nonzero $r^4$ residual. Other generators require their own admissibility test. |
| Static shell comparison with an independent nonzero shell entropy and the Einstein area target | **Fail** for the admitted conserved source in the comparison. The integrated shell term survives at order $r^4$ for generic nonzero coupling and Fourier amplitude. This classifies the stated entropy functional, not a completed microscopic candidate. |
| Linearly driven Gaussian shell with synchronized clock | **Inconclusive** for the full gate. The independent source-dependent shell entropy vanishes at fixed geometry. The minimal smooth effective-metric completion has mismatched leading Einstein coefficients for $v\ne1$. At $v=1$ the leading coefficients match and the isolated metric $R^2$ response is known; the projected connection has zero linear canonical response about the trivial flat frame. The full curved-ball trace and dynamical-clock tests remain open. |
| Clock-tensor slab models | **Inconclusive** for the gravitational entropy filter. Spatial mutual information removes local area terms and therefore does not test the required fixed-volume ball coefficient. |

No microscopic candidate has passed the full gate. Prioritize a model whose regional entropy and geometric vacuum response can be computed in the same regulator before extending the joint gravity comparison.

### Joint response checks

Check the candidate's vacuum, self-adjoint generator, clock convention, and preservation of the dynamical constraints.

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

Record the input geometry, symmetries, and fitted parameters. Check signs, units, and boundary conditions. For dimensionless entropy $[\eta]=L^{-2}$ and $G_{\mathrm N}=c^3/(4\hbar\eta)$ in SI units. Use the Section 1 limit protocol for curvature tests and document any justified exchange of limits. Recheck dependent conclusions after finding a contradiction. Preserve the nearest-neighbor anisotropy, the quadratic critical dispersion, and the TT and static linearized responses as reference cases.
