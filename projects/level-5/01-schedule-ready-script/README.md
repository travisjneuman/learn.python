# Level 5 / Project 01 - Schedule Ready Script
Home: [README](../../../README.md)

**Estimated time:** 60 minutes

## Focus
- non-interactive execution patterns

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/01-schedule-ready-script
python project.py --input data/sample_input.txt --output data/output.json --start-hour 0 --end-hour 24
pytest -q
```

## Expected terminal output
```text
{
  "processed": 5,
  "status": "completed"
}
6 passed
```

## Expected artifacts
- `data/output.json` — processed results
- `data/run.log` — execution log
- Passing tests
- Updated `notes.md`

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a script that processes files in a directory on a schedule, logging results and handling errors without human intervention.

**Step 1: Design for unattended execution.** No `input()`, no interactive prompts. Everything comes from arguments or config.

```python
import argparse
import logging
from pathlib import Path

logging.basicConfig(
    filename="process.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

def process_directory(input_dir, output_file):
    path = Path(input_dir)
    if not path.is_dir():
        logger.error("Input directory does not exist: %s", input_dir)
        return {"status": "error", "reason": "directory not found"}
    files = list(path.glob("*.txt"))
    logger.info("Found %d files to process", len(files))
    results = []
    for f in files:
        try:
            content = f.read_text()
            results.append({"file": f.name, "lines": len(content.splitlines())})
        except Exception as e:
            logger.warning("Skipping %s: %s", f.name, e)
    logger.info("Completed: %d/%d files processed", len(results), len(files))
    return {"status": "completed", "processed": len(results)}
```

**Step 2: Key design decisions.** Log to a file (not stdout) so cron/scheduler can capture it. Catch exceptions per-file so one bad file does not stop the batch. Return a status dict so the caller knows what happened.

**The thought process:** Scripts that run on a schedule must never hang waiting for input, must log everything, and must handle errors per-item. This is the same pattern the schedule-ready project uses.

## Design First
Before writing code, sketch your approach in `notes.md`:
- What functions or classes do you need?
- What data structures will you use?
- What's the flow from input to output?
- What could go wrong?

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. What resilience feature would make this script more production-ready?
2. How could the script notify someone about its results?
3. Write a test for the feature you added.

## Break it (required) — Core
1. Try running the script outside its intended conditions — what safeguards exist?
2. What happens when another instance is already running?
3. What about missing or invalid input?

## Fix it (required) — Core
1. Address a concurrency or stale-state issue you discovered.
2. Add a way to override the safety checks when needed.
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does the script use a lock file instead of checking if another process is running?
2. What is the purpose of time-window checks in scheduled scripts?
3. Why does `is_within_time_window` handle overnight windows (start > end)?
4. How would you set this up as a real cron job on Linux or Task Scheduler on Windows?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Schedule Ready Script. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to make my script work without any interactive input. Can you explain what makes a script 'schedule-ready' and what patterns to avoid?"
- "Can you explain how to set up Python logging to write to both a file and the console?"

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-alert-threshold-monitor/README.md) |
|:---|:---:|---:|
