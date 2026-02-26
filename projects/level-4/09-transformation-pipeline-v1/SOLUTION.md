# Transformation Pipeline V1 — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 4 / Project 09 — Transformation Pipeline V1.

Chains data transformations in sequence, with logging at each step.
Each transform is a pure function that takes records and returns records.
The pipeline tracks what changed at each step for auditability.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path
from typing import Any, Callable

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- transform functions ----------
# WHY: Each transform is a pure function — it takes a list of record dicts
# and returns a NEW list (no mutation). This functional style means
# transforms are composable (chain any order), testable (no shared state),
# and safe to retry (same input always gives same output).


def transform_strip_whitespace(records: list[dict]) -> list[dict]:
    """Strip leading/trailing whitespace from all string values."""
    # WHY: Whitespace is the most common data quality issue in CSV files.
    # " Alice " and "Alice" should be treated as the same value.
    return [
        {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
        for row in records
    ]


def transform_lowercase_keys(records: list[dict]) -> list[dict]:
    """Normalize all dictionary keys to lowercase."""
    # WHY: "Name", "NAME", and "name" should all map to the same key.
    # Normalizing early prevents case-sensitivity bugs downstream.
    return [
        {k.lower(): v for k, v in row.items()}
        for row in records
    ]


def transform_add_row_id(records: list[dict]) -> list[dict]:
    """Add a sequential row_id field to each record."""
    # WHY: Row IDs provide stable identifiers for tracking records through
    # the pipeline. They are especially useful in error reports.
    return [
        {**row, "row_id": idx}
        for idx, row in enumerate(records, start=1)
    ]


def transform_filter_empty_rows(records: list[dict]) -> list[dict]:
    """Remove records where all values are empty strings."""
    # WHY: Empty rows carry no data and create noise in downstream
    # processing. Filtering them early simplifies everything after.
    return [
        row for row in records
        if any(str(v).strip() for v in row.values())
    ]


def transform_coerce_numbers(records: list[dict]) -> list[dict]:
    """Try to convert string values that look numeric into int or float."""
    result = []
    for row in records:
        new_row = {}
        for k, v in row.items():
            if isinstance(v, str):
                # WHY: Try int first, then float. "42" should become int(42),
                # not float(42.0). "3.14" fails int() but succeeds float().
                try:
                    new_row[k] = int(v)
                    continue
                except ValueError:
                    pass
                try:
                    new_row[k] = float(v)
                    continue
                except ValueError:
                    pass
            new_row[k] = v
        result.append(new_row)
    return result

# ---------- pipeline engine ----------

# WHY: A registry dict maps string names to functions. This lets the
# pipeline be driven by configuration (a comma-separated list of step
# names) rather than hard-coded function calls. This is the Strategy
# pattern — behavior is selected at runtime by name.
TRANSFORMS: dict[str, Callable[..., Any]] = {
    "strip_whitespace": transform_strip_whitespace,
    "lowercase_keys": transform_lowercase_keys,
    "add_row_id": transform_add_row_id,
    "filter_empty_rows": transform_filter_empty_rows,
    "coerce_numbers": transform_coerce_numbers,
}


def run_pipeline(
    records: list[dict],
    steps: list[str],
) -> tuple[list[dict], list[dict]]:
    """Execute a sequence of named transforms, logging each step."""
    step_log: list[dict] = []
    current = records

    for step_name in steps:
        func = TRANSFORMS.get(step_name)
        if func is None:
            # WHY: Skip unknown steps instead of crashing. This makes the
            # pipeline resilient to typos in config and lets you add steps
            # to the config before implementing them.
            logging.error("Unknown transform: %s — skipping", step_name)
            step_log.append({"step": step_name, "status": "skipped", "reason": "unknown"})
            continue

        # WHY: Track records_before and records_after to make data flow
        # visible. If filter_empty_rows drops 50% of records, you want
        # to know without inspecting the full output.
        before_count = len(current)
        current = func(current)
        after_count = len(current)

        step_log.append({
            "step": step_name,
            "status": "ok",
            "records_before": before_count,
            "records_after": after_count,
        })
        logging.info("Step '%s': %d -> %d records", step_name, before_count, after_count)

    return current, step_log

# ---------- I/O ----------


def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Input not found: {path}")
    text = path.read_text(encoding="utf-8")
    return list(csv.DictReader(text.splitlines()))


def run(input_path: Path, output_path: Path, steps: list[str]) -> dict:
    """Load data, run pipeline, write results."""
    records = load_csv(input_path)
    result, step_log = run_pipeline(records, steps)

    report = {
        "input_records": len(records),
        "output_records": len(result),
        "steps": step_log,
        "data": result,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Pipeline complete: %d -> %d records", len(records), len(result))
    return report

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a data transformation pipeline")
    parser.add_argument("--input", default="data/sample_input.csv")
    parser.add_argument("--output", default="data/pipeline_output.json")
    parser.add_argument(
        "--steps",
        default="strip_whitespace,lowercase_keys,filter_empty_rows,coerce_numbers,add_row_id",
        help="Comma-separated transform names",
    )
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    steps = [s.strip() for s in args.steps.split(",")]
    report = run(Path(args.input), Path(args.output), steps)
    print(json.dumps({"steps": report["steps"], "output_records": report["output_records"]}, indent=2))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Pure functions (no mutation, return new lists) | Composability, testability, and retry safety. If a step fails, the original data is untouched. You can also test each transform independently with simple input/output assertions. |
| `TRANSFORMS` registry mapping names to functions | Decouples configuration from code. Users specify steps as strings in a CLI argument or config file — no need to edit Python code to change the pipeline. This is the Strategy pattern. |
| Step log tracks `records_before` and `records_after` | Makes data flow visible. If `filter_empty_rows` drops 50% of your data, the step log tells you immediately without inspecting the full output. |
| Unknown steps are skipped, not fatal | Resilience. A typo in one step name should not crash the entire pipeline. The step log records the skip so it is not silent. |

## Alternative Approaches

### Using a class-based pipeline with method chaining

```python
class Pipeline:
    def __init__(self, records):
        self.records = records
        self.log = []

    def strip_whitespace(self):
        self.records = [
            {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
            for row in self.records
        ]
        return self  # enables chaining

    def run(self):
        return self.records, self.log

# Usage:
result, log = Pipeline(records).strip_whitespace().lowercase_keys().run()
```

**Trade-off:** Method chaining reads nicely in code but ties transforms to the Pipeline class. The function-based approach lets you use transforms anywhere — in a pipeline, in a test, in a one-off script — without importing a class.

### Using `functools.reduce` to compose transforms

```python
from functools import reduce

def compose_pipeline(records, steps):
    return reduce(lambda data, step: TRANSFORMS[step](data), steps, records)
```

**Trade-off:** `reduce` is elegant and concise, but it makes step logging difficult (you lose the intermediate record counts) and error handling awkward (one failing step crashes the whole reduction). The explicit loop in the main solution is more transparent and gives you full control over logging and error recovery.

## Common Pitfalls

1. **Step ordering matters** — Running `add_row_id` before `filter_empty_rows` assigns IDs to rows that will be filtered out, creating gaps in the sequence. The recommended order is: strip -> normalize -> filter -> coerce -> add_id.
2. **Mutating records instead of returning new lists** — If a transform modifies records in place, earlier transforms' results are retroactively changed. This causes subtle bugs that are hard to reproduce. Always return a new list.
3. **Forgetting that `int("3.14")` raises ValueError** — The `coerce_numbers` transform tries int first and falls through to float. If you only try int, decimal values will remain as strings and break downstream numeric operations.
