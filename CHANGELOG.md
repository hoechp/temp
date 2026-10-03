# Changelog

## 0.3.0 — exact coefficients and unified geometry, unpublished on PyPI

- Fix integer exponent rounding before dispatch, including the closed types:
  `I ** (2**53 + 1) == I`, and preserve arbitrarily large positive/negative ints.
- Keep complex integer powers independent of the chosen logarithm branch,
  including powers of zero; validate branch types consistently.
- Fix scale-dependent normalization/projection in vectors, closed types and
  formulas; retain tiny angles; avoid false split-polar and vector-angle
  singularities from squaring extremely small or large lengths.
- Make closed-type scalar and root-degree bool rejection consistent with Ultra.
- Add Fraction-backed ExactUltra, ExactComplex, ExactBinary and ExactDual with
  exact arithmetic, unit detection, inverses, rational principal square roots,
  tangent operations and lossless rational coefficient JSON representation.
- Add exact decimal formulas and `--exact` CLI; numerical conversion is explicit.
- Add exact matrices, complete rational solution families, polynomial algebra,
  calculus, interpolation and Hermite interpolation.
- Add explicit circular/hyperbolic/parabolic metrics, sectors, angle parameters,
  rational Cayley factors, affine isometries, reflections and homogeneous matrices.
- Add exact orientation, line/segment intersections, barycentric coordinates,
  circumcircles and winding-independent incircle predicates.
- Add coupled ModeOperator composition/inversion and exact Cayley maps across
  the elliptic/parabolic/hyperbolic transition, including parameter sensitivities.
- Add Möbius transformations, unimodular projective points and cross ratios
  over both numerical and exact eight-dimensional values.
- Add derivative-preserving numerical amplitude, phase, real/imaginary parts
  and intensity; make these measurements available to numerical formulas.
- Add 186 tests, an executable exact-geometry demonstration and a reproducible
  figure; update the research backlog with implemented and remaining scope.

### Visual laboratory carried forward from the previous development snapshot

- Add six reproducible figures, a coupled-mode animation and an offline HTML lab.
- Revisit the original cosine maps and Euler curves with the migrated engine.
- Visualize hypercomplex angles, eight coefficient traces and nine Newton basins.
- Demonstrate two coupled modes and their parameter derivatives in one exponential.
- Document the mathematics, sample grids and color encodings; add independent checks.
- Restore the original cosine color mapping and domain; add a direct comparison
  of hyperbola, circle and line slices through the three cosine functions.
- Add travelling waves, planar robot inverse kinematics and interference-based
  parameter reconstruction, with four figures, two animations and scalar oracles.
- Use channel-specific dual seeds to obtain both robot Jacobian columns in one
  evaluation; use source-field derivatives to fit noisy intensity measurements.

## 0.2.0 — complete feature migration, unpublished on PyPI

- Restore closed Complex/Binary/Dual types, roots, branches and geometric APIs.
- Add coordinates, vectors, lines, matrices and the historical M2R experiment.
- Add joint/actor/mechanism trees with freedoms, cycle checks and axis mode.
- Add rectangular/free/inconsistent systems and polynomial interpolation.
- Restore legacy expression syntax, live shared parameters and formula systems.
- Migrate integer/RSA exercises, modular rings, all five clustering methods,
  conditional classification, association rules and concept hierarchies.
- Replace applets/Swing with interactive desktop formula, domain, vector,
  clustering and mechanism explorers; keep plotting optional.
- Add deterministic regressions, compiled Java geometry fixtures and a checked
  inventory for all 74 Java sources and 11 ancillary files.
- Preserve the historical README and document all deliberate API differences.

## 0.1.0 — prepared, unpublished

- Port the eight-component algebra to immutable, typed Python values.
- Replace the 127-factor inverse and approximate logarithm with channel calculus.
- Correct powers of zero and nilpotents; expose zero divisors and domain errors.
- Implement elementary, trigonometric, hyperbolic and inverse functions.
- Add restricted formula parsing, dependency evaluation and square linear solves.
- Add a command-line calculator and optional static plotting examples.
- Add reproducible tests, developer lock files, package build and CI configuration.
- Record the Java baseline, reproduced failures and every source file's migration status.
- License the migration under 0BSD as requested by the original author.
