# Alert Threshold Monitor — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
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

# WHY: A pure function that classifies a single value. Keeping this
# separate from evaluate_metrics makes it easy to test and reuse.
def check_threshold(value: float, warning: float, critical: float) -> str:
    """Classify a metric value against warning/critical thresholds."""
    # WHY: Check critical first because a value >= critical is also >= warning.
    # We want the most severe match to win.
    if value >= critical:
        return "critical"
    if value >= warning:
        return "warning"
    return "ok"


def evaluate_metrics(
    metrics: list[dict],
    thresholds: dict[str, dict],
) -> list[dict]:
    """Evaluate a list of metric readings against threshold definitions."""
    alerts: list[dict] = []

    for metric in metrics:
        name = metric.get("name", "")
        value = metric.get("value", 0)
        threshold = thresholds.get(name)

        # WHY: Skip metrics without thresholds rather than crashing.
        # Not every metric needs alerting.
        if threshold is None:
            continue

        status = check_threshold(value, threshold["warning"], threshold["critical"])
        if status != "ok":
            alerts.append({
                "metric": name,
                "value": value,
                "level": status,
                # WHY: Include the threshold that was breached so the operator
                # can see how far over the limit the value is.
                "threshold": threshold[status],
                "timestamp": metric.get("timestamp", ""),
            })
            logging.warning("ALERT [%s] %s=%.2f (threshold: %.2f)",
                            status.upper(), name, value, threshold[status])

    return alerts


def apply_cooldown(alerts: list[dict], cooldown_seconds: int = 300) -> list[dict]:
    """Filter alerts to enforce a cooldown period per metric.

    WHY cooldown? -- If CPU sits at 95% for an hour, you want ONE alert,
    not 720 (one per 5-second scrape). Cooldown deduplicates by metric
    name so on-call engineers get signal, not noise.
    """
    last_alert: dict[str, datetime] = {}
    filtered: list[dict] = []

    for alert in alerts:
        name = alert["metric"]
        ts_str = alert.get("timestamp", "")

        # WHY: Gracefully handle missing or unparseable timestamps by
        # falling back to "now" so the alert is not silently dropped.
        try:
            ts = datetime.fromisoformat(ts_str)
        except (ValueError, TypeError):
            ts = datetime.now(timezone.utc)

        prev = last_alert.get(name)
        # WHY: If the same metric fired within the cooldown window, skip it.
        if prev and (ts - prev).total_seconds() < cooldown_seconds:
            continue

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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Check critical before warning | A value of 95 exceeds both a 70 warning and a 90 critical threshold. Checking critical first ensures the most severe classification wins. |
| Cooldown deduplication by metric name | In production, the same metric is scraped every few seconds. Without cooldown, a sustained breach generates hundreds of duplicate alerts, causing "alert fatigue" where engineers start ignoring pages. |
| Thresholds loaded from a separate file | Separating thresholds from code lets operations teams adjust alerting sensitivity without modifying the monitoring script. |
| Fallback to `datetime.now()` for missing timestamps | Some metric sources omit timestamps. Falling back to "now" keeps the cooldown logic working rather than crashing on a `TypeError`. |

## Alternative Approaches

### Using a class-based threshold evaluator

```python
class ThresholdEvaluator:
    def __init__(self, thresholds: dict[str, dict]):
        self.thresholds = thresholds
        self._cooldown_state: dict[str, datetime] = {}

    def evaluate(self, name: str, value: float) -> str | None:
        threshold = self.thresholds.get(name)
        if not threshold:
            return None
        if value >= threshold["critical"]:
            return "critical"
        if value >= threshold["warning"]:
            return "warning"
        return None
```

A class-based approach encapsulates cooldown state alongside evaluation logic. This is cleaner when the monitor runs as a long-lived process rather than a one-shot script.

## Common Pitfalls

1. **Checking warning before critical** — If you write `if value >= warning` first and return immediately, a value that exceeds *both* thresholds is incorrectly classified as "warning" instead of "critical." Always check the most severe condition first.
2. **No cooldown on alerts** — Without cooldown, a metric that stays above the threshold generates an alert on every evaluation cycle. This floods on-call channels and teaches engineers to ignore alerts.
3. **Thresholds where warning >= critical** — If `warning=90` and `critical=80`, every value above 80 triggers as "critical" and the warning level is unreachable. Validate that `warning < critical` when loading configuration.
