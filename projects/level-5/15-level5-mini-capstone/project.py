"""Level 5 / Project 15 — Mini Capstone: Operational Pipeline.

Combines config loading, multi-file ETL extraction, row transformation,
threshold monitoring, atomic export, and structured run logging into a
single end-to-end pipeline.  This capstone ties together every Level 5
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

    # WHY three config layers? -- Defaults provide sensible out-of-box
    # behavior, file config customizes per deployment, and env vars let
    # operators override at runtime (e.g., in Docker containers) without
    # editing any files. This is the twelve-factor app pattern.

    # Layer 2: file config
    if config_path and config_path.exists():
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        merged.update(raw)

    # Layer 3: env overrides (prefix PIPELINE_)
    for key in DEFAULTS:
        env_val = os.environ.get(f"PIPELINE_{key.upper()}")
        if env_val is not None:
            # Coerce to int if default is int, else keep string.
            if isinstance(DEFAULTS[key], int):
                merged[key] = int(env_val)
            else:
                merged[key] = env_val

    return merged

# ---------------------------------------------------------------------------
# 2. Multi-file ETL extraction
# ---------------------------------------------------------------------------

def extract_csv_files(input_dir: Path) -> list[dict]:
    """Read all .csv files from input_dir and return combined rows."""
    all_rows: list[dict] = []
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

# ---------------------------------------------------------------------------
# 3. Row transformation
# ---------------------------------------------------------------------------

def transform_rows(rows: list[dict]) -> list[dict]:
    """Normalize and enrich each row with a computed 'value' field."""
    transformed: list[dict] = []
    for idx, row in enumerate(rows, start=1):
        cleaned: dict[str, Any] = {}
        for k, v in row.items():
            cleaned[k.strip().lower()] = v.strip() if isinstance(v, str) else v

        # Try to parse a numeric 'amount' or 'value' column for threshold checks.
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

# ---------------------------------------------------------------------------
# 4. Threshold monitoring
# ---------------------------------------------------------------------------

def check_thresholds(
    rows: list[dict],
    warn: int | float,
    crit: int | float,
) -> dict[str, Any]:
    """Evaluate each row's _numeric value against warn/crit thresholds."""
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
# 5. Atomic export
# ---------------------------------------------------------------------------

def atomic_write(path: Path, data: str) -> None:
    """Write data to a temp file then rename for crash safety.

    WHY atomic writes in a pipeline? -- If the pipeline crashes mid-export,
    consumers of the output file see either the previous complete version
    or the new complete version — never a truncated mix.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(data, encoding="utf-8")
    tmp.replace(path)

# ---------------------------------------------------------------------------
# 6. Pipeline orchestrator
# ---------------------------------------------------------------------------

def run_pipeline(config: dict[str, Any]) -> dict[str, Any]:
    """Execute the full ETL + monitoring pipeline and return summary."""
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
    parser.add_argument("--config", default="data/pipeline_config.json",
                        help="Path to pipeline config JSON")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    config = load_config(Path(args.config))
    summary = run_pipeline(config)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
