# Solution: Level 8 / Project 10 - Dependency Timeout Matrix

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
"""Dependency Timeout Matrix -- test timeout behavior across multiple dependencies."""

from __future__ import annotations

import argparse
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    TIMEOUT = "timeout"
    ERROR = "error"

# WHY per-dependency timeouts? -- A cache (5ms) and a payment API (2s) have
# vastly different latencies. One global timeout either kills valid slow
# operations or lets fast failures waste time. The critical flag controls
# whether a timeout degrades the whole system or just one feature.
@dataclass
class DependencyConfig:
    name: str
    timeout_seconds: float
    critical: bool = True
    retry_count: int = 1
    expected_latency_ms: float = 100.0

@dataclass
class DependencyResult:
    name: str
    status: HealthStatus
    latency_ms: float
    timed_out: bool = False
    error_message: str = ""
    retries_used: int = 0

@dataclass
class TimeoutMatrix:
    results: list[list[DependencyResult]] = field(default_factory=list)
    timeout_values: list[float] = field(default_factory=list)
    dependency_names: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        matrix = []
        for i, tv in enumerate(self.timeout_values):
            row: dict[str, Any] = {"timeout_seconds": tv}
            for r in self.results[i]:
                row[r.name] = {"status": r.status.value,
                               "latency_ms": round(r.latency_ms, 2),
                               "timed_out": r.timed_out}
            matrix.append(row)
        return {"matrix": matrix, "dependencies": self.dependency_names}

class DependencyChecker:
    """WHY ThreadPoolExecutor? -- Python has no built-in way to cancel a
    running function. future.result(timeout=N) lets the main thread give
    up waiting. In production, HTTP libraries have native timeout support."""

    def __init__(self) -> None:
        self._results: list[DependencyResult] = []

    def check(self, config: DependencyConfig,
              simulate_fn: Callable[[str], float] | None = None) -> DependencyResult:
        if simulate_fn is None:
            simulate_fn = self._default_simulate
        for attempt in range(config.retry_count):
            start = time.perf_counter()
            try:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(simulate_fn, config.name)
                    future.result(timeout=config.timeout_seconds)
                elapsed_ms = (time.perf_counter() - start) * 1000
                result = DependencyResult(name=config.name, status=HealthStatus.HEALTHY,
                                          latency_ms=elapsed_ms, retries_used=attempt)
                self._results.append(result)
                return result
            except FutureTimeout:
                elapsed_ms = (time.perf_counter() - start) * 1000
                if attempt == config.retry_count - 1:
                    result = DependencyResult(name=config.name, status=HealthStatus.TIMEOUT,
                                              latency_ms=elapsed_ms, timed_out=True,
                                              retries_used=attempt + 1)
                    self._results.append(result)
                    return result
            except Exception as exc:
                elapsed_ms = (time.perf_counter() - start) * 1000
                result = DependencyResult(name=config.name, status=HealthStatus.ERROR,
                                          latency_ms=elapsed_ms, error_message=str(exc),
                                          retries_used=attempt + 1)
                self._results.append(result)
                return result
        return DependencyResult(name=config.name, status=HealthStatus.ERROR, latency_ms=0)

    @staticmethod
    def _default_simulate(name: str) -> float:
        latency = random.uniform(0.01, 0.2)
        time.sleep(latency)
        return latency

    @property
    def all_results(self) -> list[DependencyResult]:
        return list(self._results)

def build_timeout_matrix(dependencies: list[DependencyConfig],
                         timeout_values: list[float],
                         simulate_fn: Callable[[str], float] | None = None) -> TimeoutMatrix:
    matrix = TimeoutMatrix(timeout_values=timeout_values,
                           dependency_names=[d.name for d in dependencies])
    for tv in timeout_values:
        checker = DependencyChecker()
        row = []
        for dep in dependencies:
            adjusted = DependencyConfig(name=dep.name, timeout_seconds=tv,
                                        critical=dep.critical, retry_count=dep.retry_count)
            row.append(checker.check(adjusted, simulate_fn=simulate_fn))
        matrix.results.append(row)
    return matrix

# WHY 1.5x recommended timeout? -- The minimum passing timeout has zero
# margin. 50% buffer absorbs natural latency variance without being so
# generous that failures take too long to detect.
def analyze_matrix(matrix: TimeoutMatrix) -> dict[str, Any]:
    analysis: dict[str, Any] = {}
    for dep in matrix.dependency_names:
        min_pass: float | None = None
        for i, tv in enumerate(matrix.timeout_values):
            for r in matrix.results[i]:
                if r.name == dep and r.status == HealthStatus.HEALTHY:
                    if min_pass is None or tv < min_pass:
                        min_pass = tv
                    break
        analysis[dep] = {"min_passing_timeout": min_pass,
                         "recommended_timeout": round(min_pass * 1.5, 2) if min_pass else None}
    return analysis

def run_demo() -> dict[str, Any]:
    rng = random.Random(42)
    profiles = {"auth-service": 0.03, "database": 0.05, "cache": 0.01,
                "search-api": 0.08, "notification-svc": 0.15}
    def simulate(name: str) -> float:
        base = profiles.get(name, 0.05)
        actual = base * rng.uniform(0.5, 2.0)
        time.sleep(actual)
        return actual
    deps = [DependencyConfig(name=n, timeout_seconds=0.1, critical=True) for n in profiles]
    matrix = build_timeout_matrix(deps, [0.02, 0.05, 0.1, 0.2, 0.5], simulate_fn=simulate)
    return {"matrix": matrix.to_dict(), "analysis": analyze_matrix(matrix)}

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Dependency timeout matrix tester")
    parser.add_argument("--demo", action="store_true", default=True)
    parser.parse_args(argv)
    print(json.dumps(run_demo(), indent=2))

if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Per-dependency timeout configs | Each service has different latency profiles | Global timeout -- either too aggressive for slow services or too lenient for fast ones |
| ThreadPoolExecutor for timeout enforcement | Standard library; `future.result(timeout=N)` enforces deadlines | `signal.alarm()` -- Unix-only, doesn't work on Windows or in threads |
| Matrix testing (all deps x all timeouts) | Reveals the minimum viable timeout for each service empirically | Single-timeout test -- tells pass/fail but not optimal configuration |
| 1.5x safety margin recommendation | Absorbs natural variance; not so generous that failures hang | 2-3x -- safer but delays failure detection significantly |

## Alternative approaches

### Approach B: Adaptive timeout with percentile tracking

```python
class AdaptiveTimeout:
    """Auto-adjust timeout based on observed p99 latency + margin."""
    def __init__(self, margin: float = 1.5):
        self.latencies: list[float] = []
        self.margin = margin

    def record(self, latency_ms: float) -> None:
        self.latencies.append(latency_ms)

    @property
    def recommended_timeout(self) -> float:
        if len(self.latencies) < 10:
            return 1.0  # conservative default
        p99 = sorted(self.latencies)[int(len(self.latencies) * 0.99)]
        return p99 * self.margin / 1000  # convert to seconds
```

**Trade-off:** Adaptive timeouts eliminate manual configuration. The risk is that during degradation, latencies climb and timeouts climb with them -- you might want fixed timeouts so slow responses are rejected quickly. Use adaptive for stable services, fixed for SLA-bound ones.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Timeout of 0 seconds | FutureTimeout fires immediately, even for instant operations | Validate `timeout_seconds > 0` in DependencyConfig |
| Worker thread not cancelled | Python cannot kill threads; the worker keeps running after timeout | Accept the leaked thread or use processes instead of threads |
| Retrying same broken instance | N retries against the same down server wastes time | Add jitter between retries; route retries to different instances |
