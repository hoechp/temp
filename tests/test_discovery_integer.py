import itertools
import math

import pytest

from ultracomplexmath.classification import Classification
from ultracomplexmath.clustering import Cluster, Clustering, distance, generate_clusters, silhouette
from ultracomplexmath.concepts import Property, TermDeduction, Thing, Things
from ultracomplexmath.modular import ModularRing
from ultracomplexmath.number_theory import (
    break_rsa,
    congruent_prime,
    euklid,
    extended_gcd,
    fermat_factors,
    generate_rsa,
    integer_root,
    is_prime,
    modular_inverse,
    next_prime,
    root_and_remainder,
    rsa_decoder,
    rsa_transform,
)
from ultracomplexmath.rules import Data, Rule, RuleDeduction, frequent_itemsets


def test_primes_roots_bezout_and_original_large_factors():
    for n in range(500):
        expected = n >= 2 and all(n % k for k in range(2, math.isqrt(n) + 1))
        assert is_prime(n) == expected
        root, rem = root_and_remainder(n)
        assert root * root + rem == n and 0 <= rem < 2 * root + 1
        assert integer_root(n, -1) == root
        assert integer_root(n, 1) == root + bool(rem)
        assert integer_root(n) == (None if rem else root)
    assert not is_prime(341550071728321)
    assert next_prime(100) == 101
    assert euklid(40, 7) == (1, 3, 40, -17, 7)
    for a, b in itertools.product(range(-8, 9), repeat=2):
        g, x, y = extended_gcd(a, b)
        assert g == math.gcd(a, b) == a * x + b * y
    n = 1606938044258990275551518141370982378356229797292067198570519
    result = fermat_factors(n, max_steps=2)
    assert (result.steps, result.lower, result.upper) == (
        1,
        1267650600228229401499935529979,
        1267650600228229401501009274261,
    )
    assert result.lower * result.upper == n
    with pytest.raises(TimeoutError):
        fermat_factors(101, max_steps=2)
    i, prime = congruent_prime(10, 8)
    assert prime >= 128 and prime == 10 * i + 1 and is_prime(prime)
    assert modular_inverse(3, 11) == 4


def test_textbook_rsa_and_residue_orbits():
    data = generate_rsa(16, seed=9)
    for message in (0, 1, 42, data.p, data.n - 1):
        cipher = rsa_transform(data.n, data.e, message)
        assert rsa_transform(data.n, data.d, cipher) == message
        assert break_rsa(data.n, data.e, cipher, max_steps=1000) == message
    assert rsa_decoder(data.n, data.e) == data.d
    ring = ModularRing(11)
    assert [ring(i).order for i in range(1, 11)] == [1, 10, 5, 5, 5, 10, 10, 10, 5, 2]
    assert (ring(-1) + ring(2)).value == 1
    assert (ring(3) * ring(3).inverse()).value == 1
    assert ModularRing(8)(2).powers == frozenset(ModularRing(8)(i) for i in (1, 2, 4, 0))
    assert ring.addition_table[7][9] == 5
    assert ring.multiplication_table[7][9] == 8


@pytest.mark.parametrize("method", ["kmeans", "density", "hierarchical", "grid", "subspace"])
def test_all_five_clustering_algorithms(method):
    points = [(0, 0), (0.1, 0), (0, 0.1), (5, 5), (5.1, 5), (5, 5.1)]
    data = Clustering(points)
    if method == "kmeans":
        groups = data.kmeans(2, restarts=5, seed=17)
    elif method == "density":
        result = data.density(2, 0.3)
        groups = result.clusters
        assert not result.noise
    elif method == "hierarchical":
        groups = data.hierarchical().cut(2)
    elif method == "grid":
        groups = data.grid(4)
    else:
        groups = data.subspace(4, 2).clusters
    assert {g.data for g in groups} == {frozenset(points[:3]), frozenset(points[3:])}
    assert silhouette(groups) > 0.9


def test_clustering_degeneracy_and_determinism():
    data = Clustering([(0, 1), (1, 1), (2, 1), (9, 1)])
    assert len(data.make_grid(3, include_empty=True)) == 3
    assert data.density(2, 1).noise == frozenset(data.data)  # Strict epsilon.
    groups = data.kmeans(4)
    assert all(len(g.data) == 1 for g in groups)
    assert silhouette(groups) == 0
    assert data.kmeans(2, seed=11) == data.kmeans(2, seed=11)
    assert len(data.choose_k(2, 3)) == 2
    assert Clustering().auto_kmeans() == ()
    assert distance((1, 2), (4, 6), 1) == 7
    assert distance((1, 2), (4, 6), 2) == 5
    assert distance((1, 2), (4, 6), 0) == 4
    for linkage in ("single", "complete", "average"):
        tree = data.hierarchical(linkage)
        assert tree.data == frozenset(data.data)
        assert len(tree.cut(10)) == len(data.data)
    assert generate_clusters(seed=9).data == generate_clusters(seed=9).data
    assert Cluster(frozenset(((1, 2), (3, 4)))).center == (2, 3)


def test_rules_against_exhaustive_reference_and_live_data():
    data = Data([frozenset((1, 2)), frozenset((1, 2, 3)), frozenset((1,)), frozenset((3,))])
    expected = set()
    for size in range(1, 4):
        for subset in itertools.combinations((1, 2, 3), size):
            if sum(set(subset) <= row for row in data.transactions) / 4 > 0.25:
                expected.add(frozenset(subset))
    assert {item.items for item in frequent_itemsets(data, 0.25)} == expected
    rule = Rule(data.itemset((1,)), data.itemset((2,)))
    assert rule.support == 0.5 and rule.coverage == 0.75
    assert rule.confidence == pytest.approx(2 / 3)
    deduction = RuleDeduction(data, 0, 1, 0)
    assert any(r.antecedent.items == {2} and r.consequent.items == {1} for r in deduction.rules)
    data.add((2,))
    assert rule.confidence == pytest.approx(2 / 3)
    deduction.refresh()
    assert not any(r.antecedent.items == {2} and r.consequent.items == {1} for r in deduction.rules)


def test_concept_lattice_reduction_and_classification():
    a, b, c = [Property(i, name) for i, name in enumerate("ABC")]
    things = Things([Thing(frozenset((a, b))), Thing(frozenset((a, b, c))), Thing(frozenset((c,)))])
    concepts = TermDeduction(things)
    ab, ta = concepts.find((a, b)), concepts.find("A")
    assert ta in ab.all_generalizations
    assert ab.support == pytest.approx(2 / 3)
    assert concepts.reduce()
    for term in concepts.terms:
        assert term not in term.all_generalizations
        for general in term.generalizations:
            assert term in general.specializations
            assert general.definition < term.definition
    cls = Classification(((True, True), (True, False), (False, False)))
    positive, negative = cls.indication(0)
    assert positive == (1, 1)
    assert negative == (0, 0.5)
    assert Classification(((True, True),)).indication(0)[1] == (None, None)


def test_soft_term_redefinition_propagates_to_descendants():
    a, b, c = [Property(i, name) for i, name in enumerate("ABC")]
    things = Things(
        [Thing(frozenset((a, c))), Thing(frozenset((a, b, c))), Thing(frozenset((a, b)))]
    )
    deduction = TermDeduction(things)
    ta, tab, tac = deduction.find((a,)), deduction.find((a, b)), deduction.find((a, c))
    assert tac.support == pytest.approx(2 / 3)
    ta.redefine_as(tab)
    assert tac.definition == {a, b, c}
    assert tac.support == pytest.approx(1 / 3)
    assert not tab.active and not tab.extent
    deduction.eliminate()
    assert len({t.definition for t in deduction.terms}) == len(deduction.terms)
