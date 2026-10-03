# Applications worth pursuing

[Agenda](README.md) · [Operations](operations.md) · [Roadmap](roadmap.md) · [Implemented showcase](../gallery/README.md)

The ranking favors exact coefficients and geometry, followed by applications giving the three algebras clear shared roles. Projects below are proposals unless identified as implemented examples. Accuracy, speed and usability advantages must be tested against appropriate baselines.

## Candidate comparison

| Priority | Application | Combined contribution | Starting point | Main missing capability |
| --- | --- | --- | --- | --- |
| 1 | Exact geometric constraints/calibration | C rotations, S alternate geometric forms, D variations | Exact predicates, Cayley isometries, matrices, curves | Constraint graph, implicit derivatives, rank events, algebraic coordinates |
| 2 | Higher derivatives of geometry and thermodynamic potentials | `i` and `ij` probe curvature; epsilon adds parameter differentiation | Corrected exponential and polynomial calculus | Stable mixed-component primitives and derivative API |
| 3 | Structure-preserving critical dynamics | Circular, hyperbolic, parabolic generators plus rational invariants and dual sensitivity | Exact Cayley operators | Continuous functions, time-step control, matrix Fréchet derivatives |
| 4 | Optical/wave transfer networks | C phase, S direction/flux structure, D material/geometry derivatives | Mode operators, projectivities, observables | Physical components, scattering composition, conditioning |
| 5 | Projective continuation and Riccati models | C/S/D fractional maps and tangent data in mixed charts | Möbius maps, unimodular points, cross ratios | Automatic charts, path events, incidence geometry |
| 6 | Frequency-domain identification | Complex response, split modes, dual derivatives | Interference fit and coupled motion | Arrays, response blocks, noise/uncertainty and passivity models |
| 7 | Finite coefficients and polynomial lifting | Field-specific C/S factors and nilpotents | Scalar residues, exact polynomials, exhaustive F2 probe | Modular backend, Hensel/Hasse, reconstruction |

## Exact constraints: geometry that remains auditable

A linkage/CAD constraint can use rational points, quadrances and Cayley parameters. Dual seeds give an exact rational Jacobian. Exact rank distinguishes regular and singular configurations without a tolerance. The current planar robot demo is a numerical baseline, not an exact constraint engine.

**First deliverable:** a closed linkage represented by a constraint graph. Compute exact residuals, Jacobians and admissible infinitesimal motions at rational configurations. Check regular and singular cases against independent geometry.

Circular joints, indefinite constraints and shear/deformation variables can share construction and differentiation. Every physical robot need not use all three. Generic circle intersections require irrational coordinates: retain constraints implicitly or introduce a scoped algebraic-number domain. At a singular configuration, an infinitesimal motion need not integrate into a finite motion.

## Higher derivatives: geometry meets thermodynamic response

CS is bicomplex: `i` and `ij` commute and both square to minus one. Mixed steps expose second derivatives if elementary algorithms preserve the small component. Epsilon differentiates that probe with respect to an additional parameter.

This connects geometric curvature/calibration Hessians to **thermodynamic potentials**: derivatives relate pressure, response and material sensitivity. Deiters and Bell document established multicomplex methods in thermodynamics [R4](references.md). The proposal here is an application of the existing union and exact polynomial models, not a claim of a new differentiation method.

**First deliverable:** a bounded analytic potential with one mixed Hessian entry and its parameter derivative, checked against symbolic formulas and independent high precision over step sizes. Report requested-coefficient errors.

Division, logarithm and other primitives need the same care as the corrected exponential. Piecewise branches, absolute values and physical phase transitions invalidate naive analytic-step assumptions. This package currently supplies neither a thermodynamic solver nor a general Hessian API.

## Dynamics across circular, hyperbolic and critical regimes

For `B_kappa=[[0,1],[kappa,0]]`, `B_kappa²=kappa*I`. Entire functions of kappa express the exponential without taking a singular derivative of `sqrt(kappa)` at zero. Exact Cayley maps already cover all three regimes discretely.

**First deliverable:** compare rational midpoint steps with a stable continuous solution and parameter derivatives while crossing kappa zero. Check symplecticity for Hamiltonian generators, chosen quadratic invariants and their differentiated identities. The established midpoint context is documented by Hairer [R5](references.md).

Exact geometry and numerical evolution can share generators and invariants. But invariant preservation does not guarantee trajectory accuracy. Fraction denominators grow; Cayley poles, time-step choice and damping/loss models require explicit handling. General noncommuting perturbations require a Fréchet derivative.

## Optical layers, wave interfaces and impedance

A complex pair can represent forward/backward fields. Interfaces and layers mix them; a component ratio evolves by a Möbius map. Suitable lossless optical transfer models belong to SU(1,1), linking them to Lorentz geometry [R6](references.md). Circular phase, indefinite flux and observable intensity are thus closely connected.

Epsilon carries thickness, refractive-index or frequency sensitivity through a network. Transmission-line impedance and Riccati propagation share this **mathematical pattern**, with different physical meanings and admissibility conditions.

**First deliverable:** a small lossless multilayer or line network with specified conventions. Verify composition, conserved flux, reflection/transmission and derivatives; recover one parameter from synthetic data.

Long stacks and evanescent fields can make transfer matrices ill-conditioned. Provide scattering composition and conversions alongside them. Loss, total internal reflection and normalization affect the relevant metric/group; SU(1,1) is not a universal label. Full 3D Maxwell simulation is outside this first project.

## Projective continuation: a coordinate pole can be traversable

For a matrix `[[a,b],[c,d]]` acting on `(x,y)`, the ratio evolves as `(a*r+b)/(c*r+d)`. Its affine denominator can cease to be a unit while the homogeneous state remains valid. Different split factors may require different charts; `ProjectivePoint` already handles this.

**First deliverable:** continue a parameterized family through an affine pole, preserving homogeneous data and first variations. Compare with the underlying linear evolution and record chart changes separately from physical singularities.

This brings together projective calibration, impedance/Riccati evolution and mode networks. Automatic charts and boundary events are still absent. Non-unimodular homogeneous pairs remain invalid; chart changes cannot repair them.

## Signals, fitting and uncertainty

Extend the current wave/interference examples with explicit response blocks, weighted real residuals and covariance propagation through a Jacobian. Amplitude, phase and power are different observations with different singularities.

**First deliverable:** estimate two identifiable parameters of a small transfer model. Compare derivatives and updates with an independent reference; quantify conditioning under a stated noise model.

Arrays and reusable factorizations are likely essential to performance. Epsilon is a derivative, not a noise distribution. Phase needs zero handling and path unwrapping. Compare equal outputs/accuracy against ordinary complex arrays plus an established AD library before claiming a speed advantage.

## Finite coefficients and exact lifting

Over odd prime fields the algebra's factors depend on whether −1 is a square. Over F2, `i+1`, `j+1` and epsilon are three square-zero generators. The [probe](experiments.md#finite-coefficients) checks all 256 elements.

**First deliverable:** direct-basis modular coefficients, unit detection and serialization; then simple-root Hensel steps with exact lifted residuals. Singular roots and p=2 need separate rules. Hasse derivatives avoid invalid factorial division in positive characteristic.

Uses include modular verification, rational reconstruction and scoped multiplicity-evaluation/coding experiments [R9/R10](references.md). This does not establish a new cryptographic primitive; generic RSA exercises have been separated.

## Additional directions

| Direction | Why it belongs | Remaining work |
| --- | --- | --- |
| Conics, chains and rational curves | C/S/D projective geometry connects exact constructions and transfer diagrams | Incidence definitions, degeneracy and algebraic intersections |
| Lie/Clifford or matrix poses | Spatial mechanisms require noncommuting rotations/translations | A separate representation with explicit laws/dimension; scalar Ultra is not a dual quaternion |
| Bifurcation and repeated modes | Retain a critical generator when eigenvalue coordinates coalesce | Jordan/Schur-aware methods, rank events and conditioning |
| Certified computation | Exact rational constructions supply numerical reference data | Interval/ball arithmetic or independent high precision with error contracts |
| PDE interface methods | Split characteristics naturally combine with complex phase | Boundary operators, discretization accuracy, dispersion and stability |

The testable research question is whether a coherent algebraic interface improves composition, verification or numerical reliability in a specified task. The union does not automatically solve every application.
