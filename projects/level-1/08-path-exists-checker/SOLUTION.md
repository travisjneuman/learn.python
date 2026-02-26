# Solution: Level 1 / Project 08 - Path Exists Checker

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: Path Exists Checker.

Read a list of file/directory paths, check whether each exists,
and report type (file/dir), size, and permissions.

Concepts: pathlib, os.path, file metadata, error handling.
"""


import argparse
import json
from pathlib import Path


# WHY check_path: This is the core function — given a path string,
# it probes the filesystem and returns a structured report of what
# it finds.  Wrapping everything in a dict makes the result easy
# to display and serialise to JSON.
def check_path(path_str: str) -> dict:
    """Check a single path and return its metadata.

    WHY pathlib? -- Path objects provide clean methods like .exists(),
    .is_file(), .is_dir(), and .stat() that work across operating systems.
    """
    # WHY Path(path_str.strip()): Creating a Path object normalises
    # slashes and handles platform differences automatically.
    # Stripping whitespace prevents invisible characters from causing
    # "file not found" errors.
    p = Path(path_str.strip())

    result = {
        "path": str(p),
        "exists": p.exists(),
    }

    # WHY early return for missing: If the path does not exist, there
    # is nothing more to check.  Returning immediately keeps the rest
    # of the function simpler.
    if not p.exists():
        result["type"] = "missing"
        return result

    if p.is_file():
        result["type"] = "file"
        # WHY stat(): The stat() method returns metadata including
        # file size (st_size), modification time, and permissions.
        # This is the same underlying system call used by `ls -l`.
        stat = p.stat()
        result["size_bytes"] = stat.st_size
        result["readable"] = True
        # WHY suffix: Path.suffix returns the file extension including
        # the dot (e.g., ".txt", ".py").  Empty suffix means no extension.
        result["extension"] = p.suffix if p.suffix else "(none)"
    elif p.is_dir():
        result["type"] = "directory"
        # WHY try/except for iterdir: Some directories (like system
        # folders) may deny access.  PermissionError would crash
        # without this guard.
        try:
            items = list(p.iterdir())
            result["item_count"] = len(items)
        except PermissionError:
            result["item_count"] = -1
            result["error"] = "Permission denied"
    else:
        # WHY "other": Handles symbolic links, device files, and
        # other special filesystem objects that are neither regular
        # files nor directories.
        result["type"] = "other"

    return result


# WHY format_size: Raw byte counts like 1048576 are not human-readable.
# Converting to "1.0 MB" makes the output meaningful at a glance.
def format_size(size_bytes: int) -> str:
    """Convert bytes to a human-readable size string.

    WHY loop with units? -- Each iteration divides by 1024 to move
    to the next size unit (B -> KB -> MB -> GB).
    """
    size = float(size_bytes)
    # WHY this list: B, KB, MB, GB covers the range from single bytes
    # to gigabytes.  The loop stops at the first unit where the value
    # is less than 1024, giving the most natural representation.
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    # WHY TB fallback: If the value exceeds GB range, report in TB.
    return f"{size:.1f} TB"


# WHY process_paths: Applies check_path to every path in the list.
# Using a list comprehension with a filter skips blank lines cleanly.
def process_paths(path_list: list[str]) -> list[dict]:
    """Check each path and return results."""
    return [check_path(p) for p in path_list if p.strip()]


# WHY summary: Aggregating the results into counts (existing, missing,
# files, dirs) gives a quick overview without reading every entry.
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


# WHY parse_args: Standard argparse pattern for flexible input/output.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Path Exists Checker")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


# WHY main: Orchestrates the workflow and keeps the module importable.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `pathlib.Path` instead of `os.path` | Path objects are more readable (`p.exists()` vs `os.path.exists(str)`) and work cross-platform with consistent slash handling | `os.path` functions — work fine but are string-based and less Pythonic |
| Return "missing" type instead of None for non-existent paths | Uniform result structure — every path gets a dict with `exists` and `type`, so the display loop does not need special None handling | Return None — caller must check for None before accessing dict keys |
| `format_size()` with a loop over units | Automatically scales to the right unit (B, KB, MB, GB); adding TB is just one more list item | If/elif chain with hardcoded thresholds — more repetitive, harder to extend |
| PermissionError handling in directory counting | Prevents crashes on system directories (e.g., `/root`, `C:\System Volume Information`) that deny access | Let the error propagate — would crash the whole scan on one restricted directory |

## Alternative approaches

### Approach B: Using `os.path` instead of `pathlib`

```python
import os

def check_path_os(path_str: str) -> dict:
    """Check a path using os.path functions instead of pathlib."""
    path_str = path_str.strip()
    result = {"path": path_str, "exists": os.path.exists(path_str)}

    if not result["exists"]:
        result["type"] = "missing"
        return result

    # WHY os.path: Before pathlib (Python 3.4+), all path operations
    # used os.path.  You will still see it in older codebases.
    if os.path.isfile(path_str):
        result["type"] = "file"
        result["size_bytes"] = os.path.getsize(path_str)
        _, ext = os.path.splitext(path_str)
        result["extension"] = ext if ext else "(none)"
    elif os.path.isdir(path_str):
        result["type"] = "directory"
        result["item_count"] = len(os.listdir(path_str))

    return result
```

**Trade-off:** `os.path` works on all Python versions including 2.x and is what many tutorials teach. `pathlib` is the modern approach — it is object-oriented, more readable, and handles cross-platform path separators automatically. Prefer `pathlib` for new code, but recognise `os.path` when reading older codebases.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Path with spaces like `"data/my file (1).txt"` | `Path()` handles spaces correctly; no quoting needed in Python | Using Path objects instead of raw strings avoids shell-quoting issues |
| Restricted system directory like `/root` or `C:\Windows\System32` | `iterdir()` may raise PermissionError; caught by try/except, `item_count` set to -1 | The PermissionError handler is already in place |
| Deeply nested nonexistent path like `/a/b/c/d/e/f.txt` | `p.exists()` returns False; reported as "missing" | Works correctly; `exists()` handles paths of any depth |
| Symbolic link | `p.exists()` follows the link; `p.is_file()` or `p.is_dir()` reports the type of the target, not the link itself | If you need to detect symlinks specifically, use `p.is_symlink()` |

## Key takeaways

1. **`pathlib.Path` is the modern way to work with files in Python.** Methods like `.exists()`, `.is_file()`, `.suffix`, and `.stat()` are cleaner than `os.path` string functions. Use `pathlib` in all new code.
2. **Always handle PermissionError when accessing the filesystem.** Not every file or directory is readable. Deployment scripts, backup tools, and file managers that forget this crash on the first restricted path.
3. **This project connects to deployment scripts and DevOps tools.** Checking that configuration files exist, required directories are in place, and dependencies are installed before starting a service is exactly this pattern. Ansible, Docker health checks, and CI/CD pipelines all do path existence checks.
