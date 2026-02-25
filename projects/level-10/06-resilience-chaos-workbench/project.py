"""Resilience Chaos Workbench — Chaos engineering framework for testing system resilience.

Architecture: Uses the Strategy pattern for injectable fault types and an
Experiment runner that applies faults to a simulated service, measures impact,
and produces a resilience scorecard. Each fault is a self-contained ChaosAction
that can degrade latency, inject errors, or simulate resource exhaustion.

Design rationale: Netflix's Chaos Monkey proved that systems must be tested
against failure, not just success. This framework lets teams define experiments
declaratively, run them against a service model, and quantify resilience — turning
"we think it's reliable" into "we measured it handles N fault types."
"""
from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Protocol


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class FaultType(Enum):
    LATENCY = auto()
    ERROR = auto()
    RESOURCE_EXHAUSTION = auto()
    DEPENDENCY_DOWN = auto()


class ImpactLevel(Enum):
    NONE = "none"
    DEGRADED = "degraded"
    PARTIAL_OUTAGE = "partial_outage"
    FULL_OUTAGE = "full_outage"


@dataclass(frozen=True)
class FaultResult:
    """Outcome of injecting a single fault."""
    fault_type: FaultType
    description: str
    recovered: bool
    impact: ImpactLevel
    recovery_time_ms: int = 0
    details: str = ""


@dataclass
class ResilienceScore:
    """Quantified resilience across all experiments."""
    total_experiments: int = 0
    recovered: int = 0
    degraded: int = 0
    outages: int = 0

    @property
    def recovery_rate(self) -> float:
        if self.total_experiments == 0:
            return 0.0
        return self.recovered / self.total_experiments

    @property
    def grade(self) -> str:
        rate = self.recovery_rate
        if rate >= 0.95:
            return "A"
        if rate >= 0.80:
            return "B"
        if rate >= 0.60:
            return "C"
        if rate >= 0.40:
            return "D"
        return "F"


# ---------------------------------------------------------------------------
# Simulated service (the thing we test against)
# ---------------------------------------------------------------------------

@dataclass
class ServiceState:
    """Mutable state of a service under test."""
    name: str
    healthy: bool = True
    latency_ms: int = 10
    error_rate: float = 0.0
    memory_usage_pct: float = 30.0
    dependencies_up: set[str] = field(default_factory=lambda: {"db", "cache", "queue"})

    def handle_request(self) -> tuple[bool, int]:
        """Simulate handling a request. Returns (success, latency_ms)."""
        if not self.healthy:
            return False, 0
        if random.random() < self.error_rate:
            return False, self.latency_ms
        return True, self.latency_ms


# ---------------------------------------------------------------------------
# Chaos actions (Strategy pattern)
# ---------------------------------------------------------------------------

class ChaosAction(Protocol):
    """Strategy interface: a fault injection action."""
    def fault_type(self) -> FaultType: ...
    def apply(self, service: ServiceState) -> None: ...
    def rollback(self, service: ServiceState) -> None: ...
    def description(self) -> str: ...


@dataclass
class LatencySpike:
    """Injects artificial latency into the service."""
    added_ms: int = 500

    def fault_type(self) -> FaultType:
        return FaultType.LATENCY

    def apply(self, service: ServiceState) -> None:
        service.latency_ms += self.added_ms

    def rollback(self, service: ServiceState) -> None:
        service.latency_ms = max(10, service.latency_ms - self.added_ms)

    def description(self) -> str:
        return f"Add {self.added_ms}ms latency"


@dataclass
class ErrorInjection:
    """Forces the service to produce errors at a given rate."""
    error_rate: float = 0.5

    def fault_type(self) -> FaultType:
        return FaultType.ERROR

    def apply(self, service: ServiceState) -> None:
        service.error_rate = min(1.0, service.error_rate + self.error_rate)

    def rollback(self, service: ServiceState) -> None:
        service.error_rate = max(0.0, service.error_rate - self.error_rate)

    def description(self) -> str:
        return f"Inject {self.error_rate:.0%} error rate"


@dataclass
class MemoryPressure:
    """Simulates memory pressure by increasing usage percentage."""
    added_pct: float = 50.0

    def fault_type(self) -> FaultType:
        return FaultType.RESOURCE_EXHAUSTION

    def apply(self, service: ServiceState) -> None:
        service.memory_usage_pct = min(100.0, service.memory_usage_pct + self.added_pct)
        if service.memory_usage_pct >= 95.0:
            service.healthy = False

    def rollback(self, service: ServiceState) -> None:
        service.memory_usage_pct = max(0.0, service.memory_usage_pct - self.added_pct)
        if service.memory_usage_pct < 95.0:
            service.healthy = True

    def description(self) -> str:
        return f"Add {self.added_pct:.0f}% memory pressure"


@dataclass
class DependencyKill:
    """Takes down a named dependency."""
    dependency_name: str = "db"

    def fault_type(self) -> FaultType:
        return FaultType.DEPENDENCY_DOWN

    def apply(self, service: ServiceState) -> None:
        service.dependencies_up.discard(self.dependency_name)

    def rollback(self, service: ServiceState) -> None:
        service.dependencies_up.add(self.dependency_name)

    def description(self) -> str:
        return f"Kill dependency: {self.dependency_name}"


# ---------------------------------------------------------------------------
# Experiment runner
# ---------------------------------------------------------------------------

@dataclass
class Experiment:
    """A chaos experiment: apply fault, observe, measure, rollback."""
    name: str
    action: ChaosAction
    check_fn: Callable[[ServiceState], bool] | None = None

    def run(self, service: ServiceState) -> FaultResult:
        """Execute the experiment and return the result."""
        self.action.apply(service)

        # Default health check: service is healthy and can handle a request.
        check = self.check_fn or (lambda s: s.healthy)
        start = time.monotonic()
        is_healthy = check(service)

        self.action.rollback(service)
        recovery_ms = int((time.monotonic() - start) * 1000)

        # Re-check after rollback.
        recovered = check(service)

        if is_healthy:
            impact = ImpactLevel.NONE
        elif recovered:
            impact = ImpactLevel.DEGRADED
        else:
            impact = ImpactLevel.FULL_OUTAGE

        return FaultResult(
            fault_type=self.action.fault_type(),
            description=self.action.description(),
            recovered=recovered,
            impact=impact,
            recovery_time_ms=recovery_ms,
        )


class ChaosWorkbench:
    """Runs a suite of chaos experiments and produces a resilience scorecard."""

    def __init__(self, service: ServiceState) -> None:
        self._service = service
        self._experiments: list[Experiment] = []
        self._results: list[FaultResult] = []

    def add_experiment(self, exp: Experiment) -> None:
        self._experiments.append(exp)

    def run_all(self) -> list[FaultResult]:
        self._results = []
        for exp in self._experiments:
            result = exp.run(self._service)
            self._results.append(result)
        return self._results

    def scorecard(self) -> ResilienceScore:
        score = ResilienceScore(total_experiments=len(self._results))
        for r in self._results:
            if r.recovered:
                score.recovered += 1
            if r.impact == ImpactLevel.DEGRADED:
                score.degraded += 1
            if r.impact in (ImpactLevel.PARTIAL_OUTAGE, ImpactLevel.FULL_OUTAGE):
                score.outages += 1
        return score

    def report(self) -> dict[str, Any]:
        sc = self.scorecard()
        return {
            "service": self._service.name,
            "experiments": len(self._results),
            "recovery_rate": f"{sc.recovery_rate:.0%}",
            "grade": sc.grade,
            "results": [
                {
                    "fault": r.fault_type.name,
                    "description": r.description,
                    "recovered": r.recovered,
                    "impact": r.impact.value,
                }
                for r in self._results
            ],
        }


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

def main() -> None:
    import json

    service = ServiceState(name="order-service")
    workbench = ChaosWorkbench(service)

    workbench.add_experiment(Experiment("latency-spike", LatencySpike(500)))
    workbench.add_experiment(Experiment("error-injection", ErrorInjection(0.8)))
    workbench.add_experiment(Experiment("memory-pressure", MemoryPressure(70.0)))
    workbench.add_experiment(Experiment("kill-db", DependencyKill("db")))

    workbench.run_all()
    print(json.dumps(workbench.report(), indent=2))


if __name__ == "__main__":
    main()
