# Sources, derivations and verification

[Agenda](README.md) · [Operations atlas](operations.md) · [Applications](applications.md)

Sources checked for this agenda on 2026-10-03 (Europe/Berlin). The sources below
support the established mathematics and application models. The API designs,
prioritization and proposed combinations are this project's recommendations.
This is a focused feasibility review, not an exhaustive novelty search.

## Primary references

| Key | Reference | What it supports here |
| --- | --- | --- |
| R1 | NIST Digital Library of Mathematical Functions, [§4.14](https://dlmf.nist.gov/4.14) and [§4.23](https://dlmf.nist.gov/4.23) | Complex trigonometric functions, periodicity and inverse-function branches; does not specify Ultra's additional channel conventions |
| R2 | Tevian Dray and Corinne Manogue, [The Split Complex Numbers](https://books.physics.oregonstate.edu/GELG/csplit.html) | Split quadratic form, null directions, idempotents and Lorentz-boost exponential |
| R3 | Vladimir V. Kisil, [Erlangen Program at Large—2: Inventing a wheel. The parabolic one](https://arxiv.org/abs/0707.4024), 2007/2010 | Elliptic/parabolic/hyperbolic geometry and Möbius transformations; distinguishes a geometric parabolic construction from the simple dual exponential |
| R4 | JAX, [The autodiff cookbook: JVPs and VJPs](https://docs.jax.dev/en/latest/301/cookbook.html#complex-numbers-and-differentiation) | Real-linear differentiation of complex functions, including non-holomorphic functions; a comparison framework for AD APIs |
| R5 | JuliaDiff, [HyperDualNumbers.jl documentation](https://juliadiff.org/HyperDualNumbers.jl/dev/), with its reference to Fike and Alonso's 2011 paper | Independent nilpotent directions and their mixed coefficient for first/second derivatives; a working implementation precedent |
| R6 | Awad H. Al-Mohy and Nicholas J. Higham, [Computing the Fréchet Derivative of the Matrix Exponential, with an Application to Condition Number Estimation](https://eprints.maths.manchester.ac.uk/1218/), 2009; [DOI](https://doi.org/10.1137/080716426) | Matrix-function sensitivity and established numerical methods; why scalar derivative multiplication is insufficient for noncommuting matrix perturbations |
| R7 | TU Delft, Konijnenberg, Adam and Urbach, [Interactive Optics: Polarisation](https://interactivetextbooks.tudelft.nl/interactive-optics/content/Chap4_Polarisation/Polarization_2022_01Clean.html) | Complex Jones vectors, phase plates, polarizers and Jones matrices as the physical model for the operator proposal |
| R8 | D. Han, Y. S. Kim and M. E. Noz, [Jones-matrix Formalism as a Representation of the Lorentz Group](https://arxiv.org/abs/physics/9703032), 1997; [DOI](https://doi.org/10.1364/JOSAA.14.002290) | Established connection between polarization transformations and Lorentz-group representations; no claim that scalar Ultra already represents the entire group |
| R9 | MIT OpenCourseWare, [Damped Harmonic Oscillators, 18.03SC](https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/pages/unit-ii-second-order-constant-coefficient-linear-equations/damped-harmonic-oscillators/), 2011 | Under-, over- and critical damping as the physical benchmark for the generalized-function proposal |
| R10 | Keith Conrad, [Hensel's lemma](https://kconrad.math.uconn.edu/blurbs/gradnumthy/hensel.pdf) | Polynomial Taylor correction and lifting modular roots under an invertible-derivative condition |
| R11 | Kevin Lynch and Frank Park, [Modern Robotics, §6.2: Numerical Inverse Kinematics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/) | Jacobian-based inverse kinematics as the existing robotics baseline; the proposed calibration/Hessian project goes beyond that demonstration |

R5's implementation documentation was inspected; its linked 2011 paper was
identified, not treated as independently read in full. Likewise R8's author
abstract and bibliographic record establish the published bridge; the detailed
operator construction used here is derived explicitly below and in the
application document, rather than attributed to an unread theorem.

## Project-specific derivations

The following statements can be checked directly from the defining relations;
they do not require a claim of novelty:

1. `p±=(1±j)/2` yields the complex-dual product decomposition. All seven
   nonreal basis directions are retained. The tensor-product and geometric
   viewpoints remain equally valid.
2. The epsilon ideal squares to zero. Hence it supports first-order lifts but
   no independent nonzero product of two tangent seeds for exact mixed Hessians.
3. For roots, expanding `(u+eps*v)^n` gives the complete per-channel tangent
   equation. Multiplying independent channel solution sets explains both n²
   unit roots and continuous families at a zero channel.
4. Multiplication plus the j-swap realizes any complex-dual 2 × 2 matrix.
   Expanding two such maps gives the documented composition law. The circular,
   hyperbolic and parabolic operator generators follow by multiplying J and S.
5. Separating even and odd terms of the exponential gives `C_kappa/S_kappa`.
   The oscillator matrix satisfies `B²=kappa*I` by direct multiplication.
6. Conjugating only i gives the real-linear intensity derivative. Summing
   fields before squaring supplies the coherent cross term.
7. The impossibility of a compatible total order, positive multiplicative norm
   or square root of eps follows from the short arguments in the agenda.
8. CRT over odd characteristic, the parity restriction over integers and the
   characteristic-two exceptions follow by factoring the defining polynomials.

These are algebraic arguments. The numerical probe provides additional
implementation evidence at selected points; it is not a proof by sampling.

## Reproducible evidence

```sh
python -m pip install --no-build-isolation -e .
python tools/research_probe.py
```

The probe needs only Python and this package. Its stored output is
[verification.json](verification.json). It checks:

- the distinct cosine formulas in C/S/D and the mixed Euler factorization;
- all 16 products of the four epsilon basis directions;
- 24 seeded operator examples against direct complex body/tangent formulas;
- operator composition, anticommutation and square-zero/circular generators;
- coherent intensity and an ideal balanced interferometer, including derivatives;
- bounded generalized sine/cosine examples, their quadratic identity, and
  critical derivatives from explicit series coefficients;
- oscillator positions against a two-exponential scalar solution, plus the
  independently written regular critical-damping derivative;
- all nine constructed cube roots of a generic unit and sampled zero-root families;
- one exact Hensel lift, from 3 modulo 7 to 10 modulo 49 for `x²−2`.

On the audited run the largest absolute discrepancy among these bounded
checks was **7.11 × 10⁻¹⁵**, below their `10⁻¹¹` threshold. This is not a global
accuracy guarantee. In particular, the probe's fixed 40-term series is only a
verification aid on the small documented sample range, not a robust general
implementation. Arbitrary matrix Fréchet derivatives, noisy calibration,
projective geometry, higher-order AD and performance comparisons are still
future acceptance work.

The same report separately records current gaps, including the incorrect
`I**(2**53+1)` result. A successful identity-probe run does **not** mean that
this known defect has been fixed or that the proposed features have shipped.

The documentation change was also checked with the existing suite (**480
passing tests**), Ruff lint/format checks, mypy, the migration-inventory check,
and an sdist/wheel build. All 57 local Markdown links in the touched
documentation were checked for existing targets, including explicit anchors.
These checks preserve the migration baseline; they do not turn the research
proposals into implemented library functionality.

## Interpretation discipline

The meaningful research claims to investigate are practical: whether the
unified algebra improves expression, composition, verification or numerical
behaviour in a specified task. Physical semantics must come from the chosen
model. No source here establishes that eight scalar coordinates automatically
give a new theory of spacetime, arbitrary rotations, probability or general
second-order differentiation.
