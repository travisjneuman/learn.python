"""Level 6 learning project: Sql Query Runner.

This version introduces stronger structure (logging, transforms, summary)
while keeping comments explicit for intermediate learners.
"""

from __future__ import annotations

# argparse handles command-line options.
import argparse
# json lets us serialize structured output.
import json
# logging gives runtime visibility for troubleshooting.
import logging
# Path manages file paths safely across operating systems.
from pathlib import Path

# Metadata constants included in output for traceability.
PROJECT_LEVEL = 6
PROJECT_NAME = "Sql Query Runner"


def configure_logging() -> None:
    """Set a basic logging format for readable run diagnostics."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def load_lines(path: Path) -> list[str]:
    """Load non-empty input lines from disk.

    This function is intentionally small and testable.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    raw_lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in raw_lines if line.strip()]


def transform(lines: list[str]) -> list[dict]:
    """Convert plain lines into record dictionaries.

    Each output record includes:
    - row number,
    - original value,
    - computed length.
    """
    records: list[dict] = []
    for idx, line in enumerate(lines, start=1):
        records.append(
            {
                "row_num": idx,
                "value": line,
                "length": len(line),
            }
        )
    return records


def summarize(records: list[dict]) -> dict:
    """Build a compact summary of transformed records."""
    lengths = [r["length"] for r in records]

    return {
        "project_name": PROJECT_NAME,
        "project_level": PROJECT_LEVEL,
        "record_count": len(records),
        # Guard for empty lists to avoid ValueError on max/min.
        "max_length": max(lengths) if lengths else 0,
        "min_length": min(lengths) if lengths else 0,
    }


def run(input_path: Path, output_path: Path) -> dict:
    """Execute one full project run and write summary output."""
    lines = load_lines(input_path)
    records = transform(lines)
    summary = summarize(records)

    # Ensure output directory exists for first-time runs.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    logging.info("Wrote summary to %s", output_path)
    return summary


def parse_args() -> argparse.Namespace:
    """Define command-line interface for this project."""
    parser = argparse.ArgumentParser(description="Learning project runner")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output_summary.json")
    return parser.parse_args()


def main() -> None:
    """Entrypoint that wires together logging, args, run, and console output."""
    configure_logging()
    args = parse_args()

    summary = run(Path(args.input), Path(args.output))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
