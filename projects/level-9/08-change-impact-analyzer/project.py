"""Change Impact Analyzer — analyze impact of changes across dependent systems.

Design rationale:
    Before deploying a change, engineers must understand its blast radius:
    which services, teams, and SLOs are affected. This project builds an
    impact analyzer that traverses dependency graphs and scores the risk
    of a proposed change.

Concepts practised:
    - graph traversal (BFS for impact propagation)
    - risk scoring with weighted factors
    - dataclasses for changes and impact results
    - dependency chain analysis
    - reporting with affected stakeholders
"""

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

    def _compute_risk(self, change: Change, affected_count: int,
                      max_depth: int, min_tier: int) -> float:
        score = 0.0
        # Change type weight
        type_weights = {
            ChangeType.SCHEMA: 30, ChangeType.INFRASTRUCTURE: 25,
            ChangeType.DEPENDENCY: 20, ChangeType.CODE: 10, ChangeType.CONFIG: 15,
        }
        score += type_weights.get(change.change_type, 10)
        # Blast radius
        score += min(30, affected_count * 5)
        # Depth of impact
        score += min(20, max_depth * 7)
        # Service tier (lower tier = more critical)
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
