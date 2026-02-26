"""Synthetic Monitor Runner — run synthetic checks and report health status.

Design rationale:
    Synthetic monitoring proactively detects outages by running scripted
    checks against your system at regular intervals. This project builds
    a monitor runner that executes health checks, evaluates pass/fail
    criteria, and generates status reports — the same pattern used by
    Pingdom, UptimeRobot, and custom health-check frameworks.

Concepts practised:
    - callable-based check definitions
    - dataclasses for check results and reports
    - threshold-based health evaluation
    - scheduled execution patterns
    - structured reporting with history
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

class CheckStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    SKIP = "skip"


# WHY store check_fn as a callable on the dataclass? -- Each health check
# has different logic (HTTP ping, DB query, disk space). Storing the check
# function alongside its config (interval, timeout, critical) keeps the
# definition self-contained. The runner just calls check_fn() without
# knowing what kind of check it is — the Strategy pattern in action.
@dataclass
class CheckDefinition:
    """Definition of a synthetic health check."""
    name: str
    check_fn: Callable[[], CheckResult]
    interval_seconds: float = 60.0
    timeout_seconds: float = 10.0
    critical: bool = True
    tags: list[str] = field(default_factory=list)


@dataclass
class CheckResult:
    """Result of a single check execution."""
    name: str
    status: CheckStatus
    latency_ms: float = 0.0
    message: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status.value,
            "latency_ms": round(self.latency_ms, 2),
            "message": self.message,
        }


@dataclass
class MonitorReport:
    """Aggregated report from a monitoring run."""
    total_checks: int
    passed: int
    failed: int
    warnings: int
    skipped: int
    overall_healthy: bool
    results: list[CheckResult]
    duration_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_checks": self.total_checks,
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "skipped": self.skipped,
            "overall_healthy": self.overall_healthy,
            "duration_ms": round(self.duration_ms, 2),
            "checks": [r.to_dict() for r in self.results],
        }


# --- Check library (reusable check factories) --------------------------

def http_check(name: str, url: str, expected_status: int = 200) -> CheckDefinition:
    """Create a check that simulates an HTTP endpoint test."""
    def check_fn() -> CheckResult:
        start = time.perf_counter()
        # Simulate HTTP call based on URL patterns
        latency = 0.01  # simulated
        time.sleep(latency)
        elapsed_ms = (time.perf_counter() - start) * 1000
        return CheckResult(
            name=name, status=CheckStatus.PASS,
            latency_ms=elapsed_ms,
            message=f"HTTP {expected_status} from {url}",
        )
    return CheckDefinition(name=name, check_fn=check_fn, tags=["http"])


def threshold_check(
    name: str,
    value_fn: Callable[[], float],
    warn_threshold: float,
    fail_threshold: float,
    unit: str = "",
) -> CheckDefinition:
    """Create a check that evaluates a metric against thresholds."""
    def check_fn() -> CheckResult:
        start = time.perf_counter()
        value = value_fn()
        elapsed_ms = (time.perf_counter() - start) * 1000
        if value >= fail_threshold:
            return CheckResult(
                name=name, status=CheckStatus.FAIL,
                latency_ms=elapsed_ms,
                message=f"Value {value}{unit} exceeds fail threshold {fail_threshold}{unit}",
            )
        if value >= warn_threshold:
            return CheckResult(
                name=name, status=CheckStatus.WARN,
                latency_ms=elapsed_ms,
                message=f"Value {value}{unit} exceeds warn threshold {warn_threshold}{unit}",
            )
        return CheckResult(
            name=name, status=CheckStatus.PASS,
            latency_ms=elapsed_ms,
            message=f"Value {value}{unit} within limits",
        )
    return CheckDefinition(name=name, check_fn=check_fn, tags=["threshold"])


def custom_check(name: str, fn: Callable[[], bool], message: str = "") -> CheckDefinition:
    """Create a simple pass/fail check from a boolean function."""
    def check_fn() -> CheckResult:
        start = time.perf_counter()
        try:
            passed = fn()
            elapsed_ms = (time.perf_counter() - start) * 1000
            return CheckResult(
                name=name,
                status=CheckStatus.PASS if passed else CheckStatus.FAIL,
                latency_ms=elapsed_ms,
                message=message or ("Check passed" if passed else "Check failed"),
            )
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000
            return CheckResult(
                name=name, status=CheckStatus.FAIL,
                latency_ms=elapsed_ms, message=str(exc),
            )
    return CheckDefinition(name=name, check_fn=check_fn, tags=["custom"])


# --- Monitor runner -----------------------------------------------------

class SyntheticMonitorRunner:
    """Executes synthetic health checks and produces reports."""

    def __init__(self) -> None:
        self._checks: list[CheckDefinition] = []
        self._history: list[MonitorReport] = []

    def add_check(self, check: CheckDefinition) -> None:
        """Register a check to run."""
        self._checks.append(check)

    def run_all(self) -> MonitorReport:
        """Execute all registered checks and build a report."""
        start = time.perf_counter()
        results: list[CheckResult] = []

        for check in self._checks:
            try:
                result = check.check_fn()
                results.append(result)
            except Exception as exc:
                results.append(CheckResult(
                    name=check.name, status=CheckStatus.FAIL,
                    message=f"Check raised exception: {exc}",
                ))

        elapsed_ms = (time.perf_counter() - start) * 1000
        passed = sum(1 for r in results if r.status == CheckStatus.PASS)
        failed = sum(1 for r in results if r.status == CheckStatus.FAIL)
        warnings = sum(1 for r in results if r.status == CheckStatus.WARN)
        skipped = sum(1 for r in results if r.status == CheckStatus.SKIP)

        # System is healthy if no critical checks failed
        critical_failed = any(
            r.status == CheckStatus.FAIL
            for r, c in zip(results, self._checks)
            if c.critical
        )

        report = MonitorReport(
            total_checks=len(results),
            passed=passed,
            failed=failed,
            warnings=warnings,
            skipped=skipped,
            overall_healthy=not critical_failed,
            results=results,
            duration_ms=elapsed_ms,
        )
        self._history.append(report)
        return report

    def run_by_tag(self, tag: str) -> MonitorReport:
        """Run only checks matching a specific tag."""
        original = self._checks
        self._checks = [c for c in original if tag in c.tags]
        try:
            return self.run_all()
        finally:
            self._checks = original

    @property
    def history(self) -> list[MonitorReport]:
        return list(self._history)

    @property
    def check_count(self) -> int:
        return len(self._checks)


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    """Demonstrate synthetic monitoring with various check types."""
    runner = SyntheticMonitorRunner()

    runner.add_check(http_check("api-health", "https://api.example.com/health"))
    runner.add_check(http_check("web-home", "https://www.example.com/"))
    runner.add_check(threshold_check(
        "cpu-usage", lambda: 65.0, warn_threshold=70, fail_threshold=90, unit="%",
    ))
    runner.add_check(threshold_check(
        "memory-usage", lambda: 82.0, warn_threshold=80, fail_threshold=95, unit="%",
    ))
    runner.add_check(custom_check(
        "disk-space", lambda: True, "Disk space adequate",
    ))
    runner.add_check(custom_check(
        "db-connection", lambda: True, "Database reachable",
    ))

    report = runner.run_all()
    return report.to_dict()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synthetic monitor runner")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    output = run_demo()
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
