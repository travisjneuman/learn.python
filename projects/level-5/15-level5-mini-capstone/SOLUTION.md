# Level 5 Mini Capstone — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 5 / Project 15 — Mini Capstone: Operational Pipeline.

Combines config loading, multi-file ETL extraction, row transformation,
threshold monitoring, atomic export, and structured run logging into a
single end-to-end pipeline. This capstone ties together every Level 5
skill in one realistic script.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import time
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def configure_logging() -> None:
    """Set up consistent log format for pipeline diagnostics."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------------------------------------------------------------------------
# 1. Layered configuration  (env > file > defaults)
# ---------------------------------------------------------------------------

# WHY: Defaults ensure the pipeline runs out of the box. File config
# customizes per deployment. Env vars override at runtime. This is
# the twelve-factor app pattern practiced in Project 04.
DEFAULTS: dict[str, Any] = {
    "input_dir": "data/sources",
    "output_dir": "data/output",
    "threshold_warn": 50,
    "threshold_crit": 90,
    "max_retries": 3,
}

def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Merge defaults, file config, and environment overrides."""
    merged = dict(DEFAULTS)

    # Layer 2: file config
    if config_path and config_path.exists():
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        merged.update(raw)

    # Layer 3: env overrides (prefix PIPELINE_)
    # WHY: The PIPELINE_ prefix prevents collisions with unrelated env vars.
    for key in DEFAULTS:
        env_val = os.environ.get(f"PIPELINE_{key.upper()}")
        if env_val is not None:
            # WHY: Coerce to int if the default is int, so threshold
            # comparisons work correctly (50 < 90 vs "50" < "90").
            if isinstance(DEFAULTS[key], int):
                merged[key] = int(env_val)
            else:
                merged[key] = env_val

    return merged

# ---------------------------------------------------------------------------
# 2. Multi-file ETL extraction (from Project 03)
# ---------------------------------------------------------------------------

def extract_csv_files(input_dir: Path) -> list[dict]:
    """Read all .csv files from input_dir and return combined rows."""
    all_rows: list[dict] = []
    if not input_dir.exists():
        # WHY: Log and return empty rather than crashing. The pipeline
        # summary will show "0 rows extracted" which is a clear signal.
        logging.warning("Input directory does not exist: %s", input_dir)
        return all_rows

    for csv_path in sorted(input_dir.glob("*.csv")):
        with csv_path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
            logging.info("Extracted %d rows from %s", len(rows), csv_path.name)
            all_rows.extend(rows)

    return all_rows

# ---------------------------------------------------------------------------
# 3. Row transformation (from Project 05)
# ---------------------------------------------------------------------------

def transform_rows(rows: list[dict]) -> list[dict]:
    """Normalize and enrich each row with a computed '_numeric' field."""
    transformed: list[dict] = []
    for idx, row in enumerate(rows, start=1):
        # WHY: Normalize keys (strip + lowercase) so "Amount" and "amount"
        # are treated as the same column. This is the same pattern from
        # the ETL runner (Project 03).
        cleaned: dict[str, Any] = {}
        for k, v in row.items():
            cleaned[k.strip().lower()] = v.strip() if isinstance(v, str) else v

        # WHY: Try multiple common numeric column names so the pipeline
        # works with different CSV schemas without configuration.
        for num_key in ("amount", "value", "score", "metric"):
            if num_key in cleaned:
                try:
                    cleaned["_numeric"] = float(cleaned[num_key])
                except (ValueError, TypeError):
                    cleaned["_numeric"] = 0.0
                break
        else:
            # WHY: Default to 0.0 when no numeric column is found. This
            # prevents threshold checks from crashing on non-numeric data.
            cleaned["_numeric"] = 0.0

        cleaned["_row_index"] = idx
        transformed.append(cleaned)

    return transformed

# ---------------------------------------------------------------------------
# 4. Threshold monitoring (from Project 02)
# ---------------------------------------------------------------------------

def check_thresholds(
    rows: list[dict],
    warn: int | float,
    crit: int | float,
) -> dict[str, Any]:
    """Evaluate each row's _numeric value against warn/crit thresholds.

    WHY: Same pattern as the Alert Threshold Monitor (Project 02) —
    check critical first, then warning, to get the most severe match.
    """
    alerts: list[dict] = []
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

# ---------------------------------------------------------------------------
# 5. Atomic export (from Project 12)
# ---------------------------------------------------------------------------

def atomic_write(path: Path, data: str) -> None:
    """Write data to a temp file then rename for crash safety.

    WHY: Same pattern as the Fail-Safe Exporter (Project 12). If the
    pipeline crashes mid-export, consumers see either the previous
    complete version or the new complete version.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(data, encoding="utf-8")
    tmp.replace(path)

# ---------------------------------------------------------------------------
# 6. Pipeline orchestrator
# ---------------------------------------------------------------------------

def run_pipeline(config: dict[str, Any]) -> dict[str, Any]:
    """Execute the full ETL + monitoring pipeline and return summary.

    WHY: This function orchestrates the entire pipeline in a linear
    flow: extract -> transform -> monitor -> export. Each stage uses
    patterns learned in earlier projects.
    """
    # WHY: time.monotonic() is immune to system clock changes (NTP adjustments,
    # daylight saving). It is the correct clock for measuring durations.
    start = time.monotonic()

    # Extract
    input_dir = Path(config["input_dir"])
    rows = extract_csv_files(input_dir)

    # Transform
    transformed = transform_rows(rows)

    # Monitor thresholds
    threshold_report = check_thresholds(
        transformed,
        warn=config["threshold_warn"],
        crit=config["threshold_crit"],
    )

    elapsed_ms = int((time.monotonic() - start) * 1000)

    summary: dict[str, Any] = {
        "status": "completed",
        "rows_extracted": len(rows),
        "rows_transformed": len(transformed),
        "threshold_report": threshold_report,
        "elapsed_ms": elapsed_ms,
        # WHY: Snapshot the config used for this run so the output is
        # self-documenting. If thresholds change, you can see what
        # values were active when this report was generated.
        "config_snapshot": {k: v for k, v in config.items() if not k.startswith("_")},
    }

    # Export
    output_dir = Path(config["output_dir"])
    atomic_write(output_dir / "summary.json", json.dumps(summary, indent=2))
    logging.info("Pipeline complete: %d rows, %d alerts, %dms",
                 len(transformed), len(threshold_report["alerts"]), elapsed_ms)

    return summary

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Level 5 Capstone: Operational Pipeline")
    parser.add_argument("--config", default="data/pipeline_config.json")
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    config = load_config(Path(args.config))
    summary = run_pipeline(config)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Linear pipeline: extract -> transform -> monitor -> export | Each stage depends on the previous stage's output. This is the standard ETL + monitoring pattern used in data warehousing and CI/CD pipelines. |
| Config snapshot in output | Self-documenting output: if thresholds change tomorrow, you can look at today's report and see exactly which thresholds were active. This is critical for auditing and debugging production issues. |
| `time.monotonic()` for duration | Unlike `time.time()`, `monotonic()` is not affected by NTP adjustments or clock drift. It always moves forward, making it the correct clock for measuring elapsed time. |
| Default `_numeric = 0.0` for missing columns | The pipeline should not crash on data that lacks a numeric column. Defaulting to 0.0 means no thresholds are breached for that row, which is the safe behavior. |
| Atomic write for summary export | Ties together the Fail-Safe Exporter (Project 12) pattern. If the pipeline crashes during export, consumers never see a half-written summary file. |

## Alternative Approaches

### Using a pipeline class with pluggable stages

```python
class Pipeline:
    def __init__(self):
        self.stages: list[Callable] = []

    def add_stage(self, func: Callable) -> "Pipeline":
        self.stages.append(func)
        return self

    def run(self, data):
        for stage in self.stages:
            data = stage(data)
        return data

pipeline = Pipeline()
pipeline.add_stage(extract_csv_files)
pipeline.add_stage(transform_rows)
pipeline.add_stage(check_thresholds)
```

A class-based pipeline makes stages pluggable and reorderable. This is cleaner when you have many pipelines with different stage combinations. For a single fixed pipeline, the linear function approach is simpler and more readable.

### Using Luigi or Airflow for orchestration

In production, pipelines with dependencies, retries, and scheduling are managed by workflow orchestrators like Apache Airflow, Prefect, or Luigi. These tools provide DAG visualization, retry policies, and distributed execution. This capstone teaches the fundamental pattern that those tools automate.

## Common Pitfalls

1. **Threshold warn >= crit** — If `threshold_warn=90` and `threshold_crit=50`, every value above 50 is classified as "critical" and warnings are never generated. Validate that `warn < crit` at config load time.
2. **No numeric column in CSV** — If the CSV has no column matching `("amount", "value", "score", "metric")`, all rows get `_numeric=0.0` and no thresholds are breached. The pipeline succeeds silently with misleading results. Log a warning when this happens.
3. **Non-existent input directory** — If `input_dir` does not exist, `extract_csv_files` returns an empty list and the pipeline produces "0 rows extracted." This is technically correct but may mask a configuration error. Validate the directory exists at pipeline start.
