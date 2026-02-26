"""Level 5 / Project 01 — Schedule-Ready Script.

A script designed to run non-interactively (e.g., via cron or Task
Scheduler). Features: time-window checks, lock files to prevent
overlapping runs, structured exit codes, and run logging.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------- logging ----------

def configure_logging(log_path: Path | None = None) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_path, encoding="utf-8"))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=handlers,
    )

# ---------- scheduling helpers ----------


def is_within_time_window(
    now: datetime,
    start_hour: int,
    end_hour: int,
) -> bool:
    """Check if current time is within the allowed execution window.

    Window wraps around midnight: start=22, end=6 means 10 PM to 6 AM.
    """
    hour = now.hour
    if start_hour <= end_hour:
        return start_hour <= hour < end_hour
    # Window wraps past midnight
    return hour >= start_hour or hour < end_hour


def is_skip_day(now: datetime, skip_days: list[int]) -> bool:
    """Check if today's weekday (0=Monday) is in the skip list."""
    return now.weekday() in skip_days


def acquire_lock(lock_path: Path) -> bool:
    """Try to create a lock file. Returns False if already locked.

    WHY a lock file? -- When a script is scheduled (e.g., every 5 minutes
    via cron) but sometimes takes longer than 5 minutes, two instances
    can overlap and corrupt shared output files. A lock file acts as a
    mutex: the second instance sees the lock and exits immediately.
    """
    if lock_path.exists():
        # WHY check staleness? -- If the previous run crashed without
        # releasing the lock, we'd be permanently blocked. Treating
        # locks older than 1 hour as stale provides automatic recovery.
        age_seconds = (datetime.now(timezone.utc).timestamp()
                       - lock_path.stat().st_mtime)
        if age_seconds < 3600:
            return False
        logging.warning("Removing stale lock file (age: %.0fs)", age_seconds)

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(
        json.dumps({"pid": "simulated", "locked_at": datetime.now(timezone.utc).isoformat()}),
        encoding="utf-8",
    )
    return True


def release_lock(lock_path: Path) -> None:
    """Remove the lock file after a successful run."""
    if lock_path.exists():
        lock_path.unlink()

# ---------- the actual work ----------


def do_work(input_path: Path, output_path: Path) -> dict:
    """The payload work this script is scheduled to do.

    Reads input lines, processes them, writes output.
    Replace this with your actual batch logic.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    lines = [l.strip() for l in input_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    results = [{"line": i + 1, "content": line, "length": len(line)} for i, line in enumerate(lines)]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return {"processed": len(results)}

# ---------- runner ----------


def run(
    input_path: Path,
    output_path: Path,
    lock_path: Path,
    now: datetime | None = None,
    start_hour: int = 0,
    end_hour: int = 24,
    skip_days: list[int] | None = None,
) -> dict:
    """Full scheduled run with all safety checks."""
    now = now or datetime.now(timezone.utc)
    skip_days = skip_days or []

    # Check time window
    if not is_within_time_window(now, start_hour, end_hour):
        logging.info("Outside time window (%d:00-%d:00), skipping", start_hour, end_hour)
        return {"status": "skipped", "reason": "outside_time_window"}

    # Check skip days
    if is_skip_day(now, skip_days):
        logging.info("Today is a skip day (weekday=%d), skipping", now.weekday())
        return {"status": "skipped", "reason": "skip_day"}

    # Acquire lock
    if not acquire_lock(lock_path):
        logging.warning("Lock file exists — another instance may be running")
        return {"status": "skipped", "reason": "locked"}

    try:
        result = do_work(input_path, output_path)
        result["status"] = "completed"
        logging.info("Run completed: %s", result)
        return result
    except Exception as exc:
        logging.error("Run failed: %s", exc)
        return {"status": "failed", "error": str(exc)}
    finally:
        release_lock(lock_path)

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Schedule-ready batch script")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    parser.add_argument("--lock", default="data/.run.lock")
    parser.add_argument("--log", default="data/run.log")
    parser.add_argument("--start-hour", type=int, default=0)
    parser.add_argument("--end-hour", type=int, default=24)
    parser.add_argument("--skip-days", default="", help="Comma-separated weekdays to skip (0=Mon)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_logging(Path(args.log))
    skip = [int(d) for d in args.skip_days.split(",") if d.strip()]
    result = run(
        Path(args.input), Path(args.output), Path(args.lock),
        start_hour=args.start_hour, end_hour=args.end_hour, skip_days=skip,
    )
    print(json.dumps(result, indent=2))
    # WHY structured exit codes? -- Schedulers like cron and Task Scheduler
    # use exit codes to decide whether to send failure notifications.
    # 0 = success, non-zero = something went wrong.
    sys.exit(0 if result.get("status") == "completed" else 1)


if __name__ == "__main__":
    main()
