"""Tests for Audit Log Enhancer."""

from pathlib import Path
import json
import pytest

from project import classify_severity, compute_duration_ms, enrich_entry, load_log_entries, enrich_log, run


@pytest.mark.parametrize(
    "event_type, expected",
    [
        ("login_error", "HIGH"),
        ("request_failed", "HIGH"),
        ("slow_query_warning", "MEDIUM"),
        ("connection_timeout", "MEDIUM"),
        ("user_login", "LOW"),
        ("page_view", "LOW"),
    ],
)
def test_classify_severity(event_type: str, expected: str) -> None:
    assert classify_severity(event_type) == expected


def test_compute_duration_ms() -> None:
    start = "2025-01-15T10:00:00+00:00"
    end = "2025-01-15T10:00:02+00:00"
    assert compute_duration_ms(start, end) == 2000


def test_compute_duration_ms_missing() -> None:
    assert compute_duration_ms(None, "2025-01-15T10:00:00+00:00") is None
    assert compute_duration_ms("2025-01-15T10:00:00+00:00", None) is None


def test_enrich_entry_adds_fields() -> None:
    entry = {"event_type": "user_login", "session_id": "abc"}
    enriched = enrich_entry(entry, "corr-123")
    assert enriched["correlation_id"] == "corr-123"
    assert enriched["severity"] == "LOW"
    assert "enriched_at" in enriched


def test_enrich_log_groups_by_session() -> None:
    entries = [
        {"event_type": "login", "session_id": "sess-1"},
        {"event_type": "action", "session_id": "sess-1"},
        {"event_type": "login", "session_id": "sess-2"},
    ]
    enriched = enrich_log(entries)
    # Same session should share a correlation ID
    assert enriched[0]["correlation_id"] == enriched[1]["correlation_id"]
    assert enriched[0]["correlation_id"] != enriched[2]["correlation_id"]


def test_load_log_entries_skips_malformed(tmp_path: Path) -> None:
    log_file = tmp_path / "logs.jsonl"
    log_file.write_text(
        '{"event_type": "ok"}\nnot-json\n{"event_type": "also_ok"}\n',
        encoding="utf-8",
    )
    entries = load_log_entries(log_file)
    assert len(entries) == 2


def test_run_integration(tmp_path: Path) -> None:
    log_file = tmp_path / "input.jsonl"
    log_file.write_text(
        '{"event_type": "user_login", "session_id": "s1"}\n'
        '{"event_type": "request_failed", "session_id": "s1"}\n',
        encoding="utf-8",
    )
    output = tmp_path / "enriched.jsonl"
    summary = run(log_file, output)
    assert summary["total_entries"] == 2
    assert output.exists()
