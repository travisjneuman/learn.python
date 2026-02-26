"""Executive Metrics Publisher — Transform technical metrics into executive-friendly reports.

Architecture: Uses the Adapter pattern to normalize metrics from different sources
into a common MetricPoint format. A MetricsPipeline chains transformations:
collect -> normalize -> aggregate -> format. Different output formatters
(executive summary, detailed breakdown, trend analysis) implement a Formatter
protocol for pluggable report styles.

Design rationale: Engineering teams track hundreds of metrics, but executives need
concise answers: "Are we on track?" "Where are we at risk?" This pipeline bridges
that gap by aggregating technical data into business-meaningful KPIs with trend
indicators and health ratings.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class MetricCategory(Enum):
    RELIABILITY = auto()
    PERFORMANCE = auto()
    VELOCITY = auto()
    QUALITY = auto()
    COST = auto()


class TrendDirection(Enum):
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"


class HealthRating(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


# WHY normalize into MetricPoint? -- Engineering metrics come from many
# sources in different formats. Normalizing into a common shape lets the
# pipeline aggregate across sources (Adapter pattern). The frozen=True
# ensures metric points are immutable once collected — audit-friendly
# and safe for concurrent processing.
@dataclass(frozen=True)
class MetricPoint:
    """Normalized metric data point."""
    name: str
    category: MetricCategory
    value: float
    unit: str
    target: float | None = None
    previous: float | None = None


@dataclass
class KPI:
    """Executive-facing Key Performance Indicator."""
    name: str
    category: MetricCategory
    value: float
    unit: str
    target: float | None = None
    trend: TrendDirection = TrendDirection.STABLE
    health: HealthRating = HealthRating.GREEN
    narrative: str = ""


# ---------------------------------------------------------------------------
# Metric sources (Adapter pattern)
# ---------------------------------------------------------------------------

class MetricSource(Protocol):
    """Adapter interface for collecting metrics from different systems."""
    def source_name(self) -> str: ...
    def collect(self) -> list[MetricPoint]: ...


class ReliabilitySource:
    """Collects uptime and incident metrics."""
    def __init__(self, uptime_pct: float, incidents: int, mttr_hours: float,
                 prev_uptime: float = 99.9, prev_incidents: int = 0) -> None:
        self._uptime = uptime_pct
        self._incidents = incidents
        self._mttr = mttr_hours
        self._prev_uptime = prev_uptime
        self._prev_incidents = prev_incidents

    def source_name(self) -> str:
        return "reliability"

    def collect(self) -> list[MetricPoint]:
        return [
            MetricPoint("Uptime", MetricCategory.RELIABILITY, self._uptime, "%", 99.9, self._prev_uptime),
            MetricPoint("Incidents", MetricCategory.RELIABILITY, self._incidents, "count", 0, self._prev_incidents),
            MetricPoint("MTTR", MetricCategory.RELIABILITY, self._mttr, "hours", 1.0),
        ]


class VelocitySource:
    """Collects delivery velocity metrics."""
    def __init__(self, deploy_freq: float, lead_time_days: float, change_fail_pct: float,
                 prev_freq: float = 0, prev_lead: float = 0) -> None:
        self._deploy_freq = deploy_freq
        self._lead_time = lead_time_days
        self._change_fail = change_fail_pct
        self._prev_freq = prev_freq
        self._prev_lead = prev_lead

    def source_name(self) -> str:
        return "velocity"

    def collect(self) -> list[MetricPoint]:
        return [
            MetricPoint("Deploy Frequency", MetricCategory.VELOCITY, self._deploy_freq,
                         "per week", 5.0, self._prev_freq),
            MetricPoint("Lead Time", MetricCategory.VELOCITY, self._lead_time, "days", 3.0, self._prev_lead),
            MetricPoint("Change Failure Rate", MetricCategory.VELOCITY, self._change_fail, "%", 5.0),
        ]


class QualitySource:
    """Collects code quality metrics."""
    def __init__(self, test_coverage: float, bug_count: int, tech_debt_hours: float) -> None:
        self._coverage = test_coverage
        self._bugs = bug_count
        self._debt = tech_debt_hours

    def source_name(self) -> str:
        return "quality"

    def collect(self) -> list[MetricPoint]:
        return [
            MetricPoint("Test Coverage", MetricCategory.QUALITY, self._coverage, "%", 80.0),
            MetricPoint("Open Bugs", MetricCategory.QUALITY, self._bugs, "count", 10),
            MetricPoint("Tech Debt", MetricCategory.QUALITY, self._debt, "hours", 100.0),
        ]


# ---------------------------------------------------------------------------
# Transformation pipeline
# ---------------------------------------------------------------------------

def compute_trend(current: float, previous: float | None, higher_is_better: bool = True) -> TrendDirection:
    """Determine trend based on current vs previous value."""
    if previous is None:
        return TrendDirection.STABLE
    delta = current - previous
    threshold = abs(previous) * 0.05 if previous != 0 else 1.0
    if abs(delta) < threshold:
        return TrendDirection.STABLE
    improving = delta > 0 if higher_is_better else delta < 0
    return TrendDirection.IMPROVING if improving else TrendDirection.DECLINING


def compute_health(value: float, target: float | None, higher_is_better: bool = True) -> HealthRating:
    """Determine health rating based on target proximity."""
    if target is None:
        return HealthRating.GREEN
    if higher_is_better:
        ratio = value / target if target > 0 else 1.0
        if ratio >= 0.95:
            return HealthRating.GREEN
        if ratio >= 0.80:
            return HealthRating.YELLOW
        return HealthRating.RED
    else:
        # Lower is better (e.g., incidents, lead time)
        if target == 0:
            return HealthRating.GREEN if value == 0 else HealthRating.YELLOW
        ratio = value / target
        if ratio <= 1.05:
            return HealthRating.GREEN
        if ratio <= 1.5:
            return HealthRating.YELLOW
        return HealthRating.RED


# Metrics where lower values are better
LOWER_IS_BETTER = {"Incidents", "MTTR", "Lead Time", "Change Failure Rate", "Open Bugs", "Tech Debt"}


def metric_to_kpi(point: MetricPoint) -> KPI:
    """Transform a raw metric into an executive KPI."""
    higher_is_better = point.name not in LOWER_IS_BETTER
    trend = compute_trend(point.value, point.previous, higher_is_better)
    health = compute_health(point.value, point.target, higher_is_better)

    if health == HealthRating.RED:
        narrative = f"{point.name} is below target — needs attention."
    elif health == HealthRating.YELLOW:
        narrative = f"{point.name} is near target — monitor closely."
    else:
        narrative = f"{point.name} is on track."

    return KPI(
        name=point.name, category=point.category,
        value=point.value, unit=point.unit,
        target=point.target, trend=trend,
        health=health, narrative=narrative,
    )


# ---------------------------------------------------------------------------
# Report formatters
# ---------------------------------------------------------------------------

class ReportFormatter(Protocol):
    """Protocol for report output formats."""
    def format(self, kpis: list[KPI]) -> dict[str, Any]: ...


class ExecutiveSummaryFormatter:
    """High-level summary with traffic-light indicators."""

    def format(self, kpis: list[KPI]) -> dict[str, Any]:
        by_category: dict[str, list[dict[str, Any]]] = {}
        for kpi in kpis:
            cat = kpi.category.name.lower()
            by_category.setdefault(cat, []).append({
                "name": kpi.name,
                "value": kpi.value,
                "unit": kpi.unit,
                "health": kpi.health.value,
                "trend": kpi.trend.value,
            })

        overall = HealthRating.GREEN
        for kpi in kpis:
            if kpi.health == HealthRating.RED:
                overall = HealthRating.RED
                break
            if kpi.health == HealthRating.YELLOW:
                overall = HealthRating.YELLOW

        return {
            "report_type": "executive_summary",
            "overall_health": overall.value,
            "kpi_count": len(kpis),
            "categories": by_category,
            "attention_needed": [
                {"name": k.name, "narrative": k.narrative}
                for k in kpis if k.health in (HealthRating.RED, HealthRating.YELLOW)
            ],
        }


# ---------------------------------------------------------------------------
# Metrics publisher
# ---------------------------------------------------------------------------

class MetricsPublisher:
    """Orchestrates collection, transformation, and formatting."""

    def __init__(self, formatter: ReportFormatter | None = None) -> None:
        self._sources: list[MetricSource] = []
        self._formatter = formatter or ExecutiveSummaryFormatter()

    def add_source(self, source: MetricSource) -> None:
        self._sources.append(source)

    def publish(self) -> dict[str, Any]:
        all_points: list[MetricPoint] = []
        for source in self._sources:
            all_points.extend(source.collect())

        kpis = [metric_to_kpi(p) for p in all_points]
        return self._formatter.format(kpis)


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

def main() -> None:
    publisher = MetricsPublisher()
    publisher.add_source(ReliabilitySource(99.95, 2, 0.5, prev_uptime=99.9, prev_incidents=3))
    publisher.add_source(VelocitySource(8.0, 2.5, 4.0, prev_freq=6.0, prev_lead=3.0))
    publisher.add_source(QualitySource(82.0, 15, 120.0))

    report = publisher.publish()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
