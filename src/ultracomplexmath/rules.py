"""Transaction itemsets and association rules with explicit support semantics."""

from __future__ import annotations

import itertools
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Literal


@dataclass(eq=False)
class Data:
    transactions: list[frozenset[int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.transactions = [frozenset(row) for row in self.transactions]

    def add(self, items: Iterable[int]) -> None:
        self.transactions.append(frozenset(items))

    @property
    def items(self) -> frozenset[int]:
        return frozenset().union(*self.transactions)

    def itemset(self, items: Iterable[int]) -> DataSet:
        return DataSet(self, frozenset(items))


@dataclass(frozen=True)
class DataSet:
    origin: Data
    items: frozenset[int]

    @property
    def supporters(self) -> frozenset[int]:
        return frozenset(i for i, row in enumerate(self.origin.transactions) if self.items <= row)

    @property
    def support(self) -> float:
        return (
            len(self.supporters) / len(self.origin.transactions)
            if self.origin.transactions
            else 0.0
        )


@dataclass(frozen=True)
class Rule:
    antecedent: DataSet
    consequent: DataSet

    def __post_init__(self) -> None:
        if self.antecedent.origin is not self.consequent.origin:
            raise ValueError("Rule sides must refer to the same dataset")
        if (
            not self.antecedent.items
            or not self.consequent.items
            or self.antecedent.items & self.consequent.items
        ):
            raise ValueError("Rule sides must be nonempty and disjoint")

    @property
    def support(self) -> float:
        """Standard support: fraction containing BOTH sides."""
        return self.antecedent.origin.itemset(self.antecedent.items | self.consequent.items).support

    @property
    def coverage(self) -> float:
        """Original Rule.supp(): fraction containing EITHER side."""
        count = len(self.antecedent.origin.transactions)
        return (
            len(self.antecedent.supporters | self.consequent.supporters) / count if count else 0.0
        )

    @property
    def confidence(self) -> float:
        return self.support / self.antecedent.support if self.antecedent.support else 0.0

    def __str__(self) -> str:
        return f"{sorted(self.antecedent.items)} -> {sorted(self.consequent.items)} (support={self.support:.3g}, coverage={self.coverage:.3g}, confidence={self.confidence:.3g})"


def frequent_itemsets(data: Data, minimum_support: float = 0.0) -> tuple[DataSet, ...]:
    """Apriori with the original strict support threshold (>)."""
    if not 0 <= minimum_support <= 1:
        raise ValueError("Support must be in [0,1]")
    current = {
        frozenset((item,)) for item in data.items if data.itemset((item,)).support > minimum_support
    }
    result: list[DataSet] = []
    size = 1
    while current:
        result.extend(
            data.itemset(items) for items in sorted(current, key=lambda x: tuple(sorted(x)))
        )
        candidates = {
            a | b for a, b in itertools.combinations(current, 2) if len(a | b) == size + 1
        }
        current = {
            candidate
            for candidate in candidates
            if all(frozenset(s) in current for s in itertools.combinations(sorted(candidate), size))
            and data.itemset(candidate).support > minimum_support
        }
        size += 1
    return tuple(result)


@dataclass
class RuleDeduction:
    data: Data
    minimum_item_support: float = 0.0
    minimum_confidence: float = 1.0
    minimum_rule_support: float = 0.0
    support_metric: Literal["support", "coverage"] = "coverage"
    itemsets: tuple[DataSet, ...] = field(init=False)
    rules: tuple[Rule, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.refresh()

    def refresh(self) -> None:
        if not all(
            0 <= v <= 1
            for v in (self.minimum_item_support, self.minimum_confidence, self.minimum_rule_support)
        ):
            raise ValueError("Thresholds must be in [0,1]")
        if self.support_metric not in ("support", "coverage"):
            raise ValueError("Unknown support metric")
        self.itemsets = frequent_itemsets(self.data, self.minimum_item_support)
        rules = []
        for a, b in itertools.permutations(self.itemsets, 2):
            if a.items & b.items:
                continue
            rule = Rule(a, b)
            support = rule.coverage if self.support_metric == "coverage" else rule.support
            if rule.confidence >= self.minimum_confidence and support > self.minimum_rule_support:
                rules.append(rule)
        self.rules = tuple(rules)
