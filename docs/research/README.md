# Completing the ultracomplex programme

Research and implementation agenda, 2026-10-03 (Europe/Berlin).
Code baseline: [`2a3caeffb29244e6f0289f0b0ea01d131c557155`](https://github.com/hoechp/temp/tree/2a3caeffb29244e6f0289f0b0ea01d131c557155), version 0.2.0.

The goal is to make complex, split-complex and dual arithmetic useful together
across as much mathematics as possible: ordinary calculation, geometry,
trigonometry, analysis, exact arithmetic and applications. A completed migration
of the old Java features is **not** completion of that goal.

The guiding idea is the **full unification of complex, split-complex and dual
algebras**, including their mixed products. The agenda starts from their
geometries and operations, then asks what becomes possible when they share one
calculus. Differentiable modelling is a strong application of that union, not
its definition or its only purpose. The largest gains will come from connecting
existing primitives, giving ambiguous operations explicit semantics, and adding
operator and higher-order layers where the scalar algebra is insufficient.

## Reading map

| Document | Purpose |
| --- | --- |
| [Operations atlas](operations.md) | Compare each base algebra and their combination across operation families, including domains and applications |
| [Application proposals](applications.md) | Seven ranked projects, their equations, missing prerequisites and success criteria |
| [Implementation backlog](roadmap.md) | Source-grounded gaps, one reproduced correctness defect, proposed APIs and acceptance gates |
| [Sources and evidence](references.md) | Primary references, what each supports, and reproducible checks |
| [Current mathematical contract](../mathematics.md) | What the released implementation actually promises |

Status terms used here: **existing** means source-inspected functionality;
**derived** means a consequence of the stated algebra, sometimes additionally
checked numerically; **proposed** means an API or experiment not implemented;
**research question** means an advantage still requiring evidence. Proposed API
names are design sketches. No new production mathematical APIs are introduced
by this documentation change.

## 1. One algebra, several equally valid viewpoints

The defining algebra is

$$A=\mathbb R[i,j,\varepsilon]/(i^2+1,j^2-1,\varepsilon^2),$$

with commuting generators. This tensor product contains faithful copies of all
three base algebras sharing the same real scalars, together with their mixed
directions `ij`, `eps*i`, `eps*j`, and `eps*ij`. It is not merely their direct
sum. Its universal property makes “unification” precise: compatible unital
maps from the three factors into a commutative real algebra extend uniquely to
a map from A.

Useful viewpoints include:

- **Geometric union:** circular, hyperbolic and infinitesimal behaviour and the
  operations connecting them.
- **Complexification:** complex-valued split/dual geometry, extending domains
  of functions that are restricted inside a real 2D subalgebra.
- **Dual extension:** first-order deformations of the combined complex/split
  algebra; a tangent can describe variation of an entire geometric object.
- **Bicomplex viewpoint:** two commuting complex structures, further extended
  by dual directions.
- **Idempotent or matrix representation:** useful for proofs, algorithms and
  independent verification, without prescribing a physical interpretation.

An Euler-style factorization makes the union visible before choosing any
computational representation. For real r, theta, eta, chi and
`V=a+i*b+j*c+ij*d`, commutativity gives

$$\exp(r+i\theta+j\eta+ij\chi+\varepsilon V)=
e^r(\cos\theta+i\sin\theta)
(\cosh\eta+j\sinh\eta)
(\cos\chi+ij\sin\chi)(1+\varepsilon V).$$

One expression combines scale, a circular factor, a hyperbolic factor,
a mixed circular factor and a deformation spanning all four dual directions.
Every unit of A admits such a representation through a choice of logarithm;
it is not unique. In a physical model these factors can describe common phase,
relative phase, differential gain and geometric or parameter variations.
That interpretation is a modelling choice, not dictated by a storage layout.

In the idempotent representation the structural decomposition is

$$p_\pm=(1\pm j)/2,\qquad
X=(z_++\varepsilon w_+)p_+ +(z_-+\varepsilon w_-)p_-,\qquad
A\cong\mathbb C[\varepsilon]/(\varepsilon^2)\times
\mathbb C[\varepsilon]/(\varepsilon^2).$$

This is a change of basis retaining all eight real coordinates, not a reduction
of the project's meaning to a two-channel application. For a local
holomorphic function,

$$f(X)=\sum_{s\in\{+,-\}}\bigl(f(z_s)+\varepsilon f'(z_s)w_s\bigr)p_s.$$

Consequently there are two distinct useful encodings:

- **Two states, one sensitivity per state:** both complex bodies can differ;
  all eight real coordinates may be independent.
- **One state, two derivative directions:** duplicate the complex body and seed
  the two tangent channels differently. A complex output then contains its value
  and two complex directional derivatives, with a duplicated body.

This is structural batching, not a demonstrated speedup. It is also not an
eight-variable gradient or a Hessian. The current robotics and wave examples
already demonstrate these two encodings.

| Algebra | Structure | Useful interpretation | What the combination adds |
| --- | --- | --- | --- |
| Complex, C | `i² = −1` | Planar rotation, phase, oscillation | Complex amplitudes and analytic continuation |
| Split-complex, S | `j² = +1`; R × R | Rapidity, squeezing, two characteristic coordinates | Exact separation into two real channels |
| Dual, D | `eps² = 0` | First-order tangent or infinitesimal displacement | Chain-rule propagation without a finite-difference step |
| C ⊗ S | C × C | Two complex modes, frequencies, polarizations or scenarios | Independent complex branches and coherent-mode bookkeeping |
| C ⊗ D | Complex dual numbers | Complex response and its parameter derivative | Differentiable phasors, impedance, planar kinematics |
| S ⊗ D | D × D | Two real scenarios or characteristic waves and tangents | Parallel sensitivity calculations, boost sensitivity |
| C ⊗ S ⊗ D | Two complex dual channels | Two complex states plus their derivatives | Shared formulas for forward models, measurements and local inverse design |

There is another useful connection: `k = i*j` also satisfies `k² = −1`.
Thus C ⊗ S is also a representation of the **bicomplex algebra** generated by
the commuting complex units `i` and `k`, with `j = −i*k`. This is an equivalence,
not an extra dimension or an extra independent derivative slot. The four
epsilon basis directions all belong to the same square-zero ideal.

## 2. A precise replacement for “everything real numbers can do”

Four different tasks must not be confused:

1. **Algebraic completion:** implement every well-defined operation with its
   actual domain and return complete solution sets when results are not unique.
2. **Functional calculus:** extend functions with the correct derivative,
   branch and singularity contracts, including non-holomorphic measurements.
3. **Chosen geometry:** specify what length, angle, ordering or distance means.
   Multiple useful choices can coexist under different names.
4. **Larger structures:** use matrices, independent nilpotents or exact
   coefficient rings when the original eight-dimensional scalar cannot express
   the desired operation.

Some restrictions are mathematical, not missing implementation:

- **No division by every nonzero element.** `(1+j)*(1−j)=0` and `eps²=0`.
  Division by a zero divisor may instead be posed as an equation with no
  solutions or a family of solutions. The existing `solution_space` already
  supports this approach.
- **No compatible real-style total order.** A ring order in which nonzero
  squares are positive cannot contain `i²=−1`. Sorting coefficients or choosing
  a body-channel order is a policy, not the ordered-real-number structure.
- **No positive-definite multiplicative norm.** If such a norm existed,
  `N(eps)²=N(eps²)=0` would contradict `eps != 0`. A numerical error norm, an
  indefinite metric and a physical intensity serve different purposes.
- **No global single-valued inverse trigonometry or logarithm.** Periodicity,
  independent channel windings and branch points remain. All units have a
  logarithm in A; this does not make the logarithm unique or continuous globally.
- **Not every number has a square root.** `eps` has none. A root's body would
  have to vanish in both complex channels, forcing its square to be zero.
- **No exact second derivative from the existing epsilon ideal in one lift.**
  For `N = eps*A`, `N²=0`; every product of two tangent seeds vanishes. Repeated
  evaluation of a separately differentiated function is possible, but is not
  automatic nested AD in the current scalar type.
- **No general 3D rotation group from scalar multiplication.** Ultra products
  commute; general rotations and rigid motions do not. Existing real matrix
  geometry is useful, but does not remove this distinction.
- **No canonical extension of every arbitrary real function.** A first-order
  lift needs a derivative. At a kink, discontinuity or branch boundary a
  generalized derivative or one-sided rule must be chosen explicitly.

These constraints suggest richer outputs and explicit semantics rather than
invented finite answers. They constrain what the union can mean mathematically;
they do not make its idempotent representation the preferred way to discover
applications.

## 3. Synergies that are still underused

**Computation → measurement → inverse problem.** The current engine transports
complex derivatives, but users still manually extract amplitudes and apply real
measurement derivatives. Differentiable intensity, phase, normalization and
residuals would connect optics, circuits, wave fitting and robotics end to end.

**Independent channels → interacting modes.** Ordinary Ultra multiplication
never transfers information between the two idempotent channels. The existing
automorphism `X.conjugate("j")` swaps them. Combining multiplication with this
swap represents any complex-dual 2 × 2 operator; composition is generally
noncommutative. This is a particularly small, concrete extension with substantial
new modelling reach. See [proposal 1](applications.md#1-differentiable-two-mode-optics-and-operators).

**Circular → hyperbolic → parabolic dynamics.** Stable generalized sine and
cosine functions of a squared generator can describe underdamping, overdamping
and critical damping continuously. This requires a quadratic-algebra or matrix
layer that retains the generator, not merely changing a number's type based on
the sign of a discriminant. It connects a clear visual demo to a real numerical
problem at repeated eigenvalues.

**Roots → sensitivity → exact modular lifting.** The linearization governing a
dual root is the same polynomial Taylor mechanism used in Hensel lifting.
An exact backend could make the integer utilities and hypercomplex arithmetic
parts of one coherent subject rather than neighbouring modules.

**Geometry → derivatives → calibration.** A phase, a boost parameter and a
dual slope are different quantities with related composition laws. A typed
angle/metric layer can preserve these differences while making the same
calibration and optimization tools operate on each.

## 4. Recommended order

| Order | Investment | Why now |
| --- | --- | --- |
| 1 | Fix integer exponent coercion; clarify metrics and conversions | A correctness defect and semantic ambiguity undermine every later demo |
| 2 | Public tangent API, non-holomorphic measurements, stable elementary functions | Makes existing successful demos reusable and prevents silent derivative loss |
| 3 | Unified geometry and critical-damping / propagation-cutoff laboratory | Unifies the three base behaviours and tests numerical robustness at their boundary |
| 4 | Two-mode operator API and an inverse-design optics demo | Builds on existing primitives while adding actual mode interaction |
| 5 | Complete roots, branch continuation and implicit differentiation | Makes singularities and solution families useful rather than unexplained failures |
| 6 | Independent higher-order jets; exact and modular coefficient backends | Opens Hessians and a substantial discrete/continuous connection; larger implementation scope |

The flagship mathematical demonstration should be **a smooth passage through
critical damping**, accompanied by a geometry laboratory comparing the three
base algebras. The strongest near-term engineering demonstration is **a
differentiable optical circuit**. A distinctive long-term research track is the
shared treatment of **root lifting, singularities and sensitivities**, including
exact modular examples.

None of these proposals establishes a new algebra, a novel physical theory or
superiority over NumPy/JAX/SciPy. Their value must be shown through explicit
models, independent oracles, usable APIs and comparisons against direct complex
and real formulations. The derivations here establish representability; the
application and performance advantages remain hypotheses to test.
