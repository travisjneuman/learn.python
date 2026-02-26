"""Strategic Architecture Review — Architecture fitness functions and review automation.

Architecture: Defines fitness functions as measurable checks against architectural
qualities (coupling, cohesion, complexity, dependency depth). A ReviewEngine
collects fitness results, computes a health score, and produces recommendations.
Uses the Observer pattern where each fitness function reports independently.

Design rationale: Architecture erodes silently — each small shortcut seems harmless
until the system becomes unmaintainable. Fitness functions make architectural
constraints executable and measurable, so drift is detected automatically in CI
rather than discovered during a crisis.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

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


# WHY fitness functions? -- From "Building Evolutionary Architectures":
# fitness functions are automated checks that guard architectural qualities.
# Unlike one-time reviews, they run continuously in CI. A coupling metric
# that crosses its threshold triggers a build failure before the degradation
# reaches production — making architecture constraints executable, not just
# documented.
@dataclass(frozen=True)
class FitnessResult:
    """Result of evaluating one fitness function."""
    attribute: QualityAttribute
    metric_name: str
    value: float
    threshold: float
    passed: bool
    message: str

    @property
    def status(self) -> HealthStatus:
        if self.passed:
            return HealthStatus.HEALTHY
        ratio = self.value / self.threshold if self.threshold > 0 else 0
        if ratio < 1.5:
            return HealthStatus.WARNING
        return HealthStatus.CRITICAL


@dataclass(frozen=True)
class Recommendation:
    """Actionable suggestion from a fitness function failure."""
    attribute: QualityAttribute
    priority: int  # 1=highest
    title: str
    description: str


@dataclass
class ArchitectureReport:
    """Aggregate review of all fitness functions."""
    system_name: str
    results: list[FitnessResult] = field(default_factory=list)
    recommendations: list[Recommendation] = field(default_factory=list)

    @property
    def health_score(self) -> float:
        if not self.results:
            return 0.0
        passed = sum(1 for r in self.results if r.passed)
        return (passed / len(self.results)) * 100

    @property
    def overall_status(self) -> HealthStatus:
        if self.health_score >= 80:
            return HealthStatus.HEALTHY
        if self.health_score >= 50:
            return HealthStatus.WARNING
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


# ---------------------------------------------------------------------------
# Fitness functions (Observer pattern)
# ---------------------------------------------------------------------------

class FitnessFunction(Protocol):
    """Protocol for architecture fitness checks."""
    def attribute(self) -> QualityAttribute: ...
    def evaluate(self, system: SystemModel) -> FitnessResult: ...
    def recommend(self, result: FitnessResult) -> Recommendation | None: ...


@dataclass(frozen=True)
class ServiceDef:
    """Definition of a service in the system model."""
    name: str
    dependencies: list[str] = field(default_factory=list)
    lines_of_code: int = 0
    test_coverage_pct: float = 0.0
    api_version: str = "v1"


@dataclass
class SystemModel:
    """Model of the system under review."""
    name: str
    services: dict[str, ServiceDef] = field(default_factory=dict)

    def add_service(self, svc: ServiceDef) -> None:
        self.services[svc.name] = svc

    @property
    def service_count(self) -> int:
        return len(self.services)


# ---------------------------------------------------------------------------
# Concrete fitness functions
# ---------------------------------------------------------------------------

class CouplingCheck:
    """Measures average number of dependencies per service."""
    def __init__(self, max_avg_deps: float = 3.0) -> None:
        self._threshold = max_avg_deps

    def attribute(self) -> QualityAttribute:
        return QualityAttribute.COUPLING

    def evaluate(self, system: SystemModel) -> FitnessResult:
        if not system.services:
            return FitnessResult(self.attribute(), "avg_dependencies", 0, self._threshold, True, "No services")
        avg = sum(len(s.dependencies) for s in system.services.values()) / len(system.services)
        passed = avg <= self._threshold
        return FitnessResult(
            self.attribute(), "avg_dependencies", round(avg, 2), self._threshold,
            passed, f"Average deps: {avg:.1f} (max: {self._threshold})",
        )

    def recommend(self, result: FitnessResult) -> Recommendation | None:
        if result.passed:
            return None
        return Recommendation(
            self.attribute(), 1, "Reduce service coupling",
            "Extract shared dependencies into a common library or introduce an event bus.",
        )


class ComplexityCheck:
    """Checks that no service exceeds a lines-of-code threshold."""
    def __init__(self, max_loc: int = 5000) -> None:
        self._threshold = max_loc

    def attribute(self) -> QualityAttribute:
        return QualityAttribute.COMPLEXITY

    def evaluate(self, system: SystemModel) -> FitnessResult:
        largest = max((s.lines_of_code for s in system.services.values()), default=0)
        passed = largest <= self._threshold
        return FitnessResult(
            self.attribute(), "max_service_loc", largest, self._threshold,
            passed, f"Largest service: {largest} LOC (max: {self._threshold})",
        )

    def recommend(self, result: FitnessResult) -> Recommendation | None:
        if result.passed:
            return None
        return Recommendation(
            self.attribute(), 2, "Split large services",
            "Decompose services exceeding the LOC threshold into smaller, focused modules.",
        )


class TestCoverageCheck:
    """Ensures minimum test coverage across all services."""
    def __init__(self, min_coverage: float = 70.0) -> None:
        self._threshold = min_coverage

    def attribute(self) -> QualityAttribute:
        return QualityAttribute.TEST_COVERAGE

    def evaluate(self, system: SystemModel) -> FitnessResult:
        if not system.services:
            return FitnessResult(self.attribute(), "min_coverage", 0, self._threshold, False, "No services")
        min_cov = min(s.test_coverage_pct for s in system.services.values())
        passed = min_cov >= self._threshold
        return FitnessResult(
            self.attribute(), "min_coverage", min_cov, self._threshold,
            passed, f"Lowest coverage: {min_cov:.0f}% (min: {self._threshold:.0f}%)",
        )

    def recommend(self, result: FitnessResult) -> Recommendation | None:
        if result.passed:
            return None
        return Recommendation(
            self.attribute(), 2, "Increase test coverage",
            "Add unit and integration tests to services below the coverage threshold.",
        )


class DependencyDepthCheck:
    """Checks max transitive dependency depth (prevents deep call chains)."""
    def __init__(self, max_depth: int = 4) -> None:
        self._threshold = max_depth

    def attribute(self) -> QualityAttribute:
        return QualityAttribute.DEPENDENCY_DEPTH

    def evaluate(self, system: SystemModel) -> FitnessResult:
        max_depth = 0
        for svc in system.services.values():
            depth = self._compute_depth(svc.name, system, set())
            max_depth = max(max_depth, depth)
        passed = max_depth <= self._threshold
        return FitnessResult(
            self.attribute(), "max_dep_depth", max_depth, self._threshold,
            passed, f"Max depth: {max_depth} (max: {self._threshold})",
        )

    def _compute_depth(self, name: str, system: SystemModel, visited: set[str]) -> int:
        if name in visited or name not in system.services:
            return 0
        visited.add(name)
        svc = system.services[name]
        if not svc.dependencies:
            return 0
        return 1 + max(self._compute_depth(d, system, visited) for d in svc.dependencies)

    def recommend(self, result: FitnessResult) -> Recommendation | None:
        if result.passed:
            return None
        return Recommendation(
            self.attribute(), 1, "Flatten dependency chains",
            "Introduce facades or event-driven patterns to reduce transitive depth.",
        )


# ---------------------------------------------------------------------------
# Review engine
# ---------------------------------------------------------------------------

class ReviewEngine:
    """Runs all fitness functions and produces an architecture report."""

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
    engine.register(CouplingCheck())
    engine.register(ComplexityCheck())
    engine.register(TestCoverageCheck())
    engine.register(DependencyDepthCheck())
    return engine


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

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
