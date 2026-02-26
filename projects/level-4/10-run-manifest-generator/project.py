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

    WHY chunk-based reading? -- Loading a multi-GB file entirely into
    memory would crash the process. Reading in 8 KB chunks keeps memory
    usage constant regardless of file size.
    """
    hasher = hashlib.new(algorithm)
    with path.open("rb") as f:
        # WHY iter(lambda, sentinel)? -- This two-argument form of iter()
        # calls f.read(8192) repeatedly until it returns b"" (end of file).
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def scan_files(directory: Path) -> list[dict]:
    """Scan a directory and collect metadata for each file.

    Returns a list of dicts with: name, path, size_bytes, checksum, modified.
    """
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    entries: list[dict] = []
    for file_path in sorted(directory.rglob("*")):
        if not file_path.is_file():
            continue
        stat = file_path.stat()
        entries.append({
            "name": file_path.name,
            "relative_path": str(file_path.relative_to(directory)),
            "size_bytes": stat.st_size,
            "checksum_md5": compute_checksum(file_path),
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
    """Build a complete run manifest for a directory.

    The manifest includes run metadata and a file inventory.
    """
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
