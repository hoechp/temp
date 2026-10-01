# Audit of the Java baseline

Inspected source: [`hoechp/ultracomplexmath`, commit
`954c19190ea862ee93e5e1a18295cc15f69649dd`](https://github.com/hoechp/ultracomplexmath/tree/954c19190ea862ee93e5e1a18295cc15f69649dd).
Latest commit at inspection: 2017-05-05. Inspection and migration: 2026-10-01.

There are 74 Java source files, 16,282 physical lines, including 19 test/helper
files. The project targets Java 7 through Eclipse metadata, includes a vendored
Swing layout JAR and applet artifacts, and has no Maven/Gradle build, CI
workflow or license file. Issue [#1](https://github.com/hoechp/ultracomplexmath/issues/1)
requests documentation and structural modernization. This migration does not
modify or close that issue.

## Reproduced numerical failures

The core was compiled and run on Java 17 from a temporary normalized copy.
57 source files decode as UTF-8; 17 require Windows-1252. Original files were
not modified. The small probe does not require JUnit or the GUI JAR. This was
**not** a run of the complete legacy JUnit suite.

Machine-readable observations are in [legacy-results.json](legacy-results.json).
Reproduce with `python tools/legacy_probe.py /path/to/legacy-checkout`.

| Input / operation | Observed Java result | New behavior |
| --- | --- | --- |
| Inverse of `1+j+i-ij` | Eight NaNs | `(1+j-i+ij)/4`; product is one |
| Legacy conjugate of the same element | Zero | Explicit generator conjugations; inverse uses channel formula |
| `ln(-1)` | Eight NaNs | Principal value `pi*i` |
| `0^2` | Eight NaNs | Zero |
| `eps^2` via `pow(2)` | Eight NaNs | Zero |
| `csc(0.2+0.2j+0.2i+0.2ij)` | Spurious coefficients of order `1e16` | Explicit `NonInvertibleError` |
| Inverse of `(2,3,5,7,11,13,17,19)*1e-10` | Eight NaNs | Finite inverse |
| Inverse of the same vector scaled by `1e10` | Eight NaNs | Finite inverse |

The last trigonometric example is a **mathematical singularity**, not a missing
finite answer: its minus body channel is zero, and so is that of its sine.
The Java result arises from numerical error feeding an invalid division.

## Causes in the source

1. [`Ultra.conjugate()`](https://github.com/hoechp/ultracomplexmath/blob/954c19190ea862ee93e5e1a18295cc15f69649dd/src/util/hypercomplex/ultracomplex/Ultra.java#L182)
   flips signs of every nonzero basis coefficient independently and multiplies
   `2^m-1` factors. These flips need not preserve products such as `i*j=ij`.
   They can introduce zero divisors for an originally invertible element.
   At seven nonreal coefficients there are 127 factors; scale also magnifies
   overflow, underflow and rounding errors. `inverse()` then divides by the
   real coefficient of this product without checking invertibility.
2. `Ultra.ln()` fixes the number of series terms to one and uses recursive
   approximate normalization. The subsidiary `ln2` includes integer division
   in `2 / (2*k+1)`, which would discard subsequent terms if used with more
   steps. There is no rigorous stopping/error criterion or complete domain
   and branch contract.
3. Every `pow` uses `exp(power*ln(base))`, making ordinary integer powers of
   zero and nilpotents fail needlessly.
4. `UltraBugTest` prints values and has no assertions. Numerous inverse-function
   assertions in `UltraTest` and formula assertions are commented out. Some
   proposed round trips are not globally valid because of branch choices.
   Other tests use unseeded `Math.random` and broad shared comparisons.
5. `Ultra.ONE` and `ZERO` reference mutable objects. `Hypercomplex` uses
   approximate equality plus a string-based hash, while `Ultra` overrides
   equality without a matching value hash. These are unsuitable value semantics
   for maps and sets.
6. Production classes import `util.tests.Tests` for formatting and comparison.
   Parsing is duplicated between `Calculation` and `SimpleCalculation`, and
   formula state is mutable and recursively cached.

The original multiplication table itself agrees with the commutative quotient
algebra. All 64 basis products are checked against captured Java results and a
separate literal table in the new tests.

## Positioning and priorities

The mathematical construction is worth explaining precisely. Claims in the
original README about uniqueness, string theory or all functions working
perfectly are not evidence of correctness or a physical application. The new
README leads with definitions, examples, supported domains and verified tests.

Python was selected by the project owner. A typed, dependency-free numerical
core makes experiments and later visualization straightforward. Rust can be
considered after profiling identifies a real performance requirement; this
release makes no benchmark claim against Java and is not a speed-optimized
vectorized engine.

The highest priority was correctness of algebra and domains, then immutable
value semantics and a testable parser. Full preservation of every historical
utility and GUI requires further staged work, recorded in the inventory.
