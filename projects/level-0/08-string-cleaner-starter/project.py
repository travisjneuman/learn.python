"""Level 0 project: String Cleaner Starter.

Read messy strings from a file and apply cleaning transformations:
strip whitespace, normalise case, remove special characters, collapse spaces.

Concepts: string methods (strip, lower, replace), loops, character filtering.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def strip_whitespace(text: str) -> str:
    """Remove leading and trailing whitespace from a string.

    WHY strip? -- User input and file data often have invisible
    spaces or tabs at the beginning or end.  strip() removes them.
    """
    return text.strip()


def normalise_case(text: str) -> str:
    """Convert a string to lowercase.

    WHY lowercase? -- Normalising case makes comparisons simpler.
    'Hello' and 'hello' become the same string.
    """
    return text.lower()


def remove_special_characters(text: str) -> str:
    """Keep only letters, digits, and spaces.

    WHY check each character? -- We loop through the string and
    keep only the characters we want.  isalnum() checks if a
    character is a letter or digit.
    """
    cleaned = []
    for char in text:
        # Keep letters, digits, and spaces.
        if char.isalnum() or char == " ":
            cleaned.append(char)
    # Join the list back into a single string.
    return "".join(cleaned)


def collapse_spaces(text: str) -> str:
    """Replace multiple consecutive spaces with a single space.

    WHY a while loop? -- We keep replacing double-spaces until none
    remain.  This is a simple approach that handles any number of
    consecutive spaces.
    """
    while "  " in text:
        text = text.replace("  ", " ")
    return text


def clean_string(text: str) -> str:
    """Apply all cleaning steps in order.

    WHY chain steps? -- Each function does one small job.
    Chaining them together creates a pipeline where the output
    of one step becomes the input of the next.
    """
    result = strip_whitespace(text)
    result = normalise_case(result)
    result = remove_special_characters(result)
    result = collapse_spaces(result)
    return result


def process_file(path: Path) -> list[dict]:
    """Read lines from a file and clean each one.

    Returns a list of dicts showing the before and after for each line.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    results = []

    for line in lines:
        if not line.strip():
            continue
        results.append({
            "original": line,
            "cleaned": clean_string(line),
        })

    return results


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="String Cleaner Starter")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()
    results = process_file(Path(args.input))

    print("=== String Cleaning Results ===\n")
    for r in results:
        print(f"  BEFORE: {r['original']!r}")
        print(f"  AFTER:  {r['cleaned']!r}")
        print()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"{len(results)} lines cleaned. Output written to {output_path}")


if __name__ == "__main__":
    main()
