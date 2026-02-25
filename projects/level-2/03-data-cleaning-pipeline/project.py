"""Level 2 project: Data Cleaning Pipeline.

Heavily commented beginner-friendly script:
- chain cleaning operations on text records,
- strip whitespace, normalise case, deduplicate,
- filter out invalid records, report cleaning stats.

Skills practiced: list comprehensions, dict comprehensions, try/except,
sets for deduplication, re module for pattern matching, enumerate.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def strip_whitespace(records: list[str]) -> list[str]:
    """Remove leading/trailing whitespace from every record.

    This is always the first step — many data issues are just extra spaces.
    """
    return [r.strip() for r in records]


def normalise_case(records: list[str]) -> list[str]:
    """Convert every record to lowercase for consistent comparison.

    Keeps the original data retrievable if you store raw + cleaned versions.
    """
    return [r.lower() for r in records]


def remove_blanks(records: list[str]) -> list[str]:
    """Drop empty strings that result from blank lines or whitespace-only rows."""
    return [r for r in records if r]


def deduplicate(records: list[str]) -> list[str]:
    """Remove duplicate records while preserving original order.

    Uses a set to track what we have already seen.  Sets give O(1) lookup
    which is much faster than checking a list each time.
    """
    seen: set[str] = set()
    unique: list[str] = []

    for record in records:
        if record not in seen:
            seen.add(record)
            unique.append(record)

    return unique


def filter_by_pattern(records: list[str], pattern: str) -> tuple[list[str], list[str]]:
    """Split records into matching and non-matching based on a regex pattern.

    Args:
        records: The list of cleaned strings.
        pattern: A regex pattern that valid records must match.

    Returns:
        A tuple of (valid_records, rejected_records).
    """
    # re.compile pre-builds the regex so it runs faster when used many times.
    compiled = re.compile(pattern)

    valid: list[str] = []
    rejected: list[str] = []

    for record in records:
        if compiled.search(record):
            valid.append(record)
        else:
            rejected.append(record)

    return valid, rejected


def normalise_separators(records: list[str], target: str = ",") -> list[str]:
    """Replace common field separators (tabs, semicolons, pipes) with target.

    Many CSV files use inconsistent separators. This step standardises them.
    """
    # This regex matches any of the common separators.
    separator_pattern = re.compile(r"[;\t|]")
    return [separator_pattern.sub(target, r) for r in records]


def run_pipeline(
    records: list[str],
    filter_pattern: str | None = None,
) -> dict:
    """Execute the full cleaning pipeline and return stats.

    Pipeline order:
    1. Strip whitespace
    2. Remove blanks
    3. Normalise case
    4. Normalise separators
    5. Deduplicate
    6. (Optional) Filter by regex pattern

    Returns a dict with cleaned records and statistics.
    """
    original_count = len(records)

    # Step 1-4: chain cleaning operations.
    cleaned = strip_whitespace(records)
    cleaned = remove_blanks(cleaned)
    cleaned = normalise_case(cleaned)
    cleaned = normalise_separators(cleaned)
    cleaned = deduplicate(cleaned)

    rejected: list[str] = []
    if filter_pattern:
        cleaned, rejected = filter_by_pattern(cleaned, filter_pattern)

    return {
        "original_count": original_count,
        "cleaned_count": len(cleaned),
        "duplicates_removed": original_count - len(remove_blanks(strip_whitespace(records)))
            + (len(deduplicate(normalise_case(remove_blanks(strip_whitespace(records)))))
               - len(cleaned) - len(rejected)),
        "blanks_removed": original_count - len(remove_blanks(strip_whitespace(records))),
        "rejected_count": len(rejected),
        "cleaned": cleaned,
        "rejected": rejected,
    }


def load_and_clean(path: Path, filter_pattern: str | None = None) -> dict:
    """Load a text file and run the cleaning pipeline.

    Each line in the file is treated as one record.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    raw_lines = path.read_text(encoding="utf-8").splitlines()
    return run_pipeline(raw_lines, filter_pattern=filter_pattern)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Data cleaning pipeline")
    parser.add_argument("input", help="Path to input text file")
    parser.add_argument(
        "--filter",
        default=None,
        help="Regex pattern — only records matching this are kept",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to write cleaned output (default: stdout only)",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: load data, clean it, report results."""
    args = parse_args()
    result = load_and_clean(Path(args.input), filter_pattern=args.filter)

    # Print summary stats.
    stats = {k: v for k, v in result.items() if k not in ("cleaned", "rejected")}
    print("=== Cleaning Stats ===")
    print(json.dumps(stats, indent=2))
    print(f"\n=== Cleaned Records ({result['cleaned_count']}) ===")
    for i, record in enumerate(result["cleaned"], 1):
        print(f"  {i}. {record}")

    if result["rejected"]:
        print(f"\n=== Rejected ({result['rejected_count']}) ===")
        for record in result["rejected"]:
            print(f"  - {record}")

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(
            "\n".join(result["cleaned"]) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
