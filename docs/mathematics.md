# Mathematical specification

## Algebra and basis

The legacy multiplication table defines

$$
A=\mathbb R[i,j,\varepsilon]/(i^2+1,j^2-1,\varepsilon^2),
$$

with all generators commuting. Equivalently it is the tensor product of the
complex, split-complex and dual real algebras. This is an associative,
commutative algebra with identity, of real dimension eight. It is not a field,
division algebra, quaternion algebra or octonion algebra.

The basis is `1, j, i, ij, eps, eps*j, eps*i, eps*ij`. Write

$$
x=a+bj+ci+dij+\varepsilon(e+fj+gi+hij).
$$

## Channel decomposition (derived from the defining relations)

The orthogonal idempotents

$$
p_+=(1+j)/2,\quad p_-=(1-j)/2,\quad
p_+p_-=0,\quad p_++p_-=1
$$

give

$$
x=(z_++\varepsilon w_+)p_+ +(z_-+\varepsilon w_-)p_-,
$$

where

$$
z_\pm=(a\pm b)+i(c\pm d),\qquad
w_\pm=(e\pm f)+i(g\pm h).
$$

Conversely, half-sums and half-differences recover the coefficients. Thus

$$
A\cong\mathbb C[\varepsilon]/(\varepsilon^2)
\times\mathbb C[\varepsilon]/(\varepsilon^2).
$$

This is an exact change of representation, not dimensionality reduction or an
approximation. Multiplication within one channel is

$$
(z+\varepsilon w)(v+\varepsilon t)=zv+\varepsilon(zt+wv).
$$

## Inverses and zero divisors

An element is invertible iff both `z+` and `z-` are nonzero. In each channel,

$$
(z+\varepsilon w)^{-1}=z^{-1}-\varepsilon w/z^2.
$$

If either body is zero, multiplication has a nontrivial kernel. For example
`1+j` annihilates `1-j`. A nilpotent part does not restore invertibility.
`is_invertible` tests represented zeros exactly, without imposing a tolerance.
Tiny nonzero bodies can therefore produce very ill-conditioned inverses.

`conjugate(generator)` flips the chosen generator and all basis products that
contain it. Each such map is an involutive algebra automorphism. It does **not**
mean the legacy product of every independent coefficient sign combination.

`determinant()` is the determinant of the **real eight-dimensional regular
representation**, i.e. the map `y -> x*y`:

$$
\det L_x = |z_+|^4 |z_-|^4.
$$

It is independent of the nilpotent part. This deliberately differs from the
legacy dimension-dependent `det()`. It must not be used as an invertibility
test in floating-point arithmetic: its magnitude can underflow or overflow.

## Elementary functions

For an analytic local choice of a complex function,

$$
f(z+\varepsilon w)=f(z)+\varepsilon w f'(z)
$$

because every term of Taylor order two or higher contains `eps²` and vanishes.
Evaluate this in each channel, then recover the original basis. `exp`, `sin`,
`cos`, `sinh`, `cosh` are entire; reciprocal and inverse functions have their
usual complex poles and branch restrictions in **each** body channel.

The complex scalar primitives come from
[Python's cmath](https://docs.python.org/3.12/library/cmath.html).
Coefficients and channel coordinates normalize signed zeros to **+0**. On a
branch cut, this selects the value given by `cmath` with positive zero in the
cut-side coordinate. Off cuts, its normal principal branches apply. This API
does not preserve independent signed-zero approaches from below and above.
On a cut away from a branch point the tangent uses the analytic continuation
of that chosen side, not a claim of two-sided differentiability of the
discontinuous principal-value map.

`sqrt(0)` is zero when its channel tangent is zero. A channel `eps*w` with
`w != 0` has no square root: a possible root must have zero body, whose square
then has zero tangent. Likewise nonzero tangents at the branch points of the
inverse functions are rejected with `DomainError`. Zero tangents do not require
evaluating a singular derivative.

All invertible elements have logarithms in **the full algebra**, including
`1+2*j`: its body channels are `3` and `-1`, so its principal logarithm uses
the complex generator. The real split-complex subalgebra alone has stricter
logarithm domains. Embedding constructors do not force results to stay inside
the original two-dimensional subalgebra.

The logarithm branches can be chosen independently with
`x.log(branches=(k_plus, k_minus))`, adding

$$
2\pi i(k_+p_+ + k_-p_-)
=\pi i(k_++k_-)+\pi ij(k_+-k_-),\quad k_\pm\in\mathbb Z.
$$

The old comment that only independent multiples of `2*pi*i` and `2*pi*ij`
are relevant misses some periods, for example `pi*i*(1+j)`.

`x**n` for integral scalar `n` uses repeated squaring and accepts nonunits when
`n >= 0`; `0**0 = 1`. Negative integers require an inverse. Exponent `0.5`
uses the principal square root. Other exponents use `exp(exponent*log(x))`
and require invertible `x`; some nonunit cases that possess other definitions
are outside this version's power API. Inverse functions are not global
inverses in both directions: generally `asin(sin(x)) != x`.

Reciprocal inverse functions use `asec=acos(inverse)`, `acsc=asin(inverse)`,
`acot=pi/2-atan`, `asech=acosh(inverse)`, `acsch=asinh(inverse)` and
`acoth=atanh(inverse)`. These formulas specify their branch conventions.

## Linear systems

For each channel, write `A=A0+eps*A1` and `b=b0+eps*b1`. Solve

$$
A_0x_0=b_0,\qquad A_0x_1=b_1-A_1x_0.
$$

Complex scaled partial pivoting is performed separately in both channels.
This handles invertible matrices whose entries are all zero divisors, e.g.
`[[p+,p-],[p-,p+]]`. A single common algebra pivot is not required.
The `solve` API supports square systems with unique solutions. It raises
`SingularSystemError` for singular or numerically rejected body matrices,
without distinguishing inconsistent from underdetermined systems.

The separate `solution_space` API expands the problem into real coefficients
and supports rectangular and singular systems. It returns a particular solution
and a basis of free directions parameterized by real scalars, or raises
`InconsistentSystemError`. Its `basis_indices` option restricts unknowns to a
chosen subspace while still enforcing every component of each equation.
Both solvers are numerical and use explicit rank/pivot tolerances.

## Numerical contract (`Ultra`)

- Real coefficients and complex channels use binary64, not symbolic or arbitrary precision.
- Inputs and computed coefficients must be finite. `NonFiniteError` or
  `OverflowError` reports overflow; some primitive overflow paths also use
  Python arithmetic exceptions. No blanket conversion to NaN is performed.
- Underflow to zero and cancellation remain possible, particularly when
  forming `a-b` or reconstructing widely separated channel magnitudes.
- Intermediate channels may overflow although all original coefficients were
  finite. There is no scaled extended-range backend in this release.
- `tan(pi/2)` with floating-point `pi` need not be an exact pole; large finite
  results near poles are possible. No tolerance-based snapping is applied.
- `abs(x)` is a Euclidean norm of eight coefficients, not a multiplicative norm.
- `==` and hashing use exact normalized coefficients, and compare Ultra values
  only. `isclose` provides explicit coefficientwise relative/absolute tolerances.
- Integer constructor arguments are converted to binary64 coefficients.
  Integer **exponents** are dispatched before this conversion and retain every
  bit. Choose `ExactUltra` for exact integer/rational **coefficients**.

The algebraic derivation above explains the algorithm. It does not establish
any proposed physical interpretation or novelty claim.

## Exact coefficient and geometric extensions (0.3.0)

`ExactUltra` realizes the identical algebra over Q using eight Fraction
coefficients. Its [contract](exact-arithmetic.md) covers exact arithmetic,
inversion, supported rational roots, linear solution families, polynomials and
explicit conversion to the numerical specialization above.

The [geometry contract](unified-geometry.md) specifies quadratic forms, sector
angles, rational isometries, coupled operators and projective coordinates.
Operators may compose noncommutatively while scalar multiplication remains
commutative. Projective points require unimodular coordinates, not merely a
nonzero pair. Exact and approximate equality are kept separate.

`primal` and `tangent` extract the epsilon decomposition. `real_part`,
`imag_part` and `abs2` retain first variations. Numerical `amplitude` and `phase`
use real directional derivatives; phase at zero and amplitude at a zero with
nonzero tangent are rejected. At a phase cut, the tangent follows a local
continuous phase lift rather than the discontinuous principal-value function.

## Beyond the current contract

The [research agenda](research/README.md) treats the algebra as a union of
complex, split-complex and dual structures, with several equivalent useful
representations. Its [operations atlas](research/operations.md) distinguishes
geometric angle/metric choices, analytic functions and derivative-preserving
measurements. The [backlog](research/roadmap.md) now distinguishes implemented
0.3.0 features from remaining proposals. The integer-exponent defect recorded
in the original audit is corrected.
