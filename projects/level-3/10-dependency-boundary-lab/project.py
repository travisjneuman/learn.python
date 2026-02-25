"""Level 3 project: Dependency Boundary Lab.

Demonstrates separating I/O (file reading, printing) from business logic
so that core functions can be tested without touching the filesystem.

Skills practiced: dependency inversion, typing basics, dataclasses,
logging, function composition, testable architecture.
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Protocol

logger = logging.getLogger(__name__)


# ── Protocols (interface boundaries) ──────────────────────────

class DataReader(Protocol):
    """Anything that can read data and return records."""

    def read(self) -> list[dict]:
        ...


class DataWriter(Protocol):
    """Anything that can write processed results."""

    def write(self, data: list[dict]) -> None:
        ...


# ── Concrete implementations (I/O layer) ─────────────────────

class JsonFileReader:
    """Reads records from a JSON file."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> list[dict]:
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")
        data = json.loads(self.path.read_text(encoding="utf-8"))
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


# ── Business logic (no I/O) ──────────────────────────────────

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
    """Keep only records that have all required fields with non-empty values.

    This is pure logic — no I/O.
    """
    result: list[dict] = []
    for record in records:
        if all(record.get(f) for f in required_fields):
            result.append(record)
    return result


def transform_records(
    records: list[dict],
    rename_map: dict[str, str],
) -> list[dict]:
    """Rename fields in each record according to rename_map.

    rename_map: {'old_name': 'new_name'}
    """
    result: list[dict] = []
    for record in records:
        new_record: dict = {}
        for key, value in record.items():
            new_key = rename_map.get(key, key)
            new_record[new_key] = value
        result.append(new_record)
    return result


def enrich_records(records: list[dict], defaults: dict) -> list[dict]:
    """Add default values for missing fields."""
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

    All pure logic — the caller handles I/O.
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


# ── Orchestrator (connects I/O to logic) ──────────────────────

def run(reader: DataReader, writer: DataWriter, config: dict) -> ProcessingStats:
    """Orchestrate: read -> process -> write.

    The orchestrator is the only place that touches both I/O and logic.
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
    """Build CLI parser."""
    parser = argparse.ArgumentParser(description="Dependency boundary lab")
    parser.add_argument("input", help="Input JSON file")
    parser.add_argument("output", help="Output JSON file")
    parser.add_argument("--config", help="Pipeline config JSON file")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    """Entry point."""
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
