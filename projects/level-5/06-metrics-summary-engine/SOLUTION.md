# Metrics Summary Engine — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 5 / Project 06 — Metrics Summary Engine.

Aggregates numeric metrics with percentiles, moving averages, and
statistical summaries.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- statistical helpers ----------

# WHY: Hand-roll percentile instead of using statistics.quantiles so the
# learner understands the linear interpolation algorithm that most
# statistics libraries use internally.

def percentile(values: list[float], p: float) -> float:
    """Compute the p-th percentile (0-100 scale) via linear interpolation."""
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    # WHY: k is the fractional index into the sorted list. For p=50 with
    # 10 items, k = 9 * 0.5 = 4.5, meaning the median falls between
    # index 4 and index 5.
    k = (len(sorted_vals) - 1) * (p / 100)
    floor_k = math.floor(k)
    ceil_k = math.ceil(k)
    if floor_k == ceil_k:
        return sorted_vals[int(k)]
    # WHY: Linear interpolation gives a weighted average of the two
    # surrounding values. This is more accurate than just rounding
    # to the nearest index.
    return sorted_vals[floor_k] * (ceil_k - k) + sorted_vals[ceil_k] * (k - floor_k)


def standard_deviation(values: list[float]) -> float:
    """Compute population standard deviation."""
    # WHY: With fewer than 2 values, spread is meaningless — return 0.
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    # WHY: Population stddev (divides by n, not n-1) is used here because
    # we are summarizing the entire dataset, not estimating from a sample.
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


def moving_average(values: list[float], window: int = 3) -> list[float]:
    """Compute a simple moving average with the given window size.

    WHY moving averages? -- Raw metrics are noisy (CPU jumps from 30%
    to 90% on a single spike). A moving average smooths out transient
    spikes so you can see the underlying trend.
    """
    if window <= 0 or not values:
        return []
    result: list[float] = []
    for i in range(len(values)):
        # WHY: Use max(0, i - window + 1) so early values use a smaller
        # window rather than being skipped entirely. This gives output
        # for every input point.
        start = max(0, i - window + 1)
        window_vals = values[start : i + 1]
        result.append(sum(window_vals) / len(window_vals))
    return [round(v, 2) for v in result]

# ---------- summarisation ----------

def summarize_metric(values: list[float]) -> dict:
    """Compute a full statistical summary for one metric's values."""
    if not values:
        # WHY: Return a warning instead of crashing so the caller
        # can still process other metrics that do have data.
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
    """Group raw metric entries by name and compute summaries."""
    groups: dict[str, list[float]] = {}
    skipped = 0
    for entry in data:
        name = entry.get("name", "unknown")
        value = entry.get("value")
        # WHY: Skip entries with missing values rather than crashing.
        # Partial data is common in real metrics pipelines.
        if value is None:
            skipped += 1
            continue
        try:
            # WHY: float() handles both int and string numeric values,
            # making the ingestion more resilient.
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
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    raw_text = input_path.read_text(encoding="utf-8")
    data = json.loads(raw_text)
    # WHY: Validate the top-level structure early. A JSON object instead
    # of an array would silently produce wrong results.
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
    parser = argparse.ArgumentParser(
        description="Aggregate metrics with percentiles and moving averages",
    )
    parser.add_argument("--input", default="data/metrics.json")
    parser.add_argument("--output", default="data/summary.json")
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.input), Path(args.output))
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Hand-rolled percentile with linear interpolation | Teaches the algorithm that libraries like NumPy use internally. Also avoids requiring `statistics.quantiles` which behaves differently at edge cases. |
| Population stddev (divide by n, not n-1) | We are summarizing the complete dataset, not estimating from a sample. Population stddev is the correct measure here. |
| `setdefault` for grouping | `groups.setdefault(name, []).append(value)` creates the list on first access and appends in one expression. Cleaner than checking `if name not in groups`. |
| Moving average with expanding window at start | Rather than skipping the first `window-1` values (which loses data), we use a smaller window at the start. This produces output for every input point. |

## Alternative Approaches

### Using the `statistics` standard library

```python
import statistics

def summarize_metric_stdlib(values: list[float]) -> dict:
    return {
        "count": len(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "stdev": statistics.pstdev(values),
        "p90": statistics.quantiles(values, n=10)[-1] if len(values) >= 2 else values[0],
    }
```

The standard library is more concise and handles edge cases. However, `statistics.quantiles` requires at least 2 data points, so you still need to handle the single-value case manually. Using the manual approach first builds understanding.

## Common Pitfalls

1. **Division by zero with empty values** — `sum(values) / len(values)` crashes when the list is empty. Always check `if not values` before computing aggregates.
2. **Integer division in percentile** — In Python 3 `/` always returns float, but in Python 2 it was integer division. The `(p / 100)` expression is safe in Python 3 but would need `from __future__ import division` in Python 2.
3. **Moving average with window=0** — A zero or negative window makes no mathematical sense. The function returns an empty list rather than crashing, but the caller should validate the input before calling.
