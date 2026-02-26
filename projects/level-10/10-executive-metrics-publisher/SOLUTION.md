# Solution: Level 10 / Project 10 - Executive Metrics Publisher

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
>.

---

## Complete solution

```python
"""Executive Metrics Publisher -- Transform technical metrics into executive-friendly reports."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol


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
# sources in different formats (Datadog, PagerDuty, Jira, etc.). Normalizing
# into a common shape lets the pipeline aggregate across sources without
# knowing their origin. This is the Adapter pattern: each source translates
# its native format into MetricPoint. frozen=True ensures audit integrity.
@dataclass(frozen=True)
class MetricPoint:
    name: str
    category: MetricCategory
    value: float
    unit: str
    target: float | None = None
    previous: float | None = None


@dataclass
class KPI:
    name: str
    category: MetricCategory
    value: float
    unit: str
    target: float | None = None
    trend: TrendDirection = TrendDirection.STABLE
    health: HealthRating = HealthRating.GREEN
    narrative: str = ""


# WHY Protocol for MetricSource? -- Each team owns different monitoring tools.
# The Protocol lets them contribute metrics without coupling to the publisher's
# internals. A new source (e.g., CostSource from AWS billing) just implements
# collect() and plugs in.
class MetricSource(Protocol):
    def source_name(self) -> str: ...
    def collect(self) -> list[MetricPoint]: ...


class ReliabilitySource:
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


# WHY 5% threshold for stability? -- Small fluctuations in metrics are noise,
# not signal. A 2% uptime change is within normal variance. The 5% dead zone
# prevents executives from chasing noise while still catching real trends.
def compute_trend(current: float, previous: float | None, higher_is_better: bool = True) -> TrendDirection:
    if previous is None:
        return TrendDirection.STABLE
    delta = current - previous
    threshold = abs(previous) * 0.05 if previous != 0 else 1.0
    if abs(delta) < threshold:
        return TrendDirection.STABLE
    improving = delta > 0 if higher_is_better else delta < 0
    return TrendDirection.IMPROVING if improving else TrendDirection.DECLINING


# WHY separate higher/lower-is-better logic? -- Uptime at 99% is healthy
# (higher is better), but 15 incidents is unhealthy (lower is better). Using
# a single formula for both would invert the health rating for half the metrics.
def compute_health(value: float, target: float | None, higher_is_better: bool = True) -> HealthRating:
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
        if target == 0:
            return HealthRating.GREEN if value == 0 else HealthRating.YELLOW
        ratio = value / target
        if ratio <= 1.05:
            return HealthRating.GREEN
        if ratio <= 1.5:
            return HealthRating.YELLOW
        return HealthRating.RED


LOWER_IS_BETTER = {"Incidents", "MTTR", "Lead Time", "Change Failure Rate", "Open Bugs", "Tech Debt"}


# WHY narrative text on each KPI? -- Executives do not read raw numbers.
# A sentence like "Uptime is below target -- needs attention" communicates
# the same information as "99.2% vs 99.9% target" but in 2 seconds instead
# of 30. The narrative transforms data into actionable communication.
def metric_to_kpi(point: MetricPoint) -> KPI:
    higher_is_better = point.name not in LOWER_IS_BETTER
    trend = compute_trend(point.value, point.previous, higher_is_better)
    health = compute_health(point.value, point.target, higher_is_better)

    if health == HealthRating.RED:
        narrative = f"{point.name} is below target — needs attention."
    elif health == HealthRating.YELLOW:
        narrative = f"{point.name} is near target — monitor closely."
    else:
        narrative = f"{point.name} is on track."

    return KPI(name=point.name, category=point.category,
               value=point.value, unit=point.unit,
               target=point.target, trend=trend,
               health=health, narrative=narrative)


class ReportFormatter(Protocol):
    def format(self, kpis: list[KPI]) -> dict[str, Any]: ...


# WHY traffic-light overall health? -- A single color (green/yellow/red)
# answers the executive's first question: "Do I need to pay attention?"
# If any KPI is RED, the whole report is RED. This worst-case escalation
# ensures critical issues are never hidden by averaging.
class ExecutiveSummaryFormatter:
    def format(self, kpis: list[KPI]) -> dict[str, Any]:
        by_category: dict[str, list[dict[str, Any]]] = {}
        for kpi in kpis:
            cat = kpi.category.name.lower()
            by_category.setdefault(cat, []).append({
                "name": kpi.name, "value": kpi.value, "unit": kpi.unit,
                "health": kpi.health.value, "trend": kpi.trend.value,
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


class MetricsPublisher:
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


def main() -> None:
    publisher = MetricsPublisher()
    publisher.add_source(ReliabilitySource(99.95, 2, 0.5, prev_uptime=99.9, prev_incidents=3))
    publisher.add_source(VelocitySource(8.0, 2.5, 4.0, prev_freq=6.0, prev_lead=3.0))
    publisher.add_source(QualitySource(82.0, 15, 120.0))
    report = publisher.publish()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Adapter pattern for metric sources | Each source (Datadog, Jira, PagerDuty) has a different API; adapters normalize into MetricPoint so the pipeline is source-agnostic | Single monolithic collector -- tightly couples the publisher to every monitoring tool |
| Separate higher/lower-is-better logic | Uptime and incidents have opposite health semantics; a single formula would invert ratings for half the metrics | Normalize all metrics to 0-1 scale before comparison -- adds a pre-processing step and obscures original values |
| 5% dead zone for trend detection | Small metric fluctuations are noise; the dead zone prevents executives from reacting to statistical variance | Rolling average smoothing -- more accurate but harder to explain and requires historical data |
| Narrative text on each KPI | Executives scan sentences faster than raw numbers; narratives make reports self-explanatory | Numeric-only reports -- require domain knowledge to interpret |
| Worst-case escalation for overall health | If any single KPI is RED, the report must surface it; averaging would hide critical issues | Weighted average health -- more nuanced but can mask individual failures |

## Alternative approaches

### Approach B: DORA metrics with burn-down tracking

```python
from dataclasses import dataclass

@dataclass
class DORAMetrics:
    deploy_frequency: float      # deploys per week
    lead_time_days: float        # commit to production
    change_failure_rate: float   # % of deploys causing incidents
    mttr_hours: float            # mean time to recovery

    @property
    def elite_score(self) -> int:
        """Count how many metrics meet DORA 'Elite' thresholds."""
        elite = 0
        if self.deploy_frequency >= 7:  elite += 1  # multiple per day
        if self.lead_time_days < 1:     elite += 1  # less than one day
        if self.change_failure_rate < 5: elite += 1  # under 5%
        if self.mttr_hours < 1:         elite += 1  # under one hour
        return elite

    @property
    def classification(self) -> str:
        score = self.elite_score
        if score == 4: return "Elite"
        if score >= 3: return "High"
        if score >= 2: return "Medium"
        return "Low"
```

**Trade-off:** DORA metrics are the industry standard for measuring software delivery performance (from the "Accelerate" book). They provide a well-researched framework with clear Elite/High/Medium/Low classifications. However, they cover only delivery velocity and stability -- they miss quality, cost, and business-specific KPIs that the general pipeline captures.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Target of zero for a "higher is better" metric | `compute_health` divides by zero; the guard `if target > 0` returns ratio 1.0 which maps to GREEN | Always validate that targets are positive for ratio-based health checks |
| No previous value provided | `compute_trend` returns STABLE, which is correct but may mask a first reading that is already bad | Combine trend with health: even if trend is STABLE, a RED health rating still surfaces the issue |
| No sources registered before `publish()` | Returns an empty report with zero KPIs -- valid but potentially confusing | Add a minimum KPI count guard that warns when fewer than 3 KPIs are collected |
