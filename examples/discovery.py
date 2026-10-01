"""Modern equivalents of RuleAndDatasetPrinter, TermPrinter and DS2Tinker."""

from ultracomplexmath.classification import Classification
from ultracomplexmath.concepts import TermDeduction, Things
from ultracomplexmath.modular import ModularRing
from ultracomplexmath.number_theory import congruent_prime, fermat_output
from ultracomplexmath.rules import Data, RuleDeduction


def main() -> None:
    data = Data([frozenset((1, 2)), frozenset((1, 2, 3)), frozenset((3,))])
    for rule in RuleDeduction(data).rules:
        print(rule)
    deduction = TermDeduction(Things.random(12, 4, seed=19))
    for step in deduction.reduce():
        print(step)
    for term in deduction.terms:
        print(term.name, f"support={term.support:.3f}", "aliases:", sorted(term.aliases))
    print("Conditional indications:", Classification.random(4, 12, seed=19).indication(0))
    print("Multiplication modulo 5:")
    for row in ModularRing(5).multiplication_table:
        print(*row)
    print(fermat_output(5959))
    print("Prime i*10+1 with >= 8 bits:", congruent_prime(10, 8))


if __name__ == "__main__":
    main()
