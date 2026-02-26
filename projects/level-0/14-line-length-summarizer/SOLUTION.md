# Solution: Level 0 / Project 14 - Line Length Summarizer

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: Line Length Summarizer.

Read a text file, measure the length of each line, and compute
statistics: min, max, average, and a simple text histogram.

Concepts: loops, accumulation, min/max, integer division, string * repeat.
"""


import argparse
import json
from pathlib import Path


def measure_lines(lines: list[str]) -> list[int]:
    """Return a list of line lengths.

    WHY a separate function? -- Measuring is pure logic (no I/O),
    so it is easy to test in isolation.  assert measure_lines(["hi"]) == [2]
    is a one-line test.
    """
    # WHY list comprehension: [len(line) for line in lines] is a concise
    # way to transform a list of strings into a list of integers.
    # It reads as: "the length of each line, for each line in lines."
    return [len(line) for line in lines]


def compute_stats(lengths: list[int]) -> dict:
    """Compute min, max, and average line length.

    WHY guard against empty lists? -- If the file is empty, calling
    min() or max() on an empty list crashes with ValueError.
    Dividing by zero for the average also crashes.  We check first.
    """
    if not lengths:
        return {"min": 0, "max": 0, "average": 0.0, "total_lines": 0}

    # WHY manual accumulation instead of sum(): At Level 0, seeing the
    # explicit loop makes the average calculation transparent.
    # total += length is the accumulator pattern — one of the most
    # fundamental patterns in programming.
    total = 0
    for length in lengths:
        total += length

    return {
        "min": min(lengths),
        "max": max(lengths),
        # WHY round to 2: Averages often produce long decimals.
        # Rounding keeps the output readable.
        "average": round(total / len(lengths), 2),
        "total_lines": len(lengths),
    }


def build_histogram(lengths: list[int], bar_char: str = "#", scale: int = 2) -> str:
    """Build a simple text histogram of line lengths.

    Each line gets a bar whose width is proportional to its length.
    The scale parameter controls how many characters per unit of length.

    WHY integer division? -- We divide the length by the scale factor
    to keep the bars a reasonable width on screen.  A 200-character
    line would produce a 100-character bar at scale=2, not 200.
    """
    if not lengths:
        return "(no data)"

    lines = []
    for i, length in enumerate(lengths, start=1):
        # WHY //: Integer division (floor division) drops the decimal.
        # 15 // 2 gives 7, not 7.5.  We need whole characters for the bar.
        bar_width = length // scale
        # WHY max(bar_width, 1): Even a 0-length line gets at least one
        # character so the bar is visible and the line is not blank.
        bar = bar_char * max(bar_width, 1)
        # WHY :>3 for line number: Right-justifies the number in a
        # 3-character field so single-digit and double-digit numbers align.
        lines.append(f"  Line {i:>3}: {bar} ({length})")

    return "\n".join(lines)


def categorise_lengths(lengths: list[int]) -> dict:
    """Group lines into short (< 40), medium (40-80), and long (> 80).

    WHY categories? -- Raw numbers are harder to scan than categories.
    This gives a quick overview of the file's shape — is it mostly
    short lines (poetry?) or long lines (prose?).
    """
    # WHY sum with generator: sum(1 for l in lengths if condition) counts
    # items matching the condition.  It is the counting pattern but
    # expressed as a one-liner.
    short = sum(1 for l in lengths if l < 40)
    medium = sum(1 for l in lengths if 40 <= l <= 80)
    long = sum(1 for l in lengths if l > 80)
    return {"short": short, "medium": medium, "long": long}


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Line Length Summarizer")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    lines = input_path.read_text(encoding="utf-8").splitlines()
    lengths = measure_lines(lines)
    stats = compute_stats(lengths)
    categories = categorise_lengths(lengths)

    print("=== Line Length Summary ===")
    print(f"  Total lines: {stats['total_lines']}")
    print(f"  Shortest:    {stats['min']} chars")
    print(f"  Longest:     {stats['max']} chars")
    print(f"  Average:     {stats['average']} chars")
    print(f"\n  Categories: {categories['short']} short, "
          f"{categories['medium']} medium, {categories['long']} long")

    print(f"\n=== Histogram ===\n")
    print(build_histogram(lengths))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = {"stats": stats, "categories": categories, "lengths": lengths}
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\n  Output written to {output_path}")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `measure_lines()` returns a list of integers | Pure data transformation: strings in, integers out. Testable with `assert measure_lines(["hi", "hello"]) == [2, 5]` | Compute lengths inline in `compute_stats()` — couples measuring with statistics, making each harder to test |
| `compute_stats()` uses manual accumulation | The `total += length` loop makes the average formula visible: `total / count`. Beginners can trace every step | Use `sum(lengths)` — one line but hides the accumulation concept that this project teaches |
| `build_histogram()` uses integer division for scaling | `length // scale` keeps bars proportional but manageable. A 200-char line at scale=2 gives a 100-char bar, not 200 | No scaling — long lines produce bars that wrap the terminal, destroying the visual layout |
| `categorise_lengths()` uses fixed thresholds (40/80) | Simple, understandable categories. "Short" means fits in half a terminal; "long" means wider than a standard terminal | Dynamic thresholds based on percentiles — more sophisticated but hard to explain at Level 0 |

## Alternative approaches

### Approach B: Using built-in `statistics` module

```python
import statistics

def compute_stats(lengths: list[int]) -> dict:
    if not lengths:
        return {"min": 0, "max": 0, "average": 0.0, "median": 0, "total_lines": 0}

    return {
        "min": min(lengths),
        "max": max(lengths),
        "average": round(statistics.mean(lengths), 2),
        "median": statistics.median(lengths),
        "total_lines": len(lengths),
    }
```

**Trade-off:** The `statistics` module provides `mean()`, `median()`, `stdev()` and more in one import. For production code, this is the right choice — no need to reimplement math. At Level 0, the manual accumulation loop teaches the pattern behind these functions. Once you understand how an average is computed (sum / count), using `statistics.mean()` is a confident shortcut, not magic.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Empty file (no lines) | `measure_lines([])` returns `[]`. `compute_stats([])` returns all zeros. `build_histogram([])` returns `"(no data)"`. No crash | Already handled by the empty-list guards in each function |
| File where every line is the same length | Stats show min == max == average. Histogram has uniform bars. Categorisation puts all lines in one bucket | Already works correctly — this is a valid (if boring) result |
| Very long line (10,000+ characters) | The histogram bar would be 5,000 characters at scale=2, wrapping multiple times in the terminal | Cap bar width: `bar = bar_char * min(bar_width, 50)` to limit visual overflow |
| File with only blank lines | Each blank line has length 0. `measure_lines()` returns `[0, 0, 0, ...]`. Stats show min=0, max=0, average=0.0. All categorised as "short" | Already works, though the histogram shows minimal bars (1 char each due to the `max(bar_width, 1)` guard) |
| Non-text file (binary) | `read_text()` may raise `UnicodeDecodeError` on binary content | Add a try/except for `UnicodeDecodeError` with a helpful message |

## Key takeaways

1. **The accumulator pattern (`total += value`) is fundamental.** Summing, averaging, counting, and aggregating all use this pattern. The loop `for x in items: total += x` is the manual version of `sum(items)`. Understanding the manual version makes built-in shortcuts meaningful.
2. **Integer division `//` is your tool for discrete scaling.** When you need whole numbers (bar characters, page numbers, grid positions), `//` gives you the floor of the division. `15 // 2` gives `7`, not `7.5`. This appears in pagination, histogram generation, and grid layout.
3. **Text histograms are a powerful quick-visualization technique.** `"#" * value` creates a proportional bar with no graphics library needed. This technique works in log files, terminal dashboards, and anywhere graphical charts are not available.
4. **Categorisation simplifies raw data.** Instead of showing 100 individual lengths, grouping into "short", "medium", "long" gives an instant overview. This is the same principle behind data binning in statistics and the foundation of histogram charts.
