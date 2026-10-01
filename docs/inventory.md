# Java source migration inventory

Baseline: `954c19190ea862ee93e5e1a18295cc15f69649dd`. All 74 Java files are mapped below.

`migrated` means implemented in the Python API, `replaced` means consolidated into new tests or examples, `native` uses Python facilities, and `documented` means the original contained no executable feature. Java getter/setter spellings and AWT lifecycle methods are not a compatibility target.

The machine-readable [manifest](migration-manifest.json) records source hashes, line counts and public method names. `python tools/check_migration.py ../legacy-ultracomplexmath` verifies the exact baseline and that every declared Python target and test file exists. This inventory check is structural; regression tests and the written contracts establish behavior.

| Java source | Status | Python target / feature |
| --- | --- | --- |
| `util/basics/Matrix.java` | migrated | `matrix:Matrix` — Real matrices, row-vector rotation, translation and transpose |
| `util/basics/Sets.java` | native | Python set union, intersection, difference and isdisjoint replace the Java wrappers |
| `util/basics/Vectors.java` | migrated | `geometry:Line`, `geometry:rotate`, `geometry:to_base`, `geometry:from_base`, `geometry:angle_from_vector` — Vectors, frames, projections, rotations, intersections, closest points and 3D hypercomplex angles |
| `util/ds/BigInt.java` | migrated | `number_theory:BigInt`, `number_theory:fermat_factors`, `number_theory:generate_rsa`, `number_theory:rsa_decoder`, `number_theory:extended_gcd` — Native arbitrary integers; roots, primality, Fermat, extended Euclid and textbook RSA |
| `util/ds/Restklasse.java` | migrated | `modular:Residue`, `modular:ModularRing` — Residue arithmetic, power orbits and tables |
| `util/ds/ZModuloNZRing.java` | migrated | `modular:Residue`, `modular:ModularRing` — Residue arithmetic, power orbits and tables |
| `util/hypercomplex/Binary.java` | migrated | `numbers:Complex`, `numbers:Binary`, `numbers:Dual`, `numbers:RootSet`, `geometry:angle_from_vector`, `geometry:Line` — Closed algebras, branches, all roots, polar geometry, projections, color and oriented lines |
| `util/hypercomplex/Cartesian2D.java` | migrated | `coordinates:Cartesian2D`, `coordinates:Polar2D` — Immutable coordinate conversions and polar arithmetic |
| `util/hypercomplex/Complex.java` | migrated | `numbers:Complex`, `numbers:Binary`, `numbers:Dual`, `numbers:RootSet`, `geometry:angle_from_vector`, `geometry:Line` — Closed algebras, branches, all roots, polar geometry, projections, color and oriented lines |
| `util/hypercomplex/Dual.java` | migrated | `numbers:Complex`, `numbers:Binary`, `numbers:Dual`, `numbers:RootSet`, `geometry:angle_from_vector`, `geometry:Line` — Closed algebras, branches, all roots, polar geometry, projections, color and oriented lines |
| `util/hypercomplex/Hypercomplex.java` | migrated | `numbers:Complex`, `numbers:Binary`, `numbers:Dual`, `numbers:RootSet`, `geometry:angle_from_vector`, `geometry:Line` — Closed algebras, branches, all roots, polar geometry, projections, color and oriented lines |
| `util/hypercomplex/HypercomplexLSE.java` | migrated | `linalg:solve`, `linalg:solution_space` — Unique, rectangular, free and inconsistent systems; optional subalgebra restrictions |
| `util/hypercomplex/M2R.java` | migrated | `matrix:M2R` — Canonicalizing real 2x2 experiment, preserving the documented nonassociativity |
| `util/hypercomplex/Polynominal2D.java` | migrated | `coordinates:Cartesian2D`, `coordinates:Polar2D` — Immutable coordinate conversions and polar arithmetic |
| `util/hypercomplex/calculation/Calculation.java` | migrated | `expressions:Calculation`, `expressions:CalculationNode`, `expressions:SimpleCalculation`, `formula:Formula` — Shared validated parser and calculation tree replace duplicated operator/parse-data classes |
| `util/hypercomplex/calculation/CalculationNode.java` | migrated | `expressions:Calculation`, `expressions:CalculationNode`, `expressions:SimpleCalculation`, `formula:Formula` — Shared validated parser and calculation tree replace duplicated operator/parse-data classes |
| `util/hypercomplex/calculation/Operator.java` | migrated | `expressions:Calculation`, `expressions:CalculationNode`, `expressions:SimpleCalculation`, `formula:Formula` — Shared validated parser and calculation tree replace duplicated operator/parse-data classes |
| `util/hypercomplex/calculation/OperatorParseData.java` | migrated | `expressions:Calculation`, `expressions:CalculationNode`, `expressions:SimpleCalculation`, `formula:Formula` — Shared validated parser and calculation tree replace duplicated operator/parse-data classes |
| `util/hypercomplex/formula/Formula.java` | migrated | `formula:Formula`, `expressions:BoundFormula`, `expressions:FormulaSystem`, `expressions:Parameter` — Compiled strict formulas, legacy syntax, mutable parameter graphs and cycle detection |
| `util/hypercomplex/formula/FormulaSystem.java` | migrated | `formula:Formula`, `expressions:BoundFormula`, `expressions:FormulaSystem`, `expressions:Parameter` — Compiled strict formulas, legacy syntax, mutable parameter graphs and cycle detection |
| `util/hypercomplex/formula/Parameter.java` | migrated | `formula:Formula`, `expressions:BoundFormula`, `expressions:FormulaSystem`, `expressions:Parameter` — Compiled strict formulas, legacy syntax, mutable parameter graphs and cycle detection |
| `util/hypercomplex/mechanism/Actor.java` | migrated | `mechanisms:Actor`, `mechanisms:Freedom`, `mechanisms:Joint`, `mechanisms:Machine`, `mechanisms:Mechanism` — Articulated frame trees, axis mode, scalar freedoms and actors |
| `util/hypercomplex/mechanism/Freedom.java` | migrated | `mechanisms:Actor`, `mechanisms:Freedom`, `mechanisms:Joint`, `mechanisms:Machine`, `mechanisms:Mechanism` — Articulated frame trees, axis mode, scalar freedoms and actors |
| `util/hypercomplex/mechanism/Joint.java` | migrated | `mechanisms:Actor`, `mechanisms:Freedom`, `mechanisms:Joint`, `mechanisms:Machine`, `mechanisms:Mechanism` — Articulated frame trees, axis mode, scalar freedoms and actors |
| `util/hypercomplex/mechanism/Machine.java` | migrated | `mechanisms:Actor`, `mechanisms:Freedom`, `mechanisms:Joint`, `mechanisms:Machine`, `mechanisms:Mechanism` — Articulated frame trees, axis mode, scalar freedoms and actors |
| `util/hypercomplex/mechanism/Mechanism.java` | migrated | `mechanisms:Actor`, `mechanisms:Freedom`, `mechanisms:Joint`, `mechanisms:Machine`, `mechanisms:Mechanism` — Articulated frame trees, axis mode, scalar freedoms and actors |
| `util/hypercomplex/simpleCalculation/SimpleCalculation.java` | migrated | `expressions:Calculation`, `expressions:CalculationNode`, `expressions:SimpleCalculation`, `formula:Formula` — Shared validated parser and calculation tree replace duplicated operator/parse-data classes |
| `util/hypercomplex/simpleCalculation/SimpleCalculationNode.java` | migrated | `expressions:Calculation`, `expressions:CalculationNode`, `expressions:SimpleCalculation`, `formula:Formula` — Shared validated parser and calculation tree replace duplicated operator/parse-data classes |
| `util/hypercomplex/simpleCalculation/SimpleOperator.java` | migrated | `expressions:Calculation`, `expressions:CalculationNode`, `expressions:SimpleCalculation`, `formula:Formula` — Shared validated parser and calculation tree replace duplicated operator/parse-data classes |
| `util/hypercomplex/simpleCalculation/SimpleOperatorParseData.java` | migrated | `expressions:Calculation`, `expressions:CalculationNode`, `expressions:SimpleCalculation`, `formula:Formula` — Shared validated parser and calculation tree replace duplicated operator/parse-data classes |
| `util/hypercomplex/ultracomplex/Component.java` | migrated | `core:Ultra` — Immutable coefficients and basis units replace Component; channel functions, Euler components and explicit domains |
| `util/hypercomplex/ultracomplex/Ultra.java` | migrated | `core:Ultra` — Immutable coefficients and basis units replace Component; channel functions, Euler components and explicit domains |
| `util/kd/Notes.java` | documented | Historical KDD topic notes preserved in docs/migration.md; no executable implementation existed |
| `util/kd/classification/Classification.java` | migrated | `classification:Classification` — Conditional boolean indications; unfinished prediction suggestions were comments only |
| `util/kd/clustering/Cluster.java` | migrated | `clustering:Clustering`, `clustering:Cluster`, `clustering:HierarchicalCluster`, `clustering:silhouette` — All five clustering methods, cuts, norms, silhouettes and deterministic generators |
| `util/kd/clustering/Clustering.java` | migrated | `clustering:Clustering`, `clustering:Cluster`, `clustering:HierarchicalCluster`, `clustering:silhouette` — All five clustering methods, cuts, norms, silhouettes and deterministic generators |
| `util/kd/clustering/HierarchicalCluster.java` | migrated | `clustering:Clustering`, `clustering:Cluster`, `clustering:HierarchicalCluster`, `clustering:silhouette` — All five clustering methods, cuts, norms, silhouettes and deterministic generators |
| `util/kd/rules/Data.java` | migrated | `rules:Data`, `rules:DataSet`, `rules:Rule`, `rules:RuleDeduction` — Apriori, support, coverage and association rules |
| `util/kd/rules/DataSet.java` | migrated | `rules:Data`, `rules:DataSet`, `rules:Rule`, `rules:RuleDeduction` — Apriori, support, coverage and association rules |
| `util/kd/rules/Rule.java` | migrated | `rules:Data`, `rules:DataSet`, `rules:Rule`, `rules:RuleDeduction` — Apriori, support, coverage and association rules |
| `util/kd/rules/RuleDeduction.java` | migrated | `rules:Data`, `rules:DataSet`, `rules:Rule`, `rules:RuleDeduction` — Apriori, support, coverage and association rules |
| `util/kd/terms/Property.java` | migrated | `concepts:Property`, `concepts:Term`, `concepts:TermDeduction`, `concepts:Thing`, `concepts:Things` — Property sets, concept graph, deduction and reduction |
| `util/kd/terms/Term.java` | migrated | `concepts:Property`, `concepts:Term`, `concepts:TermDeduction`, `concepts:Thing`, `concepts:Things` — Property sets, concept graph, deduction and reduction |
| `util/kd/terms/TermDeduction.java` | migrated | `concepts:Property`, `concepts:Term`, `concepts:TermDeduction`, `concepts:Thing`, `concepts:Things` — Property sets, concept graph, deduction and reduction |
| `util/kd/terms/Thing.java` | migrated | `concepts:Property`, `concepts:Term`, `concepts:TermDeduction`, `concepts:Thing`, `concepts:Things` — Property sets, concept graph, deduction and reduction |
| `util/kd/terms/Things.java` | migrated | `concepts:Property`, `concepts:Term`, `concepts:TermDeduction`, `concepts:Thing`, `concepts:Things` — Property sets, concept graph, deduction and reduction |
| `util/tests/BigIntTest.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/BinaryNumberTests.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/CalculationTest.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/ComplexNumberTests.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/DualNumberTests.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/FormulaTest.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/GuesserTest.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/HypercomplexAnglesTest.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/HypercomplexJointTest.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/HypercomplexLSETest.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/HypercomplexParseTest.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/M2RMatrixTests.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/TestHypercomplexTrigonometrics.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/Tests.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/UltraBugTest.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/UltraPerformanceTest.java` | replaced | Reproducible timing harness in tools/benchmark.py; no Java speed claim |
| `util/tests/UltraTest.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/VectorTests.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tests/ZModuloNZRingTests.java` | replaced | Deterministic pytest assertions replace JUnit / print-only exercises |
| `util/tinker/DS2Tinker.java` | replaced | `number_theory:congruent_prime`, `rules:RuleDeduction`, `concepts:TermDeduction` — Runnable demonstrations consolidated in examples/discovery.py |
| `util/tinker/PolynominalGuess.java` | migrated | `polynomial:guess`, `polynomial:Polynomial` — Newton interpolation and the next-sample guesser |
| `util/tinker/RuleAndDatasetPrinter.java` | replaced | `number_theory:congruent_prime`, `rules:RuleDeduction`, `concepts:TermDeduction` — Runnable demonstrations consolidated in examples/discovery.py |
| `util/tinker/TermPrinter.java` | replaced | `number_theory:congruent_prime`, `rules:RuleDeduction`, `concepts:TermDeduction` — Runnable demonstrations consolidated in examples/discovery.py |
| `util/visuals/ClusteringDrawer.java` | migrated | `gui:ClusteringExplorer`, `clustering:generate_clusters` — Interactive method switching and data regeneration; unfinished generators given seeded alternatives |
| `util/visuals/ComplexClusteringTest.java` | migrated | `gui:FormulaExplorer`, `visuals:domain_color_grid`, `visuals:cluster_domain` — Domain coloring, grid overlays and weighted four-dimensional pixel clustering |
| `util/visuals/HypercomplexDrawer.java` | migrated | `gui:FormulaExplorer`, `visuals:domain_color_grid` — Color planes and arbitrary coefficient projections; vector field, keyboard and click probe |
| `util/visuals/HypercomplexDrawer2.java` | migrated | `gui:FormulaExplorer`, `visuals:domain_color_grid` — Color planes and arbitrary coefficient projections; vector field, keyboard and click probe |
| `util/visuals/formulaDrawer/FormulaDrawer.java` | migrated | `gui:FormulaExplorer`, `visuals:sample_curve` — Live formula editor, all eight component traces, parametric paths, ranges and image export |

## Non-Java repository files

| Original | Replacement / disposition |
| --- | --- |
| `.classpath` | Eclipse/Java project metadata replaced by pyproject.toml, lockfiles and CI |
| `.project` | Eclipse/Java project metadata replaced by pyproject.toml, lockfiles and CI |
| `.settings/org.eclipse.jdt.core.prefs` | Eclipse/Java project metadata replaced by pyproject.toml, lockfiles and CI |
| `README.md` | Preserved verbatim in docs/historical-readme.md; current README documents verified behavior |
| `bin/.gitignore` | Obsolete applet launch/security/build files; replaced by ultracomplex-gui and modern package tooling |
| `bin/java.policy.applet` | Obsolete applet launch/security/build files; replaced by ultracomplex-gui and modern package tooling |
| `bin/util.visuals.HypercomplexDrawer1494018281955.html` | Obsolete applet launch/security/build files; replaced by ultracomplex-gui and modern package tooling |
| `bin/util.visuals.HypercomplexDrawer1494018312012.html` | Obsolete applet launch/security/build files; replaced by ultracomplex-gui and modern package tooling |
| `bin/util.visuals.HypercomplexDrawer1494018333119.html` | Obsolete applet launch/security/build files; replaced by ultracomplex-gui and modern package tooling |
| `hs_err_pid5192.log` | Historical JVM crash log, not executable project functionality; remains in the original repository |
| `lib/miglayout-4.0-swing.jar` | Swing layout dependency replaced by optional Matplotlib; not redistributed |
