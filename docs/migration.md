# Migration guide and remaining work

Version 0.1.0 is a usable mathematical core, **not a complete migration of all
74 Java source files**. The old repository is the reference for pending modules.
Each source file has a status in [inventory.md](inventory.md).

## Core API mapping

| Java | Python | Difference |
| --- | --- | --- |
| `new Ultra(a,b,c,d,e,f,g,h)` | `Ultra(a,b,c,d,e,f,g,h)` | Same basis order, immutable floats |
| `new Ultra(new Complex(a,b))` | `Ultra.complex(a,b)` or `Ultra.coerce(a+b*1j)` | Common eight-dimensional result type |
| `new Ultra(new Binary(a,b))` | `Ultra.split(a,b)` | Split-complex embedding |
| `new Ultra(new Dual(a,b))` | `Ultra.dual(a,b)` | Dual embedding |
| `Ultra.unit(n)` | `Ultra.unit(n)` | Invalid indices raise; no special `-1` zero |
| `Ultra.ZERO`, `Ultra.ONE` | `ZERO`, `ONE` | Immutable module constants |
| `plus`, `minus`, `times`, `by` | `+`, `-`, `*`, `/` | Scalars accepted in either operand position |
| `pow` | `**` | Integer powers work on nonunits |
| `ln`, `log` | `.log()` / `.ln()`, `.log(base)` | Channel branches and domains specified |
| Trigonometric/hyperbolic methods | Same lower-case method names | Stable scalar primitives and exact dual lift |
| `getDouble(n)` | `.coefficients[n]` | Tuple can be serialized |
| `length()` | `abs(x)` | Euclidean coefficient norm |
| `equals(...)` | `==` or `.isclose(...)` | Exact and approximate comparison separated |
| `conjugate()` | `.conjugate("i" / "j" / "eps")` | Deliberate semantic change: automorphisms |
| `det()` | `.determinant()` | Deliberate semantic change: real 8x8 regular determinant |
| `Calculation.calculate(text)` | `evaluate(text)` | Strict grammar and explicit errors |
| `Formula` and `Parameter` | `Formula(text).evaluate(mapping)` | No in-place parameter or result mutation |
| `FormulaSystem` | `evaluate_system(definitions, inputs)` | Dependency evaluation with cycle detection |
| `HypercomplexLSE` | `solve(matrix, rhs)` | Unique square systems over full algebra |

## Intentional differences

- Eight-dimensional values are the common numerical type. No subclass-specific
  polar geometry, real split-only logarithm restrictions or mutable setters.
- Formula multiplication is explicit. `2î` becomes `2*i`; arbitrary prefix
  function notation becomes `sin(x)`. `base_log(x)` becomes `log(x, base)`.
- Unit glyphs `î`, `Ê`, `ê` and their modern `i`, `j`, `eps` names are available;
  superscript 2 and 3 are translated to powers. Other historical parse quirks,
  `?` placeholders, `dot` syntax and unsupported demo operators are not copied.
- Unbound variables are errors, not silently invented zero values. Formulas
  use fresh supplied values on each evaluation, avoiding stale cache effects.
- Principal values can differ from Java approximations. In particular the
  full algebra can leave a two-dimensional embedded subalgebra.
- `0**0=1`; other nonintegral powers of nonunits are rejected except the
  supported principal square-root case. Domain failures raise instead of NaN.
- The owner chose maximally permissive licensing for this migration: 0BSD.
  The original repository is unchanged. No PyPI release or application deployment
  has been published.

## Staged follow-up

| Stage | Scope | Acceptance criterion |
| --- | --- | --- |
| Completed foundation | Algebra, elementary functions, strict parser, formula graph, square solve, CLI, docs, package tooling and CI definition | Tests and local build; documented domains |
| Geometry | `M2R`, coordinate/polar helpers, hypercomplex angles, joints and mechanisms | Written geometry conventions plus deterministic fixtures from original examples |
| Visualization | Interactive component plots, domain coloring, formula editor | Preserve selected original examples, isolate optional UI dependencies, label eight components accurately |
| Wider mathematics | Rectangular/singular systems, polynomial roots, optional high precision | Explicit solution sets and branch choices; independent numerical or symbolic oracles |
| Historical utilities | `util.kd`, modular rings, number-theory experiments | Decide whether these belong in separate packages; port behavior with its own tests |

Static Euler and component plots are included as examples, not as a claim that
the Swing/applet UI has been ported. There are no hidden stubs that pretend to
implement the remaining modules. Any future native backend should implement
the same mathematical contract and be validated against the Python version.
