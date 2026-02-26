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

    WHY bigrams instead of comparing whole strings? -- Bigrams capture
    local character patterns, making similarity robust to typos and minor
    variations ("Jon" vs "John" share "Jo" and are scored as similar).

    Example: "hello" -> {"he", "el", "ll", "lo"}
    """
    t = text.lower().strip()
    return {t[i:i + 2] for i in range(len(t) - 1)} if len(t) >= 2 else {t}


def jaccard_similarity(a: str, b: str) -> float:
    """Compute Jaccard similarity between two strings using bigrams.

    Returns a float between 0.0 (completely different) and 1.0 (identical).
    """
    set_a = bigrams(a)
    set_b = bigrams(b)
    if not set_a and not set_b:
        return 1.0  # both empty = same
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

    Returns a list of duplicate-pair dicts.
    """
    duplicates: list[dict] = []

    # WHY O(n^2) nested loop? -- For typical CSV datasets (hundreds to low
    # thousands of rows) this brute-force approach is simple and correct.
    # At scale you would use blocking/indexing strategies to reduce comparisons.
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            row_a = rows[i]
            row_b = rows[j]

            # Exact match check
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

            # Fuzzy match check
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
