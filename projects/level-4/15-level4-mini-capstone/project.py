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
    """Check a row for missing required fields and empty values."""
    errors: list[str] = []
    for field in required_fields:
        if field not in row or not str(row.get(field, "")).strip():
            errors.append(f"missing or empty required field: {field}")
    return errors

# ---------- stage 2: transformation ----------


def transform_row(row: dict) -> dict:
    """Clean and normalize a data row."""
    cleaned = {}
    for key, value in row.items():
        k = key.strip().lower().replace(" ", "_")
        v = value.strip() if isinstance(value, str) else value
        # WHY numeric coercion? -- CSV values are always strings. Converting
        # "42" to int and "3.14" to float enables downstream numeric
        # operations and produces cleaner JSON output.
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
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"processed_count": 0, "valid": [], "quarantined": []}


def save_checkpoint(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state), encoding="utf-8")
    tmp.replace(path)

# ---------- stage 4: manifest ----------


def build_manifest(output_dir: Path, run_id: str) -> dict:
    """Create a manifest of all output files."""
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

    # WHY checkpointing in a capstone? -- This ties together the resilience
    # pattern from project 12. If the pipeline crashes mid-run, restarting
    # picks up where it left off instead of reprocessing everything.
    cp_path = checkpoint_path or (output_dir / ".checkpoint.json")
    state = load_checkpoint(cp_path)
    start = state["processed_count"]
    valid_rows = state["valid"]
    quarantined = state["quarantined"]

    if start > 0:
        logging.info("Resuming from checkpoint at row %d", start)

    # Process rows
    for i in range(start, len(rows)):
        row = rows[i]
        errors = validate_row(row, required_fields)

        if errors:
            quarantined.append({"row": i + 1, "data": row, "errors": errors})
        else:
            transformed = transform_row(row)
            transformed["_row_num"] = i + 1
            valid_rows.append(transformed)

        # Checkpoint every batch_size rows
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

    # Build manifest
    run_id = f"capstone_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    manifest = build_manifest(output_dir, run_id)
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Clear checkpoint on success
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
