"""Level 2 project: Mock API Response Parser.

Heavily commented beginner-friendly script:
- read input lines,
- build a small summary,
- write output JSON.
"""

from __future__ import annotations

# argparse lets the user pass --input and --output paths from terminal.
import argparse
# json writes structured output you can inspect and diff.
import json
# Path is safer than plain strings for file paths.
from pathlib import Path

# Metadata constants for traceability in output files.
PROJECT_LEVEL = 2
PROJECT_TITLE = "Mock API Response Parser"
PROJECT_FOCUS = "parse response-like payloads"


def load_items(path: Path) -> list[str]:
    """Load non-empty lines from input file.

    This function is isolated so it can be tested independently.
    """
    # Explicit missing-file check gives clearer beginner feedback.
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    # Read text and split into individual lines.
    raw_lines = path.read_text(encoding="utf-8").splitlines()

    # Keep only lines with content after trimming spaces.
    cleaned = [line.strip() for line in raw_lines if line.strip()]
    return cleaned


def build_summary(items: list[str]) -> dict:
    """Build a simple dictionary summary from the input items."""
    # Count total rows after cleanup.
    total_items = len(items)

    # Count unique values to quickly spot duplicates.
    unique_items = len(set(items))

    # Provide a short preview so learners can see sample values.
    preview = items[:5]

    return {
        "project_title": PROJECT_TITLE,
        "project_level": PROJECT_LEVEL,
        "project_focus": PROJECT_FOCUS,
        "total_items": total_items,
        "unique_items": unique_items,
        "preview": preview,
    }


def parse_args() -> argparse.Namespace:
    """Define and parse command-line options."""
    parser = argparse.ArgumentParser(description="Beginner learning project runner")

    # Input path defaults to bundled sample input file.
    parser.add_argument("--input", default="data/sample_input.txt")

    # Output path defaults to bundled output location.
    parser.add_argument("--output", default="data/output_summary.json")

    return parser.parse_args()


def main() -> None:
    """Program entrypoint.

    Execution flow:
    1) parse args,
    2) load items,
    3) summarize,
    4) write JSON,
    5) print JSON.
    """
    args = parse_args()

    # Convert raw argument strings into Path objects.
    input_path = Path(args.input)
    output_path = Path(args.output)

    # Run data loading and summary logic.
    items = load_items(input_path)
    summary = build_summary(items)

    # Ensure output directory exists for first run.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write pretty JSON for easier reading and troubleshooting.
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Print the same summary to terminal for immediate feedback.
    print(json.dumps(summary, indent=2))


# Standard entrypoint guard so imports do not auto-run the script.
if __name__ == "__main__":
    main()
