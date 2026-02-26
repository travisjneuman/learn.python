# Solution: Level 10 / Project 09 - Strategic Architecture Review

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Strategic Architecture Review -- Fitness functions and automated review."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol


class QualityAttribute(Enum):
    COUPLING = auto()
    COHESION = auto()
    COMPLEXITY = auto()
    DEPENDENCY_DEPTH = auto()
    TEST_COVERAGE = auto()
    API_STABILITY = auto()


class HealthStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


# WHY fitness functions? -- From "Building Evolutionary Architectures": fitness
# functions are automated checks that guard architectural qualities. Unlike
# one-time reviews, they run continuously in CI, catching drift before it
# reaches production.
@dataclass(frozen=True)
class FitnessResult:
    attribute: QualityAttribute
    metric_name: str
    value: float
    threshold: float
    passed: bool
    message: str

    # WHY ratio-based status? -- A value 10% over threshold is a WARNING;
    # 50%+ over is CRITICAL. This graduated response avoids "all-or-nothing"
    # thinking and prioritizes the worst violations.
    @property
    def status(self) -> HealthStatus:
        if self.passed:
            return HealthStatus.HEALTHY
        ratio = self.value / self.threshold if self.threshold > 0 else 0
        return HealthStatus.WARNING if ratio < 1.5 else HealthStatus.CRITICAL


@dataclass(frozen=True)
class Recommendation:
    attribute: QualityAttribute
    priority: int  # 1=highest
    title: str
    description: str


@dataclass
class ArchitectureReport:
    system_name: str
    results: list[FitnessResult] = field(default_factory=list)
    recommendations: list[Recommendation] = field(default_factory=list)

    # WHY percentage-based health score? -- A single number communicates overall
    # system health at a glance. Executives track this over time to see if
    # architecture is improving or degrading.
    @property
    def health_score(self) -> float:
        if not self.results: return 0.0
        return (sum(1 for r in self.results if r.passed) / len(self.results)) * 100

    @property
    def overall_status(self) -> HealthStatus:
        if self.health_score >= 80: return HealthStatus.HEALTHY
        if self.health_score >= 50: return HealthStatus.WARNING
        return HealthStatus.CRITICAL

    def summary(self) -> dict[str, Any]:
        return {
            "system": self.system_name,
            "health_score": round(self.health_score, 1),
            "status": self.overall_status.value,
            "total_checks": len(self.results),
            "passed": sum(1 for r in self.results if r.passed),
            "failed": sum(1 for r in self.results if not r.passed),
            "recommendations": [
                {"priority": r.priority, "title": r.title}
                for r in sorted(self.recommendations, key=lambda x: x.priority)
            ],
        }


class FitnessFunction(Protocol):
    def attribute(self) -> QualityAttribute: ...
    def evaluate(self, system: SystemModel) -> FitnessResult: ...
    def recommend(self, result: FitnessResult) -> Recommendation | None: ...


@dataclass(frozen=True)
class ServiceDef:
    name: str
    dependencies: list[str] = field(default_factory=list)
    lines_of_code: int = 0
    test_coverage_pct: float = 0.0
    api_version: str = "v1"


@dataclass
class SystemModel:
    name: str
    services: dict[str, ServiceDef] = field(default_factory=dict)
    def add_service(self, svc: ServiceDef) -> None:
        self.services[svc.name] = svc
    @property
    def service_count(self) -> int:
        return len(self.services)


class CouplingCheck:
    def __init__(self, max_avg_deps: float = 3.0) -> None:
        self._threshold = max_avg_deps
    def attribute(self) -> QualityAttribute: return QualityAttribute.COUPLING
    def evaluate(self, system: SystemModel) -> FitnessResult:
        if not system.services:
            return FitnessResult(self.attribute(), "avg_dependencies", 0,
                                  self._threshold, True, "No services")
        avg = sum(len(s.dependencies) for s in system.services.values()) / len(system.services)
        return FitnessResult(self.attribute(), "avg_dependencies", round(avg, 2),
                              self._threshold, avg <= self._threshold,
                              f"Average deps: {avg:.1f} (max: {self._threshold})")
    def recommend(self, result: FitnessResult) -> Recommendation | None:
        if result.passed: return None
        return Recommendation(self.attribute(), 1, "Reduce service coupling",
                              "Extract shared dependencies into a common library or event bus.")


class ComplexityCheck:
    def __init__(self, max_loc: int = 5000) -> None:
        self._threshold = max_loc
    def attribute(self) -> QualityAttribute: return QualityAttribute.COMPLEXITY
    def evaluate(self, system: SystemModel) -> FitnessResult:
        largest = max((s.lines_of_code for s in system.services.values()), default=0)
        return FitnessResult(self.attribute(), "max_service_loc", largest,
                              self._threshold, largest <= self._threshold,
                              f"Largest service: {largest} LOC (max: {self._threshold})")
    def recommend(self, result: FitnessResult) -> Recommendation | None:
        if result.passed: return None
        return Recommendation(self.attribute(), 2, "Split large services",
                              "Decompose services exceeding the LOC threshold.")


class TestCoverageCheck:
    def __init__(self, min_coverage: float = 70.0) -> None:
        self._threshold = min_coverage
    def attribute(self) -> QualityAttribute: return QualityAttribute.TEST_COVERAGE
    def evaluate(self, system: SystemModel) -> FitnessResult:
        if not system.services:
            return FitnessResult(self.attribute(), "min_coverage", 0,
                                  self._threshold, False, "No services")
        min_cov = min(s.test_coverage_pct for s in system.services.values())
        return FitnessResult(self.attribute(), "min_coverage", min_cov,
                              self._threshold, min_cov >= self._threshold,
                              f"Lowest coverage: {min_cov:.0f}% (min: {self._threshold:.0f}%)")
    def recommend(self, result: FitnessResult) -> Recommendation | None:
        if result.passed: return None
        return Recommendation(self.attribute(), 2, "Increase test coverage",
                              "Add tests to services below the coverage threshold.")


class DependencyDepthCheck:
    def __init__(self, max_depth: int = 4) -> None:
        self._threshold = max_depth
    def attribute(self) -> QualityAttribute: return QualityAttribute.DEPENDENCY_DEPTH
    def evaluate(self, system: SystemModel) -> FitnessResult:
        max_depth = 0
        for svc in system.services.values():
            depth = self._compute_depth(svc.name, system, set())
            max_depth = max(max_depth, depth)
        return FitnessResult(self.attribute(), "max_dep_depth", max_depth,
                              self._threshold, max_depth <= self._threshold,
                              f"Max depth: {max_depth} (max: {self._threshold})")
    # WHY visited set? -- Prevents infinite recursion when services have
    # circular dependencies. A visited node returns depth 0, breaking the cycle.
    def _compute_depth(self, name: str, system: SystemModel, visited: set[str]) -> int:
        if name in visited or name not in system.services:
            return 0
        visited.add(name)
        svc = system.services[name]
        if not svc.dependencies:
            return 0
        return 1 + max(self._compute_depth(d, system, visited) for d in svc.dependencies)
    def recommend(self, result: FitnessResult) -> Recommendation | None:
        if result.passed: return None
        return Recommendation(self.attribute(), 1, "Flatten dependency chains",
                              "Introduce facades or event-driven patterns to reduce depth.")


class ReviewEngine:
    def __init__(self) -> None:
        self._functions: list[FitnessFunction] = []
    def register(self, fn: FitnessFunction) -> None:
        self._functions.append(fn)
    @property
    def check_count(self) -> int:
        return len(self._functions)
    def review(self, system: SystemModel) -> ArchitectureReport:
        report = ArchitectureReport(system_name=system.name)
        for fn in self._functions:
            result = fn.evaluate(system)
            report.results.append(result)
            rec = fn.recommend(result)
            if rec is not None:
                report.recommendations.append(rec)
        return report


def build_default_engine() -> ReviewEngine:
    engine = ReviewEngine()
    for check in [CouplingCheck(), ComplexityCheck(), TestCoverageCheck(), DependencyDepthCheck()]:
        engine.register(check)
    return engine


def main() -> None:
    system = SystemModel("ecommerce-platform")
    system.add_service(ServiceDef("api-gateway", ["auth", "catalog", "orders"], 2000, 85.0))
    system.add_service(ServiceDef("auth", [], 800, 90.0))
    system.add_service(ServiceDef("catalog", ["db"], 3500, 75.0))
    system.add_service(ServiceDef("orders", ["catalog", "payment", "notification"], 6000, 60.0))
    system.add_service(ServiceDef("payment", ["auth"], 1200, 80.0))
    system.add_service(ServiceDef("notification", [], 500, 40.0))
    engine = build_default_engine()
    report = engine.review(system)
    print(json.dumps(report.summary(), indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Fitness functions as executable constraints | Run in CI to catch drift automatically, unlike one-time architecture reviews | Manual architecture reviews -- infrequent and miss incremental degradation |
| Each function produces a recommendation on failure | Actionable output, not just pass/fail -- engineers know what to fix | Pass/fail only -- requires manual analysis to determine remediation |
| Visited set in depth calculation | Prevents infinite recursion on circular dependencies | Stack-based cycle detection -- more complex with no benefit for this use case |
| Health score as percentage of passing checks | Single number for executive dashboards; trends over time reveal improvement or decay | Weighted scoring -- more accurate but harder to explain |

## Alternative approaches

### Approach B: Graph-based analysis with NetworkX

```python
import networkx as nx

def analyze_architecture(system: SystemModel) -> dict:
    G = nx.DiGraph()
    for svc in system.services.values():
        for dep in svc.dependencies:
            G.add_edge(svc.name, dep)
    return {
        "cycles": list(nx.simple_cycles(G)),
        "longest_path": nx.dag_longest_path_length(G) if nx.is_directed_acyclic_graph(G) else -1,
        "avg_degree": sum(dict(G.degree()).values()) / G.number_of_nodes(),
    }
```

**Trade-off:** NetworkX provides battle-tested graph algorithms (cycle detection, longest path, centrality) out of the box. However, it adds an external dependency and obscures the learning objective of implementing these algorithms yourself.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Service with 10+ dependencies | Coupling check fails; average deps exceeds threshold | Add configurable per-service thresholds for legitimate high-dependency services |
| Circular dependency (A->B->A) | `_compute_depth` returns 0 for the cycle, which may under-report depth | Detect and report cycles explicitly before computing depth |
| No services in the system model | All checks pass trivially with default values | Add a minimum service count guard before running the review |
