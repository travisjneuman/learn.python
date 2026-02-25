"""Level 0 project: First File Reader.

Read a text file and display its contents with line numbers,
plus a summary of line count, word count, and file size.

Concepts: file I/O, Path objects, encoding, error handling.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_file_lines(path: Path) -> list[str]:
    """Read a file and return all lines (preserving blank lines).

    WHY not strip blank lines? -- In a file reader we want to show
    the file exactly as it is, including empty lines.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8").splitlines()


def format_with_line_numbers(lines: list[str]) -> str:
    """Add line numbers to each line for display.

    WHY right-justify the number? -- When files have more than 9 lines,
    lining up the numbers makes the output much easier to read.
    The width is calculated from the total number of lines.
    """
    if not lines:
        return "(empty file)"

    # Figure out how wide the line numbers need to be.
    width = len(str(len(lines)))

    numbered = []
    for i, line in enumerate(lines, start=1):
        # f-string with >{width} right-justifies the number.
        numbered.append(f"  {i:>{width}} | {line}")

    return "\n".join(numbered)


def file_summary(path: Path, lines: list[str]) -> dict:
    """Build a summary dict with stats about the file.

    Includes the file name, line count, word count, character count,
    and file size in bytes.
    """
    text = "\n".join(lines)
    word_count = len(text.split())

    # .stat().st_size gives the file size in bytes on disk.
    size_bytes = path.stat().st_size

    return {
        "file_name": path.name,
        "lines": len(lines),
        "words": word_count,
        "characters": len(text),
        "size_bytes": size_bytes,
        "non_empty_lines": sum(1 for line in lines if line.strip()),
    }


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="First File Reader")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="Path to the file to read")
    parser.add_argument("--output", default="data/output.json",
                        help="Path for the JSON summary")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()

    input_path = Path(args.input)
    lines = read_file_lines(input_path)

    # Display file contents with line numbers.
    print(f"=== Contents of {input_path.name} ===\n")
    print(format_with_line_numbers(lines))

    # Display and save the summary.
    summary = file_summary(input_path, lines)
    print(f"\n=== Summary ===")
    print(f"  Lines:      {summary['lines']} ({summary['non_empty_lines']} non-empty)")
    print(f"  Words:      {summary['words']}")
    print(f"  Characters: {summary['characters']}")
    print(f"  File size:  {summary['size_bytes']} bytes")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n  Summary written to {output_path}")


if __name__ == "__main__":
    main()
