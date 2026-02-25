"""Tests for Strategic Architecture Review.

Covers fitness functions, review engine, report generation,
health scoring, and recommendation logic.
"""
from __future__ import annotations

import pytest

from project import (
    ArchitectureReport,
    ComplexityCheck,
    CouplingCheck,
    DependencyDepthCheck,
    HealthStatus,
    QualityAttribute,
    ReviewEngine,
    ServiceDef,
    SystemModel,
    TestCoverageCheck,
    build_default_engine,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def healthy_system() -> SystemModel:
    sys = SystemModel("healthy")
    sys.add_service(ServiceDef("api", ["db"], 1000, 90.0))
    sys.add_service(ServiceDef("db", [], 500, 85.0))
    return sys


@pytest.fixture
def unhealthy_system() -> SystemModel:
    sys = SystemModel("unhealthy")
    sys.add_service(ServiceDef("monolith", ["a", "b", "c", "d", "e"], 10000, 30.0))
    sys.add_service(ServiceDef("a", ["b"], 200, 50.0))
    sys.add_service(ServiceDef("b", ["c"], 200, 50.0))
    sys.add_service(ServiceDef("c", ["d"], 200, 50.0))
    sys.add_service(ServiceDef("d", ["e"], 200, 50.0))
    sys.add_service(ServiceDef("e", [], 200, 50.0))
    return sys


# ---------------------------------------------------------------------------
# Individual fitness functions
# ---------------------------------------------------------------------------

class TestCouplingCheck:
    def test_low_coupling_passes(self, healthy_system: SystemModel) -> None:
        result = CouplingCheck(max_avg_deps=3.0).evaluate(healthy_system)
        assert result.passed

    def test_high_coupling_fails(self, unhealthy_system: SystemModel) -> None:
        result = CouplingCheck(max_avg_deps=1.0).evaluate(unhealthy_system)
        assert not result.passed

    def test_generates_recommendation_on_failure(self, unhealthy_system: SystemModel) -> None:
        check = CouplingCheck(max_avg_deps=0.5)
        result = check.evaluate(unhealthy_system)
        rec = check.recommend(result)
        assert rec is not None
        assert rec.attribute == QualityAttribute.COUPLING


class TestComplexityCheck:
    def test_small_services_pass(self, healthy_system: SystemModel) -> None:
        assert ComplexityCheck(max_loc=5000).evaluate(healthy_system).passed

    def test_large_service_fails(self, unhealthy_system: SystemModel) -> None:
        assert not ComplexityCheck(max_loc=5000).evaluate(unhealthy_system).passed


class TestCoverageChecker:
    def test_good_coverage_passes(self, healthy_system: SystemModel) -> None:
        assert TestCoverageCheck(min_coverage=70.0).evaluate(healthy_system).passed

    def test_low_coverage_fails(self, unhealthy_system: SystemModel) -> None:
        assert not TestCoverageCheck(min_coverage=70.0).evaluate(unhealthy_system).passed


class TestDependencyDepthCheck:
    def test_shallow_passes(self, healthy_system: SystemModel) -> None:
        assert DependencyDepthCheck(max_depth=4).evaluate(healthy_system).passed

    def test_deep_chain_fails(self, unhealthy_system: SystemModel) -> None:
        assert not DependencyDepthCheck(max_depth=3).evaluate(unhealthy_system).passed


# ---------------------------------------------------------------------------
# Review engine and report
# ---------------------------------------------------------------------------

class TestReviewEngine:
    def test_review_produces_report(self, healthy_system: SystemModel) -> None:
        engine = build_default_engine()
        report = engine.review(healthy_system)
        assert report.system_name == "healthy"
        assert len(report.results) == 4

    def test_healthy_system_high_score(self, healthy_system: SystemModel) -> None:
        report = build_default_engine().review(healthy_system)
        assert report.health_score >= 75.0
        assert report.overall_status in (HealthStatus.HEALTHY, HealthStatus.WARNING)

    def test_unhealthy_system_generates_recommendations(self, unhealthy_system: SystemModel) -> None:
        report = build_default_engine().review(unhealthy_system)
        assert len(report.recommendations) > 0

    def test_report_summary_structure(self, healthy_system: SystemModel) -> None:
        report = build_default_engine().review(healthy_system)
        summary = report.summary()
        assert "health_score" in summary
        assert "status" in summary
        assert "recommendations" in summary
