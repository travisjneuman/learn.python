# Solution: Level 8 / Project 11 - Synthetic Monitor Runner

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Synthetic Monitor Runner -- run synthetic checks and report health status."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

class CheckStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    SKIP = "skip"

# WHY store check_fn on the dataclass? -- Each health check has different
# logic (HTTP ping, DB query, disk space). Storing the function alongside
# its config keeps the definition self-contained. The runner calls
# check_fn() without knowing what kind of check it is -- Strategy pattern.
@dataclass
class CheckDefinition:
    name: str
    check_fn: Callable[[], CheckResult]
    interval_seconds: float = 60.0
    timeout_seconds: float = 10.0
    critical: bool = True
    tags: list[str] = field(default_factory=list)

@dataclass
class CheckResult:
    name: str
    status: CheckStatus
    latency_ms: float = 0.0
    message: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "status": self.status.value,
                "latency_ms": round(self.latency_ms, 2), "message": self.message}

@dataclass
class MonitorReport:
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
            "total_checks": self.total_checks, "passed": self.passed,
            "failed": self.failed, "warnings": self.warnings,
            "skipped": self.skipped, "overall_healthy": self.overall_healthy,
            "duration_ms": round(self.duration_ms, 2),
            "checks": [r.to_dict() for r in self.results],
        }

# --- Check factories (reusable) ----------------------------------------

# WHY factory functions instead of class inheritance? -- Factory functions
# return a CheckDefinition with a closure as check_fn. This is lighter than
# defining a class per check type. New check types are just new functions.

def http_check(name: str, url: str, expected_status: int = 200) -> CheckDefinition:
    def check_fn() -> CheckResult:
        start = time.perf_counter()
        time.sleep(0.01)  # simulated HTTP call
        elapsed_ms = (time.perf_counter() - start) * 1000
        return CheckResult(name=name, status=CheckStatus.PASS,
                           latency_ms=elapsed_ms,
                           message=f"HTTP {expected_status} from {url}")
    return CheckDefinition(name=name, check_fn=check_fn, tags=["http"])

def threshold_check(name: str, value_fn: Callable[[], float],
                    warn_threshold: float, fail_threshold: float,
                    unit: str = "") -> CheckDefinition:
    def check_fn() -> CheckResult:
        start = time.perf_counter()
        value = value_fn()
        elapsed_ms = (time.perf_counter() - start) * 1000
        if value >= fail_threshold:
            return CheckResult(name=name, status=CheckStatus.FAIL, latency_ms=elapsed_ms,
                               message=f"Value {value}{unit} exceeds fail threshold {fail_threshold}{unit}")
        if value >= warn_threshold:
            return CheckResult(name=name, status=CheckStatus.WARN, latency_ms=elapsed_ms,
                               message=f"Value {value}{unit} exceeds warn threshold {warn_threshold}{unit}")
        return CheckResult(name=name, status=CheckStatus.PASS, latency_ms=elapsed_ms,
                           message=f"Value {value}{unit} within limits")
    return CheckDefinition(name=name, check_fn=check_fn, tags=["threshold"])

def custom_check(name: str, fn: Callable[[], bool], message: str = "") -> CheckDefinition:
    def check_fn() -> CheckResult:
        start = time.perf_counter()
        try:
            passed = fn()
            elapsed_ms = (time.perf_counter() - start) * 1000
            return CheckResult(name=name,
                               status=CheckStatus.PASS if passed else CheckStatus.FAIL,
                               latency_ms=elapsed_ms,
                               message=message or ("Check passed" if passed else "Check failed"))
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000
            return CheckResult(name=name, status=CheckStatus.FAIL,
                               latency_ms=elapsed_ms, message=str(exc))
    return CheckDefinition(name=name, check_fn=check_fn, tags=["custom"])

# --- Monitor runner -----------------------------------------------------

class SyntheticMonitorRunner:
    def __init__(self) -> None:
        self._checks: list[CheckDefinition] = []
        self._history: list[MonitorReport] = []

    def add_check(self, check: CheckDefinition) -> None:
        self._checks.append(check)

    def run_all(self) -> MonitorReport:
        start = time.perf_counter()
        results: list[CheckResult] = []
        for check in self._checks:
            try:
                results.append(check.check_fn())
            except Exception as exc:
                results.append(CheckResult(name=check.name, status=CheckStatus.FAIL,
                                           message=f"Check raised exception: {exc}"))
        elapsed_ms = (time.perf_counter() - start) * 1000
        passed = sum(1 for r in results if r.status == CheckStatus.PASS)
        failed = sum(1 for r in results if r.status == CheckStatus.FAIL)
        warnings = sum(1 for r in results if r.status == CheckStatus.WARN)
        skipped = sum(1 for r in results if r.status == CheckStatus.SKIP)

        # WHY only critical failures affect overall health? -- A warning on
        # memory usage (non-critical) should not page the on-call engineer.
        # Only critical check failures mean the system is unhealthy.
        critical_failed = any(r.status == CheckStatus.FAIL
                              for r, c in zip(results, self._checks) if c.critical)
        report = MonitorReport(
            total_checks=len(results), passed=passed, failed=failed,
            warnings=warnings, skipped=skipped,
            overall_healthy=not critical_failed, results=results, duration_ms=elapsed_ms)
        self._history.append(report)
        return report

    def run_by_tag(self, tag: str) -> MonitorReport:
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

def run_demo() -> dict[str, Any]:
    runner = SyntheticMonitorRunner()
    runner.add_check(http_check("api-health", "https://api.example.com/health"))
    runner.add_check(http_check("web-home", "https://www.example.com/"))
    runner.add_check(threshold_check("cpu-usage", lambda: 65.0, 70, 90, unit="%"))
    runner.add_check(threshold_check("memory-usage", lambda: 82.0, 80, 95, unit="%"))
    runner.add_check(custom_check("disk-space", lambda: True, "Disk space adequate"))
    runner.add_check(custom_check("db-connection", lambda: True, "Database reachable"))
    return runner.run_all().to_dict()

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Synthetic monitor runner")
    parser.add_argument("--demo", action="store_true", default=True)
    parser.parse_args(argv)
    print(json.dumps(run_demo(), indent=2))

if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Factory functions for check types | Lightweight; new check type = new function; no class hierarchy | Abstract base class per check type -- more formal but excessive boilerplate |
| Callable stored on CheckDefinition | Strategy pattern: runner is agnostic to check type | Switch statement on check type -- violates open-closed principle |
| Critical flag for overall health | Non-critical failures (memory warning) should not page on-call | All failures affect health -- causes alert fatigue from non-urgent warnings |
| Tag-based filtering with `run_by_tag` | Run subsets of checks (e.g. only HTTP checks) without creating separate runners | Separate runner per category -- duplicates runner logic |

## Alternative approaches

### Approach B: Async concurrent check execution

```python
import asyncio

class AsyncMonitorRunner:
    async def run_all(self) -> MonitorReport:
        tasks = [asyncio.create_task(self._run_check(c)) for c in self._checks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        # ... build report from results
```

**Trade-off:** Running checks concurrently with asyncio reduces total execution time from O(n * avg_latency) to O(max_latency). Essential for production monitors with dozens of checks, but adds async complexity. The sequential approach is simpler for learning and sufficient when check count is small.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Check function raises an exception | Without try/except in `run_all`, one failing check kills the entire run | Wrap each check in try/except and record a FAIL result |
| `run_by_tag` without restoring original checks | If an exception occurs during tag-filtered run, `self._checks` stays filtered | Use try/finally to always restore the original check list |
| Threshold check with warn > fail | Every value that exceeds warn also exceeds fail; warn is never reported | Validate that `warn_threshold < fail_threshold` at construction time |
