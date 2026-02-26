# Level 4 Mini Capstone — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 4 / Project 15 — Mini Capstone: Full Data Ingestion Pipeline.

Ties together Level 4 skills: schema validation, CSV ingestion with
error recovery, data transformation, checkpoint/recovery, and manifest
generation — all in one end-to-end pipeline.
"""

from __future__ import annotations

import argparse
import csv
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

# ---------- stage 1: validation ----------


def validate_row(row: dict, required_fields: list[str]) -> list[str]:
    """Check a row for missing required fields and empty values.

    WHY: Validation is the first stage because dirty data should never
    reach transformation. Catching problems here prevents garbage-in,
    garbage-out downstream.
    """
    errors: list[str] = []
    for field in required_fields:
        # WHY: Check both "field not in row" and "value is empty" because
        # DictReader returns "" for empty cells, not None.
        if field not in row or not str(row.get(field, "")).strip():
            errors.append(f"missing or empty required field: {field}")
    return errors

# ---------- stage 2: transformation ----------


def transform_row(row: dict) -> dict:
    """Clean and normalize a data row."""
    cleaned = {}
    for key, value in row.items():
        # WHY: Normalize keys to lowercase with underscores so downstream
        # code can use consistent, predictable field names.
        k = key.strip().lower().replace(" ", "_")
        v = value.strip() if isinstance(value, str) else value
        # WHY: CSV values are always strings. Converting "42" to int and
        # "3.14" to float enables downstream numeric operations and
        # produces cleaner JSON output.
        if isinstance(v, str):
            try:
                v = int(v)
            except ValueError:
                try:
                    v = float(v)
                except ValueError:
                    pass
        cleaned[k] = v
    return cleaned

# ---------- stage 3: checkpoint ----------


def load_checkpoint(path: Path) -> dict:
    """Load checkpoint or return default state."""
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass  # corrupt checkpoint — start fresh
    return {"processed_count": 0, "valid": [], "quarantined": []}


def save_checkpoint(path: Path, state: dict) -> None:
    """Persist progress using atomic write-then-rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # WHY: Write to .tmp first and then atomically replace. If the process
    # crashes mid-write, the old checkpoint remains intact.
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state), encoding="utf-8")
    tmp.replace(path)

# ---------- stage 4: manifest ----------


def build_manifest(output_dir: Path, run_id: str) -> dict:
    """Create a manifest of all output files with checksums.

    WHY: The manifest provides an auditable record of exactly what the
    pipeline produced. Checksums let you verify file integrity later.
    """
    files = []
    for f in sorted(output_dir.rglob("*")):
        if f.is_file():
            content = f.read_bytes()
            files.append({
                "name": f.name,
                "size_bytes": len(content),
                "md5": hashlib.md5(content).hexdigest(),
            })
    return {
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
        "files": files,
    }

# ---------- full pipeline ----------


def run_pipeline(
    input_path: Path,
    output_dir: Path,
    required_fields: list[str],
    checkpoint_path: Path | None = None,
    batch_size: int = 10,
) -> dict:
    """Execute the full ingestion pipeline:
    1. Read CSV
    2. Validate each row
    3. Transform valid rows
    4. Checkpoint periodically
    5. Write outputs + manifest
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    # Load CSV
    text = input_path.read_text(encoding="utf-8")
    rows = list(csv.DictReader(text.splitlines()))

    # WHY: Checkpoint recovery ties together the resilience pattern from
    # project 12. If the pipeline crashes mid-run, restarting picks up
    # where it left off instead of reprocessing everything.
    cp_path = checkpoint_path or (output_dir / ".checkpoint.json")
    state = load_checkpoint(cp_path)
    start = state["processed_count"]
    valid_rows = state["valid"]
    quarantined = state["quarantined"]

    if start > 0:
        logging.info("Resuming from checkpoint at row %d", start)

    # WHY: Process rows in a single pass — validate then transform. This
    # avoids reading the data twice and keeps the pipeline linear.
    for i in range(start, len(rows)):
        row = rows[i]
        errors = validate_row(row, required_fields)

        if errors:
            # WHY: row+1 for human-readable row numbers (spreadsheet convention).
            quarantined.append({"row": i + 1, "data": row, "errors": errors})
        else:
            transformed = transform_row(row)
            # WHY: Attach the original row number so transformed data can
            # be traced back to the source file.
            transformed["_row_num"] = i + 1
            valid_rows.append(transformed)

        # Checkpoint periodically to limit re-work on crash
        if (i + 1) % batch_size == 0:
            save_checkpoint(cp_path, {
                "processed_count": i + 1,
                "valid": valid_rows,
                "quarantined": quarantined,
            })

    # Write outputs
    output_dir.mkdir(parents=True, exist_ok=True)

    valid_path = output_dir / "valid_data.json"
    valid_path.write_text(json.dumps(valid_rows, indent=2), encoding="utf-8")

    quarantine_path = output_dir / "quarantined.json"
    quarantine_path.write_text(json.dumps(quarantined, indent=2), encoding="utf-8")

    # WHY: Build the manifest AFTER writing data files so it captures
    # the final output. The manifest itself is then written as a third file.
    run_id = f"capstone_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    manifest = build_manifest(output_dir, run_id)
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # WHY: Clear checkpoint on success to prevent the next run from
    # incorrectly resuming a completed pipeline.
    if cp_path.exists():
        cp_path.unlink()

    summary = {
        "total_rows": len(rows),
        "valid": len(valid_rows),
        "quarantined": len(quarantined),
        "run_id": run_id,
    }
    logging.info(
        "Pipeline complete: %d valid, %d quarantined out of %d total",
        summary["valid"], summary["quarantined"], summary["total_rows"],
    )
    return summary

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Level 4 capstone: full data ingestion pipeline")
    parser.add_argument("--input", default="data/sample_input.csv")
    parser.add_argument("--output-dir", default="data/output")
    parser.add_argument("--required", default="name,age", help="Comma-separated required fields")
    parser.add_argument("--batch-size", type=int, default=10)
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    required = [f.strip() for f in args.required.split(",")]
    summary = run_pipeline(
        Path(args.input), Path(args.output_dir),
        required, batch_size=args.batch_size,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Four-stage pipeline: validate -> transform -> checkpoint -> manifest | Each stage has a single responsibility. Validation catches bad data early. Transformation normalizes the good data. Checkpointing provides crash recovery. The manifest provides an audit trail. |
| Validate before transforming | Dirty data should never reach transformation. If you transform first and then validate, you might normalize a bad value into something that looks valid but is still wrong. |
| Single-pass processing (validate + transform in one loop) | Reading the data once is simpler and faster than making separate passes. Each row is validated, and if it passes, immediately transformed. |
| Manifest generated after all outputs are written | The manifest captures the final state of the output directory. If it were generated before writing, the checksums would be stale. |

## Alternative Approaches

### Using a class-based pipeline with stage objects

```python
class Pipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, name, func):
        self.stages.append((name, func))

    def run(self, data):
        for name, func in self.stages:
            data = func(data)
            logging.info("Stage '%s' complete: %d records", name, len(data))
        return data

pipeline = Pipeline()
pipeline.add_stage("validate", validate_all)
pipeline.add_stage("transform", transform_all)
pipeline.run(rows)
```

**Trade-off:** A class-based pipeline is more extensible (add/remove stages dynamically) and reusable (same pipeline class for different data). However, the capstone's specific flow (validate-then-transform with quarantining and checkpointing) has enough interleaved logic that a linear function is clearer and less over-engineered.

### Separating validation and transformation into independent passes

```python
# Pass 1: validate all rows
valid_rows, quarantined = validate_all(rows, required_fields)

# Pass 2: transform valid rows
transformed = [transform_row(row) for row in valid_rows]
```

**Trade-off:** Separate passes are conceptually cleaner (each pass does one thing) but require storing intermediate results in memory and iterating over the data twice. The single-pass approach in the main solution is more memory-efficient and faster, which matters for large files.

## Common Pitfalls

1. **Not clearing the checkpoint on success** — If the checkpoint file persists after a successful run, the next run will resume from the end and produce empty output. Always delete the checkpoint when the pipeline completes normally.
2. **Building the manifest before writing all output files** — The manifest must reflect the final state. If you generate it before writing `quarantined.json`, that file's checksum will be missing from the manifest.
3. **Forgetting that this capstone combines skills from projects 01-14** — Do not try to implement this from scratch. The validation logic comes from project 01/08, the quarantine pattern from project 03/08, the transformation from project 09, the checkpoint from project 12, and the manifest from project 10. Recognize and reuse these patterns.
