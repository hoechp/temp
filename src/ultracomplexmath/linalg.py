"""Solve square systems over Ultra by reducing to complex channel systems."""

from __future__ import annotations

import math
from collections.abc import Sequence

from .core import Channel, Scalar, Ultra, _finite


class SingularSystemError(ArithmeticError):
    """No unique solution, or a pivot is numerically singular at the given tolerance."""


def _solve_complex(a: list[list[complex]], b: list[complex], rtol: float) -> list[complex]:
    n = len(b)
    rows = [row.copy() + [rhs] for row, rhs in zip(a, b, strict=True)]
    scales = [max(map(abs, row)) for row in a]
    if any(scale == 0 for scale in scales):
        raise SingularSystemError("Zero row in body matrix")
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(rows[r][col]) / scales[r])
        if abs(rows[pivot][col]) <= rtol * scales[pivot]:
            raise SingularSystemError(f"Body matrix singular at column {col}; rtol={rtol}")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scales[col], scales[pivot] = scales[pivot], scales[col]
        for row in range(col + 1, n):
            ratio = rows[row][col] / rows[col][col]
            rows[row][col] = 0j
            for k in range(col + 1, n + 1):
                rows[row][k] = _finite(rows[row][k] - ratio * rows[col][k])
    result = [0j] * n
    for row in reversed(range(n)):
        residual = rows[row][n] - sum(rows[row][k] * result[k] for k in range(row + 1, n))
        result[row] = _finite(residual / rows[row][row])
    return result


def solve(
    matrix: Sequence[Sequence[Scalar]], rhs: Sequence[Scalar], *, rtol: float = 1e-12
) -> tuple[Ultra, ...]:
    """Solve A*x=b for a nonempty square matrix with invertible body channels.

    Scaled partial pivoting happens separately in each complex channel. Thus a
    matrix may be invertible even if every individual entry is a zero divisor.
    Singular/underdetermined and rectangular systems are not handled here.
    """
    if not math.isfinite(rtol) or rtol < 0:
        raise ValueError("rtol must be finite and nonnegative")
    n = len(rhs)
    if n == 0 or len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("Expected a nonempty square matrix and matching right-hand side")
    a = [[Ultra.coerce(value).channels() for value in row] for row in matrix]
    b = [Ultra.coerce(value).channels() for value in rhs]
    solutions: list[list[Channel]] = []
    for channel in range(2):
        body = [[value[channel][0] for value in row] for row in a]
        tangent = [[value[channel][1] for value in row] for row in a]
        try:
            x = _solve_complex(body, [value[channel][0] for value in b], rtol)
            residual = [
                value[channel][1] - sum(t * z for t, z in zip(row, x, strict=True))
                for value, row in zip(b, tangent, strict=True)
            ]
            dx = _solve_complex(body, residual, rtol)
        except SingularSystemError as error:
            raise SingularSystemError(f"{'+' if channel == 0 else '-'} channel: {error}") from error
        solutions.append(list(zip(x, dx, strict=True)))
    return tuple(Ultra.from_channels(p, m) for p, m in zip(*solutions, strict=True))
