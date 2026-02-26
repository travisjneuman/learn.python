# Dependency Boundary Lab — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Dependency Boundary Lab."""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Protocol

logger = logging.getLogger(__name__)


# -- Protocols (interface boundaries) -------------------------------------
# WHY: Protocol defines a "shape" that any class can satisfy without
# inheriting from it. This is "structural typing" — if a class has
# a read() method that returns list[dict], it IS a DataReader,
# regardless of its class hierarchy.

class DataReader(Protocol):
    """Anything that can read data and return records."""

    def read(self) -> list[dict]:
        ...


class DataWriter(Protocol):
    """Anything that can write processed results."""

    def write(self, data: list[dict]) -> None:
        ...


# -- Concrete implementations (I/O layer) --------------------------------
# WHY: these classes do I/O (filesystem, network, etc.).
# They are the ONLY code that touches external resources.

class JsonFileReader:
    """Reads records from a JSON file."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> list[dict]:
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")
        data = json.loads(self.path.read_text(encoding="utf-8"))
        # WHY: wrap single dicts in a list so the pipeline always
        # operates on list[dict], regardless of input shape.
        if isinstance(data, dict):
            data = [data]
        logger.info("Read %d records from %s", len(data), self.path)
        return data


class JsonFileWriter:
    """Writes results to a JSON file."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, data: list[dict]) -> None:
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        logger.info("Wrote %d records to %s", len(data), self.path)


# WHY: in-memory implementations let tests exercise business logic
# WITHOUT touching the filesystem. This is the key insight of
# dependency inversion — swap real I/O for fake I/O in tests.

class InMemoryReader:
    """Reads from an in-memory list (useful for testing)."""

    def __init__(self, records: list[dict]) -> None:
        self.records = records

    def read(self) -> list[dict]:
        return self.records


class InMemoryWriter:
    """Writes to an in-memory list (useful for testing)."""

    def __init__(self) -> None:
        self.results: list[dict] = []

    def write(self, data: list[dict]) -> None:
        self.results = data


# -- Business logic (no I/O) ---------------------------------------------
# WHY: these functions are PURE — they take data in, return data out,
# and never read from files or print to the screen. This makes them
# trivially testable and reusable.

@dataclass
class ProcessingStats:
    """Statistics from a processing run."""
    total_input: int = 0
    total_output: int = 0
    filtered_out: int = 0
    transformed: int = 0


def filter_records(
    records: list[dict],
    required_fields: list[str],
) -> list[dict]:
    """Keep only records that have all required fields with non-empty values."""
    result: list[dict] = []
    for record in records:
        # WHY: record.get(f) returns None for missing fields and ""
        # for empty fields. Both are falsy, so this one check handles
        # both "missing" and "empty" cases.
        if all(record.get(f) for f in required_fields):
            result.append(record)
    return result


def transform_records(
    records: list[dict],
    rename_map: dict[str, str],
) -> list[dict]:
    """Rename fields in each record according to rename_map.

    WHY: data sources often use different field names than your
    application expects. A rename map ("first_name" -> "name")
    bridges the gap without modifying the source data.
    """
    result: list[dict] = []
    for record in records:
        new_record: dict = {}
        for key, value in record.items():
            # WHY: rename_map.get(key, key) returns the new name if
            # mapped, or the original name if not. Unmapped fields
            # pass through unchanged.
            new_key = rename_map.get(key, key)
            new_record[new_key] = value
        result.append(new_record)
    return result


def enrich_records(records: list[dict], defaults: dict) -> list[dict]:
    """Add default values for missing fields.

    WHY: {**defaults, **record} merges the two dicts with record
    values taking precedence. This fills in gaps without overwriting
    existing data.
    """
    result: list[dict] = []
    for record in records:
        enriched = {**defaults, **record}
        result.append(enriched)
    return result


def process_pipeline(
    records: list[dict],
    required_fields: Optional[list[str]] = None,
    rename_map: Optional[dict[str, str]] = None,
    defaults: Optional[dict] = None,
) -> tuple[list[dict], ProcessingStats]:
    """Run the full processing pipeline.

    WHY: the pipeline is a sequence of optional steps. Each step
    only runs if its config is provided. This makes the pipeline
    flexible without requiring the caller to pass every option.
    """
    stats = ProcessingStats(total_input=len(records))

    # Step 1: Filter.
    if required_fields:
        filtered = filter_records(records, required_fields)
        stats.filtered_out = len(records) - len(filtered)
    else:
        filtered = records

    # Step 2: Enrich with defaults.
    if defaults:
        enriched = enrich_records(filtered, defaults)
    else:
        enriched = filtered

    # Step 3: Rename fields.
    if rename_map:
        transformed = transform_records(enriched, rename_map)
        stats.transformed = len(transformed)
    else:
        transformed = enriched

    stats.total_output = len(transformed)
    return transformed, stats


# -- Orchestrator (connects I/O to logic) ---------------------------------

def run(reader: DataReader, writer: DataWriter,
        config: dict) -> ProcessingStats:
    """Orchestrate: read -> process -> write.

    WHY: the orchestrator is the ONLY function that touches both I/O
    and logic. Business logic functions never see a file path.
    I/O classes never see business rules. This separation is the
    core architecture lesson of this project.
    """
    records = reader.read()

    results, stats = process_pipeline(
        records,
        required_fields=config.get("required_fields"),
        rename_map=config.get("rename_map"),
        defaults=config.get("defaults"),
    )

    writer.write(results)
    logger.info("Pipeline complete: %s", asdict(stats))
    return stats


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dependency boundary lab")
    parser.add_argument("input", help="Input JSON file")
    parser.add_argument("output", help="Output JSON file")
    parser.add_argument("--config", help="Pipeline config JSON file")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    config: dict = {}
    if args.config:
        config = json.loads(Path(args.config).read_text(encoding="utf-8"))

    reader = JsonFileReader(Path(args.input))
    writer = JsonFileWriter(Path(args.output))
    stats = run(reader, writer, config)

    print(f"Processed: {stats.total_input} in, {stats.total_output} out, "
          f"{stats.filtered_out} filtered")


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| `Protocol` for DataReader/DataWriter | Defines interfaces without inheritance. Any class with a matching `read()` or `write()` method automatically satisfies the protocol. This is Python's version of Go-style interfaces. |
| In-memory reader/writer for tests | Tests can exercise the full pipeline without creating temp files. Pass `InMemoryReader([{"name": "Alice"}])` and check `writer.results`. Fast, reliable, no cleanup needed. |
| Pure business logic functions (no I/O) | `filter_records`, `transform_records`, and `enrich_records` take data in and return data out. They are trivially testable, reusable, and composable. |
| `run()` as the single orchestration point | Only `run()` connects I/O to logic. Changing the data source (JSON file to database to API) only requires a new Reader class — zero changes to business logic. |
| `{**defaults, **record}` for enrichment | Dict unpacking merges two dicts in one expression. The right-hand dict wins on key conflicts, so existing record values are preserved. |

## Alternative Approaches

### Using abstract base classes instead of Protocol

```python
from abc import ABC, abstractmethod

class DataReader(ABC):
    @abstractmethod
    def read(self) -> list[dict]:
        pass

class JsonFileReader(DataReader):
    def read(self) -> list[dict]:
        ...
```

**Trade-off:** ABC requires explicit inheritance (`class JsonFileReader(DataReader)`), which is more familiar to developers from Java/C#. Protocol uses structural typing (no inheritance needed), which is more Pythonic. Protocol is newer (Python 3.8+) and more flexible.

## Common Pitfalls

1. **Business logic calling I/O directly** — If `filter_records` reads from a file internally, you cannot test it without a real file. The whole point of dependency boundaries is that logic functions receive data as arguments, never fetch it themselves.

2. **Testing the orchestrator instead of the logic** — The `run()` function is hard to test because it involves I/O. Test `filter_records`, `transform_records`, and `enrich_records` individually with plain dicts. Only integration-test `run()` if needed.

3. **Config rename map creating duplicate keys** — If `rename_map` maps both "first_name" and "given_name" to "name", the second one silently overwrites the first. Validate the rename map for duplicate target keys before processing.
