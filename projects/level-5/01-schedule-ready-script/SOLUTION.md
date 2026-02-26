# Schedule Ready Script — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
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

# WHY: A schedule-ready script runs unattended, so all output must go to a
# log file. We also keep a StreamHandler for development/debugging.
def configure_logging(log_path: Path | None = None) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_path:
        # WHY: Create parent dirs automatically so the script works on first run
        # without requiring manual directory setup.
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
    """Check if current time is within the allowed execution window."""
    hour = now.hour
    # WHY: When start <= end (e.g. 9-17), the window is a simple range check.
    if start_hour <= end_hour:
        return start_hour <= hour < end_hour
    # WHY: When start > end (e.g. 22-6), the window wraps past midnight.
    # In that case, any hour >= start OR < end is valid.
    return hour >= start_hour or hour < end_hour


def is_skip_day(now: datetime, skip_days: list[int]) -> bool:
    """Check if today's weekday (0=Monday) is in the skip list."""
    # WHY: Some scripts should not run on weekends or specific days.
    # Using Python's weekday() convention (0=Mon) matches ISO 8601.
    return now.weekday() in skip_days


def acquire_lock(lock_path: Path) -> bool:
    """Try to create a lock file. Returns False if already locked.

    WHY a lock file? -- When a script is scheduled (e.g., every 5 minutes
    via cron) but sometimes takes longer than 5 minutes, two instances
    can overlap and corrupt shared output files. A lock file acts as a
    mutex: the second instance sees the lock and exits immediately.
    """
    if lock_path.exists():
        # WHY: Check staleness so a crashed run does not permanently block
        # all future runs. Locks older than 1 hour are considered stale.
        age_seconds = (datetime.now(timezone.utc).timestamp()
                       - lock_path.stat().st_mtime)
        if age_seconds < 3600:
            return False
        logging.warning("Removing stale lock file (age: %.0fs)", age_seconds)

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    # WHY: Write PID and timestamp into the lock so operators can debug
    # which process holds it and when it was acquired.
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
    """The payload work this script is scheduled to do."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    # WHY: Strip blank lines to avoid counting them as real data.
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

    # WHY: Check constraints in order of cheapness — time window and skip day
    # are free checks that avoid doing any I/O if the script should not run.
    if not is_within_time_window(now, start_hour, end_hour):
        logging.info("Outside time window (%d:00-%d:00), skipping", start_hour, end_hour)
        return {"status": "skipped", "reason": "outside_time_window"}

    if is_skip_day(now, skip_days):
        logging.info("Today is a skip day (weekday=%d), skipping", now.weekday())
        return {"status": "skipped", "reason": "skip_day"}

    if not acquire_lock(lock_path):
        logging.warning("Lock file exists — another instance may be running")
        return {"status": "skipped", "reason": "locked"}

    # WHY: try/finally ensures the lock is always released, even on errors.
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
    # WHY: Structured exit codes let schedulers like cron detect failures
    # and send notifications. 0 = success, non-zero = something went wrong.
    sys.exit(0 if result.get("status") == "completed" else 1)


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Lock file instead of process checking | Lock files work across reboots and are simpler than querying the OS process table. They also work when the script is run from different user accounts. |
| Stale lock auto-cleanup (1 hour) | If a previous run crashed without releasing its lock, all future runs would be permanently blocked. Auto-cleanup provides self-healing. |
| Time window with midnight wraparound | Overnight maintenance windows (e.g., 22:00-06:00) are common in operations. Handling wraparound makes the function usable for any schedule. |
| try/finally around lock release | Guarantees the lock is freed even when `do_work` raises an exception, preventing orphaned locks. |
| Structured exit codes (0/1) | Schedulers like cron and Task Scheduler use exit codes to decide whether to send alerts. Returning meaningful codes enables automated monitoring. |

## Alternative Approaches

### Using a decorator for the lock

```python
from contextlib import contextmanager

@contextmanager
def file_lock(lock_path: Path):
    if not acquire_lock(lock_path):
        raise RuntimeError("Already locked")
    try:
        yield
    finally:
        release_lock(lock_path)

# Usage:
with file_lock(Path("data/.run.lock")):
    do_work(input_path, output_path)
```

This is cleaner when you have multiple functions that need locking. The context manager pattern makes it impossible to forget to release the lock.

### Using `fcntl.flock` (Unix) or `msvcrt.locking` (Windows)

Operating-system-level file locks are more robust than lock files because the OS automatically releases them if the process crashes. However, they are platform-specific and harder to debug (you cannot inspect them with `ls`).

## Common Pitfalls

1. **Forgetting to release the lock on error** — If the lock is acquired but the script crashes before `release_lock`, all future runs are blocked until the stale timeout expires. Always use try/finally or a context manager.
2. **Using `input()` in a scheduled script** — Any call that waits for user input will cause the script to hang indefinitely when run by cron or Task Scheduler. All configuration must come from arguments, config files, or environment variables.
3. **Not logging to a file** — When a script runs unattended, stdout/stderr may be discarded. Without file-based logging, debugging production failures becomes nearly impossible.
