"""The real algebra R[i, j, eps] / (i²+1, j²-1, eps²).

All generators commute. Public coefficients retain the original Java order:
1, j, i, ij, eps, eps*j, eps*i, eps*ij.
"""

from __future__ import annotations

import cmath
import math
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, fields
from typing import Literal


class NonInvertibleError(ZeroDivisionError):
    """At least one complex body channel is zero (a zero divisor or zero)."""


class DomainError(ValueError):
    """The requested principal function is undefined at this argument."""


class NonFiniteError(ArithmeticError):
    """A coefficient or intermediate result is outside finite float arithmetic."""


type Channel = tuple[complex, complex]
type Scalar = "Ultra | int | float | complex"
type ComplexFunction = Callable[[complex], complex]
BASIS = ("1", "j", "i", "i*j", "eps", "eps*j", "eps*i", "eps*i*j")


def _canonical(z: complex) -> complex:
    """Choose +0 on both cut coordinates; coefficient storage has no cut-side bit."""
    return complex(z.real or 0.0, z.imag or 0.0)


def _finite(z: complex) -> complex:
    if not cmath.isfinite(z):
        raise NonFiniteError("Complex channel overflowed finite floating-point range")
    return _canonical(z)


def _half_sum(a: float, b: float) -> float:
    total = a + b
    return total / 2 if math.isfinite(total) else a / 2 + b / 2


@dataclass(frozen=True, slots=True)
class Ultra:
    """Immutable eight-component number with exact equality and explicit isclose.

    Arithmetic accepts Ultra, int, float and Python complex operands. Constructors
    and operations reject NaN and infinity. Use ``coefficients`` for serialization.
    """

    real: float = 0.0
    j: float = 0.0
    i: float = 0.0
    ij: float = 0.0
    eps: float = 0.0
    eps_j: float = 0.0
    eps_i: float = 0.0
    eps_ij: float = 0.0

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"{field.name} must be a real int or float")
            value = float(value)
            if not math.isfinite(value):
                raise NonFiniteError(f"{field.name} must be finite")
            object.__setattr__(self, field.name, value or 0.0)

    @classmethod
    def coerce(cls, value: Scalar) -> Ultra:
        """Embed a real/complex scalar or return an existing Ultra unchanged."""
        if isinstance(value, cls):
            return value
        if isinstance(value, bool):
            raise TypeError("Boolean values are not algebra scalars")
        if isinstance(value, complex):
            return cls(real=value.real, i=value.imag)
        if isinstance(value, (int, float)):
            return cls(real=value)
        raise TypeError(f"Cannot embed {type(value).__name__} in Ultra")

    @classmethod
    def from_coefficients(cls, values: Iterable[float]) -> Ultra:
        coefficients = tuple(values)
        if len(coefficients) != 8:
            raise ValueError("Exactly eight coefficients are required")
        return cls(*coefficients)

    @classmethod
    def unit(cls, index: int) -> Ultra:
        if type(index) is not int or not 0 <= index < 8:
            raise ValueError("Basis index must be an integer in 0..7")
        return cls(*(float(k == index) for k in range(8)))

    @classmethod
    def complex(cls, real: float, imag: float = 0.0) -> Ultra:
        return cls(real=real, i=imag)

    @classmethod
    def split(cls, real: float, imag: float = 0.0) -> Ultra:
        return cls(real=real, j=imag)

    @classmethod
    def dual(cls, real: float, tangent: float = 0.0) -> Ultra:
        return cls(real=real, eps=tangent)

    @property
    def coefficients(self) -> tuple[float, ...]:
        return (self.real, self.j, self.i, self.ij, self.eps, self.eps_j, self.eps_i, self.eps_ij)

    def __iter__(self) -> Iterator[float]:
        return iter(self.coefficients)

    def __str__(self) -> str:
        terms = []
        for coefficient, basis in zip(self, BASIS, strict=True):
            if coefficient:
                # repr preserves enough digits to round-trip through Formula.
                term = repr(abs(coefficient))
                if basis != "1":
                    term += "*" + basis
                sign = "-" if coefficient < 0 else "+"
                terms.append((sign, term))
        if not terms:
            return "0"
        first_sign, first = terms[0]
        return (
            ("-" if first_sign == "-" else "")
            + first
            + "".join(f" {sign} {term}" for sign, term in terms[1:])
        )

    def __bool__(self) -> bool:
        return any(self)

    @property
    def nonzero_components(self) -> tuple[tuple[int, float], ...]:
        return tuple((i, c) for i, c in enumerate(self) if c)

    def euler_angle_component(self, index: int) -> float:
        Ultra.unit(index)  # Validate the public basis index.
        return self.log().coefficients[index]

    def euler_length_component(self, index: int) -> float:
        return math.exp(self.euler_angle_component(index))

    @property
    def euler_length(self) -> float:
        return self.euler_length_component(0)

    def __abs__(self) -> float:
        """Euclidean coefficient norm; not a multiplicative algebra norm."""
        return math.hypot(*self)

    def isclose(self, other: Scalar, *, rel_tol: float = 1e-10, abs_tol: float = 1e-12) -> bool:
        """Compare each coefficient; approximate equality is never used by ==."""
        value = self.coerce(other)
        return all(
            math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)
            for a, b in zip(self, value, strict=True)
        )

    def __neg__(self) -> Ultra:
        return Ultra(*(-x for x in self))

    def __pos__(self) -> Ultra:
        return self

    def __add__(self, other: Scalar) -> Ultra:
        try:
            value = self.coerce(other)
        except TypeError:
            return NotImplemented
        return Ultra(*(a + b for a, b in zip(self, value, strict=True)))

    __radd__ = __add__

    def __sub__(self, other: Scalar) -> Ultra:
        try:
            value = self.coerce(other)
        except TypeError:
            return NotImplemented
        return self + -value

    def __rsub__(self, other: Scalar) -> Ultra:
        return self.coerce(other) - self

    def __mul__(self, other: Scalar) -> Ultra:
        try:
            value = self.coerce(other)
        except TypeError:
            return NotImplemented
        # Coefficient multiplication avoids unnecessary channel cancellation.
        terms: list[list[float]] = [[] for _ in range(8)]
        for a, x in enumerate(self):
            for b, y in enumerate(value):
                common = a & b
                if common & 4 or x == 0 or y == 0:  # eps² = 0
                    continue
                terms[a ^ b].append((-1 if common & 2 else 1) * x * y)
        return Ultra(*(math.fsum(term) for term in terms))

    __rmul__ = __mul__

    def channels(self) -> tuple[Channel, Channel]:
        """Return (z+, w+), (z-, w-) for z + eps*w in each j eigenspace."""
        return (
            (
                _finite(complex(self.real + self.j, self.i + self.ij)),
                _finite(complex(self.eps + self.eps_j, self.eps_i + self.eps_ij)),
            ),
            (
                _finite(complex(self.real - self.j, self.i - self.ij)),
                _finite(complex(self.eps - self.eps_j, self.eps_i - self.eps_ij)),
            ),
        )

    @classmethod
    def from_channels(cls, plus: Channel, minus: Channel) -> Ultra:
        zp, wp = map(_finite, map(complex, plus))
        zm, wm = map(_finite, map(complex, minus))
        # Avoid both overflow in a+b and premature underflow in a/2+b/2.
        a = complex(_half_sum(zp.real, zm.real), _half_sum(zp.imag, zm.imag))
        b = complex(_half_sum(zp.real, -zm.real), _half_sum(zp.imag, -zm.imag))
        c = complex(_half_sum(wp.real, wm.real), _half_sum(wp.imag, wm.imag))
        d = complex(_half_sum(wp.real, -wm.real), _half_sum(wp.imag, -wm.imag))
        return cls(a.real, b.real, a.imag, b.imag, c.real, d.real, c.imag, d.imag)

    @property
    def is_invertible(self) -> bool:
        plus, minus = self.channels()
        return plus[0] != 0 and minus[0] != 0

    def inverse(self) -> Ultra:
        result = []
        for label, (z, w) in zip(("+", "-"), self.channels(), strict=True):
            if z == 0:
                raise NonInvertibleError(f"Zero body in {label} channel; no multiplicative inverse")
            result.append((_finite(1 / z), _finite(-(w / z) / z)))
        return Ultra.from_channels(result[0], result[1])

    def __truediv__(self, other: Scalar) -> Ultra:
        value = self.coerce(other)
        # Divide channels directly to avoid forming an overflowing reciprocal.
        result = []
        for (z, w), (v, t) in zip(self.channels(), value.channels(), strict=True):
            if v == 0:
                raise NonInvertibleError("Divisor has a zero body channel")
            body = _finite(z / v)
            result.append((body, _finite(w / v - body * (t / v))))
        return Ultra.from_channels(result[0], result[1])

    def __rtruediv__(self, other: Scalar) -> Ultra:
        return self.coerce(other) / self

    def __pow__(self, exponent: Scalar) -> Ultra:
        power = self.coerce(exponent)
        if not any(power.coefficients[1:]) and power.real.is_integer():
            n = int(power.real)
            factor = self if n >= 0 else self.inverse()
            n = abs(n)
            result = ONE
            while n:
                if n & 1:
                    result = result * factor
                n >>= 1
                if n:
                    factor = factor * factor
            return result
        if power == Ultra(0.5):
            return self.sqrt()
        return (self.log() * power).exp()

    def __rpow__(self, base: Scalar) -> Ultra:
        return self.coerce(base) ** self

    def conjugate(self, generator: Literal["i", "j", "eps"] = "i") -> Ultra:
        """Flip one generator's sign, a genuine involutive algebra automorphism."""
        try:
            bit = {"i": 2, "j": 1, "eps": 4}[generator]
        except KeyError:
            raise ValueError("Generator must be i, j or eps") from None
        return Ultra(*(c * (-1 if k & bit else 1) for k, c in enumerate(self)))

    def determinant(self) -> float:
        """Determinant of the real 8×8 map y -> self*y (not Java's det())."""
        (zp, _), (zm, _) = self.channels()
        if zp == 0 or zm == 0:
            return 0.0
        result = (abs(zp) * abs(zm)) ** 4
        if not math.isfinite(result):
            raise NonFiniteError("Determinant overflow")
        return result

    def _lift(self, name: str, function: ComplexFunction, derivative: ComplexFunction) -> Ultra:
        result = []
        for label, (z, w) in zip(("+", "-"), self.channels(), strict=True):
            try:
                body = _finite(function(z))
                # sqrt(0) and asin(1) exist when no tangent is requested.
                tangent = _finite(w * derivative(z)) if w != 0 else 0j
            except (ValueError, ZeroDivisionError) as error:
                raise DomainError(
                    f"{name} undefined in {label} channel at {z}, tangent {w}"
                ) from error
            result.append((body, tangent))
        return Ultra.from_channels(result[0], result[1])

    def exp(self) -> Ultra:
        return self._lift("exp", cmath.exp, cmath.exp)

    def log(self, base: Scalar | None = None, *, branches: tuple[int, int] = (0, 0)) -> Ultra:
        """Channelwise logarithm; independent integer branches for + and - channels."""
        if len(branches) != 2 or any(type(k) is not int for k in branches):
            raise ValueError("branches must contain two integers")
        result = self._lift("log", cmath.log, lambda z: 1 / z)
        if branches != (0, 0):
            result += Ultra.from_channels(
                (2j * math.pi * branches[0], 0j), (2j * math.pi * branches[1], 0j)
            )
        return result if base is None else result / Ultra.coerce(base).log()

    ln = log

    def sqrt(self) -> Ultra:
        """Principal channel roots; reject nonzero nilpotent tangents at zero."""
        return self._lift("sqrt", cmath.sqrt, lambda z: 0.5 / cmath.sqrt(z))

    def sin(self) -> Ultra:
        return self._lift("sin", cmath.sin, cmath.cos)

    def cos(self) -> Ultra:
        return self._lift("cos", cmath.cos, lambda z: -cmath.sin(z))

    def tan(self) -> Ultra:
        return self._lift("tan", cmath.tan, lambda z: 1 + cmath.tan(z) ** 2)

    def sinh(self) -> Ultra:
        return self._lift("sinh", cmath.sinh, cmath.cosh)

    def cosh(self) -> Ultra:
        return self._lift("cosh", cmath.cosh, cmath.sinh)

    def tanh(self) -> Ultra:
        return self._lift("tanh", cmath.tanh, lambda z: 1 - cmath.tanh(z) ** 2)

    def sec(self) -> Ultra:
        return self.cos().inverse()

    def csc(self) -> Ultra:
        return self.sin().inverse()

    def cot(self) -> Ultra:
        return self.cos() / self.sin()

    def sech(self) -> Ultra:
        return self.cosh().inverse()

    def csch(self) -> Ultra:
        return self.sinh().inverse()

    def coth(self) -> Ultra:
        return self.cosh() / self.sinh()

    def asin(self) -> Ultra:
        return self._lift("asin", cmath.asin, lambda z: 1 / (cmath.sqrt(1 - z) * cmath.sqrt(1 + z)))

    def acos(self) -> Ultra:
        return self._lift(
            "acos", cmath.acos, lambda z: -1 / (cmath.sqrt(1 - z) * cmath.sqrt(1 + z))
        )

    def atan(self) -> Ultra:
        return self._lift("atan", cmath.atan, lambda z: 1 / (1 + z * z))

    def asinh(self) -> Ultra:
        return self._lift(
            "asinh", cmath.asinh, lambda z: 1 / (cmath.sqrt(1 - 1j * z) * cmath.sqrt(1 + 1j * z))
        )

    def acosh(self) -> Ultra:
        return self._lift(
            "acosh", cmath.acosh, lambda z: 1 / (cmath.sqrt(z - 1) * cmath.sqrt(z + 1))
        )

    def atanh(self) -> Ultra:
        return self._lift("atanh", cmath.atanh, lambda z: 1 / (1 - z * z))

    def asec(self) -> Ultra:
        return self.inverse().acos()

    def acsc(self) -> Ultra:
        return self.inverse().asin()

    def acot(self) -> Ultra:
        return Ultra(math.pi / 2) - self.atan()

    def asech(self) -> Ultra:
        return self.inverse().acosh()

    def acsch(self) -> Ultra:
        return self.inverse().asinh()

    def acoth(self) -> Ultra:
        return self.inverse().atanh()


ZERO = Ultra()
ONE = Ultra(1)
I = Ultra(i=1)
J = Ultra(j=1)
EPS = Ultra(eps=1)
