"""Level 5 / Project 14 — Change Detection Tool.

Detects changes between file versions using content hashing,
line-by-line diffs, and timestamp comparison.  Reports what
changed, when, and how much.

Concepts practiced:
- SHA-256 hashing for content integrity checks
- Set-based line diffing (added, removed, unchanged)
- File metadata comparison (size, modification time)
- Handling edge cases (missing files, identical paths, binary content)
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
    """Set up logging so every change detection step is traceable."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


# ---------- hashing ----------


def file_hash(path: Path) -> str:
    """Compute the SHA-256 hash of a file's contents.

    Uses ``read_bytes()`` so that binary files are handled correctly
    without encoding assumptions.
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_binary_file(path: Path, sample_size: int = 8192) -> bool:
    """Detect whether a file is binary by checking for null bytes.

    Reads the first *sample_size* bytes and looks for ``\\x00``.
    This is the same heuristic used by Git.
    """
    sample = path.read_bytes()[:sample_size]
    return b"\x00" in sample


# ---------- line diffing ----------


def line_diff(old_lines: list[str], new_lines: list[str]) -> dict:
    """Compute a simple line-based diff between two file versions.

    Uses set operations to find added, removed, and unchanged lines.
    This does not track moved lines — it treats each line as either
    present or absent.
    """
    old_set = set(old_lines)
    new_set = set(new_lines)

    added = sorted(new_set - old_set)
    removed = sorted(old_set - new_set)
    unchanged_count = len(old_set & new_set)

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

    Handles several edge cases:
    - Old file missing -> status ``new_file``
    - New file missing -> status ``deleted``
    - Identical hashes -> status ``unchanged``
    - Same path for old and new -> status ``unchanged`` (short-circuit)
    - Binary files -> hash comparison only (no line diff)
    - Text files -> full line-level diff
    """
    result: dict = {"old_file": str(old_path), "new_file": str(new_path)}

    # Edge case: both paths point to the same file.
    if old_path.resolve() == new_path.resolve() and old_path.exists():
        result["status"] = "unchanged"
        result["old_hash"] = file_hash(old_path)
        result["new_hash"] = result["old_hash"]
        logging.info("Same path — no changes possible")
        return result

    # Missing file cases.
    if not old_path.exists():
        result["status"] = "new_file"
        result["new_hash"] = file_hash(new_path) if new_path.exists() else None
        return result

    if not new_path.exists():
        result["status"] = "deleted"
        result["old_hash"] = file_hash(old_path)
        return result

    # Both exist — compare hashes.
    old_hash = file_hash(old_path)
    new_hash = file_hash(new_path)
    result["old_hash"] = old_hash
    result["new_hash"] = new_hash

    if old_hash == new_hash:
        result["status"] = "unchanged"
        return result

    # Hashes differ — report details.
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

    # Skip line-level diff for binary files.
    if is_binary_file(old_path) or is_binary_file(new_path):
        result["binary"] = True
        logging.info("Binary file detected — skipping line diff")
        return result

    old_lines = old_path.read_text(encoding="utf-8", errors="replace").splitlines()
    new_lines = new_path.read_text(encoding="utf-8", errors="replace").splitlines()
    result["diff"] = line_diff(old_lines, new_lines)

    return result


# ---------- pipeline ----------


def run(old_path: Path, new_path: Path, output_path: Path) -> dict:
    """Execute change detection and write the report."""
    report = detect_changes(old_path, new_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Change detection: %s", report["status"])
    return report


# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the change detection tool."""
    parser = argparse.ArgumentParser(
        description="Detect changes between file versions",
    )
    parser.add_argument("--old", default="data/old_version.txt", help="Baseline file")
    parser.add_argument("--new", default="data/new_version.txt", help="Current file")
    parser.add_argument("--output", default="data/change_report.json", help="Report output path")
    return parser.parse_args()


def main() -> None:
    """Entry point: configure logging, parse args, detect changes."""
    configure_logging()
    args = parse_args()
    report = run(Path(args.old), Path(args.new), Path(args.output))
    print(f"Change detection: {report['status']}")


if __name__ == "__main__":
    main()
