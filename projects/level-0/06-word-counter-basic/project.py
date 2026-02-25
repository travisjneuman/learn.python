"""Level 0 project: Word Counter Basic.

Read a text file and count words, lines, and characters.
Also find the most frequent words.

Concepts: string splitting, counting with dicts, sorting, file I/O.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def count_words(text: str) -> int:
    """Count the number of words in a string.

    WHY split()? -- Calling split() with no arguments splits on any
    whitespace (spaces, tabs, newlines) and ignores leading/trailing
    whitespace automatically.
    """
    return len(text.split())


def count_lines(text: str) -> int:
    """Count the number of lines in a string.

    WHY splitlines()? -- It handles all line-ending styles
    (\\n, \\r\\n, \\r) so the count is correct on any OS.
    """
    if not text:
        return 0
    return len(text.splitlines())


def count_characters(text: str) -> int:
    """Count the total number of characters (including spaces)."""
    return len(text)


def word_frequencies(text: str) -> dict[str, int]:
    """Build a dictionary mapping each word to its frequency.

    WHY lowercase? -- So "The" and "the" count as the same word.
    This is called normalisation.
    """
    freq = {}
    for word in text.lower().split():
        # Strip common punctuation from the edges of each word.
        cleaned = word.strip(".,!?;:\"'()-")
        if cleaned:
            # If the word is already in the dict, add 1; otherwise start at 1.
            if cleaned in freq:
                freq[cleaned] += 1
            else:
                freq[cleaned] = 1
    return freq


def top_words(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """Return the top-n most frequent words as (word, count) pairs.

    WHY sorted with key? -- sorted() can sort by any criterion.
    Using key=lambda item: item[1] sorts by the count (second element).
    reverse=True puts the highest counts first.
    """
    items = list(freq.items())
    items.sort(key=lambda item: item[1], reverse=True)
    return items[:n]


def analyse_text(text: str) -> dict:
    """Run all analyses and return a summary dict."""
    freq = word_frequencies(text)
    top = top_words(freq, 5)

    return {
        "lines": count_lines(text),
        "words": count_words(text),
        "characters": count_characters(text),
        "unique_words": len(freq),
        "top_words": [{"word": w, "count": c} for w, c in top],
    }


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Word Counter Basic")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    text = input_path.read_text(encoding="utf-8")
    summary = analyse_text(text)

    print("=== Word Count Summary ===")
    print(f"  Lines:      {summary['lines']}")
    print(f"  Words:      {summary['words']}")
    print(f"  Characters: {summary['characters']}")
    print(f"  Unique:     {summary['unique_words']}")
    print("\n  Top words:")
    for entry in summary["top_words"]:
        print(f"    {entry['word']}: {entry['count']}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n  Output written to {output_path}")


if __name__ == "__main__":
    main()
