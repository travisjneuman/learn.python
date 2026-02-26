# Solution: Level 10 / Project 15 - Level 10 Grand Capstone

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Level 10 Grand Capstone -- Full enterprise platform combining all Level 10 patterns."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol


class Severity(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class Status(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"


# WHY a universal CheckResult shared across subsystems? -- The Facade pattern
# needs a common language. Policy checks, readiness checks, and fitness
# functions all produce pass/fail/warn verdicts. A shared CheckResult lets
# the platform aggregate results into a single dashboard without translating
# between subsystem-specific result types. This is composition at scale.
@dataclass(frozen=True)
class CheckResult:
    subsystem: str
    check_id: str
    status: Status
    severity: Severity
    message: str


# ---------------------------------------------------------------------------
# Subsystem 1: Tenant Manager (from project 04)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Tenant:
    tenant_id: str
    name: str
    plan: str


class TenantManager:
    def __init__(self) -> None:
        self._tenants: dict[str, Tenant] = {}

    def register(self, tenant: Tenant) -> None:
        self._tenants[tenant.tenant_id] = tenant

    def get(self, tenant_id: str) -> Tenant | None:
        return self._tenants.get(tenant_id)

    @property
    def count(self) -> int:
        return len(self._tenants)

    def list_tenants(self) -> list[Tenant]:
        return list(self._tenants.values())


# ---------------------------------------------------------------------------
# Subsystem 2: Policy Engine (from project 03)
# ---------------------------------------------------------------------------

# WHY Protocol for PolicyCheck? -- Each policy rule has unique evaluation
# logic. The Protocol lets teams add governance rules (required fields,
# plan level, naming conventions) without modifying the platform core.
class PolicyCheck(Protocol):
    def check_id(self) -> str: ...
    def evaluate(self, context: dict[str, Any]) -> CheckResult: ...


class RequiredFieldPolicy:
    def __init__(self, field_name: str) -> None:
        self._field = field_name

    def check_id(self) -> str:
        return f"POL-REQ-{self._field}"

    def evaluate(self, context: dict[str, Any]) -> CheckResult:
        if context.get(self._field):
            return CheckResult("policy", self.check_id(), Status.PASS, Severity.INFO, f"'{self._field}' present")
        return CheckResult("policy", self.check_id(), Status.FAIL, Severity.ERROR, f"'{self._field}' missing")


class PlanLevelPolicy:
    def __init__(self, min_plan: str) -> None:
        self._min = min_plan
        self._levels = {"basic": 1, "standard": 2, "enterprise": 3}

    def check_id(self) -> str:
        return f"POL-PLAN-{self._min}"

    def evaluate(self, context: dict[str, Any]) -> CheckResult:
        plan = context.get("plan", "basic")
        if self._levels.get(plan, 0) >= self._levels.get(self._min, 0):
            return CheckResult("policy", self.check_id(), Status.PASS, Severity.INFO, f"Plan '{plan}' meets minimum")
        return CheckResult("policy", self.check_id(), Status.FAIL, Severity.WARNING, f"Plan '{plan}' below '{self._min}'")


# ---------------------------------------------------------------------------
# Subsystem 3: Change Gate (from project 07)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ChangeRequest:
    change_id: str
    title: str
    risk_score: float
    author: str


class ChangeGate:
    def __init__(self, auto_approve_threshold: float = 25.0, block_threshold: float = 75.0) -> None:
        self._auto_threshold = auto_approve_threshold
        self._block_threshold = block_threshold

    def evaluate(self, change: ChangeRequest) -> CheckResult:
        if change.risk_score < self._auto_threshold:
            return CheckResult("change_gate", change.change_id, Status.PASS, Severity.INFO, "Auto-approved")
        if change.risk_score >= self._block_threshold:
            return CheckResult("change_gate", change.change_id, Status.FAIL, Severity.CRITICAL, "Blocked — too risky")
        return CheckResult("change_gate", change.change_id, Status.WARN, Severity.WARNING, "Needs review")


# ---------------------------------------------------------------------------
# Subsystem 4: Readiness Checker (from project 11)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ServiceConfig:
    name: str
    has_monitoring: bool = False
    has_alerting: bool = False
    has_runbook: bool = False
    has_healthcheck: bool = False


class ReadinessChecker:
    def evaluate(self, svc: ServiceConfig) -> list[CheckResult]:
        results: list[CheckResult] = []
        checks = [
            ("monitoring", svc.has_monitoring),
            ("alerting", svc.has_alerting),
            ("runbook", svc.has_runbook),
            ("healthcheck", svc.has_healthcheck),
        ]
        for name, present in checks:
            status = Status.PASS if present else Status.FAIL
            severity = Severity.INFO if present else Severity.ERROR
            results.append(CheckResult("readiness", f"RDY-{name}", status, severity,
                                       f"{name}: {'present' if present else 'missing'}"))
        return results


# ---------------------------------------------------------------------------
# Subsystem 5: Architecture Fitness (from project 09)
# ---------------------------------------------------------------------------

class ArchitectureFitness:
    def __init__(self, max_services: int = 20, max_avg_deps: float = 3.0) -> None:
        self._max_svc = max_services
        self._max_deps = max_avg_deps

    def evaluate(self, service_count: int, avg_deps: float) -> list[CheckResult]:
        results: list[CheckResult] = []
        svc_ok = service_count <= self._max_svc
        results.append(CheckResult("architecture", "ARCH-svc-count",
                                   Status.PASS if svc_ok else Status.WARN, Severity.WARNING,
                                   f"{service_count} services (max {self._max_svc})"))
        dep_ok = avg_deps <= self._max_deps
        results.append(CheckResult("architecture", "ARCH-avg-deps",
                                   Status.PASS if dep_ok else Status.WARN, Severity.WARNING,
                                   f"Avg deps {avg_deps:.1f} (max {self._max_deps})"))
        return results


# ---------------------------------------------------------------------------
# Platform Facade -- composes all subsystems
# ---------------------------------------------------------------------------

@dataclass
class PlatformReport:
    results: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.status == Status.PASS)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.status == Status.FAIL)

    @property
    def warnings(self) -> int:
        return sum(1 for r in self.results if r.status == Status.WARN)

    # WHY percentage-based health score? -- A single number communicates
    # platform health at a glance. Track it over time: rising = improving
    # governance, falling = accumulating gaps.
    @property
    def health_score(self) -> float:
        if not self.results:
            return 0.0
        return (self.passed / len(self.results)) * 100

    # WHY worst-case escalation? -- If ANY check fails, the platform is
    # UNHEALTHY. This prevents a high pass rate from hiding critical
    # individual failures (e.g., 90% healthy but security review missing).
    @property
    def overall_status(self) -> str:
        if self.failed > 0:
            return "UNHEALTHY"
        if self.warnings > 0:
            return "AT_RISK"
        return "HEALTHY"

    def summary(self) -> dict[str, Any]:
        by_subsystem: dict[str, list[dict[str, str]]] = {}
        for r in self.results:
            by_subsystem.setdefault(r.subsystem, []).append({
                "check": r.check_id, "status": r.status.value, "message": r.message,
            })
        return {
            "overall": self.overall_status,
            "health_score": round(self.health_score, 1),
            "total_checks": len(self.results),
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "subsystems": by_subsystem,
        }


# WHY Facade pattern for EnterprisePlatform? -- Each subsystem (tenant,
# policy, change gate, readiness, fitness) has its own API and lifecycle.
# The Facade provides a single `full_assessment` method that orchestrates
# all subsystems and returns a unified report. Callers do not need to know
# which subsystems exist or how to invoke them individually.
class EnterprisePlatform:
    def __init__(self) -> None:
        self.tenant_manager = TenantManager()
        self.policies: list[PolicyCheck] = []
        self.change_gate = ChangeGate()
        self.readiness = ReadinessChecker()
        self.fitness = ArchitectureFitness()

    def add_policy(self, policy: PolicyCheck) -> None:
        self.policies.append(policy)

    def full_assessment(
        self,
        tenant_context: dict[str, Any],
        service: ServiceConfig,
        change: ChangeRequest | None = None,
        service_count: int = 5,
        avg_deps: float = 2.0,
    ) -> PlatformReport:
        report = PlatformReport()

        # Policy checks
        for policy in self.policies:
            report.results.append(policy.evaluate(tenant_context))

        # Readiness checks
        report.results.extend(self.readiness.evaluate(service))

        # Architecture fitness
        report.results.extend(self.fitness.evaluate(service_count, avg_deps))

        # Change gate (optional)
        if change:
            report.results.append(self.change_gate.evaluate(change))

        return report


def main() -> None:
    platform = EnterprisePlatform()

    platform.tenant_manager.register(Tenant("acme", "Acme Corp", "enterprise"))
    platform.tenant_manager.register(Tenant("globex", "Globex Inc", "standard"))

    platform.add_policy(RequiredFieldPolicy("owner"))
    platform.add_policy(RequiredFieldPolicy("cost_center"))
    platform.add_policy(PlanLevelPolicy("standard"))

    report = platform.full_assessment(
        tenant_context={"owner": "platform-team", "cost_center": "CC-100", "plan": "enterprise"},
        service=ServiceConfig("payment-svc", has_monitoring=True, has_alerting=True,
                              has_runbook=True, has_healthcheck=True),
        change=ChangeRequest("CHG-001", "Add payment method", 35.0, "alice"),
        service_count=8,
        avg_deps=2.5,
    )

    print(json.dumps(report.summary(), indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Facade pattern over composed subsystems | Provides a single `full_assessment` entry point; callers do not need to know which subsystems exist | Direct subsystem access -- flexible but burdens callers with orchestration logic and ordering |
| Universal CheckResult across all subsystems | Enables unified aggregation, health scoring, and reporting without subsystem-specific translation layers | Subsystem-specific result types -- more expressive per subsystem but requires adapters to aggregate |
| Protocol-based PolicyCheck interface | Teams add governance rules without modifying the platform; new policies are plug-and-play | Hard-coded policy list -- every new rule requires editing the platform class |
| Worst-case escalation for overall_status | Any single failure makes the platform UNHEALTHY; prevents high pass rates from masking critical gaps | Percentage-based status -- 90% healthy sounds good but may hide a missing security review |
| Subsystem-grouped report breakdown | Teams can see which domain (policy, readiness, architecture, change gate) needs work; focused action items | Flat result list -- harder to identify systematic domain-level gaps |

## Alternative approaches

### Approach B: Event-driven platform with subsystem decoupling

```python
from dataclasses import dataclass, field

@dataclass
class AssessmentEvent:
    subsystem: str
    check_id: str
    status: str
    message: str

class EventBus:
    def __init__(self) -> None:
        self._listeners: list = []
        self._events: list[AssessmentEvent] = []

    def subscribe(self, listener) -> None:
        self._listeners.append(listener)

    def publish(self, event: AssessmentEvent) -> None:
        self._events.append(event)
        for listener in self._listeners:
            listener.on_event(event)

    @property
    def all_events(self) -> list[AssessmentEvent]:
        return list(self._events)
```

**Trade-off:** An event-driven architecture decouples subsystems completely -- each publishes events to a bus, and a report aggregator subscribes. This enables async evaluation, subsystem hot-swapping, and real-time dashboards. However, it adds indirection that makes the flow harder to trace, and introduces eventual consistency concerns. The synchronous Facade is simpler, easier to debug, and sufficient for this scale.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Empty context dict passed to policies | All RequiredFieldPolicy checks fail; report shows UNHEALTHY with multiple policy violations | Validate context has minimum required fields before running assessment |
| High-risk change with unready service | Both change_gate and readiness failures cascade; overall shows UNHEALTHY from multiple subsystems | This is correct behavior -- the platform should flag compound risk |
| No policies registered | Policy section is empty in report; health score may appear artificially high | Add a minimum check count per subsystem; warn if any subsystem contributes zero checks |
