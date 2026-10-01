"""Conditional boolean indications from the original classification experiment."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Classification:
    rows: tuple[tuple[bool, ...], ...]

    def __post_init__(self) -> None:
        if self.rows and any(len(row) != len(self.rows[0]) for row in self.rows):
            raise ValueError("Ragged data")

    @classmethod
    def random(cls, columns: int, rows: int, *, seed: int = 0) -> Classification:
        if columns < 1 or rows < 1:
            raise ValueError("Dimensions must be positive")
        rng = random.Random(seed)
        return cls(tuple(tuple(rng.random() < 0.5 for _ in range(columns)) for _ in range(rows)))

    def indication(self, column: int) -> tuple[tuple[float | None, ...], tuple[float | None, ...]]:
        """P(target | feature), P(target | not feature); None for empty conditions."""
        if not self.rows or not 0 <= column < len(self.rows[0]):
            raise ValueError("Missing target column")

        def probability(feature: int, condition: bool) -> float | None:
            subset = [row for row in self.rows if row[feature] == condition]
            return sum(row[column] for row in subset) / len(subset) if subset else None

        return (
            tuple(probability(i, True) for i in range(len(self.rows[0]))),
            tuple(probability(i, False) for i in range(len(self.rows[0]))),
        )
