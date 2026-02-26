# Solution: Elite Track / Event Driven Architecture Lab

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Event Driven Architecture Lab.

This project is part of the elite extension track.
It intentionally emphasizes explicit, testable engineering decisions.
"""

# WHY event-driven architecture? -- EDA decouples producers from consumers:
# services emit events without knowing who consumes them. This enables
# independent scaling, temporal decoupling, and replay-based debugging.
# Deterministic simulation lets learners study event ordering, delivery
# guarantees, and eventual consistency without running Kafka.

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse CLI inputs for deterministic project execution."""
    parser = argparse.ArgumentParser(description="Event Driven Architecture Lab")
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
        # WHY is_high_risk for events? -- In an event-driven system, "warn"
        # and "critical" map to delivery failures, ordering violations, or
        # dead-letter queue entries. Flagging these enables replay analysis.
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

    payload = build_summary(records, "Event Driven Architecture Lab", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Deterministic event simulation | Event ordering and delivery guarantees must be testable; real message brokers add non-determinism | Live Kafka/RabbitMQ -- realistic but requires infrastructure and produces flaky tests |
| Sequential event processing | Models at-least-once, in-order delivery; the simplest guarantee to reason about | Parallel consumers -- more realistic but introduces ordering complexity |
| High-risk flagging for delivery failures | Dead-letter events and ordering violations are the most critical EDA failure modes | Treat all events equally -- misses the distinction between normal flow and error paths |
| JSON output as event log | Structured event logs enable replay analysis and debugging of ordering issues | Binary event format -- more efficient but harder to inspect during learning |

## Alternative approaches

### Approach B: Pub/sub event bus with typed events

```python
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Event:
    event_type: str
    payload: dict
    sequence_number: int

class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable]] = {}
        self._log: list[Event] = []
        self._seq = 0

    def subscribe(self, event_type: str, handler: Callable) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, payload: dict) -> None:
        self._seq += 1
        event = Event(event_type, payload, self._seq)
        self._log.append(event)
        for handler in self._subscribers.get(event_type, []):
            handler(event)

    def replay(self, from_seq: int = 0) -> list[Event]:
        """Replay events from a given sequence number."""
        return [e for e in self._log if e.sequence_number >= from_seq]
```

**Trade-off:** A typed event bus with sequence numbers demonstrates core EDA patterns: pub/sub, event replay, and ordering guarantees. It enables building event-sourced systems where state is reconstructed from the event log. However, the current scaffold focuses on the data pipeline pattern first. The event bus is a natural "Alter it" enhancement that builds on the pipeline foundation.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Consumer processes events out of order | State becomes inconsistent (e.g., "order shipped" before "order created") | Use sequence numbers and enforce ordering at the consumer level |
| Duplicate events delivered | Side effects execute twice (e.g., double-charging a customer) | Make handlers idempotent: check if the event was already processed before acting |
| Event schema changes after deployment | Old consumers fail to parse new event formats | Use schema versioning and backward-compatible changes (add fields, never remove) |
