"""Deterministic clustering, hierarchy cuts and the original grid algorithms."""

from __future__ import annotations

import itertools
import math
import random
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Literal

from .geometry import Vector, vector


def distance(a: Sequence[float], b: Sequence[float], order: float = 2) -> float:
    differences = [abs(x - y) for x, y in zip(a, b, strict=True)]
    if order == 0 or order == math.inf:
        return max(differences, default=0.0)
    if order < 1 or not math.isfinite(order):
        raise ValueError("Minkowski order must be >= 1, or 0 for maximum norm")
    largest = max(differences, default=0.0)
    return (
        largest * math.fsum((d / largest) ** order for d in differences) ** (1 / order)
        if largest
        else 0.0
    )


@dataclass(frozen=True)
class Cluster:
    data: frozenset[Vector]

    def merged_with(self, other: Cluster) -> Cluster:
        return Cluster(self.data | other.data)

    @property
    def center(self) -> Vector:
        if not self.data:
            raise ValueError("Empty cluster has no center")
        return tuple(
            math.fsum(col) / len(self.data) for col in zip(*sorted(self.data), strict=True)
        )


@dataclass(frozen=True)
class HierarchicalCluster(Cluster):
    left: HierarchicalCluster | None = None
    right: HierarchicalCluster | None = None
    key: int = -1
    merge_distance: float = 0.0

    @property
    def is_leaf(self) -> bool:
        return self.left is None

    def join(
        self, other: HierarchicalCluster, key: int, merge_distance: float = 0.0
    ) -> HierarchicalCluster:
        return HierarchicalCluster(self.data | other.data, self, other, key, merge_distance)

    def cut(self, count: int) -> tuple[Cluster, ...]:
        if count < 1:
            raise ValueError("count must be positive")
        nodes = [self]
        while sum(bool(n.data) for n in nodes) < count:
            candidates = [(node.key, i) for i, node in enumerate(nodes) if not node.is_leaf]
            if not candidates:
                break
            _, i = max(candidates)
            node = nodes.pop(i)
            assert node.left is not None and node.right is not None
            nodes.extend((node.left, node.right))
        return tuple(Cluster(n.data) for n in nodes if n.data)


@dataclass(frozen=True)
class DensityResult:
    clusters: tuple[Cluster, ...]
    noise: frozenset[Vector]


def silhouette(clusters: Sequence[Cluster], *, legacy: bool = False) -> float:
    groups = [sorted(c.data) for c in clusters if c.data]
    if len(groups) < 2:
        return 0.0
    values = []
    for index, group in enumerate(groups):
        for point in group:
            if len(group) == 1:
                values.append(0.0)
                continue
            a = math.fsum(distance(point, p) for p in group) / (
                len(group) if legacy else len(group) - 1
            )
            b = min(
                math.fsum(distance(point, p) for p in other) / len(other)
                for i, other in enumerate(groups)
                if i != index
            )
            values.append((b - a) / max(a, b) if max(a, b) else 0.0)
    return math.fsum(values) / len(values)


class Clustering:
    def __init__(
        self, data: Iterable[Sequence[float]] = (), *, dimension: int | None = None
    ) -> None:
        self.data: set[Vector] = set()
        self.dimension = dimension
        if dimension is not None and dimension < 1:
            raise ValueError("dimension must be positive")
        for point in data:
            self.add(point)

    def add(self, point: Sequence[float]) -> None:
        value = vector(point)
        if self.dimension is None:
            self.dimension = len(value)
        if len(value) != self.dimension:
            raise ValueError("Inconsistent data dimension")
        self.data.add(value)

    def kmeans(
        self, k: int, *, steps: int = 20, restarts: int = 1, seed: int = 0
    ) -> tuple[Cluster, ...]:
        points = sorted(self.data)
        if not 1 <= k <= len(points) or steps < 1 or restarts < 1:
            raise ValueError("Invalid k-means parameters")
        rng = random.Random(seed)
        best: tuple[Cluster, ...] = ()
        best_score = -math.inf
        for _ in range(restarts):
            centers = rng.sample(points, k)
            previous: list[int] = []
            for _ in range(steps):
                labels = [min(range(k), key=lambda i: (distance(p, centers[i]), i)) for p in points]
                groups = [
                    {p for p, label in zip(points, labels, strict=True) if label == i}
                    for i in range(k)
                ]
                for empty in [i for i, group in enumerate(groups) if not group]:
                    donor = max(
                        (
                            p
                            for i, group in enumerate(groups)
                            if len(group) > 1
                            for p in sorted(group)
                        ),
                        key=lambda p: distance(p, centers[labels[points.index(p)]]),
                    )
                    old = labels[points.index(donor)]
                    groups[old].remove(donor)
                    groups[empty].add(donor)
                    labels[points.index(donor)] = empty
                centers = [Cluster(frozenset(group)).center for group in groups]
                if labels == previous:
                    break
                previous = labels
            result = tuple(Cluster(frozenset(group)) for group in groups)
            score = silhouette(result)
            if score > best_score:
                best, best_score = result, score
        return best

    def choose_k(
        self, minimum: int, maximum: int, *, steps: int = 20, restarts: int = 1, seed: int = 0
    ) -> tuple[Cluster, ...]:
        if not 1 <= minimum <= maximum <= len(self.data):
            raise ValueError("Invalid k range")
        candidates = (
            self.kmeans(k, steps=steps, restarts=restarts, seed=seed + k)
            for k in range(minimum, maximum + 1)
        )
        return max(candidates, key=silhouette)

    def auto_kmeans(
        self, min_average_size: int | None = None, *, seed: int = 0
    ) -> tuple[Cluster, ...]:
        if not self.data:
            return ()
        size = max(1, math.isqrt(len(self.data))) if min_average_size is None else min_average_size
        if size < 1:
            raise ValueError("Minimum average size must be positive")
        upper = max(1, len(self.data) // size)
        return self.choose_k(min(2, upper), upper, seed=seed)

    def density(self, min_points: int, epsilon: float) -> DensityResult:
        """DBSCAN with the original strict (< epsilon), self-including neighborhoods."""
        if min_points < 1 or not math.isfinite(epsilon) or epsilon <= 0:
            raise ValueError("Invalid density parameters")
        points = sorted(self.data)
        neighbors = {p: {q for q in points if distance(p, q) < epsilon} for p in points}
        core = {p for p in points if len(neighbors[p]) >= min_points}
        assigned: set[Vector] = set()
        clusters = []
        for point in points:
            if point not in core or point in assigned:
                continue
            members, stack = set(), [point]
            while stack:
                p = stack.pop()
                if p in assigned:
                    continue
                assigned.add(p)
                members.add(p)
                if p in core:
                    stack.extend(sorted(neighbors[p] - assigned, reverse=True))
            clusters.append(Cluster(frozenset(members)))
        return DensityResult(tuple(clusters), frozenset(self.data - assigned))

    def hierarchical(
        self, linkage: Literal["single", "complete", "average"] = "single", order: float = 2
    ) -> HierarchicalCluster:
        if not self.data:
            raise ValueError("Hierarchy requires data")
        if linkage not in ("single", "complete", "average"):
            raise ValueError("Unknown linkage")
        nodes = [HierarchicalCluster(frozenset((p,))) for p in sorted(self.data)]

        def separation(a: HierarchicalCluster, b: HierarchicalCluster) -> float:
            distances = [distance(p, q, order) for p in sorted(a.data) for q in sorted(b.data)]
            return (
                min(distances)
                if linkage == "single"
                else max(distances)
                if linkage == "complete"
                else math.fsum(distances) / len(distances)
            )

        key = 0
        while len(nodes) > 1:
            dist, i, j = min(
                (separation(nodes[i], nodes[j]), i, j)
                for i in range(len(nodes))
                for j in range(i + 1, len(nodes))
            )
            joined = nodes[i].join(nodes[j], key, dist)
            nodes.pop(j)
            nodes.pop(i)
            nodes.append(joined)
            key += 1
        return nodes[0]

    def make_grid(
        self, divisions: int, *, include_empty: bool = False, max_cells: int = 50000
    ) -> dict[tuple[int, ...], frozenset[Vector]]:
        if divisions < 1:
            raise ValueError("divisions must be positive")
        if not self.data:
            return {}
        points = sorted(self.data)
        minima = [min(c) for c in zip(*points, strict=True)]
        maxima = [max(c) for c in zip(*points, strict=True)]
        sizes = [divisions if low < high else 1 for low, high in zip(minima, maxima, strict=True)]
        if include_empty and math.prod(sizes) > max_cells:
            raise ValueError("Grid exceeds max_cells; use fewer divisions")
        cells: dict[tuple[int, ...], set[Vector]] = {}
        if include_empty:
            cells = {index: set() for index in itertools.product(*(range(s) for s in sizes))}
        for p in points:
            index = tuple(
                min(divisions - 1, int((v - low) / (high - low) * divisions)) if low < high else 0
                for v, low, high in zip(p, minima, maxima, strict=True)
            )
            cells.setdefault(index, set()).add(p)
        return {index: frozenset(members) for index, members in cells.items()}

    def subspace(self, divisions: int, min_points: int) -> DensityResult:
        """Connected dense grid cells; retains the historical algorithm's name.

        This does not search projections onto subsets of dimensions.
        """
        if min_points < 1:
            raise ValueError("min_points must be positive")
        cells = {i: p for i, p in self.make_grid(divisions).items() if len(p) >= min_points}
        clusters, used = [], set()
        while cells:
            start = min(cells)
            stack = [start]
            members: set[Vector] = set()
            while stack:
                index = stack.pop()
                if index not in cells:
                    continue
                members.update(cells.pop(index))
                stack.extend(i for i in _neighbors(index) if i in cells)
            used.update(members)
            clusters.append(Cluster(frozenset(members)))
        return DensityResult(tuple(clusters), frozenset(self.data - used))

    def grid(self, divisions: int, *, max_cells: int = 50000) -> tuple[HierarchicalCluster, ...]:
        raw = self.make_grid(divisions, include_empty=True, max_cells=max_cells)
        nodes = {i: HierarchicalCluster(p) for i, p in raw.items()}
        area = dict.fromkeys(raw, 1)
        adjacent = {i: set(_neighbors(i)) & raw.keys() for i in raw}
        active, finished, key = set(raw), [], 0

        def density(i: tuple[int, ...]) -> float:
            return len(nodes[i].data) / area[i]

        while active:
            densest = min(active, key=lambda i: (-density(i), i))
            while True:
                candidates = [
                    i for i in adjacent[densest] if i in active and density(i) < density(densest)
                ]
                if not candidates:
                    break
                other = min(candidates, key=lambda i: (-density(i), i))
                nodes[densest] = nodes[densest].join(nodes.pop(other), key)
                key += 1
                area[densest] += area.pop(other)
                adjacent[densest] |= adjacent.pop(other)
                adjacent[densest].difference_update((densest, other))
                for neighbors in adjacent.values():
                    if other in neighbors:
                        neighbors.remove(other)
                        neighbors.add(densest)
                active.remove(other)
            active.remove(densest)
            if nodes[densest].data:
                finished.append(nodes[densest])
        return tuple(finished)


def _neighbors(index: tuple[int, ...]) -> Iterable[tuple[int, ...]]:
    for dimension in range(len(index)):
        for sign in (-1, 1):
            result = list(index)
            result[dimension] += sign
            yield tuple(result)


def generate_clusters(
    *,
    dimensions: int = 2,
    clusters: int = 3,
    points_per_cluster: int = 30,
    maximum: float = 10.0,
    spread: float = 0.4,
    seed: int = 0,
    distribution: Literal["uniform", "gaussian", "nested"] = "uniform",
) -> Clustering:
    if min(dimensions, clusters, points_per_cluster) < 1 or maximum <= 0 or spread < 0:
        raise ValueError("Invalid generator parameters")
    if distribution not in ("uniform", "gaussian", "nested"):
        raise ValueError("Unknown distribution")
    rng, points = random.Random(seed), []
    for k in range(clusters):
        center = [rng.uniform(0, maximum) for _ in range(dimensions)]
        if distribution == "nested":
            center = [maximum / 2] * dimensions
        for _ in range(points_per_cluster):
            if distribution == "nested":
                direction = [rng.gauss(0, 1) for _ in center]
                radius = (k + 1) * maximum / (2 * clusters)
                norm = math.hypot(*direction)
                point = tuple(
                    c + radius * d / norm + rng.uniform(-spread, spread)
                    for c, d in zip(center, direction, strict=True)
                )
            else:
                point = tuple(
                    c
                    + (
                        rng.gauss(0, spread)
                        if distribution == "gaussian"
                        else rng.uniform(-spread, spread)
                    )
                    for c in center
                )
            points.append(point)
    return Clustering(points)
