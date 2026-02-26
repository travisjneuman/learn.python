# Data Cleaning Pipeline — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Data Cleaning Pipeline — complete annotated solution."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def strip_whitespace(records: list[str]) -> list[str]:
    """Remove leading/trailing whitespace from every record."""
    # WHY: Whitespace stripping is always the first step because trailing
    # spaces make "alice " and "alice" look like different records during
    # deduplication. Clean early to prevent downstream confusion.
    return [r.strip() for r in records]


def normalise_case(records: list[str]) -> list[str]:
    """Convert every record to lowercase."""
    # WHY: Case normalisation ensures "Alice" and "alice" are treated
    # as the same record. This must happen before deduplication.
    return [r.lower() for r in records]


def remove_blanks(records: list[str]) -> list[str]:
    """Drop empty strings from the list."""
    # WHY: After stripping whitespace, blank lines become empty strings.
    # Filtering with a truthy check removes them — empty string is falsy.
    return [r for r in records if r]


def deduplicate(records: list[str]) -> list[str]:
    """Remove duplicate records while preserving original order."""
    # WHY: A set gives O(1) membership testing. Checking "if record in list"
    # would be O(n) per check, making the full loop O(n^2). With a set
    # the full loop is O(n).
    seen: set[str] = set()
    unique: list[str] = []

    for record in records:
        if record not in seen:
            seen.add(record)
            unique.append(record)

    return unique


def filter_by_pattern(records: list[str], pattern: str) -> tuple[list[str], list[str]]:
    """Split records into matching and non-matching based on a regex."""
    # WHY: re.compile pre-builds the regex state machine once. Without it,
    # re.search would recompile the pattern on every iteration — wasteful
    # when the same pattern is applied to hundreds of records.
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
    """Replace tabs, semicolons, and pipes with the target separator."""
    # WHY: Real-world CSV files use inconsistent delimiters. Standardising
    # them into a single separator makes downstream parsing reliable.
    separator_pattern = re.compile(r"[;\t|]")
    return [separator_pattern.sub(target, r) for r in records]


def run_pipeline(
    records: list[str],
    filter_pattern: str | None = None,
) -> dict:
    """Execute the full cleaning pipeline and return stats.

    Pipeline order matters:
    1. Strip whitespace   — so " alice " becomes "alice"
    2. Remove blanks      — drop now-empty lines
    3. Normalise case     — so "Alice" matches "alice"
    4. Normalise seps     — unify delimiters
    5. Deduplicate        — remove duplicates (after normalisation!)
    6. Filter (optional)  — apply regex pattern
    """
    original_count = len(records)

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
    """Load a text file and run the cleaning pipeline."""
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

    # WHY: Exclude the actual records from the stats printout — they could
    # be thousands of lines. Stats give a quick summary.
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Each cleaning step is a separate function | Single-responsibility makes each step independently testable and reorderable. You can add a new step without touching existing ones. |
| Pipeline step ordering (strip before dedupe) | Stripping and normalising must happen before deduplication, otherwise `"Alice "` and `"alice"` would be treated as different records. Order matters. |
| Set for deduplication | A set provides O(1) membership checks. Using a list for `seen` would make deduplication O(n^2) — unacceptable for large datasets. |
| `re.compile` before the loop | Compiling the regex once avoids redundant parsing on every iteration. This is a standard performance pattern when applying the same pattern to many strings. |
| Returning a result dict with both cleaned and rejected | Callers may need either or both. Returning everything in a structured dict keeps the function flexible without requiring separate calls. |

## Alternative Approaches

### Using `functools.reduce` for pipeline chaining

```python
from functools import reduce

def run_pipeline_functional(records, filter_pattern=None):
    steps = [strip_whitespace, remove_blanks, normalise_case,
             normalise_separators, deduplicate]
    cleaned = reduce(lambda data, func: func(data), steps, records)
    # ... handle filter and stats
```

This is more concise but harder to debug — you cannot easily inspect intermediate results. The explicit step-by-step approach is better for learning and for adding logging between steps.

### Using Python's `csv` module for separator handling

The `csv` module handles quoting, escaping, and multi-character delimiters automatically. The manual regex approach here teaches the fundamentals, but production code should prefer `csv.reader()` or `pandas.read_csv()`.

## Common Pitfalls

1. **Wrong pipeline order** — If you deduplicate before normalising case, `"Alice"` and `"alice"` survive as separate records. Always normalise first, then deduplicate.

2. **Invalid regex in `--filter`** — An unclosed bracket like `[abc` will crash `re.compile`. Production code should wrap this in `try/except re.error` and return a clear error message.

3. **Encoding issues** — Files saved with non-UTF-8 encoding (like Latin-1 or Windows-1252) will cause `UnicodeDecodeError`. Adding `errors="replace"` to `read_text()` prevents crashes but loses characters. The correct fix is to detect or specify the encoding.
