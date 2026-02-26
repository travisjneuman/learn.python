# Dictionary Lookup Service — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Dictionary Lookup Service — complete annotated solution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

# WHY: difflib is a stdlib module that provides fuzzy string matching.
# We use it to suggest corrections when a lookup misses, which is a
# much better user experience than just "not found".
import difflib


def load_dictionary(path: Path) -> dict[str, str]:
    """Load a dictionary from a file of 'key=value' lines."""
    if not path.exists():
        raise FileNotFoundError(f"Dictionary file not found: {path}")

    raw = path.read_text(encoding="utf-8").splitlines()

    # WHY: Dict comprehension with split("=", 1) — the maxsplit=1 argument
    # ensures definitions containing '=' characters are preserved intact.
    # Without it, "url=https://a.com/b=c" would split into 3 parts and break.
    entries = {
        parts[0].strip().lower(): parts[1].strip()
        for line in raw
        if "=" in line
        for parts in [line.split("=", 1)]
    }
    return entries


def lookup(dictionary: dict[str, str], term: str) -> dict:
    """Look up a term with fuzzy matching fallback."""
    # WHY: Normalise to lowercase so "Python", "PYTHON", and "python"
    # all find the same entry — users should not need to know the exact case.
    normalised = term.strip().lower()

    try:
        # WHY: Using dict[key] with try/except instead of dict.get() because
        # we want different behaviour for hit vs miss — try/except makes
        # the two paths explicit and easy to extend.
        definition = dictionary[normalised]
        return {
            "found": True,
            "term": normalised,
            "definition": definition,
            "suggestions": [],
        }
    except KeyError:
        # WHY: get_close_matches uses SequenceMatcher internally. The cutoff
        # of 0.6 means a word must be at least 60% similar to be suggested.
        # n=3 limits suggestions to the 3 best matches.
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
    """Look up many terms, tracking original order with enumerate."""
    results = []
    for idx, term in enumerate(terms):
        result = lookup(dictionary, term)
        # WHY: Attaching the original index lets callers correlate results
        # back to input order, which matters for batch processing.
        result["index"] = idx
        results.append(result)
    return results


def dictionary_stats(dictionary: dict[str, str]) -> dict:
    """Compute statistics about the dictionary."""
    # WHY: Set comprehension collects unique first letters in O(n) time.
    # Sets automatically discard duplicates.
    first_letters: set[str] = {k[0] for k in dictionary if k}

    # WHY: sorted() with a key function lets us rank entries by definition
    # length without modifying the original dict.
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
        samples = list(dictionary.keys())[:3] + ["nonexistent"]
        results = batch_lookup(dictionary, samples)

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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| `split("=", 1)` for parsing | Definitions may contain `=` characters (e.g. URLs). Splitting on only the first `=` preserves the full definition. |
| `try/except KeyError` instead of `dict.get()` | The two code paths (found vs not found) are very different. Using try/except makes each path explicit and keeps the happy path clean. |
| Lowercase normalisation on load | Case-insensitive lookups are the expected default. Normalising once at load time avoids doing it on every lookup. |
| Fuzzy matching with `difflib` | Returning "did you mean?" suggestions transforms a dead-end miss into a helpful interaction, which is critical for user-facing tools. |
| Returning structured dicts, not strings | Dicts are machine-readable. Callers can decide how to display results (table, JSON, GUI) without parsing strings. |

## Alternative Approaches

### Using `dict.get()` instead of `try/except`

```python
def lookup_with_get(dictionary, term):
    normalised = term.strip().lower()
    definition = dictionary.get(normalised)
    if definition is not None:
        return {"found": True, "term": normalised, "definition": definition}
    suggestions = difflib.get_close_matches(normalised, dictionary.keys())
    return {"found": False, "term": normalised, "suggestions": suggestions}
```

This is simpler and perfectly valid. The trade-off: `dict.get()` cannot distinguish between a key that maps to `None` and a missing key. In this project that does not matter (all values are strings), but the `try/except` pattern is more general and worth practicing.

### Using the `csv` module instead of manual parsing

For more complex dictionary files (quoted values, multi-line entries), Python's `csv` module handles edge cases automatically. The manual approach here is chosen because the file format is simple and it teaches `str.split()` mechanics directly.

## Common Pitfalls

1. **Splitting on every `=` sign** — Using `line.split("=")` without the `maxsplit=1` argument will break definitions containing `=`. For example, `url=https://example.com/a=b` would incorrectly split into three parts instead of two.

2. **Forgetting to normalise input** — If you normalise keys to lowercase at load time but forget to lowercase the search term, "Python" will not match "python". Always normalise both sides of a comparison.

3. **Bare `except:` instead of `except KeyError`** — Catching all exceptions hides real bugs (like `TypeError` from passing a non-string key). Always catch the most specific exception type you expect.
