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

    if pattern:
        matching = [line for line in lines if pattern in line]
        return {"total_lines": len(lines), "matching_lines": len(matching), "pattern": pattern}

    return {"total_lines": len(lines)}


def action_word_frequency(input_path: Path, params: dict) -> dict:
    """Count word frequencies, returning the top N words."""
    text = input_path.read_text(encoding="utf-8").lower()
    words = text.split()
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


# Registry of available actions
ACTIONS: dict[str, callable] = {
    "count_lines": action_count_lines,
    "word_frequency": action_word_frequency,
    "file_stats": action_file_stats,
}

# ---------- batch runner ----------


def load_config(path: Path) -> dict:
    """Load a batch configuration file.

    Expected format:
    {
      "jobs": [
        {"name": "job1", "action": "count_lines", "input": "data/file.txt", "params": {}},
        ...
      ]
    }
    """
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
        input_path = base_dir / job.get("input", "")
        params = job.get("params", {})

        func = ACTIONS.get(action_name)
        if func is None:
            results.append({"job": name, "action": action_name, "status": "skipped", "reason": "unknown action"})
            logging.warning("Skipping job '%s': unknown action '%s'", name, action_name)
            continue

        if not input_path.exists():
            results.append({"job": name, "action": action_name, "status": "error", "reason": f"file not found: {input_path}"})
            logging.error("Job '%s': input file not found", name)
            continue

        try:
            result = func(input_path, params)
            results.append({"job": name, "action": action_name, "status": "ok", "result": result})
            logging.info("Job '%s' completed successfully", name)
        except Exception as exc:
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
