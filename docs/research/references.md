# Sources and evidence

[Agenda](README.md) · [Experiments](experiments.md) · [Roadmap](roadmap.md)

Sources checked for the renewed review on 2026-10-03 (UTC). Established background is separate from project derivations, implementation findings and proposals. This is a focused feasibility review, not an exhaustive novelty search.

## Primary sources

| Key | Source | Use and scope |
| --- | --- | --- |
| R1 | Dray and Manogue, [The Split Complex Numbers](https://books.physics.oregonstate.edu/GELG/csplit.html) | Split forms, null directions and boosts |
| R2 | Kisil, [Erlangen Program at Large—2: Inventing a wheel. The parabolic one](https://arxiv.org/abs/0707.4024) | Broader elliptic/parabolic/hyperbolic geometry; a dual shear is not all of parabolic geometry |
| R3 | Havlicek, [Projective Ring Lines and Their Generalisations](https://arxiv.org/abs/1210.1921) | Ring-line background; the specialized chart criterion is derived here |
| R4 | Deiters and Bell, [Precise Numerical Differentiation of Thermodynamic Functions with Multicomplex Variables](https://pmc.ncbi.nlm.nih.gov/articles/PMC11424140/) | Mixed derivatives, thermodynamic use and numerical limitations; not evidence of a shipped Ultra Hessian API |
| R5 | Hairer, [Geometric Numerical Integration, Lecture 2](https://unige.ch/~hairer/poly_geoint/week2.pdf), 2010 | Midpoint, symplecticity and quadratic invariants; the exact Cayley identities here are derived explicitly |
| R6 | Monzón and Sánchez-Soto, [Origin of the Thomas rotation that arises in lossless multilayers](https://opg.optica.org/josaa/abstract.cfm?uri=josaa-16-11-2786), 1999 | Author abstract establishes the multilayer/SU(1,1)/Lorentz bridge; paywalled details were not used |
| R7 | Al-Mohy and Higham, [Computing the Fréchet Derivative of the Matrix Exponential](https://eprints.maths.manchester.ac.uk/1218/), 2009 | Matrix sensitivity/conditioning and noncommuting perturbations |
| R8 | Lynch and Park, [Modern Robotics §6.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/) | Jacobian-based inverse kinematics; exact constraint graphs are a further proposal |
| R9 | Keith Conrad, [Hensel's lemma](https://kconrad.math.uconn.edu/blurbs/gradnumthy/hensel.pdf) | Simple-root lifting and its derivative condition |
| R10 | Swastik Kopparty, [Some remarks on multiplicity codes](https://arxiv.org/abs/1505.07547) | Finite-field polynomial/derivative evaluations; no coding backend is shipped |
| R11 | NIST DLMF, [§4.14](https://dlmf.nist.gov/4.14), [§4.23](https://dlmf.nist.gov/4.23) | Complex trigonometry and inverse branches |
| R12 | JAX authors, [Complex numbers and differentiation](https://docs.jax.dev/en/latest/301/cookbook.html#complex-numbers-and-differentiation) | Real-linear complex differentiation as an ecosystem comparison; no JAX adapter exists here |

The [implemented applications](../gallery/applications.md) also cite their own physical-model sources. References support only the background they discuss; actual package behavior is checked locally.

## Project-specific derivations

The seven subalgebras, unit criterion and epsilon ideal follow from the defining relations. This review additionally derives the bicomplex extraction sign, Cayley symplectic/quadratic identities, transfer/Riccati correspondence and characteristic-two presentation. Root tangent equations and limits on order, norms and rational closure follow similarly. These are direct calculations, not novelty claims.

## Reproduce

```sh
python tools/research_probe.py
python tools/frontier_probe.py
python -m examples.exact_geometry
python -m pytest
```

| Evidence | Coverage | Limit |
| --- | --- | --- |
| [research_probe.py](../../tools/research_probe.py), [verification.json](verification.json) | Trig/operator identities, intensity, critical series, unit-root examples, one Hensel lift | Selected bounded cases; not a general function library |
| [frontier_probe.py](../../tools/frontier_probe.py), [frontier-verification.json](frontier-verification.json) | Mixed derivatives, exact steps/maps, exhaustive F2 and rational-power gap | Specified functions/ranges and one small finite ring |
| [Component regression tests](../../tests/test_component_accuracy.py) | Tiny exponential coefficients and compensated large values | Does not certify every other function |
| [Exact geometry example](../../examples/exact_geometry.py) | Rational constructions/invariants | Float conversion only for display |
| [Gallery tests](../../tests/test_gallery.py), [application tests](../../tests/test_applications.py) | Independent formulas, conservation, roots and inverse problems | Idealized models, not real-hardware measurements |

Checked-in figure reports describe their full render datasets; routine CI checks the models without regenerating all assets. New probes record version/source context. Tests, lint, formatting, typing, documentation checks, probes and builds protect this release. Their success does not imply that every proposed feature exists or every numerical corner case has been eliminated.
