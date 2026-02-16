"""Level 4 project: Data Contract Enforcer.

Heavily commented intermediate template:
- structured logging,
- record transforms,
- summary metrics,
- deterministic output.
"""

from __future__ import annotations

# argparse handles command-line interfaces for script runs.
import argparse
# json serializes summary payloads.
import json
# logging records run events for debugging and audit trails.
import logging
# Path provides robust filesystem operations.
from pathlib import Path

PROJECT_LEVEL = 4
PROJECT_TITLE = "Data Contract Enforcer"
PROJECT_FOCUS = "contract validation and drift detection"


def configure_logging() -> None:
    """Initialize logging format for consistent diagnostics."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def load_items(path: Path) -> list[str]:
    """Load non-empty lines from text input file."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    raw_lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in raw_lines if line.strip()]


def build_records(items: list[str]) -> list[dict]:
    """Transform plain items into structured row dictionaries.

    We keep this separate from I/O so business logic stays testable.
    """
    records: list[dict] = []
    for idx, item in enumerate(items, start=1):
        records.append(
            {
                "row_num": idx,
                "raw_value": item,
                "normalized": item.lower().replace(" ", "_"),
                "length": len(item),
            }
        )
    return records


def build_summary(records: list[dict], elapsed_ms: int = 0) -> dict:
    """Compute aggregate metrics for transformed records."""
    lengths = [r["length"] for r in records]

    return {
        "project_title": PROJECT_TITLE,
        "project_level": PROJECT_LEVEL,
        "project_focus": PROJECT_FOCUS,
        "record_count": len(records),
        "max_length": max(lengths) if lengths else 0,
        "min_length": min(lengths) if lengths else 0,
        "elapsed_ms": elapsed_ms,
    }


def run(input_path: Path, output_path: Path) -> dict:
    """Execute end-to-end run and write summary payload."""
    items = load_items(input_path)
    records = build_records(items)
    summary = build_summary(records)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    logging.info("project=%s output=%s", PROJECT_TITLE, output_path)
    return summary


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for input/output paths."""
    parser = argparse.ArgumentParser(description="Intermediate learning project runner")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output_summary.json")
    return parser.parse_args()


def main() -> None:
    """Entrypoint wiring logging, args, run, and console output."""
    configure_logging()
    args = parse_args()

    summary = run(Path(args.input), Path(args.output))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
