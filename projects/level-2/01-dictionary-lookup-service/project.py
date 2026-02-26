"""Level 2 project: Dictionary Lookup Service.

Heavily commented beginner-friendly script:
- build a dictionary from key=value lines,
- look up keys with fuzzy matching and suggestions,
- handle missing keys gracefully with try/except.

Skills practiced: dict comprehensions, try/except, sets, sorting with key,
nested data structures, enumerate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

# difflib provides get_close_matches for fuzzy string matching.
# This is a stdlib module — no pip install needed.
import difflib


def load_dictionary(path: Path) -> dict[str, str]:
    """Load a dictionary from a file of 'key=value' lines.

    Lines without '=' are silently skipped.  Duplicate keys keep
    the LAST value (dict insertion order).

    Returns:
        A dict mapping term -> definition.
    """
    if not path.exists():
        raise FileNotFoundError(f"Dictionary file not found: {path}")

    raw = path.read_text(encoding="utf-8").splitlines()

    # Dict comprehension — splits each valid line on the first '=' only.
    # str.split("=", 1) returns at most 2 parts, so definitions can
    # contain '=' characters safely.
    entries = {
        parts[0].strip().lower(): parts[1].strip()
        for line in raw
        if "=" in line
        for parts in [line.split("=", 1)]
    }
    return entries


def lookup(dictionary: dict[str, str], term: str) -> dict:
    """Look up a term in the dictionary.

    Returns a result dict with:
      - found: bool
      - term: the normalised search term
      - definition: str or None
      - suggestions: list of close matches when not found
    """
    # Normalise to lowercase so lookups are case-insensitive.
    normalised = term.strip().lower()

    try:
        # Direct lookup — this is the happy path.
        definition = dictionary[normalised]
        return {
            "found": True,
            "term": normalised,
            "definition": definition,
            "suggestions": [],
        }
    except KeyError:
        # When the key is missing we suggest close matches.
        # get_close_matches uses SequenceMatcher under the hood.
        suggestions = difflib.get_close_matches(
            normalised, dictionary.keys(), n=3, cutoff=0.6
        )
        return {
            "found": False,
            "term": normalised,
            "definition": None,
            "suggestions": suggestions,
        }


def batch_lookup(
    dictionary: dict[str, str], terms: list[str]
) -> list[dict]:
    """Look up many terms and return a list of result dicts.

    Uses enumerate so the caller can track original ordering.
    """
    results = []
    for idx, term in enumerate(terms):
        result = lookup(dictionary, term)
        result["index"] = idx
        results.append(result)
    return results


def dictionary_stats(dictionary: dict[str, str]) -> dict:
    """Compute simple statistics about the dictionary.

    Demonstrates set operations and sorting with a key function.
    """
    # Set of unique first letters.
    first_letters: set[str] = {k[0] for k in dictionary if k}

    # Sort keys by definition length (longest first).
    sorted_by_length = sorted(
        dictionary.keys(),
        key=lambda k: len(dictionary[k]),
        reverse=True,
    )

    return {
        "total_entries": len(dictionary),
        "unique_first_letters": sorted(first_letters),
        "longest_definitions": sorted_by_length[:5],
        "shortest_definitions": sorted_by_length[-5:],
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Dictionary lookup with fuzzy matching"
    )
    parser.add_argument(
        "--dict",
        default="data/sample_input.txt",
        help="Path to the dictionary file (key=value per line)",
    )
    parser.add_argument(
        "--lookup",
        nargs="*",
        default=[],
        help="Terms to look up",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Print dictionary statistics",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: load dictionary, run lookups, print results."""
    args = parse_args()
    dictionary = load_dictionary(Path(args.dict))

    if args.stats:
        stats = dictionary_stats(dictionary)
        print(f"=== Dictionary Statistics ===")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        return

    if args.lookup:
        results = batch_lookup(dictionary, args.lookup)
    else:
        # Default: look up a few sample terms to demonstrate behaviour.
        samples = list(dictionary.keys())[:3] + ["nonexistent"]
        results = batch_lookup(dictionary, samples)

    # Format results as a readable table.
    print(f"=== Lookup Results ===\n")
    print(f"  {'Term':<20} {'Found':>6}  {'Definition / Suggestions'}")
    print(f"  {'-'*20} {'-'*6}  {'-'*30}")
    for r in results:
        term = r["term"]
        if r["found"]:
            print(f"  {term:<20} {'yes':>6}  {r['definition']}")
        else:
            suggestions = ", ".join(r.get("suggestions", []))
            hint = f"Did you mean: {suggestions}" if suggestions else "(no matches)"
            print(f"  {term:<20} {'no':>6}  {hint}")


if __name__ == "__main__":
    main()
