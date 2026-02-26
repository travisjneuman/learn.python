"""Level 5 / Project 06 — Metrics Summary Engine.

Aggregates numeric metrics with percentiles, moving averages, and
statistical summaries. Reads time-series data from JSON and produces
a structured report with per-metric statistics.

Concepts practiced:
- Statistical computation (percentiles, standard deviation)
- Moving average smoothing for noisy data
- Grouping records by key and aggregating values
- Structured JSON report generation
"""

from __future__ import annotations

import argparse
import json
import logging
import math
from pathlib import Path


# ---------- logging ----------

def configure_logging() -> None:
    """Set up logging so aggregation progress is traceable."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


# ---------- statistical helpers ----------

# WHY hand-roll percentile instead of using statistics.quantiles? --
# The standard library function requires Python 3.8+ and has different
# edge-case behavior. Writing it by hand teaches the linear interpolation
# algorithm that most statistics libraries use internally.

def percentile(values: list[float], p: float) -> float:
    """Compute the p-th percentile (0-100 scale) via linear interpolation.

    If the list is empty the result is 0.0 — callers should check length
    before interpreting the return value.
    """
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    k = (len(sorted_vals) - 1) * (p / 100)
    floor_k = math.floor(k)
    ceil_k = math.ceil(k)
    if floor_k == ceil_k:
        return sorted_vals[int(k)]
    # Linear interpolation between the two surrounding values.
    return sorted_vals[floor_k] * (ceil_k - k) + sorted_vals[ceil_k] * (k - floor_k)


def standard_deviation(values: list[float]) -> float:
    """Compute population standard deviation for a list of numbers.

    Returns 0.0 for lists with fewer than 2 elements because there is
    no meaningful spread to measure.
    """
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


def moving_average(values: list[float], window: int = 3) -> list[float]:
    """Compute a simple moving average with the given window size.

    WHY moving averages? -- Raw metrics are noisy (CPU jumps from 30%
    to 90% on a single spike). A moving average smooths out transient
    spikes so you can see the underlying trend.

    A window of 0 or a negative value returns an empty list.
    """
    if window <= 0 or not values:
        return []
    result: list[float] = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        window_vals = values[start : i + 1]
        result.append(sum(window_vals) / len(window_vals))
    return [round(v, 2) for v in result]


# ---------- summarisation ----------


def summarize_metric(values: list[float]) -> dict:
    """Compute a full statistical summary for one metric's values.

    Returns count, min, max, mean, standard deviation, and
    percentiles (p50, p90, p99).
    """
    if not values:
        return {"count": 0, "warning": "no data points"}
    return {
        "count": len(values),
        "min": round(min(values), 2),
        "max": round(max(values), 2),
        "mean": round(sum(values) / len(values), 2),
        "stddev": round(standard_deviation(values), 2),
        "p50": round(percentile(values, 50), 2),
        "p90": round(percentile(values, 90), 2),
        "p99": round(percentile(values, 99), 2),
    }


def aggregate_metrics(data: list[dict]) -> dict:
    """Group raw metric entries by name and compute summaries.

    Each entry in *data* should have at least ``name`` and ``value``
    keys.  Entries with missing or non-numeric values are silently
    skipped so that partial data does not crash the pipeline.
    """
    groups: dict[str, list[float]] = {}
    skipped = 0
    for entry in data:
        name = entry.get("name", "unknown")
        value = entry.get("value")
        if value is None:
            skipped += 1
            continue
        try:
            groups.setdefault(name, []).append(float(value))
        except (ValueError, TypeError):
            skipped += 1
            logging.warning("Skipping non-numeric value for metric '%s': %r", name, value)
            continue

    summaries: dict = {}
    for name, values in sorted(groups.items()):
        summaries[name] = {
            "summary": summarize_metric(values),
            "moving_avg_3": moving_average(values, 3),
        }
        logging.info("Metric '%s': %d data points", name, len(values))

    if skipped:
        logging.warning("Skipped %d entries with missing/invalid values", skipped)

    return summaries


# ---------- pipeline ----------


def run(input_path: Path, output_path: Path) -> dict:
    """Load metrics JSON, aggregate, and write the summary report."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    raw_text = input_path.read_text(encoding="utf-8")
    data = json.loads(raw_text)
    if not isinstance(data, list):
        raise ValueError("Input must be a JSON array of metric entries")

    summaries = aggregate_metrics(data)
    report = {
        "input_file": str(input_path),
        "metric_count": len(summaries),
        "total_entries": len(data),
        "metrics": summaries,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Summarized %d metrics from %d entries", len(summaries), len(data))
    return report


# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the metrics summary engine."""
    parser = argparse.ArgumentParser(
        description="Aggregate metrics with percentiles and moving averages",
    )
    parser.add_argument("--input", default="data/metrics.json", help="Path to metrics JSON")
    parser.add_argument("--output", default="data/summary.json", help="Output report path")
    return parser.parse_args()


def main() -> None:
    """Entry point: configure logging, parse args, run the engine."""
    configure_logging()
    args = parse_args()
    report = run(Path(args.input), Path(args.output))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
