"""Dashboard KPI Assembler — aggregate metrics from multiple sources into a unified dashboard.

Design rationale:
    Real dashboards pull KPIs from heterogeneous sources (logs, databases, APIs).
    This project teaches structured aggregation, threshold evaluation, and
    trend detection — core skills for any observability or BI pipeline.

Concepts practised:
    - dataclasses for typed metric containers
    - enum for status classification
    - statistical helpers (mean, percentile)
    - JSON-based source ingestion
    - threshold-driven alerting
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


# --- Domain types -------------------------------------------------------

class KPIStatus(Enum):
    """Traffic-light status for a KPI relative to its threshold."""
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


# WHY threshold-based evaluation on the KPI itself? -- Embedding the
# evaluate method on KPIDefinition means each KPI carries its own
# alerting logic. This is the Information Expert pattern: the object
# with the threshold data is the one that decides the status colour.
@dataclass
class KPIDefinition:
    """Blueprint for a single KPI: what to measure and when to alert."""
    name: str
    unit: str
    green_threshold: float   # values <= this are green
    yellow_threshold: float  # values <= this (but > green) are yellow; above is red

    def evaluate(self, value: float) -> KPIStatus:
        """Return status colour for *value* against configured thresholds."""
        if value <= self.green_threshold:
            return KPIStatus.GREEN
        if value <= self.yellow_threshold:
            return KPIStatus.YELLOW
        return KPIStatus.RED


@dataclass
class MetricSample:
    """A single timestamped metric reading from a source."""
    source: str
    kpi_name: str
    timestamp: str
    value: float


@dataclass
class KPISummary:
    """Aggregated result for one KPI across all samples."""
    name: str
    unit: str
    sample_count: int
    mean: float
    p95: float
    minimum: float
    maximum: float
    status: KPIStatus
    trend: str  # "improving", "stable", "degrading"


@dataclass
class Dashboard:
    """Top-level dashboard containing all KPI summaries."""
    title: str
    kpis: list[KPISummary] = field(default_factory=list)
    red_count: int = 0
    yellow_count: int = 0
    green_count: int = 0
    overall_health: str = "unknown"


# --- Statistical helpers ------------------------------------------------

def percentile(values: list[float], pct: float) -> float:
    """Compute the *pct*-th percentile (0-100) of sorted *values*.

    Uses the nearest-rank method — simple and easy to reason about.
    """
    if not values:
        return 0.0
    sorted_v = sorted(values)
    rank = math.ceil(pct / 100.0 * len(sorted_v)) - 1
    return sorted_v[max(0, rank)]


def compute_trend(values: list[float]) -> str:
    """Determine whether *values* are improving, stable, or degrading.

    Splits values into first-half and second-half and compares means.
    A >10 % shift counts as a change; everything else is "stable".
    """
    if len(values) < 4:
        return "stable"
    mid = len(values) // 2
    first_mean = sum(values[:mid]) / mid
    second_mean = sum(values[mid:]) / (len(values) - mid)
    if first_mean == 0:
        return "stable"
    change_pct = (second_mean - first_mean) / abs(first_mean) * 100
    # Lower is better for latency-style KPIs
    if change_pct < -10:
        return "improving"
    if change_pct > 10:
        return "degrading"
    return "stable"


# --- Core logic ---------------------------------------------------------

def load_kpi_definitions(raw: list[dict[str, Any]]) -> list[KPIDefinition]:
    """Parse KPI definition dicts into typed objects."""
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
    """Parse raw sample dicts into typed MetricSample objects."""
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
    """Aggregate *samples* for a single KPI and evaluate health status."""
    values = [s.value for s in samples if s.kpi_name == definition.name]
    if not values:
        return KPISummary(
            name=definition.name, unit=definition.unit,
            sample_count=0, mean=0.0, p95=0.0,
            minimum=0.0, maximum=0.0,
            status=KPIStatus.GREEN, trend="stable",
        )
    mean_val = sum(values) / len(values)
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
    """Build a complete Dashboard from definitions and samples."""
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

    # Overall health: red if any red, yellow if any yellow, else green
    if dashboard.red_count > 0:
        dashboard.overall_health = "critical"
    elif dashboard.yellow_count > 0:
        dashboard.overall_health = "warning"
    else:
        dashboard.overall_health = "healthy"
    return dashboard


def dashboard_to_dict(dashboard: Dashboard) -> dict[str, Any]:
    """Serialize a Dashboard to a plain dict for JSON output."""
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
                "name": k.name,
                "unit": k.unit,
                "sample_count": k.sample_count,
                "mean": k.mean,
                "p95": k.p95,
                "min": k.minimum,
                "max": k.maximum,
                "status": k.status.value,
                "trend": k.trend,
            }
            for k in dashboard.kpis
        ],
    }


# --- CLI ----------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Assemble KPI data from multiple sources into a dashboard."
    )
    parser.add_argument(
        "--input", default="data/sample_input.json",
        help="Path to JSON file with kpi_definitions and samples",
    )
    parser.add_argument(
        "--output", default="data/dashboard_output.json",
        help="Path for dashboard JSON output",
    )
    parser.add_argument(
        "--title", default="Operations Dashboard",
        help="Dashboard title",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Entry point: load data, assemble dashboard, write output."""
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
