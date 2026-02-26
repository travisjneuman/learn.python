# Solution: Level 10 / Project 11 - Production Readiness Director

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Production Readiness Director -- Automated production readiness review checklist."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol


class Category(Enum):
    OBSERVABILITY = auto()
    RELIABILITY = auto()
    SECURITY = auto()
    OPERATIONS = auto()
    DOCUMENTATION = auto()


class CheckVerdict(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    SKIP = "skip"


# WHY three-level launch decisions? -- Binary go/no-go is too rigid.
# CONDITIONAL_GO says "launch is acceptable with known gaps if the team
# commits to fixing them within a deadline." This matches real-world
# launch reviews where perfect readiness is rare but acceptable risk
# thresholds exist.
class LaunchDecision(Enum):
    GO = "go"
    CONDITIONAL_GO = "conditional_go"
    NO_GO = "no_go"


# WHY frozen=True on CheckResult? -- A check result is a snapshot of what
# was observed. If it could be mutated after evaluation, the audit trail
# would be unreliable. Immutability guarantees the result is exactly what
# the check produced.
@dataclass(frozen=True)
class CheckResult:
    check_id: str
    category: Category
    verdict: CheckVerdict
    title: str
    detail: str


# WHY frozen=True on ServiceManifest? -- The manifest describes the service
# AS IT IS at evaluation time. If fields could change during evaluation,
# different checks might see different states, producing inconsistent results.
@dataclass(frozen=True)
class ServiceManifest:
    name: str
    has_logging: bool = False
    has_metrics: bool = False
    has_alerts: bool = False
    has_healthcheck: bool = False
    has_runbook: bool = False
    has_rollback_plan: bool = False
    has_load_test: bool = False
    has_security_review: bool = False
    has_backup: bool = False
    has_on_call: bool = False
    test_coverage_pct: float = 0.0
    sla_defined: bool = False


class ReadinessCheck(Protocol):
    def check_id(self) -> str: ...
    def category(self) -> Category: ...
    def evaluate(self, manifest: ServiceManifest) -> CheckResult: ...


# WHY separate check classes instead of one big function? -- Each check
# is independently testable, can be enabled/disabled per service, and
# new checks can be added without modifying existing ones. This is the
# Strategy pattern applied to readiness evaluation.
class LoggingCheck:
    def check_id(self) -> str: return "OBS-001"
    def category(self) -> Category: return Category.OBSERVABILITY
    def evaluate(self, m: ServiceManifest) -> CheckResult:
        verdict = CheckVerdict.PASS if m.has_logging else CheckVerdict.FAIL
        return CheckResult(self.check_id(), self.category(), verdict,
                          "Structured logging configured",
                          "Logging enabled" if m.has_logging else "No logging detected")


class MetricsCheck:
    def check_id(self) -> str: return "OBS-002"
    def category(self) -> Category: return Category.OBSERVABILITY
    def evaluate(self, m: ServiceManifest) -> CheckResult:
        verdict = CheckVerdict.PASS if m.has_metrics else CheckVerdict.FAIL
        return CheckResult(self.check_id(), self.category(), verdict,
                          "Metrics instrumentation", "Metrics " + ("present" if m.has_metrics else "missing"))


class AlertsCheck:
    def check_id(self) -> str: return "OBS-003"
    def category(self) -> Category: return Category.OBSERVABILITY
    # WHY WARN instead of FAIL? -- Alerting is important but not a hard
    # blocker. A service can launch without alerts if the team monitors
    # dashboards manually. WARN flags the gap without blocking launch.
    def evaluate(self, m: ServiceManifest) -> CheckResult:
        verdict = CheckVerdict.PASS if m.has_alerts else CheckVerdict.WARN
        return CheckResult(self.check_id(), self.category(), verdict,
                          "Alerting rules defined",
                          "Alerts " + ("configured" if m.has_alerts else "not configured"))


class HealthCheckCheck:
    def check_id(self) -> str: return "REL-001"
    def category(self) -> Category: return Category.RELIABILITY
    def evaluate(self, m: ServiceManifest) -> CheckResult:
        verdict = CheckVerdict.PASS if m.has_healthcheck else CheckVerdict.FAIL
        return CheckResult(self.check_id(), self.category(), verdict,
                          "Health check endpoint",
                          "Health check " + ("present" if m.has_healthcheck else "missing"))


class LoadTestCheck:
    def check_id(self) -> str: return "REL-002"
    def category(self) -> Category: return Category.RELIABILITY
    def evaluate(self, m: ServiceManifest) -> CheckResult:
        verdict = CheckVerdict.PASS if m.has_load_test else CheckVerdict.WARN
        return CheckResult(self.check_id(), self.category(), verdict,
                          "Load testing completed",
                          "Load test " + ("completed" if m.has_load_test else "not run"))


class SecurityReviewCheck:
    def check_id(self) -> str: return "SEC-001"
    def category(self) -> Category: return Category.SECURITY
    def evaluate(self, m: ServiceManifest) -> CheckResult:
        verdict = CheckVerdict.PASS if m.has_security_review else CheckVerdict.FAIL
        return CheckResult(self.check_id(), self.category(), verdict,
                          "Security review completed",
                          "Security review " + ("done" if m.has_security_review else "pending"))


class RunbookCheck:
    def check_id(self) -> str: return "OPS-001"
    def category(self) -> Category: return Category.OPERATIONS
    def evaluate(self, m: ServiceManifest) -> CheckResult:
        verdict = CheckVerdict.PASS if m.has_runbook else CheckVerdict.WARN
        return CheckResult(self.check_id(), self.category(), verdict,
                          "Runbook available",
                          "Runbook " + ("exists" if m.has_runbook else "missing"))


class OnCallCheck:
    def check_id(self) -> str: return "OPS-002"
    def category(self) -> Category: return Category.OPERATIONS
    def evaluate(self, m: ServiceManifest) -> CheckResult:
        verdict = CheckVerdict.PASS if m.has_on_call else CheckVerdict.FAIL
        return CheckResult(self.check_id(), self.category(), verdict,
                          "On-call rotation assigned",
                          "On-call " + ("assigned" if m.has_on_call else "not assigned"))


@dataclass
class ReadinessReport:
    service_name: str
    results: list[CheckResult] = field(default_factory=list)
    decision: LaunchDecision = LaunchDecision.NO_GO

    @property
    def pass_count(self) -> int:
        return sum(1 for r in self.results if r.verdict == CheckVerdict.PASS)

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results if r.verdict == CheckVerdict.FAIL)

    @property
    def warn_count(self) -> int:
        return sum(1 for r in self.results if r.verdict == CheckVerdict.WARN)

    @property
    def pass_rate(self) -> float:
        if not self.results:
            return 0.0
        return self.pass_count / len(self.results) * 100

    def summary(self) -> dict[str, Any]:
        by_cat: dict[str, list[dict[str, str]]] = {}
        for r in self.results:
            cat = r.category.name.lower()
            by_cat.setdefault(cat, []).append({
                "check": r.check_id, "verdict": r.verdict.value, "title": r.title,
            })
        return {
            "service": self.service_name,
            "decision": self.decision.value,
            "pass_rate": f"{self.pass_rate:.0f}%",
            "passed": self.pass_count,
            "failed": self.fail_count,
            "warnings": self.warn_count,
            "categories": by_cat,
        }


class ReadinessDirector:
    # WHY configurable thresholds? -- Different organizations have different
    # risk tolerances. A startup might allow 1 failure for speed; a bank
    # might require zero. Thresholds make the decision logic adaptable
    # without changing the check implementations.
    def __init__(self, fail_threshold: int = 0, warn_threshold: int = 2) -> None:
        self._checks: list[ReadinessCheck] = []
        self._fail_threshold = fail_threshold
        self._warn_threshold = warn_threshold

    def register(self, check: ReadinessCheck) -> None:
        self._checks.append(check)

    @property
    def check_count(self) -> int:
        return len(self._checks)

    # WHY fail_count > threshold, not >=? -- A threshold of 0 means
    # "zero failures allowed." Using > 0 means any failure triggers NO_GO.
    # Using >= 0 would mean even zero failures triggers NO_GO, which is wrong.
    def evaluate(self, manifest: ServiceManifest) -> ReadinessReport:
        report = ReadinessReport(service_name=manifest.name)
        for check in self._checks:
            result = check.evaluate(manifest)
            report.results.append(result)

        if report.fail_count > self._fail_threshold:
            report.decision = LaunchDecision.NO_GO
        elif report.warn_count > self._warn_threshold:
            report.decision = LaunchDecision.CONDITIONAL_GO
        else:
            report.decision = LaunchDecision.GO
        return report


def build_default_director() -> ReadinessDirector:
    director = ReadinessDirector()
    for check_cls in [LoggingCheck, MetricsCheck, AlertsCheck, HealthCheckCheck,
                      LoadTestCheck, SecurityReviewCheck, RunbookCheck, OnCallCheck]:
        director.register(check_cls())
    return director


def main() -> None:
    manifest = ServiceManifest(
        name="payment-service",
        has_logging=True, has_metrics=True, has_alerts=True,
        has_healthcheck=True, has_runbook=True, has_rollback_plan=True,
        has_load_test=False, has_security_review=True,
        has_backup=True, has_on_call=True, test_coverage_pct=82.0, sla_defined=True,
    )
    director = build_default_director()
    report = director.evaluate(manifest)
    print(json.dumps(report.summary(), indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Strategy pattern for individual checks | Each check is independently testable and can be toggled per service; new checks added without modifying the director | Single large function with if/elif branches -- hard to test and extend |
| Three-tier decision (GO/CONDITIONAL/NO_GO) | Matches real launch reviews where perfect readiness is rare but acceptable risk exists | Binary go/no-go -- too rigid for real-world operations |
| Frozen ServiceManifest | Ensures all checks see the same service state; prevents inconsistent results from mid-evaluation mutation | Mutable manifest with defensive copies -- more error-prone |
| Configurable thresholds | Different organizations tolerate different risk levels; a startup and a bank have different standards | Hard-coded thresholds -- forces everyone into the same risk model |
| Category-grouped results | Lets teams see which domain (observability, security, operations) needs the most work | Flat list of results -- harder to identify systematic gaps |

## Alternative approaches

### Approach B: Weighted scoring with category multipliers

```python
CATEGORY_WEIGHTS = {
    Category.SECURITY: 3.0,      # Security failures count triple
    Category.RELIABILITY: 2.0,   # Reliability failures count double
    Category.OBSERVABILITY: 1.5,
    Category.OPERATIONS: 1.0,
}

def weighted_decision(results: list[CheckResult]) -> LaunchDecision:
    weighted_fails = sum(
        CATEGORY_WEIGHTS.get(r.category, 1.0)
        for r in results if r.verdict == CheckVerdict.FAIL
    )
    if weighted_fails >= 6.0: return LaunchDecision.NO_GO
    if weighted_fails >= 3.0: return LaunchDecision.CONDITIONAL_GO
    return LaunchDecision.GO
```

**Trade-off:** Weighted scoring lets security failures automatically block launch regardless of pass rate, which is more realistic. However, it is harder to explain to teams why the same number of failures produces different decisions in different categories. The simple threshold approach is more transparent.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| All manifest fields set to False | Every check fails or warns; report shows NO_GO with 0% pass rate | Add a "minimum viable service" validation before running checks |
| No checks registered | `evaluate` produces an empty report with NO_GO (0 fails > 0 threshold is False, so it falls through to GO) | Add a minimum check count guard that requires at least 3 checks |
| Thresholds set too permissively (fail_threshold=99) | Every service auto-approves regardless of failures | Validate thresholds at construction time; warn if fail_threshold exceeds check_count |
