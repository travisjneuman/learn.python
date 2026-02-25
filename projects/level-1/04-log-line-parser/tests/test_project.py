"""Tests for Log Line Parser."""

from project import count_by_level, filter_by_level, parse_log_line


def test_parse_valid_log_line() -> None:
    result = parse_log_line("2024-01-15 09:30:00 [INFO] Server started on port 8080")
    assert result["level"] == "INFO"
    assert result["message"] == "Server started on port 8080"
    assert result["timestamp"] == "2024-01-15 09:30:00"


def test_parse_error_level() -> None:
    result = parse_log_line("2024-01-15 10:00:00 [ERROR] Database connection failed")
    assert result["level"] == "ERROR"


def test_parse_malformed_line() -> None:
    result = parse_log_line("this is not a log line")
    assert "error" in result


def test_count_by_level() -> None:
    entries = [
        {"level": "INFO", "message": "a"},
        {"level": "ERROR", "message": "b"},
        {"level": "INFO", "message": "c"},
    ]
    counts = count_by_level(entries)
    assert counts["INFO"] == 2
    assert counts["ERROR"] == 1


def test_filter_by_level() -> None:
    entries = [
        {"level": "INFO", "message": "a"},
        {"level": "ERROR", "message": "b"},
    ]
    filtered = filter_by_level(entries, "error")
    assert len(filtered) == 1
    assert filtered[0]["level"] == "ERROR"
