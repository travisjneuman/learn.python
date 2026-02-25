"""Tests for Level 9 Mini-Capstone — Platform Engineering Toolkit.

Covers: SLO budgets, cost tracking, reliability scoring, governance checks,
health determination, and platform reporting.
"""

from __future__ import annotations

import pytest

from project import (
    CostEntry,
    CostProfile,
    CostTrend,
    GovernanceStatus,
    HealthStatus,
    PlatformReport,
    PlatformService,
    PlatformToolkit,
    ReliabilityMetrics,
    SLODefinition,
    run_governance_checks,
)


# --- SLO subsystem ------------------------------------------------------

class TestSLO:
    def test_slo_met(self) -> None:
        slo = SLODefinition("avail", 99.9, 99.95)
        assert slo.is_met is True

    def test_slo_breached(self) -> None:
        slo = SLODefinition("avail", 99.9, 99.5)
        assert slo.is_met is False

    @pytest.mark.parametrize("target,current,min_budget", [
        (99.9, 99.95, 40),
        (99.0, 99.0, 0),
        (99.0, 100.0, 90),
    ])
    def test_budget_remaining(self, target: float, current: float, min_budget: float) -> None:
        slo = SLODefinition("slo", target, current)
        assert slo.budget_remaining_pct >= min_budget


# --- Cost subsystem -----------------------------------------------------

class TestCost:
    def test_latest_cost(self) -> None:
        profile = CostProfile(entries=[CostEntry("jan", 100), CostEntry("feb", 150)])
        assert profile.latest_cost == 150

    def test_average_cost(self) -> None:
        profile = CostProfile(entries=[CostEntry("jan", 100), CostEntry("feb", 200)])
        assert profile.average_cost == pytest.approx(150.0)

    def test_over_budget(self) -> None:
        profile = CostProfile(budget_monthly=100, entries=[CostEntry("jan", 150)])
        assert profile.over_budget is True

    def test_under_budget(self) -> None:
        profile = CostProfile(budget_monthly=200, entries=[CostEntry("jan", 150)])
        assert profile.over_budget is False

    @pytest.mark.parametrize("amounts,expected_trend", [
        ([100, 150], CostTrend.SPIKING),
        ([100, 103], CostTrend.STABLE),
        ([100, 80], CostTrend.DECREASING),
    ])
    def test_cost_trend(self, amounts: list[float], expected_trend: CostTrend) -> None:
        entries = [CostEntry(f"m{i}", a) for i, a in enumerate(amounts)]
        profile = CostProfile(entries=entries)
        assert profile.trend == expected_trend


# --- Reliability subsystem -----------------------------------------------

class TestReliability:
    def test_perfect_reliability(self) -> None:
        m = ReliabilityMetrics(uptime_pct=99.99, mttr_minutes=3, incidents_30d=0, change_failure_rate_pct=2)
        assert m.reliability_score == 100

    def test_poor_reliability(self) -> None:
        m = ReliabilityMetrics(uptime_pct=95.0, mttr_minutes=120, incidents_30d=10, change_failure_rate_pct=50)
        assert m.reliability_score < 30

    def test_score_between_0_and_100(self) -> None:
        m = ReliabilityMetrics(uptime_pct=99.5, mttr_minutes=20, incidents_30d=3, change_failure_rate_pct=10)
        assert 0 <= m.reliability_score <= 100


# --- Governance subsystem ------------------------------------------------

class TestGovernance:
    def test_all_checks_pass(self) -> None:
        checks = run_governance_checks(
            "svc", has_runbook=True, has_monitoring=True,
            has_owner=True, has_documentation=True, has_incident_response=True,
        )
        assert all(c.passed for c in checks)

    def test_no_checks_pass(self) -> None:
        checks = run_governance_checks("svc")
        assert all(not c.passed for c in checks)
        assert all(c.message for c in checks)

    def test_check_count(self) -> None:
        checks = run_governance_checks("svc")
        assert len(checks) == 5


# --- Health determination ------------------------------------------------

class TestHealth:
    def test_healthy_service(self) -> None:
        svc = PlatformService(
            name="ok", team="t",
            slos=[SLODefinition("a", 99.9, 99.95)],
            reliability=ReliabilityMetrics(99.9, 10, 1, 5),
            governance_checks=run_governance_checks(
                "ok", has_runbook=True, has_monitoring=True,
                has_owner=True, has_documentation=True, has_incident_response=True,
            ),
        )
        assert svc.health == HealthStatus.HEALTHY

    def test_critical_service(self) -> None:
        svc = PlatformService(
            name="bad", team="t",
            slos=[SLODefinition("a", 99.9, 98.0)],
            reliability=ReliabilityMetrics(95.0, 120, 10, 50),
            governance_checks=run_governance_checks("bad"),
        )
        assert svc.health == HealthStatus.CRITICAL

    def test_governance_status_compliant(self) -> None:
        svc = PlatformService(
            name="ok", team="t",
            governance_checks=run_governance_checks(
                "ok", has_runbook=True, has_monitoring=True,
                has_owner=True, has_documentation=True, has_incident_response=True,
            ),
        )
        assert svc.governance_status == GovernanceStatus.COMPLIANT

    def test_governance_status_non_compliant(self) -> None:
        svc = PlatformService(name="bad", team="t", governance_checks=run_governance_checks("bad"))
        assert svc.governance_status == GovernanceStatus.NON_COMPLIANT


# --- Platform report -----------------------------------------------------

class TestPlatformReport:
    def test_empty_toolkit(self) -> None:
        toolkit = PlatformToolkit()
        report = toolkit.generate_report()
        assert report.total_services == 0

    def test_report_counts(self) -> None:
        toolkit = PlatformToolkit()
        toolkit.register_service(PlatformService(
            name="healthy", team="t",
            reliability=ReliabilityMetrics(99.9, 5, 0, 2),
        ))
        toolkit.register_service(PlatformService(
            name="unhealthy", team="t",
            slos=[SLODefinition("a", 99.9, 98.0)],
            reliability=ReliabilityMetrics(95.0, 120, 10, 50),
            governance_checks=run_governance_checks("bad"),
        ))
        report = toolkit.generate_report()
        assert report.total_services == 2
        assert report.healthy_count + report.degraded_count + report.critical_count == 2

    def test_report_serialization(self) -> None:
        toolkit = PlatformToolkit()
        toolkit.register_service(PlatformService(
            name="svc", team="t",
            cost=CostProfile(entries=[CostEntry("jan", 500)]),
        ))
        d = toolkit.generate_report().to_dict()
        assert "total_services" in d
        assert "services" in d
        assert d["total_monthly_cost"] == 500.0
