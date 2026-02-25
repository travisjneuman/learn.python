"""Tests for Operational Run Logger."""
from __future__ import annotations

import json
import pytest
from pathlib import Path

from project import RunLogger, process_items, run


# ---------- RunLogger ----------

def test_run_logger_creates_events() -> None:
    logger = RunLogger(run_id="test-001")
    logger.log_event("test", {"key": "value"})
    summary = logger.finish()
    assert summary["run_id"] == "test-001"
    assert summary["event_count"] >= 3  # start + test + finish


def test_run_logger_tracks_duration() -> None:
    logger = RunLogger()
    summary = logger.finish()
    assert "duration_ms" in summary
    assert summary["duration_ms"] >= 0


def test_run_logger_error_counting() -> None:
    logger = RunLogger()
    logger.log_error("something broke", {"code": 500})
    logger.log_error("another issue")
    summary = logger.finish("failed")
    assert summary["error_count"] == 2
    error_events = [e for e in summary["events"] if e["event_type"] == "error"]
    assert len(error_events) == 2


def test_run_logger_warning() -> None:
    logger = RunLogger()
    logger.log_warning("disk space low")
    summary = logger.finish()
    warning_events = [e for e in summary["events"] if e["event_type"] == "warning"]
    assert len(warning_events) == 1


# ---------- process_items ----------

@pytest.mark.parametrize("item_count", [0, 1, 5])
def test_process_items_various_counts(item_count: int) -> None:
    logger = RunLogger()
    items = [f"item_{i}" for i in range(item_count)]
    results = process_items(items, logger)
    assert len(results) == item_count
    if item_count > 0:
        assert all(r["processed"] for r in results)


def test_process_items_logs_each_step() -> None:
    logger = RunLogger()
    process_items(["a", "b", "c"], logger)
    item_events = [e for e in logger.events if e["event_type"] == "item_processed"]
    assert len(item_events) == 3


# ---------- integration: run ----------

def test_run_completes_successfully(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_text("task1\ntask2\ntask3\n", encoding="utf-8")
    output = tmp_path / "output.json"
    log = tmp_path / "log.json"
    summary = run(input_file, output, log, run_id="test-run")
    assert summary["status"] == "completed"
    assert summary["run_id"] == "test-run"
    assert log.exists() and output.exists()
    saved_log = json.loads(log.read_text())
    assert saved_log["event_count"] == summary["event_count"]


def test_run_handles_missing_input(tmp_path: Path) -> None:
    output = tmp_path / "output.json"
    log = tmp_path / "log.json"
    summary = run(tmp_path / "missing.txt", output, log)
    assert summary["status"] == "failed"
    assert summary["error_count"] >= 1
    assert log.exists()


@pytest.mark.parametrize("content,expected_status", [
    ("line1\nline2\n", "completed"),
    ("", "completed"),  # empty file should still complete
])
def test_run_various_inputs(
    tmp_path: Path, content: str, expected_status: str,
) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_text(content, encoding="utf-8")
    output = tmp_path / "output.json"
    log = tmp_path / "log.json"
    summary = run(input_file, output, log)
    assert summary["status"] == expected_status
