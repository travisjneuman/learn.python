"""Tests for Level 8 Mini Capstone — Observability Platform.

Covers: metrics collection, health evaluation, alerting, reporting, and simulation.
"""

from __future__ import annotations

import pytest

from project import (
    Alert,
    ObservabilityPlatform,
    PlatformReport,
    ServiceHealth,
    ServiceMetrics,
    run_simulation,
)


# --- ServiceMetrics -----------------------------------------------------

class TestServiceMetrics:
    def test_error_rate_zero(self) -> None:
        m = ServiceMetrics(name="svc", success_count=100, error_count=0)
        assert m.error_rate == 0.0

    @pytest.mark.parametrize("successes,errors,expected_rate", [
        (90, 10, 0.1),
        (100, 0, 0.0),
        (0, 10, 1.0),
    ])
    def test_error_rate(self, successes: int, errors: int, expected_rate: float) -> None:
        m = ServiceMetrics(name="s", success_count=successes, error_count=errors)
        assert m.error_rate == pytest.approx(expected_rate)

    def test_health_classification(self) -> None:
        healthy = ServiceMetrics(
            name="h", latency_ms=[50, 60, 70], success_count=100, error_count=1,
            uptime_checks=10, uptime_passes=10,
        )
        assert healthy.health() == ServiceHealth.HEALTHY

        degraded = ServiceMetrics(
            name="d", latency_ms=[50, 60, 70], success_count=90, error_count=10,
            uptime_checks=10, uptime_passes=10,
        )
        assert degraded.health() in (ServiceHealth.DEGRADED, ServiceHealth.CRITICAL)

    def test_availability_calculation(self) -> None:
        m = ServiceMetrics(name="s", uptime_checks=100, uptime_passes=99)
        assert m.availability == 99.0

    def test_empty_latency_percentiles(self) -> None:
        m = ServiceMetrics(name="s")
        assert m.p50_latency == 0.0
        assert m.p99_latency == 0.0


# --- ObservabilityPlatform ----------------------------------------------

class TestPlatform:
    def test_record_and_report(self) -> None:
        platform = ObservabilityPlatform(["svc-a", "svc-b"])
        for _ in range(50):
            platform.record_request("svc-a", 100.0, True)
            platform.record_request("svc-b", 200.0, True)
            platform.record_health_check("svc-a", True)
            platform.record_health_check("svc-b", True)

        report = platform.report()
        assert report.overall_health == ServiceHealth.HEALTHY
        assert len(report.services) == 2

    def test_alerting_on_errors(self) -> None:
        platform = ObservabilityPlatform(["bad-svc"])
        for _ in range(100):
            platform.record_request("bad-svc", 100.0, False)  # all errors
            platform.record_health_check("bad-svc", True)
        alerts = platform.evaluate_alerts()
        assert len(alerts) > 0

    def test_unknown_service_ignored(self) -> None:
        platform = ObservabilityPlatform(["known"])
        platform.record_request("unknown", 100.0, True)  # should not crash
        report = platform.report()
        assert len(report.services) == 1


# --- Report serialization -----------------------------------------------

class TestReportSerialization:
    def test_to_dict_structure(self) -> None:
        platform = ObservabilityPlatform(["svc"])
        for _ in range(10):
            platform.record_request("svc", 50.0, True)
            platform.record_health_check("svc", True)
        d = platform.report().to_dict()
        assert "overall_health" in d
        assert "services" in d
        assert "summary" in d
        assert "alerts" in d


# --- Full simulation ----------------------------------------------------

class TestSimulation:
    def test_simulation_deterministic(self) -> None:
        r1 = run_simulation(num_requests=50, seed=42)
        r2 = run_simulation(num_requests=50, seed=42)
        assert r1["overall_health"] == r2["overall_health"]
        assert r1["service_count"] == r2["service_count"]

    def test_simulation_has_services(self) -> None:
        result = run_simulation(num_requests=20, seed=0)
        assert result["service_count"] == 5
        assert len(result["services"]) == 5
