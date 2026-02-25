"""Tests for Resilience Chaos Workbench.

Covers fault injection, rollback behavior, experiment execution,
scorecard computation, and resilience grading.
"""
from __future__ import annotations

import pytest

from project import (
    ChaosWorkbench,
    DependencyKill,
    ErrorInjection,
    Experiment,
    FaultType,
    ImpactLevel,
    LatencySpike,
    MemoryPressure,
    ResilienceScore,
    ServiceState,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def healthy_service() -> ServiceState:
    return ServiceState(name="test-svc")


# ---------------------------------------------------------------------------
# Individual fault actions
# ---------------------------------------------------------------------------

class TestLatencySpike:
    def test_apply_increases_latency(self, healthy_service: ServiceState) -> None:
        original = healthy_service.latency_ms
        LatencySpike(200).apply(healthy_service)
        assert healthy_service.latency_ms == original + 200

    def test_rollback_restores_latency(self, healthy_service: ServiceState) -> None:
        original = healthy_service.latency_ms
        spike = LatencySpike(200)
        spike.apply(healthy_service)
        spike.rollback(healthy_service)
        assert healthy_service.latency_ms == original


class TestErrorInjection:
    def test_apply_sets_error_rate(self, healthy_service: ServiceState) -> None:
        ErrorInjection(0.5).apply(healthy_service)
        assert healthy_service.error_rate == 0.5

    def test_error_rate_capped_at_one(self, healthy_service: ServiceState) -> None:
        ErrorInjection(1.5).apply(healthy_service)
        assert healthy_service.error_rate == 1.0


class TestMemoryPressure:
    def test_high_pressure_kills_service(self, healthy_service: ServiceState) -> None:
        MemoryPressure(70.0).apply(healthy_service)
        assert not healthy_service.healthy

    def test_rollback_recovers_service(self, healthy_service: ServiceState) -> None:
        pressure = MemoryPressure(70.0)
        pressure.apply(healthy_service)
        pressure.rollback(healthy_service)
        assert healthy_service.healthy


class TestDependencyKill:
    def test_removes_dependency(self, healthy_service: ServiceState) -> None:
        DependencyKill("db").apply(healthy_service)
        assert "db" not in healthy_service.dependencies_up

    def test_rollback_restores_dependency(self, healthy_service: ServiceState) -> None:
        kill = DependencyKill("cache")
        kill.apply(healthy_service)
        kill.rollback(healthy_service)
        assert "cache" in healthy_service.dependencies_up


# ---------------------------------------------------------------------------
# Experiment runner
# ---------------------------------------------------------------------------

class TestExperiment:
    def test_recoverable_fault_returns_recovered(self, healthy_service: ServiceState) -> None:
        exp = Experiment("test", LatencySpike(100))
        result = exp.run(healthy_service)
        assert result.recovered
        assert result.fault_type == FaultType.LATENCY

    def test_severe_fault_reports_impact(self, healthy_service: ServiceState) -> None:
        exp = Experiment("test", MemoryPressure(80.0))
        result = exp.run(healthy_service)
        assert result.impact != ImpactLevel.NONE


# ---------------------------------------------------------------------------
# Workbench and scorecard
# ---------------------------------------------------------------------------

class TestChaosWorkbench:
    def test_run_all_produces_results(self, healthy_service: ServiceState) -> None:
        wb = ChaosWorkbench(healthy_service)
        wb.add_experiment(Experiment("e1", LatencySpike(100)))
        wb.add_experiment(Experiment("e2", ErrorInjection(0.3)))
        results = wb.run_all()
        assert len(results) == 2

    def test_report_structure(self, healthy_service: ServiceState) -> None:
        wb = ChaosWorkbench(healthy_service)
        wb.add_experiment(Experiment("e1", LatencySpike(100)))
        wb.run_all()
        report = wb.report()
        assert report["service"] == "test-svc"
        assert "grade" in report
        assert "results" in report


class TestResilienceScore:
    @pytest.mark.parametrize("recovered,total,expected_grade", [
        (10, 10, "A"),
        (8, 10, "B"),
        (6, 10, "C"),
        (4, 10, "D"),
        (2, 10, "F"),
    ])
    def test_grading_thresholds(self, recovered: int, total: int, expected_grade: str) -> None:
        score = ResilienceScore(total_experiments=total, recovered=recovered)
        assert score.grade == expected_grade

    def test_empty_score_zero_rate(self) -> None:
        score = ResilienceScore()
        assert score.recovery_rate == 0.0
