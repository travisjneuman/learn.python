"""Tests for Dashboard KPI Assembler.

Covers: threshold evaluation, statistical helpers, aggregation, and dashboard assembly.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from project import (
    Dashboard,
    KPIDefinition,
    KPIStatus,
    KPISummary,
    MetricSample,
    aggregate_kpi,
    assemble_dashboard,
    compute_trend,
    dashboard_to_dict,
    load_kpi_definitions,
    load_metric_samples,
    percentile,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def latency_kpi() -> KPIDefinition:
    return KPIDefinition(
        name="response_time_ms", unit="ms",
        green_threshold=200, yellow_threshold=500,
    )


@pytest.fixture
def sample_definitions() -> list[dict]:
    return [
        {"name": "latency", "unit": "ms", "green_threshold": 100, "yellow_threshold": 300},
        {"name": "errors", "unit": "%", "green_threshold": 1, "yellow_threshold": 5},
    ]


@pytest.fixture
def sample_metrics() -> list[MetricSample]:
    return [
        MetricSample("src-a", "latency", "t1", 80),
        MetricSample("src-a", "latency", "t2", 120),
        MetricSample("src-b", "latency", "t3", 90),
        MetricSample("src-a", "errors", "t1", 0.5),
        MetricSample("src-b", "errors", "t2", 0.3),
    ]


# --- Threshold evaluation -----------------------------------------------

class TestKPIEvaluation:
    @pytest.mark.parametrize("value,expected", [
        (50, KPIStatus.GREEN),
        (200, KPIStatus.GREEN),   # boundary — exactly green
        (201, KPIStatus.YELLOW),  # just over green
        (500, KPIStatus.YELLOW),  # boundary — exactly yellow
        (501, KPIStatus.RED),     # just over yellow
        (1000, KPIStatus.RED),
    ])
    def test_evaluate_thresholds(
        self, latency_kpi: KPIDefinition, value: float, expected: KPIStatus,
    ) -> None:
        assert latency_kpi.evaluate(value) == expected


# --- Statistical helpers -------------------------------------------------

class TestPercentile:
    @pytest.mark.parametrize("values,pct,expected", [
        ([10, 20, 30, 40, 50], 50, 30),
        ([10, 20, 30, 40, 50], 95, 50),
        ([100], 99, 100),
    ])
    def test_percentile_values(self, values: list[float], pct: float, expected: float) -> None:
        assert percentile(values, pct) == expected

    def test_empty_list_returns_zero(self) -> None:
        assert percentile([], 50) == 0.0


class TestTrend:
    @pytest.mark.parametrize("values,expected", [
        ([100, 110, 120, 130, 200, 210, 220, 250], "degrading"),
        ([200, 210, 220, 230, 100, 90, 80, 70], "improving"),
        ([100, 102, 98, 101, 100, 99, 101, 100], "stable"),
        ([10, 20], "stable"),  # too few samples
    ])
    def test_trend_detection(self, values: list[float], expected: str) -> None:
        assert compute_trend(values) == expected


# --- Aggregation ---------------------------------------------------------

class TestAggregation:
    def test_aggregate_kpi_computes_correct_stats(
        self, latency_kpi: KPIDefinition,
    ) -> None:
        samples = [
            MetricSample("a", "response_time_ms", "t1", 100),
            MetricSample("a", "response_time_ms", "t2", 150),
            MetricSample("b", "response_time_ms", "t3", 200),
        ]
        summary = aggregate_kpi(latency_kpi, samples)
        assert summary.sample_count == 3
        assert summary.mean == 150.0
        assert summary.minimum == 100.0
        assert summary.maximum == 200.0
        assert summary.status == KPIStatus.GREEN

    def test_aggregate_no_samples_returns_defaults(
        self, latency_kpi: KPIDefinition,
    ) -> None:
        summary = aggregate_kpi(latency_kpi, [])
        assert summary.sample_count == 0
        assert summary.mean == 0.0
        assert summary.status == KPIStatus.GREEN


# --- Dashboard assembly --------------------------------------------------

class TestDashboardAssembly:
    def test_overall_health_critical_when_red_present(self) -> None:
        defs = [
            KPIDefinition("fast", "ms", green_threshold=100, yellow_threshold=200),
            KPIDefinition("slow", "ms", green_threshold=10, yellow_threshold=20),
        ]
        samples = [
            MetricSample("s", "fast", "t", 50),
            MetricSample("s", "slow", "t", 999),  # way over red
        ]
        dashboard = assemble_dashboard("Test", defs, samples)
        assert dashboard.overall_health == "critical"
        assert dashboard.red_count == 1

    def test_serialization_round_trip(self, sample_definitions: list[dict]) -> None:
        defs = load_kpi_definitions(sample_definitions)
        samples = load_metric_samples([
            {"source": "x", "kpi_name": "latency", "timestamp": "t", "value": 80},
            {"source": "x", "kpi_name": "errors", "timestamp": "t", "value": 0.2},
        ])
        dashboard = assemble_dashboard("Round Trip", defs, samples)
        as_dict = dashboard_to_dict(dashboard)
        text = json.dumps(as_dict)
        reloaded = json.loads(text)
        assert reloaded["overall_health"] == "healthy"
        assert len(reloaded["kpis"]) == 2
