# Complete Java source inventory

Baseline: `hoechp/ultracomplexmath@954c19190ea862ee93e5e1a18295cc15f69649dd`.

Every Java file is accounted for. Pending means it is **not implemented** in this release.

| Original file | Lines | Migration status |
| --- | ---: | --- |
| `util/basics/Matrix.java` | 169 | Matrix/vector utilities pending; square algebra systems covered by solve |
| `util/basics/Sets.java` | 59 | Matrix/vector utilities pending; square algebra systems covered by solve |
| `util/basics/Vectors.java` | 399 | Matrix/vector utilities pending; square algebra systems covered by solve |
| `util/ds/BigInt.java` | 461 | Out of core scope; arbitrary integers already native to Python; other algorithms pending |
| `util/ds/Restklasse.java` | 71 | Out of core scope; arbitrary integers already native to Python; other algorithms pending |
| `util/ds/ZModuloNZRing.java` | 119 | Out of core scope; arbitrary integers already native to Python; other algorithms pending |
| `util/hypercomplex/Binary.java` | 832 | Embedded in Ultra.split; closed-subalgebra restrictions not retained |
| `util/hypercomplex/Cartesian2D.java` | 168 | Coordinate containers replaced by immutable numeric coefficients |
| `util/hypercomplex/Complex.java` | 1078 | Embedded in Ultra.complex; geometry and subclass API pending |
| `util/hypercomplex/Dual.java` | 748 | Embedded in Ultra.dual; geometry helpers pending |
| `util/hypercomplex/Hypercomplex.java` | 2207 | Arithmetic consolidated; geometry, parsing quirks and convenience methods only partly replaced |
| `util/hypercomplex/HypercomplexLSE.java` | 353 | Square unique systems replaced by channel solve; rectangular systems pending |
| `util/hypercomplex/M2R.java` | 148 | 2x2 matrix classification and embedding API pending |
| `util/hypercomplex/Polynominal2D.java` | 166 | Polar-coordinate helpers pending |
| `util/hypercomplex/calculation/Calculation.java` | 251 | Replaced by restricted AST Formula |
| `util/hypercomplex/calculation/CalculationNode.java` | 180 | Replaced by restricted AST Formula |
| `util/hypercomplex/calculation/Operator.java` | 106 | Replaced by restricted AST Formula |
| `util/hypercomplex/calculation/OperatorParseData.java` | 33 | Replaced by restricted AST Formula |
| `util/hypercomplex/formula/Formula.java` | 348 | Formula and evaluate_system; mutable API not retained |
| `util/hypercomplex/formula/FormulaSystem.java` | 248 | Formula and evaluate_system; mutable API not retained |
| `util/hypercomplex/formula/Parameter.java` | 52 | Formula and evaluate_system; mutable API not retained |
| `util/hypercomplex/mechanism/Actor.java` | 111 | Pending: geometric semantics and kinematics need separate specification |
| `util/hypercomplex/mechanism/Freedom.java` | 80 | Pending: geometric semantics and kinematics need separate specification |
| `util/hypercomplex/mechanism/Joint.java` | 131 | Pending: geometric semantics and kinematics need separate specification |
| `util/hypercomplex/mechanism/Machine.java` | 30 | Pending: geometric semantics and kinematics need separate specification |
| `util/hypercomplex/mechanism/Mechanism.java` | 185 | Pending: geometric semantics and kinematics need separate specification |
| `util/hypercomplex/simpleCalculation/SimpleCalculation.java` | 250 | Consolidated into Formula; intentional syntax changes |
| `util/hypercomplex/simpleCalculation/SimpleCalculationNode.java` | 229 | Consolidated into Formula; intentional syntax changes |
| `util/hypercomplex/simpleCalculation/SimpleOperator.java` | 122 | Consolidated into Formula; intentional syntax changes |
| `util/hypercomplex/simpleCalculation/SimpleOperatorParseData.java` | 33 | Consolidated into Formula; intentional syntax changes |
| `util/hypercomplex/ultracomplex/Component.java` | 179 | Replaced by immutable Ultra and channel calculus |
| `util/hypercomplex/ultracomplex/Ultra.java` | 668 | Replaced by immutable Ultra and channel calculus |
| `util/kd/Notes.java` | 19 | Out of core scope; keep original, decide on a separate package |
| `util/kd/classification/Classification.java` | 62 | Out of core scope; keep original, decide on a separate package |
| `util/kd/clustering/Cluster.java` | 41 | Out of core scope; keep original, decide on a separate package |
| `util/kd/clustering/Clustering.java` | 856 | Out of core scope; keep original, decide on a separate package |
| `util/kd/clustering/HierarchicalCluster.java` | 137 | Out of core scope; keep original, decide on a separate package |
| `util/kd/rules/Data.java` | 35 | Out of core scope; keep original, decide on a separate package |
| `util/kd/rules/DataSet.java` | 53 | Out of core scope; keep original, decide on a separate package |
| `util/kd/rules/Rule.java` | 62 | Out of core scope; keep original, decide on a separate package |
| `util/kd/rules/RuleDeduction.java` | 141 | Out of core scope; keep original, decide on a separate package |
| `util/kd/terms/Property.java` | 34 | Out of core scope; keep original, decide on a separate package |
| `util/kd/terms/Term.java` | 205 | Out of core scope; keep original, decide on a separate package |
| `util/kd/terms/TermDeduction.java` | 208 | Out of core scope; keep original, decide on a separate package |
| `util/kd/terms/Thing.java` | 21 | Out of core scope; keep original, decide on a separate package |
| `util/kd/terms/Things.java` | 112 | Out of core scope; keep original, decide on a separate package |
| `util/tests/BigIntTest.java` | 66 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/BinaryNumberTests.java` | 169 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/CalculationTest.java` | 34 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/ComplexNumberTests.java` | 379 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/DualNumberTests.java` | 197 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/FormulaTest.java` | 194 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/GuesserTest.java` | 17 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/HypercomplexAnglesTest.java` | 162 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/HypercomplexJointTest.java` | 64 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/HypercomplexLSETest.java` | 59 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/HypercomplexParseTest.java` | 62 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/M2RMatrixTests.java` | 255 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/TestHypercomplexTrigonometrics.java` | 279 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/Tests.java` | 136 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/UltraBugTest.java` | 22 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/UltraPerformanceTest.java` | 258 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/UltraTest.java` | 338 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/VectorTests.java` | 90 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tests/ZModuloNZRingTests.java` | 26 | Selected core fixtures and regressions replaced; not a line-for-line JUnit port |
| `util/tinker/DS2Tinker.java` | 57 | Historical experiments; not ported |
| `util/tinker/PolynominalGuess.java` | 88 | Historical experiments; not ported |
| `util/tinker/RuleAndDatasetPrinter.java` | 28 | Historical experiments; not ported |
| `util/tinker/TermPrinter.java` | 77 | Historical experiments; not ported |
| `util/visuals/ClusteringDrawer.java` | 207 | Applet/Swing UI not ported; new static example plots replace selected demonstrations |
| `util/visuals/ComplexClusteringTest.java` | 194 | Applet/Swing UI not ported; new static example plots replace selected demonstrations |
| `util/visuals/HypercomplexDrawer.java` | 150 | Applet/Swing UI not ported; new static example plots replace selected demonstrations |
| `util/visuals/HypercomplexDrawer2.java` | 225 | Applet/Swing UI not ported; new static example plots replace selected demonstrations |
| `util/visuals/formulaDrawer/FormulaDrawer.java` | 249 | Applet/Swing UI not ported; new static example plots replace selected demonstrations |
