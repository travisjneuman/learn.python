# Level 5 Mini Capstone: Operational Pipeline — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This capstone combines every Level 5 skill into one tool, so spend at least 45 minutes attempting it independently.

## Thinking Process

This capstone builds an operational pipeline -- the kind of tool that runs daily in production to extract data from multiple CSV files, transform rows, check for threshold violations, and export results safely. It ties together five Level 5 patterns: layered configuration, multi-file ETL, row transformation, threshold monitoring, and atomic export.

The most important new concept is **layered configuration**. Instead of hardcoded values or a single config file, the pipeline uses three layers: **defaults** (sensible out-of-the-box behavior), **file config** (per-deployment customization), and **environment variables** (runtime overrides). Each layer can override the one below it. This is the twelve-factor app pattern used in modern deployment.

Before coding, think about the complete flow: load config -> extract all CSVs from a directory -> transform each row -> check numeric values against thresholds -> export results atomically. Each stage is a function. The orchestrator calls them in sequence and times the entire run.

## Step 1: Implement Layered Configuration

**What to do:** Write a `load_config()` function that merges defaults, a JSON config file, and environment variables into a single config dict.

**Why:** Defaults mean the tool works without any config file. The config file lets you customize per project or environment. Environment variables let operators override at runtime without editing files (critical in Docker containers and CI systems).

```python
DEFAULTS = {
    "input_dir": "data/sources",
    "output_dir": "data/output",
    "threshold_warn": 50,
    "threshold_crit": 90,
    "max_retries": 3,
}

def load_config(config_path: Path | None = None) -> dict:
    merged = dict(DEFAULTS)

    # Layer 2: file config
    if config_path and config_path.exists():
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        merged.update(raw)

    # Layer 3: env overrides (prefix PIPELINE_)
    for key in DEFAULTS:
        env_val = os.environ.get(f"PIPELINE_{key.upper()}")
        if env_val is not None:
            if isinstance(DEFAULTS[key], int):
                merged[key] = int(env_val)
            else:
                merged[key] = env_val

    return merged
```

Three details to notice:

- **`dict(DEFAULTS)` creates a copy**, so updates do not modify the original defaults.
- **`merged.update(raw)` overwrites** only the keys present in the config file, leaving other defaults intact.
- **Environment variables use the prefix `PIPELINE_`** to avoid conflicts with other system variables. `PIPELINE_THRESHOLD_WARN=80` overrides the `threshold_warn` setting.

**Predict:** If the defaults say `threshold_warn=50`, the config file says `threshold_warn=60`, and the environment has `PIPELINE_THRESHOLD_WARN=80`, what is the final value? Why?

## Step 2: Extract Data from Multiple CSV Files

**What to do:** Write a function that reads all `.csv` files from a directory and combines their rows into one list.

**Why:** Real pipelines often process multiple input files (e.g., one per day, one per source system). Glob-based extraction means you do not need to know the exact filenames -- just drop CSVs into the directory and they get picked up.

```python
def extract_csv_files(input_dir: Path) -> list[dict]:
    all_rows = []
    if not input_dir.exists():
        logging.warning("Input directory does not exist: %s", input_dir)
        return all_rows

    for csv_path in sorted(input_dir.glob("*.csv")):
        with csv_path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
            logging.info("Extracted %d rows from %s", len(rows), csv_path.name)
            all_rows.extend(rows)

    return all_rows
```

Notice that `sorted()` ensures deterministic processing order. Without it, the glob might return files in any order, making the output non-reproducible.

**Predict:** If one CSV file is malformed (e.g., has no header row), what happens? Does `csv.DictReader` crash or produce empty results?

## Step 3: Transform Rows

**What to do:** Write a function that normalizes keys, strips whitespace, and extracts a numeric value for threshold checking.

**Why:** The transformation stage bridges raw CSV data (everything is a string, keys might have inconsistent casing) and the monitoring stage (which needs a clean numeric value to compare against thresholds).

```python
def transform_rows(rows: list[dict]) -> list[dict]:
    transformed = []
    for idx, row in enumerate(rows, start=1):
        cleaned = {}
        for k, v in row.items():
            cleaned[k.strip().lower()] = v.strip() if isinstance(v, str) else v

        # Find a numeric column for threshold checks
        for num_key in ("amount", "value", "score", "metric"):
            if num_key in cleaned:
                try:
                    cleaned["_numeric"] = float(cleaned[num_key])
                except (ValueError, TypeError):
                    cleaned["_numeric"] = 0.0
                break
        else:
            cleaned["_numeric"] = 0.0

        cleaned["_row_index"] = idx
        transformed.append(cleaned)

    return transformed
```

The `for/else` pattern is worth understanding: the `else` block runs only if the `for` loop completes without hitting `break`. This means `_numeric` defaults to 0.0 only when none of the candidate column names are found.

**Predict:** What does the `for/else` construct do here? If a row has both "amount" and "score" columns, which one gets used for `_numeric`?

## Step 4: Check Thresholds

**What to do:** Write a function that evaluates each row's numeric value against warning and critical thresholds.

**Why:** Threshold monitoring is how pipelines detect problems. If a daily sales report suddenly shows a value of 500 when the critical threshold is 90, that is either a data error or a genuine anomaly that needs attention.

```python
def check_thresholds(rows, warn, crit):
    alerts = []
    for row in rows:
        val = row.get("_numeric", 0.0)
        if val >= crit:
            alerts.append({"row": row["_row_index"], "value": val, "level": "critical"})
        elif val >= warn:
            alerts.append({"row": row["_row_index"], "value": val, "level": "warning"})

    return {
        "total_rows": len(rows),
        "warnings": sum(1 for a in alerts if a["level"] == "warning"),
        "criticals": sum(1 for a in alerts if a["level"] == "critical"),
        "alerts": alerts,
    }
```

**Predict:** What happens if `threshold_warn` is set higher than `threshold_crit` (e.g., warn=90, crit=50)? Would a value of 75 be classified as critical, warning, or neither? Is this a bug?

## Step 5: Implement Atomic Export

**What to do:** Write an `atomic_write()` function that writes to a temporary file then renames it to the final path.

**Why:** If the pipeline crashes during the export, the output file would be half-written and corrupt. Atomic writes ensure the file is either complete (from the current run) or complete (from the previous run) -- never truncated.

```python
def atomic_write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(data, encoding="utf-8")
    tmp.replace(path)
```

The `tmp.replace(path)` call is the key. On most filesystems, `replace` is an atomic operation -- either the rename happens completely or it does not happen at all. This is the same pattern databases use for write-ahead logs.

**Predict:** Why use `.replace()` instead of renaming? What is the difference between `Path.rename()` and `Path.replace()` on Windows?

## Step 6: Orchestrate the Full Pipeline

**What to do:** Write `run_pipeline()` that calls each stage in sequence and measures elapsed time.

**Why:** The orchestrator is the backbone that ties everything together. It also times the entire run, which is useful for monitoring pipeline performance over time.

```python
def run_pipeline(config):
    start = time.monotonic()

    # Extract
    rows = extract_csv_files(Path(config["input_dir"]))

    # Transform
    transformed = transform_rows(rows)

    # Monitor thresholds
    threshold_report = check_thresholds(
        transformed,
        warn=config["threshold_warn"],
        crit=config["threshold_crit"],
    )

    elapsed_ms = int((time.monotonic() - start) * 1000)

    summary = {
        "status": "completed",
        "rows_extracted": len(rows),
        "rows_transformed": len(transformed),
        "threshold_report": threshold_report,
        "elapsed_ms": elapsed_ms,
        "config_snapshot": {k: v for k, v in config.items() if not k.startswith("_")},
    }

    # Atomic export
    output_dir = Path(config["output_dir"])
    atomic_write(output_dir / "summary.json", json.dumps(summary, indent=2))

    logging.info("Pipeline complete: %d rows, %d alerts, %dms",
                 len(transformed), len(threshold_report["alerts"]), elapsed_ms)
    return summary
```

Notice `time.monotonic()` instead of `time.time()`. Monotonic clocks are not affected by system clock changes (daylight saving, NTP adjustments), making them reliable for measuring elapsed time.

**Predict:** Why does the summary include a `config_snapshot`? When would you look at it?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Env vars do not override config | Applying env overrides before file config | Apply layers in order: defaults, file, env (env wins) |
| `threshold_warn > threshold_crit` | Config file has inverted values | Validate at config load time; log a warning |
| Non-atomic export | Writing directly to the output file | Use tmp-file-then-replace pattern |
| `time.time()` for elapsed measurement | More familiar than `time.monotonic()` | `monotonic()` is immune to clock changes |
| `_numeric` defaults to 0 silently | No numeric column in the CSV | Log a clear warning when no numeric column is found |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
8 passed
```

Test from the command line:

```bash
python project.py --config data/pipeline_config.json
```

Then inspect `data/output/summary.json` for the complete results, including threshold alerts and timing data.

## What You Learned

- **Layered configuration** (defaults -> file -> env vars) is the twelve-factor app pattern. It makes the same code work across development, staging, and production without code changes.
- **Multi-file ETL extraction** using glob patterns means the pipeline adapts to new input files automatically. No code change needed when a new CSV appears in the input directory.
- **Atomic export** prevents consumers from reading half-written files. Combined with threshold monitoring, this creates a pipeline that is both safe and observable in production.
