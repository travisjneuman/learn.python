# Level 4 Mini Capstone: Data Ingestion Pipeline — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This capstone combines every Level 4 skill, so spend at least 45 minutes attempting it independently.

## Thinking Process

This capstone builds a production-grade data ingestion pipeline with a feature you have not seen before: **checkpoint recovery**. In a real data pipeline, processing might take hours. If it crashes at row 5000 of 10000, you do not want to start over from row 1. Checkpointing saves progress periodically so the pipeline can resume from where it left off.

Plan the pipeline as four stages: **validate** each row against required fields, **transform** valid rows (clean keys, convert numeric strings to actual numbers), **checkpoint** progress periodically, and **manifest** the output files with checksums. Each stage builds on patterns from earlier Level 4 projects -- validation from project 01, transformation from project 09, checkpointing from project 12, and manifests from project 10.

Before coding, think about the data lifecycle: CSV rows arrive as strings. Some rows are invalid and get quarantined (set aside with error messages). Valid rows are transformed (cleaned, type-coerced) and written to output. A manifest records what was produced. If anything goes wrong mid-process, the checkpoint file lets you resume.

## Step 1: Validate Each Row

**What to do:** Write a `validate_row()` function that checks for missing required fields and returns a list of error strings.

**Why:** Validation is the first filter in the pipeline. Invalid rows get quarantined (stored separately with their error messages) rather than silently dropped or allowed through. This means no data is lost -- you can always review and fix quarantined records.

```python
def validate_row(row: dict, required_fields: list[str]) -> list[str]:
    errors: list[str] = []
    for field in required_fields:
        if field not in row or not str(row.get(field, "")).strip():
            errors.append(f"missing or empty required field: {field}")
    return errors
```

This is a simpler validator than project 01's schema engine because the capstone focuses on the pipeline architecture, not validation complexity. You could plug in the full schema validator as an extension.

**Predict:** What is the difference between `field not in row` and `not str(row.get(field, "")).strip()`? Can a field be present but still fail validation?

## Step 2: Transform Valid Rows

**What to do:** Write a `transform_row()` function that normalizes keys (lowercase, underscores) and coerces numeric strings to actual Python numbers.

**Why:** CSV values are always strings. The string `"42"` needs to become the integer `42` for downstream numeric operations, and `"3.14"` needs to become the float `3.14`. Key normalization (`"First Name"` becomes `"first_name"`) makes the data consistent and JSON-friendly.

```python
def transform_row(row: dict) -> dict:
    cleaned = {}
    for key, value in row.items():
        k = key.strip().lower().replace(" ", "_")
        v = value.strip() if isinstance(value, str) else value
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
```

The nested `try/except` pattern is intentional: try `int` first (more specific), fall back to `float`, and leave as string if neither works. This is the "try the strictest conversion first" pattern.

**Predict:** What does `transform_row({"Age": " 25 ", "Name": " Alice "})` produce? Walk through each key-value pair.

## Step 3: Implement Checkpoint Recovery

**What to do:** Write `load_checkpoint()` and `save_checkpoint()` functions that persist pipeline state to a JSON file.

**Why:** This is the capstone's distinguishing feature. If the pipeline crashes at row 500, restarting loads the checkpoint and resumes from row 501. Without checkpointing, you would reprocess all 500 already-completed rows.

```python
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
```

Notice the **atomic write pattern** in `save_checkpoint`: write to a `.tmp` file first, then rename. If the process crashes during the write, you get either the old checkpoint (complete) or the new one (complete) -- never a half-written file that would corrupt the state.

**Predict:** Why does `load_checkpoint` catch `json.JSONDecodeError` and return a fresh state instead of crashing? When would a corrupted checkpoint file occur?

## Step 4: Build the Output Manifest

**What to do:** Write a `build_manifest()` function that inventories all output files with sizes and MD5 checksums.

**Why:** The manifest is an audit trail. It tells downstream consumers exactly what files were produced and lets them verify integrity. If a file gets corrupted during transfer, the MD5 checksum will not match.

```python
import hashlib

def build_manifest(output_dir: Path, run_id: str) -> dict:
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
```

**Predict:** Why does the code use `read_bytes()` instead of `read_text()` for MD5 hashing? What would go wrong with `read_text()`?

## Step 5: Orchestrate the Full Pipeline

**What to do:** Write `run_pipeline()` that chains all stages together with periodic checkpointing.

**Why:** This is where everything comes together. The pipeline loads CSV rows, resumes from checkpoint if available, processes each row through validation and transformation, saves checkpoints every `batch_size` rows, and writes final outputs plus manifest.

```python
def run_pipeline(input_path, output_dir, required_fields,
                 checkpoint_path=None, batch_size=10):
    text = input_path.read_text(encoding="utf-8")
    rows = list(csv.DictReader(text.splitlines()))

    cp_path = checkpoint_path or (output_dir / ".checkpoint.json")
    state = load_checkpoint(cp_path)
    start = state["processed_count"]
    valid_rows = state["valid"]
    quarantined = state["quarantined"]

    for i in range(start, len(rows)):
        errors = validate_row(rows[i], required_fields)
        if errors:
            quarantined.append({"row": i + 1, "data": rows[i], "errors": errors})
        else:
            transformed = transform_row(rows[i])
            transformed["_row_num"] = i + 1
            valid_rows.append(transformed)

        if (i + 1) % batch_size == 0:
            save_checkpoint(cp_path, {
                "processed_count": i + 1,
                "valid": valid_rows,
                "quarantined": quarantined,
            })

    # Write outputs
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "valid_data.json").write_text(
        json.dumps(valid_rows, indent=2), encoding="utf-8")
    (output_dir / "quarantined.json").write_text(
        json.dumps(quarantined, indent=2), encoding="utf-8")

    # Build manifest and clean up checkpoint
    run_id = f"capstone_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    manifest = build_manifest(output_dir, run_id)
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")

    if cp_path.exists():
        cp_path.unlink()  # Clean up checkpoint on success

    return {"total_rows": len(rows), "valid": len(valid_rows),
            "quarantined": len(quarantined), "run_id": run_id}
```

Notice that the checkpoint is **deleted on success**. This is important -- if the checkpoint remains, the next run would try to resume instead of starting fresh.

**Predict:** If `batch_size=3` and there are 8 rows, how many times is `save_checkpoint` called during processing? At which row numbers?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Checkpoint not deleted after success | Forgetting the cleanup step | `cp_path.unlink()` after writing final outputs |
| Writing directly to output file (not atomic) | Simpler to write directly | Use tmp-file-then-rename pattern for crash safety |
| Not resuming from checkpoint | Always starting at row 0 | Load checkpoint state and start from `state["processed_count"]` |
| Numeric coercion breaks on empty strings | `int("")` raises ValueError | The `try/except` chain handles this, but be aware of it |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
6 passed
```

Test from the command line:

```bash
python project.py --input data/sample_input.csv --output-dir data/output --required name,age --batch-size 3
```

Then inspect the output directory:
- `data/output/valid_data.json` -- validated and transformed rows
- `data/output/quarantined.json` -- rejected rows with reasons
- `data/output/manifest.json` -- file inventory with checksums

## What You Learned

- **Checkpoint recovery** lets long-running pipelines resume after failures instead of starting over. The pattern is: save state periodically, load state on startup, clean up state on success.
- **Atomic writes** (write to `.tmp`, then rename) prevent half-written files. This is critical for checkpoints -- a corrupted checkpoint is worse than no checkpoint.
- **Manifests with checksums** provide an audit trail that downstream consumers can verify. This is standard practice in data engineering and file transfer systems.
