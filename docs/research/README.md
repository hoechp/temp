# Research agenda: the full union in use

[Documentation](../README.md) · [Operation atlas](operations.md) · [Applications](applications.md) · [Roadmap](roadmap.md) · [Evidence](references.md)

This review starts from **complex, split-complex and dual algebra as a full union**, including all mixed directions. Its question is practical: which operations and constructions let this union do more useful work together?

The implementation was reassessed from [the 0.3.0 source snapshot](https://github.com/hoechp/temp/tree/fb4870cbf8a47a89b4ac10cf3ff34f37fe0cc541), with the resulting documentation, scope cleanup and exponential correction included in 0.4.0. Exact coefficients, intrinsic planar geometry, coupled operators and projective points already exist. They must no longer be listed as wholly missing features.

## The strongest findings

| Finding | Why it matters | Present status |
| --- | --- | --- |
| `i*j` is a second commuting imaginary unit | CS supports bicomplex finite-step second derivatives; epsilon can add a mixed third derivative | Derived and checked; exponential cancellation fixed; other primitives need componentwise accuracy work |
| Rational geometry extends naturally into dynamics | Cayley maps can preserve geometric forms and first variations exactly over Q | Existing API, new symplectic/reversibility checks; no general integrator yet |
| Optics, wave interfaces and impedance share transfer geometry | Phase, opposing directions, projective ratios and sensitivities can use one operator framework | Building blocks exist; physical components and stable scattering composition remain open |
| Projective boundaries are richer than one infinity | Mixed charts retain valid states when neither full coordinate is a unit | Point/map APIs exist; automatic continuation and incidence geometry are missing |
| Thermodynamic response is a strong additional candidate | Derivatives of a potential link pressure, response and parameter sensitivity | Established external multicomplex precedent; stable higher-derivative primitives are needed first |
| Modular coefficients reveal different behavior | Characteristic two turns body generators into extra nilpotents | Derived and exhaustively checked in a 256-element probe; no public backend yet |

These are opportunities grounded in algebra and existing literature. No mathematical novelty, universal superiority or engineering readiness is inferred merely from combining the generators.

## What to build first

1. **Reliable coefficient-level numerics.** Extend the exponential fix to relevant division, logarithm and trigonometric paths. A full-value norm can conceal an incorrect tiny Hessian coefficient.
2. **Exact geometric constraints and coefficient completeness.** Add rational nth roots where supported, algebraic-number boundaries, constraint Jacobians and exact rank/degeneracy classifications. This continues the owner's rational/geometric priorities.
3. **Continuous circular–hyperbolic–parabolic dynamics.** Implement stable generalized sine/cosine across the critical parameter, retaining first variations; pair them with the exact discrete Cayley framework.
4. **A differentiable transfer-network showcase.** Compose specified optical or wave components, verify flux/passivity assumptions and derivatives, then solve an identifiable inverse problem.

The [roadmap](roadmap.md) supplies dependencies and completion criteria. [Applications](applications.md) compares usefulness, fit and prerequisites. [Experiments](experiments.md) gives derivations and reproducible checks.

## Read the claims precisely

- **Implemented:** a callable interface and tests exist here.
- **Verified experiment:** a bounded script checks the stated example; it is not a production API.
- **Derived:** a mathematical consequence of explicit assumptions.
- **Proposed:** implementation and application validation remain necessary.

The operation atlas examines C, S, D, CS, CD, SD and CSD in every domain. Split eigenspaces are one useful representation of the union, not its identity; they can also be the wrong numerical coordinates for tiny mixed components.
