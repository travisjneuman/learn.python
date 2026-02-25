"""Tests for Logging Baseline Tool.

Uses pytest fixtures and tmp_path for file-based tests.
"""

from pathlib import Path

import pytest

from project import (
    LogEntry,
    RunSummary,
    filter_entries,
    format_entry,
    parse_log_file,
    parse_log_line,
    summarise_entries,
)


@pytest.fixture
def sample_log(tmp_path: Path) -> Path:
    """Create a sample log file."""
    log = tmp_path / "test.log"
    log.write_text(
        "INFO | auth | User logged in\n"
        "WARNING | db | Slow query detected\n"
        "ERROR | api | Timeout on /users\n"
        "# This is a comment\n"
        "DEBUG | cache | Cache hit for key=abc\n"
        "\n",
        encoding="utf-8",
    )
    return log


def test_parse_log_line_structured() -> None:
    """Structured lines should parse into correct fields."""
    entry = parse_log_line("ERROR | api | Connection refused")
    assert entry is not None
    assert entry.level == "ERROR"
    assert entry.source == "api"
    assert entry.message == "Connection refused"


def test_parse_log_line_plain_text() -> None:
    """Plain text lines should become INFO entries."""
    entry = parse_log_line("Just a plain message")
    assert entry is not None
    assert entry.level == "INFO"
    assert entry.message == "Just a plain message"


def test_parse_log_line_blank() -> None:
    """Blank lines should return None."""
    assert parse_log_line("") is None
    assert parse_log_line("   ") is None


def test_parse_log_file(sample_log: Path) -> None:
    """File parsing should skip comments and blanks."""
    entries = parse_log_file(sample_log)
    assert len(entries) == 4
    assert entries[0].level == "INFO"
    assert entries[2].level == "ERROR"


def test_parse_log_file_missing(tmp_path: Path) -> None:
    """Missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        parse_log_file(tmp_path / "nope.log")


def test_summarise_entries() -> None:
    """Summary should count entries by level."""
    entries = [
        LogEntry(timestamp=1.0, level="INFO", message="a"),
        LogEntry(timestamp=2.0, level="INFO", message="b"),
        LogEntry(timestamp=3.0, level="ERROR", message="c"),
    ]
    summary = summarise_entries(entries)
    assert summary.total_entries == 3
    assert summary.by_level["INFO"] == 2
    assert summary.by_level["ERROR"] == 1
    assert summary.duration_seconds == 2.0


def test_summarise_empty() -> None:
    """Empty list should produce zeroed summary."""
    summary = summarise_entries([])
    assert summary.total_entries == 0


def test_filter_entries_by_level() -> None:
    """Filter should respect minimum level."""
    entries = [
        LogEntry(timestamp=1.0, level="DEBUG", message="a"),
        LogEntry(timestamp=2.0, level="WARNING", message="b"),
        LogEntry(timestamp=3.0, level="ERROR", message="c"),
    ]
    filtered = filter_entries(entries, min_level="WARNING")
    assert len(filtered) == 2
    assert all(e.level in ("WARNING", "ERROR") for e in filtered)


def test_filter_entries_by_source() -> None:
    """Filter should match on source when specified."""
    entries = [
        LogEntry(timestamp=1.0, level="INFO", message="a", source="auth"),
        LogEntry(timestamp=2.0, level="INFO", message="b", source="db"),
    ]
    filtered = filter_entries(entries, source="auth")
    assert len(filtered) == 1
    assert filtered[0].source == "auth"


def test_format_entry_text() -> None:
    """Text format should be human-readable."""
    entry = LogEntry(timestamp=1.0, level="ERROR", source="api", message="Timeout")
    text = format_entry(entry, "text")
    assert "ERROR" in text
    assert "api" in text
    assert "Timeout" in text


def test_format_entry_json() -> None:
    """JSON format should be valid JSON."""
    import json
    entry = LogEntry(timestamp=1.0, level="INFO", source="db", message="OK")
    result = json.loads(format_entry(entry, "json"))
    assert result["level"] == "INFO"
