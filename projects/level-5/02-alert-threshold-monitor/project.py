"""Level 5 / Project 02 — Alert Threshold Monitor.

Monitors metric values against configurable thresholds and triggers
alerts when thresholds are breached. Supports warning and critical
levels with cooldown periods to avoid alert storms.
"""

from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# ---------- threshold logic ----------


def check_threshold(value: float, warning: float, critical: float) -> str:
    """Classify a metric value against warning/critical thresholds.

    Returns 'critical', 'warning', or 'ok'.
    Assumes higher values are worse (e.g., CPU usage, latency).
    """
    if value >= critical:
        return "critical"
    if value >= warning:
        return "warning"
    return "ok"


def evaluate_metrics(
    metrics: list[dict],
    thresholds: dict[str, dict],
) -> list[dict]:
    """Evaluate a list of metric readings against threshold definitions.

    metrics: [{"name": "cpu", "value": 85.5, "timestamp": "..."}]
    thresholds: {"cpu": {"warning": 70, "critical": 90}}

    Returns a list of alert dicts for breached thresholds.
    """
    alerts: list[dict] = []

    for metric in metrics:
        name = metric.get("name", "")
        value = metric.get("value", 0)
        threshold = thresholds.get(name)

        if threshold is None:
            continue  # no threshold defined for this metric

        status = check_threshold(value, threshold["warning"], threshold["critical"])
        if status != "ok":
            alerts.append({
                "metric": name,
                "value": value,
                "level": status,
                "threshold": threshold[status],
                "timestamp": metric.get("timestamp", ""),
            })
            logging.warning("ALERT [%s] %s=%.2f (threshold: %.2f)", status.upper(), name, value, threshold[status])

    return alerts


def apply_cooldown(alerts: list[dict], cooldown_seconds: int = 300) -> list[dict]:
    """Filter alerts to enforce a cooldown period per metric.

    Only the first alert per metric within the cooldown window is kept.
    Prevents alert storms when a metric stays above threshold.
    """
    last_alert: dict[str, datetime] = {}
    filtered: list[dict] = []

    for alert in alerts:
        name = alert["metric"]
        ts_str = alert.get("timestamp", "")

        try:
            ts = datetime.fromisoformat(ts_str)
        except (ValueError, TypeError):
            ts = datetime.now(timezone.utc)

        prev = last_alert.get(name)
        if prev and (ts - prev).total_seconds() < cooldown_seconds:
            continue  # within cooldown, skip

        last_alert[name] = ts
        filtered.append(alert)

    return filtered

# ---------- runner ----------


def run(metrics_path: Path, thresholds_path: Path, output_path: Path, cooldown: int = 300) -> dict:
    if not metrics_path.exists():
        raise FileNotFoundError(f"Metrics file not found: {metrics_path}")
    if not thresholds_path.exists():
        raise FileNotFoundError(f"Thresholds file not found: {thresholds_path}")

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    thresholds = json.loads(thresholds_path.read_text(encoding="utf-8"))

    alerts = evaluate_metrics(metrics, thresholds)
    filtered = apply_cooldown(alerts, cooldown)

    report = {
        "total_metrics": len(metrics),
        "raw_alerts": len(alerts),
        "alerts_after_cooldown": len(filtered),
        "alerts": filtered,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Monitoring complete: %d alerts (%d after cooldown)", len(alerts), len(filtered))
    return report

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitor metrics against thresholds")
    parser.add_argument("--metrics", default="data/metrics.json")
    parser.add_argument("--thresholds", default="data/thresholds.json")
    parser.add_argument("--output", default="data/alert_report.json")
    parser.add_argument("--cooldown", type=int, default=300)
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.metrics), Path(args.thresholds), Path(args.output), args.cooldown)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
