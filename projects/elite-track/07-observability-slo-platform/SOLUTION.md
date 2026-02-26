# Solution: Elite Track / Observability SLO Platform

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
>.

---

## Complete solution

```python
"""Observability SLO Platform.

This project is part of the elite extension track.
It intentionally emphasizes explicit, testable engineering decisions.
"""

# WHY SLOs over SLAs? -- SLAs are contractual (penalties for breach). SLOs are
# internal targets set tighter than SLAs, giving teams an error budget to spend
# on velocity. When the error budget is exhausted, freeze features and fix
# reliability. This SRE pattern (from Google's SRE book) balances innovation
# with stability.

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse CLI inputs for deterministic project execution."""
    parser = argparse.ArgumentParser(description="Observability SLO Platform")
    parser.add_argument("--input", required=True, help="Path to input text data")
    parser.add_argument("--output", required=True, help="Path to output JSON summary")
    parser.add_argument("--run-id", default="manual-run", help="Optional run identifier")
    return parser.parse_args()


def load_lines(input_path: Path) -> list[str]:
    """Load normalized input lines and reject empty datasets safely."""
    if not input_path.exists():
        raise FileNotFoundError(f"input file not found: {input_path}")
    lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError("input file contains no usable lines")
    return lines


def classify_line(line: str) -> dict[str, Any]:
    """Transform one CSV-like line into structured fields with validation."""
    parts = [piece.strip() for piece in line.split(",")]
    if len(parts) != 3:
        raise ValueError(f"invalid line format (expected 3 comma fields): {line}")

    name, score_raw, severity = parts
    score = int(score_raw)
    return {
        "name": name,
        "score": score,
        "severity": severity,
        # WHY is_high_risk for SLOs? -- In an observability context, "warn"
        # and "critical" map to SLO violations (error budget consumed). Low
        # scores indicate poor SLI values. Flagging these triggers error
        # budget alerts and potential feature freezes.
        "is_high_risk": severity in {"warn", "critical"} or score < 5,
    }


def build_summary(records: list[dict[str, Any]], project_title: str, run_id: str) -> dict[str, Any]:
    """Build deterministic summary payload for testing and teach-back review."""
    high_risk_count = sum(1 for record in records if record["is_high_risk"])
    avg_score = round(sum(record["score"] for record in records) / len(records), 2)

    return {
        "project_title": project_title,
        "run_id": run_id,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "record_count": len(records),
        "high_risk_count": high_risk_count,
        "average_score": avg_score,
        "records": records,
    }


def write_summary(output_path: Path, payload: dict[str, Any]) -> None:
    """Write JSON output with parent directory creation for first-time runs."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    """Execute end-to-end project run."""
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    lines = load_lines(input_path)
    records = [classify_line(line) for line in lines]

    payload = build_summary(records, "Observability SLO Platform", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| SLO-focused rather than SLA-focused | SLOs are internal targets that teams control; SLAs are legal contracts -- SLOs drive engineering behavior | SLA monitoring only -- reactive (penalties after breach) rather than proactive (error budget management) |
| Deterministic SLI data from files | SLO calculations must be reproducible to validate alerting thresholds and error budget math | Live Prometheus/Grafana integration -- realistic but requires infrastructure |
| High-risk = SLO violation | Maps directly to the SRE concept of error budget exhaustion; high-risk records trigger the "freeze features" response | Binary pass/fail -- misses the gradient between healthy and critical |
| JSON output as SLO report | Structured data enables automated SLO dashboards and historical trend analysis | Console-only output -- not persistent, not suitable for tracking error budgets over time |

## Alternative approaches

### Approach B: Error budget calculator with burn rate alerts

```python
from dataclasses import dataclass

@dataclass
class SLODefinition:
    name: str
    target_pct: float          # e.g., 99.9
    window_days: int = 30      # rolling window

    @property
    def error_budget_pct(self) -> float:
        """Total allowed error percentage."""
        return 100.0 - self.target_pct  # e.g., 0.1% for 99.9% SLO

def compute_error_budget(slo: SLODefinition, current_good: int, current_total: int) -> dict:
    """Calculate remaining error budget."""
    actual_pct = (current_good / current_total * 100) if current_total > 0 else 100.0
    budget_total = slo.error_budget_pct
    budget_consumed = max(0, 100.0 - actual_pct)
    budget_remaining = max(0, budget_total - budget_consumed)
    burn_rate = budget_consumed / budget_total if budget_total > 0 else 0

    return {
        "slo_name": slo.name,
        "target": f"{slo.target_pct}%",
        "actual": f"{actual_pct:.3f}%",
        "budget_remaining_pct": round(budget_remaining / budget_total * 100, 1) if budget_total > 0 else 0,
        "burn_rate": round(burn_rate, 3),
        "alert": burn_rate > 1.0,  # Burning faster than budget allows
    }
```

**Trade-off:** An error budget calculator with burn rate alerts is the core SRE pattern from Google's SRE book. It quantifies exactly how much unreliability a team can tolerate and alerts when the budget is being consumed too fast. However, it requires time-series data and a rolling window implementation. The current scaffold teaches the pipeline pattern first; error budgets can be layered on as the "Alter it" enhancement.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| SLO target set too tight (e.g., 99.999%) | Error budget is tiny; normal operations consume it instantly, causing perpetual feature freezes | Start with achievable targets (99.5%) and tighten gradually based on data |
| Measuring SLIs at the wrong layer | Server-side metrics show 100% but users experience failures due to CDN/DNS issues | Measure SLIs from the user's perspective (synthetic monitoring, real user monitoring) |
| No distinction between planned and unplanned downtime | Maintenance windows consume error budget unfairly | Exclude planned maintenance from SLI calculations using maintenance window annotations |
