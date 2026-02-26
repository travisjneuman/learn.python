# Schedule-Ready Script — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 30 minutes attempting it independently.

## Thinking Process

This project teaches you how to write scripts that run without human supervision. Everything you have built so far assumed a human was at the keyboard: they start the script, they read the output, they handle errors. A schedule-ready script runs at 3 AM via cron or Task Scheduler while you sleep. If it crashes, nobody is there to restart it. If two copies run simultaneously, they might corrupt each other's output.

Three patterns make a script schedule-ready: **time-window checks** (should the script run right now?), **lock files** (is another copy already running?), and **structured exit codes** (did it succeed or fail?). Think of these as the safety rails that prevent a scheduled script from causing damage.

Before coding, think about all the ways a scheduled run can go wrong. The input file might be missing. The previous run might still be going. It might be a holiday when no data is expected. The script needs to handle all of these gracefully -- log what happened and exit cleanly, rather than crashing with an unhandled exception.

## Step 1: Set Up File-Based Logging

**What to do:** Configure logging to write to both a file and the console.

**Why:** When a script runs at 3 AM, `print()` output goes nowhere useful. File-based logging creates a permanent record of what happened. Console output is still useful during manual testing. Configuring both at once covers both use cases.

```python
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
```

The timestamp in the format string is critical. Without it, you cannot tell when each log entry was produced, which makes debugging scheduled runs nearly impossible.

**Predict:** Why does the code create the log file's parent directory with `mkdir(parents=True, exist_ok=True)`? What would happen on a fresh system without that line?

## Step 2: Implement Time-Window Checks

**What to do:** Write a function that determines whether the current time falls within an allowed execution window.

**Why:** Many scheduled scripts should only run during certain hours (e.g., after business hours when the database is less busy). The time-window check lets the script skip execution gracefully instead of running when it should not.

```python
def is_within_time_window(now: datetime, start_hour: int, end_hour: int) -> bool:
    hour = now.hour
    if start_hour <= end_hour:
        return start_hour <= hour < end_hour
    # Window wraps past midnight (e.g., 22:00 to 06:00)
    return hour >= start_hour or hour < end_hour
```

The midnight-wrapping logic is the tricky part. A window from 22:00 to 06:00 means "10 PM to 6 AM." The hour is valid if it is >= 22 OR < 6. Without this handling, an overnight window would never match.

**Predict:** For `start_hour=22, end_hour=6`, is 23:00 within the window? Is 03:00? Is 12:00? Work through each case.

## Step 3: Implement Lock File Protection

**What to do:** Write `acquire_lock()` and `release_lock()` functions that prevent two copies of the script from running simultaneously.

**Why:** If a script is scheduled every 5 minutes but sometimes takes 8 minutes, two copies will overlap. Without a lock, both might write to the same output file, producing garbage. The lock file acts as a mutex (mutual exclusion).

```python
def acquire_lock(lock_path: Path) -> bool:
    if lock_path.exists():
        age_seconds = (datetime.now(timezone.utc).timestamp()
                       - lock_path.stat().st_mtime)
        if age_seconds < 3600:
            return False  # Lock is active
        logging.warning("Removing stale lock file (age: %.0fs)", age_seconds)

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(
        json.dumps({"pid": "simulated", "locked_at": datetime.now(timezone.utc).isoformat()}),
        encoding="utf-8",
    )
    return True

def release_lock(lock_path: Path) -> None:
    if lock_path.exists():
        lock_path.unlink()
```

Two important details:

- **Stale lock detection**: If the previous run crashed without releasing the lock, the lock file stays. Treating locks older than 1 hour as stale provides automatic recovery.
- **Lock content**: Writing a timestamp (and potentially PID) to the lock file helps debugging -- you can see when the lock was created.

**Predict:** What happens if the process crashes between `acquire_lock()` and `release_lock()`? How does the stale lock detection solve this?

## Step 4: Write the Payload Work Function

**What to do:** Write a `do_work()` function that contains the actual processing logic, separated from all the scheduling infrastructure.

**Why:** Separating "the work" from "the scheduling scaffolding" means you can test the work function independently. It also makes it easy to swap in different payloads while keeping the same scheduling infrastructure.

```python
def do_work(input_path: Path, output_path: Path) -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    lines = [l.strip() for l in input_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    results = [{"line": i + 1, "content": line, "length": len(line)}
               for i, line in enumerate(lines)]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return {"processed": len(results)}
```

**Predict:** Why does this function raise `FileNotFoundError` instead of returning an error dict? How is the exception handled by the caller?

## Step 5: Orchestrate with Full Safety Checks

**What to do:** Write a `run()` function that performs all safety checks (time window, skip days, lock) before calling the work function.

**Why:** This is the orchestrator that ties all the safety patterns together. Each check returns early with a status dict if the condition is not met, so the work only runs when all conditions are satisfied.

```python
def run(input_path, output_path, lock_path, now=None,
        start_hour=0, end_hour=24, skip_days=None):
    now = now or datetime.now(timezone.utc)
    skip_days = skip_days or []

    if not is_within_time_window(now, start_hour, end_hour):
        logging.info("Outside time window, skipping")
        return {"status": "skipped", "reason": "outside_time_window"}

    if is_skip_day(now, skip_days):
        logging.info("Today is a skip day, skipping")
        return {"status": "skipped", "reason": "skip_day"}

    if not acquire_lock(lock_path):
        logging.warning("Lock file exists — another instance may be running")
        return {"status": "skipped", "reason": "locked"}

    try:
        result = do_work(input_path, output_path)
        result["status"] = "completed"
        return result
    except Exception as exc:
        logging.error("Run failed: %s", exc)
        return {"status": "failed", "error": str(exc)}
    finally:
        release_lock(lock_path)
```

Notice the `try/finally` block: `release_lock` runs whether the work succeeds or fails. Without `finally`, a failed run would leave a lock file that blocks future runs.

**Predict:** Why does the function accept `now` as a parameter instead of always calling `datetime.now()`? (Hint: think about testing.)

## Step 6: Use Structured Exit Codes

**What to do:** In `main()`, translate the result status into a process exit code.

**Why:** Schedulers like cron and Windows Task Scheduler use exit codes to determine whether a run succeeded. Exit code 0 means success; any non-zero value means something went wrong. This lets the scheduler send alerts on failure.

```python
def main():
    # ... parse args, configure logging, run ...
    result = run(...)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("status") == "completed" else 1)
```

**Predict:** If the script is outside its time window and returns `"status": "skipped"`, the exit code is 1. Should the scheduler treat this as a failure? This is a design decision -- in some setups, "skipped" is expected and should not trigger alerts.

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Using `input()` or interactive prompts | Habit from interactive scripts | All input comes from arguments or config files |
| Forgetting to release the lock on failure | Only releasing in the happy path | Use `try/finally` to guarantee release |
| No stale lock detection | Lock from a crashed run blocks all future runs | Check lock file age and remove if older than threshold |
| Logging to stdout only | No record of what happened at 3 AM | Always log to a file alongside the console |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
6 passed
```

Test from the command line:

```bash
python project.py --input data/sample_input.txt --output data/output.json --start-hour 0 --end-hour 24
```

Check `data/run.log` afterward to see the structured log output.

## What You Learned

- **Lock files** prevent concurrent execution of the same script. Combined with stale-lock detection, they handle both normal operation and crash recovery.
- **Time-window checks** let scripts skip execution outside their intended hours, including overnight windows that wrap past midnight.
- **Structured exit codes** communicate success or failure to the scheduler, enabling automated alerting and retry logic.
