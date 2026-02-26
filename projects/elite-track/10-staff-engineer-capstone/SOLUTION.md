# Solution: Elite Track / Staff Engineer Capstone

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Staff Engineer Capstone.

This project is part of the elite extension track.
It intentionally emphasizes explicit, testable engineering decisions.
"""

# WHY a staff engineer capstone? -- Staff+ engineering is about system-level
# thinking: making decisions that affect multiple teams, balancing technical
# debt against feature velocity, and building platforms that scale organizational
# output. This capstone integrates all prior elite track concepts into a
# single system design exercise.

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse CLI inputs for deterministic project execution."""
    parser = argparse.ArgumentParser(description="Staff Engineer Capstone")
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
        # WHY is_high_risk for system design? -- In a staff engineer context,
        # "warn" and "critical" map to architectural risks: high coupling,
        # single points of failure, scalability bottlenecks. Low scores
        # indicate areas where system-level decisions need to be made.
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

    payload = build_summary(records, "Staff Engineer Capstone", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Integrative capstone that touches all prior domains | Staff engineers must synthesize across security, reliability, performance, and operations | Deep-dive into a single domain -- does not exercise the cross-cutting system-level thinking |
| Deterministic pipeline as the foundation | Every concept from the elite track (algorithms, concurrency, caching, auth, profiling, events, SLOs, compliance, OSS) can be expressed through this pipeline | Free-form design exercise -- harder to evaluate and compare across learners |
| Risk scoring across domains | System-level thinking requires seeing risk holistically; a single high-risk item in security affects the entire system | Per-domain scoring -- more detailed but misses cross-domain interactions |
| JSON evidence for decision documentation | Staff engineers must document and defend their decisions; structured output enables review and critique | Presentation slides -- less rigorous, harder to version-control |

## Alternative approaches

### Approach B: Architecture Decision Record (ADR) generator

```python
from dataclasses import dataclass
from datetime import date

@dataclass
class ADR:
    """Architecture Decision Record -- documents a key technical decision."""
    number: int
    title: str
    status: str             # "proposed", "accepted", "deprecated", "superseded"
    context: str            # What is the issue that motivated this decision?
    decision: str           # What is the change that is being proposed?
    consequences: list[str] # What becomes easier or harder because of this decision?
    date: str = ""

    def __post_init__(self):
        if not self.date:
            self.date = date.today().isoformat()

    def to_markdown(self) -> str:
        consequences = "\n".join(f"- {c}" for c in self.consequences)
        return f"""# ADR-{self.number:04d}: {self.title}

**Status:** {self.status}
**Date:** {self.date}

## Context
{self.context}

## Decision
{self.decision}

## Consequences
{consequences}
"""
```

**Trade-off:** ADR generation is a core staff engineer skill -- documenting decisions with context, alternatives, and consequences ensures institutional knowledge survives team changes. However, it is a documentation exercise rather than a systems engineering exercise. The pipeline capstone tests both the technical foundation (data processing, validation, output) and the ability to reason about system-level tradeoffs through the "Explain it" section.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Optimizing for a single quality attribute (e.g., performance) | Other attributes degrade (reliability, security, maintainability); the system becomes fragile | Use architecture fitness functions to track multiple attributes simultaneously |
| Making decisions without documenting context | When the original team leaves, the next team does not understand why decisions were made and reverses them | Write ADRs for every significant technical decision; store them in the repository |
| Scope creep in system design | Trying to solve every problem at once leads to an unshippable monolith | Define clear boundaries and milestones; ship incrementally and validate at each stage |
