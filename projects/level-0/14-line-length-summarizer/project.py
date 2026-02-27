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
    so it is easy to test in isolation.
    """
    return [len(line) for line in lines]


def compute_stats(lengths: list[int]) -> dict[str, int | float]:
    """Compute min, max, and average line length.

    WHY guard against empty lists? -- If the file is empty, calling
    min() or max() on an empty list crashes.  We check first.
    """
    if not lengths:
        return {"min": 0, "max": 0, "average": 0.0, "total_lines": 0}

    total = 0
    for length in lengths:
        total += length

    return {
        "min": min(lengths),
        "max": max(lengths),
        "average": round(total / len(lengths), 2),
        "total_lines": len(lengths),
    }


def build_histogram(lengths: list[int], bar_char: str = "#", scale: int = 2) -> str:
    """Build a simple text histogram of line lengths.

    Each line gets a bar whose width is proportional to its length.
    The scale parameter controls how many characters per unit of length.

    WHY integer division? -- We divide the length by the scale factor
    to keep the bars a reasonable width on screen.
    """
    if not lengths:
        return "(no data)"

    lines = []
    for i, length in enumerate(lengths, start=1):
        bar_width = length // scale
        bar = bar_char * max(bar_width, 1)  # At least one character.
        lines.append(f"  Line {i:>3}: {bar} ({length})")

    return "\n".join(lines)


def categorise_lengths(lengths: list[int]) -> dict[str, int]:
    """Group lines into short (< 40), medium (40-80), and long (> 80).

    WHY categories? -- Raw numbers are harder to scan than categories.
    This gives a quick overview of the file's shape.
    """
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
