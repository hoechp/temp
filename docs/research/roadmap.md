# Implementation backlog and completeness criteria

[Agenda](README.md) · [Operations](operations.md) · [Applications](applications.md)

This is a source audit against commit `2a3caef`, not a promise that the proposed
APIs already exist. “Missing” means absent as a reusable library capability;
some operations can already be assembled manually or appear in a single demo.
The work in this change documents and probes these gaps; it does not implement
the proposed production features.

## Current capability map

| Area | Existing source and capability | Remaining distinction |
| --- | --- | --- |
| Scalar calculus | [`core.py`](../../src/ultracomplexmath/core.py): arithmetic, all elementary trig/hyperbolic functions, log branches, `_lift`, channel conversion | `_lift` is private; no public AD façade, full root families or stable special limits |
| Closed algebras | [`numbers.py`](../../src/ultracomplexmath/numbers.py): C/S/D, roots, rational powers, four split sectors | Mixed types reject implicit arithmetic; geometry names mix Euclidean and algebra-specific meanings |
| Coordinates and geometry | [`coordinates.py`](../../src/ultracomplexmath/coordinates.py), [`geometry.py`](../../src/ultracomplexmath/geometry.py): polar forms, vectors, frames, lines, dual angles | No common geometry/metric/branch protocol or derivative-preserving angle API |
| Linear equations | [`linalg.py`](../../src/ultracomplexmath/linalg.py): `solve`, rectangular/singular `solution_space` | No retained factorization, QR/SVD, conditioning report or matrix functions |
| Matrices and mechanisms | [`matrix.py`](../../src/ultracomplexmath/matrix.py), [`mechanisms.py`](../../src/ultracomplexmath/mechanisms.py) | `Matrix` is real; `M2R` loses its similarity basis and is not associative |
| Polynomials | [`polynomial.py`](../../src/ultracomplexmath/polynomial.py): interpolation and guessing | No complete polynomial algebra, Hermite interpolation or general root solver |
| Discrete mathematics | [`number_theory.py`](../../src/ultracomplexmath/number_theory.py), [`modular.py`](../../src/ultracomplexmath/modular.py): exact Python-int utilities and scalar residues | Ultra converts coefficients to binary64; no shared exact or finite-ring algebra backend |
| Applications | [`examples/applications.py`](../../examples/applications.py), [`gallery.py`](../../examples/gallery.py) | Demonstrations, not reusable optics/AD/optimization/ODE modules |
| Formulas | [`formula.py`](../../src/ultracomplexmath/formula.py), [`expressions.py`](../../src/ultracomplexmath/expressions.py) | New APIs will need coordinated safe parser exposure and documented types |

## P0: correctness and semantic contracts

| ID | Gap and proposed change | Acceptance evidence |
| --- | --- | --- |
| G01 | **Confirmed defect:** `Ultra.__pow__` coerces a Python integer exponent to float before deciding it is integral. Dispatch exact Python ints first, preserving sign/parity; audit closed-type power forwarding. Keep approximate float exponents a separate contract. | `I**(2**53+1)==I`, `(-ONE)**(2**53+1)==-ONE`, large positive/negative powers of units, zero-divisor negative powers rejected, bool policy explicit |
| G02 | Define embeddings and mixed-type promotion. Keep `reinterpret` explicitly a coordinate reinterpretation, never an algebra-preserving conversion. Add an explicit common promotion path for C/S/D. | Each embedding preserves sums/products; mixed examples reach A; `Complex(0,1)` cannot silently become a split unit; exact-to-float conversion is visible |
| G03 | Separate Euclidean display geometry, intrinsic quadratic forms and physical measurements. Preserve old names with clear documentation or an intentional deprecation path. | C length, S null vectors and four sectors, D degeneracy; coefficient norm remains a diagnostic; no silent change to migration conventions |

Minimal G01 reproduction on the audited baseline:

```python
from ultracomplexmath import I, Ultra

n = 2**53 + 1
print(I**n)  # 1.0; mathematically it must be I
print(Ultra(n) == Ultra(n - 1))  # True: documented binary64 coefficient limitation
```

The second observation is a representation limitation already documented by the
core. The first is avoidable loss of an **exact input exponent**; preserving
integer coefficients everywhere is not required to fix it. A broad existing
test suite can pass without covering this case. This agenda records the defect
without silently changing arithmetic while conducting a documentation task.

## P1: make existing mathematics reusable

| ID | Proposed capability | Why it matters and how to verify it |
| --- | --- | --- |
| G04 | `primal`, `tangent`, seed/extract helpers, `jvp`, two-direction Jacobian helper, public analytic lift with derivative/domain metadata | Replaces repeated manual channel manipulation; compare composition and seed linearity with independent derivatives; specify when bodies must match |
| G05 | Channel-preserving `real_part`, `imag_part`, `abs2`, `amplitude`, `phase`, and a real-linear lift | Connects complex fields to real losses; test conjugation and intensity analytically; reject undefined phase at zero and avoid confusing `.real` coefficient extraction with a differentiable projection |
| G06 | Stable `expm1`, `log1p`, `sinc`, `sinhc`, exprel and `C_kappa/S_kappa`; optional `sinpi/cospi` and scaled forms | Remove false singularities and cancellation; test exact limits and first derivatives at zero against series/high precision, plus large-argument range behaviour |
| G07 | Explicit angle results with geometry/sector/winding; dual-preserving `atan2`; per-channel log/root path continuation | Handles physical phase tracking and rapidity correctly; test loop windings, cut crossing, null directions, poles and unwrapping sampling assumptions |
| G08 | `UltraRootSet` with discrete branches and complex/real affine parameters; rational-power and nonunit policies | Represent n² unit roots, empty sets and continuous families; verify completeness from channel equations and residuals for family samples |
| G09 | Polynomial coefficient algebra, derivative/integral, Hermite interpolation and root lifting | Bridges integer utilities, AD and interpolation; use independently differentiated polynomials and exact small examples; detect zero-divisor denominators and identically zero body polynomials |
| G10 | Implicit differentiation of equations, local Newton/Gauss–Newton adapters and continuation | Differentiate equilibria rather than solver iteration history where appropriate; compare implicit and explicit derivatives; detect rank loss and constrain claims to a local branch |

A branch-tracking API needs a path and continuity assumptions. It cannot infer
an arbitrary winding from two distant samples. A nondifferentiable primitive
needs a chosen policy or a precise error, not a fabricated zero tangent.

## P2: structures extending the scalar algebra

| ID | Proposed capability | Boundary and acceptance evidence |
| --- | --- | --- |
| G11 | Ultra matrices, cached channel factorizations, weighted least squares, matrix exp/log and Fréchet derivatives | Scalars commute but matrices do not; test noncommuting tangent matrices with an independent block-matrix oracle; document metrics, rank tolerance and singular behavior |
| G12 | Two-mode operator `T(X)=alpha*X+beta*swap(X)`; quadratic generator objects retaining `B²=kappa` | Exact complex-dual 2 × 2 matrix oracle, correct noncommutative composition and optical conservation laws; preserve state/operator dimension distinction |
| G13 | Independent hyper-duals or general Taylor jets over suitable coefficient algebras | Keep Ultra's existing relations fixed; a full extra independent dual doubles real dimension to 16; test mixed Hessians and perturbation separation, not just repeated first derivatives |
| G14 | Batched channel arrays, NumPy adapters, FFT/convolution and integration/ODE adapters | Define memory layout and derivative-preserving ufunc coverage; test every adapter for tangent loss; benchmark against direct complex arrays, including conversion costs |
| G15 | Exact Z/Q coefficient backends, arbitrary precision as a separate numerical backend | Never route exact values through `float`; check integer growth and exact identities; transcendental results require an explicit numerical/symbolic backend |
| G16 | Modular hypercomplex arithmetic, CRT and Hensel experiments | State characteristic and unit tests of the coefficient ring; handle p=2 separately; do not transplant real idempotents or analytic logarithms into finite rings |
| G17 | Geometry-aware fractional transformations and projective charts | Retain metric and sector semantics; use unimodular coordinates over rings; independent matrix and invariant checks; do not mistake zero-divisor denominators for ordinary infinity |
| G18 | Function/domain registry, parser integration and serialization metadata | Keep safe AST evaluation; disclose branches, coefficient ring and representation; build tests from actual domain partitions and identities rather than blanket inverse round trips |

The P1/P2 distinction is architectural, not a claim that every P1 task is
small. Complete algebraic root classification and robust continuation can be
substantial. The two-mode operator is relatively contained; general projective
geometry, sparse solvers and arbitrary jets are larger research tracks.

## Proposed implementation sequence

1. **Foundation:** G01–G03, then G04–G07. Acceptance is reliable arithmetic and
   unambiguous, derivative-preserving measurements and angle semantics.
2. **Algebraic flagship:** the bounded part of G11/G12 needed for retained
   quadratic generators, followed by the critical-damping demo and the basic
   C/S/D geometry comparison. Prove regularity at the transition.
3. **Engineering flagship:** two-mode operator composition, coherent measurements
   and optical inverse design. Reuse the foundation rather than adding another
   example-local derivative implementation.
4. **Mathematical completion:** G08–G10, branch topology and root-family demo.
5. **Two explicit expansion tracks:** G13 for higher-order modelling, and
   G15–G16 for exact algebra and number theory. G14 follows real profiling needs;
   G17 follows a written geometry specification. Apply G18 throughout.

## What “complete” should mean for an operation

Each operation needs a compact contract with these fields:

| Field | Required question |
| --- | --- |
| Algebra and coefficient ring | C, S, D, A, an operator algebra, or an exact/modular variant? |
| Meaning | Analytic function, geometric measurement, equation solver or policy-selected discrete operation? |
| Domain | Units, sectors, regular body points, null directions, poles and branch points? |
| Output | One value, branches, an affine family, no solution, or an explicit unsupported case? |
| Differentiation | Holomorphic derivative, real-linear derivative, implicit derivative or a declared nonsmooth policy? |
| Numerical guarantee | Tolerances, overflow, cancellation, conditioning and any certified bound? |
| Interoperability | Closure in a base algebra versus explicit promotion to A; matrix/array behavior? |
| Evidence | Exact example, independent oracle and singular/degenerate boundary cases? |

No finite list of function names proves “all real operations” are complete.
This contract makes systematic expansion possible without silently changing
meaning between algebras. Symbolic antiderivatives and closed-form solutions
also cannot be promised for arbitrary inputs merely by enlarging the scalars.

## Validation and research gates

- Preserve all basis products and the current explicit zero-divisor errors.
- Use independent real/complex formulas and faithful matrix representations,
  including degeneracies; do not just compare two wrappers over `_lift`.
- For exact roots and modular arithmetic, use exact residuals; for numerical
  calculus, report a scale-aware residual and condition estimate.
- For an application, state the forward model, observables, unknowns and noise
  assumptions; compare recovered parameters, not just an attractive picture.
- For speed or compactness claims, compare equivalent mathematical work:
  two complex bodies plus two complex tangents, including array overhead.
- For a novelty claim, conduct a dedicated literature review. The sources in
  this agenda establish precedents and feasibility, not absence of prior work.

The [research probe](../../tools/research_probe.py) checks selected derived
identities and records baseline gaps. It is evidence for this agenda, not a
production solver or a substitute for the acceptance tests of future features.
