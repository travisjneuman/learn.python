"""Tests for Level 10 Grand Capstone.

Covers individual subsystems, platform composition, report generation,
and end-to-end assessment.
"""
from __future__ import annotations

from typing import Any

import pytest

from project import (
    ArchitectureFitness,
    ChangeGate,
    ChangeRequest,
    EnterprisePlatform,
    PlanLevelPolicy,
    PlatformReport,
    ReadinessChecker,
    RequiredFieldPolicy,
    ServiceConfig,
    Status,
    Tenant,
    TenantManager,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def platform() -> EnterprisePlatform:
    p = EnterprisePlatform()
    p.add_policy(RequiredFieldPolicy("owner"))
    p.add_policy(PlanLevelPolicy("standard"))
    return p


@pytest.fixture
def good_context() -> dict[str, Any]:
    return {"owner": "team-a", "plan": "enterprise"}


@pytest.fixture
def ready_service() -> ServiceConfig:
    return ServiceConfig("svc", has_monitoring=True, has_alerting=True,
                          has_runbook=True, has_healthcheck=True)


# ---------------------------------------------------------------------------
# Tenant manager
# ---------------------------------------------------------------------------

class TestTenantManager:
    def test_register_and_get(self) -> None:
        tm = TenantManager()
        tm.register(Tenant("t1", "Test", "basic"))
        assert tm.get("t1") is not None
        assert tm.count == 1

    def test_unknown_tenant_returns_none(self) -> None:
        assert TenantManager().get("x") is None


# ---------------------------------------------------------------------------
# Policy subsystem
# ---------------------------------------------------------------------------

class TestPolicies:
    def test_required_field_passes(self) -> None:
        result = RequiredFieldPolicy("owner").evaluate({"owner": "alice"})
        assert result.status == Status.PASS

    def test_required_field_fails(self) -> None:
        result = RequiredFieldPolicy("owner").evaluate({})
        assert result.status == Status.FAIL

    @pytest.mark.parametrize("plan,min_plan,expected", [
        ("enterprise", "standard", Status.PASS),
        ("basic", "standard", Status.FAIL),
        ("standard", "standard", Status.PASS),
    ])
    def test_plan_level_policy(self, plan: str, min_plan: str, expected: Status) -> None:
        result = PlanLevelPolicy(min_plan).evaluate({"plan": plan})
        assert result.status == expected


# ---------------------------------------------------------------------------
# Change gate
# ---------------------------------------------------------------------------

class TestChangeGate:
    def test_low_risk_approved(self) -> None:
        result = ChangeGate().evaluate(ChangeRequest("c1", "t", 10.0, "a"))
        assert result.status == Status.PASS

    def test_high_risk_blocked(self) -> None:
        result = ChangeGate().evaluate(ChangeRequest("c1", "t", 80.0, "a"))
        assert result.status == Status.FAIL

    def test_medium_risk_warns(self) -> None:
        result = ChangeGate().evaluate(ChangeRequest("c1", "t", 50.0, "a"))
        assert result.status == Status.WARN


# ---------------------------------------------------------------------------
# Readiness checker
# ---------------------------------------------------------------------------

class TestReadinessChecker:
    def test_fully_ready_all_pass(self, ready_service: ServiceConfig) -> None:
        results = ReadinessChecker().evaluate(ready_service)
        assert all(r.status == Status.PASS for r in results)

    def test_unready_service_has_failures(self) -> None:
        results = ReadinessChecker().evaluate(ServiceConfig("bad"))
        assert any(r.status == Status.FAIL for r in results)


# ---------------------------------------------------------------------------
# Architecture fitness
# ---------------------------------------------------------------------------

class TestArchitectureFitness:
    def test_healthy_architecture(self) -> None:
        results = ArchitectureFitness().evaluate(5, 2.0)
        assert all(r.status == Status.PASS for r in results)

    def test_too_many_services_warns(self) -> None:
        results = ArchitectureFitness(max_services=5).evaluate(10, 2.0)
        svc_result = next(r for r in results if "svc-count" in r.check_id)
        assert svc_result.status == Status.WARN


# ---------------------------------------------------------------------------
# Full platform assessment
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestEnterprisePlatform:
    def test_healthy_assessment(self, platform: EnterprisePlatform,
                                 good_context: dict[str, Any],
                                 ready_service: ServiceConfig) -> None:
        report = platform.full_assessment(good_context, ready_service)
        assert report.overall_status in ("HEALTHY", "AT_RISK")
        assert report.health_score > 50

    def test_unhealthy_assessment(self, platform: EnterprisePlatform) -> None:
        report = platform.full_assessment(
            {}, ServiceConfig("bad"),
            change=ChangeRequest("c1", "t", 90.0, "a"),
        )
        assert report.overall_status == "UNHEALTHY"
        assert report.failed > 0

    def test_report_summary_structure(self, platform: EnterprisePlatform,
                                       good_context: dict[str, Any],
                                       ready_service: ServiceConfig) -> None:
        summary = platform.full_assessment(good_context, ready_service).summary()
        assert "overall" in summary
        assert "subsystems" in summary
        assert "health_score" in summary


class TestPlatformReport:
    def test_empty_report_zero_score(self) -> None:
        assert PlatformReport().health_score == 0.0

    def test_all_passed_is_healthy(self) -> None:
        from project import CheckResult, Severity
        report = PlatformReport(results=[
            CheckResult("test", "T1", Status.PASS, Severity.INFO, "ok"),
        ])
        assert report.overall_status == "HEALTHY"
