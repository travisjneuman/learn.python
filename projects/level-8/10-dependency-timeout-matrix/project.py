"""Dependency Timeout Matrix — test timeout behavior across multiple dependencies.

Design rationale:
    Microservice systems depend on many external services, each with different
    latency profiles. This project builds a dependency manager that configures
    per-service timeouts, tracks timeout violations, and identifies which
    dependencies are degrading system performance.

Concepts practised:
    - threading with timeout enforcement
    - dataclasses for dependency configuration
    - matrix-style testing across configurations
    - concurrent.futures for parallel dependency checks
    - statistical analysis of timeout patterns
"""

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class DependencyConfig:
    """Configuration for a single external dependency."""
    name: str
    timeout_seconds: float
    critical: bool = True  # If True, timeout means system degraded
    retry_count: int = 1
    expected_latency_ms: float = 100.0


@dataclass
class DependencyResult:
    """Result of a single dependency check."""
    name: str
    status: HealthStatus
    latency_ms: float
    timed_out: bool = False
    error_message: str = ""
    retries_used: int = 0


@dataclass
class TimeoutMatrix:
    """Results of testing all dependencies at various timeout settings."""
    results: list[list[DependencyResult]] = field(default_factory=list)
    timeout_values: list[float] = field(default_factory=list)
    dependency_names: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        matrix: list[dict[str, Any]] = []
        for i, timeout_val in enumerate(self.timeout_values):
            row: dict[str, Any] = {"timeout_seconds": timeout_val}
            for result in self.results[i]:
                row[result.name] = {
                    "status": result.status.value,
                    "latency_ms": round(result.latency_ms, 2),
                    "timed_out": result.timed_out,
                }
            matrix.append(row)
        return {"matrix": matrix, "dependencies": self.dependency_names}


# --- Dependency checker -------------------------------------------------

class DependencyChecker:
    """Checks dependency health with configurable timeouts.

    Simulates calling external services and enforces timeout constraints.
    In production, the simulate_fn would be replaced with actual HTTP calls.
    """

    def __init__(self) -> None:
        self._results: list[DependencyResult] = []

    def check(
        self,
        config: DependencyConfig,
        simulate_fn: Callable[[str], float] | None = None,
    ) -> DependencyResult:
        """Check a dependency with timeout enforcement and retries."""
        if simulate_fn is None:
            simulate_fn = self._default_simulate

        for attempt in range(config.retry_count):
            start = time.perf_counter()
            try:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(simulate_fn, config.name)
                    simulated_latency = future.result(timeout=config.timeout_seconds)

                elapsed_ms = (time.perf_counter() - start) * 1000
                result = DependencyResult(
                    name=config.name,
                    status=HealthStatus.HEALTHY,
                    latency_ms=elapsed_ms,
                    retries_used=attempt,
                )
                self._results.append(result)
                return result

            except FutureTimeout:
                elapsed_ms = (time.perf_counter() - start) * 1000
                if attempt == config.retry_count - 1:
                    result = DependencyResult(
                        name=config.name,
                        status=HealthStatus.TIMEOUT,
                        latency_ms=elapsed_ms,
                        timed_out=True,
                        retries_used=attempt + 1,
                    )
                    self._results.append(result)
                    return result

            except Exception as exc:
                elapsed_ms = (time.perf_counter() - start) * 1000
                result = DependencyResult(
                    name=config.name,
                    status=HealthStatus.ERROR,
                    latency_ms=elapsed_ms,
                    error_message=str(exc),
                    retries_used=attempt + 1,
                )
                self._results.append(result)
                return result

        # Should not reach here, but satisfy type checker
        return DependencyResult(
            name=config.name, status=HealthStatus.ERROR, latency_ms=0,
        )

    @staticmethod
    def _default_simulate(name: str) -> float:
        """Default simulation with random latency."""
        import random
        latency = random.uniform(0.01, 0.2)
        time.sleep(latency)
        return latency

    @property
    def all_results(self) -> list[DependencyResult]:
        return list(self._results)


# --- Matrix builder -----------------------------------------------------

def build_timeout_matrix(
    dependencies: list[DependencyConfig],
    timeout_values: list[float],
    simulate_fn: Callable[[str], float] | None = None,
) -> TimeoutMatrix:
    """Test all dependencies across multiple timeout configurations.

    This creates a matrix showing which dependencies pass at each timeout level,
    helping identify the minimum viable timeout for each service.
    """
    matrix = TimeoutMatrix(
        timeout_values=timeout_values,
        dependency_names=[d.name for d in dependencies],
    )

    for timeout_val in timeout_values:
        checker = DependencyChecker()
        row_results: list[DependencyResult] = []
        for dep in dependencies:
            adjusted = DependencyConfig(
                name=dep.name,
                timeout_seconds=timeout_val,
                critical=dep.critical,
                retry_count=dep.retry_count,
            )
            result = checker.check(adjusted, simulate_fn=simulate_fn)
            row_results.append(result)
        matrix.results.append(row_results)

    return matrix


def analyze_matrix(matrix: TimeoutMatrix) -> dict[str, Any]:
    """Analyze matrix results to find optimal timeout per dependency."""
    analysis: dict[str, Any] = {}
    for dep_name in matrix.dependency_names:
        min_passing_timeout: float | None = None
        for i, timeout_val in enumerate(matrix.timeout_values):
            for result in matrix.results[i]:
                if result.name == dep_name and result.status == HealthStatus.HEALTHY:
                    if min_passing_timeout is None or timeout_val < min_passing_timeout:
                        min_passing_timeout = timeout_val
                    break
        analysis[dep_name] = {
            "min_passing_timeout": min_passing_timeout,
            "recommended_timeout": round(min_passing_timeout * 1.5, 2)
            if min_passing_timeout else None,
        }
    return analysis


# --- CLI ----------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    """Run a demo timeout matrix test."""
    import random
    rng = random.Random(42)

    # Simulate dependencies with different latency profiles
    latency_profiles = {
        "auth-service": 0.03,
        "database": 0.05,
        "cache": 0.01,
        "search-api": 0.08,
        "notification-svc": 0.15,
    }

    def simulate(name: str) -> float:
        base = latency_profiles.get(name, 0.05)
        actual = base * rng.uniform(0.5, 2.0)
        time.sleep(actual)
        return actual

    dependencies = [
        DependencyConfig(name=name, timeout_seconds=0.1, critical=True)
        for name in latency_profiles
    ]

    timeout_values = [0.02, 0.05, 0.1, 0.2, 0.5]
    matrix = build_timeout_matrix(dependencies, timeout_values, simulate_fn=simulate)
    analysis = analyze_matrix(matrix)

    return {
        "matrix": matrix.to_dict(),
        "analysis": analysis,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dependency timeout matrix tester")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    output = run_demo()
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
