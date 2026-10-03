# API map

[Documentation](README.md) · [Getting started](getting-started.md)

This is a task-oriented map of the implemented interfaces. Mathematical domains and examples live in the linked guides; method docstrings define local argument contracts.

| Task | Public interface / module | Guide |
| --- | --- | --- |
| Full numerical algebra | `Ultra`, `ONE`, `ZERO`, `I`, `J`, `EPS`; `core` | [Foundation](mathematics.md) |
| Closed numerical planes | `Complex`, `Binary`, `Dual`, `RootSet`; `numbers` | [Geometry](unified-geometry.md) |
| Exact coefficients | `ExactUltra`, `ExactComplex`, `ExactBinary`, `ExactDual`, `QONE`, `QZERO`, `QI`, `QJ`, `QEPS`; `exact` | [Exact arithmetic](exact-arithmetic.md) |
| Numerical formulas | `Formula`, `evaluate`, `evaluate_system`; `formula` | [Getting started](getting-started.md) |
| Exact formulas and JSON | `ExactFormula`, `evaluate_exact`, exact values' `to_json` / `from_json` | [Exact arithmetic](exact-arithmetic.md) |
| Bound/legacy expressions | `FormulaSystem`, `BoundFormula`, `Parameter`, `Calculation`, `SimpleCalculation`; `expressions` | [Compatibility](compatibility.md) |
| Numerical linear equations | `solve`, `solution_space`, `LinearSolution`; `linalg` | [Operation atlas](research/operations.md#linear-algebra-and-implicit-equations) |
| Exact matrices and solution families | `ExactMatrix`, `exact_solve`, `exact_solution_space`, `ExactLinearSolution` | [Exact arithmetic](exact-arithmetic.md) |
| Polynomials and interpolation | `Polynomial`, `ExactPolynomial`; `polynomial`, `exact_polynomial` | [Exact arithmetic](exact-arithmetic.md) |
| Intrinsic metrics and angles | `CIRCULAR`, `HYPERBOLIC`, `PARABOLIC`, `QuadraticPlane`, `PlanePolar`, `metric_dot`, `metric_project`, `metric_reflect` | [Unified geometry](unified-geometry.md) |
| Isometries | `PlaneIsometry`, plane `.rotor()` / `.cayley()` | [Unified geometry](unified-geometry.md) |
| Exact Euclidean constructions | `orientation2d`, `line_intersection2d`, `segment_intersection2d`, `barycentric2d`, `circumcircle2d`, `incircle2d` | [Unified geometry](unified-geometry.md) |
| Interacting modes | `ModeOperator`, `.from_matrix()`, `.matrix()`, `.cayley()` | [Unified geometry](unified-geometry.md) |
| Projective maps | `Mobius`, `ProjectivePoint`, `cross_ratio` | [Unified geometry](unified-geometry.md) |
| Real vectors and mechanisms | `geometry`, `Matrix`, `Joint`, `Actor`, `Freedom`, `Machine`, `Mechanism` | [Showcase](gallery/README.md) |
| Sampling and displays | `visuals.sample_curve`, `visuals.domain_color_grid`, `gui` | [Getting started](getting-started.md) |
| Integer/modular foundations | `number_theory`, `modular.ModularRing`, `modular.Residue` | [Scope](scope.md) |

`M2R` is a retained compatibility experiment, not an ordinary matrix algebra; see [compatibility](compatibility.md).

## Choose an observable deliberately

| Operation | Meaning |
| --- | --- |
| `.real`, `.i`, `.j`, … | One stored coefficient; no automatic preservation of other components |
| `.coefficients` / iteration | All eight components in the documented basis order |
| `.primal` / `.tangent` | Epsilon-free body / coefficient of epsilon, each in CS |
| `.with_tangent(seed)` | Replace the epsilon coefficient with a CS seed |
| `.real_part()` / `.imag_part()` | Project complex components while preserving split and dual structure |
| `.abs2()` | Squared complex amplitude in each split factor, including tangents |
| Numerical `.amplitude()` / `.phase()` | Real directional derivatives of modulus / local unwrapped phase; domain restrictions at zero |
| `abs(value)` for `Ultra` | Euclidean coefficient norm for diagnostics, returning a float |
| `plane.quadrance(value)` | Intrinsic circular, hyperbolic or parabolic form |
| `.channels()` | Faithful split-eigenspace coordinates; numerical conversion can lose small differences |

There is no exported general `jacobian`, `hessian`, ODE solver, FFT, constraint graph, arbitrary-precision backend or `Ultra.roots()` in this release. Names proposed in the [roadmap](research/roadmap.md) are designs, not imports.
