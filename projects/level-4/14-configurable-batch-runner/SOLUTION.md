# Configurable Batch Runner — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 4 / Project 14 — Configurable Batch Runner.

Runs batch jobs defined in a JSON configuration file. Each job
specifies an action (count_lines, word_frequency, file_stats),
input/output paths, and optional parameters. The runner executes
jobs in sequence and reports results.
"""

from __future__ import annotations

import argparse
import json
import logging
from collections import Counter
from pathlib import Path
from typing import Any, Callable

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- job actions ----------
# Each action takes (input_path, params) and returns a result dict.


def action_count_lines(input_path: Path, params: dict) -> dict:
    """Count lines in a text file, optionally filtering by a pattern."""
    text = input_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    pattern = params.get("pattern", "")

    # WHY: Pattern filtering is optional. When present, it gives the user
    # grep-like functionality without leaving the batch runner.
    if pattern:
        matching = [line for line in lines if pattern in line]
        return {"total_lines": len(lines), "matching_lines": len(matching), "pattern": pattern}

    return {"total_lines": len(lines)}


def action_word_frequency(input_path: Path, params: dict) -> dict:
    """Count word frequencies, returning the top N words."""
    text = input_path.read_text(encoding="utf-8").lower()
    words = text.split()
    # WHY: Default top_n=10 keeps the output manageable. Users can override
    # with {"top_n": 50} in the config if they need more detail.
    top_n = params.get("top_n", 10)
    counter = Counter(words)
    return {"total_words": len(words), "top_words": counter.most_common(top_n)}


def action_file_stats(input_path: Path, params: dict) -> dict:
    """Compute basic file statistics: size, line count, char count."""
    text = input_path.read_text(encoding="utf-8")
    return {
        "size_bytes": input_path.stat().st_size,
        "line_count": len(text.splitlines()),
        "char_count": len(text),
        "word_count": len(text.split()),
    }


# WHY: A registry dict maps action names to functions. This lets users define
# jobs in JSON config files without writing Python code. Adding a new action
# is just writing a function and registering it here — no if/elif chains.
ACTIONS: dict[str, Callable[..., Any]] = {
    "count_lines": action_count_lines,
    "word_frequency": action_word_frequency,
    "file_stats": action_file_stats,
}

# ---------- batch runner ----------


def load_config(path: Path) -> dict:
    """Load a batch configuration file."""
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def run_batch(config: dict, base_dir: Path) -> list[dict]:
    """Execute all jobs in the config and return results.

    Each result includes: job_name, action, status, result/error.
    """
    jobs = config.get("jobs", [])
    results: list[dict] = []

    for job in jobs:
        name = job.get("name", "unnamed")
        action_name = job.get("action", "")
        # WHY: Resolve input paths relative to the config file's directory,
        # not the current working directory. This makes the config portable
        # — move the config and its data files together and everything works.
        input_path = base_dir / job.get("input", "")
        params = job.get("params", {})

        func = ACTIONS.get(action_name)
        if func is None:
            # WHY: Skip unknown actions instead of crashing. This lets you
            # add future action types to the config before implementing them.
            results.append({"job": name, "action": action_name, "status": "skipped", "reason": "unknown action"})
            logging.warning("Skipping job '%s': unknown action '%s'", name, action_name)
            continue

        if not input_path.exists():
            # WHY: Per-job error handling. One missing file should not
            # prevent other jobs from running.
            results.append({"job": name, "action": action_name, "status": "error", "reason": f"file not found: {input_path}"})
            logging.error("Job '%s': input file not found", name)
            continue

        try:
            result = func(input_path, params)
            results.append({"job": name, "action": action_name, "status": "ok", "result": result})
            logging.info("Job '%s' completed successfully", name)
        except Exception as exc:
            # WHY: Catch all exceptions per-job so one failing job does
            # not crash the entire batch. The error is recorded in the
            # results for later investigation.
            results.append({"job": name, "action": action_name, "status": "error", "reason": str(exc)})
            logging.error("Job '%s' failed: %s", name, exc)

    return results

# ---------- runner ----------


def run(config_path: Path, output_path: Path) -> dict:
    """Load config, run all jobs, write report."""
    config = load_config(config_path)
    base_dir = config_path.parent
    results = run_batch(config, base_dir)

    report = {
        "total_jobs": len(results),
        "succeeded": sum(1 for r in results if r["status"] == "ok"),
        "failed": sum(1 for r in results if r["status"] == "error"),
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
        "results": results,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Batch complete: %d ok, %d failed, %d skipped",
                 report["succeeded"], report["failed"], report["skipped"])
    return report

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run batch jobs from a config file")
    parser.add_argument("--config", default="data/batch_config.json")
    parser.add_argument("--output", default="data/batch_report.json")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.config), Path(args.output))
    print(json.dumps({
        "total_jobs": report["total_jobs"],
        "succeeded": report["succeeded"],
        "failed": report["failed"],
    }, indent=2))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| `ACTIONS` registry instead of `if/elif` chains | Adding a new action is a two-step process: write the function, add it to the dict. No need to touch the runner logic. This is the Open/Closed Principle — open for extension, closed for modification. |
| Per-job error handling (try/except around each job) | One failing job should not prevent the other 99 from running. Each job's result includes its own status, so you can see exactly which jobs succeeded and which failed. |
| Resolve paths relative to config file directory | Makes the config portable. If you move the config and its data directory to another machine, relative paths still work. Using the current working directory would break this. |
| Three-tier status: ok / error / skipped | "Error" means the job was attempted but failed (e.g., bad input). "Skipped" means the job was not attempted (e.g., unknown action). Different problems require different fixes. |

## Alternative Approaches

### Using a plugin system with dynamic imports

```python
import importlib

def load_action(module_path: str, func_name: str):
    module = importlib.import_module(module_path)
    return getattr(module, func_name)

# Config: {"action": "my_actions.count_lines"}
func = load_action("my_actions", "count_lines")
```

**Trade-off:** Dynamic imports let users add new actions without modifying the runner's source code — they just drop a Python file in a directory and reference it in the config. However, this introduces security risks (arbitrary code execution from config) and debugging difficulty (import errors at runtime). The static registry is safer and simpler for a learning project.

### Using `subprocess` to run external scripts as jobs

```python
import subprocess

def action_run_script(input_path: Path, params: dict) -> dict:
    cmd = params.get("command", "")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {"returncode": result.returncode, "stdout": result.stdout}
```

**Trade-off:** Running external scripts gives maximum flexibility — any language, any tool. But `shell=True` is a security risk, subprocess management is complex, and error handling is harder. For a data processing batch runner, keeping actions as Python functions is safer and more debuggable.

## Common Pitfalls

1. **Using `if/elif` chains for action dispatch** — Adding the 10th action means editing a growing chain of conditionals. If you misspell an action name in the chain, you get a silent bug. The registry pattern catches unknown actions explicitly.
2. **Not handling the empty config case** — A config with `"jobs": []` should produce a valid report with zero jobs, not crash. The loop simply runs zero times, which is correct, but the report should still be written.
3. **Broad `except Exception` hiding bugs** — Catching all exceptions per job is necessary for resilience, but it can hide programming errors (like typos in variable names). In development, consider logging the full traceback with `logging.exception()` to preserve debugging context.
