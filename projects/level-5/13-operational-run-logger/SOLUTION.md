# Operational Run Logger — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 5 / Project 13 — Operational Run Logger.

Structured operational logging with run IDs, timestamps, duration
tracking, and JSON-formatted output.
"""

from __future__ import annotations

import argparse
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- run logger ----------

class RunLogger:
    """Context-aware logger that tracks run metadata.

    WHY a dedicated class instead of plain logging? -- Standard logging
    writes lines to a file and forgets them. RunLogger collects every
    event into a structured list with timing data, so the complete run
    history can be serialized to JSON and queried programmatically
    (e.g., "show me all runs that took longer than 5 seconds").
    """

    def __init__(self, run_id: str | None = None) -> None:
        # WHY: UUID-based run IDs let you trace a specific execution
        # across logs, outputs, and monitoring dashboards. Truncating
        # to 8 characters keeps IDs human-readable while still being
        # unique enough for practical use.
        self.run_id = run_id or str(uuid.uuid4())[:8]
        # WHY: timezone.utc ensures consistent timestamps regardless of
        # which machine or timezone the script runs in.
        self.start_time = datetime.now(timezone.utc)
        self.events: list[dict] = []
        self.error_count = 0
        self.log_event("run_started", {"run_id": self.run_id})

    def log_event(self, event_type: str, data: dict | None = None) -> None:
        """Record a timestamped event in the run log."""
        event = {
            "run_id": self.run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "data": data or {},
        }
        self.events.append(event)
        logging.info("[%s] %s: %s", self.run_id, event_type, data)

    def log_error(self, message: str, details: dict | None = None) -> None:
        """Record an error event and increment the error counter.

        WHY separate from log_event? -- Errors need a counter so the
        summary can report "3 errors occurred" without the caller
        needing to filter events by type.
        """
        self.error_count += 1
        self.log_event("error", {"message": message, **(details or {})})

    def log_warning(self, message: str, details: dict | None = None) -> None:
        """Record a non-fatal warning event."""
        self.log_event("warning", {"message": message, **(details or {})})

    def finish(self, status: str = "completed") -> dict:
        """Finalize the run: compute duration and return the full summary.

        WHY compute duration here? -- Measuring wall-clock time from
        start to finish captures the total run duration including I/O
        waits, which is what operators care about for SLA monitoring.
        """
        end_time = datetime.now(timezone.utc)
        duration_ms = int((end_time - self.start_time).total_seconds() * 1000)
        self.log_event(
            "run_finished",
            {"status": status, "duration_ms": duration_ms, "errors": self.error_count},
        )
        return {
            "run_id": self.run_id,
            "status": status,
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_ms": duration_ms,
            "event_count": len(self.events),
            "error_count": self.error_count,
            "events": self.events,
        }

# ---------- processing ----------

def process_items(items: list[str], logger: RunLogger) -> list[dict]:
    """Process a list of text items while logging each step.

    WHY log every item? -- In production, when a batch job fails at
    item 47 of 100, the run log shows exactly which items were
    processed successfully and where it stopped.
    """
    results: list[dict] = []
    logger.log_event("processing_started", {"item_count": len(items)})

    for i, item in enumerate(items):
        logger.log_event(
            "item_processed",
            {"index": i, "item": item, "length": len(item)},
        )
        results.append({"index": i, "item": item, "processed": True})

    logger.log_event("processing_completed", {"results_count": len(results)})
    return results

# ---------- pipeline ----------

def run(
    input_path: Path,
    output_path: Path,
    log_path: Path,
    run_id: str | None = None,
) -> dict:
    """Execute a full logged run.

    WHY try/except with finally-like behavior? -- Even if processing
    fails, the run logger's finish() is called so that partial run
    data is persisted for debugging. The "failed" status in the log
    tells operators something went wrong.
    """
    logger = RunLogger(run_id=run_id)

    try:
        if not input_path.exists():
            raise FileNotFoundError(f"Input not found: {input_path}")

        raw = input_path.read_text(encoding="utf-8")
        items = [line.strip() for line in raw.splitlines() if line.strip()]

        if not items:
            logger.log_warning("Input file is empty — 0 items to process")

        results = process_items(items, logger)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
        summary = logger.finish("completed")
    except Exception as exc:
        logger.log_error(str(exc))
        summary = logger.finish("failed")

    # WHY: Always write the run log, even on failure. A missing run log
    # for a failed run makes debugging nearly impossible.
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary

# ---------- CLI ----------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Operational run logger with lifecycle tracking")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/processed.json")
    parser.add_argument("--log", default="data/run_log.json")
    parser.add_argument("--run-id", default=None)
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    summary = run(Path(args.input), Path(args.output), Path(args.log), args.run_id)
    print(json.dumps(
        {"run_id": summary["run_id"], "status": summary["status"], "events": summary["event_count"]},
        indent=2,
    ))

if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| UUID-based run IDs (truncated to 8 chars) | Unique IDs let you correlate a run across logs, output files, and monitoring dashboards. 8 hex characters give ~4 billion unique values, which is enough for practical use while staying human-readable. |
| Structured events list (not just log lines) | JSON events can be queried programmatically: "find all runs where duration_ms > 5000" or "count errors by type." Plain log lines require regex parsing. |
| Always write the run log, even on failure | When a job fails, the run log is the primary debugging tool. If the log is only written on success, failed runs leave no trace. |
| Separate `log_error` from `log_event` | The error counter in the summary (`error_count: 3`) gives operators a quick severity signal without scanning the full event list. |

## Alternative Approaches

### Using a context manager for run lifecycle

```python
from contextlib import contextmanager

@contextmanager
def tracked_run(run_id=None):
    logger = RunLogger(run_id=run_id)
    try:
        yield logger
        logger.finish("completed")
    except Exception as exc:
        logger.log_error(str(exc))
        logger.finish("failed")
        raise

# Usage:
with tracked_run("demo-001") as logger:
    logger.log_event("processing", {"items": 10})
    process_items(items, logger)
```

A context manager guarantees `finish()` is always called, even on exceptions. The `yield` pattern makes the lifecycle explicit and prevents forgetting to call `finish()`.

## Common Pitfalls

1. **Forgetting to call `finish()` on error** — If processing raises an exception and `finish()` is never called, the run log has no end time, duration, or status. Always use try/except to ensure `finish()` runs.
2. **Using local time instead of UTC** — `datetime.now()` returns local time, which changes with timezones and daylight saving. `datetime.now(timezone.utc)` gives consistent timestamps that can be compared across machines.
3. **Logging too much detail per item** — Logging every item works for small batches, but a 1-million-row ETL job would produce a 1-million-entry event list. In production, log summary events (every 1000 items) instead of per-item events.
