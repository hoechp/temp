"""Eight-dimensional commutative arithmetic, formulas and linear systems."""

from .core import (
    BASIS,
    EPS,
    ONE,
    ZERO,
    DomainError,
    I,
    J,
    NonFiniteError,
    NonInvertibleError,
    Ultra,
)
from .formula import ExpressionError, Formula, evaluate, evaluate_system
from .linalg import SingularSystemError, solve

__version__ = "0.1.0"
__all__ = [
    "BASIS",
    "EPS",
    "I",
    "J",
    "ONE",
    "ZERO",
    "DomainError",
    "ExpressionError",
    "Formula",
    "NonFiniteError",
    "NonInvertibleError",
    "SingularSystemError",
    "Ultra",
    "evaluate",
    "evaluate_system",
    "solve",
]
