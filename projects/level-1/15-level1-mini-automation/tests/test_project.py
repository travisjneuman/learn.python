"""Tests for Level 1 Mini Automation."""

from pathlib import Path

from project import (
    run_pipeline,
    step_filter_active,
    step_parse_records,
    step_summarise,
    step_transform,
)


def test_step_parse_records() -> None:
    lines = ["Alice | active | 100", "Bob | failed | 50"]
    records = step_parse_records(lines)
    assert len(records) == 2
    assert records[0]["name"] == "Alice"
    assert records[1]["status"] == "failed"


def test_step_parse_records_skips_short_lines() -> None:
    lines = ["Only two parts | here", "Good | active | 10"]
    records = step_parse_records(lines)
    assert len(records) == 1


def test_step_filter_active() -> None:
    records = [
        {"name": "A", "status": "active", "value": "10"},
        {"name": "B", "status": "failed", "value": "20"},
        {"name": "C", "status": "ok", "value": "30"},
    ]
    active = step_filter_active(records)
    assert len(active) == 2
    assert all(r["status"] in ("active", "ok") for r in active)


def test_step_transform() -> None:
    records = [{"name": "alice smith", "status": "active", "value": "42.5"}]
    transformed = step_transform(records)
    assert transformed[0]["name"] == "Alice Smith"
    assert transformed[0]["value"] == 42.5


def test_step_transform_bad_value() -> None:
    records = [{"name": "bob", "status": "ok", "value": "not_a_number"}]
    transformed = step_transform(records)
    assert transformed[0]["value"] == 0.0


def test_step_summarise() -> None:
    records = [
        {"name": "A", "status": "active", "value": 10.0},
        {"name": "B", "status": "ok", "value": 30.0},
    ]
    summary = step_summarise(records)
    assert summary["count"] == 2
    assert summary["total_value"] == 40.0
    assert summary["average_value"] == 20.0


def test_step_summarise_empty() -> None:
    summary = step_summarise([])
    assert summary["count"] == 0
    assert summary["total_value"] == 0.0


def test_run_pipeline(tmp_path: Path) -> None:
    data = tmp_path / "data.txt"
    data.write_text(
        "Alice | active | 100\n"
        "Bob | failed | 50\n"
        "Carol | ok | 75\n",
        encoding="utf-8",
    )
    result = run_pipeline(data)
    assert result["total_lines"] == 3
    assert result["parsed_records"] == 3
    assert result["active_records"] == 2
    assert result["summary"]["count"] == 2
    assert result["summary"]["total_value"] == 175.0
