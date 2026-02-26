# Solution: Level 8 / Project 01 - Dashboard KPI Assembler

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Dashboard KPI Assembler -- aggregate metrics from multiple sources into a unified dashboard."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


# --- Domain types -------------------------------------------------------

# WHY Enum for status? -- Traffic-light status is a closed set of values.
# Using an Enum prevents typos ("grren") and enables IDE autocomplete.
# The .value attribute gives the JSON-friendly string when serializing.
class KPIStatus(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


# WHY embed evaluate() on KPIDefinition? -- This is the Information Expert
# pattern: the object that holds the threshold data is the one that decides
# the status colour. Putting evaluation logic elsewhere would scatter
# knowledge about thresholds across multiple locations.
@dataclass
class KPIDefinition:
    name: str
    unit: str
    green_threshold: float   # values <= this are green
    yellow_threshold: float  # values <= this (but > green) are yellow; above is red

    def evaluate(self, value: float) -> KPIStatus:
        if value <= self.green_threshold:
            return KPIStatus.GREEN
        if value <= self.yellow_threshold:
            return KPIStatus.YELLOW
        return KPIStatus.RED


@dataclass
class MetricSample:
    source: str
    kpi_name: str
    timestamp: str
    value: float


@dataclass
class KPISummary:
    name: str
    unit: str
    sample_count: int
    mean: float
    p95: float
    minimum: float
    maximum: float
    status: KPIStatus
    trend: str  # "improving", "stable", "degrading"


# WHY a Dashboard dataclass with count fields? -- Pre-computing red/yellow/green
# counts at assembly time avoids re-iterating the KPI list every time a consumer
# needs the summary. The overall_health field gives a single top-level verdict.
@dataclass
class Dashboard:
    title: str
    kpis: list[KPISummary] = field(default_factory=list)
    red_count: int = 0
    yellow_count: int = 0
    green_count: int = 0
    overall_health: str = "unknown"


# --- Statistical helpers ------------------------------------------------

# WHY nearest-rank percentile? -- It is the simplest percentile method and
# matches what most monitoring dashboards display. More complex interpolation
# methods (e.g. linear) add precision but also complexity that distracts
# from the core lesson of threshold-based evaluation.
def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    sorted_v = sorted(values)
    # WHY math.ceil? -- Nearest-rank: the smallest value whose rank
    # is >= the requested percentile. ceil ensures we never undershoot.
    rank = math.ceil(pct / 100.0 * len(sorted_v)) - 1
    return sorted_v[max(0, rank)]


# WHY split-half trend detection? -- Comparing first-half mean to second-half
# mean is a lightweight approach that doesn't require scipy or numpy.
# The 10% threshold avoids noise: small fluctuations report "stable".
def compute_trend(values: list[float]) -> str:
    # WHY minimum 4 samples? -- With fewer than 4, the halves contain
    # 1-2 values each, making the comparison statistically meaningless.
    if len(values) < 4:
        return "stable"
    mid = len(values) // 2
    first_mean = sum(values[:mid]) / mid
    second_mean = sum(values[mid:]) / (len(values) - mid)
    if first_mean == 0:
        return "stable"
    change_pct = (second_mean - first_mean) / abs(first_mean) * 100
    # WHY "lower is better"? -- For latency-style KPIs, a decrease is
    # improvement. This convention matches how Grafana and Datadog render trends.
    if change_pct < -10:
        return "improving"
    if change_pct > 10:
        return "degrading"
    return "stable"


# --- Core logic ---------------------------------------------------------

def load_kpi_definitions(raw: list[dict[str, Any]]) -> list[KPIDefinition]:
    # WHY parse into typed objects? -- Working with dicts throughout the
    # codebase invites KeyError bugs. Typed dataclasses catch missing fields
    # at construction time and give IDE support downstream.
    return [
        KPIDefinition(
            name=d["name"],
            unit=d.get("unit", ""),
            green_threshold=float(d["green_threshold"]),
            yellow_threshold=float(d["yellow_threshold"]),
        )
        for d in raw
    ]


def load_metric_samples(raw: list[dict[str, Any]]) -> list[MetricSample]:
    return [
        MetricSample(
            source=s["source"],
            kpi_name=s["kpi_name"],
            timestamp=s.get("timestamp", ""),
            value=float(s["value"]),
        )
        for s in raw
    ]


def aggregate_kpi(
    definition: KPIDefinition,
    samples: list[MetricSample],
) -> KPISummary:
    # WHY filter samples by kpi_name here? -- Each call aggregates one KPI.
    # Filtering inside the function keeps the caller simple (pass all samples).
    values = [s.value for s in samples if s.kpi_name == definition.name]
    if not values:
        return KPISummary(
            name=definition.name, unit=definition.unit,
            sample_count=0, mean=0.0, p95=0.0,
            minimum=0.0, maximum=0.0,
            status=KPIStatus.GREEN, trend="stable",
        )
    mean_val = sum(values) / len(values)
    # WHY evaluate on mean? -- The mean is the primary aggregation for
    # threshold comparison. The p95 is reported for context but doesn't
    # drive the traffic-light status in this design.
    return KPISummary(
        name=definition.name,
        unit=definition.unit,
        sample_count=len(values),
        mean=round(mean_val, 2),
        p95=round(percentile(values, 95), 2),
        minimum=round(min(values), 2),
        maximum=round(max(values), 2),
        status=definition.evaluate(mean_val),
        trend=compute_trend(values),
    )


def assemble_dashboard(
    title: str,
    definitions: list[KPIDefinition],
    samples: list[MetricSample],
) -> Dashboard:
    dashboard = Dashboard(title=title)
    for defn in definitions:
        summary = aggregate_kpi(defn, samples)
        dashboard.kpis.append(summary)
        if summary.status == KPIStatus.RED:
            dashboard.red_count += 1
        elif summary.status == KPIStatus.YELLOW:
            dashboard.yellow_count += 1
        else:
            dashboard.green_count += 1

    # WHY worst-status-wins for overall_health? -- A single red KPI means
    # the system needs attention. This mirrors how Grafana dashboards show
    # a red banner if any panel is alerting.
    if dashboard.red_count > 0:
        dashboard.overall_health = "critical"
    elif dashboard.yellow_count > 0:
        dashboard.overall_health = "warning"
    else:
        dashboard.overall_health = "healthy"
    return dashboard


def dashboard_to_dict(dashboard: Dashboard) -> dict[str, Any]:
    # WHY a separate serialization function? -- Keeps the Dashboard dataclass
    # free of JSON concerns. You could swap this for Protobuf or MessagePack
    # without touching the domain model.
    return {
        "title": dashboard.title,
        "overall_health": dashboard.overall_health,
        "counts": {
            "red": dashboard.red_count,
            "yellow": dashboard.yellow_count,
            "green": dashboard.green_count,
        },
        "kpis": [
            {
                "name": k.name, "unit": k.unit,
                "sample_count": k.sample_count, "mean": k.mean,
                "p95": k.p95, "min": k.minimum, "max": k.maximum,
                "status": k.status.value, "trend": k.trend,
            }
            for k in dashboard.kpis
        ],
    }


# --- CLI ----------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble KPI data from multiple sources into a dashboard."
    )
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/dashboard_output.json")
    parser.add_argument("--title", default="Operations Dashboard")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    raw = json.loads(input_path.read_text(encoding="utf-8"))
    definitions = load_kpi_definitions(raw["kpi_definitions"])
    samples = load_metric_samples(raw["samples"])

    dashboard = assemble_dashboard(args.title, definitions, samples)
    output = dashboard_to_dict(dashboard)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Evaluate status on mean, not p95 | Mean gives a stable central measure for threshold comparison; p95 is reported for context | Evaluate on p95 -- better for latency KPIs but overly sensitive for throughput metrics |
| Split-half trend detection | Zero-dependency approach that works without numpy/scipy | Linear regression -- more accurate but adds a heavy dependency for a simple dashboard |
| Worst-status-wins for overall health | A single failing KPI warrants attention; mirrors Grafana/Datadog behaviour | Majority voting -- hides critical issues if most KPIs are green |
| Separate `dashboard_to_dict` function | Decouples domain model from serialization format | `to_dict()` method on Dashboard -- couples serialization to the dataclass |

## Alternative approaches

### Approach B: Pandas-based aggregation

```python
import pandas as pd

def aggregate_kpi_pandas(definition, samples_df):
    filtered = samples_df[samples_df["kpi_name"] == definition.name]
    return {
        "mean": filtered["value"].mean(),
        "p95": filtered["value"].quantile(0.95),
        "min": filtered["value"].min(),
        "max": filtered["value"].max(),
    }
```

**Trade-off:** Pandas makes aggregation one-liners but adds a 30MB dependency. For a dashboard assembler processing thousands of KPIs, the DataFrame overhead could actually be slower than pure Python list comprehensions. Use Pandas when you need complex groupby operations or already have it in the stack.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| KPI with zero samples | Division by zero in mean calculation | Return a default KPISummary with 0.0 values and GREEN status |
| Trend with fewer than 4 data points | Split-half comparison is meaningless with 1-2 values per half | Return "stable" for any KPI with fewer than 4 samples |
| first_mean is exactly 0.0 | Division by zero in percentage change calculation | Guard with `if first_mean == 0: return "stable"` |
