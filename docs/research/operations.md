# Operations atlas: three geometries and their combinations

[Agenda](README.md) · [Applications](applications.md) · [Backlog](roadmap.md)

Notation: C = complex, S = split-complex (`Binary`), D = dual, A = `Ultra`.
All exact statements below concern the mathematical algebras; the implementation
uses floating-point coefficients. Domains and branch choices are part of an
operation, not afterthoughts. Source keys refer to [references.md](references.md).

## 1. Arithmetic, division and equations

| Algebra | Distinctive behaviour | Uses |
| --- | --- | --- |
| C | Every nonzero scalar is invertible; multiplication combines scale and rotation | Impedances, transfer functions, phasors, planar similarity maps |
| S | `a+bj` acts independently on `a+b` and `a−b`; null lines contain zero divisors | Left/right characteristics, common/differential modes, Lorentz boosts |
| D | `(a+eps*b)(c+eps*d)=ac+eps*(ad+bc)`; invertible iff `a != 0` | Product and quotient rules, first-order perturbations |
| A | Two complex divisions with differentiated quotients; invertible iff both bodies are nonzero | Two operating points and their sensitivities, symmetric two-mode systems |

**Existing:** all basic arithmetic; `solve` for invertible square systems;
`solution_space` for complete affine solution families, including zero divisors
and rectangular systems. **Missing:** a convenient scalar `solve_product(a,b)`
wrapper for `a*x=b`, channel rank/conditioning diagnostics and reusable
factorizations. Never replace division by an arbitrary representative of a
solution family. For example `eps*x=eps` fixes the body of `x` but leaves its
four real tangent coordinates free in A.

## 2. Exponentials, logarithms, powers and roots

| Algebra | Distinctive behaviour | Uses |
| --- | --- | --- |
| C | Complex logarithm branches; n roots for a nonzero scalar | Phase, frequency response, analytic continuation |
| S | `exp(a+bj)=exp(a)*(cosh(b)+j*sinh(b))`; real log iff `a+b>0` and `a−b>0` | Hyperbolic scaling and multiplicative growth in two channels |
| D | `exp(a+eps*b)=exp(a)*(1+eps*b)`; real log requires `a>0`; root tangents follow the derivative | Growth sensitivity, infinitesimal composition |
| A | Independent complex log branches; n² roots of every unit for positive integer n | Mode-specific branches, continuation and polynomial inverse problems |

For `n>=2`, solving one channel of `Y^n=X` means

$$u^n=z,\qquad n u^{n-1}v=w.$$

If `z != 0`, each of the n complex roots gives a unique tangent. If `z=0,w!=0`,
there is no root. If `z=w=0`, `u=0` and **every complex v** works. Two channels
produce products of discrete roots and continuous families; four real free
parameters are possible. A single principal `sqrt` cannot represent this.

**Existing:** elementary powers, principal square root, independently selected
log branches in A; root sets and rational powers in the closed 2D types.
**Missing:** full A root sets, branch-selectable A powers and a documented
nonunit rational-power policy. Polynomial relations, branch values and local
analytic functions are different contracts. `sqrt(X²)=X` is not universal.
The current large-integer exponent defect is [G01](roadmap.md#p0-correctness-and-semantic-contracts).

## 3. Length, metric, conjugation and normalization

| Algebra | Intrinsic quadratic form | Geometry and use |
| --- | --- | --- |
| C | `a²+b²` | Positive Euclidean length; phase/amplitude decomposition |
| S | `a²−b²` | Indefinite Minkowski metric; nonzero null vectors; spacetime intervals and squeezing |
| D | `a²` | Degenerate form; epsilon directions are invisible to it; tangent geometry |
| A | No unique preferred scalar length; two complex channel amplitudes coexist with a coefficient norm | Choose numerical error metric, channel energy or physical measurement separately |

`abs(Ultra)` is currently the Euclidean norm of **all eight coefficients** and
returns a `float`. This is legitimate for coefficient error measurement. It
does not compute a dual-preserving physical amplitude. `Hypercomplex.dot`,
`.normalized`, `.angle` and `.turned_by` also use Euclidean coordinate geometry,
even on `Binary` and `Dual`; `.euler_angle` has different semantics.

**Needed:** named `coefficient_norm`, `metric_form`, channel `abs2`,
`amplitude`, and explicit normalization policies. The generator conjugations
must remain distinct: `i` conjugates complex values and tangents; `j` swaps
channels; `eps` reverses tangent signs. A determinant that ignores tangents
cannot measure tangent sensitivity or replace an invertibility test.

For a complex dual channel with a real perturbation parameter,

$$|z+\varepsilon w|^2:=|z|^2+
2\varepsilon\operatorname{Re}(\overline z w).$$

This differentiable measurement is already expressible with
`X * X.conjugate("i")` channel by channel. It remains meaningful at `z=0`;
amplitude and phase derivatives need additional restrictions.

## 4. Angles, polar forms and relative orientation

| Algebra | Natural parameter and domain | Uses |
| --- | --- | --- |
| C | `theta=atan2(b,a)`, modulo `2*pi`, undefined at zero | Heading, phase alignment, planar rotation |
| S | `theta=atanh(b/a)` in the positive timelike sector; four sectors require a discrete direction label | Rapidity, velocity composition in 1+1 dimensions, squeeze ratios |
| D | `tau=b/a` for `a!=0`; `a*(1+eps*tau)`; additive shear parameter, not a periodic angle | Galilean shear, local slope and infinitesimal displacement |
| A | Two phases, two log-amplitudes and their tangent changes; no single universal 8D angle | Relative phase and gain, phase-sensitive calibration, two-mode geometry |

For `z!=0` the tangent of log-amplitude is `Re(w/z)` and the tangent of phase
is `Im(w/z)`. A dual-preserving real two-input angle needs

$$d\operatorname{atan2}(y,x)=\frac{x\,dy-y\,dx}{x^2+y^2}.$$

**Existing:** Cartesian/polar conversions, all four split sectors, dual Euler
parameters, 3D angle/vector maps, line dual angles. **Missing:** a common typed
angle result recording geometry, sector, winding and singular status;
dual-preserving `atan2`; relative phase; path unwrapping per channel. Null rays
cannot acquire a finite hyperbolic angle by adding an epsilon-sized tolerance.

The current `geometry.vector_from_angle` provides sphere, hyperboloid and
cylinder parameterizations. They are useful maps, not a proof that their
coordinate parameters form a 3D rotation algebra. Likewise a line's
angle-plus-distance encoding is distinct from a function derivative.

## 5. Trigonometric, hyperbolic and inverse functions

The same analytic function behaves differently from the exponential generated
by each unit. This distinction is central to the original visualization goal.

| Algebra | Ordinary analytic sine and cosine | Unit exponential |
| --- | --- | --- |
| C | `cos(a+ib)=cos(a)cosh(b)−i sin(a)sinh(b)`; `sin(a+ib)=sin(a)cosh(b)+i cos(a)sinh(b)` | `exp(i*t)=cos(t)+i*sin(t)` |
| S | `cos(a+jb)=cos(a)cos(b)−j sin(a)sin(b)`; `sin(a+jb)=sin(a)cos(b)+j cos(a)sin(b)` | `exp(j*t)=cosh(t)+j*sinh(t)` |
| D | `cos(a+eps*b)=cos(a)−eps*b*sin(a)`; `sin(a+eps*b)=sin(a)+eps*b*cos(a)` | `exp(eps*t)=1+eps*t` |
| A | Evaluate two complex trigonometric functions and propagate their two tangents | Combines phase, hyperbolic channel scaling and first-order transport |

Thus, fixing `a=pi/4` and varying `b`, the two coefficients of `cos(a+u*b)`
trace a **hyperbola for C, circle for S, line for D**. The corresponding
`exp(u*t)` picture is **circle, hyperbola, line**. There is no contradiction.
At general fixed a the cosine curves are scaled conics and may degenerate.

Hyperbolic functions reverse the roles again:

$$\cosh(a+ib)=\cosh(a)\cos(b)+i\sinh(a)\sin(b),$$
$$\cosh(a+jb)=\cosh(a)\cosh(b)+j\sinh(a)\sinh(b),\qquad
\cosh(a+\varepsilon b)=\cosh(a)+\varepsilon b\sinh(a).$$

The identities `sin(X)²+cos(X)²=1` and `cosh(X)²−sinh(X)²=1` hold throughout A.
Reciprocal functions need unit denominators, even when the denominator is
nonzero. Inverse trig functions are local branches, not global undo buttons.
The closed S type applies real-domain restrictions in both real channels;
the closed D type additionally needs a finite derivative for nonzero tangents.
A can leave a 2D subalgebra to use a complex branch. See R1–R3.

**Applications:** oscillators and circular kinematics (C), boosts and hyperbolic
trajectories (S), their velocities/Jacobians (D), and phase-sensitive fitting
with two modes (A). **Existing:** all six trig/hyperbolic functions and their
inverses. **Missing:** stable `sinc`, `sinhc`, paired `sincos`, `sinpi/cospi`,
branch continuation and geometry-specific inverse angle functions. More names
alone matter less than stable evaluation and clear domains.

## 6. A continuous elliptic–hyperbolic–parabolic calculus

For a generator or matrix B satisfying `B²=kappa*1`, define entire functions

$$C_\kappa(t)=\sum_{n\ge0}\frac{\kappa^n t^{2n}}{(2n)!},\qquad
S_\kappa(t)=\sum_{n\ge0}\frac{\kappa^n t^{2n+1}}{(2n+1)!}.$$

Then

$$e^{tB}=C_\kappa(t)1+S_\kappa(t)B,\qquad
C_\kappa(t)^2-\kappa S_\kappa(t)^2=1.$$

| Regime | Functions | Applications |
| --- | --- | --- |
| `kappa<0` (complex type) | cosine and scaled sine | Oscillation, propagating waves, stable focus |
| `kappa>0` (split type) | cosh and scaled sinh | Exponential modes, evanescence, saddle dynamics |
| `kappa=0` (dual type if B is nonzero) | `C=1`, `S=t` | Critical damping, a Jordan shear, repeated eigenvalues |
| Combined with A coefficients | Evaluate two parameter regimes and their first variations | Compare two devices; differentiate response across a regime boundary |

The series are analytic in kappa at zero. Consequently
`dC/dkappa=t²/2` and `dS/dkappa=t³/6` there. A naive differentiated square-root
formula obscures this regularity. This is a proposed numerical primitive,
not an existing API. It uses the ordinary quadratic-algebra exponential;
alternative geometric notions of “parabolic trigonometry” such as R3 are
different constructions.

**Important embedding limit:** choosing `sqrt(kappa)*j` on one side and
`sqrt(−kappa)*i` on the other approaches zero, not a nonzero dual generator.
Indeed if `u²=kappa` with real nonzero kappa, both body channels are nonzero,
so the equations `2*z*w=0` force both tangent channels to vanish. A continuous
family of these scalars cannot converge to `eps`. Preserve a quadratic
generator or a 2 × 2 matrix through the transition instead. The historical
`M2R` canonicalization loses the similarity basis and is unsuitable for this.

## 7. Differentiation, non-holomorphic functions and optimization

| Algebra | Contribution | Uses and boundaries |
| --- | --- | --- |
| C | Holomorphic calculus; complex-step approximation for suitable real analytic programs | Derivative checking; complex-step has a step size and differs from exact nilpotent lifting |
| S | Two independent evaluation points or real tangent lanes when combined with D | Scenario comparison; finite differences still suffer subtraction error |
| D | `f(a+eps*b)=f(a)+eps*b*f'(a)` for differentiable real f | Forward AD, Jacobian-vector products, differentiating a solver |
| A | Two complex directional derivatives; i-conjugation also transports real-linear derivatives | Complex models followed by real loss functions, calibration and design |

For a real-differentiable complex function the correct general rule is

$$df=f_z\,w+f_{\overline z}\,\overline w,$$

not always `f'(z)*w`. This permits intensity, conjugation and real-valued losses
without pretending they are holomorphic (R4). A public real-linear lift should
coexist with a public analytic lift. Reject or explicitly define derivatives
of `abs` at zero, `min/max` at ties, rounding boundaries and branch jumps.
Extracting `.real` or calling `float` is not an automatic derivative rule.

**Missing:** `primal`, `tangent`, `seed`, `jvp`, `jacobian`, real-linear lifts,
custom derivative rules, differentiable measurements and implicit-function
wrappers. Independent hyper-dual generators or jets are needed for automatic
Hessians (R5). Using `eps*i` or `eps*j` as a “second epsilon” fails because their
products with `eps` also vanish. Dense parameter gradients still need multiple
seeds or reverse-mode AD; two lanes do not remove that scaling cost.

## 8. Polynomials, nonlinear equations and continuation

| Algebra | Root behaviour | Uses |
| --- | --- | --- |
| C | Finite roots counted with multiplicity for a nonconstant polynomial | Modal frequencies, poles and zeros |
| S | Independent real polynomial equations in the two channels | Multiple combinations of real equilibria |
| D | `P=P0+eps*P1`: `P0(u)=0`, `P0'(u)*v+P1(u)=0` | Root sensitivities and first-order deformation |
| A | Apply this complex-dual root condition independently twice | Mode branches with sensitivities; discrete roots and continuous families |

At a simple body root, `v=−P1(u)/P0'(u)`. At a multiple root the tangent equation
may have no solution or an arbitrary complex tangent. A degree-n polynomial
whose two body polynomials have n simple roots yields n² combined roots.
Without these assumptions the degree alone does not bound the root set in A.
If a body polynomial vanishes identically, even its body roots need not be
discrete.

**Existing:** Newton interpolation at distinct real nodes, next-value guessing,
and a demonstration-specific Newton fractal. **Missing:** polynomial derivative,
integral and arithmetic APIs; Hermite interpolation; general root classification;
parameter continuation; residual and multiplicity reports. Hermite data are a
particularly natural bridge between polynomial interpolation and dual numbers.
Do not apply Vandermonde inversion when node differences are zero divisors.

## 9. Linear algebra, matrix functions and transformation groups

| Algebra | Structure | Uses |
| --- | --- | --- |
| C | Standard complex matrices | Phasor networks, eigenmodes, signal processing |
| S | Two real matrix systems | Characteristic coordinates and scenario separation |
| D | Body solve followed by tangent solve | `dx=A0^−1*(db−dA*x)`; calibration of implicit linear models |
| A | Two complex body/tangent matrix systems | Two frequencies or operating points with derivatives |

**Existing:** channel-aware square solves and real-expanded complete solution
spaces. **Missing:** retained LU/QR factorizations, least squares with an
explicit metric, matrix functions, eigensystem sensitivities, sparse/batched
operations. The `Matrix` class itself currently stores real floats, not Ultra
entries. A real least-squares fit can be legitimate, but it must specify how
body and tangent residuals are weighted; a pseudoinverse depends on that choice.

For matrix functions, `f(M+eps*E)=f(M)+eps*L_f(M,E)`. In general
`L_f(M,E) != f'(M)*E`, since M and E need not commute. For exp it equals
`integral_0^1 exp((1−s)M)*E*exp(sM) ds`. R6 gives the established numerical
framework. Repeated eigenvalues require special treatment; individual
eigenvectors can be ill-conditioned while the matrix exponential is smooth.

C and D support planar kinematics and its sensitivities. S supports collinear
boosts. General 3D rotations, non-collinear boosts and rigid motion need an
operator/matrix or quaternion/Clifford layer. Do not change Ultra's commutative
product to imitate those groups.

## 10. Integration, differential equations and transforms

| Algebra | Natural contribution | Uses |
| --- | --- | --- |
| C | Oscillatory kernels; harmonic/holomorphic functions | Fourier methods, circuits, wave envelopes |
| S | Characteristic directions; kernels split into growing/decaying exponentials | 1+1 wave equations, transport, Laplace-like transforms |
| D | Tangents of integrals and ODE solutions | Parameter estimation, trajectory sensitivity |
| A | Two complex solutions or modes with their parameter tangents | Wave inversion, filter design, coupled-mode models in a suitable fixed basis |

**Missing:** integration and ODE adapters retaining all channels, event-time
derivatives, FFT/convolution adapters, boundary-condition handling and error
control for both bodies and tangents. Differentiating an integral additionally
requires the usual regularity assumptions and boundary terms for moving limits.
Differentiate a discontinuous event through its event equation, not by silently
reusing the derivative of an unchanged control-flow branch.

For a smooth S-holomorphic function `u+j*v`, the generalized Cauchy–Riemann
relations imply `u_xx−u_yy=0`; for C the sign is plus, giving Laplace's equation.
For D they instead become `u_y=0, v_y=u_x`, a degenerate tangent structure.
This links elliptic, hyperbolic and degenerate first-order structures; it does
**not** make every parabolic PDE (such as the heat equation) a dual-holomorphic
problem. Such PDEs need an explicit time-evolution operator.

A transform using `exp(−i*omega*t)` can process both complex channels and their
tangents. Replacing i by j creates exponential growth/decay, not a bounded
unitary Fourier kernel. Benchmarks must compare with four ordinary complex
arrays (two bodies, two tangents), not just a slow scalar loop.

## 11. Special functions and stable limiting cases

| Algebra | Extension rule | Uses |
| --- | --- | --- |
| C | Choose a complex special function and its branches | Bessel waves, error functions, gamma and Lambert W models |
| S | Evaluate in the two real channels when their domains permit | Paired real boundary or growth problems |
| D | Value plus derivative, including well-defined removable limits | Sensitivity of special-function models |
| A | Two complex values and derivative lifts with independent branch metadata | Differentiable wave/scattering models and inverse response models |

**Missing:** a public function-registration protocol and stable `expm1`,
`log1p`, `sinc`, `sinhc`, exprel and scaled exponentials; optional special-function
backends after that. A backend must expose derivative and branch contracts,
not merely a list of names. A singular intermediate formula need not mean
a singular final function: `sinc(0)=1` is an example. Conversely, a finite
special-function value does not guarantee a finite tangent at a branch point.

## 12. Integers, modular arithmetic, ordering and discrete operations

| Algebra | Exact discrete counterpart | Useful scope |
| --- | --- | --- |
| C | Gaussian integers Z[i]; rational complex numbers Q[i] | Divisibility, lattice arithmetic, exact polynomial identities |
| S | Z[j] embeds in pairs of integers of the same parity | CRT structure after inverting 2, paired congruences |
| D | R[eps]/eps² over an exact coefficient ring R | Formal first variations, polynomial lifting |
| A | R[i,j,eps] with explicit coefficient-ring rules | Exact identity verification; finite-ring and lifting experiments |

**Existing:** Python-integer primality/factorization/Euclid/RSA exercises and
residue rings, alongside a binary64 Ultra core. These do not yet form an exact
hypercomplex backend. Over Z, `(1+j)/2` is unavailable; over Q it is available.
Modulo an odd prime p the j decomposition works. The complex factor splits
when `p=1 mod 4` and is the quadratic field extension when `p=3 mod 4`.
In characteristic two, `j²−1=(j−1)²`; the idempotent formula and the real-algebra
structure cannot be reused. Zero divisors also preclude blindly transplanting
integer gcd, prime factorization or Euclidean division.

**Needed:** exact integer/rational/modular coefficient types, explicit embedding
and conversion rules, exact powers and polynomial evaluation before any
transcendentals. Floors, ceilings, comparisons, remainder and bitwise operations
should either require an exact embedded scalar or name a selected coordinate
policy. There is no uniquely privileged “floor of an Ultra”. Factorial on
integers and gamma continuation are different operations and domains.

## 13. Statistics, uncertainty and the meaning of two channels

| Algebra | Legitimate interpretation | Uses |
| --- | --- | --- |
| C | Complex random variables and Hermitian covariance with a specified probability model | Signal statistics |
| S | Two scenarios/endpoints with a chosen ordering; not automatically an interval | Scenario comparison and sensitivity bounds under extra monotonicity assumptions |
| D | First-order perturbations, not a probability distribution | Delta-method covariance propagation and local error analysis |
| A | Two complex scenarios plus local derivatives | Comparing device configurations and propagating a specified parameter covariance |

`Binary.range_from/range_to` store two channel values, but split multiplication
is **not interval arithmetic**. Encoding `[-1,1]` as `j` and squaring yields
`1`, whereas the set of squared values is `[0,1]`. Likewise a tangent alone
does not encode a finite uncertainty interval or its higher-order remainder.

**Needed:** an explicitly separate interval/enclosure backend for certified
bounds; Jacobians and `J*Sigma*J.T` for first-order covariance propagation;
clear distinction between model, parameter and numerical uncertainty. Existing
clustering and classification utilities are adjacent applications, not evidence
of an intrinsic probability theory of A. A coefficient norm cannot silently
become a physical probability or a metric appropriate for every dataset.

## 14. What each pair contributes, operation by operation

The full algebra is not the only useful combination. The following matrix
complements the individual C/S/D comparisons above. “Sensitivity” here refers
to a chosen first-order lift; it is one interpretation of the dual factor.

| Operation family | C ⊗ S | C ⊗ D | S ⊗ D | Full A |
| --- | --- | --- | --- | --- |
| Products and quotients | Two complex products; complexification extends the real split domain | Complex product/quotient and its variation | Two real product/quotient variations | Compose all of these; zero-divisor conditions remain explicit |
| Exp/log | Common and relative phases plus differential gain | Complex exponential/logarithm and infinitesimal variation | Hyperbolic scaling with its variation | Mixed Euler factorization with circular, hyperbolic and dual factors |
| Powers and roots | Independent complex branches, n² unit roots | Each simple complex root has a determined tangent | Real root choices in each split sector plus tangent equations | Independent branches with tangents and degenerate solution families |
| Metric and conjugation | Two amplitudes; swapping and complex conjugation have different meanings | Amplitude/intensity plus variation | Indefinite form plus variation, with null-direction issues | Numerical norm, geometric forms and physical measurements remain separate choices |
| Angles | Common/relative complex phase and hyperbolic amplitude ratio | Phase or heading with angular variation | Rapidity/shear variation and sector data | Phase, relative phase, gain and their variations in a common expression |
| Trigonometry | Bicomplex trigonometric functions and their two complex structures | Sine/cosine with exact first-order variation | Split trigonometry and its first-order variation | Full mixed-argument identities and the differential geometry of their outputs |
| Differentiation | Complex calculus or step approximations; no nilpotent AD factor | Complex and real-linear directional AD with appropriate primitives | Two real directional lifts | Two complex directional lifts; higher orders need an extension |
| Polynomial equations | Cartesian products of complex root sets | Polynomial tangent-lifting equation | Two real tangent-lifting problems | Branch combinations, compatibility conditions and free tangent families |
| Linear algebra | Two complex systems | Complex solve with sensitivity equation | Two real body/tangent solves | Two complex body/tangent solves; mode interaction via an operator layer |
| Integration and ODEs | Complex modes with split structure, e.g. opposite characteristics | Integrals/trajectories with their variation | Characteristic flow with parameter variation | Wave phase, propagation and model sensitivity together |
| Transforms | Two complex transforms, or mixed oscillatory/exponential kernels with stated domains | Complex transform with differentiated parameters | Characteristic/Laplace-type transform with variation | Shared transform interface with explicit kernel and metric |
| Special functions | Two complex branch choices | Complex special-function lift | Real-domain split special-function lift | Mixed branches and sensitivities; domains are checked per factor |
| Exact/discrete arithmetic | Gaussian/split tensor arithmetic; CRT when available | Exact complex polynomial deformation | CRT and exact real/modular deformation | Full coefficient-ring-aware polynomial calculus |
| Statistics/uncertainty | Two complex scenarios | Complex local variation | Two real scenarios with local variations | Joint scenario/sensitivity models; no automatic interval or probability semantics |

For instance, a complex field with a dual angle can describe an infinitesimal
rotation; adding the split factor distinguishes common from relative rotations
of two modes. Conversely, complexifying split arithmetic admits logarithms of
units outside the positive real split sector. These are distinct gains from
combination: transport of geometry, and extension of functional domains.
