"""Level 5 / Project 13 — Operational Run Logger.

Structured operational logging with run IDs, timestamps, duration
tracking, and JSON-formatted output.  Every operation is tracked
from start to finish with a unique run identifier.

Concepts practiced:
- Lifecycle tracking (start -> process -> finish)
- UUID-based run identification for traceability
- Duration measurement with timezone-aware datetimes
- Error handling that still records partial run data
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
    """Set up logging so every run event is traceable."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


# ---------- run logger ----------


class RunLogger:
    """Context-aware logger that tracks run metadata.

    Each run has a unique ID, a start time, and a list of events.
    Call ``finish()`` at the end to record the final status and
    compute the total duration.
    """

    def __init__(self, run_id: str | None = None) -> None:
        self.run_id = run_id or str(uuid.uuid4())[:8]
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
        """Record an error event and increment the error counter."""
        self.error_count += 1
        self.log_event("error", {"message": message, **(details or {})})

    def log_warning(self, message: str, details: dict | None = None) -> None:
        """Record a non-fatal warning event."""
        self.log_event("warning", {"message": message, **(details or {})})

    def finish(self, status: str = "completed") -> dict:
        """Finalise the run: compute duration and return the full summary.

        The summary includes the run ID, status, timing information,
        event count, error count, and the complete event list.
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

    Each item is recorded as a separate event so the run log
    provides full visibility into what was processed and in
    what order.
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
    """Execute a full logged run: read input, process, write output and log.

    Even if an error occurs, the run logger's ``finish()`` is always
    called so that partial run data is persisted for debugging.
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

    # Always write the run log, even on failure.
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the operational run logger."""
    parser = argparse.ArgumentParser(
        description="Operational run logger with lifecycle tracking",
    )
    parser.add_argument("--input", default="data/sample_input.txt", help="Input text file")
    parser.add_argument("--output", default="data/processed.json", help="Processed output path")
    parser.add_argument("--log", default="data/run_log.json", help="Run log output path")
    parser.add_argument("--run-id", default=None, help="Custom run ID (auto-generated if omitted)")
    return parser.parse_args()


def main() -> None:
    """Entry point: configure logging, parse args, execute the run."""
    configure_logging()
    args = parse_args()
    summary = run(Path(args.input), Path(args.output), Path(args.log), args.run_id)
    print(json.dumps(
        {"run_id": summary["run_id"], "status": summary["status"], "events": summary["event_count"]},
        indent=2,
    ))


if __name__ == "__main__":
    main()
