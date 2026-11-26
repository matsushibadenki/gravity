# Quantum Information Emergent Gravity (QIEG) Research Roadmap

Updated 26 November 2026

## Research objective and current scope

QIEG studies whether entropy and spacetime geometry emerge from the same quantum information structure. The microscopic inputs are a subsystem structure, a quantum state, and a self-adjoint Hamiltonian or constraint. The goal is to derive spatial geometry, causal dynamics, and a gravitational response with the same independently calculated coupling in one model.

At low energies, a smooth Lorentzian metric, a local conformal vacuum, an orientation-independent area coefficient, and fixed-volume entanglement equilibrium give the linearized semiclassical Einstein equation. In natural units, the matching is $G_{\mathrm N}=1/(4\eta)$. Its covariant two-derivative completion is $G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G_{\mathrm N}\langle T_{\mu\nu}\rangle$. The completion uses the additional assumption of a two-derivative metric effective theory. Microscopic equilibrium and the values of $\eta$ and $\Lambda$ remain open. [Jacobson, *Entanglement Equilibrium and the Einstein Equation*](https://arxiv.org/abs/1505.04753) · [Casini, Huerta, and Myers, spherical modular flow](https://arxiv.org/abs/1102.0440)

## Status

- 🟢 [Done] Implemented in the current workspace
- 🟠 [Next] High-priority unfinished work
- 🔴 [Later] Planned work after the nearest milestones
- ⭕️ [Pending] On hold because it cannot be tested in the development environment

## Research priority after comparison with null-cone quantization

Retain the microscopic emergence objective and the fixed-generalized-volume entropy test. Give the definition and gluing of the physical regional algebra priority over further smooth-background coefficient fits. Chandrasekaran starts from four-dimensional vacuum Einstein gravity with a specified Newton coupling. The paper's affine null clock, selected diamond states and corner trace supply a comparison for our vacuum Einstein limit. Our scalar clock carries stress and our ball moves at fixed generalized volume. Equivalence of the two region and state prescriptions would require a separate derivation. In particular, Eq. (5.50) includes a trace normalization in addition to the mean area term, and the horizon application imposes the null-expansion conditions of Eq. (5.51). [Chandrasekaran, Sections 3.6 and 5.3, v1](https://arxiv.org/html/2611.34924v1)

- 🟢 [Done] Reproduced the existing flat CFT control at four radii. The maximum absolute total entropy variation divided by the fourth power of the radius was below $5\times10^{-12}$ in the benchmark units. The physical clock calculation remains open. [Local sphere calculation](experiments/matched_pure_ball.py)
### Implementation order and decision criteria

The first implementation is a vacuum Einstein cut-and-glue calculation on a round two-sphere in a flat reference geometry. Use one weak, nonconstant boundary source as well as the source-free amplitude. The outer preparation and regulator must agree on both sides of every comparison. The steps below set the project-wide priority for the clock–gravity candidate.

1. 🟠 [Next] **Derive the boundary data and test composition at one replica.** Obtain the corner symplectic potential from the regulated Einstein action. Identify the induced two-metric, the identification of points across the cut and the relative boost of the two normal frames. With the two faces given opposite orientations, the common frame shift must have zero total charge and the relative boost must be conjugate to the area density divided by $8\pi G_{\rm N}$. Use the Newton coupling from the action for this calibration. Integrate the shared data once with the induced measure and treat the common gauge freedom and its zero modes consistently. Compute the glued and uncut amplitudes independently. Compare their ratio at zero source and their logarithmic source derivatives for a nonzero probe with the same geometric support on both descriptions. Repeat after a common frame change and under refinement. Advance when the ratio approaches one and the source and frame differences approach zero within controlled errors. A persistent discrepancy reopens the measure, matching conditions and boundary action. [Chandrasekaran, Eqs. (3.60)–(3.66) and Sec. 4](https://arxiv.org/html/2611.34924v1#S3.SS6)
2. 🟠 [Next] **Construct the trace for the physical clock region.** Restore the dynamical scalar clock and the matched curvature terms, including $R(\nabla T)^2$. Derive which boundary data are held fixed, which are integrated, and which transformations are gauge. Compare sewing before constraint reduction with the transported sewing and Jacobian in reduced variables. Recheck one-sheet composition in this coupled model. For the same prepared state and region define $F(n)=\log Z_n-n\log Z_1$ and evaluate $S=-F'(1)$ from a physical density operator or a derived replica family. Determine finite surface terms independently of the sphere response. The identity $F(1)=0$ alone has no sensitivity to a surface insertion proportional to $n-1$. An unresolved surface coefficient or choice of trace leaves the physical entropy undetermined. [Reduced-clock seam](experiments/reduced_clock_ball_seam.py) · [Canonical transfer calculation](experiments/reduced_clock_transfer.py)
3. 🔴 [Later] **Decide the fixed-generalized-volume sphere response.** Derive the generalized volume $W$ from the same action and move the clock-defined boundary with $\delta W=0$. On independently prepared, constraint-satisfying perturbations, report the signed renormalized $\delta S_{\rm total}|_W$, including the state response and counting each local term once. Resolve the $r^2$ term before extracting the $r^4$ coefficient. Use multiple profiles, at least one nonzero geometric $r^4$ signal and the established order of limits. A controlled nonzero residual rejects the tested equilibrium prescription. A vanishing residual within a bound that resolves the signal supports the tested class. Insufficient resolution or an undetermined finite term leaves the question open. Record the microscopic entropy–geometry residual separately under the [Section 3 filter](#entropy-response-filter). [Order of limits](#order-of-limits-for-a-curvature-measurement)

Keep the completed bulk coefficient and flat-sphere calculations as controls. Resume bulk coefficient fits when a specific subtraction uncertainty limits the sphere measurement. The paper's finite-dimensional diamond Hilbert space and horizon trace are results for its own state selection. Establishing analogous results here would require a map of states, observables and boundary conditions between the two constructions. [Chandrasekaran, Sec. 5](https://arxiv.org/html/2611.34924v1#S5)

### Vacuum corner charge and radial composition control

- 🟢 [Done] Calibrated the classical corner charge by rounding the joint in the normal plane. For the Einstein boundary action with coefficient $1/(8\pi G_{\rm N})$, the singular part of the rounded cap's extrinsic curvature is the rate of rotation of its normal with respect to cap arc length. Integrating that part and continuing the normal-plane rotation to an oriented Lorentzian boost $\Gamma$ gives the joint action $\int_\Sigma \sqrt q\,\Gamma/(8\pi G_{\rm N})$. The angle–area symplectic pair is represented by $\sqrt q\,\delta\Gamma/(8\pi G_{\rm N})$, up to an exact variation for the alternative choice of corner polarization. For a matched two-metric, the oriented sum is $\sqrt q\,\delta(\Gamma_R-\Gamma_L)/(8\pi G_{\rm N})$. A common boost is therefore null in this corner sector. For smooth $X=(\nabla T)^2$ with a common limiting value at the cap, the $RX$ term with coefficient $\lambda$ adds $2\lambda\sqrt q$ times $X$ to the boost charge density via the $2\lambda X K$ boundary term in the metric variation at fixed $X$. This only calibrates the local angle term. The scalar variation and coupled sewing measure still require a derivation. [Null-cone comparison, Eqs. (3.63)–(3.66)](https://arxiv.org/html/2611.34924v1#S3.SS6)
- 🟢 [Done] Tested one-sheet amplitude composition of a canonically normalized static linearized Einstein master field in the $\ell=2$ sector. The source $j\,u(1)$ couples to the gauge-invariant master variable with quadrupolar angular dependence. Cut at radius one and fix regularity at zero and Dirichlet data at radius two. Independently assemble the full radial action and the two open interval actions. Integrate the latter using the Gaussian measure $du/\sqrt{2\pi}$ per node and one integral over the common seam variable. For $j=0,0.2$ the maximum absolute log amplitude mismatch was $5.69\times10^{-14}$ and the maximum absolute source-response mismatch was $2.09\times10^{-16}$. Doubling the cells per side from 16 to 128 reduced the error against the continuum seam Green function $31/160$ from $5.51\times10^{-4}$ to $8.65\times10^{-6}$, consistent with second-order convergence. [Reproduction script](experiments/einstein_radial_gluing.py) · [Kodama and Ishibashi, vacuum master equations](https://academic.oup.com/ptp/article/110/4/701/1875052)
- 🟠 [Next] Derive the induced seam measure in metric variables, including the relation between the master source and geometric boundary data, frame matching, the constraint determinant and residual gauge modes. The radial control assumes the canonical reduced measure. Its determinant equality follows from Gaussian composition and provides a reference for testing that independent metric calculation. The full vacuum gate remains open.

### Linearized ADM measure before spherical cutting

- 🟢 [Done] Calibrated the bulk constraint measure in the original canonical metric and momentum components. For a nonzero spatial Fourier mode the linearized lapse and shift impose $C_0=k^2\operatorname{tr}h-k_i k_j h_{ij}$ and $C_i=2k_j\pi^{ij}$, with Fourier phases absorbed into the shift multipliers. Integrating the multipliers with the Fourier delta normalization gives $\delta(C)$. A linear gauge $\chi$ supplies $\delta(\chi)|\det\{\chi,C\}|$. In canonical coordinates $x=(h,\pi)$ the change of variables to $(C,\chi,Px)$, where $P$ projects onto an orthonormal TT phase-space basis, has determinant magnitude $|\det\{\chi,C\}|$ for the checked gauges. The two factors cancel, leaving the canonical measure of two graviton pairs. Numerically the maximum absolute log measure error is $3.56\times10^{-15}$ across three wave vectors and two gauges, including a slice tilted by physical data. A TT source gives the same response on both gauge slices. The zero Fourier mode has rank zero and requires its own boundary or global treatment. [ADM measure check](experiments/einstein_adm_measure.py)

- 🟠 [Next] Extend this calculation to the spherical boundary. Integrations by parts in the lapse and shift constraints change the generator when smearing functions have nonzero boundary values. Derive those surface terms, evaluate the constraint and gauge Jacobians with the same allowed boundary data on each side, and compare the induced seam measure with the radial master-field control. The Fourier calculation fixes the bulk normalization. The boundary charge measure and the source map to the induced two-metric remain open.

### Surface terms of the linearized ADM generators

🟢 [Done] Derived the surface terms before eliminating lapse and shift. On a flat spatial slice, set $C_h=\partial_i\partial_j h_{ij}-\Delta h_{ii}$ and $C^i_\pi=2\partial_j\pi^{ij}$ in the flux sign convention. With outward normal $n$ and $\partial_n=n^i\partial_i$ the Green identities are
$$
\begin{aligned}
\int_D \big[N C_h-h_{ij}(\partial_i\partial_j N-\delta_{ij}\Delta N)\big]\,d^3x
&=\int_{\partial D}\big[Nn_i(\partial_jh_{ij}-\partial_i h_{jj})
-n_i h_{ij}\partial_j N+h_{jj}\partial_n N\big]\,dA,\\
\int_D (W_i C^i_\pi+2\pi^{ij}\partial_j W_i)\,d^3x
&=\int_{\partial D}2W_i n_j\pi^{ij}\,dA.
\end{aligned}
$$

For $N=0$ on the sphere the first flux reduces to $(\partial_n N)\operatorname{tr}_{\Sigma}h$. Multiplying the flux by the Einstein normalization $1/(16\pi G_{\rm N})$ gives $\int_\Sigma (\partial_n N)\delta(dA)/(8\pi G_{\rm N})$, since $\delta(dA)=\tfrac12\operatorname{tr}_{\Sigma}h\,dA$. Thus even lapse smearings vanishing on the seam can carry a boost charge. Pure gauge generators supported away from the seam have zero boundary flux. For a common smooth smearing across an artificial seam, the opposite oriented fluxes cancel when their geometric data agree. The shift tests the normal momentum flux, while a nonzero lapse value also probes first derivatives of the metric.

🟢 [Done] Tested both Green identities on the inner ball, outer shell, and their union using an axisymmetric quadrupole. The one-sided dimensionless lapse and shift fluxes at unit radius are $10.0530964915$ and $5.0265482457$. Both internal sums vanish and the lapse flux agrees with the independent area variation. The polynomial probe is an off-shell test of the identities. [Boundary calculation](experiments/einstein_adm_boundary.py)

🟠 [Next] Construct the spherical constraint and gauge matrices with these surface terms. Retain the nonvanishing boundary charges when defining the proper gauge subgroup and determine the residual mode and seam Jacobians. Compare the induced metric source with the radial master-field source. The boundary identities supply tests for this construction. The induced quantum seam measure remains open.

### Spherical lapse constraint and boundary trace matrix

🟢 [Done] Assembled the quadrupolar lapse matrix on the unit ball with conformal metric probes $h_{ij}=f\delta_{ij}$. Expand both $f$ and $N$ in $r^2P_2(\cos\theta)$ times Legendre polynomials in $2r^2-1$. The bulk matrix represents $\int N(-2\Delta f)\,d^3x$. Its antisymmetric part is exactly the Green flux $2\int_\Sigma(f\partial_n N-N\partial_n f)\,dA$. The code computes the volume and boundary matrices independently.

Let $T$ return the two radial boundary traces $(N(1),N'(1))$. For basis sizes 4, 6, 8, and 10, the boundary matrix has rank two and vanishes on $\ker T$. The restricted bulk constraint matrix has full row rank on $\ker T$, with dimensions 2, 4, 6, and 8 respectively. For this canonical lapse block, its singular vectors give gauge coordinates for the proper momentum shifts. The Faddeev–Popov determinant cancels the corresponding delta-function Jacobian to within $1.1\times10^{-14}$ in log measure. The two lapse traces remain available to probe the seam. This rank counts boundary data in the restricted ansatz. A count of physical gravitational edge modes requires the full gauge and constraint system. [Reproduction script](experiments/einstein_spherical_lapse.py)

🟠 [Next] Include the independent even-parity metric and momentum components and radial and angular shift constraints in the spherical matrix. Use the same angular and radial spaces on each face for the oriented charge match, then determine the induced interface measure and compare the geometric quadrupole source with the master-field source.

### Even-parity quadrupole boundary charge map

🟢 [Done] Extended the spherical calculation to independent even-parity boundary traces of the metric and momentum. On the unit sphere write $h_{rr}=aY$, $h_{rA}=bD_A Y$, and the tangential trace as $2cY$, in a frame with unit tangential normalization at each radius. Include the tangential trace-free component independently. Write the corresponding momentum amplitudes as $p$ and $s$ for the radial and mixed components. In a common radial orientation the four flux coefficients paired with the lapse value, lapse slope, radial shift, and gradient shift are
$$
\frac{4\pi}{5}(2a-12b-2c-2c',\ 2c,\ 2p,\ 12s).
$$
Here $Y=P_2(\cos\theta)$ and $c'$ is the radial derivative. The mixed metric term receives equal contributions from the tangential divergence and from the angular derivative of the lapse in the Green identity. All coefficients use the flux normalization of the preceding ADM calculation.

🟢 [Done] The boundary matrix computed by angular quadrature has rank four, with a five-dimensional kernel on the nine input trace amplitudes. The calculation verifies cancellation for opposite orientations when the four paired charges agree, including a test with different one-sided traces in the kernel of the charge map. Independent jumps in the four charges are detected by the four smearings. The common tangential trace-free metric remains part of induced metric matching even though this charge map is insensitive to it. Charge matching therefore supplies four linear tests alongside continuity of geometric data. [Boundary charge matrix](experiments/einstein_even_boundary.py)

🟠 [Next] Construct the radial bulk matrices for these even-parity components and test the first-class algebra for the zero-trace lapse and shift smearings. Use the charge map as a boundary test and derive the remaining seam Jacobian from the constrained canonical measure. The boundary matrix alone does not determine that Jacobian or the map from the induced metric source to the master variable.

### Even-parity radial constraint algebra

🟢 [Done] Constructed exact polynomial Galerkin matrices on the unit ball for the proper lapse and both even-parity shift components. The tensor basis consists of radial polynomials multiplying $YI$, $Q$, $x(Qx)^T+(Qx)x^T$, and $Yxx^T$, where $Y=x^TQx=r^2P_2$ and $Q=\operatorname{diag}(-1/2,-1/2,1)$. Lapses contain $(1-r^2)^2$ and shifts contain $(1-r^2)$, which kill their boundary fluxes. The rows are the integrated pairings with $\partial_i\partial_j N-\delta_{ij}\Delta N$ and $-(\partial_i W_j+\partial_j W_i)$, respectively. The inverse tensor Gram matrix enters the canonical contraction. The shift gradients are reconstructed exactly in the tensor basis before computing the mixed bracket. Consequently a projection of the gauge variations cannot be responsible for the zero bracket. Same-kind brackets vanish because their rows depend only on the metric or only on its canonical momentum. The test uses exact unit-ball polynomial moments. [Reproduction script](experiments/einstein_even_bulk.py)

🟠 [Next] Retain the charged smearings and construct a common inner-ball and outer-shell discretization. Determine the interface measure with the proper orbits removed on each side and independently compose the sourced amplitude. The proper-constraint algebra supplies a bulk consistency check. The residual boundary measure and geometric source map remain open.

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

🟠 [Next] The next section tests a constrained perturbation with nonzero intrinsic curvature and a moving relational cut. Higher-derivative matching follows after the moving-cut vacuum response is controlled. The present result is an aligned momentum test in the coupled Einstein-scalar model, not the full entropy gate for the clock-tensor candidate.

### Intrinsic curvature and a moving clock-defined boundary

🟢 [Done] Solved a second physical perturbation of the coupled Einstein-scalar model, tracked its fixed-volume geodesic ball, and separated the reduced-state modular response from reference entropy due to the moving cut. Run [moving_clock_ball.py](experiments/moving_clock_ball.py).

Keep the expanding scalar-clock reference and the initial-state and regional prescriptions of the preceding section. Normalize $a_{\rm FLRW}=1$ at the selected clock reading. In the reduced physical phase space, displace the configuration with $\delta\zeta=f(\varrho)=\sin(k\varrho)/(k\varrho)-1$ and keep $\delta\dot\zeta=0$ on this slice, where $\varrho$ is the coordinate distance from the marked center. A smooth envelope can be chosen equal to one over the test balls, or the test can be made with the indicated local profile and a distant infrared boundary. The constant term sets the perturbation to zero at the center and can be included in a local test profile with an envelope. It need not be treated as an independent homogeneous oscillator.

The solved nonhomogeneous constraints give $\delta\alpha=0$ and $\delta\psi=-f/H$, with the infrared convention for the homogeneous part. Consequently

$$
\delta\rho_\varphi=0,\qquad
\delta K=\Delta f/H,\qquad
\delta R^{(3)}=-4\Delta f.
$$

In particular $\delta R^{(3)}(0)=4k^2$ while $\delta R^{(3)}+4H\delta K=0$. The two constraints admit these configuration initial data. The reference is still an expanding clock background, so a nonzero intrinsic curvature variation is compatible with zero instantaneous energy-density variation.

The spatial metric on the slice is conformal to the original coordinates. Spherical symmetry makes the physical geodesic ball a coordinate sphere with a varying coordinate radius $R(\epsilon)$. At fixed $W=V$ and reference physical radius $r$, let $A_0=4\pi r^2$ and denote the surface and volume averages on the reference sphere by $f_\Sigma$ and $f_B$. Varying the volume and area gives

$$
\delta R=-r f_B,\qquad
\delta A|_V=2A_0(f_\Sigma-f_B)
=-\frac{8\pi}{15}k^2r^4+O(r^6).
$$

The geometry is also checked by solving the fixed-volume condition for the finite conformal metric $e^{2\epsilon f}\delta_{ij}$ at positive and negative amplitudes and differentiating at zero. At the finest tested radius the area coefficient approaches its $r^4$ limit. The weighted expansion contribution satisfies
$\delta(A/4G)|_V=2\pi\int w\,2M_{\rm Pl}^2H\delta K\,dV_0$ for this profile, using the same weight as before. This sign and normalization follow from the solved constraint with zero clock-density change and are checked by independent radial quadrature.

The configuration displacement is generated by the reduced momentum. On any one fixed coordinate region it factorizes across that region and preserves its reference entanglement spectrum. Thus the first-order modular energy and the state entropy relative to the undisplaced Gaussian on the **same** coordinate region vanish. This statement also applies to comparing the two states on the moved coordinate region at each $\epsilon$. The total first variation of the reduced entropy is a separate shape response:

$$
S_{\rm red}(\rho_\epsilon,B_\epsilon)-S_{\rm red}(\rho_0,B_0)
=S_{\rm red}(\rho_0,B_\epsilon)-S_{\rm red}(\rho_0,B_0).
$$

Here $B_\epsilon$ denotes the coordinate representation of the tracked physical ball. At a finite site regulator this identity holds for each selected set of sites; a continuous shape variation requires a continuum or smoothed-cut prescription. Keeping only the Einstein area and same-cut state entropy gives a nonzero $r^4$ response. This is a diagnostic of that comparison, not the total renormalized generalized entropy of the moving ball.

The instantaneous reference Gaussian for the massless reduced scalar is equivalent on the flat reference slice to the free scalar vacuum after constant canonical rescaling. For example, at fixed coordinate cutoff its round-sphere logarithmic term is $-(1/90)\log(R/\epsilon_{\rm coord})$. This piece changes under the coordinate displacement by $-\delta R/(90r)$, even though the same-cut state entropy is unchanged. A cutoff fixed in proper distance, or a matched gravitational entropy counterterm, must be handled with the spatial metric variation as well. The coordinate-cut example cannot fix the renormalized shape contribution in the physical comparison. [Casini and Huerta, scalar sphere logarithm and concentric-sphere mutual information](https://arxiv.org/abs/1512.06182)

🟠 [Next] The following section evaluates the vacuum shape response with a fixed proper-distance collar. The full microscopic matching and higher-derivative generalized volume still require an independent calculation.

### Proper-distance collar and the moving vacuum contribution

🟢 [Done] Computed the collar contribution from the area and logarithmic terms of the reduced scalar reference vacuum. Matched the power divergence to a local Einstein area subtraction with the same collar scale. In this specified comparison the fixed-volume $r^4$ term does not cancel. Run [proper_distance_collar.py](experiments/proper_distance_collar.py).

Keep the clock-aligned Einstein-scalar configuration perturbation $f(\varrho)=\sin(k\varrho)/(k\varrho)-1$. The spatial metric at the selected clock reading is $e^{2\epsilon f}\delta_{ij}$ and the central geodesic sphere has coordinate radius $R(\epsilon)$ fixed by its physical volume. Define the inner and outer cuts $R_\pm$ at signed radial proper distances $\pm d/2$ from this sphere, with $d$ fixed. Take the spatial continuum at nonzero $d$ and then $d/r\to0$ at fixed $r$ before extracting the small-ball coefficient. The first variations are

$$
\delta R_\pm=\delta R-\int_r^{r\pm d/2}f(\varrho)\,d\varrho,
\qquad \delta R=-r f_B .
$$

Use half the mutual information of the interior of $R_-$ and the exterior of $R_+$ as the regulated entropy. The state is a displacement of the instantaneous flat reference Gaussian, and the displacement factorizes for both regions and their union. Only the change of the cuts enters this mutual information. The reference scalar vacuum uses $\xi=(R_++R_-)/[2(R_+-R_-)]$. Its area and logarithmic contributions are $s_2\xi^2+s_{\log}\log\xi$ with $s_2=4\pi(0.0055351600)$ and $s_{\log}=-1/90$. This calculation uses the established short-collar coefficients. Any additional remainder with vanishing logarithmic derivative as $\xi\to\infty$ has zero limiting first variation here. The script checks the geometry and the variation of these terms without recomputing the full mutual information spectrum. [Casini and Huerta, concentric-sphere scalar coefficients, Section 4.2](https://arxiv.org/abs/1512.06182)

The logarithmic scale varies as

$$
\delta\log\xi
=f(r)-f_B+d^2\left[\frac{f''(r)}{24}-\frac{f'(r)}{8r}\right]+O(d^4)
$$

at fixed $r$. The leading area divergence in the entropy variation is $(s_2/4\pi d^2)\delta A|_V$. The $O(d^2)$ shape correction also matters because it multiplies $d^{-2}$. Subtracting the divergent local area term leaves

$$
\delta S_{\rm vac}^{\rm sub}
=s_{\log}\,[f(r)-f_B]
+\frac{s_2r^2}{12}\left(f''(r)-\frac{3f'(r)}r\right).
$$

The second term belongs to the specified symmetric proper-distance collar.

The local Einstein action coefficient $A_E(d)$ gives conical entropy density $4\pi A_E(d)$. Hold the renormalized coefficient $A_{E,R}=M_{\rm Pl,R}^2/2$ fixed and use the same $d$ to impose $4\pi A_E(d)=4\pi A_{E,R}-s_2/(4\pi d^2)$. This local renormalization condition cancels the collar power divergence. It does not supply an independent calculation of the smooth gravitational determinant regulated by the collar. In particular, additive local surface functionals cancel in the separated-region mutual information, so independent finite gravitational counterterms cannot be extracted from it alone.

For this profile, $f(r)-f_B=-k^2r^2/15+k^4r^4/210+O(r^6)$. The $r^4$ coefficient of the finite $s_2$ term is zero because the derivative combination annihilates the $r^4$ monomial in $f$. Including the renormalized Einstein area and the unchanged same-cut state entropy gives

$$
\delta S_{\rm comparison}|_V
=k^2\left(\frac{s_2}{18}+\frac1{1350}\right)r^2
-\left(\frac{16\pi^2M_{\rm Pl,R}^2}{15}k^2+\frac{k^4}{18900}\right)r^4
+O(r^6).
$$

The two displayed $r^4$ contributions have the same sign for positive $M_{\rm Pl,R}^2$ and nonzero $k$. The numerical check uses four collar widths and four ball radii. The result is for the calculated reduced vacuum terms and the Einstein area matching, with no additional finite geometric terms specified. The full coupled gravitational response remains open until the smooth determinant and finite boundary terms are derived in a physically matched regulator.

🟠 [Next] The following section evaluates the usual local metric curvature-squared entropy on the moving-ball data. The common microscopic regulator and finite clock-dependent terms still require independent derivation.

### Local curvature-squared matching on the moving clock data

🟢 [Done] Tested the ordinary covariant curvature-squared entropy terms on the solved Einstein-scalar initial data. Used two nonuniform profiles to separate them from the collar logarithm. Run [clock_curvature_counterterms.py](experiments/clock_curvature_counterterms.py).

Keep the two-derivative expanding scalar-clock solution and the configuration displacement at the selected clock reading, with $a_{\rm FLRW}=1$, $\delta\zeta=f$, $\delta\dot\zeta=0$, $\delta\alpha=0$, and $\delta\psi=-f/H$. The constraint gives $\delta R^{(3)}=-4\Delta f$ and $\delta K=\Delta f/H$. These are generally nonzero. The spacetime curvature that enters a covariant local entropy term is different. The trace-reversed Einstein-scalar equation gives $R_{\mu\nu}=M_{\rm Pl}^{-2}\partial_\mu\varphi\,\partial_\nu\varphi$. In the uniform-clock frame this gives $R_{ij}^{(4)}=0$ and $R^{(4)}=-\dot{\bar\varphi}^{\,2}/(M_{\rm Pl}^2N^2)$. Because the lapse is unperturbed on this slice, $\delta R^{(4)}=0$ there.

To compute the electric Weyl tensor, use the spatially projected Gauss equation in the clock frame:

$$
E_{ij}=\left[R^{(3)}_{ij}+K K_{ij}-K_i{}^k K_{kj}-\tfrac12 R^{(4)}_{ij}\right]^{\rm TF}.
$$

Here the trace-free part of the intrinsic Ricci perturbation is $-(\partial_i\partial_j f)^{\rm TF}$. The linear extrinsic-curvature combination gives $H\delta K^{\rm TF}_{ij}=(\partial_i\partial_j f)^{\rm TF}$ from the solved shift. Thus $\delta E_{ij}=0$ throughout the slice. The linear magnetic Weyl tensor vanishes as well because the shear is a spatial Hessian and its symmetrized curl is zero. This cancellation does not require spherical symmetry. The test uses a nondiagonal Hessian as well as an isotropic Hessian. [Arnowitt, Deser, and Misner, constraints and spatial geometry](https://arxiv.org/abs/gr-qc/0405109)

Consider a local entropy functional from metric terms $A_E R+B_R R^2+B_C C^2+B_E E_4$, at fixed physical volume, using the same collar definition as in the previous section. In the usual metric replica prescription on a spherical cut, the $R^2$ entropy changes by $8\pi B_R\bar R^{(4)}\,\delta A$ because $\delta R^{(4)}=0$ on the slice. This has the same area dependence as the Einstein term; it can be included once in a reference entropy-area density $\eta_{\rm ref}=4\pi A_E+8\pi B_R\bar R^{(4)}$. The Weyl entropy has zero first variation: both the spacetime Weyl perturbation and the background trace-free extrinsic curvatures vanish for this sphere. The Euler entropy depends only on the sphere topology and has zero first variation. Thus this metric curvature-squared sector provides no separate shape term at fixed physical volume when evaluated on the specified initial data. It does not fix $\eta_{\rm ref}$ from an independent static measurement. [Fursaev, Patrushev, and Solodukhin, curvature-squared replica terms](https://arxiv.org/abs/1306.4000)

For a radial profile $f=c_2 r^2+c_4r^4+O(r^6)$ at the center, the half-mutual-information collar comparison gives the following $r^4$ coefficient after the leading $r^2$ term is accounted for:

$$
\left[\delta S_{\rm comparison}|_V\right]_{r^4}
=\frac{16\pi}{5}\eta_{\rm ref}c_2+\frac47s_{\log}c_4.
$$

The finite power-collar term annihilates the $r^4$ monomial. In addition to the original profile, take
$f=(\mathrm{sinc}(kr)-1)-(\mathrm{sinc}(2kr)-1)/16$, with $\mathrm{sinc}(x)=\sin(x)/x$. It has $c_2=-k^2/8$ and $c_4=0$. This removes the logarithmic $r^4$ contribution without removing the geometric area response. For positive independently matched $\eta_{\rm ref}$ the nonzero coefficient is then $-2\pi\eta_{\rm ref}k^2/5$. The script checks the two profiles over four radii.

The calculation evaluates the curvature-squared entropy terms on the leading Einstein-scalar initial data. If the higher-derivative operators are included in the field equations, their corrections to the constrained geometry and to a possibly different fixed geometric quantity must also be computed at the same order. This result therefore classifies the local metric entropy terms on these data. It does not exclude clock-dependent operators, higher derivatives of curvature, edge contributions, or a different vacuum selected in a completed microscopic theory.

🟠 [Next] The following section tests a specified induced action that couples to both intrinsic curvature and clock expansion. More general clock operators and higher-derivative corrected constraints remain open.

### Induced clock-foliation terms on the moving ball

🟢 [Done] Added a specified induced action that couples directly to intrinsic spatial curvature and clock expansion. Re-solved the scalar constraints with those coefficients and tested the fixed-volume $r^4$ response using the area entropy of the same heavy-field proper-time band. Run [clock_induced_ball.py](experiments/clock_induced_ball.py).

Use the clock-defined effective metric of the Gaussian tensor determinant, with $\widetilde h_{ij}=v^{-2}h_{ij}$, unchanged lapse and shift, and $v>0$ constant. Fix a finite proper-time band $[s_1,s_2]$ in the effective metric, with $\sqrt{s_2}\ll r$ and both metric and clock smooth at that scale away from the cut. Let $C=5(192\pi^2)^{-1}\int_{s_1}^{s_2}e^{-M^2s}\,ds/s$. Retain the two-derivative part and match away the zeroth-derivative term. Combine the induced $\widetilde R$ term with the bare physical Einstein term and a minimally coupled massless scalar clock. The gravity action in clock-adapted coordinates is

$$
\Gamma_{\rm grav}^{(2)}
=\int N\sqrt h\left[A_R R^{(3)}
  +A_K(K_{ij}K^{ij}-K^2)\right]\,dt\,d^3x,\qquad
A_R=A_0+C/v,\quad A_K=A_0+C/v^3.
$$

Both coefficients are positive for $A_0,C>0$. The two induced pieces are linked by the specified determinant; their coefficients are not fit to a ball. The calculation uses the usual smooth ADM decomposition, including the same convention for its discarded bulk total divergence as in the earlier matching. [Vassilevich, Laplace-type heat coefficients](https://arxiv.org/abs/hep-th/0306138) · [Arnowitt, Deser, and Misner, canonical decomposition](https://arxiv.org/abs/gr-qc/0405109)

The lapse constraint is $A_RR^{(3)}+A_K(K^2-K_{ij}K^{ij})=\rho_\varphi$. The homogeneous reference obeys $\bar\rho_\varphi=6A_K H^2$. In uniform-clock scalar gauge, the nonhomogeneous momentum constraint still gives $\alpha=\dot\zeta/H$, since $A_K$ is constant and the scalar momentum density normal to the slice vanishes. For $\delta\zeta=f$, $\delta\dot\zeta=0$, at a reference reading with $a_{\rm FLRW}=1$, the solution is

$$
\alpha=0,\qquad \psi=-\frac{A_R}{A_K}\frac{f}{H},\qquad
\delta K=\frac{A_R}{A_K}\frac{\Delta f}{H},\qquad
\delta R^{(3)}=-4\Delta f,\qquad \delta\rho_\varphi=0 .
$$

This changes the shift and expansion of the earlier data when $v\ne1$, while the intrinsic conformal geometry at the chosen reading is still set by $f$. To obtain the reduced quadratic scalar action, rescale the lapse by $\widehat N=c_gN$ with $c_g^2=A_R/A_K$. The smooth gravity action is then Einstein with coefficient $\widehat A=\sqrt{A_R A_K}$ in the rescaled metric. In uniform-clock gauge the massless clock kinetic term takes the standard comoving form after $\widehat\varphi=\sqrt{c_g}\varphi$. The resulting $\zeta$ action has time-kinetic coefficient $2A_Ka_{\rm FLRW}^3\varepsilon_H$ and spatial gradient coefficient $2A_Ra_{\rm FLRW}\varepsilon_H$ in the physical time convention. Here $\varepsilon_H=3$ for the homogeneous massless clock. The instantaneous vacuum on the flat slice has the same regional entropies as the massless scalar after a constant local canonical rescaling. The configuration displacement preserves the same-cut state entropy. [Maldacena, uniform-field constraint reduction](https://arxiv.org/abs/astro-ph/0210603)

For the heavy determinant's entropy use canonical fiber gluing and retain its local leading cone area term, with the same $s_1,s_2$ used in $C$. The area in its effective metric is $A_h/v^2$. Therefore its entropy is $4\pi C A_h/v^2$, and including the physical Einstein term gives the density $\eta_{\rm band}=4\pi(A_0+C/v^2)$. This derives the area contribution used here from the regulated heavy sector. Neither the coefficient of $R^{(3)}$ by itself nor the smooth lapse rescaling is an independent prescription for sewing the physical cut. The reduced scalar keeps its separate proper-distance collar and its previously specified local area subtraction. Here $A_0$ includes any matched reference contribution used for that subtraction, and the heavy band is counted only once. A common microscopic matching of the complete light and heavy entropy, including their finite boundary terms, is outside this leading-area calculation. [Solodukhin, proper-time cone entropy](https://arxiv.org/abs/1104.3712)

At fixed physical volume use the two-sinc profile of the previous section, with $c_2=-k^2/8$ and $c_4=0$ in its central expansion. The area is $\delta A|_V=-(2\pi/5)k^2r^4+O(r^6)$. The area-subtracted light vacuum collar has no $r^4$ coefficient on this profile, and the same-cut light state entropy is unchanged. Thus the retained response is

$$
\left[\delta S_{\rm comparison}|_V\right]_{r^4}
=-\frac{2\pi}{5}\,\eta_{\rm band} k^2\ne0.
$$

The time- and space-curvature couplings change the constraint coefficients without producing cancellation in this comparison. The script checks three speeds, including the luminal reference, and solves the updated lapse equation before testing the entropy. Its proper-time band is shorter than the squared radii in the numerical window. The calculation is a two-derivative and leading-area test, rather than a strict small-ball limit through the proper-time scale or a proof for arbitrary foliation-dependent operators. Additional local curvature or clock terms and their entropy may contribute beyond the retained order.

🟠 [Next] The next section computes the four-derivative terms of the luminal member, solves the corrected constraints, and tests the retained local entropy. The nonluminal member and independent finite clock terms remain open.

### Four-derivative shell terms and the corrected moving-ball constraint

🟢 [Done] Derived the four-derivative terms from the same heavy-tensor proper-time band and solved the corrected scalar lapse and momentum constraints for the luminal member. Recomputed the local boundary entropy on that data. Run [higher_derivative_clock_ball.py](experiments/higher_derivative_clock_ball.py).

Set $v=1$, so the matter and shell effective metrics agree. Write $A=A_0+C$ for the matched two-derivative coefficient and define
$J=\int_{s_1}^{s_2}e^{-M^2s}\,ds/s$ in the same band that gives $C=5(192\pi^2)^{-1}\int_{s_1}^{s_2}e^{-M^2s}\,ds/s^2$. The Lorentzian higher-derivative Lagrangian from the minimal rank-five Bochner operator is

$$
\frac{J}{32\pi^2}
\left[5\left(\frac{R^2}{72}+\frac{C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}}{120}
-\frac{E_4}{360}\right)
+\frac{\operatorname{tr}(\Omega_{\mu\nu}\Omega^{\mu\nu})}{12}\right].
$$

Here $C_{\mu\nu\rho\sigma}$ is the Weyl tensor, distinct from the coefficient $C$. Denote the scalar and Weyl couplings by $B_R=5J/(2304\pi^2)$ and $B_C=5J/(3840\pi^2)$. Use the same treatment of the integrated total derivative and the topologically completed Euler term as in the curved-ball calculation. Use identity fiber gluing for the heavy regional trace and the usual metric cone prescription for the rank part. Work on the perturbative branch continuously connected to the Einstein-scalar solution. In a constraint term already proportional to a four-derivative coefficient, evaluate the higher time derivatives using the leading equations, rather than keeping extra modes of a truncated action. [Vassilevich, four-derivative heat coefficient](https://arxiv.org/abs/hep-th/0306138) · [Fursaev, Patrushev, and Solodukhin, geometric cone curvature terms](https://arxiv.org/abs/1306.4000)

Choose the positive-expansion reference and the initial comoving scalar data $\zeta=f$, $\dot\zeta=0$ at $a_{\rm FLRW}=1$. This notation refers to the perturbation coefficient. At zeroth order in $B_R,B_C$, $\bar R=-6H^2$, $\dot{\bar R}=-6H\bar R$, $\delta K_0=\Delta f/H$, and $\delta R$ and the electric and magnetic Weyl tensors vanish on the test slice. They need not remain zero in time. In particular, $\delta\dot R=-2\bar R\,\Delta f/H$ follows from the clock trace equation and the leading scalar evolution $\ddot\zeta=\Delta f$ at the chosen time. The clock-projected spatial bundle has a trivial reference connection on flat FLRW slices in a comoving orthonormal frame. At linear order its spatial connection is that of the spatial metric, and the temporal internal rotation from a scalar shift is zero. Thus the quadratic connection-curvature action in this scalar calculation is independent of lapse and longitudinal shift. It does not correct these two constraints. Its canonical entropy variation also vanishes by the component trace under the stipulated gluing.

Let $U^{R}_{\mu\nu}$ and $U^{C}_{\mu\nu}$ be the metric Euler tensors of $R^2$ and Weyl-squared, so the field equation reads $2(A G_{\mu\nu}+B_R U^{R}_{\mu\nu}+B_C U^{C}_{\mu\nu})=T_{\mu\nu}$ in the metric sector. Work with projections onto the normalized clock normal $n$ and the slice. The $R^2$ tensor is $2R R_{\mu\nu}-g_{\mu\nu}R^2/2+2(g_{\mu\nu}\Box-\nabla_\mu\nabla_\nu)R$. The nonzero contributions to the order-reduced constraint at the chosen reading are

$$
\delta U^R_{nn}=-24\bar R\,\Delta f,\qquad
\delta U^R_{ni}=\frac{4\bar R}{H}\partial_i\Delta f,\qquad
\delta U^C_{ni}=-8H\partial_i\Delta f,\qquad
\delta U^C_{nn}=0.
$$

For the Weyl momentum contribution, the Weyl-squared variation is conformally covariant on the four-dimensional conformally flat background. In the flat conformal frame at the chosen reading the nonzero term is $4\partial_j\delta\dot E_{ij}$, where $\delta\dot E_{ij}=-3H(\partial_i\partial_j f)^{\rm TF}$. The lapse contraction contains only spatial derivatives of $E_{ij}$ and vanishes on this slice. [Bueno et al., curvature-action variation](https://arxiv.org/abs/1612.04374) · [Conformal weight of the Bach tensor](https://link.springer.com/article/10.1140/epjc/s10052-024-13168-9)

The corrected homogeneous lapse equation at fixed $H$ is $\bar\rho_\varphi=6AH^2+324B_RH^4$ at this order. In the linear density variation, use $\delta\rho_\varphi=-12AH^2\alpha$ because the lapse perturbation $\alpha$ is already of first order in the higher-derivative coefficients. The momentum equation fixes $\alpha$ and the lapse equation then fixes $\psi$, with the same infrared convention as before:

$$
\alpha=\frac{12B_R+4B_C}{A}\Delta f,\qquad
\psi=-\frac{f}{H}\left(1+\frac{12B_R\bar R}{A}\right),\qquad
\delta K=-3H\alpha-\Delta\psi .
$$

The correction induces a nonzero clock energy variation even though it was zero in the two-derivative comparison. The script checks both updated constraints exactly for the example Fourier amplitude.

For the boundary calculation the intrinsic slice data $f$ are held fixed by the initial-data choice, so the physical fixed-volume area variation is the same geometric functional of $f$. The $R^2$ entropy shifts the reference area density by $8\pi B_R\bar R$. Its additional term proportional to $B_R\delta R$ is second order in four-derivative coefficients, since $\delta R$ vanished at leading order. Likewise the Weyl entropy is zero at the retained order, even though the Weyl momentum contribution changed the lapse. The connected fiber heat trace has no linear contribution on the specified replica. The local geometric result is $\eta_{\rm ref}\delta A|_V$, with $\eta_{\rm ref}=4\pi(A+2B_R\bar R)$.

For a one-loop comparison, retain the leading reduced scalar vacuum collar response of the previous section. In a loop expansion a heavy one-loop change of the light vacuum determinant is a mixed higher-loop correction. The regional algebra, clock conditioning, and collar subtraction are those specified earlier. For the two-sinc profile with no central quartic monomial the retained light collar has zero $r^4$ coefficient. Therefore the retained fixed-volume coefficient is

$$
\left[\delta S_{\rm comparison}|_V\right]_{r^4}
=-\frac{2\pi}{5}\eta_{\rm ref}k^2 .
$$

It is nonzero in the perturbative regime with $\eta_{\rm ref}>0$. The numerical check uses a common band $[10^{-6},2\times10^{-6}]$ for the heavy induced Einstein coefficient and both curvature-squared couplings. It verifies the coefficient over four radii in the local band regime. This test includes solved higher-derivative constraints and the corresponding local entropy, at fixed physical volume, for $v=1$. It does not derive the finite terms of a unified microscopic collar prescription, evaluate additional clock interactions, or establish the result at $v\ne1$.

🟠 [Next] The next section supplies a common proper-time Gaussian benchmark and an action-derived fixed volume. The physical inhomogeneous light determinant still has to be computed.

### Shared proper-time band and the Einstein-frame volume test

🟢 [Done] Matched a light and heavy Gaussian comparison in a common proper-time band, derived its local boundary terms and a fixed generalized volume from the retained action, and tested the corrected constraints. The actual inhomogeneous reduced clock determinant remains open. Run [shared_regulator_clock_ball.py](experiments/shared_regulator_clock_ball.py).

Stay in the luminal member and use the expanding clock-aligned reference. At leading order the reduced scalar on homogeneous flat FLRW has constant $\varepsilon_H=3$. Its quadratic action on that reference becomes the massless minimally coupled scalar action after a constant canonical normalization. This equivalence fixes the homogeneous operator. To conduct a shared-regulator benchmark, **choose** its off-reference extension to be the minimal covariant scalar operator $D_l=-\nabla^2$. For the five heavy components use the previously specified projected Bochner operator $D_h=-\nabla_\Omega^2+M^2$. Take a single finite proper-time band on the same metric, with identity gluing for the internal bundle, and the metric cone prescription for the rank terms. This defines a common Gaussian comparison. It is not yet a derivation of the physical light Hessian on the inhomogeneous constrained background. [Maldacena, reduced scalar dynamics](https://arxiv.org/abs/astro-ph/0210603) · [Vassilevich, Laplace-type coefficients](https://arxiv.org/abs/hep-th/0306138)

Write $I_l,I_h$ for $\int_{s_1}^{s_2}ds\,e^{-m^2s}/s^2$ at masses $0,M$, and $J_l,J_h$ for the integrals with $ds/s$. After matching the cosmological term, the smooth coefficients are

$$
A_E=A_0+\frac{I_l+5I_h}{192\pi^2},\qquad
B_R=\frac{J_l+5J_h}{2304\pi^2},\qquad
B_C=\frac{J_l+5J_h}{3840\pi^2}.
$$

The Euler coefficient is $-(J_l+5J_h)/(11520\pi^2)$ and the projected connection contributes $J_h\operatorname{tr}\Omega^2/(384\pi^2)$ in the action. Use the topologically completed Euler contribution and the same total-derivative convention as before. The cone area response is $(I_l+5I_h)/(48\pi)$ per unit area, exactly $4\pi(A_E-A_0)$. The band contributions are accounted for once through the matched action and its boundary terms; the separate light mutual-information collar is not added to this benchmark. For fixed band bounds these contributions are finite, but this is not a claim about all finite terms of the renormalized theory. [Solodukhin, proper-time entropy and coupling renormalization](https://arxiv.org/abs/1104.3712)

For a specified generalized volume use the Einstein-frame volume of the $F(R)=A_E R+B_R R^2$ sector. This is defined from the action by its auxiliary scalar $F'(R)$, not by imposing stationarity on the test ball. Normalize the conformal transformation to the spatially homogeneous reference at the chosen clock reading. For $F'(\bar R)>0$ this gives

$$
W_E=\int_B\left[\frac{F'(R)}{F'(\bar R)}\right]^{3/2}dV,\qquad
\delta W_E=\delta V+\frac{3B_R}{A_E+2B_R\bar R}\int_B\delta R\,dV_0 .
$$

This coincides at first order with the normalized curvature-derivative expression of the $f(R)$ comparison. The Weyl curvature derivative is trace free and has zero volume-projection contribution, while the explicitly spatial projected connection has zero contraction with the clock normal in that projection. The Euler term is treated topologically. This defines a fixed geometric quantity in the specified local action. It does not assert that the maximally symmetric causal-diamond first law already holds on expanding FLRW with a fluctuating clock. [Bueno et al., $f(R)$ generalized volume](https://arxiv.org/abs/1612.04374)

Re-solve the luminal expanding-background constraints of the preceding section with the total $A_E,B_R,B_C$. At $\zeta=f,\ \dot\zeta=0$ on the chosen reading, the corrected lapse is $(12B_R+4B_C)\Delta f/A_E$ and the shift potential is $-f(1+12B_R\bar R/A_E)/H$. The scalar energy changes through this lapse, and the checked normal and momentum constraints include these corrections. On the leading constrained data $\delta R=\delta C_{\mu\nu\rho\sigma}=0$ on the slice. The corrected scalar curvature perturbation enters $\delta W_E$ multiplied by $B_R$ and the corrected Weyl perturbation enters the entropy multiplied by $B_C$. Both effects are beyond first order in the four-derivative couplings for this profile. Thus fixed $W_E$ gives the same ball displacement as fixed $V$ at the retained order.

The finite $R^2$ boundary response in the band is $8\pi B_R\bar R\,\delta A|_V$. The Weyl and Euler variations and the identity-sewn projected-connection term add no first-order response on these data. For the two-sinc profile in the previous section the retained result is therefore

$$
\left[\delta S_{\rm band+local}|_{W_E}\right]_{r^4}
=-\frac{8\pi^2}{5}(A_E+2B_R\bar R)\,k^2 .
$$

The same-cut displacement has zero linear state modular response in the Gaussian comparison. This nonzero coefficient is verified with the corrected constraints and four ball radii in the short proper-time regime. There is also a perturbative obstruction independent of the numerical band: with a nonzero bare Einstein term and quantum and finite curvature corrections treated as loops, the leading coefficient is $-8\pi^2 A_0 k^2/5$. A candidate cancellation order by order would need another term at that same classical order, or a different leading fixed-quantity prescription. This observation does not apply to a purely induced theory with no tree Einstein term.

The result leaves open the actual shared microscopic clock-tensor question. To replace $D_l$ by the true reduced light operator, expand the coupled action to quadratic order in quantum fluctuations about the spatially inhomogeneous constraint solution, include the measure from eliminating lapse and shift, and derive the branched regional trace. Agreement of homogeneous covariances alone does not fix that operator or its finite boundary terms. The remaining long proper-time and possible clock-dependent contributions are also outside this local band result.

🟠 [Next] The following sections derive the inhomogeneous bulk scalar block and its canonical Gaussian measure. The common regulated boundary trace remains to be evaluated.

### Reduced light Hessian on inhomogeneous clock data

🟢 [Done] Derived the first-order-in-background scalar bulk Hessian by constraint elimination and the induced configuration measure of the reduced canonical theory. Found an explicit kinetic response that differs from the minimal scalar extension used in the shared-band benchmark. The branched determinant and its finite boundary coefficient remain open. Run [inhomogeneous_clock_hessian.py](experiments/inhomogeneous_clock_hessian.py).

Work at the leading Einstein-scalar order for the light one-loop operator. In uniform-clock gauge put $h_{ij}=a_{\rm FLRW}^2e^{2\zeta}\delta_{ij}$ in the scalar sector, keeping the original metric variable that specifies the cut. Let $A=M_{\rm Pl}^2/2$, $N_i$ be the covariant shift, and $E_{ij}=(\dot h_{ij}-2D_{(i}N_{j)})/2$. With the ordinary Einstein boundary convention the scalar-gauge bulk ADM action is

$$
S=\int dt\,d^3x\,\sqrt h
\left[N A R^{(3)}+
\frac{A(E_{ij}E^{ij}-E^2)+\dot{\bar\varphi}^{\,2}/2}{N}\right].
$$

The inhomogeneous background profile is $\zeta=\epsilon f(t,x)$, with $f$ evolving by the leading equation and with $\dot f=0$ at the test reading. Write the fluctuation as $z$, and use the fixed infrared inverse of the coordinate Laplacian in
$\alpha[q]=\dot q/H$ and $\psi[q]=-q/H+a_{\rm FLRW}^2\varepsilon_H\Delta^{-1}\dot q$.
The complete scalar-to-scalar quadratic **bulk form through first order in $\epsilon$** has the following coefficient-extraction representation:

1. In the ADM action substitute $\zeta=\epsilon f+t z$, $N=1+\alpha[\epsilon f+t z]$, and $N_i=\partial_i\psi[\epsilon f+t z]$.
2. Expand to total degree three and extract the coefficient of $t^2$, retaining $\epsilon^0$ and $\epsilon^1$. Polarize this form in $z$ to define the Hessian. Time and space derivatives act before the coefficient extraction. This definition preserves the original field variable and avoids integrating by parts across the future replica cut.

The representation eliminates the lapse and shift for the bulk scalar block to the stated order. Corrections to their homogeneous linear solution multiply a constraint already zero on that solution and first affect the substituted cubic action only at higher degree. Equivalently this is the first derivative of the auxiliary Schur complement. A background scalar can mix the reduced scalar and tensors at quadratic order. A mixed insertion has zero first trace against a block-diagonal reference operator with independent sewing, but block-diagonal sewing must be checked for the constrained regional algebra. The extraction here gives the scalar diagonal block and makes no assertion of full regional factorization. [Maldacena, constraint substitution through cubic order, Section 3.2](https://arxiv.org/abs/astro-ph/0210603)

The auxiliary lapse stiffness illustrates why the homogeneous extension fails. At fixed $h$, set $\delta N=\bar N\alpha$, $e_{ij}=\delta E_{ij}$, and $Q_0=A(\bar E_{ij}\bar E^{ij}-\bar E^2)+\dot{\bar\varphi}^{\,2}/2$. The quadratic terms in these auxiliary variables are

$$
\frac{\sqrt h}{\bar N}\left[
Q_0\alpha^2-2A\alpha(\bar E^{ij}-\bar Eh^{ij})e_{ij}
+A(e_{ij}e^{ij}-e^2)\right].
$$

On the leading constrained background $Q_0=\bar N^2 A R^{(3)}$, so the first term vanishes in flat FLRW and is generally present on the perturbed slice. The reduced kinetic form $\mathcal M_f$ is the velocity-velocity Hessian of the extracted action. At the test reading, an independent expression for its quadratic form is obtained by setting $z=0$, $\dot z=w$, $e_{ij}=h_{ij}w-D_{(i}s_{j)}$, and $s_i=3\partial_i\Delta^{-1}w$ at $a_{\rm FLRW}=1$. Insert these in the displayed form with $\alpha=w/H$. The script differentiates the result at zero background amplitude. For an explicit noncollinear Fourier test $f=\cos z_{\rm coord}$ and $w=\cos x_{\rm coord}(1+\cos z_{\rm coord})$, the variation of the velocity-quadratic action density divided by $A$ is $31.75$ in the chosen units. A minimal scalar with the same homogeneous kinetic normalization on the perturbed metric gives $9.00$. Both agree at zero background amplitude. This is a bulk operator comparison, not a new curvature coefficient inferred from entropy.

### Reduced measure and the remaining replica calculation

In the reduced scalar phase-space convention the canonical momentum is conjugate to the original $\zeta$ variable, as follows from the trace part of $\pi^{ij}\delta h_{ij}$. Use the canonical Liouville measure in these variables at a finite time-sliced regulator. Gaussian integration of the reduced momentum multiplies the configuration measure by $(\det\mathcal M_f)^{1/2}$ on each time step, up to a common normalization. At first order its log variation is $\tfrac12\operatorname{Tr}(\mathcal M_0^{-1}\delta\mathcal M)$. This is the measure of the reduced scalar canonical model. It is not permission to discard the determinants from an unreduced gauge-fixed covariant integral if that integral is used instead.

On a finite bulk regulator where $\mathcal O_f$ is the Euclidean quadratic form and $\mathcal M_f$ the measure metric, the normalized determinant is that of $\mathcal M_f^{-1/2}\mathcal O_f\mathcal M_f^{-1/2}$ with its induced domain. Since the inverse spatial Laplacian enters the reduced kinetic form, normalizing the field this way need not commute with restricting it to a ball. Consequently the canonical cyclic sewing of the original variables cannot just be reused as scalar identity sewing for the normalized field. The lapse and shift Green functions, the physical regional algebra, and the induced measure must be implemented on the sewn regulator before taking the shared proper-time trace.

If that replica operator is $D_n$ with the canonical measure included, the needed first variation in the same band would be $\tfrac12\int_{s_1}^{s_2}ds\,\operatorname{Tr}(e^{-sD_{n,0}}\delta D_n)$ before taking the replica derivative. The bulk Hessian above determines inputs to this trace but does not determine the sewn domains and boundary operators. A scalar Laplace-type coefficient from the earlier minimal extension is therefore not a calculation of the finite boundary term for the true reduced clock. No full fixed-generalized-volume $r^4$ cancellation is decided here. The previous nonzero classical coefficient for a separate bare Einstein term remains a perturbative check, with the same limitations on the leading boundary prescription. [Vassilevich, operator and boundary dependence of heat coefficients](https://arxiv.org/abs/hep-th/0306138)

The domain transformation can be fixed at finite time spacing. If the original configuration variable obeys $z^+=P_Bz^-$ across the seam, with $P_B$ the cyclic permutation of the retained sites, then $y^\pm=\mathcal M_\pm^{1/2}z^\pm$ obeys

$$
y^+=\mathcal M_+^{1/2}P_B\mathcal M_-^{-1/2}y^- .
$$

The two measures need not be the same if the data differ on the two sides. Even with the same mass matrix on both sides, this transformation does not reduce to $P_B$ if the mass matrix mixes sites across the cut. A finite coupled Gaussian transfer comparison in [reduced_clock_sewing.py](experiments/reduced_clock_sewing.py) implements both domains with the same proper-time band. The one-sheet response agrees; at two sheets the linear band-action responses are $-0.046293670$ for the transported canonical seam and $+0.015549479$ if the permutation is left unchanged. This benchmark isolates the change in replica domain. It is not a numerical estimate of the finite sphere coefficient of the constrained clock.

🟠 [Next] The next section evaluates the transported seam insertion of the inhomogeneous ADM kinetic operator on a lattice ball. The complete sewn trace and the finite ball coefficient remain to be extracted.

### Induced replica seam of the reduced clock on a spherical cut

🟢 [Done] Applied the transported sewing rule to the actual first-order ADM kinetic block for a radially inhomogeneous clock profile on a spatial lattice. Evaluated the seam insertion in a common finite proper-time band for the light block and the heavy reference. The full ball determinant and generalized-volume coefficient remain open. Run [reduced_clock_ball_seam.py](experiments/reduced_clock_ball_seam.py).

To isolate this term, freeze the clock data at the test reading. Use the constrained velocity form of the preceding section, divide by the homogeneous coefficient, and write the normalized mass metric $\mathcal M=I+\epsilon M_1+O(\epsilon^2)$. Construct $M_1$ from the spatial derivative matrices, the fixed inverse Laplacian on nonconstant modes, and the chosen profile $f$. At $a_{\rm FLRW}=1$, the fields used in the velocity form are $w=\dot z$, $s_i=3\partial_i\Delta^{-1}w$, and $\alpha=w/H$. The implemented matrix reproduces the prior noncollinear Fourier test of the bulk kinetic form. The test relative to the physical region uses a sampled radial sinc-minus-one profile tapered outside the ball. Its periodic spectral regulator projects out the homogeneous part of the *mass variation*, while a positive reference oscillator regulator retains a full local site algebra. The ball is the set of lattice sites inside the clock-slice sphere at the reference amplitude. For small enough variation no site changes membership. This construction evaluates the sewing insertion at that set of sites; it does not approximate the moving-cut derivative by that fact.

For $n$ integer sheets let $P_B$ be the canonical cyclic permutation. Its first transported variation is $\delta\widetilde P_B=[M_1,P_B]/2$, with $M_1$ repeated across sheets. In the replica Fourier basis the unperturbed seam in branch $j$ is $I+(e^{2\pi i j/n}-1)\Pi_B$, where $\Pi_B$ is the spatial projector onto the sites in the ball. The normalizations use the same frozen mass metric on each side. Each Euclidean time-link action is a squared difference of adjacent normalized variables. Vary the final link by the transported seam, leaving the bulk Hessian fixed to extract the domain contribution. For each branch this gives an explicit Hermitian operator insertion $\delta D_{\rm seam}$ and a band variation

$$
\delta W_{\rm seam}(n)
=\frac12\int_{s_1}^{s_2}ds\,
\operatorname{Tr}(e^{-sD_{n,0}}\delta D_{\rm seam}).
$$

In the finite numerical test use the same dimensionless band $[0.02,0.04]$ and time lattice for the two reference field operators. With 125 spatial sites and four temporal steps the results are:

| Reference radius | Sites in ball | $\delta W_{\rm seam}(1)$ | $\delta W_{\rm seam}(2)$ | $\delta W_{\rm seam}(3)$ |
|---:|---:|---:|---:|---:|
| 0.27 | 7 | 0 | +0.280214 | +0.423390 |
| 0.38 | 19 | 0 | -0.087399 | -0.134431 |

The two-sheet trace insertion agrees with a separate central difference that transports the seam by the exact square root of the perturbed mass matrix. The heavy reference has a site-local mass metric from the volume element, which commutes with the site projector. Its transported-seam contribution is zero in this same band. This heavy statement is only about the domain change from kinetic normalization. The heavy field can still have a bulk curvature response and the ordinary cone entropy.

The contrast establishes that the original-variable sewing can change the light proper-time replica response even when the reference is a local Gaussian. The displayed entries are **integer-replica action variations from one insertion**, not von Neumann entropies or finite coefficients of $r^4$. Two radii on one coarse lattice do not resolve a small-ball expansion. A replica derivative at one requires the normalized physical replica family, not an interpolation of these entries alone. The full regulated calculation also needs the remaining inhomogeneous time and spatial Hessian insertion, smooth-background subtraction, the continuum moving-cut response at fixed generalized volume, and any scalar-tensor regional constraint contribution. None of these is determined by the isolated insertion. Consequently no full fixed-generalized-volume cancellation is decided here.

🟠 [Next] The next section implements the full frozen-reading quadratic transfer matrix. The time-dependent and continuum moving-cut traces remain open.

### Frozen-reading transfer matrix and the canonical replica derivative

🟢 [Done] Constructed the finite transfer Hamiltonian of the reduced scalar, including its position, velocity, and mixed forms. Evaluated the canonical $n=1$ derivative and compared separate integer-replica band traces with the heavy field at the same regulator. Run [reduced_clock_transfer.py](experiments/reduced_clock_transfer.py).

At the selected clock reading use $a_{\rm FLRW}=1$, $\dot f=0$, and freeze the background coefficients for a transfer comparison. Compute the scalar quadratic fluctuation form from the cubic ADM action by subtracting the constant term and extracting the term quadratic in the fluctuation around the nonuniform $f$. The implementation retains the intrinsic spatial-curvature terms, clock kinetic energy, longitudinal shift, and all velocity-position cross terms. Its velocity block agrees with the independent kinetic extraction used in the seam test. Use the standard reduced quadratic-action convention at the homogeneous reference and the direct cubic ADM extraction for the change. This is a specified canonical convention at one reading. It does not evolve the background or determine a boundary prescription for the full time-dependent path integral.

In original reduced clock variables $z,p$ write the quadratic Lagrangian as
$\dot z^{\mathsf T}\mathcal M\dot z/2+\dot z^{\mathsf T}Bz-z^{\mathsf T}Kz/2$. Its canonical momentum is $p=\mathcal M\dot z+Bz$ and the frozen Hamiltonian is

$$
H_{\rm fr}=\tfrac12(p-Bz)^{\mathsf T}\mathcal M^{-1}(p-Bz)+\tfrac12z^{\mathsf T}Kz .
$$

Use symmetric operator ordering and the canonical Hilbert space of the finite oscillator sites. The background perturbation is small enough that the Hamiltonian is positive. The transfer operator is $e^{-\Delta\tau H_{\rm fr}}$. Integrating over $p$ in the short-step kernel gives the configuration measure proportional to $(\det\mathcal M)^{1/2}$ and gives an imaginary mixed derivative in the Euclidean action. This kernel sews the original variables on the sites inside the cut. A change to normalized variables transports the seam as in the preceding section.

For the canonical Gaussian transfer trace use the ground-state limit of the frozen Hamiltonian. Obtain the regional occupation numbers $b_j=\nu_j-\tfrac12$ from its restricted covariance. They determine the normalized fractional trace for real $n$ near one:

$$
W_n^{\rm can}=-\log\operatorname{Tr}\rho_B^n
=\sum_j\log[(1+b_j)^n-b_j^n].
$$

The derivative at one is the Gaussian entropy and is checked directly against the derivative of the fractional trace, without fitting integer replicas. A two-sided change of the inhomogeneous background gives first variations $-0.377703421$ and $-0.505796764$ for the seven-site and nineteen-site balls. They are unbanded finite-regulator state comparisons on fixed sets of sites. They are not finite gravitational boundary coefficients.

Independently, put the full change of the frozen quadratic form on a four-step Euclidean time regulator, using midpoint links and the canonical measure. Include the transported seam in both the velocity and potential terms. Compare the heavy reference on the same regulator and proper-time band $[0.02,0.04]$. For the heavy test include the base-metric kinetic, gradient, and mass variations. The identity-sewn connection has zero first trace at the trivial reference. For both fields subtract $n\delta W_1$ from the integer-replica band variation. The resulting first variations are:

| Reference radius | Light, $n=2$ | Light, $n=3$ | Heavy rank five, $n=2$ | Heavy rank five, $n=3$ |
|---:|---:|---:|---:|---:|
| 0.27 | -0.075035 | -0.112641 | +0.003127 | +0.004884 |
| 0.38 | -0.017884 | -0.043499 | +0.003657 | +0.005753 |

The band-restricted determinant is a different observable from the complete normalized canonical fractional trace. An analytic continuation of the partial band contributions must be tied to a common physical prescription; the canonical formula for the complete transfer trace does not give that continuation by itself. In particular, the finite one-sheet subtraction cancels the replicated smooth contribution for the same time regulator but does not prove that any remaining number is a universal continuum surface term.

Both calculations use a $3^3$ spatial grid with a fixed set of sites at each radius and a positive infrared oscillator convention. The data do not control the change in site membership when the physical ball moves, the time evolution of the clock background, or possible scalar-tensor sewing from the constrained regional algebra. The two radii therefore do not isolate an $r^4$ coefficient. No conclusion about the cancellation of the finite fixed-$W$ residual follows from these checks.

🟠 [Next] The next section implements time-dependent canonical transfer on a shared spatial regulator and tests boundary tracking. The common renormalized continuum response remains open.

### Evolving clock transfer and a moving-boundary lattice diagnostic

🟢 [Done] Implemented time-dependent Gaussian transfer operators for the light and heavy sectors in original canonical variables, computed their normalized canonical $n=1$ derivatives on a common spatial regulator, and separated the reference shape response of the moving ball. The continuum entropy matching remains open. Run [evolving_clock_transfer.py](experiments/evolving_clock_transfer.py).

Use the luminal Einstein-scalar reference with $a_{\rm FLRW}(t)=t^{1/3}$ between $t=0.9$ and $1$ in the chosen units. Evolve the leading inhomogeneous clock-slice background by its linear scalar equation, with a radially tapered sinc profile and $\dot f=0$ at the final clock reading. Use the same periodic box of length $1.8$ and the same spatial spectral regulator for both sectors. The spatially constant scalar mode has the infrared convention of the transfer comparison; a lattice mean is removed from the sampled deformation. The light Hessian is extracted from the constrained cubic ADM form at each time step, including the background rate $\dot f$ in the lapse and shift. At $a_{\rm FLRW}=1$ and $\dot f=0$ the implementation agrees with the independent frozen-reading Hessian.

The heavy field is a rank-five Gaussian bundle on the same leading geometry. Its kinetic, potential, and mixed matrices include the volume-element, lapse, and shift variations. In the trivial comoving reference frame the five component covariances agree, and the terms linear in the internal projected connection have zero first-order entropy trace with component-blind regional sewing. The rank-five results below use five times the base-metric response. All reported entropy variations are first order in the prescribed background deformation.

For each sector take a specified initial Gaussian, namely the homogeneous instantaneous vacuum at $t=0.9$, and use it in all perturbed evolutions. Propagate the centered covariance by midpoint symplectic transfer with $JH(t)$ in the original canonical variables. Each discrete step is checked to preserve the canonical symplectic form. The momentum measure is the canonical phase-space one; converting to a configuration kernel would again require the kinetic determinant and the transported domain. At the final reading compute the normalized fractional trace from the restricted Gaussian covariance of the physical site algebra. The numerical $n=1$ derivative agrees with the direct Gaussian entropy. This common-regulator calculation uses a spatial cutoff and the complete canonical trace, not an interpolation of a truncated proper-time determinant. The common initial state on the finite regulator has not been shown to have the required ultraviolet behavior on the inhomogeneous continuum background.

Track the physical sphere using the previously defined action-based $W_E$. At the retained order for these data $\delta R^{(4)}=0$ at leading order, so the radius variation at fixed $W_E$ is the fixed-volume result $\delta R_{\rm coord}=-r f_B$. On all three tested lattices the two displaced sphere radii select the same sites as each other. Thus the canonical state variation at that fixed center has no contribution from changes in site membership. It is unsafe to treat this zero discrete crossing count as the physical shape derivative.

As a separate shape calculation, average the center of the **homogeneous reference** over one lattice cell. Let $S_0(B)$ be its regional entropy and let $B_{\mathbf n}$ be the set of sites strictly inside the radius-$r$ sphere centered at $r\mathbf n$, excluding the origin. A boundary crossing adds the origin, and translation invariance relates all lattice sites to this one. The first shape variation of the center-averaged reference entropy is then

$$
\delta S_{\rm shape}
=\frac{r^2\,\delta R_{\rm coord}}{a^3}\int_{S^2}
\left[S_0(B_{\mathbf n}\cup\{0\})-S_0(B_{\mathbf n})\right]d\Omega .
$$

The integral keeps the regulator dependence of the finite reference entropy. This is a shape diagnostic under the declared center average. It cannot simply be added to a state derivative taken at only the centered cut. A common averaged observable must also average perturbed states with the same translation prescription.

At the larger radius $r=0.67$ the numerical results are:

| Spacing | Light state response, centered | Heavy state response, centered | Light reference shape response | Heavy reference shape response |
|---:|---:|---:|---:|---:|
| 0.600 | -3.240375 | +0.790005 | +0.015113 | +0.047269 |
| 0.360 | -11.944221 | +3.371235 | +0.046972 | +0.192904 |
| 0.257 | +232.207971 | +14.560293 | +0.107227 | +0.479072 |

The small-radius case $r=0.46$ is also evaluated. Halving the time step at $a=0.36$ changed the centered state responses by at most about $0.0431$ in absolute value, much smaller than the spatial refinement changes. The sphere quadrature was varied on the coarser two spatial grids. There is no controlled continuum plateau. The raw entropies have not been matched to the gravitational determinant in this common spatial scheme, and the spatial dependence may include regulator and initial-state effects. These observations neither prove nor rule out cancellation of the renormalized $r^4$ term at fixed generalized volume.

🟠 [Next] The next section implements a first-adiabatic-order state and a common center average. Independent gravitational matching and a controlled continuum response remain open.

### Adiabatic initial data and a common average of the moving cut

🟢 [Done] Replaced the common homogeneous initial state by a background-matched first-adiabatic-order Gaussian. Evaluated the state and moving-boundary terms with the same cell-center average on three spatial cutoffs. Tested why the known first-order reduced operator is insufficient for matching the smooth gravitational counterterms. Run [adiabatic_clock_ball.py](experiments/adiabatic_clock_ball.py) and [lattice_counterterm_identifiability.py](experiments/lattice_counterterm_identifiability.py).

At the initial clock reading diagonalize each positive, inhomogeneous phase-space Hamiltonian $H$ and construct its instantaneous pure covariance $V_0$. The first adiabatic correction $V_1$ in the tangent space of pure Gaussian covariances solves

$$
\dot V_0=(JH)V_1+V_1(JH)^{\mathsf T}.
$$

In the basis that diagonalizes $i H^{1/2}JH^{1/2}$, the off-diagonal pure tangent connects the opposite frequency signs. Solve those entries by dividing the transformed $\dot V_0$ by $-i(\omega_i-\omega_j)$, where the eigenvalues $\omega_i$ are signed. In particular the denominators are frequency sums in absolute value for the mixing of positive and negative frequencies. Set the other entries to zero, then project the positive candidate covariance to the pure Gaussian manifold so the regulator obeys the uncertainty relation exactly. This projection changes the construction beyond the linear adiabatic term. The numerical evolution checks $VJV=J/4$ at the initial and final readings and checks the first-order transport equation in the paired spectral block. The prescription matches the finite-lattice background and its first time derivative. A first-order construction alone does not prove a continuum Hadamard property or sufficient ultraviolet control for the renormalized entropy.

For the region at the final clock reading, average the actual retained site set over centers $c$ in one lattice cell, with the same fixed inhomogeneous profile for both parts of the response. The geometry is the conformal perturbation $f$ of the final slice. Define $f_B(c)$ as its average over the unperturbed radius-$r$ ball about $c$, and let

$$
L(c,n)=\int_0^r f(c+s n)\,ds .
$$

The coordinate displacement of the geodesic boundary at fixed volume is
$\delta R(c,n)=\langle L(c,n)\rangle_{S^2}-r f_B(c)-L(c,n)$.
A first-order geodesic length can be evaluated on the reference radial segment; path deflections first enter at higher order for fixed endpoints. The mean displacement satisfies the physical volume constraint including the conformal metric variation. As above, fixed $W_E$ and fixed $V$ give this same geometry at the retained order in four-derivative couplings for these data.

Evaluate the state part by averaging its entropy derivative on the unperturbed site sets centered at $c$. Evaluate the shape part by integrating the entropy increment of the site that crosses the cut, with the same center-cell prescription and with the directional displacement $\delta R(c,n)$ inside the integral. Translation invariance is used only to evaluate the *reference* entropy increment at the origin. In the displacement weight the center is mapped back into the original cell and the actual inhomogeneous profile is evaluated there. Thus the measured combination uses one cell average for both parts, unlike the preceding centered-state comparison. The calculation retains the prescribed physical site algebra and normalized canonical fractional traces. Center and angular quadratures are varied separately within two combined numerical settings.

At $r=0.67$ the sums of the state and shape derivatives, with the finer quadratures, are:

| Spatial spacing | Light clock | Heavy rank five |
|---:|---:|---:|
| 0.600 | -0.599132 | +0.124442 |
| 0.360 | -0.104221 | +1.201198 |
| 0.257 | +43.610937 | +2.990797 |

At $r=0.46$ the light results are approximately $0.346415$, $2.444661$, and $7.417648$. These are bare finite-lattice derivatives. They differ from the earlier experiment in both the initial state and the cut average, so the change cannot be attributed to either modification alone. There is still no controlled spatial-cutoff plateau. The run does not fit an $r^4$ coefficient.

### What is needed for the lattice gravitational subtraction

A same-lattice entropy subtraction requires an independent smooth-action match, including its response at second order in a metric perturbation. The spatial integral of the scalar curvature has zero first variation about a flat periodic slice. In a fixed proper-time band the second variation of a smooth determinant contains both a two-insertion term from $\delta D$ and a single insertion of $\delta^2D$. For example, taking $D_\epsilon=D_0+\epsilon V+\epsilon^2 Q$, changing $Q$ leaves every first-order replica insertion unchanged but changes the smooth determinant's second derivative by $\int_{s_1}^{s_2}ds\,\operatorname{Tr}(e^{-sD_0}\Delta Q)$. The numerical check uses the same type of spatial spectral lattice and a gradient-squared $Q$, and verifies that the change survives at both tested spacings while the first variation is unchanged. This is an identifiability test, not an added term in the proposed theory.

For the physical reduced light operator, this second insertion requires the metric dependence of the constrained Hessian to second order, including the corresponding measure. The cubic bulk reduction supplies the first insertion only. Assigning a lattice Newton counterterm from the first-order entropy or importing its value from the continuum proper-time comparison would bypass the required independent match. Thus the gravitational divergence subtraction in this spatial regulator and the continuum fixed-$W_E$ cancellation are not yet established.

### Quartic constraint elimination and the smooth action response

🟢 [Done] Computed the second background variation of the reduced scalar Hessian and its canonical measure at a fixed clock reading. Evaluated the smooth determinant response on the same spatial spectral lattice used in the preceding ball tests. Reproduce the calculation with [quartic_clock_reduction.py](experiments/quartic_clock_reduction.py) using NumPy and PyTorch.

Let $q=(\zeta,\dot\zeta)$ and $b=(\alpha,s_i)$ denote the scalar initial data and all four ADM auxiliaries. Write $S_k$ for the homogeneous degree-$k$ ADM action on the uniform-clock slice, $C=\partial_b^2 S_2$ on the mean-zero auxiliary space, and $b_1(q)$ for the linear constraint solution. With $g=P_{\ne0}\partial_b S_3(q,b_1)$ the second-order correction and quartic action are

$$
b_2=-C^{-1}g,\qquad
S_{4,\mathrm{red}}=S_4(q,b_1)-\tfrac12g^{\mathsf T}C^{-1}g .
$$

The latter follows from substituting $b_2$ into $g^{\mathsf T}b_2+\tfrac12 b_2^{\mathsf T}Cb_2$. Terms containing $b_3$ multiply the vanishing linear constraint. The implementation includes the transverse shift and the spatial connection. It checks both projected constraints and recovers the existing cubic Hessian. This calculation uses the frozen scalar diagonal block. The homogeneous constraint and scalar–tensor mixing remain open.

At background $q=\epsilon f$, the fluctuation Hessian has derivatives $H_1=S_{3,\mathrm{red}}''(f)$ and $H_2=2S_{4,\mathrm{red}}''(f)$, where primes denote fluctuation Hessians. The kinetic blocks $M_i$ give the canonical configuration weight $\mu\propto\sqrt{\det M}$ and

$$
(\log\mu)_2=\tfrac12\operatorname{Tr}(M_0^{-1}M_2-M_0^{-1}M_1M_0^{-1}M_1).
$$

The lattice log determinant verifies this expression. For $M_0=m_0I$, write $m_\epsilon=M_\epsilon/m_0$ and $O_\epsilon$ for the frozen Euclidean quadratic operator scaled by $m_0$. Normalizing on a common domain gives $D_\epsilon=m_\epsilon^{-1/2}O_\epsilon m_\epsilon^{-1/2}$ and

$$
D_2=O_2-\{m_1,O_1\}
+\{3m_1^2/4-m_2/2,O_0\}+\tfrac12m_1O_0m_1,
$$

where braces denote the anticommutator. The numerical smooth calculation uses the canonical frequencies of the full frozen kinetic, mixed and potential blocks. It integrates their heat trace per unit Euclidean time over $s\in[0.02,0.04]$, independently of the regional entropy. Amplitude derivatives agree with half-step estimates at relative tolerance $10^{-4}$.

| Spacing | Initial data | Second smooth derivative, cubic alone | Second smooth derivative through quartic |
|---:|---|---:|---:|
| 0.600 | Axial, zero velocity | 19846.38 | -22608.66 |
| 0.360 | Axial, zero velocity | -172592.67 | -287183.56 |
| 0.360 | Diagonal, zero velocity | -3888429.56 | -4394614.13 |
| 0.360 | Axial, zero linear extrinsic perturbation | -179772240.06 | -181607112.22 |

The last row uses $\dot f=\Delta f/(3H)$, so the first-order shift vanishes and $\delta K^i{}_j=0$. Its spatial metric agrees with the second row throughout the conformal path on the clock slice. The intrinsic benchmark $\partial_\epsilon^2\int\sqrt h\,{}^{(3)}R=4\int|\nabla f|^2$ is identical for both rows. Their smooth responses differ substantially. A single fit to this benchmark would conflate intrinsic curvature with lapse, evolution, and other operator dependence. At the finer spacing the smallest axial momentum has $qa=2\pi/5$. The fixed positive proper-time band gives a finite smooth response and leaves the ultraviolet divergence undetermined.

🟠 [Next] Match independent curvature and clock invariants on smooth time-dependent backgrounds at $qa\ll1$ using a controlled ultraviolet cutoff sequence and the complete constrained field content. Apply the independently matched counterterms to the common center average, with a verified ultraviolet initial state. Take the continuum limit at fixed generalized volume before extracting the small-ball coefficient. The divergence subtraction and continuum $r^4$ cancellation remain undetermined.

### Time-dependent ultraviolet control

🟢 [Done] Matched the curvature and independent potential insertions in a time-dependent Laplace-type control, using the same periodic box and spectral spatial derivative as the clock reduction. Reproduce the cutoff and spacing sweep with [time_dependent_uv_match.py](experiments/time_dependent_uv_match.py).

Use one real scalar of mass $m=2$, with independent multiplication source $X$, in the Euclidean metric $dt^2+e^{2z(t)}d\mathbf{x}^2$. This tests the minimal scalar part of an effective heavy-sector model. It omits the tensor connection, the dynamical clock and its constraints. For each spatial mode, conjugating by $e^{3z/2}$ gives the flat-measure operator

$$
D_k=-\partial_t^2+e^{-2z}k^2+m^2+X+\tfrac32 z''+\tfrac94(z')^2 .
$$

Set $z=\epsilon\cos\nu t$ and average over a period. The first insertion is $(-2k^2-\tfrac32\nu^2)\cos\nu t$. The averaged second insertion is $2k^2+\tfrac94\nu^2$. The two-insertion heat trace contains $\int_0^1 e^{-s u(1-u)\nu^2}du$, from the continuous time momentum Gaussian. Combining it with the single second insertion gives the coefficient of $\nu^2$ in the second variation of the trace per mode as the unperturbed trace times

$$
s\left[-\tfrac94+3(sk^2)-\tfrac13(sk^2)^2\right].
$$

The zero-frequency part is projected out by this derivative. The integrated curvature has second variation $6\nu^2$ per reference four-volume, since $\int\sqrt g R=6\int e^{3z}(z')^2$ after periodic integration by parts. This path measures the temporal curvature projection. Varying a constant $X$ at flat metric separately multiplies the heat trace by $-s$. The two independent source derivatives determine the benchmark action coefficients $c_R$ and $c_X$. The spatial regulator can break Euclidean rotation symmetry at finite spacing, so the temporal projection alone cannot identify every geometric operator.

At each fixed lower proper time $\sigma$, compute the action in the band $[\sigma,2\sigma]$. Refine the spatial grid before decreasing $\sigma$. On the $97^3$ lattice the results per scalar are:

| $\sigma$ | $\sigma c_R$ | $\sigma c_X$ |
|---:|---:|---:|
| 0.02000 | -0.000236218 | 0.001417306 |
| 0.00500 | -0.000256646 | 0.001539876 |
| 0.00125 | -0.000262035 | 0.001572209 |

The dimensionless coefficients approach $-1/(384\pi^2)$ and $1/(64\pi^2)$ in the small-$\sigma$ limit. They follow from the continuum heat trace insertion $R/6-X$ and $\int_\sigma^{2\sigma}s^{-2}ds=1/(2\sigma)$. At $\sigma=0.00125$ the $25^3$ result for $\sigma c_R$ is $-0.000223735$, which quantifies the error from moving the cutoff too close to the spatial resolution. [Continuum heat kernel reference](https://arxiv.org/abs/hep-th/0306138).

In the control calculation only, apply the independently determined $c_R$ to the continuum Gaussian cone area term in the same proper-time band. The latter gives $A\int_\sigma^{2\sigma}(ds/s^2)e^{-s m^2}/(48\pi)$, using the flat normal cone and two tangential dimensions. Adding $4\pi c_R A$ subtracts this term in the spatial continuum and large-box limits at fixed band. At fixed geometric volume the area change is $-(4\pi/30)r^4\delta{}^{(3)}R+O(r^6)$ for a geodesic ball in three spatial dimensions. The local remainder for a unit curvature variation at $\sigma=0.00125$ falls from $-0.16128$ to $+0.00016029$ and then below $10^{-12}$ in units of $r^4$ across the three grids. This comparison uses the continuum local cone expression at every spacing. It tests the sign and normalization of the local subtraction. The generalized volume at Einstein order with constant curvature coefficient is proportional to geometric volume.

🟠 [Next] Derive independent time-dependent curvature and clock vertices for the actual constrained light Hessian, including its second-order background dependence, and for the projected heavy tensor. Match the spatial and temporal curvature projections and the remaining clock invariants at fixed cutoff before taking the small-proper-time limit. The control coefficients cannot be applied to the coupled canonical ball entropy. The subtraction of its divergences and the finite $r^4$ coefficient at fixed full generalized volume remain open.

### Projected tensor ultraviolet matching and the reduced clock source rank

🟢 [Done] Matched the isolated connection term of the rank-five projected tensor on the spectral spatial regulator. Tested which curvature and clock perturbations can be varied independently after applying the implemented ADM constraints. Reproduce both calculations with [projected_uv_matching.py](experiments/projected_uv_matching.py).

For the heavy bundle, insert an independent infinitesimal connection $A_x=\epsilon J\cos(\nu y)$ at fixed base metric, with $y=t$ or $z$. This probes the spin-two representation of the projected connection before pulling it back to the clock and metric. The skew generator $J$ obtained from the tensor basis obeys $\mathrm{tr}(J^2)=-10$ for unit rotation. The perturbations of $-(\partial_x+A_x)^2$ are $-2ik_xJ\cos(\nu y)$ and $-2J^2\cos^2(\nu y)$ at first and second order. In the time probe, the two-insertion term contains the factor $\int_0^1 e^{-su(1-u)\nu^2}du$. In the spatial probe it is evaluated on the same spectral lattice, by shifting the $k_z$ mode by one box momentum and integrating the interpolated heat factors over $u$. In both cases the second insertion cancels from the difference with the zero-momentum heat response. With both index orders included, the integrated $\mathrm{tr}(\Omega_{\mu\nu}\Omega_{\mu\nu})$ has amplitude second derivative $2\nu^2\mathrm{tr}(J^2)$ per reference volume. The temporal coefficient is therefore

$$
c_{\Omega,t}(\sigma)
=-\frac{1}{12}\int_\sigma^{2\sigma}ds\,s^2\,
\frac{e^{-sm^2}}{\sqrt{4\pi s}\,L^3}\sum_k k_x^2 e^{-s|k|^2}.
$$

This is a Euclidean effective-action coefficient multiplying the trace over the bundle, with no extra rank factor. The temporal column uses the frequency slope and the spatial column uses a finite difference at $2\pi/L$. At $L=1.8$, $m=2$, and $N=97$ points per axis:

| Lower proper time $\sigma$ | Temporal connection coefficient | Spatial connection coefficient |
|---:|---:|---:|
| 0.02000 | -0.000162999 | -0.000157440 |
| 0.00500 | -0.000177693 | -0.000176143 |
| 0.00125 | -0.000181578 | -0.000181179 |

At the smallest cutoff the spatial and temporal results differ by about 0.22%. The temporal result agrees within 1% with the logarithmic shell coefficient $-\log(2)/(384\pi^2)$ from the continuum heat coefficient $\mathrm{tr}(\Omega^2)/12$. At the same cutoff the temporal value on $N=25$ is $-0.000161773$, showing the need to refine the lattice first. The probe fixes the connection coefficient independently of the regional entropy. Its first variation about the trivial connection has zero component trace on any component-blind cut, consistent with the existing canonical sewing check. Its local counterterm is quadratic in $\Omega$ about $\Omega=0$. Both derivatives therefore vanish separately for this insertion in the linear moving-ball test, including at order $r^4$. The result is specific to the connection and the reference with vanishing bundle curvature. [Heat-kernel coefficient conventions](https://arxiv.org/abs/hep-th/0306138).

For the clock, let $\alpha=\dot\zeta/H$ and $\psi=-\zeta/H+3a_{\mathrm{FLRW}}^2\Delta^{-1}\dot\zeta$ be the implemented lapse and shift. On the mean-zero modes at a fixed reading,

$$
\delta{}^{(3)}R=-4a_{\mathrm{FLRW}}^{-2}\Delta\zeta,\qquad
\delta K=-a_{\mathrm{FLRW}}^{-2}\Delta\psi,\qquad
\delta{}^{(3)}R+4H\delta K+12H^2\alpha=0.
$$

Here $K$ uses the convention $K=3H$ on the reference. In uniform-clock gauge the perturbation of $-g^{\mu\nu}\partial_\mu T\partial_\nu T$ is proportional to $\alpha$. The pointwise identity holds for arbitrary allowed linear initial data, including time-dependent profiles, because it follows from the constraint solution. The three displayed linear sources have rank two, and their six quadratic products have rank three on the tested grids $N=3,5,7$. Thus a fit to the quadratic products alone determines only three combinations. This rank statement concerns the products of first variations. A complete smooth action match would also have to include the nonlinear background completions of the invariants and their tadpoles.

🟠 [Next] Specify a pre-reduction smooth action match with independent lapse, metric and clock sources, or fix a basis modulo the constraints and derive the entropy and generalized volume in that same basis. Supply the corresponding time-dependent smooth operators and match the remaining background vertices, including the base metric part of the tensor and the full reduced clock measure. Apply those coefficients to the physical lattice cut and take the continuum limit at fixed generalized volume before taking the small-ball limit. The isolated connection result supplies no subtraction for the remaining clock and metric response, and the coupled $r^4$ cancellation remains open.

### Independent lapse and metric sources for the heavy Einstein term

🟢 [Done] Measured the off-shell lapse–metric cross response of the base-metric part of the projected tensor. Compared the resulting Einstein coefficient with the independently computed time-dependent metric response. Reproduce the comparison with [off_shell_tensor_curvature.py](experiments/off_shell_tensor_curvature.py).

Take the static Euclidean metric $ds^2=e^{2n}dt^2+e^{2z}d\mathbf{x}^2$ and the independent source profiles $n=\epsilon_n\cos(qx_3)$ and $z=\epsilon_z\cos(qx_3)$. Before solving any constraint the massive bundle has, in its base-metric block, the quadratic operator formed from the time weight $e^{3z-n}$ and the spatial gradient weight $e^{n+z}$, with configuration weight $e^{n+3z}$. Conjugate the quadratic matrix by multiplication by $e^{-(n+3z)/2}$ on both sides to use the flat spatial and temporal measure. Use the same periodic spectral derivative as in the preceding calculations. The connection has zero internal trace and starts at second order in the effective action with two background derivatives on each connection curvature term. The independent connection form factor is tracked in the preceding section.

For spatial momenta $k,k'$ related by a shift of one box mode, the first lapse and metric vertices, with the Fourier components of the cosine factored out, are

$$
V_n=-2\omega^2-\tfrac12|k'-k|^2,\qquad
V_z=k\cdot k'-\tfrac32(|k|^2+|k'|^2).
$$

The mixed insertion on the diagonal is $\frac54|k|^2+\frac34\langle |k'|^2\rangle-2\langle k\cdot k'\rangle$, where the average uses the two shifted modes. The heat trace uses both insertions and the continuous time Gaussian. Subtract the zero-momentum cross response with the same cosine mean square to remove the derivative-free volume term. On the periodic background, $\int\sqrt g R=\int e^n\sqrt h\,{}^{(3)}R$ up to a total derivative. Its mixed variation per reference four-volume is $2q^2$. Dividing the smooth response by this value estimates the Einstein coefficient at a finite spatial momentum. This estimate includes higher-derivative corrections at finite $\sigma q^2$.

| Lower proper time $\sigma$ | $\sigma c_R$, lapse–metric cross response | $\sigma c_R$, temporal metric response |
|---:|---:|---:|
| 0.02000 | -0.000257956 | -0.000236218 |
| 0.00500 | -0.000262994 | -0.000256646 |
| 0.00125 | -0.000263685 | -0.000262035 |

Values are per component on $N=97$ points per axis in the existing $L=1.8$ box. Multiply by five for the base-metric trace of the projected tensor. At the smallest cutoff the two estimates differ by 0.63%; $a\to0$ at fixed $\sigma$ precedes $\sigma\to0$. Together with the previous time-dependent calculation this matches the leading heavy Einstein term in two independent projections.

In this Einstein truncation the induced Euclidean term is $5c_R\int\sqrt g R$. The cone contributes $-20\pi c_R A$ to the entropy because the integrated curvature adds $4\pi(1-n_{\rm replica})A$. The opposite bulk counterterm thus gives $+20\pi c_R A$. The Einstein curvature derivative is a constant multiple of the metric antisymmetrizer, so the normalized generalized volume at this order is the ordinary volume. Thus the heavy Einstein subtraction cancels the local coefficient of $\delta A|_V=-(4\pi/30)r^4\delta{}^{(3)}R+O(r^6)$ in the continuum. This tests a specific local divergence using the continuum cone, with the coefficient matched from the smooth lattice. [Generalized volume and its reference-background assumptions](https://arxiv.org/abs/1612.04374).

An independent clock deformation $T=t+\chi$ at fixed flat metric tilts the projected spatial planes. For the specified Levi-Civita projected bundle the connection curvature takes the form $PRP+P(\nabla P\wedge\nabla P)P$ on the vector bundle, then acts in the spin-two representation. With $R=0$ and constant reference $P$, the first clock variation of that curvature is zero. The previously matched $\mathrm{tr}(\Omega^2)$ operator therefore has no quadratic pure-clock response along this path. This is a property of the isolated heavy connection on this reference. The kinetic operator and determinants of the dynamical light clock and gravity on a background with independent sources remain to be supplied.

🟠 [Next] Construct the gauge-fixed smooth clock and gravity Hessian before reduction, with the lapse and shift blocks and the corresponding gauge and measure factors on the same lattice. Match clock and higher-curvature couplings with independent source variations. Derive their boundary entropy and generalized volume with the same action and sewing, then subtract the remaining divergences from the canonical lattice ball calculation. The heavy Einstein result does not determine the finite coupled $r^4$ coefficient.

### Canonical gauge fixing before the homogeneous constraint reduction

🟢 [Done] Fixed the linear ADM gauge on the clock FLRW reference, derived the canonical determinant cancellation for nonzero modes, and checked the unreduced scalar lapse–shift Hessian against the physical kinetic block on three grids. Reproduce the check with [canonical_clock_gauge_measure.py](experiments/canonical_clock_gauge_measure.py).

Start from the Einstein action with a canonically normalized massless clock. Use the ADM phase-space Liouville measure with lapse and shift integrated as multipliers of the Hamiltonian and momentum constraints $\mathcal C_\mu$. At linear order on the homogeneous solution impose $\chi=\delta T=0$ and $G_i=\partial^j\gamma_{ij}=0$, where $\gamma_{ij}$ is the trace-free spatial metric fluctuation divided by the square of the background scale factor. The linear gauge map is block diagonal,

$$
\delta\chi=\dot{\bar T}\,\xi^0,\qquad
\delta G_i=\Delta \xi_i+\tfrac13\partial_i\partial_j\xi_j .
$$

The time diffeomorphism changes only the trace of the homogeneous spatial metric. Use the same odd periodic spatial spectral lattice as the reduced computation, and project out the spatial zero mode as in that computation. The ghost action is $\bar c_\mu M^\mu{}_\nu c^\nu$ with $M=\{G^\mu,\mathcal C_\nu\}$ in an equivalent orientation convention. In this basis it is instantaneous in time. The absolute determinant on each nonzero real Fourier mode is $|\dot{\bar T}|\, (4/3)|k|^6$, from the temporal eigenvalue and the two transverse and one longitudinal spatial eigenvalues. This determinant and the delta-function Jacobian for removing the gauge orbit coordinate cancel mode by mode.

The equivalent phase-space argument uses linear canonical coordinates with the gauge conditions as gauge coordinates. At vanishing gauge coordinates the linearized constraints are affine in the conjugate gauge momenta with coefficient $M$. Integrating the lapse and shift first gives $\delta(\mathcal C_\mu)$. Integrating the gauge momenta then gives $1/|\det M|$, cancelling the ghost determinant in these coordinates and leaving the physical Liouville measure. Gaussian integration over the physical momenta produces the configuration weight $\sqrt{\det M_{\rm kin}}$, where $M_{\rm kin}$ is the physical kinetic matrix. This argument uses the normalized canonical multiplier prescription. A flat configuration-space integral over lapse and shift after integrating the unreduced momenta has a different apparent measure. Its auxiliary Gaussian determinant alone is neither the canonical measure nor the inverse ghost determinant.

The numerical check starts from the unreduced projected ADM scalar action, includes the transverse shift, and verifies that the Schur complement of all four auxiliary blocks has $M_{\rm kin}=12a_{\rm lattice}^3 I$ at $a_{\rm FLRW}=1$ in the action units used in the quartic calculation. This holds to the stated tolerance for $26$, $124$, and $342$ nonzero real spatial modes. On the $5^3$ grid, for example, the log absolute ghost factor is $+1584.368748$, while the separate log absolute auxiliary Gaussian weight in cell units is $-794.570166$. The latter uses the absolute determinant and is only diagnostic for the indefinite Lorentzian auxiliary block. For the homogeneous reference the two transverse traceless graviton polarizations decouple from these constraints at quadratic order. Their canonical measure follows by integrating their physical momenta in the same way. [Uniform-clock scalar and tensor quadratic actions](https://arxiv.org/abs/astro-ph/0210603).

The independent curved backgrounds required for coupling matching are off shell. The derivative of the gauge identity $S_{,i}R^i{}_\alpha=0$ gives

$$
S_{,ij} R^j{}_\alpha=-S_{,j}\partial_iR^j{}_\alpha
$$

in the continuum, where $R^i{}_\alpha$ is a gauge generator. Thus the Hessian on a generic independently sourced background has source-dependent entries along the reference gauge directions. The homogeneous determinant identities alone cannot justify dropping these entries or fitting the curved counterterms from only the reduced physical kinetic matrix. On the spectral lattice the homogeneous linear calculation is exact for the specified mode projection. A nonlinear realization of the gauge identity requires additional checks, since products of fields need not satisfy the continuum Leibniz rule on the finite grid.

🟠 [Next] Specify an off-shell source and gauge prescription and verify its lattice Ward identity, including the source-dependent terms. Construct the time-dependent background Hessian together with the accompanying lapse, shift, and ghost contributions, including a prescription for the homogeneous mode. Determine the remaining smooth curvature and clock counterterms before any ball fit. The homogeneous gauge check supplies no new curvature subtraction or generalized-volume correction. The continuum coefficient of the fully subtracted fixed-generalized-volume ball remains undetermined.

### Off-shell Ward identity with independent lapse, shift, metric and clock profiles

🟢 [Done] Tested the classical off-shell Ward identity and the gauge-fixing insertion on a time-dependent Einstein–clock sector with a common spectral derivative in space and time. The test exposed a substantial defect at momenta close to the lattice cutoff. Reproduce it with [off_shell_clock_ward.py](experiments/off_shell_clock_ward.py).

Use a periodic two-coordinate sector of the four-dimensional theory, $ds^2=g_{ab}(t,x)dx^a dx^b+e^{2w(t,x)}(dy^2+dz^2)$, with $T=t+\chi(t,x)$ and periodic $dT$. Parameterize the Lorentzian base by independent lapse, spatial metric and shift, and impose no background equation. In this sector the Einstein density after integration by parts is $\sqrt{-g_2}e^{2w}(R_2+2|\nabla w|^2)$, and the clock density is $-\sqrt{-g_2}e^{2w}|\nabla T|^2/2$. Take the fluctuation Hessian on symmetric metric variations, retaining the metric entries occupied by the lapse and shift. The fields and their Lie derivatives use collocation products and the preceding periodic spectral spatial symbol. This is a symmetry-restricted Lorentzian Hessian test per transverse area and reference base volume, with spectral time discretization for the Ward test.

For a prescribed diffeomorphism vector let $R$ denote the corresponding field variation and $J=S_{,\phi}$ the off-shell tadpole. Automatic differentiation independently forms $H R$ and $(\partial R)^{\mathsf T}J$. Their sum is the differentiated classical Ward defect. A fixed external source in the tangent expansion may cancel the linear term, but then its gauge variation must still be tracked. To test the gauge-fixed Hessian in the two retained directions, use $Fh=(\delta T,\partial_x\delta g_{xx})$. The ghost operator is $M=FR$ and the quadratic gauge term is $\|Fh\|^2/2$ in the coordinate norm of this test. The code checks $(H+F^{\mathsf T}F)R-HR=F^{\mathsf T}M$ by differentiating the gauge-fixed action and independently applying the ghost operator. This test does not invert the ghost operator or assign a determinant to residual gauge directions.

For a fixed smooth low-frequency background and gauge vector the full relative norm $\|HR+(\partial R)^{\mathsf T}J\|/(\|HR\|+\|(\partial R)^{\mathsf T}J\|)$ is:

| Points per retained coordinate | Einstein term | Clock term |
|---:|---:|---:|
| 9 | 0.319 | 0.113 |
| 17 | $3.95\times10^{-3}$ | $2.08\times10^{-4}$ |
| 33 | $7.55\times10^{-9}$ | $6.74\times10^{-11}$ |
| 65 | $1.27\times10^{-12}$ | $2.75\times10^{-13}$ |

For fixed low output momenta the residual is already at roundoff on the $33$-point grid. Omitting the source term leaves a relative residual of about $0.5$ with the same normalization. On the $65$-point grid, increasing the spatial harmonic from 1 to 15 also moves a clock harmonic to 30, near the spectral edge. The full residual increases to $0.291$ and $0.829$ respectively. The continuum Ward identity for these smooth functions and the discrete gauge-fixing algebra are distinct from a Ward identity uniform across the loop momenta of the collocation regulator.

🟠 [Next] Extend the source and gauge prescription to all four dimensions with the complete metric and ghost sectors and a treatment of residual gauge modes. For smooth-action matching either control the regulator terms in the Ward identity or verify convergence of the gauge and ghost traces with the proper-time band held fixed during spatial refinement. Only then decrease the proper-time cutoff and determine the remaining local coefficients. An off-shell gauge-fixed determinant also requires a specified source or field parametrization convention before comparing local coefficients. This restricted check yields no new divergence subtraction or generalized-volume correction, and the fully subtracted $r^4$ coefficient remains open. [Background field and gauge-fixing dependence](https://arxiv.org/abs/1805.02149).

### Four-dimensional de Donder operators and flat heat-trace calibration

🟢 [Done] Specified the continuum background Hessian in all four dimensions and verified the complete component count, zero-mode prescription, Ward algebra, and leading volume divergence on a flat four-torus. Reproduce the lattice calibration with [four_dimensional_gauge_heat.py](experiments/four_dimensional_gauge_heat.py).

For the Euclidean Einstein–clock action $S=\int\sqrt g\,(-A R + X/2)$, with $X=T_\mu T^\mu$ and $T_\mu=\partial_\mu T$, use a linear background split $(h_{\mu\nu},\chi)=(\delta g_{\mu\nu},\delta T)$. A differential construction of the bare Hessian is to vary the two density gradients at fixed coordinate volume,

$$
\sqrt g \left[A G^{\mu\nu}+\tfrac14g^{\mu\nu}X-\tfrac12 T^\mu T^\nu\right],
\qquad -\sqrt g\,\nabla^2 T .
$$

In this variation use $\delta\sqrt g=\sqrt g\,h/2$, $\delta T^\mu=\nabla^\mu\chi-h^{\mu\nu}T_\nu$ and $\delta R_{\mu\nu}=\nabla_\rho\delta\Gamma^\rho_{\mu\nu}-\nabla_\nu\delta\Gamma^\rho_{\mu\rho}$, where $\delta\Gamma^\rho_{\mu\nu}=(\nabla_\mu h_\nu{}^\rho+\nabla_\nu h_\mu{}^\rho-\nabla^\rho h_{\mu\nu})/2$. Mixed derivatives and terms multiplying off-shell density gradients are retained by varying the whole density. The de Donder map is $F_\mu=\nabla^\nu h_{\mu\nu}-\nabla_\mu h/2$ and the ghost in the positive principal-symbol convention is $-\nabla^2\delta_\mu{}^\nu-R_\mu{}^\nu$. This gauge acts on the full metric, including its lapse and shift components. These differential expressions specify a continuum starting point. The implemented determinant test below uses only the flat specialization, where the contour and treatment of zero modes are explicit. [Covariant metric–scalar quantization](https://www.numdam.org/item/?id=AIHPA_1974__20_1_69_0).

On a flat Euclidean torus with constant reference $T$, the clock fluctuation is a real free massless scalar and is decoupled from the graviton. In normalized metric units, omitting the Fourier factors of $i$ in $F$ and the linear orbit $R_{\rm gauge}$, the bare and fixed metric symbols obey

$$
H_{\rm bare}=k^2P-2F^\dagger F,\qquad
H_{\rm fixed}=k^2P,\qquad
F R_{\rm gauge}=k^2 I_4,\qquad H_{\rm bare}R_{\rm gauge}=0 ,
$$

where $P$ is the trace-reversal involution. The check constructs all ten symmetric metric components and tests the identities on 625 Fourier momenta, including the zero mode. The constant vector ghosts represent the residual translations and are removed with their gauge-group volume. Constant metric modes are fixed torus moduli, and the constant scalar is fixed by shift symmetry. These last two omissions are separate infrared prescriptions. The metric trace has one negative direction in the fixed Euclidean Hessian. Rotate that direction to define the magnitude of the Gaussian determinant. The calculation tracks its absolute heat action, with no assignment of a background-dependent contour phase. A constant reference clock does not define a relational time slice.

Discretize all four directions with the odd periodic spectral derivative, including time for this calibration. The primed heat trace per four-volume entering $-\tfrac12\int ds/s$ is

$$
\frac{10+1-2(4)}{L^4}\sum_{k\ne0}e^{-s k^2}.
$$

The factor of two is the complex Grassmann ghost weight relative to a real boson. For $L=1.8$ and band $[\sigma,2\sigma]$, the $65^4$ and $129^4$ traces agree at the tested quadrature nodes to relative tolerance $2\times10^{-6}$ for each of the three bands. At $\sigma=0.00125$ the scaled actions $\sigma^2\Gamma_{\rm band}/L^4$ for $N=17,33,65,129$ are $-0.002437064$, $-0.003541289$, $-0.00356191808$, and $-0.00356191811$. In the small-$\sigma$ limit the independently calibrated bulk coefficient satisfies

$$
\lim_{\sigma\to0}\sigma^2 \frac{\Gamma_{\rm band}}{L^4}
=-\frac{9}{256\pi^2}.
$$

This follows from the continuum heat density $3/(4\pi s)^2$. Removing the constant modes shifts the unscaled action density by $3\log 2/(2L^4)$ and leaves the ultraviolet coefficient invariant. The volume divergence has no direct conical entropy in the regular replica limit because its extensive part is proportional to the replica number. It must still be absorbed in the cosmological coupling when imposing the background field equations. It supplies no direct $r^4$ entropy subtraction.

🟠 [Next] Implement the full coupled Hessian on independent curved, varying-clock sources and define the Euclidean contour and zero-mode treatment there. Extend the fixed-band Ward and trace convergence tests to those sources. The flat run cannot probe curvature or clock-gradient counterterms, and it does not define the moving clock ball. The remaining divergence subtraction, corrected generalized volume, and finite $r^4$ coefficient of the coupled model remain open.

### Independent clock-gradient insertion in the full flat metric Hessian

🟢 [Done] Matched the quadratic clock-gradient divergence of the Euclidean clock–gravity determinant on the flat spectral four-torus. The full metric–clock mixing and all ten metric components are retained. Reproduce the Ward and heat-trace checks with [clock_gradient_heat.py](experiments/clock_gradient_heat.py).

Use $S=\int\sqrt g\,(-A R+X/2)$ in the dimensionless action units $A=1$, with $X=g^{\mu\nu}\partial_\mu T\partial_\nu T$. Set the reference clock one-form to $v\,dt$ at fixed flat metric. This is a prescribed winding background with periodic fluctuations. It isolates the $X$ insertion at $R=0$ and is off shell for the metric. Its metric tadpole is $J^{ab}=v^2(\delta^{ab}/4-t^at^b/2)$, with $t$ the unit time covector. The de Donder gauge fixing depends only on the metric fluctuation. Its flat vector ghost determinant is independent of $v$ and cancels in the derivative with respect to $X$. Use the same constant-mode projection and perturbative conformal contour as in the flat calibration.

For an orthonormal basis of symmetric matrices $h_a$, define $\tau_a=\mathrm{tr}(h_a)$, $\ell_a=t^{\mathsf T}h_a t$, and $u_a=h_at$. The contribution of the clock action to the metric block at order $v^2$ is

$$
B_{ab}=\tfrac18\tau_a\tau_b-\tfrac14\delta_{ab}
-\tfrac14(\tau_a\ell_b+\tau_b\ell_a)+u_a\cdot u_b.
$$

The metric–clock block at momentum $k$ is $iv b_a(k)$ with $b_a(k)=k\cdot(\tau_a t/2-u_a)$. The scalar block is $k^2$. The code tests the off-shell Ward identity on three nonzero four-momenta and all four gauge directions. With orbit $(i(k_\mu\xi_\nu+k_\nu\xi_\mu),\,v\,t\cdot\xi)$, the bare Hessian acting on the orbit cancels the contraction of $J$ with the Lie derivative of the metric fluctuation. The scalar image vanishes separately. The pure gravitational and gauge-fixing parts obey the flat identities tested in the preceding section. This calculation uses a constant one-form, so the spectral derivatives in the Hessian and the tested Ward identity act mode by mode.

Upon normalizing the metric Gaussian to the flat principal symbol, the congruence matrix obeys $CC^{\mathsf T}=2P$, where $P$ is trace reversal. The single-insertion weight is $\mathrm{tr}(2PB)=0$. The two-insertion weight summed over the four momentum directions is $8$. Cubic symmetry makes their contributions equal after the momentum sum. Expand the heat trace to order $v^2$ around the common flat symbol. The surviving weight is $s^2 k^2 e^{-sk^2}$ after the lattice momentum sum, and the one-loop action uses $-\tfrac12\int ds/s$ as before. In particular, keeping the diagonal metric vertex alone would miss the divergence.

At fixed band $[\sigma,2\sigma]$ and box $L=1.8$, the $65^4$ and $129^4$ differentiated traces agree within relative tolerance $2\times10^{-6}$ at all tested quadrature nodes. At $\sigma=0.00125$, the scaled action coefficient $\sigma c_X$ on $N=17,33,65,129$ is $-0.001493325$, $-0.003109179$, $-0.003166287$, and $-0.003166287$. Integrating the continuum moment $\int d^4k\, k^2e^{-sk^2}/(2\pi)^4=2(4\pi s)^{-2}/s$ gives

$$
\lim_{\sigma\to0}\sigma c_X=-\frac{1}{32\pi^2}.
$$

This is a power-divergent coefficient in the chosen proper-time regulator, field split and off-shell gauge, per unit four-volume and in $A=1$ units. The clock-dependent part has no constant-mode contribution at this order. The matching was done from the smooth determinant without a ball fit. [Context for the covariant metric–scalar Hessian](https://www.numdam.org/item/?id=AIHPA_1974__20_1_69_0).

The counterterm $-c_X\int\sqrt g\,X$ renormalizes the clock kinetic coupling. For smooth clock sewing it has no explicit curvature derivative and no direct conical entropy term. In the Einstein truncation it does not change the curvature-derived generalized volume. It does change the clock stress tensor used in the constraint and can affect the entropy balance through the state and background solution. A zero direct surface term therefore leaves the finite coupled $r^4$ test open.

🟠 [Next] Implement the curvature-only and simultaneous curvature–clock backgrounds for the dynamical graviton, clock and ghost determinant, and verify fixed-band Ward and trace convergence there. Match the curvature and mixed counterterms, derive their geometric and state contributions from the same action, and take the continuum limit of the subtracted canonical ball at fixed generalized volume before extracting $r^4$.

### Four-dimensional curved Einstein–clock Ward test

🟢 [Done] Implemented matrix-free applications of the metric–clock Hessian and the de Donder ghost on time-dependent curved four-dimensional backgrounds, with and without an independent clock gradient. Reproduce the grid sequence with [curved_clock_ward_4d.py](experiments/curved_clock_ward_4d.py).

Use an odd periodic spectral grid in all four coordinates. Form the Euclidean action $-R+X/2$ with $X=g^{\mu\nu}T_\mu T_\nu$ using the periodic first-derivative Einstein density. The metric is unconstrained in the fluctuation Hessian, with the ten symmetric variations represented by a symmetrized array. The background is $g=e^{2w}\delta$ with $w=0.08\cos(2\pi(t+x)/L)+0.025\cos(2\pi(y-z)/L)$. The clock is $T=v[t+0.015\sin(2\pi(t-x+y)/L)]$ with winding in $t$. The values $v=0$ and $v=0.35$ give the curvature-only and combined paths at identical metric. The winding derivative is supplied analytically and the fluctuation $\delta T$ is periodic.

Differentiate the same action density for the Hessian and the off-shell tadpole. Apply the discrete vector variation $R_\xi=(\mathcal L_\xi g,\xi\cdot dT)$ and independently form the differentiated tadpole term $(\partial R_\xi)^{\mathsf T} S_{,\phi}$. Construct $F_\mu=\nabla^\nu h_{\nu\mu}-\nabla_\mu h/2$ at fixed background and the positive-symbol ghost application $M=-F R$. With adjoint taken using the background vector norm, automatic differentiation verifies $(H_{\rm fixed}-H)R=-F^\dagger M$ to relative tolerance $10^{-10}$. The full classical Ward residual $\|HR+(\partial R)^{\mathsf T}S_{,\phi}\|/(\|HR\|+\|(\partial R)^{\mathsf T}S_{,\phi}\|)$ for the tested smooth vector is:

| Points per axis | Curvature only | Curvature with clock gradient |
|---:|---:|---:|
| 5 | 0.142332 | 0.142238 |
| 7 | 0.0113223 | 0.0113141 |
| 9 | 0.000508360 | 0.000507991 |
| 11 | 0.0000153655 | 0.0000153543 |

These are Hessian and ghost applications before contour rotation or projection of residual gauge modes on the curved background. Their convergence is for the selected smooth gauge vector. The fixed-band heat-trace convergence has yet to be checked.

For a future independent fit of the two curvature–clock invariants $RX$ and $R_{\mu\nu}T^\mu T^\nu$, take $T=vt$ and use separate conformal waves $w=\epsilon\cos(qt)$ and $w=\epsilon\cos(qx)$. After periodic integration by parts, their integrated densities reduce to $-6v^2\int|\partial w|^2$ and $2v^2\int[(\partial_t w)^2-|\partial w|^2]$. The first responds equally to the two probes, while the second responds only to the spatial probe. These two columns are linearly independent at order $v^2\epsilon^2$. The clock Hessian invariant $(\nabla^2 T)^2$ also has to be included or eliminated in a specified basis. Its integrated leading response is $4v^2\int(\partial_t w)^2$, making these two probes insufficient for all three invariants. Independent clock waves at fixed flat metric provide a third direction, with zero curvature entries and nonzero $(\nabla^2 T)^2$. Likewise, separate pure metric profiles beyond conformal waves are required to distinguish curvature-squared terms that coincide or are related by total derivatives on the conformal family.

🟠 [Next] Specify the conformal contour, kinetic normalization and residual-mode prescription for this curved Hessian, then check the weighted metric–clock and ghost heat traces on the same bands through spatial and temporal refinement. Use the independent probes to isolate the curvature and mixed coefficients, and derive the boundary and generalized-volume terms from the resulting action prior to the canonical sphere test. The smooth Ward convergence does not determine those coefficients or the subtracted finite $r^4$ response. [Reference for the generalized-volume identity and its assumptions](https://arxiv.org/abs/1612.04374).

### Curved heat trace with conformal rotation and projected low modes

🟢 [Done] Defined and checked a perturbative curved-space Gaussian contour and a low-mode prescription. Evaluated the metric–clock and ghost heat traces at fixed positive proper time on a static conformal family with and without a clock gradient. Reproduce the calculations with [curved_clock_heat_blocks.py](experiments/curved_clock_heat_blocks.py).

Use $g=e^{2w(x)}\delta$, $w=0.015\cos(2\pi x/L)$, $T=vt$, $v=0$ or $0.1$, and $L=1.8$. The action, gauge term, and ghost application come from the four-dimensional lattice Hessian in the previous section. The background is constant along the other three coordinates. Resolve every retained transverse momentum by a real sine–cosine pair and diagonalize the small remaining $x$-dependent blocks. One auxiliary phase grid with three points suffices for evaluating the quadratic form on this pair: the background is phase independent and all terms in the quadratic form have at most two phase factors. Reflections and interchange of the two transverse spatial momenta reduce the number of distinct blocks without dropping their multiplicities.

Use the background norms for symmetric metric tensors, scalars, and contravariant ghosts. For the conformal background, metric norm half-density factors cancel in covariant metric components, the scalar fluctuation is $e^{-2w}$ times its normalized component, and the ghost vector is $e^{-3w}$ times its normalized component. Multiply the metric components by $\sqrt2$ for the Einstein kinetic normalization in action units $A=1$. Then rotate the normalized unit trace direction $\delta_{\mu\nu}/2$ by $i$. The quadratic Hessian transforms by complex congruence, not by Hermitian conjugation. In the tested blocks its rotated real part is strictly positive, including with metric–clock mixing, and the heat traces are real to numerical precision. The phase of the Gaussian is fixed by continuation from the flat prescription. This check is specific to the weak backgrounds tested. [Euclidean conformal rotation](https://www.sciencedirect.com/science/article/pii/055032137890161X).

At zero transverse momentum remove the normalized profiles of the three constant coordinate vectors along Killing directions, with the companion scalar shift when the translation changes the winding clock by a constant. The code also projects out the constant coordinate vector in the $x$ direction as a continuation of the flat infrared convention. That fourth profile is fixed by prescription on this curved family and is not identified as an exact Killing zero mode. In the bosonic block fix the mean values of the normalized fields, continuing the flat moduli and scalar infrared prescription. The finite torus traces depend on this choice. The flat calibration on several blocks reproduces $11$ boson and $4$ complex ghost channels before the one-loop weighting $K_{\rm boson}-2K_{\rm ghost}$.

For the zero and first transverse momentum blocks and samples $s=0.025,0.0375,0.05$, refinement from $N_x=13$ to $17$ agrees at relative tolerance $2\times10^{-5}$ for both traces. Separately sum the full retained transverse box with mode integers between $-3$ and $3$ in each direction. Across $s=0.07,0.085,0.10$, refinement from $N_x=9$ to $13$ changes the traces by about $2\times10^{-7}$ for the curvature-only background. Including the last transverse shell changes the traces by at most about $1.6\times10^{-3}$. At $s=0.085$ the curvature-only traces are $90.361080122$ for metric plus clock and $32.879605218$ for the ghost. The analogous clock-gradient sequence is tested with the same tolerances. The two resolution checks address different grid directions. The shell change is a measured sensitivity and is not an error bound on an extrapolation.

🟠 [Next] Tighten transverse tail control as the proper-time cutoff is reduced. Use all independent background profiles from the preceding section, including temporal curvature and a clock wave at flat metric, and extrapolate the response derivatives before fitting the local coefficients. Fixed-band trace agreement for this one spatial profile leaves the ultraviolet curvature and mixed coefficients undetermined. The full generalized volume and the subtracted fixed-volume $r^4$ result remain open.

### Temporal curvature and flat clock wave

🟢 [Done] Added the temporal conformal and flat clock-wave probes under the same spectral and conformal-contour prescriptions. Run [clock_wave_uv.py](experiments/clock_wave_uv.py).

In the curved Fourier blocks move the winding direction onto the coordinate along which the metric varies. Relabeling that coordinate as Euclidean time gives the temporal curvature profile. With zero winding, this is a permutation of the spatial curvature probe. At nonzero winding the two profiles differ. Compare 9 and 13 points along the inhomogeneous direction and compare transverse mode bounds 2 and 3 at fixed samples $s=0.07,0.085,0.10$. In the temporal probe the maximum relative changes are $2.002×10^{-7}$ under longitudinal refinement and $1.593×10^{-3}$ from the last transverse shell. These measure finite-time trace resolution.

For the independent clock probe use a flat metric and a periodic clock-gradient wave of external momentum $q$. At quadratic order in the wave amplitude the diagonal metric insertion has zero rotated trace, and the ghost is independent of the clock. The norm of the metric–clock vertex in the rotated normalization is the scalar momentum squared times the gradient amplitude squared. Subtract the homogeneous clock-gradient response with the same integrated $X$. The continuum two-insertion momentum integral, divided by the unperturbed heat density, has form factor

$$
\int_0^1du\, e^{-s u(1-u)q^2}\left(\frac{2}{s}+u^2q^2\right).
$$

The $q^2$ coefficient is $\int_0^1[u^2-2u(1-u)]du=0$. Consequently the logarithmic shell coefficient of the flat integrated $(\Box T)^2$ term is zero in this field split and gauge. This statement treats integrated clock Hessian squared and integrated $(\Box T)^2$ as the same flat operator; curvature lifts that equivalence.

The numerical check sums the exact spectral weights with both internal global zero modes excluded when applicable. After dividing by the integrated $(\Box T)^2$, the finite shell estimates on the $129$-point grid are $3.60119\times10^{-5}$, $4.87756\times10^{-6}$ and $9.11458\times10^{-7}$ at lower proper times $0.02000$, $0.00500$ and $0.00125$. The $65$- and $129$-point sums agree within the specified fixed-band tolerance. At the smallest cutoff the $17$-point estimate is $-2.02415\times10^{-4}$. The nonzero finite-shell response includes higher-momentum and finite-box contributions.

🟠 [Next] Resolve the amplitude derivatives of the temporal and spatial curved traces, including transverse refinement at each lowered band and subtraction of lower-dimensional terms. Use a nonconformal metric probe for pure curvature-squared operators. The flat clock wave fixes one coefficient but leaves $RX$ and $R_{\mu\nu}T^\mu T^\nu$ unmeasured. Their boundary and generalized-volume contributions and the subtracted finite $r^4$ coefficient remain open.

### Mixed heat-response resolution and nonconformal curvature probe

🟢 [Done] Evaluated finite-amplitude mixed heat differences for temporal and spatial curvature, tested their cutoff sensitivity, and implemented a nonconformal shear probe. Reproduce with [mixed_curvature_response.py](experiments/mixed_curvature_response.py).

For metric amplitude $b$ and clock winding $v$, form $K(b,v)-K(b,0)-f_b[K(0,v)-K(0,0)]$, where $f_b=\langle e^{2b\cos(qx)}\rangle$ is the ratio of integrated $X$ at fixed winding. The ghost cancels within each clock difference. Integrate the result over $[\sigma,2\sigma]$ and divide by $b^2v^2 L^4$. Denote the resulting responses by $D_t$ and $D_x$, for curvature parallel and orthogonal to the winding. The independent geometric responses of $RX$ and $R_{\mu\nu}T^\mu T^\nu$ give the projections $-D_t/(3q^2)$ and $(D_t-D_x)/q^2$, respectively. These are finite-shell estimates, with finite amplitudes and higher derivatives still present. The flat clock-wave logarithm determined in the previous section is zero in the chosen operator basis.

At $b=0.025$, $v=0.3$, the estimates are:

| Lower proper time | Longitudinal points | Transverse integer bound | $RX$ projection | Ricci–clock projection |
|---:|---:|---:|---:|---:|
| 0.0700 | 9 | 2 | 0.00117027 | -0.00036292 |
| 0.0700 | 9 | 3 | 0.00128573 | -0.00039320 |
| 0.0700 | 13 | 3 | 0.00128511 | -0.00039337 |
| 0.0350 | 13 | 2 | -0.00108493 | -0.00030360 |
| 0.0350 | 13 | 3 | 0.00081937 | -0.00063305 |
| 0.0175 | 9 | 3 | -0.00157493 | 0.00027104 |
| 0.0175 | 13 | 3 | -0.00346501 | -0.00016067 |

Halving $b$ at the coarse transverse bound moves the Ricci–clock projection at $\sigma=0.035$ from $-0.00027877$ to $+0.00061883$. Thus even the finite-amplitude extrapolation is unresolved at that resolution. At the lower bands the lattice changes are of the same order as the projected coefficients or reverse their sign. The trace convergence tested at larger positive proper times does not carry over to these differences. No row is used as a counterterm.

For a nonconformal probe take $g=\mathrm{diag}(1,1,e^{2w},e^{-2w})$ with $w=b\cos(qx)$, where $x$ is the second coordinate. The metric, scalar and ghost normalization uses the diagonal background frame and volume density. The same constant coordinate ghost profiles are removed using their frame-weighted representations. In the zero transverse sector the $13$- and $17$-point traces agree to relative tolerance $2\times10^{-5}$ at $s=0.035,0.07,0.14$. At $s=0.07$ the traces are $10.10901861$ for metric plus clock and $3.67529200$ for the ghost. On the torus, modulo the Euler term, the conformal and shear rows for integrated $(R^2,R_{\mu\nu}R^{\mu\nu})/(b^2q^4L^4)$ are $(18,6)$ and $(0,1)$ at quadratic order. The two probes therefore separate the invariants geometrically. The summed shear heat derivative needed to fit their coefficients is still open.

For the candidate Lorentzian local action $A R+\lambda RX+\beta R_{\mu\nu}T^\mu T^\nu$, use the curvature-derivative Wald entropy and the curvature-derivative volume functional with Einstein reference normalization $E_0=A/2$. For a clock-aligned slice and a perturbative comparison about the Einstein reference, writing $c=\lambda+\beta/2$, the mixed terms add $4\pi c\int_{\partial B} X\,dA$ to the entropy and $3c/(2A)\int_B X\,dV$ to the volume functional. This follows because the Ricci coupling $\beta T^\mu T^\nu$ contributes half its normal-plane trace to the Wald area coefficient, and contributes $3\beta X/4$ to $E^{abcd}u_a h_{bc}u_d$ in four dimensions. This is the curvature-derivative part, with no replica-dependent boundary completion assigned. [Generalized-volume prescription and reference assumptions](https://arxiv.org/html/1612.04374).

Holding this volume functional fixed for a variation of $X$ on a reference flat ball gives the local entropy response $4\pi c\,4\pi r^2(\langle\delta X\rangle_{\partial B}-\langle\delta X\rangle_B)$ at first order in the mixed couplings. For a smooth $\delta X$ this is $(16\pi^2/15)c\,r^4\Delta\delta X(0)+O(r^6)$. Thus the boundary and volume terms alone cancel a constant response but can leave a derivative response of precisely the requested order. This conditional local expression has no state or constraint response included.

🟠 [Next] Evaluate amplitude insertions directly or extrapolate both amplitudes after resolving the transverse and longitudinal tails of the mixed difference at each band. Fit the pure curvature coefficients with the summed conformal and shear derivatives. Until those coefficients and the matching canonical state and constraint responses are fixed, the subtracted coupled $r^4$ cancellation remains undetermined.

### Direct lattice heat-trace derivatives

🟢 [Done] Implemented direct second curvature derivatives and direct fourth mixed curvature–clock derivatives of the regulated heat traces. Reproduce with [direct_curvature_insertion.py](experiments/direct_curvature_insertion.py) using NumPy, PyTorch and SciPy.

The differentiated operators include the background normalization, conformal rotation, and ghost projection. The zero-sector ghost basis uses an explicit differentiable Householder map onto the orthogonal complement of the removed background profile. Its projector is the same as in the finite-amplitude calculation. For the curvature derivative, differentiate the operator to obtain $D_1$ and $D_2$. For each reference eigenvalue pair, the two-insertion term uses the divided difference of the exponent:

$$
K_{bb}
=-s\,\mathrm{Tr}(e^{-sD_0}D_2)
+s^2\sum_{ij}\frac{e^{-s\lambda_j}-e^{-s\lambda_i}}{s(\lambda_i-\lambda_j)}
(D_1)_{ij}(D_1)_{ji}.
$$

The coincidence limit is $e^{-s\lambda_i}$. In particular the product is not a squared modulus after the complex contour rotation. The implementation checks both curvature probes against centered differences on the same grid and keeps the differentiation result independent of the finite-difference step.

For $K_{bbvv}$ the boson operator is exactly quadratic in winding $v$ at fixed metric. Extract the three winding coefficients of each directly differentiated curvature insertion. Represent multiplication by the resulting operator polynomial on the nine Taylor coefficients of bidegrees $(i,j)$ with $0\le i,j\le2$. The exponential of this block triangular matrix gives the Taylor coefficient of $b^2v^2$ in its last block acting on the constant term. Multiplication by $2!2!$ gives the mixed derivative. The ghost has zero winding derivative. This construction includes all insertion orders and avoids subtraction of finite-amplitude heat traces. [Matrix exponential action algorithm](https://doi.org/10.1137/100788860).

At zero transverse momentum and $s=0.07$, the direct pure curvature derivatives at $N_x=17$ are $(20.41451582,-25.47612885)$ for the conformal probe and $(-7.99977176,-5.19641869)$ for the shear, listing the boson and ghost traces before ghost weighting. The $13$- and $17$-point results meet the tested tolerance at all three sampled proper times for both probes. This is a longitudinal check in one sector.

The raw mixed derivatives are:

| Longitudinal points | Spatial curvature at $s=0.035$ | Temporal curvature at $s=0.035$ | Spatial curvature at $s=0.07$ | Temporal curvature at $s=0.07$ |
|---:|---:|---:|---:|---:|
| 9 | -0.110804 | 0.689496 | -0.473668 | 1.262641 |
| 13 | -0.183925 | 0.647863 | -0.475744 | 1.261189 |

These values are derivatives of a sector trace before the integrated $X$ subtraction, not counterterm coefficients. The smaller proper time shows significant longitudinal dependence even with exact amplitude derivatives. At $N_x=9$, the six first axial transverse momenta contribute $-0.157446$ (spatial curvature) and $+2.850612$ (temporal curvature) at $s=0.035$. At $s=0.07$ they contribute $-1.149659$ and $+1.692727$. These contributions are comparable to or larger than the zero transverse sector. This checks the sensitivity to including transverse momenta, while a sum with a controlled tail is still needed to fit the local invariants.

🟠 [Next] Factor the momentum-space insertions by their finite Fourier transfers to accelerate and control the full transverse sums of the direct responses. Require both longitudinal and transverse tolerances on each subtracted band before lowering its cutoff. The curvature and mixed divergence coefficients and the constrained, state-inclusive $r^4$ cancellation remain undetermined.

### Transverse sums of direct heat-trace insertions

🟢 [Done] Factored and summed the transverse Fourier dependence of the direct mixed and pure-curvature trace derivatives. Reproduce with [transverse_insertion_sum.py](experiments/transverse_insertion_sum.py) and [pure_transverse_insertion_sum.py](experiments/pure_transverse_insertion_sum.py).

For the flat reference inside the Taylor calculation the transverse part of the heat operator is $p_\perp^2 I$. Factor out $e^{-s p_\perp^2}$ before computing the block exponential. A curvature vertex is at most quadratic in transverse momentum. A first winding vertex is at most linear in momentum and a second winding vertex is independent of momentum. Thus the coefficient of $b^2v^2$ after factoring the Gaussian has degree at most six. With temporal curvature, rotation symmetry among the transverse coordinates makes it a polynomial of degree at most three in $p_\perp^2$. With spatial curvature it is a polynomial of total degree at most three in the squared transverse time momentum and squared transverse spatial momentum. For the pure second curvature derivative the degree is at most four in momentum. The shear probe uses all three squared transverse components. Independent off-axis evaluations check the polynomial identities. The projected zero-transverse sector replaces the unprojected zero-sector polynomial value. Longitudinal Fourier insertions in the unprojected mixed calculation shift mode indices by at most the curvature order. The implementation tests that entries outside this support are roundoff before removing them for the sparse exponential.

For the mixed derivative subtract $4s^2\sum_k k^2e^{-sk^2}$ on the same momentum grid. This is the winding derivative of the flat $X$ response times the curvature derivative of the integrated $X$ volume factor. For the conformal pure derivative subtract the leading flat heat density times the second derivative of the volume factor, using the adopted finite-box projection. The shear has constant volume. The pure traces still contain the Einstein term. These operations do not fit any local coefficient to the sphere.

At $N_x=9$, the subtracted spatial mixed response at $s=0.035$ is $1.723596$, $7.261759$, and $7.273777$ for transverse bounds 3, 5, and 12. At $s=0.07$ those values are $4.382605$, $4.413309$, and $4.413309$. The temporal projection at bound 12 gives $8.192987$ and $5.322469$ at the two respective times. The summation removes large transverse-cutoff shifts seen in the earlier finite-shell estimates. It is a check at fixed longitudinal resolution and sampling times.

At $s=0.07,0.105,0.14$ the volume-subtracted pure responses on the two grids agree to better than $0.06\%$ between $N_x=9$ and 13 with transverse bound 8. At the shorter diagnostic time $s=0.035$ the shear result changes from $433.242729$ to $359.642382$ and the conformal result from $-1018.655926$ to $-935.767237$. At $N_x=13$, increasing the transverse bound from 5 to 8 changes the shorter-time shear result by about $0.022$ and the conformal result by about $0.027$. Longitudinal resolution is therefore the limiting error for these shorter-time pure probes. These are proper-time samples and are not a fit to logarithmic coefficients.

🟠 [Next] Resolve the longitudinal short-time error and verify quadrature convergence on each full band before lowering the cutoff. Separate the Einstein term from the two curvature-squared responses with independent momentum or band scaling. Use the resulting ultraviolet coefficients, a matched physical state, and the same fixed generalized volume to test the coupled $r^4$ residual. No partial heat response has been used as a sphere counterterm. [Heat-kernel expansion and local counterterms](https://arxiv.org/abs/hep-th/0306138).

### Proper-time quadrature and momentum separation of the Einstein term

🟢 [Done] Added proper-time band integration and a distinct external-momentum check for the pure metric fit. Reproduce with [curvature_band_matching.py](experiments/curvature_band_matching.py) and [mixed_band_resolution.py](experiments/mixed_band_resolution.py).

Write $b^2L^4$ times the band response at external momentum $q$ as the quadratic-in-amplitude part of the one-loop action after the volume subtraction. For the conformal and volume-preserving shear probes, the leading local predictions for the band response per $b^2L^4$ are

$$
C(q)=3q^2 c_R+q^4(18c_{R^2}+6c_{\rm Ric^2}),\qquad
S(q)=-q^2c_R+q^4c_{\rm Ric^2}.
$$

The Einstein coefficients follow from the respective integrated spatial curvature variations. The periodic Einstein action for the conformal wave gives $6\int e^{2w}|\partial w|^2$, while the two opposite shear warps give $-2\int|\partial w|^2$. At fixed band fit the lowest two momenta for $c_R$ and the conformal quartic combination, then independently extract $c_{\rm Ric^2}$ from each shear momentum. Agreement is necessary before interpreting the quartic part as a local band coefficient. Higher-derivative form factors and finite-box effects can contribute to this comparison. [Curvature expansion and momentum-dependent form factors](https://arxiv.org/abs/1203.2034).

The pure calculation compares longitudinal grids, transverse bounds 5 and 8, and 8- and 16-node Gauss–Legendre quadratures at fixed band. For the fundamental conformal wave at $[0.035,0.070]$, the volume-subtracted action responses per $b^2L^4$ at transverse bound 8 are $10.78569359$, $10.78555307$, and $10.78555306$ at longitudinal sizes 13, 17, and 21. At size 21 the transverse bound 5 gives $10.78559328$. The two quadratures agree to the displayed precision. This passes the selected 0.1% numerical criterion for that probe, before separating the Einstein term. For the mixed check, integrating the earlier samples with Simpson quadrature gives the following subtracted trace integrals $\int ds\,K_{\mathrm{sub}}/s$, before conversion to action and invariant normalization:

| Band | Spatial, 9 points | Spatial, 13 points | Temporal, 9 points | Temporal, 13 points |
|---|---:|---:|---:|---:|
| $[0.035,0.070]$ | 3.531235 | 2.796268 | 4.216393 | 3.492674 |
| $[0.070,0.140]$ | 3.476941 | 3.473303 | 3.879759 | 3.876409 |

The short band changes by 17–21% under this longitudinal refinement. Even the longer band has a 2–3% Simpson–trapezoid discrepancy at 13 points with these three quadrature samples. The separate mixed band script uses additional samples for the longer band and higher longitudinal resolution. For the spatial mixed probe at size 13 the five-node Simpson integral on the longer band is $3.47771728$, and the difference with trapezoid quadrature on the same nodes is $-0.01634$. For the short band that difference is $-0.04182$ and extending the transverse bound from 8 to 12 changes the integral by about $1.1\times10^{-10}$. The limiting errors are longitudinal resolution and quadrature. These finite-band numbers do not determine ultraviolet coefficients.

🟠 [Next] Require the lattice and quadrature checks on the short mixed band and test the local momentum expansion independently of quadrature. Use only the independently matched action coefficients in the subsequent physical-region entropy and constraint calculation. The subtracted, state-inclusive $r^4$ ball coefficient remains open.

### Short-band refinement and a two-wave Einstein projection

🟢 [Done] Verified two further pure-metric band responses under quadrature and lattice refinement, obtained an independent shear prediction from the two-wave fit, and implemented nested mixed-band quadrature. Reproduce with [curvature_band_matching.py](experiments/curvature_band_matching.py) and [short_mixed_quadrature.py](experiments/short_mixed_quadrature.py).

For $\sigma=0.035$ the band responses per $b^2 L^4$ at transverse bound 8 are:

| Probe | $N_x=13$ | $N_x=17$ | $N_x=21$ |
|---|---:|---:|---:|
| Fundamental conformal | 10.78569359 | 10.78555307 | 10.78555306 |
| Fundamental shear | -4.31360285 | -4.31352211 | -4.31352211 |
| Second conformal harmonic | 28.74525502 | 28.74121439 | 28.74121415 |
| Second shear harmonic | -18.02980337 | -18.02549223 | -18.02549206 |

For all four rows the band agrees under 8- to 16-node Gauss–Legendre refinement and under transverse bound 5 to 8 at the chosen 0.1% diagnostic tolerance. Solving the two conformal equations from the preceding section gives the finite-band projection $c_R=0.32788769$ and $18c_{R^2}+6c_{\rm Ric^2}=-0.00808317$. Applying the fundamental shear equation gives $c_{\rm Ric^2}=-0.00214398$ and predicts the second-harmonic shear response $S(2q)=-21.07380881$. The independently computed second-harmonic shear gives $-18.02549206$, a discrepancy of $3.04831675$, around 14.5% of the prediction. The extracted Ricci-squared projection changes from $-0.00214398$ to $-0.00086073$. The local $q^2+q^4$ truncation therefore fails its independent momentum test at the current band and box even though the heat integrals converge. The matching script now accepts an independent longitudinal box length, keeping the transverse regulator and proper-time band fixed. The flat metric–clock and ghost spectra at double longitudinal length reproduce the analytically rescaled Fourier eigenvalues. This validates the new momentum control at the flat reference; the longer-box curved fit is still open. In particular $sq^2$ reaches 3.41 for the second harmonic at the top of the band, allowing appreciable higher-derivative form-factor contributions.

The spatial mixed short-band integral estimated on three Simpson nodes is $2.796268301$ at $N_x=13$ and $2.794929099$ at $N_x=17$. This apparent integrated stability is insufficient: the pointwise change reaches $0.008008$ and the $N_x=17$ trapezoid–Simpson discrepancy is $0.04115$. At 21 points the three-node integral is $2.794929048$, and the maximum change from 17 points across the three sampled subtracted traces is $3.011\times10^{-7}$. The new mixed script compares nested Simpson quadratures at 3, 5 and 9 nodes without moving either end of the band. For the spatial probe at 17 points the integrals are $2.794929099$, $2.790639481$, and $2.790300621$. The last quadrature comparison changes the integral by $0.0122\%$, and the transverse bound change from 8 to 12 at nine nodes is $2.82\times10^{-11}$. This resolves the spatial probe to the numerical diagnostic tolerance on the tested refinements. The temporal orientation still requires the same check. In the direct insertion code the winding-dependent Hessian is now constructed separately from the metric-independent-winding operator. In an orthonormal frame it is the quadratic Taylor coefficient of $\sqrt g\,g^{ab}T_aT_b/2$, keeping the $h^2 T^2$ and $h\,T\,d\chi$ terms. The separate computation reproduces the difference of the full operator jets to $6\times10^{-14}$ in the tested nonzero transverse block for both winding orientations. This reduces repeated gravitational differentiation without changing the winding or curvature insertion orders.

🟠 [Next] Complete the dense quadrature and longitudinal checks for the temporal mixed orientation and reduce external momentum at fixed band and independently controlled finite-box errors. Use the shear response to validate the local momentum projection before accepting the fitted coefficients. Keep smaller cutoffs out of the coefficient fit until these independent checks pass. The fitted finite-band projections have not been used for a generalized-volume sphere subtraction. The state- and constraint-inclusive $r^4$ response remains open.

### Longer longitudinal box and clock-aligned constraint check

🟢 [Done] Resolved the short-band temporal mixed quadrature on the 17-point grid. At fixed band $[0.035,0.070]$ and transverse bound 12 the nested 3-, 5-, and 9-node Simpson integrals are $3.491366826$, $3.486887287$, and $3.486540709$. The last change is $0.00994\%$. Changing the transverse bound from 8 to 12 at nine nodes changes the result by $2.85\times10^{-11}$. [Nested mixed quadrature](experiments/short_mixed_quadrature.py).

For the pure metric fit, double $L_x$ from $1.8$ to $3.6$ with transverse length and proper-time band fixed. The two probe momenta become $q/2$ and $q$, where $q=2\pi/1.8$. The shared momentum $q$ provides a control for the changed box and infrared mode prescription. The maximum value of $s q_{\rm probe}^2$ across the band and the two waves falls from about $3.41$ to $0.85$. Use both the independent shear prediction and the direct combination $(C+3S)/q^4$ to test the extraction. This combination removes the Einstein term algebraically at each momentum and would equal $18c_{R^2}+9c_{\rm Ric^2}$ in the local truncation. For the previous box its two measured values are $-0.01451512$ and $-0.01066537$, showing the discrepancy even before fitting $c_R$. On the long box the fundamental conformal band response is $2.83247869$, $2.82674677$, and $2.82666877$ at 21, 25, and 29 longitudinal points, respectively. At 29 points the transverse bound 5 gives $2.82672474$, compared with $2.82666877$ at bound 8. The 8- and 16-node integrations agree to the displayed precision. The long-box fundamental conformal result passes the fixed-band numerical tolerance. This alone cannot test the local curvature decomposition. [Longitudinal-box matching](experiments/curvature_band_matching.py).

The leading constraints also give a check on how the mixed local term enters the ball response. In uniform clock gauge the Lorentzian invariant is $X=-\dot{\bar T}^{\,2}/N^2$. Its linear variation is $\delta X=-2\bar X\,\alpha$, where the leading lapse constraint gives $\alpha=\dot\zeta/H$. Substitution into the preceding fixed-$W$ formula yields the mixed local $r^4$ term

$$
(\delta S_{\rm mixed})_{r^4}
=-\frac{32\pi^2}{15}
\left(\lambda+\frac{\beta}{2}\right)\frac{\bar X}{H}\,
r^4\Delta_h\dot\zeta(0)
$$

to first order in the mixed couplings. Correcting $\alpha$ in this particular term would affect it at higher order in the couplings. The term vanishes for the previous zero-velocity profile, but the leading constraint alone does not force it to vanish for other initial data. For a Fourier mode, the surface and volume averages can be checked from $\sin(qr)/(qr)$ and $3[\sin(qr)-qr\cos(qr)]/(qr)^3$. Their difference divided by $r^2$ approaches $-q^2/15$. The check concerns the explicit mixed surface and volume corrections. It leaves the correction to the constraint in the Einstein and matter sectors and the change of the quantum state to be computed.

🟠 [Next] Complete the longitudinal refinement of the temporal mixed response and the two-wave shear check at the longer box. Keep the cutoff fixed until the short-band and momentum checks pass. Then use a resolved cutoff sequence to determine the counterterms and compute the full entropy and state response at fixed generalized volume.

### Resumable longitudinal-band matching

🟢 [Done] Reduced the transverse shear reconstruction from ten to seven operator samples using exchange symmetry of the two shear axes. At second order in the shear amplitude the polynomial is symmetric in $y^2,z^2$ and can be reconstructed using their sum and product. An independent off-axis sample still checks the reconstructed polynomial. On the previous nine-point grid the optimized response agrees with the recorded reference at both tested proper times to relative tolerance $10^{-8}$.

🟢 [Done] Added an optional JSON checkpoint to the longitudinal-band driver. Each completed grid, harmonic, and probe is saved before starting the next calculation. The stored key includes box length and lower proper time. A resume test confirmed that a completed row is reused and a different harmonic is recomputed.

    python3 -B experiments/curvature_band_matching.py --length-x 3.6 --sizes 21 25 29 --checkpoint /tmp/gravity-long-box.json

At fixed band $[0.035,0.070]$ on the 21-point long box, the conformal and shear responses were $(2.83247869,-1.05409106)$ for the fundamental and $(10.86620566,-4.34241678)$ for the second harmonic. The two conformal values and fundamental shear predict $-5.38097252$ for the second shear in the local truncation, about 19.3% away when measured relative to that prediction. The four-response pilot uses a single longitudinal grid. It does not distinguish longitudinal discretization, finite-box terms and momentum dependence. Keep the proper-time band fixed while refining this check.

🟠 [Next] Use the checkpointed long-box driver to test both shear harmonics and repeat the temporal mixed longitudinal convergence check. The independent momentum and cutoff checks still precede counterterm matching and the fixed-generalized-volume subtraction.

### Temporal mixed convergence and checkpointed long-box refinement

🟢 [Done] Completed the short-band temporal mixed integral checks. At $[0.035,0.070]$ the 21-point 3-, 5-, and 9-node Simpson integrals are $3.491366778$, $3.486887262$, and $3.486540695$. The 17-point nine-node result was $3.486540709$, a change of $1.40	imes10^{-8}$. At 21 points, changing the transverse bound from 8 to 12 shifts the nine-node integral by $2.85	imes10^{-11}$. The last quadrature change is approximately $0.010\%$. These comparisons establish convergence of this band integral to the selected numerical diagnostic tolerance. [Nested mixed quadrature](experiments/short_mixed_quadrature.py).

The mixed driver now persists the full sampled response through the same checkpoint mechanism as the pure driver, so the longitudinal check can compare individual quadrature samples as well as the integral. The long-box driver accepts any increasing sequence of at least two supported grids and evaluates the shear probes first. At $L_x=3.6$ the fundamental shear band response is $-1.051188791$ at 25 points and $-1.051153422$ at 29 points. Their relative difference is $3.36\times10^{-5}$. At 29 points the transverse bounds 5 and 8 agree to about $3.08\times10^{-5}$ relative, and the change between the 8- and 16-node proper-time integrals is $2.92\times10^{-11}$ in absolute units. The second-harmonic shear moves from $-4.322094709$ to $-4.321766559$ between the same grids, a relative change of $7.59\times10^{-5}$. Both shear probes pass all three numerical checks at the fixed band.

The completed 29-point checkpoint gives conformal responses $2.826668773$ and $10.837045453$ at the two momenta. All four probes pass the longitudinal, transverse, and quadrature checks at the fixed band. The Einstein-free projections $(C+3S)/q^4$ are $-0.03521772$ and $-0.01433488$. Fitting the conformal pair and the fundamental shear predicts $-5.355236445$ for the second shear, versus the direct $-4.321766559$. The 19.3% mismatch persists after numerical refinement, so these projections cannot be used as ultraviolet coefficients.

As an infrared diagnostic, restoring the global zero sector in the heat trace and using the corresponding unprojected volume subtraction changes the Einstein-free projections to $-0.01532208$ and $-0.01415452$. The zero-sector convention therefore accounts for most of the discrepancy in this particular difference of projections. A momentum dependence of about 7.6% relative to the fundamental remains. This comparison does not change the prescription for the physical clock state or certify either projection as an ultraviolet coefficient. The checkpointed driver can repeat it with `--compare-zero-projection`.

After the fixed-band numerical checks, lower the proper-time band to $[0.028,0.056]$ for a fundamental shear pilot. At transverse bound 8 and 16 quadrature nodes the 29- and 33-point responses are $-1.308558118$ and $-1.308544829$. At 33 points the transverse bound 5 gives $-1.307783109$ and the eight-node result at bound 8 agrees within $3.0$ times $10^{-11}$. This pilot passes the same 0.1% numerical criteria. It does not separately determine the Einstein and Ricci-squared coefficients.

🟠 [Next] Complete the shorter-band probe family and distinguish finite-volume and finite-momentum contributions before fitting a divergence. The long-box driver exposes the lower proper-time cutoff as a checkpoint key. The bulk coefficients and the state-inclusive fixed-generalized-volume entropy residual have yet to be determined.

### Common volume reference for the curvature fit

🟢 [Done] Corrected the volume reference in [curvature_band_matching.py](experiments/curvature_band_matching.py). Earlier conformal checkpoint rows subtracted 24 times the primed flat heat trace. The two curvature probes should use a common flat volume subtraction when comparing the projected and unprojected quadratic traces. The missing flat unit is independent of momentum and proper time. Restoring it subtracts 24 from the conformal heat derivative and adds $6\log 2/(L_x L_\perp^3)$ to each dyadic conformal band, since the action response per amplitude squared integrates the second derivative with weight $-1/4$. The shear probe has no quadratic volume change. The conversion is applied during matching, so the raw checkpoint data remain reusable.

For $L_x=3.6$, $L_\perp=1.8$, and the resolved band $[0.035,0.070]$, the common-reference shift is $+0.198087329$. The Einstein-free momentum projections change from $(-0.03521772,-0.01433488)$ to $(-0.01387021,-0.01300066)$. In the unprojected trace with the same volume subtraction they are $(-0.01532208,-0.01415452)$. The common reference removes the constant subtraction artifact; neither comparison meets the existing momentum consistency tolerance. The individual Ricci-squared projections with the common reference are $-0.00143858$ and $-0.00114873$. A synthetic local action check independently recovers its Einstein, scalar-squared and Ricci-squared inputs through the new extraction routine.

At $[0.028,0.056]$ the temporal mixed nine-node band integrals are $3.33146513156331$ and $3.33146513153210$ at 21 and 25 points. On the 25-point grid the five-node integral is $3.33178746622918$ and the transverse bound change from 8 to 12 is $1.79\times10^{-8}$. Longitudinal, transverse, and quadrature checks pass. This is one orientation of the mixed probe. The dyadic mixed driver now accepts the lower cutoff as a parameter and keeps it in the checkpoint key.

Both harmonics of both pure probes pass the numerical checks at $[0.028,0.056]$ on the 29- and 33-point grids. With the common reference, the Einstein-free projections are $(-0.01403405,-0.01354088)$, a difference of 3.51% relative to the fundamental, down from 6.27% at $sigma=0.035$. The scaled finite-band Einstein projection $sigma c_R$ changes from $0.01192419$ to $0.01190774$. The two Ricci-squared projections remain distinct at $-0.00140942$ and $-0.00124503$. These are converged band responses and a scaling diagnostic. They do not establish independent ultraviolet coefficients.

🟠 [Next] Complete the spatial mixed probe on the shorter band and extend the resolved cutoff and momentum sequence with the common reference. Use agreement of the local curvature projections to determine which coefficients can be used for a sphere subtraction. The finite $r^4$ balance including the constraint and state responses remains open.

### Spatial mixed convergence and longer-box scaling checks

🟢 [Done] Added joint orientation matching and independent longitudinal length to [short_mixed_quadrature.py](experiments/short_mixed_quadrature.py). The integrated fourth derivative is converted to an action density with factor $-1/(8 L_\perp^3 L_x)$, including the two factorials and the determinant factor. The temporal and spatial curvature responses then give the separate $RX$ and $R_{\mu\nu}T^\mu T^\nu$ projections. A synthetic local action check recovers both inputs, and a nondefault box test checks factorized against unfactorized mixed traces. The flat-gradient subtraction uses the distinct longitudinal and transverse momenta. The driver reports projections only after both orientation checks pass.

At $[0.028,0.056]$ the spatial mixed nine-node integrals at 21 and 25 points are $2.655051033989727$ and $2.655051033957530$. The five-node result at 25 points is $2.655370888723786$, and the transverse bound 8 to 12 changes the integral by about $1.77$ times $10^{-8}$. The joint checkpoint replay passes the longitudinal, quadrature, and transverse criteria for both orientations. The two finite-band mixed projections are $c_{RX}=0.001085223735$ and $c_{\mathrm{RicTT}}=-0.000661025048$. The corresponding nine-node estimates in the previous band are $0.001135739551$ and $-0.000680399965$. The propagated shifts from the tested numerical refinements are $1.05$ times $10^{-7}$ and $6.28$ times $10^{-7}$ on the shorter band. The differences from the previous band, approximately 4.45% and 2.85%, exceed those shorter-band shifts and show remaining cutoff dependence at fixed external momentum. No coefficient from either band is used in a ball subtraction.

🟢 [Done] Added configurable transverse bounds and propagated the observed refinement shifts into the Einstein-free quartic projection. For the completed band $[0.028,0.056]$ at $L_x=3.6$, the observed shifts from the three numerical refinement directions sum to $4.04\times10^{-4}$ for the fundamental and $2.61\times10^{-5}$ for the second harmonic after propagation through $(C+3S)/q^4$. The two projections differ by $4.93\times10^{-4}$. This is close to the propagated shifts. They are numerical diagnostics and do not bound the true remainder. Tightening the transverse check is particularly important once division by the small momentum to the fourth power amplifies the response error.

The first shear response at $L_x=4.2$ and $[0.024,0.048]$ is $-1.116853828$ at 33 points and $-1.116625954$ at 37 points. The 37-point transverse bound 5 gives $-1.111951449$. Longitudinal refinement and quadrature pass, while transverse bounds 5 and 8 fail the 0.1% response-level comparison. On the 33-point grid the tighter transverse comparison moves from $-1.1168538280$ at bound 8 to $-1.1168538502$ at bound 12, a change of $2.22$ times $10^{-8}$. The larger bound resolves this response at fixed longitudinal size. The complete tightly controlled two-wave fit remains pending.

🟠 [Next] Complete the refined pure-curvature family at $[0.024,0.048]$ and $L_x=4.2$ and repeat with tighter transverse bounds if needed. Then test the momentum and cutoff extrapolations before using any coefficient in the fixed-generalized-volume entropy. The state and constraint contributions to the renormalized $r^4$ term remain open.

### Tight transverse cutoff and curvature extrapolation

🟢 [Done] Verified both long-box shear harmonics at transverse bounds 8 and 12 on 33- and 37-point longitudinal grids. At $L_x=4.2$ and $[0.024,0.048]$ the 37-point, bound-12 values are $-1.1166259767$ and $-4.5458330012$. Raising the transverse bound changes each by approximately $2.22\times10^{-8}$. The longitudinal and quadrature checks pass for both shear harmonics.

🟢 [Done] Implemented common-reference cutoff diagnostics in [curvature_cutoff_extrapolation.py](experiments/curvature_cutoff_extrapolation.py). For each numerically resolved band, use the two harmonic projections to form a linear $q^2$ intercept of the scalar- and Ricci-squared terms and scale the Einstein projection by $\sigma$. Compare a three-band linear intercept in $\sigma$ with the two-shortest-band intercept. Propagate the observed refinement shifts through the linear weights. A synthetic test recovers the inputs after both extrapolations and the volume correction.

Both conformal harmonics also pass the longitudinal, transverse and quadrature checks. At 37 points and bound 12 their stored band responses are $3.1078970213$ and $12.3394231103$, and the respective changes from bound 8 are about $3.79$ and $3.40$ times $10^{-8}$. With the common volume reference, the Einstein-free projections are $-0.01441336$ and $-0.01407917$. Their difference $3.34$ times $10^{-4}$ is comparable to the sum of the observed refinement shifts, $3.17$ times $10^{-4}$. The requirement of a momentum-independent local projection is not resolved at this precision.

| Cutoff extrapolation | Scaled Einstein | Scalar squared | Ricci squared |
|---|---:|---:|---:|
| Three bands | 0.01183473 | -0.00014299 | -0.00139905 |
| Two shortest bands | 0.01182302 | -0.00003901 | -0.00175339 |
| Propagated observed shifts for three bands | 0.00001565 | 0.00021162 | 0.00058958 |

The Einstein intercept is consistent across the two fits on this diagnostic. The higher-curvature intercepts vary substantially. Two momenta leave the next momentum power untested, and changing $L_x$ on the shortest band confounds the cutoff comparison. These are finite-data extrapolations and no coefficient is used to subtract the physical entropy.

🟠 [Next] Compare bands at fixed box and add a momentum to test the higher-power remainder. Continue independent clock matching and the matched state and constraint calculation before inferring a renormalized held-volume $r^4$ coefficient.

### Fixed-box cutoff comparison and third-wave holdout

🟢 [Done] Implemented [curvature_momentum_validation.py](experiments/curvature_momentum_validation.py). At fixed $L_x=4.2$, the same two momenta can be compared between $\sigma=0.028$ and $0.024$ without changing the volume reference. A separate test removes the Einstein term through $(C+3S)/q^4$, fits a line in $q^2$ at the first two waves, and evaluates its prediction on the third wave. The line retains a $q^6$ term in the original response. The code propagates observed numerical refinement shifts through this prediction. A synthetic local action with an additional $q^6$ term gives a zero holdout residual.

The operator jet now obtains the value and both derivatives from one nested JVP. The earlier direct trace derivative at five points is reproduced to relative tolerance $10^{-8}$. The temporary checkpoints from the earlier run are unavailable. The previously recorded 37-point reference and observed grid shifts are included explicitly in the diagnostic. The new fixed-box and third-wave rows are saved in [experiments/checkpoints](experiments/checkpoints/) as they complete.

At the third harmonic, 37-point, bound-12 conformal and shear responses are $25.762006601$ and $-10.476547731$. They pass the longitudinal, transverse, and quadrature checks. The common-reference Einstein-free projections for all three waves are $(-0.01441336,-0.01407917,-0.01355144)$. The third-wave holdout residual is $-2.92$ times $10^{-5}$, compared with $6.60$ times $10^{-4}$ from the propagated observed refinement shifts. The residual is unresolved at this resolution and consistent with the tested $q^6$ term. Fitting the two response families independently through $q^6$ gives Einstein projections $0.49572092$ and $0.49574055$, with observed shifts $0.00018262$ and $0.00026028$ respectively. Their agreement is a finite-band diagnostic.

The two shear harmonics on the same box also pass numerical refinement at $[0.028,0.056]$, with 37-point band responses $-0.95869174$ and $-3.91058036$. The shear-only two-wave projection gives scaled Einstein values $0.01191528$ at $\sigma=0.028$ and $0.01190362$ at $\sigma=0.024$. Its corresponding Ricci-squared projections are $-0.00126137$ and $-0.00131986$. This comparison holds external momentum and box size fixed. It remains a two-wave approximation with no separate conformal constraint.

🟢 [Done] Completed the fixed-box comparison at $L_x=4.2$. All four $[0.028,0.056]$ probes pass the longitudinal, transverse and quadrature gates. The common-reference conformal and shear data give $sigma c_R=0.0119033520$ at $sigma=0.028$ and $0.0118956412$ at $sigma=0.024$. The two-band linear intercept and propagated observed shifts are:

| Projection | Intercept | Observed shift propagated through fit |
|---|---:|---:|
| Scaled Einstein | 0.01184938 | 0.00002470 |
| Scalar squared | -0.00007951 | 0.00038625 |
| Ricci squared | -0.00154240 | 0.00106509 |

The Einstein scaling is consistent with the earlier varying-box diagnostic. The higher-curvature extrapolation remains sensitive to the short cutoff lever arm and propagated numerical error. The three-wave test covers one band only and constrains a combination of higher-curvature operators. No band estimate is used to subtract physical entropy.

🟠 [Next] Increase the cutoff lever arm at fixed geometry, refine the cancellation-sensitive low-wave projections, and repeat the higher-power momentum check across bands. Complete independent mixed matching before applying coefficients to the held-volume constraint and state comparison.

### Fixed-box multi-band and low-wave refinement

🟢 [Done] Implemented [curvature_band_batch.py](experiments/curvature_band_batch.py) to evaluate several proper-time bands from the same operator samples. The batch calculation uses the same 8- and 16-node quadratures and writes the existing individual checkpoint records. A seven-point numerical run reproduces the separate integrations to relative tolerance $10^{-10}$.

🟢 [Done] Extended [curvature_momentum_validation.py](experiments/curvature_momentum_validation.py) to run the third-wave holdout at each available fixed-box band and substitute a finer fundamental only after checking it against the 37-point result. The three-wave projections allow distinct $q^6$ terms for the conformal and shear families. Reconstruct their $q^2$ and $q^4$ coefficients and propagate the observed refinement shifts through the linear fit. A synthetic check with independent $q^6$ terms verifies the lower-order projections. The state and constraint terms are not included in this smooth-action diagnostic.

At $L_x=4.2$ and $sigma=0.024$, refining only the fundamental from 37 to 41 points changes the conformal and shear actions by $-1.7690$ times $10^{-5}$ and $+7.2047$ times $10^{-6}$. In the third-wave comparison the propagated observed variation drops from $6.60$ times $10^{-4}$ to $2.69$ times $10^{-4}$. The held-out residual stays at $-2.79$ times $10^{-5}$, still below the variation. The refined three-wave diagnostic gives $(sigma c_R,c_{R^2},c_{mathrm{Ric}^2})=(0.0118974323,-0.00007678386,-0.0014566861)$ with corresponding observed shifts $(0.000002168,0.000024136,0.000055733)$. These are finite-band values.

🟢 [Done] Completed both mixed orientations at $[0.024,0.048]$ on the separate $L_x=1.8$ mixed-probe box. At 25 points, the nine-node spatial and temporal integrals are $2.580284846529$ and $3.219399454039$. Both pass against 21 points, transverse bounds 8 and 12, and five-node quadrature. The finite-band mixed projections are $c_{RX}=0.001048718375$ and $c_{mathrm{RicTT}}=-0.000624574156$. The propagated observed shifts are $1.04$ times $10^{-7}$ and $6.26$ times $10^{-7}$. Relative to $sigma=0.028$ the magnitudes change by roughly 3.36% and 5.51%. With the two previous bands included, a linear cutoff extrapolation gives approximately $(0.00086275,-0.00051571)$, while the two shortest bands give $(0.00082969,-0.00040587)$. The different intercepts motivate more cutoff and momentum checks before matching a divergence.

The held-out third wave distinguishes the momentum truncation from the discretization at fixed $L_x=4.2$. At $sigma=0.035$ its residual is $-0.00121317$, against an observed propagated shift of $7.50$ times $10^{-7}$. At $sigma=0.028$ the residual is $-0.000135237$, against $3.07$ times $10^{-5}$. Both exceed the tested shifts, while the $0.024$ residual does not. This rejects use of the $q^6$ truncation as an accurate description across the full interval of bands.

For comparison, separate three-wave fits followed by a linear cutoff extrapolation give:

| Cutoff fit | Scaled Einstein | Scalar squared | Ricci squared |
|---|---:|---:|---:|
| 0.035, 0.028, 0.024 | 0.01182197 | 0.00002639 | -0.00191153 |
| 0.028, 0.024 | 0.01184242 | -0.00001773 | -0.00174217 |

These values are diagnostic. In particular the scalar-squared projection changes sign, the mixed two-band and three-band fits disagree, and the momentum holdout detects truncation error. No extrapolated value is used as a counterterm in the ball.

🟢 [Done] All six pure responses at the shortest band, $sigma=0.021$, pass the 37-to-41-point, transverse, and quadrature checks. The third-wave residual is $-1.42$ times $10^{-5}$ against a propagated shift of $2.01$ times $10^{-4}$. The three-wave projections are $(0.0118918218,-0.00007192219,-0.0014831267)$ with observed shifts $(0.000001417,0.000010575,0.000023594)$.

With this band included, the four-band cutoff intercept is $(0.0118304322,0.00000849983,-0.0018435925)$, and the two-shortest-band intercept is $(0.0118525484,-0.00003789055,-0.0016682108)$. Their comparison still leaves the higher-curvature coefficients sensitive to the cutoff range. The broad fit also includes bands rejected by the third-wave test of the momentum truncation.

🟠 [Next] Use a smaller third momentum or test additional momentum terms before treating the cutoff extrapolation as ultraviolet matching. Extend the independent mixed sequence to reduce its cutoff and momentum sensitivity. No extrapolated counterterm has been applied to the state- and constraint-inclusive fixed-generalized-volume entropy, so $r^4$ cancellation remains undetermined.

### Fourth-wave curvature test and shorter mixed band

🟢 [Done] Added the fourth harmonic to the batch driver and implemented [curvature_four_wave.py](experiments/curvature_four_wave.py). It fits each response family through $q^8$, compares the lower-order projections with the previous $q^6$ fit, and propagates the observed refinements through the fits. Independently, it fits the first three Einstein-free quartic projections as a quadratic in $q^2$ and predicts the fourth. A synthetic pair of responses verifies both the coefficient recovery and the fourth-wave holdout. The box and the common volume reference are fixed for all comparisons.

The fourth conformal harmonic passes longitudinal refinement from 37 to 41 points in all four bands. At the shortest cutoff $\sigma=0.021$ its bound-12 action response changes from $48.063335599$ to $48.056043569$. The shear and mixed refinements complete the numerical checks.

🟢 [Done] At the mixed band $[0.021,0.042]$ on the same $L_x=1.8$ probe box, both orientations pass the 21-to-25-point, transverse 8-to-12, and quadrature checks. The 25-point nine-node integrals are $2.527453745687$ (spatial) and $3.125669117002$ (temporal). They give $(c_{RX},c_{mathrm{RicTT}})=(0.001018185747,-0.000584605416)$ with propagated observed shifts $(1.08$ times $10^{-7},6.49$ times $10^{-7})$. The four-band linear intercept is $(0.00084716,-0.00046022)$ and the two-shortest-band intercept is $(0.00080446,-0.00030482)$. For the combination $c_{RX}+c_{mathrm{RicTT}}/2$ entering the earlier local sphere diagnostic, the finite-band value falls from $0.00073643$ to $0.00072588$ between the last two bands. These results do not supply a stable mixed ultraviolet counterterm.

🟢 [Done] Both fourth-wave responses pass longitudinal, transverse, and quadrature checks in all four bands. The independent fourth-wave holdout gives:

| Lower proper time | Fourth-wave residual | Propagated observed refinements |
|---:|---:|---:|
| 0.035 | 0.00249111 | 0.00000243 |
| 0.028 | 0.00025259 | 0.00009511 |
| 0.024 | 0.00002985 | 0.00080830 |
| 0.021 | 0.00000185 | 0.00051280 |

The residual exceeds observed refinements for the two longer bands. At the two shorter bands the test is compatible with $q^8$ at the current precision. After $q^8$ fits, the cutoff intercepts are:

| Cutoff fit | Scaled Einstein | Scalar squared | Ricci squared |
|---|---:|---:|---:|
| Four bands | 0.01183060 | 0.00001426 | -0.00187211 |
| Two shortest bands | 0.01185291 | -0.00003909 | -0.00166807 |

Adding $q^8$ barely changes the two-shortest-band results from the previous $q^6$ fits. The scalar-squared coefficient still changes sign across fit ranges and its propagated shifts exceed its magnitude. The Ricci-squared shift is also substantial in the two-shortest extrapolation. Convergence of the band integrals therefore does not establish the ultraviolet counterterms.

🟠 [Next] Extend the short-cutoff interval using independent lower-momentum probes and improve the low-wave curvature precision. Continue mixed momentum and cutoff matching. No extrapolated value in this section has been applied to the held-volume entropy, so the constraint- and state-inclusive $r^4$ cancellation remains undetermined.

### Independent lower-momentum probes on longer boxes

🟢 [Done] Made the longitudinal box length a parameter of the batched curvature driver and added [curvature_cross_box.py](experiments/curvature_cross_box.py). The new pure probe uses $L_x=5.6$ with unchanged transverse lengths. Its fundamental momentum is $3/4$ of the $L_x=4.2$ fundamental. The cutoff comparison uses $[0.024,0.048]$ and $[0.021,0.042]$ at each fixed box length. The longer box uses 49 and 53 longitudinal points and transverse bounds 8 and 12. Fundamental conformal results on the 53-point grid are $1.727715005$ and $1.994222202$ at the two respective cutoffs and pass all three numerical checks. The comparison also tests the Einstein-free combination at the two new momenta against a $q^6$ prediction from the shorter box. This change of momentum and box probes the combined sensitivity. An overlapping physical momentum would make an additional independent finite-volume check.

The mixed probes use $L_x=2.4$ with unchanged transverse lengths and keep the same shortest band $[0.021,0.042]$ for a direct comparison with the previous $L_x=1.8$ data. Their fundamental momentum is also reduced by a factor of $3/4$. The temporal nine-node integrals at 29 and 33 points are $2.014610329765$ and $2.014610321681$. They pass longitudinal, transverse and quadrature refinement. The corresponding spatial orientation is evaluated independently.

🟢 [Done] Both mixed orientations on the longer box pass the three numerical checks. At 33 points the spatial integral is $1.795785983417$, compared with $1.795785991451$ at 29 points. At the same band the projections change from $(0.001018185747,-0.000584605416)$ at $L_x=1.8$ to $(0.000875011584,-0.000285127842)$ at $L_x=2.4$. For the longer box the observed shifts are $1.10$ times $10^{-7}$ and $6.63$ times $10^{-7}$. The changes in magnitude, about 14.1% and 51.2%, are far larger than those numerical shifts. The comparison changes both the external momentum and the finite box. [Mixed cross-box diagnostic](experiments/mixed_cross_box.py).

Restoring the global zero sector only as an infrared diagnostic gives mixed projections $(0.001092986652,-0.000836663029)$ at $L_x=1.8$ and $(0.000933589793,-0.000474171051)$ at $L_x=2.4$. The change remains large in both projections. Zero-sector exclusion alone therefore does not explain the cross-box dependence at this band.

On the 53-point grid the fundamental shear responses at the two cutoffs are $-0.6260867423$ and $-0.7149672512$. With the common volume subtraction, the Einstein-free fundamental projections are $-0.0146414355$ and $-0.0147261980$. The shorter-box three-wave prediction at this momentum gives $-0.0144553051$ and $-0.0145997397$, respectively. The differences are about $1.86$ times $10^{-4}$ and $1.26$ times $10^{-4}$, compared with propagated refinement shifts $6.74$ times $10^{-5}$ and $2.40$ times $10^{-4}$. The longer band resolves a discrepancy, while the shorter band does not. The comparison alone does not separate the box dependence from higher momentum terms.

🟢 [Done] Both harmonics and both pure probe families pass all numerical checks at both cutoffs in the longer box. Using the common volume reference, independent two-wave momentum fits followed by two-band cutoff extrapolation give:

| Longitudinal box | Scaled Einstein | Scalar squared | Ricci squared |
|---:|---:|---:|---:|
| 4.2 | 0.01185337 | -0.00003687 | -0.00165919 |
| 5.6 | 0.01185961 | -0.00007188 | -0.00155251 |
| Observed shifts propagated for 5.6 | 0.00000983 | 0.00030197 | 0.00083533 |

The scaled Einstein result is stable across this comparison. The observed higher-curvature shifts exceed the cross-box differences, so the lower momenta and narrower numerical errors do not resolve those ultraviolet coefficients. In the Einstein-free comparison the longer-box second harmonic differs from the shorter-box three-wave prediction by about $1.39$ times $10^{-4}$ at $sigma=0.024$ and $1.11$ times $10^{-4}$ at $sigma=0.021$. The observed variations are $3.89$ times $10^{-5}$ and $9.36$ times $10^{-5}$. This comparison still combines a changed box and momentum.

🟠 [Next] Use a common physical momentum across boxes, for example harmonic 3 at $L_x=4.2$ and harmonic 4 at $L_x=5.6$. Increase the fixed-box cutoff lever arm and independently resolve the clock momentum dependence. No coefficient from this comparison is applied to the held-volume sphere, so cancellation of $r^4$ including the state and constraint variations remains unresolved.

### Matched physical momentum across longitudinal boxes

🟢 [Done] Added a physical-momentum comparison in [matched_wave_comparison.py](experiments/matched_wave_comparison.py). For the pure action, harmonic 3 on $L_x=4.2$ and harmonic 4 on $L_x=5.6$ have identical $q=2\pi\,3/4.2$. Both transverse lengths and proper-time bands stay fixed. The test compares the common-reference responses and their Einstein-free combination $(C+3S)/q^4$. At this matched momentum a difference between the two regulated responses measures longitudinal box dependence, including the finite-volume zero-sector prescription.

🟢 [Done] Extended the mixed insertion to arbitrary resolved harmonics. At curvature order $j$ it retains the discrete Fourier transfers $0,\pm h,\ldots,\pm jh$ modulo the lattice size. At second order in curvature a closed contribution to the trace visits only the starting momentum and its neighbors displaced by $\pm h$. A factorized second-harmonic block agrees with the full block, and the normalization uses the physical momentum and four-volume. The mixed comparison matches harmonic 1 at $L_x=1.8$ to harmonic 2 at $L_x=3.6$ at fixed proper-time band $[0.021,0.042]$. Both orientations are required.

For the matched conformal wave, both boxes pass all numerical checks at both bands. The longer-minus-shorter common-reference responses are $-0.03783116$ at $sigma=0.024$ and $-0.03083834$ at $sigma=0.021$. The corresponding combined observed refinement shifts are $0.00811461$ and $0.00522716$. Hence the conformal response has a resolvable longitudinal-box dependence at fixed momentum in the regulated calculation. This comparison has yet to combine the conformal and shear responses.

🟢 [Done] Extended the fixed $L_x=1.8$ mixed sequence to $[0.018,0.036]$. Both orientations pass the 25-to-29-point, transverse 8-to-12, and quadrature checks. Their nine-node integrals are $2.477970861532$ and $3.024137303398$. The projections are approximately $(0.000985112,-0.000533741)$, with observed shifts $(1.57$ times $10^{-7},9.40$ times $10^{-7})$. Linear fits to all five bands and the shortest two give $(0.00083241,-0.00040480)$ and $(0.00078667,-0.00022855)$ respectively. The longer cutoff sequence does not remove the fit-range sensitivity.

🟢 [Done] All matched-momentum pure probes pass numerical refinement. At $q=4.487989505$ the longer-minus-shorter Einstein-free differences are $-1.11215$ times $10^{-4}$ and $-8.95990$ times $10^{-5}$ at $sigma=0.024$ and $0.021$, respectively. Their combined observed shifts are $5.93854$ times $10^{-5}$ and $3.63384$ times $10^{-5}$. Consequently the box dependence survives in the curvature-sensitive combination with the Einstein term eliminated. This fixed-momentum result includes the zero-sector convention.

🟢 [Done] Both matched-momentum mixed orientations on $L_x=3.6$ pass the 41-to-45-point, transverse 8-to-12 and quadrature checks. At $q=3.490658504$ and $sigma=0.021$, the longer-minus-shorter shifts in the two projections are $(3.74003$ times $10^{-5},-1.26029$ times $10^{-4})$. The corresponding propagated refinement shifts are $(2.16306$ times $10^{-7},1.29737$ times $10^{-6})$. This is longitudinal-box dependence at exactly the same external momentum in the regulated mixed calculation. It is independent of the earlier comparison in which both the box and the wave number changed.

🟢 [Done] Extended the pure comparison to the same three lower cutoffs $0.028,0.024,0.021$ at each fixed box length. The new $L_x=5.6$ band passes on 41 and 45 points, transverse bounds 8 and 12, and the two quadratures. With the common volume reference and the two-wave momentum fit:

| Longitudinal box | Cutoff fit | Scaled Einstein | Scalar squared | Ricci squared |
|---:|---|---:|---:|---:|
| 4.2 | Three bands | 0.01185119 | -0.00006021 | -0.00159527 |
| 4.2 | Two shortest | 0.01185337 | -0.00003687 | -0.00165919 |
| 5.6 | Three bands | 0.01185880 | -0.00016711 | -0.00127801 |
| 5.6 | Two shortest | 0.01185961 | -0.00007188 | -0.00155251 |

At $L_x=5.6$ the propagated observed shifts for the three-band fit are $(0.00001318,0.00034297,0.00094886)$. The Einstein projection is consistent across the fit ranges, while the higher-curvature projections are unresolved at that precision. The longer mixed box is matched at one cutoff only. The five-band mixed extrapolation for the short box remains fit-range dependent.

🟠 [Next] Repeat the matched mixed comparison across cutoff bands on both boxes and independently control the residual box dependence of the pure coefficients. Determine the counterterm set before using it in the state- and constraint-inclusive fixed-generalized-volume entropy. The numerical matching reported here does not establish $r^4$ cancellation.

### Matched-band zero-sector diagnostics

🟢 [Done] Repeated the matched pure comparison after restoring the global zero sector in the differentiated traces. Both conventions use the same full flat volume reference. The original Einstein-free differences at $\sigma=0.024,0.021$ are $-1.11215$ and $-0.89599$, respectively, in units of $10^{-4}$. With the sector restored the differences are $+6.46$ times $10^{-7}$ and $-3.75$ times $10^{-7}$. These are below the coarse-to-fine shifts of $5.94$ and $3.63$ times $10^{-5}$ in the restored responses. Thus the zero-sector exclusion explains the resolved pure box dependence to the present precision. This is a diagnostic on heat traces and does not change the physical clock prescription. Reproduce using [matched_wave_comparison.py](experiments/matched_wave_comparison.py) with the pure comparison and zero-sector diagnostics.

At fixed box length and fixed external harmonic, removing a finite-dimensional global sector changes the leading heat trace by a rank term. Its curvature and clock amplitude derivatives vanish at $s=0$ while the rank stays fixed. In the finite lattice calculation the remaining change is $O(s)$ at short proper time. At the derivative orders used here the changed zero-sector contributions transfer only finitely many multiples of the external momentum. The diagnostic removes a finite-band infrared effect without assigning a new prescription to the physical ball.

The same infrared diagnostic on the two lower harmonics gives the following two-band cutoff intercepts with a common volume reference:

| Longitudinal box | Restored scaled Einstein | Restored scalar squared | Restored Ricci squared |
|---:|---:|---:|---:|
| 4.2 | 0.01187579 | -0.00006698 | -0.00153792 |
| 5.6 | 0.01187551 | -0.00009024 | -0.00146966 |

The Einstein intercepts agree more closely than in the projected calculation. The higher-curvature differences are small relative to the previous numerical variation propagated through the same two-band fit. With two bands and two momenta neither the higher momentum remainder nor the short-time tail is controlled. [Restored-sector cutoff diagnostic](experiments/matched_wave_comparison.py).

🟢 [Done] Completed the equal-momentum mixed comparison in both boxes at both cutoffs. The new $L_x=3.6$ band passes the 41-to-45-point, transverse, and quadrature checks. The two-projection results are:

| Lower proper time | $L_x=1.8$: $RX$, Ricci–clock | $L_x=3.6$: $RX$, Ricci–clock |
|---:|---:|---:|
| 0.024 | $(0.00104872,-0.000624574)$ | $(0.00109699,-0.000789183)$ |
| 0.021 | $(0.00101819,-0.000584605)$ | $(0.00105559,-0.000710634)$ |

The raw same-momentum box differences exceed the propagated numerical shifts in both bands. The magnitude of the box difference falls at the shorter band. The projected two-band cutoff intercepts are approximately $(0.00080446,-0.00030482)$ and $(0.00076577,-0.00016079)$. Their difference is substantial for the Ricci–clock projection.

🟢 [Done] Restored the zero sector in both mixed bands at matched momentum. The raw zero-sector changes of the integrated traces agree between the two boxes to roundoff for each orientation. After volume normalization and restoration, the largest remaining same-momentum difference in the two mixed projections is $1.67$ times $10^{-9}$ at $sigma=0.024$ and $1.90$ times $10^{-10}$ at $sigma=0.021$. Both are far below the numerical shifts observed in the primed responses. The restored two-band intercepts agree across boxes, approximately $(0.00072705,-0.00001676)$. This agreement tests finite volume at one momentum. It does not test the cutoff fit over a wider range or resolve the momentum dependence of either mixed coefficient. The projected-to-restored correction is diagnostic and does not insert a new clock state.

🟠 [Next] Extend the restored common-reference comparison across cutoff and momentum ranges, especially at lower external momentum. The ultraviolet coefficients and the matched constraint and state variations remain to be fixed. None of these diagnostic coefficients has been applied to the held-volume sphere; $r^4$ cancellation remains undetermined.

### Restored short-cutoff and lower-momentum comparison

🟢 [Done] Implemented [restored_short_cutoff.py](experiments/restored_short_cutoff.py). It compares pure responses on the fixed $L_x=5.6$ box over the lower cutoffs $0.024,0.021,0.018$ using longitudinal points 53 and 57 for the shortest band. The corresponding restored mixed comparison uses $L_x=2.4$ at $0.021$ and $0.018$ and retains $L_x=1.8$ as a higher-momentum control. The two momenta differ by a factor of $3/4$. Both the projected band check and the independently checkpointed zero-sector correction are recorded. The reported numerical shifts are those of the raw grid test, propagated through the restored fit; they do not bound extrapolation error.

At the higher-momentum reference $L_x=1.8$, the zero-sector-restored mixed coefficient pair at $sigma=0.018$ is approximately $(0.00104078,-0.00071893)$. Using $0.024,0.021,0.018$ gives a linear intercept $(0.000727333,-0.000014428)$, compared with $(0.000727563,-0.000012503)$ from the two shortest bands. The combination $c_{RX}+c_{mathrm{RicTT}}/2$ has intercepts $0.000720119$ and $0.000721312$, respectively. The low-momentum comparison is still needed before interpreting this apparent cutoff stability.

For the fundamental conformal wave at $L_x=5.6$, the shortest-band responses are $2.34983411717$ at 53 points and $2.34969419803$ at 57 points before the common volume correction. On the finer grid the 8-to-12 transverse change is about $1.71$ times $10^{-5}$. The longitudinal, transverse and quadrature comparisons pass for this response.

The zero-sector correction itself is numerically independent of the large longitudinal grids in the tested channels. The pure correction at $L_x=5.6$, $sigma=0.018$ reproduces the 57-point result on 17 points for both harmonics and both probes, to about $1.1$ times $10^{-15}$ absolute. The mixed correction at $L_x=2.4$, $sigma=0.021$ reproduces the 33-point result on 9 points in both orientations to $1.3$ times $10^{-15}$. This supports using the raw-grid refinement shifts as the dominant numerical contribution in those restored comparisons, without changing the grid needed for the full heat trace.

🟢 [Done] Both low-momentum mixed orientations at $L_x=2.4$ and $[0.018,0.036]$ pass longitudinal, transverse and quadrature refinement. With the zero sector restored, linear extrapolations to zero momentum at the two cutoffs give $(0.000728651,-0.000008110)$ at $0.021$ and $(0.000729341,-0.000005898)$ at $0.018$. A subsequent two-cutoff linear intercept is $(0.000733479,+0.000007376)$ with corresponding propagated observed shifts $(0.000006937,0.000041572)$. The Ricci–clock estimate is compatible with zero at this precision. The momentum extrapolation uses two distinct boxes, assumes residual unprojected box effects are negligible, and has no third-momentum holdout.

The fundamental pure Einstein-free projection, with the sector restored, is $-0.01510661$, $-0.01508339$, and $-0.01508823$ in the three bands. The differences are smaller than the propagated grid shifts. Its two independent invariants still require the second harmonic.

Both conformal waves pass longitudinal, transverse and quadrature refinement at the shortest band. With the common volume reference, the restored conformal two-wave estimates of $\sigma c_R$ are $0.01187273359$, $0.01187308071$, and $0.01187325470$ at $\sigma=0.024,0.021,0.018$. Their propagated raw-grid shifts are $1.40$ times $10^{-7}$, $1.11$ times $10^{-6}$, and $1.19$ times $10^{-6}$.

🟢 [Done] Both harmonics of both pure probes pass the numerical checks on the 53- and 57-point grids at $[0.018,0.036]$. Restoring the zero sector and applying the common volume reference gives:

| Lower proper time | Scaled Einstein | Scalar squared | Ricci squared |
|---:|---:|---:|---:|
| 0.024 | 0.01187273359 | -0.00003425976 | -0.00161961173 |
| 0.021 | 0.01187308071 | -0.00004125777 | -0.00160086812 |
| 0.018 | 0.01187325470 | -0.00004383839 | -0.00159505987 |
| Three-band linear intercept | 0.01187484694 | -0.00007331053 | -0.00151924841 |
| Two-shortest-band intercept | 0.01187429866 | -0.00005932208 | -0.00156021036 |

The propagated shifts for the three-band extrapolation are $(0.000005365,0.000191201,0.000530828)$. Removing the global sector effect makes the Einstein scale exceptionally stable and the two cutoff intercepts compatible. The scalar-squared shift still exceeds its estimated magnitude, and the Ricci-squared uncertainty remains substantial. The two-wave fit does not independently test higher powers of momentum.

🟠 [Next] Add an independent low momentum for the restored mixed fit and reduce the pure low-wave numerical errors before accepting the ultraviolet counterterm set. No diagnostic coefficient here is used to subtract the sphere. Cancellation of the fixed-generalized-volume $r^4$ term including constraints and state is still undetermined.

### Paired refinement and third mixed momentum

🟢 [Done] Added signed longitudinal, transverse, and quadrature refinement differences in [curvature_band_matching.py](experiments/curvature_band_matching.py). Propagating each simultaneous change through the pure projection keeps the observed cancellations between conformal and shear responses and between harmonics on the same grid. Summing magnitudes only after this propagation preserves the distinction between observed paired changes and the older independent-response variation. The three-band restored pure intercepts remain $(0.01187485,-0.00007331,-0.00151925)$. Their paired observed shifts are $(0.000003601,0.000022329,0.000068691)$, versus $(0.000005365,0.000191201,0.000530828)$ with independent-response propagation. These comparisons do not bound the cutoff or momentum remainder.

🟢 [Done] Implemented [mixed_momentum_holdout.py](experiments/mixed_momentum_holdout.py). It compares the original two low momenta with an independent fundamental at $L_x=3.0$ in $[0.018,0.036]$. The third momentum is $2\pi/3.0$. The code propagates the measured numerical shifts through both a linear prediction from the first two momenta and a quadratic fit to all three. The third zero-sector correction agrees between 9 and 13 points in both orientations.

The same accounting is available for the mixed orientations, whose quadrature shifts are nearly equal before subtraction. In the previous joint two-momentum, two-cutoff intercept the Ricci–clock estimate $+7.38$ times $10^{-6}$ has a paired observed shift of $4.98$ times $10^{-8}$, rather than the independent-response sum $4.16$ times $10^{-5}$. The value therefore exceeds this particular numerical diagnostic. Its sensitivity to the momentum and cutoff fits must be tested separately, and the paired shifts are not a total error bar.

🟢 [Done] Both third-wave orientations pass the longitudinal, transverse, and quadrature checks. From 37 to 41 points the nine-node integrals change from $1.393242594227$ to $1.393242504461$ in the spatial orientation and from $1.485398128938$ to $1.485398036787$ in the temporal orientation.

At fixed proper-time band the restored third-wave residual relative to the two-momentum linear prediction is $(4.763	imes10^{-7},1.379	imes10^{-6})$ in $(RX,mathrm{Ricci!-!clock})$ order. The paired observed shifts are $(6.145	imes10^{-7},5.258	imes10^{-9})$. The independent-response shifts are $(6.145	imes10^{-7},3.682	imes10^{-6})$. Fitting a quadratic in $q^2$ to all three momenta changes the Ricci–clock intercept from $-5.898	imes10^{-6}$ to $+8.552	imes10^{-8}$. The quadratic uses all three data points, and the third point changes both momentum and box length. These values establish sensitivity to the extrapolation and leave the ultraviolet coefficient undetermined.

🟢 [Done] Added `--matched-box` and `--two-bands` to [mixed_momentum_holdout.py](experiments/mixed_momentum_holdout.py). The volume control compares the fundamental in $L_x=3$ with harmonic two in $L_x=6$ at the same $q=2\pi/3$ and proper-time band. The second mode repeats the three-wave test at $[0.021,0.042]$ and compares two-band cutoff intercepts obtained with the two momentum fits. Both diagnostics propagate observed refinement shifts.

The zero-sector correction for the matched wave agrees across the 9- and 13-point calculations and scales inversely with longitudinal volume. In the short band it is $(-3.549\times10^{-5},1.111\times10^{-4})$ at $L_x=3$ and $(-1.774\times10^{-5},5.556\times10^{-5})$ at $L_x=6$. The full-trace comparison restores the corresponding correction in each box before forming their difference.

🟢 [Done] Replaced the dense longitudinal Fourier conjugation in the mixed insertion with orthonormal FFTs along the bra and ket site axes. The mixed heat derivatives agree with the dense reference within $6.9\times10^{-15}$ in representative spatial and temporal blocks, including harmonic two.

🟢 [Done] Both orientations pass longitudinal (37 to 41 points), transverse (8 to 12), and quadrature refinement for $[0.021,0.042]$. The third-wave residuals in $(RX,\mathrm{Ricci\!-!clock})$ order are $(5.962\times10^{-7},1.899\times10^{-6})$, with paired observed variations $(3.253\times10^{-7},7.085\times10^{-10})$. Thus the Ricci–clock discrepancy recurs in both bands. The two-band Ricci–clock cutoff intercept changes from $+7.376\times10^{-6}$ with the linear two-momentum fit to $-1.866\times10^{-7}$ with the quadratic three-momentum fit. The latter has an observed paired refinement variation of $1.284\times10^{-7}$. The two time bands determine a line exactly, and the momentum fit still combines different box lengths, so these intercepts are diagnostics.

🟢 [Done] Both orientations in the doubled box pass the 65-to-73-point longitudinal, transverse, and quadrature checks. The restored differences $L_x=6$ minus $L_x=3$ change from $(1.104\times10^{-8},-1.275\times10^{-9})$ at 65 points to $(9.893\times10^{-11},-8.271\times10^{-12})$ at 73 points. The summed paired observed variations are $(5.143\times10^{-7},4.895\times10^{-9})$. For the Ricci–clock channel the box difference and its observed paired variation are both below the short-band third-wave residual of $1.379\times10^{-6}$. This controls the box-length change at the tested momentum and band.

### Independent cutoff and momentum holdouts

🟢 [Done] Extended [mixed_momentum_holdout.py](experiments/mixed_momentum_holdout.py) with `--three-bands` and `--fourth-wave`. The added proper-time band is $[0.024,0.048]$ at the same three physical momenta. The additional fundamental at $L_x=3.6$ gives $q=2\pi/3.6$. Zero-sector corrections for the new rows agree between 9 and 13 points in each orientation.

Predict the third band from a linear fit in the two shorter lower cutoffs at fixed momenta. Predict the fourth wave from a quadratic in $q^2$ at each fixed band. Compare the holdout residuals with measured numerical refinements. Compare the inferred intercepts with and without each added data point. The fourth wave changes longitudinal volume along with momentum. The earlier matched-wave box control applies at $q=2\pi/3$ and the shortest band.

🟢 [Done] The third band passes longitudinal, transverse, and quadrature refinement for the three fixed momenta. In decreasing momentum order the finite-momentum Ricci–clock holdout residuals are $(6.080\times10^{-7},1.708\times10^{-7},5.777\times10^{-8})$. Each exceeds its paired observed variation of about $2.9\times10^{-9}$. At zero momentum the Ricci–clock residual becomes $-3.693\times10^{-9}$ with paired variation $2.660\times10^{-8}$ after the three-wave projection. The short-pair linear, all-band linear, and all-band quadratic Ricci–clock cutoff intercepts are $-1.866\times10^{-7}$, $-1.749\times10^{-7}$, and $-2.642\times10^{-7}$ respectively. The quadratic intercept's paired variation is $6.871\times10^{-7}$. These are numerical diagnostics. The finite-momentum cutoff curvature and the propagated variation of the quadratic intercept limit inference about the divergence.

🟢 [Done] The fourth wave passes longitudinal (45 to 49 points), transverse, and quadrature checks in all three bands. The $RX$ residual is inside the observed refinement variation in every band.

| Lower cutoff | Fourth-wave Ricci–clock residual | Paired variation | Independent variation |
| ---: | ---: | ---: | ---: |
| 0.018 | -1.072e-8 | 6.986e-9 | 5.848e-6 |
| 0.021 | -1.660e-8 | 9.447e-10 | 2.633e-6 |
| 0.024 | -2.415e-8 | 2.449e-9 | 2.379e-6 |

The same-sign Ricci–clock residuals exceed the paired numerical variations and are smaller than the independent-response sums. At zero momentum the all-band linear cutoff estimate changes from $-1.749\times10^{-7}$ with three waves to $+5.966\times10^{-8}$ with four. The four-wave quadratic cutoff estimate is $-3.453\times10^{-7}$ with paired numerical variation $1.609\times10^{-6}$. The fourth momentum still needs a matched-volume control, and three bands fix a quadratic in the cutoff without an independent validation point.

🟢 [Done] Added a fourth-wave matched-box diagnostic at $q=2\pi/3.6$ and $[0.024,0.048]$. It compares the fundamental in $L_x=3.6$ with harmonic two in $L_x=7.2$. Independent zero-sector calculations at 9 and 13 points agree in both boxes. The doubled-volume correction is $(-2.637\times10^{-5},8.230\times10^{-5})$, half the original-box correction to within $2.2\times10^{-18}$.

🟢 [Done] Added signed propagation of simultaneous longitudinal, transverse, and quadrature refinements through the momentum and proper-time fits. For the four-wave quadratic cutoff estimate the Ricci–clock shifts in that order are $(-5.468\times10^{-10},-4.510\times10^{-8},8.065\times10^{-9})$. The orientation-paired sum allowing separate changes at every fit point remains $1.609\times10^{-6}$. These two summaries describe the observed refinement patterns and leave momentum and cutoff model uncertainty open.

🟢 [Done] Factorized the transverse Gaussian moments into one-dimensional sums and added configurable cap pairs to [short_mixed_quadrature.py](experiments/short_mixed_quadrature.py). The factorization agrees with explicit transverse enumeration through cap 16. At 9 longitudinal sites in the original fourth-wave box, the largest pointwise cap-10-to-12 changes over the shortest band are about $2.2\times10^{-6}$ in both orientations. The cap-12-to-16 changes are about $1.6\times10^{-10}$. The small-grid comparison tests tail sensitivity and still requires confirmation on the production grids.

🟢 [Done] Both doubled-box orientations pass longitudinal (65 to 73 points), transverse, and quadrature refinement. The restored differences $L_x=7.2$ minus $L_x=3.6$ in $(RX,\mathrm{Ricci\!-!clock})$ order are $(5.322\times10^{-10},-5.290\times10^{-11})$. The orientation-paired variations summed across boxes are $(2.439\times10^{-7},6.729\times10^{-9})$. Both the Ricci–clock box difference and its paired variation are below the magnitude of the fourth-wave residual $2.415\times10^{-8}$ at the tested band. The independent-response variation is $1.457\times10^{-6}$. This comparison controls box length only at this momentum and band to the resolution of the paired checks.

### Production transverse tails and the shorter cutoff holdout

🟢 [Done] Added [mixed_uv_refinement.py](experiments/mixed_uv_refinement.py) for cap-12-to-16 comparisons on the original production grids and for the independent band $[0.015,0.030]$ at all four original physical momenta. The driver reuses the same operator insertions across multiple time grids and retains separate quadrature and checkpoint data for each band. Grouped traces agree with separate evaluations in the small-grid reference.

The new band is held out of the three-band quadratic fit. The analysis reports the pointwise-in-momentum residual, its zero-momentum projection, and the changes in cutoff intercepts under linear, quadratic, and cubic fits. The sign and size of an intercept must be interpreted alongside the measured refinement variations and the changes across fit choices.

🟢 [Done] Applied the existing finite Fourier-transfer trace to the projected zero-transverse-momentum block. The change of basis uses the same mean-zero subspace as the original operator, and each closed curvature-order-two path visits only its starting mode and the two adjacent probe transfers. Grouped traces agree with the original full exponential within $1.8\times10^{-15}$ in tests covering both orientations and harmonics one and two.

🟢 [Done] Verified the cap-12-to-16 comparison at all four momenta and in both orientations on production grids. The largest pointwise trace change is $5.755\times10^{-8}$ in the new shortest band and $1.875\times10^{-10}$ across the three earlier bands. In the shortest band the cap change alters the restored $RX$ and Ricci–clock projections by at most $1.721\times10^{-12}$ and $8.023\times10^{-15}$, respectively. The new band passes longitudinal and quadrature refinement at all four momenta.

At fixed momenta, the fourth-band Ricci–clock residuals against the quadratic cutoff fit to the earlier bands range from $4.294\times10^{-9}$ to $1.487\times10^{-8}$. Their orientation-paired observed variations are at most $1.320\times10^{-9}$. After the four-wave momentum projection the residual is $1.523\times10^{-8}$ with observed variation $2.621\times10^{-8}$. The four-band, four-wave Ricci–clock cutoff intercepts for linear, quadratic, and cubic fits are $+3.174\times10^{-8}$, $-1.556\times10^{-7}$, and $+5.077\times10^{-7}$. The corresponding observed variations are $3.357\times10^{-8}$, $1.983\times10^{-7}$, and $1.058\times10^{-6}$. These are fit diagnostics rather than total uncertainties. For the four-band quadratic intercept the simultaneous Ricci–clock changes are $-1.596\times10^{-8}$ from longitudinal refinement, $-1.014\times10^{-13}$ from the cap increase, and $+4.207\times10^{-9}$ from quadrature refinement.

### Separate quadrature from longitudinal refinement

🟢 [Done] Added nested Romberg integration to [mixed_uv_refinement.py](experiments/mixed_uv_refinement.py). It reuses the nine production time nodes and recomputes the zero-sector correction with the same quadrature. For the four-wave four-band quadratic Ricci–clock cutoff fit, the separately propagated observed shifts decrease from $1.983\times10^{-7}$ to $1.017\times10^{-7}$, while the intercept changes from $-1.556\times10^{-7}$ to $-1.553\times10^{-7}$. The simultaneous longitudinal and quadrature changes in the Romberg fit are $-1.521\times10^{-8}$ and $1.030\times10^{-9}$. The earlier-band longitudinal differences still use the stored Simpson comparisons. These diagnostics measure observed changes under the stated refinements.

The Romberg all-band Ricci–clock intercepts remain sensitive to fit degree. The four-wave linear, quadratic, and cubic intercepts are $+3.165\times10^{-8}$, $-1.553\times10^{-7}$, and $+5.071\times10^{-7}$. Reduced quadrature variation leaves this fit dependence visible.

🟢 [Done] At the lowest momentum and shortest band, verified the overlap of the 9- and 17-node traces at 49 longitudinal points and ran both orientations at 53 points. With Romberg quadrature and the matching zero-sector correction, the Ricci–clock projection changes by $5.267\times10^{-13}$ from adding time nodes and by $2.879\times10^{-12}$ from refining the longitudinal grid. Substituting the refined row shifts the four-wave, four-band quadratic cutoff intercept by $3.330\times10^{-10}$. The measured change is small compared with the spread across fit degrees.

🟢 [Done] Rank individual rows by their observed contributions to the quadratic intercept variation. The largest remaining longitudinal contribution is at $L_x=3$, $\sigma=0.015$ and is $3.335\times10^{-8}$. The $L_x=3$, $\sigma=0.024$ row gives a quadrature contribution of $1.604\times10^{-8}$. The initial ranking still includes the older $L_x=3.6$ grid pair, for which the independent refinement is reported above.

### Audit of ultraviolet matching and the sphere test

🟢 [Done] At $L_x=3$, refined the longitudinal grid from 41 to 45 points in $[0.015,0.030]$ and the time quadrature from 9 to 17 nodes in $[0.024,0.048]$. Both orientations pass the refinement checks, and the denser time grid reproduces the shared nodes. With matched zero-sector corrections, the changes in $(RX,\mathrm{Ricci\!-\!clock})$ are $(-2.621\times10^{-11},+2.281\times10^{-12})$ and $(-3.123\times10^{-10},-1.942\times10^{-12})$, respectively.

🟢 [Done] Refit all four waves and four bands with these rows and the previously verified $L_x=3.6$ refinement. The Ricci–clock cutoff intercepts are $+3.163\times10^{-8}$, $-1.551\times10^{-7}$, and $+5.066\times10^{-7}$ at degrees one, two, and three. The paired variation propagated independently across rows for the quadratic fit decreases to $3.461\times10^{-8}$. The held-out shortest-band residual after the four-wave momentum projection is $1.520\times10^{-8}$, compared with a propagated observed variation of $6.622\times10^{-9}$. The refinements preserve the model dependence. Reproduce with `mixed_uv_refinement.py --analyse --quadrature romberg --refined-fit` and the production checkpoint directory.

The accumulated probes provide useful checks of the discretized trace, of the volume reference, and of individual numerical refinements. The extraction of a local Wilson coefficient needs additional evidence. For the four-wave, four-band quadratic estimate, the sums of absolute momentum and cutoff intercept weights are $21.21$ and $41.00$. Their product $869.64$ is the amplification for arbitrary uniform per-row errors. Signed paired changes can be much smaller, and they test only the simultaneous refinements actually performed. Moreover, a function proportional to $\prod_j(\sigma-\sigma_j)$ vanishes at the measured lower cutoffs $\sigma_j$ and changes the extrapolated constant. An independently justified short-time remainder or an analytic coefficient is therefore needed.

🟠 [Next] Derive the local short-time expansion of the complete gauge-fixed metric, clock, and ghost operator with its measure and contour. Verify the relevant principal symbol and show which power terms survive subtraction. For a projected kernel with a local constant term $k_0$ and bounded $O(s)$ remainder, the dyadic integral $B(\sigma)=\int_\sigma^{2\sigma}k(s)\,ds/s$ approaches $k_0\log 2$. This links the band diagnostic to the logarithmic divergence only after lower powers, operator mixing, and reference terms are controlled. The exact relation $\partial_{\log\sigma}B=k(2\sigma)-k(\sigma)$ gives a check on the running from endpoint traces without a time quadrature. Check the projected kernel directly at shared proper times and check the analytic coefficient against held-out regulated data. The standard Laplace-type result provides a benchmark. [Vassilevich, heat-kernel expansion and one-loop divergences](https://arxiv.org/abs/hep-th/0306138)

🟢 [Done] Evaluated the restored mixed kernel before integration in [mixed_kernel_endpoints.py](experiments/mixed_kernel_endpoints.py). Overlapping bands agree at identical proper times, including points recomputed on different production grids. At $s=0.015$ the measured Ricci–clock ratio $k(s,q)/(sq^2)$ ranges from $-0.0033184$ to $-0.0032992$ over the four momenta. This motivates testing a short-time, finite-momentum correction proportional to $sq^2$. It does not determine the local constant.

The exact endpoint derivative of the shortest band, extrapolated in momentum, is $1.464\times10^{-7}$ with three waves and $2.763\times10^{-9}$ with four. In the longest band it is $1.996\times10^{-7}$ and $-3.285\times10^{-7}$, respectively. Thus strong momentum-model sensitivity is present even before time quadrature. The shortest-band endpoint changes propagated from substituting the refined rows are at most $1.101\times10^{-9}$ in the four-wave projection.

On a periodic smooth background, integration by parts relates $\int R_{\mu\nu}\nabla^\mu T\nabla^\nu T$ to $\int[(\Box T)^2-(\nabla_\mu\nabla_\nu T)^2]$. Fix the bulk basis and track the associated total derivative separately on the replica geometry.

🟢 [Done] Checked the independent bulk basis $(RX,R_{\mu\nu}T^\mu T^\nu,(\Box T)^2)$ for the constant-winding conformal probes in [mixed_invariant_rank.py](experiments/mixed_invariant_rank.py). Normalized by the integrated squared conformal gradient and the squared winding, the parallel and transverse rows are $(-6,0,4)$ and $(-6,-2,0)$. Their null direction is $(2,-6,3)$. The flat clock wave adds the independent row $(0,0,1)$ after its own normalization, giving determinant $12$. If its coefficient is $c_{\Box}$, the two curved-only projections give $c_{RX}-2c_{\Box}/3$ and $c_{\rm Ric}+2c_{\Box}$. The existing flat-wave continuum form factor has zero $q^2$ coefficient in the specified gauge and starts at $-sq^4/60$ after the homogeneous subtraction. This controls the flat bulk combination for that operator. The full mixed short-time coefficient and the replica total derivative remain open.

🟢 [Done] Implemented the transverse physical-period comparison using the same momentum polynomial with rescaled Gaussian moments. Fractional-momentum insertions agree with the rescaled polynomial in both orientations. At fixed $L_x=3$, $q=2\pi/3$, and 41 longitudinal points, changing all three transverse periods from $1.8$ to $2.4$ changes the Ricci–clock endpoint by $-4.272\times10^{-17}$ at $s=0.015$ and by $+3.351\times10^{-7}$ at $s=0.048$. The $RX$ change at $s=0.048$ is $+3.916\times10^{-6}$. The cap tests at both periods agree to floating-point precision at these endpoints. The original-period traces reproduce the production checkpoints. This measures a finite transverse-volume effect in the longer-time data at the tested wave. An all-wave infinite-volume extrapolation is still needed.

### Transverse continuum at fixed longitudinal momentum

🟢 [Done] Added the analytic Gaussian moments and [mixed_transverse_continuum.py](experiments/mixed_transverse_continuum.py). For dimensionless transverse momentum $p=k_\perp/w$ with $w=2\pi/1.8$, the one-dimensional moments are $\Gamma(j+1/2)/(sw^2)^{j+1/2}$. Products and binomial expansions generate the two- and three-dimensional moments of the same polynomial used in the periodic trace. A periodic sum with common transverse period $P$ is multiplied by $(1.8/P)^3$ before comparing to the integral. The periodic comparison restores the global sector, whose isolated contribution per transverse volume vanishes in the continuum. Independent one-dimensional quadrature and normalized periodic Gaussian moments verify the formula.

🟢 [Done] Verified all four waves and four bands in both orientations at transverse periods $1.8$, $2.4$, $3.6$, and $4.8$. The maximum projected Ricci–clock pointwise discrepancies from the transverse continuum, over all waves and time nodes, are $3.387\times10^{-7}$, $2.037\times10^{-12}$, $2.353\times10^{-16}$, and $2.819\times10^{-16}$, respectively. The cap pairs agree at each period. The continuum longitudinal grid comparisons and 9-to-17-node quadrature checks pass. Reproduce the fit with `mixed_transverse_continuum.py --analyse` and the production checkpoint directory.

| Cutoff fit degree | Four-wave transverse-continuum $RX$ intercept | Four-wave finite-period Ricci–clock intercept | Four-wave transverse-continuum Ricci–clock intercept | Observed Ricci–clock refinement variation |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 7.315758e-4 | +3.167e-8 | -5.915e-9 | 9.865e-11 |
| 2 | 7.315580e-4 | -1.553e-7 | +5.681e-9 | 5.591e-10 |
| 3 | 7.315785e-4 | +5.073e-7 | -2.876e-9 | 2.534e-9 |

The transverse continuum removes the large negative long-band endpoint running seen at period $1.8$. For the four-wave projection on $[0.024,0.048]$ it changes from $-3.285\times10^{-7}$ to $+1.847\times10^{-8}$. After transverse decompactification, the shortest-band Ricci–clock holdout residual is $-1.965\times10^{-10}$ with observed variation $4.536\times10^{-11}$. The remaining cutoff-fit spread and the disagreement of the three- and four-wave extrapolations preclude a matched Ricci–clock coefficient. The $RX$ value near $7.316\times10^{-4}$ is a stable scale in this diagnostic.

### Matched longitudinal boxes in the transverse continuum

🟢 [Done] Added a matched-box mode to [mixed_transverse_continuum.py](experiments/mixed_transverse_continuum.py). It holds the physical momentum fixed when changing from the fundamental in $L_x=1.8$ or $3.6$ to harmonic two in $L_x=3.6$ or $7.2$. It uses the same transverse continuum, 17-node proper-time grids, and four bands in both boxes. The analysis replaces the two matched rows of the four-wave fit without changing its momenta, and reports the separate contribution of each replacement to the cutoff intercept.

🟢 [Done] Added a radial integration path for matched-box traces. The response quadratic in the winding direction has scalar and rank-two dependence under transverse rotations. For a transverse winding the angular average is obtained at $p_t^2=|p|^2/3$. Four radial samples determine the cubic in $|p|^2$, and an independent angular check uses the axial and perpendicular probes. On a test grid in the doubled box the radial and full Gaussian integration paths agree within $8.0\times10^{-13}$ in both orientations.

🟢 [Done] At the highest physical momentum $q=2\pi/1.8$, both orientations in the doubled box pass the 49-to-57 lattice and 9-to-17-node quadrature checks in all four bands. The Ricci–clock integrated difference $L_x=3.6$ minus $L_x=1.8$ grows from $8.780\times10^{-15}$ at $\sigma=0.015$ to $2.307\times10^{-10}$ at $\sigma=0.024$. At the longer band the separate-box refinement variation is $1.667\times10^{-14}$. The change at this fixed physical momentum is a longitudinal finite-volume effect. Substituting the highest-wave row changes the quadratic cutoff intercept by $-4.232\times10^{-10}$.

🟢 [Done] At the lowest physical momentum $q=2\pi/3.6$, both orientations pass the band checks in the doubled box. The longer bands use the 73-to-81 lattice comparison, and the two shorter bands use 81-to-89. At $\sigma=0.015$ the Ricci–clock band difference $L_x=7.2$ minus $L_x=3.6$ is $-2.845\times10^{-10}$ with a separate-box refinement variation of $1.031\times10^{-8}$. In all four bands the difference is below the observed refinement variation. The tested resolution therefore leaves the magnitude of the low-momentum longitudinal finite-volume effect unresolved.

🟢 [Done] Refit the four waves and four bands with both matched-wave substitutions. The Ricci–clock linear, quadratic, and cubic cutoff intercepts are $-1.073\times10^{-8}$, $-2.163\times10^{-8}$, and $-1.301\times10^{-7}$. The corresponding propagated observed variations are $1.835\times10^{-7}$, $1.102\times10^{-6}$, and $5.652\times10^{-6}$. For the quadratic fit, the highest- and lowest-wave substitutions change the intercept by $-4.232\times10^{-10}$ and $-2.689\times10^{-8}$ respectively. The stronger influence of the lowest wave comes with larger longitudinal grid sensitivity. Reproduce using `mixed_transverse_continuum.py --analyse --matched` with the production checkpoint directory.

### Independent local expansion of the mixed operator

🟢 [Done] Implemented [mixed_local_expansion.py](experiments/mixed_local_expansion.py). The calculation starts from the gauge-fixed metric–clock Fourier vertices with the trace contour already applied. The mixed insertion takes two winding derivatives. In this gauge the ghost acts on the metric gauge condition and its winding derivative vanishes. The field normalization depends on the metric, so its Jacobian also has no winding derivative in this calculation.

A vertex at winding degree $w$ is homogeneous of degree $2-w$ in the input momentum and the probe wave number. The driver reconstructs these local polynomials from operator matrix elements and checks them at a separate momentum and wave number. At curvature degree two a closed path from a given input momentum visits only that momentum and the neighboring transfers $\pm q$. The flat $e^{-p^2}$ factor is removed after scaling the loop momenta by $\sqrt{s}$. Expanding the remaining matrix exponential in the two amplitudes and the scaled probe wave number gives finite polynomials that are integrated by Hermite and generalized Laguerre moments over the fully decompactified loop momenta. The homogeneous mixed coefficient reproduces the flat $X$ subtraction.

For $z=sq^2$ the projected $RX$ kernel starts at $1.0554289963\times10^{-3}$, consistent with $1/(96\pi^2)$ in the Euclidean action normalization. The Ricci–clock kernel has zero constant at the evaluated precision and starts at $-0.0033246013383z+0.0001356980138z^2+0.0000194751779z^3$. The constant dyadic-band values are approximately $(7.31567633\times10^{-4},0)$. These numbers are obtained without fitting the production bands. The cubic prediction reduces the maximum Ricci–clock band residual on the highest wave from $9.538\times10^{-4}$ for a constant to $9.335\times10^{-8}$. At the lowest wave its maximum residual is $3.754\times10^{-10}$.

🟢 [Done] Extended the independently derived series to $z^5$ using the probe expansion through $q^{12}$. In the Ricci–clock projection the extra coefficients are $-3.54094144\times10^{-6}z^4$ and $+3.10820852\times10^{-7}z^5$. The constant is stable under the change of expansion order and the independent Gaussian rules, with a Ricci–clock value of $-1.04\times10^{-17}$ in the kernel at the higher order. Against the production data, the maximum Ricci–clock band residual decreases to $3.537\times10^{-10}$ at the highest wave and $3.571\times10^{-14}$ at the lowest. Over all sixteen band and momentum combinations, subtracting the derived nonconstant terms gives an $RX$ band constant in $[7.31567634,7.31569432]\times10^{-4}$ and a Ricci–clock band constant in $[-3.537\times10^{-10},-5.409\times10^{-15}]$. This residual range combines the finite longitudinal volume, truncation of the local series, and numerical effects.

🟢 [Done] Refined the lowest-wave doubled box at $L_x=7.2$ with 97 longitudinal points in the shortest band. The 89-to-97 comparison passes in both orientations. The separate-box Ricci–clock refinement variation decreases from $1.031\times10^{-8}$ to $2.831\times10^{-10}$. The new box difference is $-5.138\times10^{-12}$, and the 97-point residual against the independently derived $z^5$ series is $-5.174\times10^{-12}$. The box difference remains below the observed refinement variation. Substituting both matched waves gives conventional linear, quadratic, and cubic cutoff intercepts $-5.906\times10^{-9}$, $+5.687\times10^{-9}$, and $-7.258\times10^{-9}$. This extrapolation still depends on the fit degree. The directly derived local mixed coefficient and the freely fitted intercept measure different levels of control of finite-momentum terms.

### Independent pure-curvature matching and a local sphere benchmark

🟢 [Done] Extended the independent expansion to the conformal and shear probes in [pure_local_expansion.py](experiments/pure_local_expansion.py). At second amplitude order the local trace contains the diagonal second derivative and a pair of first derivatives linked by the flat heat divided difference. For input longitudinal momentum $k$, the shifted contribution has the weight $\int_0^1 du\,e^{-u(2k\delta q+q^2)}$ for $\delta=\pm1$ after extracting the flat Gaussian. The two metric–clock and ghost traces are evaluated separately and combined as $K_{bb}^{\rm boson}-2K_{bb}^{\rm ghost}$, with the two real Fourier phases divided out. The independent Gaussian rules reproduce the conformal volume term $24/(16\pi^2)$ at scaled time one and zero for the volume-preserving shear. Subtract the volume term and isolate the $q^2$ Einstein term before comparing $q^4$ responses.

In the action integrand with measure $ds/s$, the local Einstein coefficient is $15/(64\pi^2s)$, and the scalar-squared and Ricci-squared logarithmic coefficients are consistent numerically with $-1/(1280\pi^2)$ and $-43/(1920\pi^2)$, respectively. These are in the action normalization of the production traces and the bulk basis modulo the Euler density. The Einstein coefficients inferred from the two orientations agree. The two periodic probes leave the Euler coefficient unidentified.

🟢 [Done] Validated both probes at two physical wave numbers and all four proper-time bands with analytic transverse continuum moments. The longitudinal pairs are 53-to-57 points and, for the shortest band, 57-to-65. All pass the pointwise trace and 9-to-17-node quadrature checks. The independently derived Einstein kernel is subtracted before quadrature to keep its integration error out of the $q^4$ comparison. The band residual of the independent expansion through $q^{10}$ is smaller than the observed longitudinal-plus-quadrature variation in each row. For harmonic two at $\sigma=0.024$, the two-probe scalar-squared estimate after removing the independent higher terms is $-7.91552\times10^{-5}$, compared with the directly derived $-7.91572\times10^{-5}$.

🟢 [Done] Added a flat CFT control with the same matched local band action in [matched_pure_ball.py](experiments/matched_pure_ball.py). Write $A,B,D$ for its $R,R^2,\mathrm{Ricci}^2$ coefficients. For a flat reference sphere its curvature-derivative entropy and first-order generalized-volume variation are

$$
S_{\rm Wald}=4\pi\int_{\partial B}(A+2BR+D[-R_{uu}+R_{nn}])\,dA,
\qquad
\delta W=\delta V+A^{-1}\int_B[3B\,\delta R+(D/2)(\delta R-2\delta R_{uu})],dV_0.
$$

The standard local smooth-cone Ricci term adds $-2\pi D\int k^2dA$ to the entropy for this static slice. Shift $W$ by the corresponding surface term with linear variation $r\delta S_{\rm cone-Wald}/(8\pi A)$. The code verifies the resulting fixed-$W$ entropy equals the Wald-pair result and agrees with the Weyl representative with topologically completed Euler term. This is a local conical completion. It does not specify the microscopic clock and ghost sewing. [Fursaev, Patrushev, and Solodukhin, squashed cones](https://arxiv.org/abs/1306.4000) · [Bueno et al., paired entropy and volume ambiguities](https://arxiv.org/abs/1612.04374)

Use the static cosine Fourier component from the difference of the two improved-scalar standing-wave preparations with opposite relative phases. Its density amplitude, per inverse normalization volume, is $2q/3$. Conservation and tracelessness give zero longitudinal pressure and transverse pressures equal to half the density. The constraint solution has $\Phi=2\Psi$ and $\Psi_0=\rho_0/(-4Aq^2+4Dq^4)$. The linearized trace and momentum constraints vanish for this profile. Integrate the independently fixed flat-vacuum CFT modular kernel on the ball. For normalized $q=0.8$ the separate $r^4$ coefficients from the Einstein term, the fixed-$W$ Ricci term, and the state are $-2.80378858$, $-0.00356556$, and $+2.80735414$. Their analytic sum is zero, and the four-radius quadrature has maximum absolute residual divided by $r^4$ below $5\times10^{-12}$. This test uses the matched local action as a continuum effective action. It does not evaluate a finite-band microscopic replica trace at these radii. [Casini, Huerta, and Myers, flat CFT ball modular kernel](https://arxiv.org/abs/1102.0440)

For the active clock, the matched smooth $\lambda RX$ term adds $4\pi\lambda\int_{\partial B}X\,dA$ to the curvature derivative and $3\lambda/(2A)\int_B X\,dV$ to the local volume functional at the Einstein reference normalization. The same action contributes $\lambda[XG_{\mu\nu}+(g_{\mu\nu}\Box-\nabla_\mu\nabla_\nu)X+R\nabla_\mu T\nabla_\nu T]$ to the metric variation and $-2\lambda\nabla_\mu(R\nabla^\mu T)$ to the clock variation for $X=(\nabla T)^2$. These smooth variations specify inputs to the physical constraint solve. The local flat CFT test does not involve those active-clock sources or their canonical state response.

🟠 [Next] For the physical clock-aligned sphere, derive the replica total derivatives, boundary and finite renormalization data, and the reduced clock state response in the same regulator. The local flat CFT cancellation leaves the physical preferred-clock $r^4$ test open.

🟠 [Next] Before a physical sphere subtraction, match the counterterms and finite renormalization conditions independently. Derive the generalized volume, boundary terms, constraint response, and state response from the same action and regulator. Preserve the hierarchy $a\ll\sqrt{s}\ll r$ in the renormalized small-ball comparison and demand an independently measured nonzero $r^4$ signal in at least one on-shell test. The causal-diamond identity on a maximally symmetric reference is a benchmark. Applying it to a reference with a preferred clock requires checking the background symmetry and clock contributions. [Bueno et al., higher-order entanglement equilibrium](https://arxiv.org/abs/1612.04374)

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

### Follow-up for the disjoint-slab calculation

🔴 [Later] Evaluate the branch amplitudes as functions of transverse momentum and compare a two-scale asymptotic expansion with the integrated active-block response. Refine the pure-mode treatment and vary the normal grid, transverse grid, and covariance floor independently. Use the asymptotic amplitudes to test the continuum extrapolation without interpreting disjoint-slab information as a local gravitational entropy coefficient.

## 3. Joint gravitational response in a single model

### Entropy-response filter

For the coupled clock–gravity candidate, use the regional algebra and normalized trace tested in the [cut-and-glue calculation](#implementation-order-and-decision-criteria). The vacuum Einstein composition test calibrates the boundary prescription. The microscopic candidate must also satisfy the entropy and geometric response criteria below.

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
