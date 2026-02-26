# Change Detection Tool — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 5 / Project 14 — Change Detection Tool.

Detects changes between file versions using content hashing,
line-by-line diffs, and timestamp comparison.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- hashing ----------

def file_hash(path: Path) -> str:
    """Compute the SHA-256 hash of a file's contents.

    WHY SHA-256? -- It produces a fixed-length 64-character hex string
    regardless of file size. Comparing two hashes is O(1), while
    comparing two files byte-by-byte is O(n). If the hashes match,
    the files are identical (with astronomically high probability).
    """
    # WHY: read_bytes() handles binary files correctly without
    # encoding assumptions. Text files are also just bytes.
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_binary_file(path: Path, sample_size: int = 8192) -> bool:
    """Detect whether a file is binary by checking for null bytes.

    WHY the null-byte heuristic? -- Text files virtually never contain
    null bytes (\\x00), while binary formats (images, executables) do.
    Git uses this same check to decide whether to show diffs.
    """
    sample = path.read_bytes()[:sample_size]
    return b"\x00" in sample

# ---------- line diffing ----------

def line_diff(old_lines: list[str], new_lines: list[str]) -> dict:
    """Compute a simple line-based diff between two file versions.

    WHY sets instead of line-by-line comparison? -- Set operations
    (intersection, difference) identify added and removed lines in
    O(n) time. Ordered diffing (like `difflib`) is O(n*m) but shows
    where lines moved. The set approach is simpler and sufficient
    for "what changed?" without needing "where did it move?"
    """
    old_set = set(old_lines)
    new_set = set(new_lines)

    added = sorted(new_set - old_set)
    removed = sorted(old_set - new_set)
    unchanged_count = len(old_set & new_set)

    # WHY: max(..., 1) prevents division by zero when both files are empty.
    total_lines = max(len(old_lines), len(new_lines), 1)
    change_pct = round(
        (len(added) + len(removed)) / total_lines * 100, 1,
    )

    return {
        "added": added,
        "removed": removed,
        "added_count": len(added),
        "removed_count": len(removed),
        "unchanged_count": unchanged_count,
        "change_percentage": change_pct,
    }

# ---------- change detection ----------

def detect_changes(old_path: Path, new_path: Path) -> dict:
    """Compare two files and return a structured change report.

    Handles edge cases: missing files, identical paths, binary content.
    """
    result: dict = {"old_file": str(old_path), "new_file": str(new_path)}

    # WHY: Short-circuit when both paths resolve to the same file.
    # No comparison needed — the file is identical to itself.
    if old_path.resolve() == new_path.resolve() and old_path.exists():
        result["status"] = "unchanged"
        result["old_hash"] = file_hash(old_path)
        result["new_hash"] = result["old_hash"]
        logging.info("Same path — no changes possible")
        return result

    # WHY: Handle missing-file cases before computing hashes.
    # A new file (old missing) or deleted file (new missing) are
    # distinct statuses from "modified."
    if not old_path.exists():
        result["status"] = "new_file"
        result["new_hash"] = file_hash(new_path) if new_path.exists() else None
        return result

    if not new_path.exists():
        result["status"] = "deleted"
        result["old_hash"] = file_hash(old_path)
        return result

    # Both exist — compare hashes first (fast O(1) check).
    old_hash = file_hash(old_path)
    new_hash = file_hash(new_path)
    result["old_hash"] = old_hash
    result["new_hash"] = new_hash

    if old_hash == new_hash:
        result["status"] = "unchanged"
        return result

    # Hashes differ — report detailed changes.
    result["status"] = "modified"

    old_stat = old_path.stat()
    new_stat = new_path.stat()
    result["size_change"] = new_stat.st_size - old_stat.st_size
    result["old_modified"] = datetime.fromtimestamp(
        old_stat.st_mtime, tz=timezone.utc,
    ).isoformat()
    result["new_modified"] = datetime.fromtimestamp(
        new_stat.st_mtime, tz=timezone.utc,
    ).isoformat()

    # WHY: Skip line-level diff for binary files. Binary content
    # produces meaningless "lines" and huge diffs.
    if is_binary_file(old_path) or is_binary_file(new_path):
        result["binary"] = True
        logging.info("Binary file detected — skipping line diff")
        return result

    # WHY: errors="replace" handles files with mixed encodings
    # by substituting undecodable bytes with the Unicode replacement
    # character instead of crashing.
    old_lines = old_path.read_text(encoding="utf-8", errors="replace").splitlines()
    new_lines = new_path.read_text(encoding="utf-8", errors="replace").splitlines()
    result["diff"] = line_diff(old_lines, new_lines)

    return result

# ---------- pipeline ----------

def run(old_path: Path, new_path: Path, output_path: Path) -> dict:
    report = detect_changes(old_path, new_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Change detection: %s", report["status"])
    return report

# ---------- CLI ----------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect changes between file versions")
    parser.add_argument("--old", default="data/old_version.txt")
    parser.add_argument("--new", default="data/new_version.txt")
    parser.add_argument("--output", default="data/change_report.json")
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.old), Path(args.new), Path(args.output))
    print(f"Change detection: {report['status']}")

if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| SHA-256 hash comparison before line diff | Hashing is O(n) for file size but the comparison is O(1). If hashes match, the files are identical and we skip the more expensive line diff entirely. This is the same optimization git uses. |
| Set-based line diff instead of ordered diff | Set operations find added/removed lines in O(n) time. `difflib.unified_diff` preserves order but is O(n*m). The set approach is sufficient for "what changed?" without needing move detection. |
| Null-byte binary detection | The null-byte heuristic is simple, fast, and matches git's behavior. Binary files produce meaningless line diffs, so skipping them prevents confusing output. |
| `errors="replace"` for text reading | Files with mixed encodings (e.g., UTF-8 with a few Latin-1 characters) would crash with strict decoding. Replacing undecodable bytes keeps the diff working, with the tradeoff of some garbled characters. |

## Alternative Approaches

### Using `difflib` for ordered diffs

```python
import difflib

def ordered_diff(old_lines, new_lines):
    diff = list(difflib.unified_diff(
        old_lines, new_lines,
        fromfile="old", tofile="new",
        lineterm="",
    ))
    return "\n".join(diff)
```

`difflib.unified_diff` produces git-style diffs that show exactly where lines were added, removed, or moved. This is more informative but computationally more expensive and produces larger output.

## Common Pitfalls

1. **Comparing binary files as text** — Reading a PNG file with `read_text()` produces garbage lines. The binary detection check prevents this, but forgetting it leads to massive, meaningless diffs.
2. **Duplicate lines break set-based diff** — If a file has the same line repeated 5 times, the set only sees it once. Adding a 6th occurrence of that line would not appear in the "added" set. For production diffing, use `collections.Counter` or `difflib`.
3. **Same path for --old and --new** — Without the `resolve()` short-circuit, the tool would hash the file twice and report "unchanged," which is correct but wasteful. The short-circuit also prevents confusing output when someone accidentally passes the same file for both arguments.
