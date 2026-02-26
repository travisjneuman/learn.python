# Duplicate Record Investigator — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 4 / Project 07 — Duplicate Record Investigator.

Finds near-duplicate records in a CSV dataset using simple similarity
scoring. Exact matches use key-field comparison; fuzzy matches use
character-level similarity (Jaccard on character bigrams).
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- similarity scoring ----------


def bigrams(text: str) -> set[str]:
    """Generate character bigrams for fuzzy matching.

    WHY bigrams instead of comparing whole strings? Bigrams capture local
    character patterns, making similarity robust to typos and minor
    variations ("Jon" vs "John" share "Jo" and are scored as similar).

    Example: "hello" -> {"he", "el", "ll", "lo"}
    """
    t = text.lower().strip()
    # WHY: If the string is shorter than 2 characters, return it as a
    # single-element set so we still have something to compare.
    return {t[i:i + 2] for i in range(len(t) - 1)} if len(t) >= 2 else {t}


def jaccard_similarity(a: str, b: str) -> float:
    """Compute Jaccard similarity between two strings using bigrams.

    Returns a float between 0.0 (completely different) and 1.0 (identical).
    """
    set_a = bigrams(a)
    set_b = bigrams(b)
    # WHY: Two empty strings are considered identical (both have no content).
    if not set_a and not set_b:
        return 1.0
    # WHY: Jaccard = |intersection| / |union|. This ratio naturally handles
    # strings of different lengths and rewards shared substrings.
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union) if union else 0.0


def find_duplicates(
    rows: list[dict],
    key_fields: list[str],
    threshold: float = 0.8,
) -> list[dict]:
    """Compare all record pairs and find duplicates.

    Two records are considered duplicates if:
    - Exact match: all key_fields are identical, OR
    - Fuzzy match: average Jaccard similarity across key_fields >= threshold.
    """
    duplicates: list[dict] = []

    # WHY: O(n^2) nested loop is simple and correct for typical CSV datasets
    # (hundreds to low thousands of rows). At scale, you would use blocking
    # or indexing strategies (like LSH) to reduce comparisons.
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            row_a = rows[i]
            row_b = rows[j]

            # WHY: Check exact match first because it is cheaper (string
            # equality) and lets us skip the more expensive bigram computation.
            exact = all(
                row_a.get(f, "").strip().lower() == row_b.get(f, "").strip().lower()
                for f in key_fields
            )

            if exact:
                duplicates.append({
                    "row_a": i + 1,
                    "row_b": j + 1,
                    "match_type": "exact",
                    "similarity": 1.0,
                    "fields_compared": key_fields,
                })
                continue

            # Fuzzy match: average Jaccard similarity across all key fields
            scores = []
            for f in key_fields:
                val_a = row_a.get(f, "")
                val_b = row_b.get(f, "")
                scores.append(jaccard_similarity(val_a, val_b))

            avg_score = sum(scores) / len(scores) if scores else 0.0
            if avg_score >= threshold:
                duplicates.append({
                    "row_a": i + 1,
                    "row_b": j + 1,
                    "match_type": "fuzzy",
                    "similarity": round(avg_score, 3),
                    "fields_compared": key_fields,
                })

    return duplicates

# ---------- runner ----------


def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8")
    return list(csv.DictReader(text.splitlines()))


def run(
    input_path: Path,
    output_path: Path,
    key_fields: list[str],
    threshold: float = 0.8,
) -> dict:
    """Load data, find duplicates, write report."""
    rows = load_csv(input_path)
    duplicates = find_duplicates(rows, key_fields, threshold)

    report = {
        "total_records": len(rows),
        "key_fields": key_fields,
        "threshold": threshold,
        "duplicate_pairs_found": len(duplicates),
        "duplicates": duplicates,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Found %d duplicate pairs in %d records", len(duplicates), len(rows))
    return report

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find duplicate records in CSV data")
    parser.add_argument("--input", default="data/sample_input.csv")
    parser.add_argument("--output", default="data/duplicates_report.json")
    parser.add_argument("--keys", default="name,email", help="Comma-separated key fields")
    parser.add_argument("--threshold", type=float, default=0.8, help="Similarity threshold")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    key_fields = [k.strip() for k in args.keys.split(",")]
    report = run(Path(args.input), Path(args.output), key_fields, args.threshold)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Bigram-based Jaccard similarity instead of character-by-character comparison | Bigrams capture local context ("Jo" in both "Jon" and "John"), making the metric robust to typos, insertions, and deletions. Single-character comparison treats "abc" and "cab" as identical (same characters), which is wrong. |
| Average similarity across all key fields | A single low-scoring field should not disqualify a match if all other fields are identical. Averaging balances the signal across multiple comparison dimensions. |
| Separate exact vs. fuzzy match types in the report | Exact matches need different handling than fuzzy ones (exact = definite duplicates, fuzzy = candidates for human review). Distinguishing them in the report lets downstream tools apply different workflows. |
| O(n^2) brute-force comparison | Correct and simple for the expected data size. Premature optimization with blocking/LSH adds complexity that is not justified for CSV files with a few thousand rows. |

## Alternative Approaches

### Using Levenshtein (edit) distance instead of Jaccard similarity

```python
def levenshtein_distance(a: str, b: str) -> int:
    """Count minimum edits (insert, delete, replace) to transform a into b."""
    if len(a) < len(b):
        return levenshtein_distance(b, a)
    if len(b) == 0:
        return len(a)
    prev_row = range(len(b) + 1)
    for i, ca in enumerate(a):
        curr_row = [i + 1]
        for j, cb in enumerate(b):
            cost = 0 if ca == cb else 1
            curr_row.append(min(
                curr_row[j] + 1,          # insert
                prev_row[j + 1] + 1,      # delete
                prev_row[j] + cost,        # replace
            ))
        prev_row = curr_row
    return prev_row[-1]

def levenshtein_similarity(a: str, b: str) -> float:
    max_len = max(len(a), len(b))
    if max_len == 0:
        return 1.0
    return 1.0 - levenshtein_distance(a, b) / max_len
```

**Trade-off:** Levenshtein distance counts the minimum number of single-character edits needed to transform one string into another, which is more intuitive for typo detection ("John" -> "Jon" = 1 edit). However, it is slower (O(n*m) per pair) and less effective for rearrangements ("Smith, John" vs "John Smith"). Jaccard bigrams handle both cases well.

## Common Pitfalls

1. **Setting the threshold too low** — A threshold of 0.1 will flag almost every pair as duplicates. Short strings share bigrams easily ("Al" and "Alice" share "al"). Start with 0.8 and tune down only if you are missing real duplicates.
2. **Not validating that key fields exist in the CSV** — If a key field name is misspelled or absent from the headers, `row.get(field, "")` silently returns empty strings and every row will appear identical on that field, causing a flood of false positives.
3. **Forgetting the single-record edge case** — A CSV with only one data row should produce zero duplicate pairs. The nested loop naturally handles this (the inner loop range is empty), but it is worth testing explicitly.
