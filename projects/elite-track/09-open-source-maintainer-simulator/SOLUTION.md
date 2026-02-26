# Solution: Elite Track / Open Source Maintainer Simulator

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Open Source Maintainer Simulator.

This project is part of the elite extension track.
It intentionally emphasizes explicit, testable engineering decisions.
"""

# WHY simulate open-source maintenance? -- Maintaining OSS requires skills
# beyond coding: triaging issues, reviewing PRs from strangers, managing
# breaking changes, writing changelogs, and communicating decisions. This
# simulation exposes learners to the full maintainer workflow.

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse CLI inputs for deterministic project execution."""
    parser = argparse.ArgumentParser(description="Open Source Maintainer Simulator")
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
        # WHY is_high_risk for OSS maintenance? -- In an open-source context,
        # "warn" and "critical" map to security vulnerabilities, breaking
        # changes, and stale PRs from contributors. Low scores indicate issues
        # that need immediate maintainer attention to keep the project healthy.
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

    payload = build_summary(records, "Open Source Maintainer Simulator", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Deterministic issue/PR simulation | Maintainer decisions must be reviewable; non-deterministic input makes teach-back exercises unrepeatable | Live GitHub API integration -- realistic but rate-limited and changes between runs |
| CSV-based triage data | Each line represents an issue or PR with priority and severity; simple to generate and modify | GitHub webhook payloads -- more realistic but adds JSON parsing complexity |
| High-risk flagging for urgent items | Security vulnerabilities and breaking changes need immediate attention; flagging them teaches triage prioritization | FIFO processing -- treats all items equally, which does not match real maintainer workflow |
| JSON output as triage report | Structured output enables tracking triage decisions over time and measuring maintainer responsiveness | Markdown output -- human-readable but not automatable |

## Alternative approaches

### Approach B: Issue triage system with SLA tracking

```python
from dataclasses import dataclass, field
from enum import Enum, auto

class IssuePriority(Enum):
    CRITICAL = auto()   # Security vulnerability -- respond within 1 hour
    HIGH = auto()       # Breaking change -- respond within 1 day
    MEDIUM = auto()     # Bug report -- respond within 1 week
    LOW = auto()        # Feature request -- respond within 1 month

@dataclass
class Issue:
    issue_id: str
    title: str
    priority: IssuePriority
    author: str
    is_first_time_contributor: bool = False
    labels: list[str] = field(default_factory=list)

@dataclass
class TriageDecision:
    issue_id: str
    action: str            # "fix", "label", "close", "delegate", "needs-info"
    assigned_to: str = ""
    response_time_hours: float = 0.0

    @property
    def within_sla(self) -> bool:
        sla_hours = {
            IssuePriority.CRITICAL: 1,
            IssuePriority.HIGH: 24,
            IssuePriority.MEDIUM: 168,
            IssuePriority.LOW: 720,
        }
        # SLA check would compare response_time against priority threshold
        return True  # Simplified for illustration
```

**Trade-off:** A full triage system with SLA tracking models real maintainer workflows: prioritize security issues, welcome first-time contributors, close stale issues. It measures maintainer health (response time, resolution rate). However, the current scaffold focuses on the data pipeline pattern. The triage system is a natural "Alter it" enhancement that builds on the pipeline foundation.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Ignoring first-time contributor PRs | Contributors leave and never return; the project loses potential maintainers | Prioritize first-time PRs with welcome messages and fast reviews (< 48 hours) |
| Security vulnerability disclosed publicly | Attackers exploit it before a fix is ready; users are at risk | Use private security advisories (GitHub Security Advisories); coordinate disclosure |
| Semver major version bump without migration guide | Users cannot upgrade; they either stay on the old version or fork the project | Always publish a migration guide with breaking changes; use deprecation warnings first |
