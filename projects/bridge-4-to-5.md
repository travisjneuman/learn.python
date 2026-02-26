# Bridge Exercise: Level 4 to Level 5

You have completed Level 4. You can validate data with schemas, use dataclasses, and build multi-step pipelines. Level 5 introduces **scheduling and automation**, **multi-file ETL pipelines**, **configuration-driven programs**, and **resilient error recovery**. This bridge exercise connects schema validation with scheduled, repeatable tasks.

---

## What Changes in Level 5

In Level 4, you validated data and built pipelines that ran once. In Level 5, you will:
- Run tasks on a **schedule** (every hour, every day)
- Build **ETL pipelines** that extract, transform, and load data between formats
- Use **configuration files** to control what your program does without changing code
- Handle **partial failures** gracefully so one bad record does not stop the whole job

---

## Part 1: Configuration-Driven Processing

### Why configuration?

Hardcoding values (file paths, thresholds, rules) means changing behavior requires editing code. Configuration files let users change behavior without touching Python.

### Exercise

Create `bridge_4_to_5.py`:

```python
import json
import csv
import logging
from dataclasses import dataclass
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """Configuration for a data processing pipeline."""

    input_file: str
    output_file: str
    min_value: float = 0.0
    max_value: float = float("inf")
    required_fields: list[str] = None

    def __post_init__(self):
        if self.required_fields is None:
            self.required_fields = []

    @classmethod
    def from_json(cls, filepath):
        """Load config from a JSON file."""
        data = json.loads(Path(filepath).read_text())
        return cls(**data)


def run_pipeline(config):
    """Run an ETL pipeline based on configuration.

    1. Extract: read CSV rows
    2. Transform: validate and filter
    3. Load: write cleaned data to output

    Returns a summary dict.
    """
    # Extract
    input_path = Path(config.input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {config.input_file}")

    with open(input_path, newline="") as f:
        rows = list(csv.DictReader(f))

    logger.info("Extracted %d rows from %s", len(rows), config.input_file)

    # Transform
    valid = []
    errors = []
    for i, row in enumerate(rows):
        # Check required fields
        missing = [f for f in config.required_fields if f not in row or not row[f].strip()]
        if missing:
            errors.append({"row": i, "reason": f"missing fields: {missing}"})
            continue

        # Check numeric bounds (if 'value' column exists)
        if "value" in row:
            try:
                val = float(row["value"])
                if val < config.min_value or val > config.max_value:
                    errors.append({"row": i, "reason": f"value {val} out of range"})
                    continue
            except ValueError:
                errors.append({"row": i, "reason": f"invalid number: {row['value']}"})
                continue

        valid.append(row)

    logger.info("Transformed: %d valid, %d errors", len(valid), len(errors))

    # Load
    if valid:
        output_path = Path(config.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=valid[0].keys())
            writer.writeheader()
            writer.writerows(valid)
        logger.info("Loaded %d rows to %s", len(valid), config.output_file)

    return {
        "input_rows": len(rows),
        "output_rows": len(valid),
        "errors": errors,
    }
```

**New concepts introduced:**
- `@classmethod` as an alternative constructor — `PipelineConfig.from_json("config.json")`.
- **ETL pattern**: Extract (read) -> Transform (validate/filter) -> Load (write).
- **Configuration-driven**: the same code handles different files and rules based on config.
- **Partial failure handling**: bad rows are logged and skipped, not fatal.

---

## Part 2: Simulating a Scheduled Job

### Exercise

Add a function that simulates running the pipeline on a schedule.

Add to `bridge_4_to_5.py`:

```python
import time
from datetime import datetime


def run_on_schedule(config, interval_seconds=60, max_runs=3):
    """Run the pipeline repeatedly on a schedule.

    In real code, you would use a library like schedule or APScheduler.
    This simplified version demonstrates the pattern.
    """
    results = []

    for run_number in range(1, max_runs + 1):
        timestamp = datetime.now().isoformat()
        logger.info("--- Run %d at %s ---", run_number, timestamp)

        try:
            result = run_pipeline(config)
            result["run"] = run_number
            result["timestamp"] = timestamp
            result["status"] = "success"
        except Exception as e:
            result = {
                "run": run_number,
                "timestamp": timestamp,
                "status": "failed",
                "error": str(e),
            }
            logger.error("Run %d failed: %s", run_number, e)

        results.append(result)

        if run_number < max_runs:
            logger.info("Sleeping %d seconds...", interval_seconds)
            time.sleep(interval_seconds)

    return results
```

**Key idea:** In production, you would not use `time.sleep()` in a loop. Libraries like `schedule`, `APScheduler`, or system tools like `cron` handle this. But the pattern is the same: run a function, record the result, handle errors, repeat.

---

## Part 3: Tests

Create `test_bridge_4_to_5.py`:

```python
import json
import pytest
from bridge_4_to_5 import PipelineConfig, run_pipeline


@pytest.fixture
def config_and_data(tmp_path):
    """Create a config file and matching data file."""
    data_file = tmp_path / "input.csv"
    data_file.write_text(
        "name,value,category\n"
        "Alice,100,A\n"
        "Bob,200,B\n"
        "Charlie,,A\n"  # missing value
        "Diana,999,C\n"  # will be out of range
    )

    output_file = tmp_path / "output.csv"

    config = PipelineConfig(
        input_file=str(data_file),
        output_file=str(output_file),
        min_value=0,
        max_value=500,
        required_fields=["name", "value", "category"],
    )
    return config, output_file


def test_pipeline_filters_correctly(config_and_data):
    config, output_file = config_and_data
    result = run_pipeline(config)
    assert result["input_rows"] == 4
    assert result["output_rows"] == 2  # Alice and Bob
    assert len(result["errors"]) == 2  # Charlie (missing) and Diana (out of range)


def test_pipeline_creates_output(config_and_data):
    config, output_file = config_and_data
    run_pipeline(config)
    assert output_file.exists()
    lines = output_file.read_text().strip().split("\n")
    assert len(lines) == 3  # header + 2 data rows


def test_pipeline_missing_input(tmp_path):
    config = PipelineConfig(
        input_file=str(tmp_path / "nope.csv"),
        output_file=str(tmp_path / "out.csv"),
    )
    with pytest.raises(FileNotFoundError):
        run_pipeline(config)


def test_config_from_json(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({
        "input_file": "data.csv",
        "output_file": "output.csv",
        "min_value": 10,
        "max_value": 100,
        "required_fields": ["name"],
    }))
    config = PipelineConfig.from_json(config_file)
    assert config.min_value == 10
    assert config.required_fields == ["name"]
```

Run: `pytest test_bridge_4_to_5.py -v`

---

## You Are Ready

If you can build a configuration-driven ETL pipeline, handle partial failures without crashing, and understand the pattern of scheduled repeated execution, you are ready for Level 5.

---

| [Level 4 Projects](level-4/README.md) | [Home](../README.md) | [Level 5 Projects](level-5/README.md) |
|:---|:---:|---:|
