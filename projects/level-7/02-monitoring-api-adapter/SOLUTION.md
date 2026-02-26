# Solution: Level 7 / Project 02 - Monitoring API Adapter

> **STOP — Try it yourself first!**
>
> You learn by building, not by reading answers. Spend at least 30 minutes
> attempting this project before looking here.
>
> - Re-read the [README](./README.md) for requirements
> 
---

## Complete solution

```python
"""Level 7 / Project 02 — Monitoring API Adapter.

Collects metrics from simulated monitoring APIs (CPU, memory, disk)
and normalizes them into a unified metrics format.
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Metric model
# ---------------------------------------------------------------------------

# WHY a unified Metric dataclass? -- Each monitoring API returns different
# field names and units (pct, value_mb, free_pct).  Normalizing into one
# shape lets downstream alerting logic work identically regardless of source.
@dataclass
class Metric:
    name: str
    value: float
    unit: str
    source: str
    timestamp: str
    alert: bool = False
    alert_reason: str = ""


# ---------------------------------------------------------------------------
# Mock monitoring APIs
# ---------------------------------------------------------------------------

# WHY separate mock functions? -- Each simulates a different monitoring
# endpoint with its own response shape.  In production these would be HTTP
# calls; mocking them lets us test adapter logic without network dependencies.
def mock_cpu_api() -> list[dict]:
    return [
        {"metric": "cpu_usage", "pct": 45.2, "host": "web-01", "time": "2025-01-15T08:00:00"},
        {"metric": "cpu_usage", "pct": 92.1, "host": "web-02", "time": "2025-01-15T08:00:00"},
    ]


def mock_memory_api() -> list[dict]:
    return [
        {"type": "memory_used_mb", "value_mb": 3200, "server": "web-01", "at": "2025-01-15T08:00:00"},
        {"type": "memory_used_mb", "value_mb": 7800, "server": "db-01", "at": "2025-01-15T08:00:00"},
    ]


def mock_disk_api() -> list[dict]:
    return [
        {"check": "disk_free_pct", "free_pct": 15.0, "node": "db-01", "ts": "2025-01-15T08:00:00"},
        {"check": "disk_free_pct", "free_pct": 72.0, "node": "web-01", "ts": "2025-01-15T08:00:00"},
    ]


# ---------------------------------------------------------------------------
# Adapters — each maps one API's response shape → Metric
# ---------------------------------------------------------------------------

def adapt_cpu(raw: list[dict]) -> list[Metric]:
    return [
        Metric(name="cpu_usage", value=r["pct"], unit="percent",
               source=r["host"], timestamp=r["time"])
        for r in raw
    ]


def adapt_memory(raw: list[dict]) -> list[Metric]:
    return [
        Metric(name="memory_used", value=r["value_mb"], unit="MB",
               source=r["server"], timestamp=r["at"])
        for r in raw
    ]


def adapt_disk(raw: list[dict]) -> list[Metric]:
    return [
        Metric(name="disk_free", value=r["free_pct"], unit="percent",
               source=r["node"], timestamp=r["ts"])
        for r in raw
    ]


# ---------------------------------------------------------------------------
# Alerting
# ---------------------------------------------------------------------------

# WHY threshold-based alerting? -- Raw metrics are useless without context.
# Thresholds turn a number (92.1%) into an actionable signal ("CPU is too high").
# Using a dict keyed by metric name makes it trivial to add new thresholds
# without modifying the alerting function.
DEFAULT_THRESHOLDS = {
    "cpu_usage": {"max": 90.0, "reason": "CPU above 90%"},
    "memory_used": {"max": 7500, "reason": "Memory above 7500 MB"},
    "disk_free": {"min": 20.0, "reason": "Disk free below 20%"},
}


def check_alerts(
    metrics: list[Metric],
    thresholds: dict | None = None,
) -> list[Metric]:
    """Apply threshold checks and flag metrics that breach limits."""
    thresholds = thresholds or DEFAULT_THRESHOLDS

    for m in metrics:
        rule = thresholds.get(m.name)
        if not rule:
            continue
        # WHY separate max/min checks? -- CPU "too high" and disk "too low"
        # are opposite directions.  Supporting both in one rule dict handles
        # both cases without separate alerting functions.
        if "max" in rule and m.value > rule["max"]:
            m.alert = True
            m.alert_reason = rule["reason"]
        elif "min" in rule and m.value < rule["min"]:
            m.alert = True
            m.alert_reason = rule["reason"]

    return metrics


# ---------------------------------------------------------------------------
# Collector
# ---------------------------------------------------------------------------

def collect_all(custom_sources: dict | None = None) -> list[Metric]:
    """Fetch from all monitoring APIs and normalize."""
    # WHY (fetcher, adapter) tuples? -- Pairing the data source with its
    # adapter keeps them co-located.  Adding a new metric type means adding
    # one tuple, not modifying two separate registries.
    sources = custom_sources or {
        "cpu": (mock_cpu_api, adapt_cpu),
        "memory": (mock_memory_api, adapt_memory),
        "disk": (mock_disk_api, adapt_disk),
    }

    all_metrics: list[Metric] = []
    for name, (fetcher, adapter) in sources.items():
        try:
            raw = fetcher() if callable(fetcher) else fetcher
            metrics = adapter(raw)
            all_metrics.extend(metrics)
            logging.info("collected source=%s metrics=%d", name, len(metrics))
        except Exception as exc:
            logging.warning("skip source=%s error=%s", name, exc)

    return all_metrics


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def run(input_path: Path, output_path: Path) -> dict:
    metrics = collect_all()
    check_alerts(metrics)

    alerts = [m for m in metrics if m.alert]

    summary = {
        "total_metrics": len(metrics),
        "alerts": len(alerts),
        "metrics": [
            {"name": m.name, "value": m.value, "unit": m.unit,
             "source": m.source, "alert": m.alert, "reason": m.alert_reason}
            for m in metrics
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("collected %d metrics, %d alerts", len(metrics), len(alerts))
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monitoring API Adapter — collect and normalize metrics"
    )
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/output_summary.json")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `Metric` dataclass with mutable `alert` fields | Alerting is a post-processing step that enriches the same objects -- avoids creating a separate AlertedMetric type | Immutable metrics + separate Alert dataclass -- cleaner but doubles the object count |
| `(fetcher, adapter)` tuple registry | Co-locates data source and its normalizer so they cannot get out of sync | Separate `FETCHERS` and `ADAPTERS` dicts -- risks mismatched keys |
| Threshold dict supports both `max` and `min` | CPU and disk alert in opposite directions; one rule structure handles both | Separate `max_thresholds` / `min_thresholds` dicts -- more verbose |
| `check_alerts` mutates metrics in place | Avoids copying large metric lists; caller already owns the list | Return new list of AlertedMetric -- purer but allocates more memory |

## Alternative approaches

### Approach B: Observer pattern for alerting

```python
class AlertObserver:
    def __init__(self, thresholds):
        self.thresholds = thresholds
        self.alerts = []

    def on_metric(self, metric: Metric):
        rule = self.thresholds.get(metric.name)
        if rule and metric.value > rule.get("max", float("inf")):
            self.alerts.append(metric)
```

**Trade-off:** The observer pattern decouples metric collection from alerting, which is useful when you have multiple consumers (alerts, dashboards, storage). Overkill here where we only have one consumer.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| A monitoring API returns an empty list | No crash, but the missing source goes unnoticed | Log a warning when a source returns 0 metrics |
| Threshold rule has both `max` and `min` for same metric | Only the first matching branch fires due to `elif` | Use separate `if` blocks if a metric could breach both directions |
| Metric value is a string instead of float | Comparison `>` between str and float raises `TypeError` | Cast values to float in adapters, or validate types before alerting |
