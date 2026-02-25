"""Tests for Alarm Message Generator."""

from project import alarm_summary, format_alarm, parse_alarm, sort_by_severity


def test_parse_valid_alarm() -> None:
    """A well-formed line should produce a structured alarm dict."""
    result = parse_alarm("critical | web-01 | CPU at 99%")
    assert result["severity"] == "critical"
    assert result["source"] == "web-01"
    assert result["message"] == "CPU at 99%"


def test_parse_bad_severity() -> None:
    """An unknown severity should return an error."""
    result = parse_alarm("danger | web-01 | disk full")
    assert "error" in result
    assert "Unknown severity" in result["error"]


def test_format_alarm_includes_fields() -> None:
    """The formatted message should contain all alarm fields."""
    alarm = {"severity": "warning", "source": "db-01", "message": "Slow query"}
    output = format_alarm(alarm)
    assert "WARNING" in output
    assert "db-01" in output
    assert "Slow query" in output


def test_sort_by_severity_critical_first() -> None:
    """Critical alarms should sort before warning and info."""
    alarms = [
        {"severity": "info", "source": "a", "message": "ok"},
        {"severity": "critical", "source": "b", "message": "bad"},
        {"severity": "warning", "source": "c", "message": "hmm"},
    ]
    sorted_alarms = sort_by_severity(alarms)
    assert sorted_alarms[0]["severity"] == "critical"
    assert sorted_alarms[1]["severity"] == "warning"
    assert sorted_alarms[2]["severity"] == "info"


def test_alarm_summary_counts() -> None:
    """Summary should count alarms by severity."""
    alarms = [
        {"severity": "critical", "source": "a", "message": "x"},
        {"severity": "critical", "source": "b", "message": "y"},
        {"severity": "info", "source": "c", "message": "z"},
    ]
    summary = alarm_summary(alarms)
    assert summary["by_severity"]["critical"] == 2
    assert summary["by_severity"]["info"] == 1
    assert summary["total"] == 3
