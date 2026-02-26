# Solution: Level 0 / Project 10 - Duplicate Line Finder

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: Duplicate Line Finder.

Enter lines of text and find which ones appear more than once.
Report duplicates and their counts.

Concepts: dictionaries for counting, sets for uniqueness, text input.
"""


def count_line_occurrences(lines: list) -> dict:
    """Count how many times each line appears.

    WHY a dict? -- A dictionary maps each unique line (the key) to its
    count (the value).  This is the fundamental pattern for counting
    things in Python.
    """
    counts = {}
    for line in lines:
        # WHY if/else instead of dict.get(): The explicit check makes the
        # counting pattern visible.  "If we have seen this line before,
        # add 1.  Otherwise, start counting at 1."  This is the same
        # pattern used in word_frequencies() in project 06.
        if line in counts:
            counts[line] += 1
        else:
            counts[line] = 1
    return counts


def find_duplicates(lines: list) -> list:
    """Find lines that appear more than once and report details.

    Returns a list of dicts, each containing the duplicated text,
    the count, and the line numbers where it appears.
    """
    counts = count_line_occurrences(lines)

    duplicates = []
    for text, count in counts.items():
        # WHY count > 1: By definition, a duplicate appears more than once.
        # Lines that appear exactly once are not duplicates and are skipped.
        if count > 1:
            # WHY find line numbers: Knowing WHERE duplicates occur (not just
            # that they exist) is far more useful.  "apple on lines 1 and 3"
            # helps the user find and fix the duplication.
            positions = []
            for i, line in enumerate(lines):
                if line == text:
                    # WHY i + 1: Humans count from 1, enumerate counts from 0.
                    positions.append(i + 1)

            duplicates.append({
                "text": text,
                "count": count,
                "line_numbers": positions,
            })

    return duplicates


def build_report(lines: list) -> dict:
    """Build a full report about duplicates in the input.

    WHY filter non_empty first? -- Empty lines are noise.  Counting
    them as duplicates would give misleading results ("blank appears
    47 times" is not useful).
    """
    non_empty = [line for line in lines if line]
    duplicates = find_duplicates(non_empty)

    return {
        "total_lines": len(non_empty),
        # WHY set(non_empty): A set automatically removes duplicates,
        # so its length equals the number of unique lines.  This is a
        # clean way to count distinct items.
        "unique_lines": len(set(non_empty)),
        "duplicate_count": len(duplicates),
        "duplicates": duplicates,
    }


if __name__ == "__main__":
    print("=== Duplicate Line Finder ===")
    print("Enter lines of text. Enter a blank line when done.\n")

    lines = []
    line_num = 1
    while True:
        line = input(f"  Line {line_num}: ")
        if line == "":
            break
        # WHY strip: Trailing spaces are invisible but would make
        # "hello" and "hello " different.  Stripping ensures consistent
        # comparison.
        lines.append(line.strip())
        line_num += 1

    if not lines:
        print("No lines entered.")
    else:
        report = build_report(lines)

        print(f"\n=== Duplicate Line Report ===")
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `count_line_occurrences()` is a separate function | It isolates the counting logic so `find_duplicates()` can focus on filtering and position tracking. Each function has one job | Do everything in `find_duplicates()` — combines counting and filtering, making it harder to test the counting logic alone |
| `find_duplicates()` returns line numbers, not just counts | Knowing that "apple" appears on lines 1 and 3 is actionable — the user can go fix it. Just knowing "apple appears twice" is less helpful | Return only counts — simpler but less useful for debugging or data cleanup |
| `build_report()` filters out empty lines first | Empty lines appearing multiple times is noise, not meaningful duplication. Filtering them produces cleaner results | Keep empty lines — technically correct but floods the report with useless entries |
| `set(non_empty)` for counting unique lines | A set is the cleanest way to count distinct items in Python. `len(set(items))` is a one-line idiom for "how many unique values?" | Count manually with a loop and a seen-list — works but reinvents what `set` does natively |

## Alternative approaches

### Approach B: Using `collections.Counter` and list comprehension

```python
from collections import Counter

def find_duplicates(lines: list) -> list:
    counter = Counter(lines)
    duplicates = []
    for text, count in counter.items():
        if count > 1:
            # List comprehension to find positions.
            positions = [i + 1 for i, line in enumerate(lines) if line == text]
            duplicates.append({
                "text": text,
                "count": count,
                "line_numbers": positions,
            })
    return duplicates
```

**Trade-off:** `Counter` handles the counting in one line, and the list comprehension for positions is more concise than an explicit loop. This is the approach you would use in real projects. However, at Level 0, the manual counting loop teaches the dictionary increment pattern that underlies `Counter`. Understanding the manual approach first makes `Counter` feel like a natural shortcut rather than magic.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| All lines are unique | `find_duplicates()` returns an empty list. The report shows "No duplicates found." | Already handled |
| Every line is identical | `count_line_occurrences()` returns one entry with a high count. `find_duplicates()` reports it correctly | Already handled |
| Lines with trailing spaces (`"hello"` vs `"hello "`) | Without `.strip()`, these are different strings and would not be detected as duplicates | The `__main__` block strips input. For file-based input, strip lines during loading |
| Case differences (`"Hello"` vs `"hello"`) | These are treated as different lines. `find_duplicates()` is case-sensitive by default | For case-insensitive comparison, call `.lower()` on each line before processing |
| Empty input (no lines entered) | `build_report([])` returns zero counts. The `__main__` block prints "No lines entered." | Already handled |

## Key takeaways

1. **Dictionaries are Python's universal counting tool.** The pattern `if key in dict: dict[key] += 1; else: dict[key] = 1` solves word counting, vote tallying, frequency analysis, and duplicate detection. Master this pattern — you will use it in nearly every project.
2. **Sets give you uniqueness for free.** `len(set(items))` counts distinct values in one line. `set` automatically removes duplicates because it only stores unique values. This is the standard Python idiom for deduplication.
3. **Reporting WHERE something occurs is more valuable than reporting THAT it occurs.** "apple appears on lines 1 and 3" is actionable; "apple appears twice" is not. Including positions takes extra code but dramatically increases the report's usefulness.
4. **Filter noise before analysis.** Empty lines, whitespace-only lines, and other non-content should be excluded before counting. Pre-filtering with a list comprehension (`[line for line in lines if line]`) keeps the analysis clean and the results meaningful.
