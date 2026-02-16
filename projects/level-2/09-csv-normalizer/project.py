"""Level 2 learning project: Csv Normalizer.

This script is intentionally simple and heavily commented so beginners can
understand every step before moving to more advanced patterns.
"""

from __future__ import annotations

# argparse lets us accept command-line flags such as --input and --output.
import argparse
# json is used to write a human-readable output summary file.
import json
# Path gives safer file handling than raw string paths.
from pathlib import Path

# Constant metadata so you can see which project produced the output.
PROJECT_LEVEL = 2
PROJECT_NAME = "Csv Normalizer"


def load_lines(path: Path) -> list[str]:
    """Read non-empty lines from a text file.

    Why this function exists:
    - Keeps file-reading logic in one place.
    - Makes it easier to test separately from main().
    """
    # Always fail loudly with a clear message if input file is missing.
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    # Read all lines, trim whitespace, and ignore blank lines.
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    cleaned_lines = [line.strip() for line in raw_lines if line.strip()]
    return cleaned_lines


def build_summary(lines: list[str]) -> dict:
    """Create a small summary dictionary from the cleaned lines."""
    # len(lines) = total number of lines after cleanup.
    line_count = len(lines)

    # set(lines) removes duplicates, then len() counts unique values.
    unique_count = len(set(lines))

    # Keep a tiny preview to quickly inspect what data looked like.
    sample = lines[:3]

    return {
        "project_name": PROJECT_NAME,
        "project_level": PROJECT_LEVEL,
        "line_count": line_count,
        "unique_count": unique_count,
        "sample": sample,
    }


def parse_args() -> argparse.Namespace:
    """Define and parse command-line arguments for this script."""
    parser = argparse.ArgumentParser(
        description="Beginner learning project runner"
    )

    # Input text file path. Defaults to included sample data.
    parser.add_argument("--input", default="data/sample_input.txt")

    # Output JSON file path where summary results are written.
    parser.add_argument("--output", default="data/output_summary.json")

    return parser.parse_args()


def main() -> None:
    """Program entrypoint.

    Flow:
    1) Parse arguments.
    2) Load input lines.
    3) Build summary.
    4) Write JSON output.
    5) Print JSON to console.
    """
    args = parse_args()

    # Convert CLI string paths into Path objects for safer file operations.
    input_path = Path(args.input)
    output_path = Path(args.output)

    # Read data and compute summary result.
    lines = load_lines(input_path)
    summary = build_summary(lines)

    # Ensure output directory exists before writing output file.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write pretty JSON for easy inspection during learning.
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Also print the same JSON to terminal so you see immediate feedback.
    print(json.dumps(summary, indent=2))


# Standard Python pattern: only run main() when file is executed directly.
if __name__ == "__main__":
    main()
