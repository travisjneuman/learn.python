"""Level 7 / Project 02 — Monitoring API Adapter.

Collects metrics from simulated monitoring APIs (CPU, memory, disk)
and normalizes them into a unified metrics format.

Key concepts:
- Simulating API responses with mock data (no real HTTP)
- Metric normalization: different units → standard format
- Threshold-based alerting on collected metrics
- Timestamp handling for time-series data
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
# Adapters
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


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


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
