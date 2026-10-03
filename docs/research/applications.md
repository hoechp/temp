# Seven application and research proposals

[Agenda](README.md) · [Operations atlas](operations.md) · [Backlog](roadmap.md)

**Version note:** these proposals originate in the 0.2.0 audit. Version 0.3.0
now supplies exact rational coefficients, plane isometries, coupled operators,
Cayley maps, projective charts and derivative-preserving measurements. The
[geometry guide](../unified-geometry.md#most-promising-next-projects) explains
which application steps these enable and what remains to be built.

These proposals start with the union of the three algebras. Representations
are selected afterwards to suit the geometry or computation. “New” below means
new to this project unless explicitly stated otherwise; the underlying physical
models and mathematical constructions have established precedents.

| Candidate | Main connection | Priority and evidence |
| --- | --- | --- |
| 1. Optical circuits and two-mode operators | Phase + hyperbolic gain + mode mixing + infinitesimal variation | Highest near-term engineering payoff; operator identity derived and checked |
| 2. Dynamics through critical damping | Circular, hyperbolic and dual behaviour as three regimes of one equation | Best algebraic flagship; regular transition formula derived and checked |
| 3. Geometry and transformation laboratory | Angles, metrics, conics and fractional transformations across C/S/D | Closest to the original geometric ambition; individual ingredients established |
| 4. Root families and branch continuation | Algebraic equations + topology + tangent geometry | Highest direct contribution to mathematical completeness |
| 5. Calibration and motion optimization | Geometric models + Jacobians + higher-order jets | Strong practical follow-up to the existing robot demo |
| 6. Waves, circuits and spectral inverse problems | Propagation + response functions + differentiable measurements | Broad practical reach; requires array and solver infrastructure |
| 7. Exact deformation and modular lifting | Integer arithmetic + polynomial derivatives + CRT | Strongest connection to the original discrete-mathematics scope |

## 1. Differentiable two-mode optics and operators

**Question:** can phase shifts, attenuation, mixing, measurement and calibration
share one ultracomplex expression pipeline?

C represents optical phase. S separates modes and represents reciprocal gain
or attenuation through `exp(j*eta)`. D transports variations in path length,
plate thickness, angle or coupling. The existing interference demo uses some
of these ingredients, but does not yet provide a reusable circuit/operator API.

Let `sigma(X)=X.conjugate("j")`. For complex-dual coefficients a,b,c,d, define

$$\alpha=ap_+ +dp_-,\qquad \beta=bp_+ +cp_-,\qquad
T(X)=\alpha X+\beta\sigma(X).$$

In idempotent coordinates this is exactly

$$\begin{pmatrix}X_+\\X_-\end{pmatrix}\mapsto
\begin{pmatrix}a&b\\c&d\end{pmatrix}
\begin{pmatrix}X_+\\X_-\end{pmatrix}.$$

The swap already exists; the proposed feature is a first-class operator type
with correct composition and basis conventions. Composition obeys

$$(\alpha,\beta)\circ(\gamma,\delta)=
(\alpha\gamma+\beta\sigma(\delta),\;
\alpha\delta+\beta\sigma(\gamma)).$$

This is the algebra of 2 × 2 matrices over complex dual numbers, with **16 real
parameters**. Its state still has eight real coordinates. Scalar Ultra remains
commutative; these operators generally do not commute. In particular, swapping
modes and multiplying by j anticommute. This is an actual extension of what
scalar multiplication alone can express, constructed from existing operations.

A further connection unifies the three base behaviours *inside the operator
layer*. Write S for the swap and J for multiplication by j. Then

$$S^2=J^2=1,\quad SJ=-JS,\quad (JS)^2=-1,\quad (J+JS)^2=0.$$

Thus operator exponentials can generate a circular rotation, a hyperbolic
squeeze and a nonzero parabolic shear in the same retained representation.
Here the nilpotent **operator** describes a geometric shear; the independent
scalar epsilon can still describe its parameter sensitivity. The two meanings
of “dual” need not compete for the same storage role.

For coherent recombination, already valid with today's API,

```python
amplitude = X + X.conjugate("j")
intensity = amplitude * amplitude.conjugate("i")
```

Both channels then contain the same summed amplitude and its derivative,
followed by the intensity and its derivative. In contrast, multiplying X by
its i-conjugate *before* summing produces separate mode intensities; it omits
the coherent interference cross term. That distinction deserves an explicit
measurement API.

**Demo:** a Mach–Zehnder interferometer with two beam splitters, an adjustable
phase plate and differential attenuation. Show both complex fields, output
intensities and path-length sensitivities. Fit a path offset and loss parameter
from synthetic measurements; reveal indistinguishable parameter combinations.
For an ideal balanced, lossless convention, verify complementary port powers
`cos²(phi/2)` and `sin²(phi/2)` and derivatives `∓sin(phi)/2`.

**Missing:** G04–G07, G12. **Acceptance:** agreement with direct complex Jones
matrices; correct ordering of noncommuting components; lossless power
conservation; gradients against independent formulas; noisy-fit residuals and
parameter identifiability. Polarization optics supplies another direct use of
the same operators (R7). The established Jones/Lorentz connection (R8) makes
the bridge between circular phase and hyperbolic attenuation particularly
interesting. Physical gains, losses and normalization must be specified.

**Research question:** does the unified expression and derivative API reduce
modelling errors or improve usability versus ordinary complex matrices plus
AD? No speed advantage has yet been measured. Two interacting modes also use
the two state channels, so they cannot simultaneously represent two independent
whole-circuit scenarios without another batch axis.

## 2. One oscillator through all three algebraic regimes

**Question:** can one numerically stable formula cover oscillation, exponential
relaxation and critical damping, including derivatives through the transition?

For `x''+2*gamma*x'+omega0²*x=0`, let

$$M=\begin{pmatrix}0&1\\-\omega_0^2&-2\gamma\end{pmatrix},\qquad
B=M+\gamma I_2,\qquad B^2=\kappa I_2,\quad
\kappa=\gamma^2-\omega_0^2.$$

Using the [generalized functions](operations.md#6-a-continuous-elliptichyperbolicparabolic-calculus),

$$e^{tM}=e^{-\gamma t}\bigl(C_\kappa(t)I_2+S_\kappa(t)B\bigr).$$

- **Complex regime:** `kappa<0`, damped circular oscillation.
- **Split regime:** `kappa>0`, two real exponential modes.
- **Dual regime:** `kappa=0`, a nonzero square-zero B and the critical factor
  `I+t*B` (assuming `omega0>0`).
- **Union:** one functional calculus for these behaviours, with Ultra-valued
  parameters available to compare settings and transport their variations.

At critical damping the response is smooth, even though separate eigenvalue
derivatives and naive square-root formulas can become singular. The series in
kappa retain finite derivatives. Preserve the matrix or quadratic generator;
do not use `M2R`, which canonicalizes away information needed for composition.

**Demo:** move a damping slider through the critical point. Show displacement,
the phase portrait, eigenvalues and the derivative of settling behaviour.
Fit damping from synthetic trajectories on both sides of the transition.
Use fixed-time trajectory objectives first; settling-time thresholds introduce
event and differentiability questions of their own.

**Missing:** G06, G10–G12. **Acceptance:** independent matrix-exponential and ODE
oracles; exact critical solution; continuity of response and its parameter
derivatives; a sweep through `kappa=0` with no artificial epsilon snapping;
stress tests for long-time overflow and cancellation. R9 describes the physical
oscillator; the proposed stable parameter calculus is the project's design.

**Extensions:** RLC transients, paraxial optical transfer, repeated poles in
control, and propagation/evanescence near a waveguide cutoff. Different media
or successive optical elements need matrices retaining their bases; a single
commuting scalar cannot represent arbitrary ordered compositions.

## 3. A unified geometry and transformation laboratory

**Question:** how much of circular, Lorentzian and Galilean geometry can share
an API without erasing their different meanings of length and angle?

Start with `u²=sigma` for `sigma=-1,+1,0` and the faithful real matrices

$$a+bu\longleftrightarrow
\begin{pmatrix}a&\sigma b\\b&a\end{pmatrix}.$$

The quadratic form is `a²−sigma*b²`. The exponential generates rotation,
hyperbolic squeeze or shear. A common algebraic expression produces visibly
different orbits and invariants. Pairing this with the ordinary analytic cosine
comparison makes clear why its conics reverse the circular/hyperbolic roles.

Then add fractional transformations

$$z\mapsto(az+b)(cz+d)^{-1},$$

with explicit coefficient domains and unit denominators. Real-coefficient
SL(2,R) actions provide a common comparison across C/S/D; R3 studies this
elliptic/parabolic/hyperbolic programme. Ultra coefficients can carry deformed
transformations and combine the subalgebras in one calculation.

**Demo:** a linked canvas displaying the same construction in all three
geometries: a point orbit, two rays and their relative parameter, a preserved
quadratic form, and the transformed conic. Add a full-Ultra inspector showing
mixed coefficients. Let a user compare `i*j`, `eps*i` and `eps*j` rather than
restricting every experiment to one plane. Possible exercises include velocity
addition `tanh(eta1+eta2)`, phase addition and composition of infinitesimal
shears, with their domains visible.

**Missing:** G03, G07, G12, G17. **Acceptance:** preserve the appropriate
invariants; test sector changes and null directions; agree with faithful matrix
representations; distinguish geometric quantities from numerical display axes.
Do not label every dual shear as a Euclidean translation in the original plane.

**Deeper research:** a projective completion that treats affine singularities
as changes of chart where possible. Over a ring with zero divisors, projective
points require unimodular pairs, not just arbitrary nonzero coordinate pairs;
some apparent singularities are genuine obstructions. A richer parabolic-angle
definition would be a new explicit geometry API, not a silent replacement of
the existing epsilon exponential. Practical uses include geometry education,
coordinate-system debugging, transformation design and local kinematic models.

## 4. Complete root families, monodromy and implicit sensitivity

**Question:** can the library turn multiple roots, missing roots and branches
into inspectable mathematical objects?

Complex analysis supplies roots and windings; S lets independent branch choices
coexist; D exposes the tangent condition at a root. For
`P=P0+eps*P1`, a channel root `u+eps*v` obeys

$$P_0(u)=0,\qquad P_0'(u)v+P_1(u)=0.$$

This explains three qualitatively different results: a unique tangent at a
simple root, a free tangent at a compatible repeated root, or no lifted root
when the tangent equation is inconsistent. It also explains why `Y²=eps` has
no solution even though the body equation has a root.

**Demo:** continue `Y³=X` along a loop whose plus body winds around zero while
the minus body remains fixed. Show all nine roots of a unit, how one loop
permutes three plus branches, and how three loops restore them. Then approach
zero and display divergent root sensitivities, continuous root families or
inconsistency instead of inventing a finite derivative.

**Missing:** G08–G10. **Acceptance:** complete discrete/family classification;
residuals for sampled family parameters; independent branch winding counts;
no global claims based on a local principal function. For general polynomial
coefficients, report when a body polynomial drops degree or vanishes identically.

**Applications:** tracking dispersion branches, resonances, polynomial
constraints, bifurcation education and differentiating equilibria. The tangent
equation is also the finite-dimensional implicit-function formula. At a
singular Jacobian, ordinary implicit differentiation is not automatically valid;
continuation may need a different parameterization.

## 5. Robot calibration, geometric fitting and higher-order jets

The existing planar robot demo already differentiates two joint angles and
tracks a curve. Repeating it with more targets adds little mathematical scope.
The useful next problem is **calibration**: infer link lengths, joint offsets
and sensor bias jointly from noisy observations, then optimize a trajectory.

C expresses position and heading, D gives variations, and S can either compare
two configurations or carry two derivative directions at a common body.
Metric-aware residuals can connect rotational errors and positional errors
without treating their units as interchangeable. This also links planar
kinematics to the angle and line-geometry APIs.

For genuine automatic second derivatives, introduce an independent eta:

$$\varepsilon^2=\eta^2=0,\quad\varepsilon\eta\ne0,\qquad
f(x+\varepsilon u+\eta v)=f(x)+\varepsilon Df[u]+
\eta Df[v]+\varepsilon\eta D^2f[u,v].$$

Retaining all of A and adjoining eta has 16 real dimensions. Alternatively,
`C[eps,eta]/(eps²,eta²)` has eight real dimensions but replaces the split
factor and therefore is a **different algebra**. A Taylor-jet backend can
support higher orders. None of these should silently alter Ultra's relations.
R5 provides an established hyper-dual implementation precedent.

**Missing:** G04, G07, G10–G11, G13. **Acceptance:** recover identifiable
calibration parameters; report Jacobian rank and covariance approximation;
compare Jacobians and Hessian-vector products against analytic or independent
AD results; demonstrate what second derivatives improve over Gauss–Newton.
For full 3D pose use matrices or a suitable noncommutative geometry library,
with Ultra/jet-valued parameters for sensitivity. Do not claim scalar Ultra
multiplication composes arbitrary rigid poses.

## 6. Waves, circuits and spectral inverse problems

**Question:** can one response-and-measurement interface serve travelling
waves, resonant circuits and filter design?

C supplies oscillatory phase, S distinguishes propagation characteristics or
modal coordinates, and D supplies parameter variation. Existing wave packets
and scalar interference make this a grounded extension rather than an empty
application list.

Examples include a transfer function `H(omega,theta)`, its phase delay and its
parameter derivatives; a discretized linear wave problem with

$$K(\theta)u=b(\theta),\qquad
K\,u_\theta=b_\theta-K_\theta u;$$

and spectral convolution where bodies and tangents undergo the same FFT.
Two frequencies, scenarios or modes can occupy the split structure, but a
spatial field and a broad spectrum still require arrays.

**Demo:** reconstruct a propagation speed and attenuation from complex receiver
signals at multiple frequencies. Compare amplitude-only, phase-only and joint
fits to expose ambiguous measurements. Use explicit phase unwrapping, then
test a model near a response zero where phase is undefined. A second version
could fit component values of an RLC filter from the same style of data.

**Missing:** G04–G07, G10–G11, G14. **Acceptance:** correct boundary conditions,
independent forward-model checks, noise-aware residuals, gradient checks and
identifiability. Compare computation and memory with direct complex arrays and
forward/reverse AD; a convenient scalar API alone is not a performance result.
The known relation between complex holomorphy and harmonic functions, and split
holomorphy and the wave equation, offers a companion mathematical visualization.

## 7. Exact arithmetic: dual deformation meets Hensel lifting

**Question:** can the integer and modular modules share the same polynomial
linearization machinery as the geometric and numerical core?

For an integer polynomial and a prime p,

$$f(a+pt)\equiv f(a)+pt f'(a)\pmod{p^2}.$$

Given a root a modulo p with `f'(a)` invertible modulo p, the linear correction
determines its unique lift modulo p². This is the same first-order Taylor
mechanism that controls a dual root (R10). It links discrete divisibility and
continuous-looking tangent algebra in an exact, concrete example.

**Do not identify the rings:** Z/p²Z and Fp[eps]/eps² have different
characteristics. The shared mechanism is a square-zero correction ideal and
linearization; p is not literally an independent epsilon over Fp in Z/p²Z.

The split factor gives a second connection through CRT. Over an odd prime,
`p±=(1±j)/2` decomposes the j part. For `p=1 mod 4`, the i factor splits too;
for `p=3 mod 4`, it remains a quadratic field extension. At `p=2`, both
factorizations change character and require separate handling.

**Demo:** show root-lifting trees with unique, absent and branching lifts next
to the analogous dual root cases. Then show the full multiplication structure
over small primes and compare it with exact rational calculations. A first
example is `f(x)=x²−2`, root 3 modulo 7, lifting to root 10 modulo 49.

**Missing:** G01, G08–G09, G15–G16. **Acceptance:** exact residuals modulo p^k;
explicit coefficient domains; checks at p=2 and at singular derivatives;
agreement with an independent computer algebra system. This is a promising
research/education module and exact verification tool, not evidence of a new
cryptographic primitive or faster factoring.
