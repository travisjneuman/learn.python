"""Level 5 / Project 12 — Fail-Safe Exporter.

Exports data with atomic writes and rollback on failure.
Writes to a temp file first, then renames on success.
If export fails, the original file is preserved untouched.

Concepts practiced:
- Atomic file operations (write-to-temp then rename)
- Multi-format export (JSON and CSV)
- Pre-export validation to catch errors early
- Backup creation before overwriting existing files
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import shutil
from pathlib import Path


# ---------- logging ----------

def configure_logging() -> None:
    """Set up logging so every export operation is traceable."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


# ---------- atomic write helpers ----------

# The "atomic write" pattern writes data to a temporary file first,
# then uses rename (which is atomic on most filesystems) to replace
# the target.  If anything fails, the temp file is cleaned up and
# the original target is never touched.


def atomic_write_json(data: object, path: Path) -> None:
    """Write JSON atomically: write to ``.tmp``, then rename."""
    tmp_path = path.with_suffix(".tmp")
    try:
        content = json.dumps(data, indent=2, ensure_ascii=False)
        tmp_path.write_text(content, encoding="utf-8")
        # Rename replaces the target atomically.
        tmp_path.replace(path)
        logging.info("Atomic JSON write to %s (%d bytes)", path, len(content))
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


def atomic_write_csv(rows: list[dict], path: Path) -> None:
    """Write CSV atomically: write to ``.tmp``, then rename.

    Headers are derived from the keys of the first row.  If rows
    have inconsistent keys, missing values are written as empty strings.
    """
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    # Collect all unique keys across rows to handle inconsistent records.
    all_keys: list[str] = list(rows[0].keys())
    seen = set(all_keys)
    for row in rows[1:]:
        for key in row:
            if key not in seen:
                all_keys.append(key)
                seen.add(key)

    tmp_path = path.with_suffix(".tmp")
    try:
        with tmp_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=all_keys, restval="")
            writer.writeheader()
            writer.writerows(rows)
        tmp_path.replace(path)
        logging.info("Atomic CSV write to %s (%d rows)", path, len(rows))
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


# ---------- validation ----------


def validate_records(data: list[dict]) -> list[str]:
    """Validate export data before writing.

    Returns a list of error messages (empty list means valid).
    """
    errors: list[str] = []
    if not isinstance(data, list):
        errors.append("data must be a list")
        return errors
    for i, row in enumerate(data):
        if not isinstance(row, dict):
            errors.append(f"row {i}: expected dict, got {type(row).__name__}")
    return errors


# ---------- backup ----------


def create_backup(path: Path) -> Path | None:
    """If *path* exists, copy it to ``path.bak`` before overwriting.

    Returns the backup path or None if no backup was needed.
    """
    if not path.exists():
        return None
    backup_path = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup_path)
    logging.info("Created backup: %s", backup_path)
    return backup_path


# ---------- export pipeline ----------


def export_data(
    data: list[dict],
    output_path: Path,
    fmt: str = "json",
    validate: bool = True,
    backup: bool = False,
) -> dict:
    """Export data in the specified format with atomic writes.

    Returns a status dict with the outcome, count, and any errors.
    """
    if validate:
        errors = validate_records(data)
        if errors:
            return {"status": "validation_failed", "errors": errors, "exported": 0}

    output_path.parent.mkdir(parents=True, exist_ok=True)

    backup_path = None
    if backup:
        backup_path = create_backup(output_path)

    if fmt == "csv":
        atomic_write_csv(data, output_path)
    else:
        atomic_write_json(data, output_path)

    result: dict = {
        "status": "success",
        "exported": len(data),
        "format": fmt,
        "path": str(output_path),
    }
    if backup_path:
        result["backup"] = str(backup_path)

    return result


# ---------- pipeline ----------


def run(input_path: Path, output_path: Path, fmt: str = "json") -> dict:
    """Load input JSON, validate, and export atomically."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    data = json.loads(input_path.read_text(encoding="utf-8"))
    result = export_data(data, output_path, fmt=fmt)
    logging.info("Export result: %s — %d records", result["status"], result.get("exported", 0))
    return result


# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the fail-safe exporter."""
    parser = argparse.ArgumentParser(
        description="Fail-safe data exporter with atomic writes",
    )
    parser.add_argument("--input", default="data/sample_input.json", help="Input JSON file")
    parser.add_argument("--output", default="data/exported.json", help="Output file path")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Export format")
    return parser.parse_args()


def main() -> None:
    """Entry point: configure logging, parse args, run the exporter."""
    configure_logging()
    args = parse_args()
    result = run(Path(args.input), Path(args.output), args.format)
    print(f"Exported {result.get('exported', 0)} records to {result.get('path', 'N/A')} (atomic write)")


if __name__ == "__main__":
    main()
