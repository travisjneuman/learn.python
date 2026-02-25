"""Tests for Alert Threshold Monitor."""
import pytest
from pathlib import Path
import json
from project import check_threshold, evaluate_metrics, apply_cooldown, run

@pytest.mark.parametrize("value,warning,critical,expected", [
    (50, 70, 90, "ok"),
    (75, 70, 90, "warning"),
    (95, 70, 90, "critical"),
    (70, 70, 90, "warning"),
    (90, 70, 90, "critical"),
])
def test_check_threshold(value, warning, critical, expected):
    assert check_threshold(value, warning, critical) == expected

def test_evaluate_metrics_finds_alerts():
    metrics = [
        {"name": "cpu", "value": 85, "timestamp": "2025-01-15T10:00:00+00:00"},
        {"name": "cpu", "value": 50, "timestamp": "2025-01-15T10:01:00+00:00"},
        {"name": "memory", "value": 95, "timestamp": "2025-01-15T10:00:00+00:00"},
    ]
    thresholds = {"cpu": {"warning": 70, "critical": 90}, "memory": {"warning": 80, "critical": 95}}
    alerts = evaluate_metrics(metrics, thresholds)
    assert len(alerts) == 2  # cpu warning + memory critical

def test_evaluate_metrics_ignores_unknown():
    metrics = [{"name": "unknown_metric", "value": 100}]
    assert evaluate_metrics(metrics, {}) == []

def test_apply_cooldown_filters_rapid_alerts():
    alerts = [
        {"metric": "cpu", "value": 85, "timestamp": "2025-01-15T10:00:00+00:00", "level": "warning", "threshold": 70},
        {"metric": "cpu", "value": 87, "timestamp": "2025-01-15T10:01:00+00:00", "level": "warning", "threshold": 70},
        {"metric": "cpu", "value": 86, "timestamp": "2025-01-15T10:10:00+00:00", "level": "warning", "threshold": 70},
    ]
    filtered = apply_cooldown(alerts, cooldown_seconds=300)
    assert len(filtered) == 2  # first + third (10 min apart)

def test_run_integration(tmp_path: Path):
    metrics_file = tmp_path / "metrics.json"
    metrics_file.write_text(json.dumps([
        {"name": "cpu", "value": 85, "timestamp": "2025-01-15T10:00:00+00:00"},
        {"name": "disk", "value": 40, "timestamp": "2025-01-15T10:00:00+00:00"},
    ]), encoding="utf-8")
    thresholds_file = tmp_path / "thresholds.json"
    thresholds_file.write_text(json.dumps({"cpu": {"warning": 70, "critical": 90}}), encoding="utf-8")
    output = tmp_path / "report.json"
    report = run(metrics_file, thresholds_file, output)
    assert report["raw_alerts"] == 1
    assert output.exists()
