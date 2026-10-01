"""Commutative algebras, formulas, geometry and mathematical experiments."""

from .coordinates import Cartesian2D, Polar2D
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
from .expressions import BoundFormula, Calculation, FormulaSystem, Parameter, SimpleCalculation
from .formula import ExpressionError, Formula, evaluate, evaluate_system
from .linalg import (
    InconsistentSystemError,
    LinearSolution,
    SingularSystemError,
    solution_space,
    solve,
)
from .matrix import M2R, Matrix
from .mechanisms import Actor, Freedom, Joint, Machine, Mechanism
from .numbers import Binary, Complex, Dual, Hypercomplex, RootSet
from .polynomial import Polynomial, guess

__version__ = "0.2.0"
__all__ = [
    "Actor",
    "Binary",
    "BoundFormula",
    "Calculation",
    "Cartesian2D",
    "Complex",
    "Dual",
    "FormulaSystem",
    "Freedom",
    "Hypercomplex",
    "InconsistentSystemError",
    "Joint",
    "LinearSolution",
    "M2R",
    "Machine",
    "Matrix",
    "Mechanism",
    "Parameter",
    "Polar2D",
    "Polynomial",
    "RootSet",
    "SimpleCalculation",
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
    "guess",
    "solution_space",
    "solve",
]
