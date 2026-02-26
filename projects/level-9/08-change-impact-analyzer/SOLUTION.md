# Solution: Level 9 / Project 08 - Change Impact Analyzer

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Change Impact Analyzer — analyze impact of changes across dependent systems."""

from __future__ import annotations

import argparse
import json
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

class ChangeType(Enum):
    CODE = "code"
    CONFIG = "config"
    SCHEMA = "schema"
    INFRASTRUCTURE = "infrastructure"
    DEPENDENCY = "dependency"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# WHY tier on each service? -- Blast radius depends on criticality. A change
# affecting a tier-1 (customer-facing) service requires more review gates
# than the same change on a tier-3 (internal) service. BFS traversal of
# the dependency graph propagates impact, and tier amplifies the risk score
# at each hop — matching how incident commanders triage in practice.
@dataclass
class Service:
    """A service in the dependency graph."""
    name: str
    team: str
    tier: int = 1  # 1=critical, 2=important, 3=internal
    slos: list[str] = field(default_factory=list)


@dataclass
class Change:
    """A proposed change to a service."""
    change_id: str
    service: str
    change_type: ChangeType
    description: str
    files_changed: int = 0
    lines_changed: int = 0


@dataclass
class ImpactResult:
    """Result of analyzing a change's impact."""
    change_id: str
    directly_affected: list[str]
    transitively_affected: list[str]
    affected_teams: list[str]
    affected_slos: list[str]
    risk_level: RiskLevel
    risk_score: float  # 0-100
    max_depth: int
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "change_id": self.change_id,
            "directly_affected": self.directly_affected,
            "transitively_affected": self.transitively_affected,
            "affected_teams": self.affected_teams,
            "affected_slos": self.affected_slos,
            "risk_level": self.risk_level.value,
            "risk_score": round(self.risk_score, 1),
            "max_depth": self.max_depth,
            "recommendations": self.recommendations,
        }


# --- Service graph ------------------------------------------------------

class ServiceGraph:
    """Directed graph of service dependencies."""

    def __init__(self) -> None:
        self._services: dict[str, Service] = {}
        self._dependencies: dict[str, set[str]] = {}  # service -> depends_on
        self._dependents: dict[str, set[str]] = {}     # service -> depended_on_by

    def add_service(self, service: Service) -> None:
        self._services[service.name] = service
        self._dependencies.setdefault(service.name, set())
        self._dependents.setdefault(service.name, set())

    def add_dependency(self, from_svc: str, to_svc: str) -> None:
        """from_svc depends on to_svc."""
        self._dependencies.setdefault(from_svc, set()).add(to_svc)
        self._dependents.setdefault(to_svc, set()).add(from_svc)

    def get_service(self, name: str) -> Service | None:
        return self._services.get(name)

    def direct_dependents(self, service: str) -> set[str]:
        """Services that directly depend on this one."""
        return set(self._dependents.get(service, set()))

    # WHY BFS instead of DFS for transitive dependents? -- BFS naturally
    # tracks depth (distance from the changed service). Depth is a key
    # factor in risk scoring: a service 1 hop away is more affected than
    # one 4 hops away. DFS would need extra bookkeeping to track depth.
    def transitive_dependents(self, service: str) -> tuple[set[str], int]:
        """All services transitively affected by a change to this service."""
        visited: set[str] = set()
        queue: deque[tuple[str, int]] = deque([(service, 0)])
        max_depth = 0

        while queue:
            current, depth = queue.popleft()
            for dep in self._dependents.get(current, set()):
                if dep not in visited:
                    visited.add(dep)
                    max_depth = max(max_depth, depth + 1)
                    queue.append((dep, depth + 1))

        return visited, max_depth

    @property
    def services(self) -> list[Service]:
        return list(self._services.values())


# --- Impact analyzer ----------------------------------------------------

class ChangeImpactAnalyzer:
    """Analyzes the blast radius and risk of proposed changes."""

    def __init__(self, graph: ServiceGraph) -> None:
        self._graph = graph

    def analyze(self, change: Change) -> ImpactResult:
        """Analyze the impact of a proposed change."""
        direct = self._graph.direct_dependents(change.service)
        transitive, max_depth = self._graph.transitive_dependents(change.service)

        # Collect affected teams and SLOs
        all_affected = direct | transitive | {change.service}
        teams: set[str] = set()
        slos: set[str] = set()
        min_tier = 3

        for svc_name in all_affected:
            svc = self._graph.get_service(svc_name)
            if svc:
                teams.add(svc.team)
                slos.update(svc.slos)
                min_tier = min(min_tier, svc.tier)

        risk_score = self._compute_risk(change, len(all_affected), max_depth, min_tier)
        risk_level = self._score_to_level(risk_score)

        recommendations = self._generate_recommendations(
            change, risk_level, len(teams), max_depth,
        )

        return ImpactResult(
            change_id=change.change_id,
            directly_affected=sorted(direct),
            transitively_affected=sorted(transitive - direct),
            affected_teams=sorted(teams),
            affected_slos=sorted(slos),
            risk_level=risk_level,
            risk_score=risk_score,
            max_depth=max_depth,
            recommendations=recommendations,
        )

    # WHY a multi-factor risk score? -- Risk depends on change type (schema
    # changes are riskier than config), blast radius (more affected services
    # = more risk), depth (deeper chains are harder to test), and tier
    # (critical services demand more caution). A single-factor score would
    # miss important dimensions.
    def _compute_risk(self, change: Change, affected_count: int,
                      max_depth: int, min_tier: int) -> float:
        score = 0.0
        type_weights = {
            ChangeType.SCHEMA: 30, ChangeType.INFRASTRUCTURE: 25,
            ChangeType.DEPENDENCY: 20, ChangeType.CODE: 10, ChangeType.CONFIG: 15,
        }
        score += type_weights.get(change.change_type, 10)
        score += min(30, affected_count * 5)
        score += min(20, max_depth * 7)
        tier_weight = {1: 20, 2: 10, 3: 5}
        score += tier_weight.get(min_tier, 5)
        return min(100, score)

    def _score_to_level(self, score: float) -> RiskLevel:
        if score >= 75:
            return RiskLevel.CRITICAL
        if score >= 50:
            return RiskLevel.HIGH
        if score >= 25:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def _generate_recommendations(self, change: Change, risk: RiskLevel,
                                  team_count: int, depth: int) -> list[str]:
        recs: list[str] = []
        if risk in (RiskLevel.HIGH, RiskLevel.CRITICAL):
            recs.append("Use canary deployment with extended monitoring")
        if team_count > 1:
            recs.append(f"Coordinate with {team_count} affected teams before deploy")
        if change.change_type == ChangeType.SCHEMA:
            recs.append("Ensure backward-compatible schema migration")
        if depth > 2:
            recs.append("Test full dependency chain in staging environment")
        return recs


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    graph = ServiceGraph()
    graph.add_service(Service("api-gateway", "platform", tier=1, slos=["availability-99.9"]))
    graph.add_service(Service("user-service", "identity", tier=1, slos=["latency-p99-200ms"]))
    graph.add_service(Service("order-service", "commerce", tier=1, slos=["availability-99.9"]))
    graph.add_service(Service("payment-service", "commerce", tier=1, slos=["availability-99.99"]))
    graph.add_service(Service("notification-svc", "engagement", tier=2))
    graph.add_service(Service("analytics-svc", "data", tier=3))

    graph.add_dependency("api-gateway", "user-service")
    graph.add_dependency("api-gateway", "order-service")
    graph.add_dependency("order-service", "payment-service")
    graph.add_dependency("order-service", "notification-svc")
    graph.add_dependency("notification-svc", "user-service")
    graph.add_dependency("analytics-svc", "order-service")

    analyzer = ChangeImpactAnalyzer(graph)

    change = Change(
        change_id="CHG-2025-042",
        service="user-service",
        change_type=ChangeType.SCHEMA,
        description="Add 'preferences' column to users table",
        files_changed=5,
        lines_changed=120,
    )

    result = analyzer.analyze(change)
    return result.to_dict()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Change impact analyzer")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| BFS for transitive impact propagation | Naturally tracks depth (distance from changed service); depth is a risk factor | DFS -- explores deep paths first but requires extra bookkeeping for depth tracking |
| Multi-factor risk scoring (type + blast radius + depth + tier) | Risk is multi-dimensional; a schema change to a tier-1 service with 5 dependents is riskier than a config change to a tier-3 service | Single-factor (e.g., blast radius only) -- misses the qualitative difference between change types and service criticality |
| Separate direct vs transitive dependents | Direct dependents need API compatibility testing; transitive dependents need integration testing. Different actions for different relationships | Lumping all dependents together -- loses the distinction between first-hop and multi-hop impact |
| Context-aware recommendations | Recommendations change based on risk level, team count, change type, and depth | Static checklist -- same recommendations regardless of risk, causing alert fatigue for low-risk changes |
| Capped risk score at 100 | Prevents unbounded scores when many factors compound; keeps the 0-100 scale interpretable | Uncapped -- a service with 20 dependents, deep chains, and schema change could score 200+, breaking the level mapping |

## Alternative approaches

### Approach B: Probabilistic impact analysis with failure cascade simulation

```python
import random

class CascadeSimulator:
    """Instead of deterministic graph traversal, simulate probabilistic
    failure cascades. Each dependency has a probability of propagating
    failure, reflecting real-world partial outages."""
    def __init__(self, graph: ServiceGraph, seed: int = 42):
        self._graph = graph
        self._rng = random.Random(seed)

    def simulate_cascade(self, origin: str, propagation_prob: float = 0.7,
                         runs: int = 1000) -> dict[str, float]:
        """Return probability of each service being affected."""
        affected_counts: dict[str, int] = {}
        for _ in range(runs):
            affected = {origin}
            queue = [origin]
            while queue:
                current = queue.pop(0)
                for dep in self._graph.direct_dependents(current):
                    if dep not in affected and self._rng.random() < propagation_prob:
                        affected.add(dep)
                        queue.append(dep)
            for svc in affected:
                affected_counts[svc] = affected_counts.get(svc, 0) + 1
        return {svc: count / runs for svc, count in affected_counts.items()}
```

**Trade-off:** Probabilistic simulation accounts for the fact that not every dependency failure cascades. A degraded user-service might not affect notification-service if the notification path has retry logic. Monte Carlo simulation produces probabilities ("80% chance payment-service is affected") rather than binary yes/no. The tradeoff is computational cost and the need to calibrate propagation probabilities. Use deterministic analysis for planning; probabilistic analysis when you have historical cascade data to calibrate probabilities.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Service not in graph | `get_service` returns `None`; `direct_dependents` returns empty set | Validate that the changed service exists in the graph before analyzing |
| Circular dependency (A depends on B depends on A) | BFS `visited` set prevents infinite loops, but the cycle itself is a structural issue | Report cycles as a separate finding; circular dependencies are a design smell |
| Change to a leaf service with no dependents | Impact result shows 0 affected services, risk score may still be non-trivial due to change type and tier | This is correct -- leaf changes have limited blast radius but may still be risky (schema change on tier-1) |
