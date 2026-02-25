"""Tests for Executive Metrics Publisher.

Covers metric sources, KPI transformation, trend/health computation,
report formatting, and pipeline composition.
"""
from __future__ import annotations

import pytest

from project import (
    ExecutiveSummaryFormatter,
    HealthRating,
    KPI,
    MetricCategory,
    MetricPoint,
    MetricsPublisher,
    QualitySource,
    ReliabilitySource,
    TrendDirection,
    VelocitySource,
    compute_health,
    compute_trend,
    metric_to_kpi,
)


# ---------------------------------------------------------------------------
# Trend computation
# ---------------------------------------------------------------------------

class TestComputeTrend:
    def test_no_previous_is_stable(self) -> None:
        assert compute_trend(100.0, None) == TrendDirection.STABLE

    @pytest.mark.parametrize("current,previous,higher_better,expected", [
        (100.0, 90.0, True, TrendDirection.IMPROVING),
        (90.0, 100.0, True, TrendDirection.DECLINING),
        (5.0, 10.0, False, TrendDirection.IMPROVING),   # lower is better
        (10.0, 5.0, False, TrendDirection.DECLINING),
        (100.0, 99.9, True, TrendDirection.STABLE),      # within 5% threshold
    ])
    def test_trend_directions(self, current: float, previous: float,
                               higher_better: bool, expected: TrendDirection) -> None:
        assert compute_trend(current, previous, higher_better) == expected


# ---------------------------------------------------------------------------
# Health computation
# ---------------------------------------------------------------------------

class TestComputeHealth:
    @pytest.mark.parametrize("value,target,higher_better,expected", [
        (99.95, 99.9, True, HealthRating.GREEN),
        (85.0, 99.9, True, HealthRating.YELLOW),
        (50.0, 99.9, True, HealthRating.RED),
        (1.3, 1.0, False, HealthRating.YELLOW),    # lower is better, 1.3x target
        (0.0, 0.0, False, HealthRating.GREEN),
    ])
    def test_health_ratings(self, value: float, target: float,
                             higher_better: bool, expected: HealthRating) -> None:
        assert compute_health(value, target, higher_better) == expected

    def test_no_target_is_green(self) -> None:
        assert compute_health(50.0, None) == HealthRating.GREEN


# ---------------------------------------------------------------------------
# Metric sources
# ---------------------------------------------------------------------------

class TestReliabilitySource:
    def test_collects_three_metrics(self) -> None:
        source = ReliabilitySource(99.95, 2, 0.5)
        points = source.collect()
        assert len(points) == 3
        assert all(p.category == MetricCategory.RELIABILITY for p in points)


class TestVelocitySource:
    def test_collects_three_metrics(self) -> None:
        points = VelocitySource(8.0, 2.5, 4.0).collect()
        assert len(points) == 3


class TestQualitySource:
    def test_collects_three_metrics(self) -> None:
        points = QualitySource(82.0, 15, 120.0).collect()
        assert len(points) == 3


# ---------------------------------------------------------------------------
# KPI transformation
# ---------------------------------------------------------------------------

class TestMetricToKPI:
    def test_on_target_metric_is_green(self) -> None:
        point = MetricPoint("Uptime", MetricCategory.RELIABILITY, 99.95, "%", 99.9)
        kpi = metric_to_kpi(point)
        assert kpi.health == HealthRating.GREEN
        assert "on track" in kpi.narrative

    def test_below_target_metric_is_red(self) -> None:
        point = MetricPoint("Test Coverage", MetricCategory.QUALITY, 40.0, "%", 80.0)
        kpi = metric_to_kpi(point)
        assert kpi.health == HealthRating.RED
        assert "needs attention" in kpi.narrative

    def test_lower_is_better_handling(self) -> None:
        point = MetricPoint("Incidents", MetricCategory.RELIABILITY, 0, "count", 0)
        kpi = metric_to_kpi(point)
        assert kpi.health == HealthRating.GREEN


# ---------------------------------------------------------------------------
# Publisher and report
# ---------------------------------------------------------------------------

class TestMetricsPublisher:
    def test_publish_produces_report(self) -> None:
        pub = MetricsPublisher()
        pub.add_source(ReliabilitySource(99.95, 2, 0.5))
        report = pub.publish()
        assert report["report_type"] == "executive_summary"
        assert report["kpi_count"] == 3

    def test_full_pipeline(self) -> None:
        pub = MetricsPublisher()
        pub.add_source(ReliabilitySource(99.95, 2, 0.5))
        pub.add_source(VelocitySource(8.0, 2.5, 4.0))
        pub.add_source(QualitySource(82.0, 15, 120.0))
        report = pub.publish()
        assert report["kpi_count"] == 9
        assert "categories" in report


class TestExecutiveSummaryFormatter:
    def test_format_groups_by_category(self) -> None:
        kpis = [
            KPI("Uptime", MetricCategory.RELIABILITY, 99.9, "%"),
            KPI("Deploy Freq", MetricCategory.VELOCITY, 5.0, "per week"),
        ]
        result = ExecutiveSummaryFormatter().format(kpis)
        assert "reliability" in result["categories"]
        assert "velocity" in result["categories"]

    def test_red_kpi_triggers_overall_red(self) -> None:
        kpis = [KPI("Bad Metric", MetricCategory.QUALITY, 0, "%", health=HealthRating.RED)]
        result = ExecutiveSummaryFormatter().format(kpis)
        assert result["overall_health"] == "red"
