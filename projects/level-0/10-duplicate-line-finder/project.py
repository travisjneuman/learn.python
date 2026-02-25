"""Level 0 project: Duplicate Line Finder.

Read a text file and find lines that appear more than once.
Report which lines are duplicated and how many times.

Concepts: dictionaries for counting, sets for uniqueness, file I/O.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def count_line_occurrences(lines: list[str]) -> dict[str, int]:
    """Count how many times each line appears.

    WHY a dict? -- A dictionary maps each unique line (the key) to its
    count (the value).  This is the fundamental pattern for counting
    things in Python.
    """
    counts = {}
    for line in lines:
        if line in counts:
            counts[line] += 1
        else:
            counts[line] = 1
    return counts


def find_duplicates(lines: list[str]) -> list[dict]:
    """Find lines that appear more than once and report details.

    Returns a list of dicts, each containing the duplicated text,
    the count, and the line numbers where it appears.
    """
    counts = count_line_occurrences(lines)

    duplicates = []
    for text, count in counts.items():
        if count > 1:
            # Find all line numbers (1-based) where this text appears.
            positions = []
            for i, line in enumerate(lines):
                if line == text:
                    positions.append(i + 1)

            duplicates.append({
                "text": text,
                "count": count,
                "line_numbers": positions,
            })

    return duplicates


def load_lines(path: Path) -> list[str]:
    """Load all lines from a file, stripping trailing whitespace.

    WHY strip each line? -- Trailing spaces are invisible but would
    make 'hello' and 'hello ' look like different lines.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    raw = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in raw]


def build_report(lines: list[str]) -> dict:
    """Build a full report about duplicates in the file."""
    non_empty = [line for line in lines if line]
    duplicates = find_duplicates(non_empty)

    return {
        "total_lines": len(non_empty),
        "unique_lines": len(set(non_empty)),
        "duplicate_count": len(duplicates),
        "duplicates": duplicates,
    }


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Duplicate Line Finder")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()

    lines = load_lines(Path(args.input))
    report = build_report(lines)

    print("=== Duplicate Line Report ===")
    print(f"  Total lines: {report['total_lines']}")
    print(f"  Unique lines: {report['unique_lines']}")
    print(f"  Duplicated lines: {report['duplicate_count']}")

    if report["duplicates"]:
        print("\n  Duplicates found:")
        for dup in report["duplicates"]:
            positions = ", ".join(str(n) for n in dup["line_numbers"])
            print(f"    '{dup['text']}' appears {dup['count']} times (lines {positions})")
    else:
        print("\n  No duplicates found.")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\n  Report written to {output_path}")


if __name__ == "__main__":
    main()
