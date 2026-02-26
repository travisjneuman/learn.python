# Solution: Level 10 / Project 06 - Resilience Chaos Workbench

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
>.

---

## Complete solution

```python
"""Resilience Chaos Workbench -- Chaos engineering framework for testing system resilience."""
from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Protocol


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


# WHY track recovery_time_ms per fault? -- Resilience is not binary. A system
# that recovers in 50ms vs 30 seconds has vastly different user impact.
# Measuring recovery time per fault type produces a quantified scorecard.
@dataclass(frozen=True)
class FaultResult:
    fault_type: FaultType
    description: str
    recovered: bool
    impact: ImpactLevel
    recovery_time_ms: int = 0
    details: str = ""


@dataclass
class ResilienceScore:
    total_experiments: int = 0
    recovered: int = 0
    degraded: int = 0
    outages: int = 0

    @property
    def recovery_rate(self) -> float:
        if self.total_experiments == 0:
            return 0.0
        return self.recovered / self.total_experiments

    # WHY letter grades? -- Executives and non-technical stakeholders understand
    # A/B/C/D/F immediately. The thresholds (95/80/60/40) are inspired by SRE
    # practices where 95%+ recovery is "production-ready."
    @property
    def grade(self) -> str:
        rate = self.recovery_rate
        if rate >= 0.95: return "A"
        if rate >= 0.80: return "B"
        if rate >= 0.60: return "C"
        if rate >= 0.40: return "D"
        return "F"


@dataclass
class ServiceState:
    name: str
    healthy: bool = True
    latency_ms: int = 10
    error_rate: float = 0.0
    memory_usage_pct: float = 30.0
    dependencies_up: set[str] = field(default_factory=lambda: {"db", "cache", "queue"})

    def handle_request(self) -> tuple[bool, int]:
        if not self.healthy:
            return False, 0
        if random.random() < self.error_rate:
            return False, self.latency_ms
        return True, self.latency_ms


# WHY Strategy pattern for ChaosAction? -- Each fault type (latency, errors,
# memory, dependency kill) has unique apply/rollback logic. The Strategy pattern
# lets you add new fault types without modifying the experiment runner.
class ChaosAction(Protocol):
    def fault_type(self) -> FaultType: ...
    def apply(self, service: ServiceState) -> None: ...
    def rollback(self, service: ServiceState) -> None: ...
    def description(self) -> str: ...


@dataclass
class LatencySpike:
    added_ms: int = 500
    def fault_type(self) -> FaultType: return FaultType.LATENCY
    def apply(self, service: ServiceState) -> None:
        service.latency_ms += self.added_ms
    # WHY max(10, ...) on rollback? -- Ensures latency never goes below a
    # realistic baseline, even if multiple rollbacks stack.
    def rollback(self, service: ServiceState) -> None:
        service.latency_ms = max(10, service.latency_ms - self.added_ms)
    def description(self) -> str: return f"Add {self.added_ms}ms latency"


@dataclass
class ErrorInjection:
    error_rate: float = 0.5
    def fault_type(self) -> FaultType: return FaultType.ERROR
    def apply(self, service: ServiceState) -> None:
        service.error_rate = min(1.0, service.error_rate + self.error_rate)
    def rollback(self, service: ServiceState) -> None:
        service.error_rate = max(0.0, service.error_rate - self.error_rate)
    def description(self) -> str: return f"Inject {self.error_rate:.0%} error rate"


@dataclass
class MemoryPressure:
    added_pct: float = 50.0
    def fault_type(self) -> FaultType: return FaultType.RESOURCE_EXHAUSTION
    # WHY unhealthy at 95%? -- OOM kills happen at 100%. Setting the threshold
    # at 95% simulates the realistic "danger zone" where GC thrashing begins.
    def apply(self, service: ServiceState) -> None:
        service.memory_usage_pct = min(100.0, service.memory_usage_pct + self.added_pct)
        if service.memory_usage_pct >= 95.0:
            service.healthy = False
    def rollback(self, service: ServiceState) -> None:
        service.memory_usage_pct = max(0.0, service.memory_usage_pct - self.added_pct)
        if service.memory_usage_pct < 95.0:
            service.healthy = True
    def description(self) -> str: return f"Add {self.added_pct:.0f}% memory pressure"


@dataclass
class DependencyKill:
    dependency_name: str = "db"
    def fault_type(self) -> FaultType: return FaultType.DEPENDENCY_DOWN
    def apply(self, service: ServiceState) -> None:
        service.dependencies_up.discard(self.dependency_name)
    def rollback(self, service: ServiceState) -> None:
        service.dependencies_up.add(self.dependency_name)
    def description(self) -> str: return f"Kill dependency: {self.dependency_name}"


@dataclass
class Experiment:
    name: str
    action: ChaosAction
    check_fn: Callable[[ServiceState], bool] | None = None

    # WHY apply -> check -> rollback -> re-check? -- This four-step cycle measures
    # both the fault impact (check during fault) and the recovery ability
    # (re-check after rollback). A system that does not recover after rollback
    # has state corruption issues.
    def run(self, service: ServiceState) -> FaultResult:
        self.action.apply(service)
        check = self.check_fn or (lambda s: s.healthy)
        start = time.monotonic()
        is_healthy = check(service)
        self.action.rollback(service)
        recovery_ms = int((time.monotonic() - start) * 1000)
        recovered = check(service)

        if is_healthy:
            impact = ImpactLevel.NONE
        elif recovered:
            impact = ImpactLevel.DEGRADED
        else:
            impact = ImpactLevel.FULL_OUTAGE

        return FaultResult(self.action.fault_type(), self.action.description(),
                           recovered, impact, recovery_ms)


class ChaosWorkbench:
    def __init__(self, service: ServiceState) -> None:
        self._service = service
        self._experiments: list[Experiment] = []
        self._results: list[FaultResult] = []

    def add_experiment(self, exp: Experiment) -> None:
        self._experiments.append(exp)

    def run_all(self) -> list[FaultResult]:
        self._results = []
        for exp in self._experiments:
            self._results.append(exp.run(self._service))
        return self._results

    def scorecard(self) -> ResilienceScore:
        score = ResilienceScore(total_experiments=len(self._results))
        for r in self._results:
            if r.recovered: score.recovered += 1
            if r.impact == ImpactLevel.DEGRADED: score.degraded += 1
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
                {"fault": r.fault_type.name, "description": r.description,
                 "recovered": r.recovered, "impact": r.impact.value}
                for r in self._results
            ],
        }


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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Strategy pattern for ChaosAction | Each fault type has unique apply/rollback logic; new faults added without modifying the runner | Single function with if/elif branches -- hard to extend and test independently |
| Apply-check-rollback-recheck cycle | Measures both fault impact and recovery ability in one experiment | Apply-rollback only -- misses the "did it actually recover?" question |
| Letter grade scoring (A-F) | Communicates resilience posture to non-technical stakeholders instantly | Raw percentage -- less intuitive for executive reporting |
| Mutable ServiceState | Chaos actions must modify state to simulate faults; immutability would require copying entire state per experiment | Copy-on-write -- correct but adds allocation overhead for rapid experiments |

## Alternative approaches

### Approach B: Async parallel experiment runner

```python
import asyncio

async def run_parallel(experiments: list[Experiment], service: ServiceState) -> list[FaultResult]:
    # Each experiment gets its own copy to avoid interference.
    async def run_one(exp: Experiment) -> FaultResult:
        svc_copy = ServiceState(name=service.name, healthy=service.healthy,
                                 latency_ms=service.latency_ms)
        return exp.run(svc_copy)
    return await asyncio.gather(*(run_one(e) for e in experiments))
```

**Trade-off:** Parallel execution is faster and tests fault isolation (experiments do not interfere). However, it requires copying state per experiment and does not model the real-world scenario where faults compound on the same service.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| MemoryPressure set to 100% | Service becomes unhealthy; rollback restores memory but `healthy` flag may remain False if math is imprecise | Use `< 95.0` threshold consistently in both apply and rollback |
| Running experiments on shared mutable state without resetting | Earlier experiments contaminate later ones (e.g., latency stays elevated) | Reset service state between experiments or use per-experiment copies |
| No experiments added before calling `scorecard()` | Returns 0.0 recovery rate and grade "F" with zero experiments | Add a guard requiring at least one experiment before producing a scorecard |
