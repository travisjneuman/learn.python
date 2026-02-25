"""Tests for Production Readiness Director.

Covers individual checks, director decisions, threshold logic,
and report generation.
"""
from __future__ import annotations

import pytest

from project import (
    Category,
    CheckVerdict,
    HealthCheckCheck,
    LaunchDecision,
    LoggingCheck,
    OnCallCheck,
    ReadinessDirector,
    ReadinessReport,
    SecurityReviewCheck,
    ServiceManifest,
    build_default_director,
)


@pytest.fixture
def ready_manifest() -> ServiceManifest:
    return ServiceManifest(
        name="ready-svc", has_logging=True, has_metrics=True, has_alerts=True,
        has_healthcheck=True, has_runbook=True, has_rollback_plan=True,
        has_load_test=True, has_security_review=True,
        has_on_call=True, test_coverage_pct=90.0,
    )


@pytest.fixture
def unready_manifest() -> ServiceManifest:
    return ServiceManifest(name="unready-svc")


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

class TestIndividualChecks:
    def test_logging_pass(self) -> None:
        m = ServiceManifest(name="svc", has_logging=True)
        assert LoggingCheck().evaluate(m).verdict == CheckVerdict.PASS

    def test_logging_fail(self) -> None:
        m = ServiceManifest(name="svc", has_logging=False)
        assert LoggingCheck().evaluate(m).verdict == CheckVerdict.FAIL

    def test_security_review_required(self) -> None:
        m = ServiceManifest(name="svc", has_security_review=False)
        assert SecurityReviewCheck().evaluate(m).verdict == CheckVerdict.FAIL

    def test_healthcheck_required(self) -> None:
        m = ServiceManifest(name="svc", has_healthcheck=False)
        assert HealthCheckCheck().evaluate(m).verdict == CheckVerdict.FAIL

    def test_oncall_required(self) -> None:
        m = ServiceManifest(name="svc", has_on_call=False)
        assert OnCallCheck().evaluate(m).verdict == CheckVerdict.FAIL


# ---------------------------------------------------------------------------
# Director decisions
# ---------------------------------------------------------------------------

class TestReadinessDirector:
    def test_ready_service_gets_go(self, ready_manifest: ServiceManifest) -> None:
        report = build_default_director().evaluate(ready_manifest)
        assert report.decision == LaunchDecision.GO
        assert report.fail_count == 0

    def test_unready_service_gets_no_go(self, unready_manifest: ServiceManifest) -> None:
        report = build_default_director().evaluate(unready_manifest)
        assert report.decision == LaunchDecision.NO_GO
        assert report.fail_count > 0

    def test_partial_readiness_conditional(self) -> None:
        m = ServiceManifest(
            name="partial", has_logging=True, has_metrics=True,
            has_healthcheck=True, has_security_review=True, has_on_call=True,
            has_alerts=False, has_load_test=False, has_runbook=False,
        )
        report = build_default_director().evaluate(m)
        assert report.decision == LaunchDecision.CONDITIONAL_GO

    def test_custom_thresholds(self, ready_manifest: ServiceManifest) -> None:
        strict_director = ReadinessDirector(fail_threshold=0, warn_threshold=0)
        strict_director.register(LoggingCheck())
        report = strict_director.evaluate(ready_manifest)
        assert report.decision == LaunchDecision.GO


class TestReadinessReport:
    def test_pass_rate_calculation(self, ready_manifest: ServiceManifest) -> None:
        report = build_default_director().evaluate(ready_manifest)
        assert report.pass_rate == 100.0

    def test_summary_structure(self, ready_manifest: ServiceManifest) -> None:
        summary = build_default_director().evaluate(ready_manifest).summary()
        assert "decision" in summary
        assert "categories" in summary
        assert "pass_rate" in summary

    def test_empty_report_zero_pass_rate(self) -> None:
        report = ReadinessReport(service_name="empty")
        assert report.pass_rate == 0.0
