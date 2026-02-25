"""Level 9 Mini-Capstone — Platform Engineering Toolkit.

Design rationale:
    This capstone integrates the core Level 9 concepts: architecture
    decisions, SLO management, cost estimation, reliability scoring,
    and governance checks into a unified platform engineering toolkit.
    It demonstrates how multiple domain engines compose into a
    cohesive operational view.

Concepts practised:
    - facade pattern unifying multiple subsystems
    - dataclasses for rich domain modeling
    - composition over inheritance
    - scoring and grading systems
    - structured reporting with multiple perspectives
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class GovernanceStatus(Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    NEEDS_REVIEW = "needs_review"


class CostTrend(Enum):
    DECREASING = "decreasing"
    STABLE = "stable"
    INCREASING = "increasing"
    SPIKING = "spiking"


# --- SLO subsystem ------------------------------------------------------

@dataclass
class SLODefinition:
    """Service Level Objective definition."""
    name: str
    target: float  # e.g. 99.9 for 99.9%
    current: float = 100.0

    @property
    def budget_remaining_pct(self) -> float:
        """How much error budget remains."""
        total_budget = 100.0 - self.target
        if total_budget <= 0:
            return 0.0
        consumed = 100.0 - self.current
        remaining = max(0, total_budget - consumed)
        return round(remaining / total_budget * 100, 1)

    @property
    def is_met(self) -> bool:
        return self.current >= self.target


# --- Cost subsystem -----------------------------------------------------

@dataclass
class CostEntry:
    """Monthly cost entry for a service."""
    month: str
    amount: float

    def to_dict(self) -> dict[str, Any]:
        return {"month": self.month, "amount": round(self.amount, 2)}


@dataclass
class CostProfile:
    """Cost tracking for a service."""
    budget_monthly: float = 0.0
    entries: list[CostEntry] = field(default_factory=list)

    @property
    def latest_cost(self) -> float:
        return self.entries[-1].amount if self.entries else 0.0

    @property
    def average_cost(self) -> float:
        if not self.entries:
            return 0.0
        return sum(e.amount for e in self.entries) / len(self.entries)

    @property
    def trend(self) -> CostTrend:
        if len(self.entries) < 2:
            return CostTrend.STABLE
        recent = self.entries[-1].amount
        prev = self.entries[-2].amount
        if prev == 0:
            return CostTrend.STABLE
        change_pct = (recent - prev) / prev * 100
        if change_pct > 20:
            return CostTrend.SPIKING
        elif change_pct > 5:
            return CostTrend.INCREASING
        elif change_pct < -5:
            return CostTrend.DECREASING
        return CostTrend.STABLE

    @property
    def over_budget(self) -> bool:
        return self.latest_cost > self.budget_monthly > 0


# --- Reliability subsystem ----------------------------------------------

@dataclass
class ReliabilityMetrics:
    """Reliability metrics for a service."""
    uptime_pct: float = 100.0
    mttr_minutes: float = 0.0  # Mean time to recovery
    incidents_30d: int = 0
    change_failure_rate_pct: float = 0.0

    @property
    def reliability_score(self) -> float:
        """Weighted reliability score (0-100)."""
        score = 0.0
        # Uptime: 40 points
        if self.uptime_pct >= 99.99:
            score += 40
        elif self.uptime_pct >= 99.9:
            score += 35
        elif self.uptime_pct >= 99.5:
            score += 25
        elif self.uptime_pct >= 99.0:
            score += 15
        else:
            score += 5

        # MTTR: 25 points (lower is better)
        if self.mttr_minutes <= 5:
            score += 25
        elif self.mttr_minutes <= 15:
            score += 20
        elif self.mttr_minutes <= 30:
            score += 15
        elif self.mttr_minutes <= 60:
            score += 10
        else:
            score += 5

        # Incidents: 20 points (fewer is better)
        if self.incidents_30d == 0:
            score += 20
        elif self.incidents_30d <= 2:
            score += 15
        elif self.incidents_30d <= 5:
            score += 10
        else:
            score += 5

        # Change failure rate: 15 points
        if self.change_failure_rate_pct <= 5:
            score += 15
        elif self.change_failure_rate_pct <= 15:
            score += 10
        elif self.change_failure_rate_pct <= 30:
            score += 5

        return score


# --- Governance subsystem -----------------------------------------------

@dataclass
class GovernanceCheck:
    """A single governance policy check."""
    name: str
    passed: bool
    message: str = ""


def run_governance_checks(
    service_name: str,
    has_runbook: bool = False,
    has_monitoring: bool = False,
    has_owner: bool = False,
    has_documentation: bool = False,
    has_incident_response: bool = False,
) -> list[GovernanceCheck]:
    """Run standard governance checks for a service."""
    checks: list[GovernanceCheck] = []
    checks.append(GovernanceCheck(
        "runbook", has_runbook,
        "" if has_runbook else f"{service_name} missing operational runbook",
    ))
    checks.append(GovernanceCheck(
        "monitoring", has_monitoring,
        "" if has_monitoring else f"{service_name} missing monitoring configuration",
    ))
    checks.append(GovernanceCheck(
        "ownership", has_owner,
        "" if has_owner else f"{service_name} has no designated owner",
    ))
    checks.append(GovernanceCheck(
        "documentation", has_documentation,
        "" if has_documentation else f"{service_name} lacks documentation",
    ))
    checks.append(GovernanceCheck(
        "incident_response", has_incident_response,
        "" if has_incident_response else f"{service_name} has no incident response plan",
    ))
    return checks


# --- Platform service ---------------------------------------------------

@dataclass
class PlatformService:
    """A service registered in the platform toolkit."""
    name: str
    team: str
    tier: int = 1  # 1 = critical, 2 = important, 3 = best-effort
    slos: list[SLODefinition] = field(default_factory=list)
    cost: CostProfile = field(default_factory=CostProfile)
    reliability: ReliabilityMetrics = field(default_factory=ReliabilityMetrics)
    governance_checks: list[GovernanceCheck] = field(default_factory=list)

    @property
    def health(self) -> HealthStatus:
        """Determine overall health from all subsystems."""
        issues = 0
        # SLO breaches
        if any(not slo.is_met for slo in self.slos):
            issues += 2
        # Low reliability
        if self.reliability.reliability_score < 50:
            issues += 2
        elif self.reliability.reliability_score < 70:
            issues += 1
        # Governance failures
        failed_checks = sum(1 for g in self.governance_checks if not g.passed)
        if failed_checks >= 3:
            issues += 2
        elif failed_checks >= 1:
            issues += 1
        # Cost overrun
        if self.cost.over_budget:
            issues += 1

        if issues >= 4:
            return HealthStatus.CRITICAL
        elif issues >= 2:
            return HealthStatus.DEGRADED
        return HealthStatus.HEALTHY

    @property
    def governance_status(self) -> GovernanceStatus:
        if not self.governance_checks:
            return GovernanceStatus.NEEDS_REVIEW
        failed = sum(1 for g in self.governance_checks if not g.passed)
        if failed == 0:
            return GovernanceStatus.COMPLIANT
        elif failed <= 2:
            return GovernanceStatus.NEEDS_REVIEW
        return GovernanceStatus.NON_COMPLIANT


# --- Platform toolkit (facade) -----------------------------------------

@dataclass
class PlatformReport:
    """Aggregated platform engineering report."""
    total_services: int
    healthy_count: int
    degraded_count: int
    critical_count: int
    slo_breach_count: int
    over_budget_count: int
    governance_compliant_count: int
    total_monthly_cost: float
    avg_reliability_score: float
    service_details: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_services": self.total_services,
            "healthy": self.healthy_count,
            "degraded": self.degraded_count,
            "critical": self.critical_count,
            "slo_breaches": self.slo_breach_count,
            "over_budget": self.over_budget_count,
            "governance_compliant": self.governance_compliant_count,
            "total_monthly_cost": round(self.total_monthly_cost, 2),
            "avg_reliability_score": round(self.avg_reliability_score, 1),
            "services": self.service_details,
        }


class PlatformToolkit:
    """Facade that unifies SLOs, costs, reliability, and governance."""

    def __init__(self) -> None:
        self._services: dict[str, PlatformService] = {}

    def register_service(self, service: PlatformService) -> None:
        self._services[service.name] = service

    def get_service(self, name: str) -> PlatformService | None:
        return self._services.get(name)

    def generate_report(self) -> PlatformReport:
        """Generate a comprehensive platform report."""
        services = list(self._services.values())
        if not services:
            return PlatformReport(0, 0, 0, 0, 0, 0, 0, 0.0, 0.0)

        health_counts = {s: 0 for s in HealthStatus}
        for svc in services:
            health_counts[svc.health] += 1

        slo_breaches = sum(
            1 for svc in services
            if any(not slo.is_met for slo in svc.slos)
        )
        over_budget = sum(1 for svc in services if svc.cost.over_budget)
        compliant = sum(
            1 for svc in services
            if svc.governance_status == GovernanceStatus.COMPLIANT
        )
        total_cost = sum(svc.cost.latest_cost for svc in services)
        avg_reliability = sum(svc.reliability.reliability_score for svc in services) / len(services)

        details = [
            {
                "name": svc.name,
                "team": svc.team,
                "health": svc.health.value,
                "reliability_score": svc.reliability.reliability_score,
                "governance": svc.governance_status.value,
                "monthly_cost": round(svc.cost.latest_cost, 2),
                "slos_met": sum(1 for s in svc.slos if s.is_met),
                "slos_total": len(svc.slos),
            }
            for svc in services
        ]

        return PlatformReport(
            total_services=len(services),
            healthy_count=health_counts[HealthStatus.HEALTHY],
            degraded_count=health_counts[HealthStatus.DEGRADED],
            critical_count=health_counts[HealthStatus.CRITICAL],
            slo_breach_count=slo_breaches,
            over_budget_count=over_budget,
            governance_compliant_count=compliant,
            total_monthly_cost=total_cost,
            avg_reliability_score=avg_reliability,
            service_details=details,
        )


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    toolkit = PlatformToolkit()

    # Healthy service
    api = PlatformService(
        name="api-gateway", team="platform",
        slos=[SLODefinition("availability", 99.9, 99.95)],
        cost=CostProfile(5000, [CostEntry("2024-01", 4200), CostEntry("2024-02", 4500)]),
        reliability=ReliabilityMetrics(99.95, 8, 1, 5),
        governance_checks=run_governance_checks(
            "api-gateway", has_runbook=True, has_monitoring=True,
            has_owner=True, has_documentation=True, has_incident_response=True,
        ),
    )

    # Degraded service
    payments = PlatformService(
        name="payments", team="fintech",
        slos=[SLODefinition("availability", 99.99, 99.8)],  # SLO breach
        cost=CostProfile(3000, [CostEntry("2024-01", 2800), CostEntry("2024-02", 3500)]),
        reliability=ReliabilityMetrics(99.8, 25, 3, 12),
        governance_checks=run_governance_checks(
            "payments", has_runbook=True, has_monitoring=True,
            has_owner=True, has_documentation=False, has_incident_response=False,
        ),
    )

    toolkit.register_service(api)
    toolkit.register_service(payments)

    return toolkit.generate_report().to_dict()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Platform engineering toolkit")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
