# Run Manifest Generator — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 4 / Project 10 — Run Manifest Generator.

Generates manifest files that document batch run metadata: what files
were processed, file sizes, checksums (MD5), timestamps, and run status.
Useful for auditing and reproducibility.
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

# ---------- manifest helpers ----------


def compute_checksum(path: Path, algorithm: str = "md5") -> str:
    """Compute a hex digest checksum for a file.

    WHY chunk-based reading? Loading a multi-GB file entirely into memory
    would crash the process. Reading in 8 KB chunks keeps memory usage
    constant regardless of file size.
    """
    hasher = hashlib.new(algorithm)
    with path.open("rb") as f:
        # WHY: iter(lambda, sentinel) is a two-argument form of iter()
        # that calls f.read(8192) repeatedly until it returns b"" (end
        # of file). This is more Pythonic than a while-True-break loop.
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def scan_files(directory: Path) -> list[dict]:
    """Scan a directory and collect metadata for each file."""
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    entries: list[dict] = []
    # WHY: rglob("*") recursively scans all subdirectories, unlike
    # iterdir() which only lists immediate children. This matters for
    # nested output directories.
    for file_path in sorted(directory.rglob("*")):
        if not file_path.is_file():
            continue
        stat = file_path.stat()
        entries.append({
            "name": file_path.name,
            # WHY: Store the path relative to the scanned directory so
            # the manifest is portable (works if the directory is moved).
            "relative_path": str(file_path.relative_to(directory)),
            "size_bytes": stat.st_size,
            "checksum_md5": compute_checksum(file_path),
            # WHY: Store modification time as UTC ISO format for
            # unambiguous, timezone-aware timestamps.
            "modified_utc": datetime.fromtimestamp(
                stat.st_mtime, tz=timezone.utc
            ).isoformat(),
        })

    return entries


def build_manifest(
    run_id: str,
    directory: Path,
    status: str = "completed",
) -> dict:
    """Build a complete run manifest for a directory."""
    files = scan_files(directory)
    total_size = sum(f["size_bytes"] for f in files)

    return {
        "run_id": run_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "directory": str(directory),
        "status": status,
        "file_count": len(files),
        "total_size_bytes": total_size,
        "files": files,
    }

# ---------- runner ----------


def run(
    directory: Path,
    output_path: Path,
    run_id: str = "auto",
) -> dict:
    """Generate and write a manifest for a directory."""
    # WHY: Auto-generate a run_id from the current timestamp if none is
    # provided. This ensures every run has a unique identifier for
    # traceability without requiring the user to think of one.
    if run_id == "auto":
        run_id = f"run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"

    manifest = build_manifest(run_id, directory)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    logging.info(
        "Manifest generated: %d files, %d bytes total",
        manifest["file_count"], manifest["total_size_bytes"],
    )
    return manifest

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a run manifest for a directory")
    parser.add_argument("--dir", default="data", help="Directory to scan")
    parser.add_argument("--output", default="data/manifest.json")
    parser.add_argument("--run-id", default="auto", help="Run identifier")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    manifest = run(Path(args.dir), Path(args.output), run_id=args.run_id)
    print(json.dumps({
        "run_id": manifest["run_id"],
        "file_count": manifest["file_count"],
        "total_size_bytes": manifest["total_size_bytes"],
    }, indent=2))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Chunk-based checksum reading (8192 bytes at a time) | Keeps memory usage constant regardless of file size. A 10 GB file would consume 10 GB of RAM if read at once; chunked reading uses only 8 KB. |
| MD5 as the default checksum algorithm | MD5 is fast and widely understood. It is sufficient for integrity checking (detecting accidental corruption). For security-sensitive contexts, SHA-256 should be used instead (see the Alter extension). |
| Store relative paths in the manifest | Makes the manifest portable. If you move the output directory to another machine, the relative paths still work. Absolute paths would break. |
| Auto-generated run_id from timestamp | Every run gets a unique identifier without requiring user input. This is important for auditing — you can trace any output file back to the exact run that created it. |

## Alternative Approaches

### Using `hashlib.file_digest()` (Python 3.11+)

```python
import hashlib

def compute_checksum_modern(path: Path) -> str:
    with path.open("rb") as f:
        digest = hashlib.file_digest(f, "md5")
    return digest.hexdigest()
```

**Trade-off:** `hashlib.file_digest()` was added in Python 3.11 and handles chunked reading internally, making the code cleaner. However, using the manual chunk approach teaches you the underlying pattern and works on older Python versions.

### Using `os.walk()` instead of `Path.rglob()`

```python
import os

def scan_files_walk(directory: str) -> list[dict]:
    entries = []
    for root, dirs, files in os.walk(directory):
        for name in sorted(files):
            full_path = os.path.join(root, name)
            entries.append({"name": name, "path": full_path})
    return entries
```

**Trade-off:** `os.walk()` gives you explicit control over directory traversal (you can modify `dirs` in-place to skip subdirectories). `Path.rglob()` is more concise and Pythonic but less flexible. Both produce the same results for basic use cases.

## Common Pitfalls

1. **Computing checksums on the manifest file itself** — If the manifest is written to the same directory being scanned, and you scan after writing, the manifest will include its own checksum. This creates a chicken-and-egg problem. Write the manifest to a separate location or exclude it from the scan.
2. **Using MD5 for security purposes** — MD5 is cryptographically broken (collisions can be crafted). It is fine for detecting accidental corruption but should not be used to verify file authenticity. Use SHA-256 for security-sensitive applications.
3. **Not handling permission errors** — Some files in a directory may be unreadable due to OS permissions. Without a try/except around the checksum computation, one unreadable file crashes the entire manifest generation.
