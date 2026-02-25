"""Tests for Dependency Boundary Lab.

Demonstrates testing business logic WITHOUT touching the filesystem,
using InMemoryReader/InMemoryWriter instead of real files.
"""

import pytest

from project import (
    InMemoryReader,
    InMemoryWriter,
    ProcessingStats,
    enrich_records,
    filter_records,
    process_pipeline,
    run,
    transform_records,
)


# --- Pure logic tests (no I/O) ---

def test_filter_records() -> None:
    """Should keep only records with all required fields."""
    records = [
        {"name": "Alice", "email": "a@b.com"},
        {"name": "Bob", "email": ""},
        {"name": "Carol"},
    ]
    result = filter_records(records, ["name", "email"])
    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_filter_no_requirements() -> None:
    """No required fields means keep everything."""
    records = [{"a": 1}, {"b": 2}]
    result = filter_records(records, [])
    assert len(result) == 2


def test_transform_records() -> None:
    """Should rename fields according to map."""
    records = [{"first_name": "Alice", "age": 30}]
    result = transform_records(records, {"first_name": "name"})
    assert result[0]["name"] == "Alice"
    assert result[0]["age"] == 30
    assert "first_name" not in result[0]


def test_enrich_records() -> None:
    """Should add defaults for missing fields."""
    records = [{"name": "Alice"}, {"name": "Bob", "role": "admin"}]
    result = enrich_records(records, {"role": "user", "active": True})
    assert result[0]["role"] == "user"
    assert result[0]["active"] is True
    assert result[1]["role"] == "admin"  # Not overwritten.


# --- Pipeline tests ---

def test_process_pipeline_full() -> None:
    """Full pipeline with filter + enrich + rename."""
    records = [
        {"first": "Alice", "email": "a@b.com"},
        {"first": "Bob", "email": ""},
    ]
    result, stats = process_pipeline(
        records,
        required_fields=["first", "email"],
        rename_map={"first": "name"},
        defaults={"active": True},
    )
    assert len(result) == 1
    assert result[0]["name"] == "Alice"
    assert result[0]["active"] is True
    assert stats.filtered_out == 1


def test_process_pipeline_passthrough() -> None:
    """No config means passthrough."""
    records = [{"a": 1}]
    result, stats = process_pipeline(records)
    assert result == records
    assert stats.filtered_out == 0


# --- Integration tests (using in-memory I/O) ---

def test_run_with_in_memory_io() -> None:
    """Full run using InMemoryReader/Writer (no filesystem)."""
    records = [
        {"name": "Alice", "score": 90},
        {"name": "Bob", "score": 60},
    ]
    reader = InMemoryReader(records)
    writer = InMemoryWriter()

    config = {"required_fields": ["name", "score"]}
    stats = run(reader, writer, config)

    assert stats.total_input == 2
    assert stats.total_output == 2
    assert len(writer.results) == 2


def test_run_filters_in_memory() -> None:
    """Filtering should work through the full pipeline."""
    reader = InMemoryReader([
        {"name": "Alice", "email": "a@b.com"},
        {"name": "Bob"},
    ])
    writer = InMemoryWriter()

    stats = run(reader, writer, {"required_fields": ["name", "email"]})
    assert stats.total_output == 1
    assert writer.results[0]["name"] == "Alice"
