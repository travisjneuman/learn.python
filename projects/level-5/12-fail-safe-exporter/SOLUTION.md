# Fail-Safe Exporter — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 5 / Project 12 — Fail-Safe Exporter.

Exports data with atomic writes and rollback on failure.
Writes to a temp file first, then renames on success.
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
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- atomic write helpers ----------

# WHY atomic writes? -- If the process crashes while writing, a partially
# written file corrupts the data. "Write-to-temp, then rename" guarantees
# the target file is either the old complete version or the new complete
# version — never a half-written mix. rename() is atomic on most
# filesystems (POSIX guarantees it).

def atomic_write_json(data: object, path: Path) -> None:
    """Write JSON atomically: write to .tmp, then rename."""
    tmp_path = path.with_suffix(".tmp")
    try:
        content = json.dumps(data, indent=2, ensure_ascii=False)
        tmp_path.write_text(content, encoding="utf-8")
        # WHY: .replace() overwrites the target atomically. Unlike
        # writing directly to the target, a crash here leaves only
        # the .tmp file — the original is untouched.
        tmp_path.replace(path)
        logging.info("Atomic JSON write to %s (%d bytes)", path, len(content))
    except Exception:
        # WHY: Clean up the temp file on failure so it does not
        # accumulate as garbage on repeated failed exports.
        if tmp_path.exists():
            tmp_path.unlink()
        raise


def atomic_write_csv(rows: list[dict], path: Path) -> None:
    """Write CSV atomically: write to .tmp, then rename."""
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    # WHY: Collect all unique keys across all rows. If some rows are
    # missing columns, DictWriter's restval="" fills them with empty
    # strings instead of crashing.
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

    WHY validate before writing? -- Catching errors before the write
    means we never create a partial or malformed output file. The
    validation is cheap; the write is expensive and hard to undo.
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
    """If *path* exists, copy it to path.bak before overwriting.

    WHY backup? -- Even with atomic writes, the new data might be
    wrong (e.g., a bug in the transform step). Having the previous
    version as .bak lets operators roll back quickly.
    """
    if not path.exists():
        return None
    backup_path = path.with_suffix(path.suffix + ".bak")
    # WHY: shutil.copy2 preserves metadata (timestamps, permissions).
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
    """Export data in the specified format with atomic writes."""
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
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    data = json.loads(input_path.read_text(encoding="utf-8"))
    result = export_data(data, output_path, fmt=fmt)
    logging.info("Export result: %s — %d records", result["status"], result.get("exported", 0))
    return result

# ---------- CLI ----------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fail-safe data exporter with atomic writes")
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/exported.json")
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    result = run(Path(args.input), Path(args.output), args.format)
    print(f"Exported {result.get('exported', 0)} records to {result.get('path', 'N/A')} (atomic write)")

if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Write to `.tmp` then rename | `Path.replace()` is atomic on POSIX filesystems. If the process crashes during write, the original file is untouched. The worst case is an orphaned `.tmp` file, which is cleaned up on the next attempt. |
| Clean up `.tmp` on failure | If `json.dumps` raises (e.g., non-serializable data), the partial `.tmp` file is deleted so it does not accumulate as garbage or confuse future runs. |
| Collect all keys for CSV headers | Real data often has inconsistent keys across rows. `DictWriter` with `restval=""` fills missing columns with empty strings, producing a valid CSV instead of crashing. |
| Validate before writing | Catching data issues (non-dict rows, non-list input) before the write means we never create a corrupt output file. Validation is cheap; cleaning up a bad write is expensive. |

## Alternative Approaches

### Using `tempfile.NamedTemporaryFile`

```python
import tempfile

def atomic_write_safe(data: str, path: Path) -> None:
    with tempfile.NamedTemporaryFile(
        mode="w", dir=path.parent, suffix=".tmp", delete=False
    ) as f:
        f.write(data)
        temp_path = Path(f.name)
    temp_path.replace(path)
```

`NamedTemporaryFile` generates a unique filename, avoiding collisions if two processes export simultaneously. The `dir=path.parent` ensures the temp file is on the same filesystem as the target (required for atomic rename).

## Common Pitfalls

1. **Atomic rename across filesystems** — `Path.replace()` only works atomically when source and target are on the same filesystem. Writing `.tmp` to `/tmp/` and renaming to `/data/` will copy-then-delete, which is not atomic. Always place the temp file in the same directory as the target.
2. **CSV with inconsistent keys** — If row 1 has keys `["a", "b"]` and row 2 has `["a", "c"]`, a naive `DictWriter` using `rows[0].keys()` as headers will crash on row 2's extra key. Collecting all keys from all rows first prevents this.
3. **No backup before overwrite** — Atomic writes protect against crashes, but not against bugs. If the new data is wrong, without a `.bak` file there is no way to recover the previous version.
