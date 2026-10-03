# Prioritized implementation roadmap

[Agenda](README.md) · [Operations](operations.md) · [Applications](applications.md)

Reviewed against 0.3.0 and updated for 0.4.0. **P0** protects numerical correctness; **P1** continues exact coefficients and geometry; **P2** broadens application coverage. Proposed APIs below are not imports.

## Correctness before new promises

The huge-integer exponent bug is fixed: `I**(2**53+1)==I`. Rational coefficients, exact matrices/polynomials and geometry are implemented. The renewed review found a different defect: channel reconstruction erased the `j` coefficient of `exp(1+i*h+ij*h)`. Version 0.4.0 uses component-preserving factors and scaled real exponentials, with tests down to h=`1e-100` and large compensated split exponents.

The same accuracy risk remains in other operations, including channel-based logarithm and inverse. A dominant body can be accurate while a tiny mixed coefficient is wrong. The frontier probe reports this explicitly; a general bicomplex Hessian API would currently promise too much.

## Work packages

| ID / priority | Gap | Next deliverable | Completion evidence |
| --- | --- | --- | --- |
| G01 / P0 | Componentwise accuracy and near-zero functions | Audit inverse/division/log/trig; stable selected paths, `expm1`, `log1p`, `sinc`, `sinhc` | Independent analytic/high-precision scale sweeps; coefficient errors; branch, range, underflow and compensated-large cases |
| G02 / P1 | Rational powers whose result is rational | Exact nth-root detection and explicit rational-power branches, starting with real/closed inputs | Cube root of 8, negative odd roots, reciprocals, irrational/singular cases and exact powered-back identities |
| G03 / P1 | Coefficient-domain extensibility | Minimal shared coefficient protocol; scoped algebraic/high-precision adapters | Same basis laws, domains and serialization; no implicit float conversion |
| G04 / P1 | Exact constraints and implicit geometry | Constraint graph, rational Jacobians, exact rank/free motions and regular implicit sensitivities | Closed linkage/CAD examples; independent singularity classification; infinitesimal versus finite motion distinguished |
| G05 / P1 | Continuous dynamics and matrix functions | Entire `C_kappa/S_kappa`, operator exponential/Fréchet derivative, midpoint time-step interface | Critical limits, independent ODE/matrix oracle, convergence order, invariant and differentiated identities |
| G06 / P1 | General derivative interface | JVP/seed helpers, real-linear contracts, scoped bicomplex Hessian entries and epsilon variations | Analytic oracles, non-holomorphic contracts, step/underflow diagnostics, repeated-seed Jacobians |
| G07 / P1 | Angles and projective continuation | Derivative-aware `atan2`, phase/sector histories and chart events | Loops/cuts/zeros/null rays/mixed-chart poles; agreement with homogeneous evolution |
| G08 / P1 | Conics and spatial geometry | Incidence, algebraic intersections, separate 3D pose/operator layer | Exact degeneracies/transformed incidence; noncommuting pose composition |
| G09 / P2 | Polynomial algebra over a ring | Nonunit-leading division strategy, factor/root metadata, resultants and rational splines | Degenerate/zero-divisor examples; field assumptions explicitly checked |
| G10 / P1 | Reusable and conditioned linear algebra | Factorizations, condition/rank diagnostics, repeated RHS, adjoints and sparse adapters | Exact residuals, independent references, singular families and scale tests |
| G11 / P2 | Modular hypercomplex coefficients | Full `A_(Z/nZ)`, unit algorithms, Hensel/Hasse and reconstruction | Exhaustive small rings including F2, odd-prime factors, lifted residuals/nonunit failures |
| G12 / P2 | Integration, transforms, special functions | Selected derivative-preserving quadrature/response APIs and FFT adapter | Scalar/complex references, branch/singularity contracts and convergence evidence |
| G13 / P2 | Ecosystem interoperability | NumPy batching/ufunc policy, schemas, units and AD boundaries | Round trips, dtype/shape errors and benchmarks with equal requested work |
| G14 / P2 | Validated application components | One transfer/scattering network, observations, fit and noise model | Model-specific conservation/passivity, independent solver, derivatives and identifiability |
| G15 / P1 | Complete root families | Independent sheets, tangent families and singular classifications; exact counterparts where supported | n² unit roots, empty/infinite cases, residuals and path consistency |

## Suggested sequence

**Milestone A: trustworthy exact geometry and derivatives.** G01, the small rational-root portion of G02, G04 linearized constraints and G06 first-order helpers. Deliver a closed-linkage showcase with exact residuals. Introduce G03 abstractions around concrete coefficient needs.

**Milestone B: motion and charts.** G05 generalized functions with existing exact Cayley steps, plus G07 continuation. Show all three motion regimes and their parameter sensitivities.

**Milestone C: a full-union application.** G14's transfer network using the relevant G10/G13 pieces. Compare transfer/scattering stability and solve an identifiable inverse problem.

**Research branch:** after G01, investigate bicomplex/dual higher derivatives on a thermodynamic potential. Modular G11 work can proceed independently of the numerical calculus. These are dependency recommendations, not implementations already underway.

## Decisions that remain explicit

- Full-algebra order, floor, remainder and probability need chosen semantics; naming them does not inherit real-number laws.
- Exact coefficient domains must state their closure. Q excludes generic radicals; a small algebraic extension excludes generic transcendental values.
- The epsilon ideal alone gives first-order jets. Arbitrary exact higher jets need a larger algebra; bicomplex finite steps are a different opportunity within the current algebra.
- General 3D poses need noncommuting operators or another extension. Keep scalar, operator and point types distinct.
- Accuracy contracts must identify protected components, not merely a body-dominated total norm.

No existing benchmark establishes an advantage over specialized arrays or established AD libraries. Compare equal requested outputs and accuracy in each concrete application.
