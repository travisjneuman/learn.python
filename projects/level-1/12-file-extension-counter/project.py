"""Level 1 project: File Extension Counter.

Scan a directory tree and count files by extension.
Report the distribution and optionally filter by extension.

Concepts: pathlib.rglob, dictionaries for counting, directory traversal.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def count_extensions(directory: Path) -> dict[str, int]:
    """Count files by extension in a directory tree.

    WHY rglob('*')? -- rglob recursively walks all subdirectories,
    returning every file.  The '*' pattern matches all filenames.
    """
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    counts = {}
    for item in directory.rglob("*"):
        if item.is_file():
            ext = item.suffix.lower() if item.suffix else "(no extension)"
            counts[ext] = counts.get(ext, 0) + 1

    return counts


def count_extensions_from_list(file_paths: list[str]) -> dict[str, int]:
    """Count extensions from a list of file path strings.

    WHY a separate function? -- For testing, we can pass a list of
    path strings without needing actual files on disk.
    """
    counts = {}
    for path_str in file_paths:
        path_str = path_str.strip()
        if not path_str:
            continue
        p = Path(path_str)
        ext = p.suffix.lower() if p.suffix else "(no extension)"
        counts[ext] = counts.get(ext, 0) + 1
    return counts


def sort_by_count(counts: dict[str, int]) -> list[tuple[str, int]]:
    """Sort extensions by count (most common first)."""
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    return items


def format_report(sorted_counts: list[tuple[str, int]]) -> str:
    """Format the extension counts as a table."""
    if not sorted_counts:
        return "  (no files found)"

    total = sum(count for _, count in sorted_counts)
    lines = []

    for ext, count in sorted_counts:
        pct = round(count / total * 100, 1)
        bar = "#" * max(1, int(pct / 2))
        lines.append(f"  {ext:<20} {count:>5}  ({pct:>5.1f}%)  {bar}")

    lines.append(f"\n  Total files: {total}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="File Extension Counter")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="File with path list, or use --dir to scan a directory")
    parser.add_argument("--dir", default=None, help="Directory to scan directly")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.dir:
        counts = count_extensions(Path(args.dir))
    else:
        path = Path(args.input)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")
        lines = path.read_text(encoding="utf-8").splitlines()
        counts = count_extensions_from_list(lines)

    sorted_counts = sort_by_count(counts)

    print("=== File Extension Counter ===\n")
    print(format_report(sorted_counts))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(dict(sorted_counts), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
