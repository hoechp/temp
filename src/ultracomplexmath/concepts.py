"""Property conjunctions, implication graphs and concept reduction."""

from __future__ import annotations

import random
from collections.abc import Iterable
from dataclasses import dataclass, field

from .rules import Data, DataSet, RuleDeduction, frequent_itemsets


@dataclass(frozen=True, order=True)
class Property:
    identifier: int
    name: str


@dataclass(frozen=True, eq=False)
class Thing:
    properties: frozenset[Property]


@dataclass
class Things:
    things: list[Thing] = field(default_factory=list)
    properties: frozenset[Property] = frozenset()

    def __post_init__(self) -> None:
        self.properties = frozenset(self.properties).union(*(t.properties for t in self.things))
        if len({p.identifier for p in self.properties}) != len(self.properties):
            raise ValueError("Property identifiers must be unique")

    def property(self, identifier: int) -> Property:
        for p in self.properties:
            if p.identifier == identifier:
                return p
        raise KeyError(identifier)

    def to_data(self) -> Data:
        return Data([frozenset(p.identifier for p in t.properties) for t in self.things])

    @classmethod
    def random(
        cls, count: int, property_count: int, chance: float = 0.5, *, seed: int = 0
    ) -> Things:
        if count < 0 or property_count < 0 or not 0 <= chance <= 1:
            raise ValueError("Invalid generator parameters")
        rng = random.Random(seed)
        properties = frozenset(Property(i, f"p{i}") for i in range(property_count))
        return cls(
            [
                Thing(frozenset(p for p in sorted(properties) if rng.random() < chance))
                for _ in range(count)
            ],
            properties,
        )


@dataclass(eq=False)
class Term:
    definition: frozenset[Property]
    origin: Things
    name: str = ""
    generalizations: set[Term] = field(default_factory=set, repr=False)
    specializations: set[Term] = field(default_factory=set, repr=False)
    aliases: set[str] = field(default_factory=set)
    active: bool = True

    def __post_init__(self) -> None:
        if not self.name:
            self.name = " & ".join(p.name for p in sorted(self.definition))
        self.aliases.add(self.name)

    @property
    def extent(self) -> frozenset[Thing]:
        if not self.active:
            return frozenset()
        return frozenset(t for t in self.origin.things if self.definition <= t.properties)

    @property
    def support(self) -> float:
        return len(self.extent) / len(self.origin.things) if self.origin.things else 0.0

    def _closure(self, attribute: str) -> frozenset[Term]:
        visited: set[Term] = set()
        pending = list(getattr(self, attribute))
        while pending:
            term = pending.pop()
            if term is self or term in visited:
                continue
            visited.add(term)
            pending.extend(getattr(term, attribute))
        return frozenset(visited)

    @property
    def all_generalizations(self) -> frozenset[Term]:
        return self._closure("generalizations")

    @property
    def all_specializations(self) -> frozenset[Term]:
        return self._closure("specializations")

    def adopt_properties(self, other: Term) -> None:
        if self.origin is not other.origin:
            raise ValueError("Different universes")
        self.definition |= other.definition

    def detach(self) -> None:
        for term in self.generalizations:
            term.specializations.discard(self)
        for term in self.specializations:
            term.generalizations.discard(self)
        self.generalizations.clear()
        self.specializations.clear()

    def redefine_as(self, other: Term) -> None:
        if self is other:
            return
        if self.origin is not other.origin:
            raise ValueError("Different universes")
        generals = (self.generalizations | other.generalizations) - {self, other}
        specifics = (self.specializations | other.specializations) - {self, other}
        descendants = (self.all_specializations | other.all_specializations) - {self, other}
        self.detach()
        other.detach()
        self.definition |= other.definition
        self.aliases |= other.aliases
        for term in descendants:
            term.adopt_properties(self)
        other.discard()
        self.generalizations = {t for t in generals if t.definition < self.definition}
        self.specializations = {t for t in specifics if self.definition < t.definition}
        for term in self.generalizations:
            term.specializations.add(self)
        for term in self.specializations:
            term.generalizations.add(self)

    def discard(self) -> None:
        """Retire a term and detach its graph edges (the old didntExist operation)."""
        self.detach()
        self.active = False
        self.definition = frozenset()
        self.aliases.clear()
        self.name = ""


class TermDeduction:
    def __init__(self, things: Things, minimum_support: float = 0.0) -> None:
        self.things, self.minimum_support = things, minimum_support
        self.terms = [
            Term(frozenset(things.property(i) for i in itemset.items), things)
            for itemset in frequent_itemsets(things.to_data(), minimum_support)
        ]
        self.reduction_log: list[str] = []
        self._link()

    def _link(self) -> None:
        for term in self.terms:
            term.detach()
        # Hasse edges: immediate proper-definition inclusions only.
        for term in self.terms:
            below = [t for t in self.terms if t.definition < term.definition]
            for general in below:
                if not any(general.definition < t.definition < term.definition for t in below):
                    term.generalizations.add(general)
                    general.specializations.add(term)

    def find(self, value: str | DataSet | Iterable[Property]) -> Term | None:
        if isinstance(value, str):
            return next((t for t in self.terms if value in t.aliases), None)
        definition = (
            frozenset(self.things.property(i) for i in value.items)
            if isinstance(value, DataSet)
            else frozenset(value)
        )
        return next((t for t in self.terms if t.definition == definition), None)

    def eliminate(self) -> None:
        unique: dict[frozenset[Property], Term] = {}
        for term in self.terms:
            if not term.active or term.support <= self.minimum_support:
                term.discard()
            elif term.definition in unique:
                unique[term.definition].aliases |= term.aliases
                term.discard()
            else:
                unique[term.definition] = term
        self.terms = list(unique.values())
        self._link()

    def reduce(
        self, minimum_confidence: float = 1.0, minimum_support: float = 0.0
    ) -> tuple[str, ...]:
        rules = RuleDeduction(
            self.things.to_data(), self.minimum_support, minimum_confidence, minimum_support
        ).rules
        pending = [(self.find(r.antecedent), self.find(r.consequent), r.confidence) for r in rules]
        for index in range(len(pending)):
            antecedent, consequent, confidence = pending[index]
            if antecedent is None or consequent is None or antecedent is consequent:
                continue
            both = self.find(antecedent.definition | consequent.definition)
            if antecedent is None or both is None or antecedent is both:
                continue
            self.reduction_log.append(
                f"{antecedent.name} := {both.name} (confidence={confidence:g})"
            )
            pending = [
                (antecedent if a is both else a, antecedent if b is both else b, c)
                for a, b, c in pending
            ]
            antecedent.redefine_as(both)
            self.terms.remove(both)
        self.eliminate()
        return tuple(self.reduction_log)
