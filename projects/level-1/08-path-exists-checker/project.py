"""Level 1 project: Path Exists Checker.

Read a list of file/directory paths, check whether each exists,
and report type (file/dir), size, and permissions.

Concepts: pathlib, os.path, file metadata, error handling.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def check_path(path_str: str) -> dict:
    """Check a single path and return its metadata.

    WHY pathlib? -- Path objects provide clean methods like .exists(),
    .is_file(), .is_dir(), and .stat() that work across operating systems.
    """
    p = Path(path_str.strip())

    result = {
        "path": str(p),
        "exists": p.exists(),
    }

    if not p.exists():
        result["type"] = "missing"
        return result

    if p.is_file():
        result["type"] = "file"
        stat = p.stat()
        result["size_bytes"] = stat.st_size
        result["readable"] = True  # If we can stat it, we can read it.
        result["extension"] = p.suffix if p.suffix else "(none)"
    elif p.is_dir():
        result["type"] = "directory"
        # Count items in the directory.
        try:
            items = list(p.iterdir())
            result["item_count"] = len(items)
        except PermissionError:
            result["item_count"] = -1
            result["error"] = "Permission denied"
    else:
        result["type"] = "other"

    return result


def format_size(size_bytes: int) -> str:
    """Convert bytes to a human-readable size string.

    WHY loop with units? -- Each iteration divides by 1024 to move
    to the next size unit (B -> KB -> MB -> GB).
    """
    size = float(size_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def process_paths(path_list: list[str]) -> list[dict]:
    """Check each path and return results."""
    return [check_path(p) for p in path_list if p.strip()]


def summary(results: list[dict]) -> dict:
    """Build a summary of path check results."""
    existing = [r for r in results if r["exists"]]
    missing = [r for r in results if not r["exists"]]
    files = [r for r in existing if r["type"] == "file"]
    dirs = [r for r in existing if r["type"] == "directory"]

    return {
        "total_checked": len(results),
        "existing": len(existing),
        "missing": len(missing),
        "files": len(files),
        "directories": len(dirs),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Path Exists Checker")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    paths = input_path.read_text(encoding="utf-8").splitlines()
    results = process_paths(paths)
    stats = summary(results)

    print("=== Path Exists Checker ===\n")
    for r in results:
        if r["type"] == "missing":
            print(f"  MISSING  {r['path']}")
        elif r["type"] == "file":
            size = format_size(r.get("size_bytes", 0))
            print(f"  FILE     {r['path']}  ({size})")
        elif r["type"] == "directory":
            count = r.get("item_count", "?")
            print(f"  DIR      {r['path']}  ({count} items)")

    print(f"\n  {stats['existing']} exist, {stats['missing']} missing "
          f"({stats['files']} files, {stats['directories']} dirs)")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"results": results, "summary": stats}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
