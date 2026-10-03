# Migration guide

Version 0.2.0 covers every implemented feature family in the original 74 Java
files. The [inventory](inventory.md) and [machine-readable manifest](migration-manifest.json)
map source files, source hashes, public method names, Python entry points and
regression files. The [historical README](historical-readme.md) preserves the
original text and image references.

No Java binaries, applet permission files, Eclipse metadata, bundled Swing JAR
or JVM crash dump are needed by the Python package. Their disposition is listed
in the inventory. The Java repository remains unchanged.

## Version 0.3.0 additions and corrections

The [exact arithmetic](exact-arithmetic.md) and [unified geometry](unified-geometry.md)
guides describe the new APIs. `Ultra` and existing closed types retain their
numerical coefficient domain; choose `ExactUltra` or the exact closed types for
integers/Fractions. Exact and numerical domains never mix implicitly.

Python integer exponents are now dispatched before conversion to float. This
intentionally corrects wrong answers for large exponents. Boolean operands and
root degrees are consistently rejected in closed types. Normalization and
projection now use scale-stable vector calculations; a zero direction raises
`DomainError`. Tiny vector angles and non-null split polar forms no longer
vanish just because an intermediate square underflows.

Complex integer `.power(n, branch=k)` now returns the same integer power for
every valid branch, including at zero. It does not take a logarithm just because
`k` is nonzero. Branch arguments must be Python integers; nonzero logarithm
branches remain unavailable in the real split and dual closed types.

Existing `.angle`, `.angle_to()`, `.length`, Euclidean projection and mirror
names keep their geometric conventions. Intrinsic metrics and the oriented
start-to-end `QuadraticPlane.angle_between` have explicit new names.
`PlaneIsometry` uses `A @ B` for applying B first, as do `ModeOperator` and
`Mobius`. The `.real` coefficient and `abs(Ultra)` keep their old meanings;
`real_part()`, `abs2()`, `amplitude()` and `phase()` are the new measurements
that retain derivatives and split structure.

The exact parser is separate from the numerical and legacy parsers. It reads
decimal literals exactly but rejects transcendental constants/functions;
`.approximate()` provides the existing numerical calculus explicitly.

## Numeric APIs

| Java | Python | Contract |
| --- | --- | --- |
| `Ultra(a,b,c,d,e,f,g,h)` | `Ultra(a,b,c,d,e,f,g,h)` | Identical basis order; immutable finite floats |
| `Component(type,value)` | `Ultra.unit(type) * value` | Components become ordinary immutable algebra values; multiply them normally |
| `Complex`, `Binary`, `Dual` | Classes with the same names | Closed 2D algebras, each with `real`, `imag`, `to_ultra()` |
| Static type reinterpretation | `Target.reinterpret(value)` | Copies two coefficients; embedding uses `to_ultra()` instead |
| `plus`, `minus`, `times`, `by`, `pow` | `+`, `-`, `*`, `/`, `**` | Scalar operands accepted on both sides |
| Setters and mutating operators | Reassignment / `with_coefficients(...)` | Numeric values remain immutable; use `from_polar` for polar changes |
| `roots(n)`, `pow(a,n)` | `roots(n)`, `rational_power(a,n)` | `RootSet.values` plus a continuous dual-zero family via `.at(t)` |
| `isLn`, `isLog`, `isPow`, `isRoot` | `is_log_of`, `is_power_of`, `is_root_of` | Explicit branch argument for powers; equality checked approximately |
| `isReal`, `isRealInteger` | `.is_real`, `.is_real_integer` | Exact tests on represented coefficients |
| `x`, `re`, `y`, `im`, getters | `.real`, `.imag`, `.cartesian`, `.polar`, `.angle`, `.length` | No duplicate Java getter spellings |
| `r0`, `r(n)`, `turnedBy` | `normalized()`, `r(n)`, `turned_by(...)` | Euclidean coefficient geometry |
| `dot`, angle/projection/mirror/Hilbert helpers | Snake-case methods on the 2D types | Preserves legacy mirror naming: radial mirror negates the parallel part |
| `det()` on 2D types | `.determinant` | `a² - square*b²` |
| `det()` on Ultra | `.determinant()` | Correct real 8×8 regular determinant, deliberately changed |
| `conjugate()` | 2D `.conjugate()`; Ultra `.conjugate("i"/"j"/"eps")` | Ultra uses algebra automorphisms instead of the defective product of sign flips |
| `eulerLength`, component Euler helpers | `.euler_length`, `.euler_angle_component(k)`, `.euler_length_component(k)` | Coefficients of the selected logarithm reconstruct an invertible Ultra by exponentiation |
| `diagonalBasis`, `nullBasis` | Binary `.diagonal`, `.null_basis` and inverse class methods | The two idempotent-channel coefficients |
| `hyperbolicForm`, `fromHyperbolicForm` | Binary `.hyperbolic_form()`, `.from_hyperbolic(...)` | Radius, sector unit and rapidity; null rays raise `DomainError` |
| `unitSpherePosition`, inverse | Dual `.unit_sphere_position()`, `.from_unit_sphere(x,y,z)` | Stereographic map, excluding the north pole |
| `containsNaN`, `nonZeroComponents` | NaN rejected at construction; `.nonzero_components` | Nonfinite values cannot be silently stored |
| Parse helpers / `parseDouble` | `Target.parse(text)`, `float(Target.parse(text))` | One unambiguous grammar; nonreal float conversion raises |
| Approximate equals, hash, ordering | Exact `==`/hash; `.isclose`; sort with an explicit key | No implicit mathematical ordering of complex values |

All elementary and reciprocal/inverse trig/hyperbolic operations exist on both
Ultra and the closed types. `log(branch=...)` selects complex branches;
`Ultra.log(branches=(plus,minus))` selects each complex channel independently.
Full Ultra functions may leave an embedded 2D subalgebra. Closed-type operations
raise when their result leaves their algebra. Mixing closed types requires an
explicit reinterpretation or Ultra embedding.

## Formulas

`Formula` is a compiled strict AST with explicit multiplication. `Calculation`
is the legacy mathematical grammar, compiled into the same restricted AST:

```python
from ultracomplexmath import Calculation, BoundFormula, Parameter, FormulaSystem

assert Calculation("10_log(100) + 2î").result().real == 2
x = Parameter("x", 2)
f = BoundFormula("?²", ["x"]).set("x", x)
g = BoundFormula("sqrt(y)").set("y", f)
x.set(4)
assert g.result().real == 4
assert FormulaSystem("f=x²; x=sqrt(y); y=5").result().isclose(5)
```

Named definitions may be separated by semicolons, newlines or top-level commas;
`=` and `:=` are accepted. Inputs override definitions. `set(name, value)` changes
a definition; parameters can reference other bound formulas. No stale result
cache is used. Unbound names raise unless `BoundFormula(default_zero=True)` is
explicitly selected. Cycles, executable Python syntax and excessive expression
size/depth are rejected.

`SimpleCalculation` evaluates within one inferred or explicitly chosen 2D
algebra. It preserves split/dual conjugation and scalar geometric semantics.
Use `Calculation` for mixed units. The duplicated Java operator enums, parse-data
containers and private parsing helpers are implementation details consolidated
into `CalculationNode` and the checked AST. There is no support for injecting
unchecked mutable syntax nodes.

The weak/weakest Java parsers disagreed even on basic expressions; their accidental
results are not copied. For example `1 + 1 + 1î` consistently means `2 + i`.
Modulo is available with real operands; rounding uses `floor(real + 0.5)` as in Java.

## Geometry, mechanisms and linear systems

`geometry` exposes tuples, `add/sub/scale/dot/cross`, projection/rejection,
`rotate`, normalized bases/frames and their coordinate conversions. `Line`
provides closest points, connecting normals, intersections, normalized pairs,
dual angles and screw transformation. `angle_from_vector(v, kind)` returns both
hypercomplex direction and its algebra-dependent scale; `vector_from_angle`
is its forward map. `Matrix` supports row-vector `@` multiplication, transpose,
rotation and translation. `M2R` intentionally retains canonicalization after each
operation and **is not associative**; use `Matrix` for ordinary linear algebra.

`Joint`, `Mechanism`, `Freedom`, `Actor` and `Machine` preserve the frame-tree
model and axis mode. Changed joints take effect at `update()`. `reparent()` checks
cycles and maintains both sides of the tree. A `Machine.connect()` also creates
an actor for the connected joint. Freedoms are `stretch`, `roll`, `turn`,
`elevate`, `real`, `imag`. Repeated `Actor.act()` starts rotations from the captured
frame and does not compound them. The exactly antiparallel mechanism case now
uses a proper half-turn rather than Java's early return/inconsistent reflection.

`solve` efficiently handles unique square systems over Ultra. `solution_space`
returns all solutions, including singular/rectangular systems and zero-divisor
constraints, as `.particular + sum(t_i * basis_i)` with **real** parameters.
Use `basis_indices=(0,2)`, `(0,1)` or `(0,4)` for complex, split or dual unknowns.
Every output coefficient equation is still enforced. Contradictions raise
`InconsistentSystemError`; finite precision and the configurable pivot tolerance
remain relevant. `Polynomial.interpolate` uses divided differences; `guess`
extrapolates one next sample from the selected most recent values.

## Integer mathematics and knowledge discovery

Python `int`, sets and tuples replace their Java wrappers. Integer algorithms
are in `number_theory`; `ModularRing` supplies residue arithmetic, powers and
complete addition/multiplication tables. `integer_root` returns `None` for a
non-square unless a floor/ceiling direction is requested. Primality uses a
deterministic Miller–Rabin witness set below 2⁶⁴, probabilistic rounds above it.
Fermat factoring accepts an optional step limit. RSA is the original unpadded
textbook exercise, including the factorization/decoder demonstration.

`Clustering` stores unique finite vectors, matching the original set semantics.
It supports k-means with restarts/k selection, strict-radius self-including
DBSCAN, single/complete/average hierarchical linkage, density grid merging and
connected dense-cell subspace clustering. The historical name “subspace” is
retained; it is not a search over dimension subsets. Empty clusters are repaired,
constant-coordinate grids are defined, ordering/seeds are deterministic, and
density noise is returned explicitly. Standard silhouette excludes self-distance
from the denominator; `legacy=True` retains the old denominator convention.
Singletons have score zero. These reference algorithms favor clarity over scale.

`Classification.indication(column)` returns conditional boolean probabilities,
with `None` for empty conditions. The original proposed prediction strategy was
a TODO, not an existing classifier. `Data`, `DataSet`, `RuleDeduction` implement
Apriori with the original strict support threshold. `Rule.support` means support
of **both** sides; `.coverage` preserves old `Rule.supp()` (either side).
`RuleDeduction` defaults to legacy coverage filtering; select
`support_metric="support"` for conventional rule support. Transactions preserve
multiplicity, unlike clustering vectors.

`Things`, `Property`, `Thing`, `Term`, `TermDeduction` implement conjunctions,
implication hierarchies, graph traversal, property adoption and term reduction.
Reductions preserve aliases and rebuild immediate inclusion links. Generated
property names are deterministic identifiers. `util.kd.Notes` was documentation
only: grouping N-dimensional points, discovering dependencies in yes/no data,
and deriving hierarchies of terms; those three purposes are preserved here.

## Visuals and demonstrations

Install `.[plot]` and run `ultracomplex-gui`. A graphical Matplotlib backend is
needed for desktop windows; `--output image.png` uses the headless Agg backend.
The numerical package itself does not import Matplotlib. Paths, plots and all
widgets share the tested Python implementation.

| Java demonstration | Modern entry point |
| --- | --- |
| `FormulaDrawer` | `ultracomplex-gui`: components / paths, expression and definitions, range, plot bounds, eight labels |
| `HypercomplexDrawer` | `--view domain`, select complex/split/dual; arbitrary Ultra projections via `domain_color_grid` |
| `HypercomplexDrawer2` | `--view vectors`: arrows/WASD or mouse move the probe; `t` slider and play/pause animate formulas |
| `ComplexClusteringTest` | `--view domain-clusters`: cluster `(x,y,magnitude,angle)`; grid overlays via `contours` |
| `ClusteringDrawer` | `--view clustering`: five algorithms, parameters, three seeded generators, regenerate button |
| Joint examples | `--view mechanism`: three sliders and interactive 3D view |
| `RuleAndDatasetPrinter`, `TermPrinter`, `DS2Tinker` | `python examples/discovery.py` |
| `PolynominalGuess` | `guess(values, max_variables)` |
| `UltraPerformanceTest` | `python tools/benchmark.py`; descriptive timings with Python version, no speed assertion |

Ranges use `start, stop, samples`; view bounds use `xmin, xmax, ymin, ymax` or
`auto`. Formula sampling supports up to 10,000 points. Interactive domain and
vector views deliberately cap resolution to keep redraws usable. The sampler
accepts up to 256×256 pixels. Domain errors are gray pixels or gaps in traces;
syntax and dependency errors are reported instead of plotted as numbers.

Example corresponding to the original Ultra coefficient color renderer:

```python
from ultracomplexmath import I, J, EPS
from ultracomplexmath.visuals import domain_color_grid, cluster_domain

grid = domain_color_grid(
    "cos(x)",
    input_basis=(I + J, EPS),
    components=(0, 4),
    resolution=65,
    legacy_colors=True,
    contours=(8, 1, 0.5),
)
# None in components selects the coefficient norm, as the old negative index did.
clusters = cluster_domain(grid, k=5, weights=(1, 1, 1000, 1000))
```

The old 800×600 applet repaint threads, incidental colors/layout, unseeded random
datasets, dead commented-out experiments and broken placeholder return values
are not a behavioral contract. Existing live demonstrations have runnable
replacements; no unimplemented migration stage is hidden behind a stub.

## Validation boundaries

The normal test suite does not execute the old JUnit tests verbatim. It replaces
them with deterministic assertions and independent mathematical references.
`legacy_probe.py` and `legacy_extended_probe.py` compile selected Java paths in an
isolated encoding-normalized copy; captured observations are checked in. The
extended fixtures cover numbers, vector angles, rotation/frame conventions,
M2R, joint/child/axis endpoints and polynomial guessing. GUI callbacks are tested
with Agg and rendered for visual inspection; OS-specific window behavior is not
exercised by headless CI. Inventory validation verifies accounting and target
existence; it is not by itself proof of semantic equivalence.
