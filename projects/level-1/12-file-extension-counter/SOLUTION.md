# Solution: Level 1 / Project 12 - File Extension Counter

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: File Extension Counter.

Scan a directory tree and count files by extension.
Report the distribution and optionally filter by extension.

Concepts: pathlib.rglob, dictionaries for counting, directory traversal.
"""


import argparse
import json
from pathlib import Path


# WHY count_extensions: This is the core function — it walks a
# directory tree recursively and counts how many files have each
# extension.  This teaches directory traversal, which is fundamental
# to build systems, file managers, and deployment tools.
def count_extensions(directory: Path) -> dict[str, int]:
    """Count files by extension in a directory tree.

    WHY rglob('*')? -- rglob recursively walks all subdirectories,
    returning every file.  The '*' pattern matches all filenames.
    """
    # WHY raise NotADirectoryError: If the user passes a file path
    # instead of a directory, rglob would silently return nothing.
    # Raising an explicit error prevents confusion.
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    counts = {}
    for item in directory.rglob("*"):
        # WHY is_file(): rglob returns both files and directories.
        # We only want to count files — directories do not have
        # meaningful extensions.
        if item.is_file():
            # WHY .lower(): Normalising extensions to lowercase means
            # ".PY", ".Py", and ".py" are all counted together.
            # Without this, the same type would appear multiple times.
            ext = item.suffix.lower() if item.suffix else "(no extension)"
            # WHY .get(ext, 0) + 1: Standard counting pattern — get
            # the current count (defaulting to 0) and add 1.
            counts[ext] = counts.get(ext, 0) + 1

    return counts


# WHY count_extensions_from_list: For testing, we need to count
# extensions without real files on disk.  This function takes a list
# of path strings and counts their extensions purely from the names.
def count_extensions_from_list(file_paths: list[str]) -> dict[str, int]:
    """Count extensions from a list of file path strings."""
    counts = {}
    for path_str in file_paths:
        path_str = path_str.strip()
        if not path_str:
            continue
        p = Path(path_str)
        # WHY Path.suffix: Path.suffix extracts the extension
        # including the dot: Path("photo.jpg").suffix returns ".jpg".
        # For files with no extension (like "Makefile"), suffix is "".
        ext = p.suffix.lower() if p.suffix else "(no extension)"
        counts[ext] = counts.get(ext, 0) + 1
    return counts


# WHY sort_by_count: Showing the most common extensions first makes
# the report immediately useful — you see the dominant file types
# at the top.
def sort_by_count(counts: dict[str, int]) -> list[tuple[str, int]]:
    """Sort extensions by count (most common first)."""
    items = list(counts.items())
    # WHY lambda x: x[1]: Each item is a tuple like (".py", 5).
    # x[1] is the count.  reverse=True puts the highest count first.
    items.sort(key=lambda x: x[1], reverse=True)
    return items


# WHY format_report: The bar chart gives a visual sense of the
# distribution.  Percentages add context — "50% of files are .py"
# is more meaningful than "5 files are .py" without knowing the total.
def format_report(sorted_counts: list[tuple[str, int]]) -> str:
    """Format the extension counts as a table."""
    if not sorted_counts:
        return "  (no files found)"

    total = sum(count for _, count in sorted_counts)
    lines = []

    for ext, count in sorted_counts:
        pct = round(count / total * 100, 1)
        # WHY int(pct / 2): Each '#' represents 2%, so 50% gets
        # 25 hashes.  max(1, ...) ensures at least one hash even
        # for very small percentages.
        bar = "#" * max(1, int(pct / 2))
        lines.append(f"  {ext:<20} {count:>5}  ({pct:>5.1f}%)  {bar}")

    lines.append(f"\n  Total files: {total}")
    return "\n".join(lines)


# WHY parse_args: Supports two modes: --input (read path list from
# file) and --dir (scan a directory directly).  This flexibility
# lets users choose the approach that fits their workflow.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="File Extension Counter")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="File with path list, or use --dir to scan a directory")
    parser.add_argument("--dir", default=None, help="Directory to scan directly")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


# WHY main: Orchestrates the workflow — choose input mode, count,
# sort, display, and save.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `rglob("*")` for recursive scanning | Walks the entire directory tree including subdirectories, which is what users expect when counting files in a project | `iterdir()` — only lists the top-level directory, missing nested files |
| Two counting functions (directory scan and path list) | Allows testing without real files; the list-based function can be tested with plain strings | One function that always scans a directory — harder to test, no way to count from a file list |
| Normalise extensions to lowercase | Prevents `.PY` and `.py` from being counted as different types; this is especially important on case-insensitive filesystems (Windows, macOS) | Case-sensitive counting — would over-count on platforms where file extensions vary in case |
| `"(no extension)"` for files without a suffix | Explicitly tracks extensionless files (Makefile, Dockerfile, README) instead of silently ignoring them | Skip extensionless files — would lose data; they are often important files |

## Alternative approaches

### Approach B: Using `collections.Counter`

```python
from collections import Counter
from pathlib import Path

def count_extensions_counter(directory: Path) -> dict[str, int]:
    """Count extensions using Counter — more concise."""
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    # WHY Counter: It is purpose-built for counting.  Pass it an
    # iterable of items and it returns a dict-like object with counts.
    extensions = [
        (f.suffix.lower() if f.suffix else "(no extension)")
        for f in directory.rglob("*")
        if f.is_file()
    ]
    return dict(Counter(extensions))
```

**Trade-off:** Counter reduces the counting logic to two lines. The manual `.get(ext, 0) + 1` approach teaches the underlying pattern — you will encounter situations where Counter is not sufficient (e.g., summing values instead of counting). Learn the manual pattern first, then use Counter as a shortcut.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Empty directory | `count_extensions()` returns `{}`, `format_report()` displays "(no files found)" | The empty-dict case is handled by the `if not sorted_counts` guard |
| Files with double extensions like `archive.tar.gz` | `Path.suffix` returns only `.gz`, not `.tar.gz` | This is by design — Python's Path.suffix only returns the last extension; use `.suffixes` if you need all of them |
| Non-existent directory path | `is_dir()` returns False, `NotADirectoryError` is raised with a clear message | The explicit check before `rglob()` catches this |
| Very large directory tree (thousands of files) | `rglob()` iterates lazily, but `list()` would load everything into memory; counting in a loop is memory-efficient | The loop approach streams results without materialising the full list |

## Key takeaways

1. **`Path.suffix` extracts the file extension including the dot.** `Path("photo.jpg").suffix` returns `".jpg"`. Files without extensions (like `Makefile`) return an empty string. Always normalise with `.lower()` to avoid case-sensitivity issues.
2. **`rglob()` vs `iterdir()` — know the difference.** `iterdir()` lists only the immediate contents of a directory. `rglob("*")` walks the entire tree recursively. Use `rglob` when you need to find all files in a project, and `iterdir` when you only want the top level.
3. **File type distribution analysis connects to real-world tools.** Disk usage analysers (WinDirStat, ncdu), build systems (which files to compile), and code quality tools (how much code vs documentation) all start by counting file types. The count-sort-display pattern you built here is the foundation.
