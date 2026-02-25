"""Production Readiness Director — Automated production readiness review checklist.

Architecture: Uses a checklist-driven approach where each ReadinessCheck evaluates
one aspect of production preparedness. Checks are categorized (observability,
reliability, security, operations) and produce pass/fail/warn verdicts. A
ReadinessDirector orchestrates all checks and computes a go/no-go decision based
on configurable thresholds.

Design rationale: Launching a service without checking readiness leads to incidents.
By codifying the readiness review as executable checks, teams get consistent
evaluation and a clear audit trail of what was verified before production.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

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


class LaunchDecision(Enum):
    GO = "go"
    CONDITIONAL_GO = "conditional_go"
    NO_GO = "no_go"


@dataclass(frozen=True)
class CheckResult:
    """Outcome of a single readiness check."""
    check_id: str
    category: Category
    verdict: CheckVerdict
    title: str
    detail: str


@dataclass(frozen=True)
class ServiceManifest:
    """Description of the service being evaluated."""
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


# ---------------------------------------------------------------------------
# Readiness checks (Strategy pattern)
# ---------------------------------------------------------------------------

class ReadinessCheck(Protocol):
    """Protocol for production readiness checks."""
    def check_id(self) -> str: ...
    def category(self) -> Category: ...
    def evaluate(self, manifest: ServiceManifest) -> CheckResult: ...


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


# ---------------------------------------------------------------------------
# Readiness director
# ---------------------------------------------------------------------------

@dataclass
class ReadinessReport:
    """Complete production readiness assessment."""
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
    """Orchestrates readiness checks and produces a go/no-go decision."""

    def __init__(self, fail_threshold: int = 0, warn_threshold: int = 2) -> None:
        self._checks: list[ReadinessCheck] = []
        self._fail_threshold = fail_threshold
        self._warn_threshold = warn_threshold

    def register(self, check: ReadinessCheck) -> None:
        self._checks.append(check)

    @property
    def check_count(self) -> int:
        return len(self._checks)

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
