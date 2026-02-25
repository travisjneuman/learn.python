"""Tests for Monitoring API Adapter."""

from __future__ import annotations

import json

import pytest

from project import (
    Metric,
    adapt_cpu,
    adapt_disk,
    adapt_memory,
    check_alerts,
    collect_all,
    mock_cpu_api,
    run,
)


class TestAdapters:
    def test_cpu_adapter(self) -> None:
        metrics = adapt_cpu(mock_cpu_api())
        assert len(metrics) == 2
        assert metrics[0].unit == "percent"

    def test_memory_adapter(self) -> None:
        raw = [{"type": "mem", "value_mb": 4000, "server": "s1", "at": "t"}]
        metrics = adapt_memory(raw)
        assert metrics[0].value == 4000

    def test_disk_adapter(self) -> None:
        raw = [{"check": "disk", "free_pct": 50.0, "node": "n1", "ts": "t"}]
        metrics = adapt_disk(raw)
        assert metrics[0].name == "disk_free"


class TestAlerts:
    @pytest.mark.parametrize("value,should_alert", [
        (45.0, False),
        (91.0, True),
        (90.0, False),
    ])
    def test_cpu_threshold(self, value: float, should_alert: bool) -> None:
        m = Metric(name="cpu_usage", value=value, unit="pct", source="h", timestamp="t")
        check_alerts([m])
        assert m.alert is should_alert

    def test_disk_low_free(self) -> None:
        m = Metric(name="disk_free", value=10.0, unit="pct", source="h", timestamp="t")
        check_alerts([m])
        assert m.alert is True

    def test_no_alert_for_unknown_metric(self) -> None:
        m = Metric(name="custom_metric", value=999, unit="x", source="h", timestamp="t")
        check_alerts([m])
        assert m.alert is False


class TestCollector:
    def test_collect_all_returns_metrics(self) -> None:
        metrics = collect_all()
        assert len(metrics) == 6  # 2 cpu + 2 memory + 2 disk


def test_run_end_to_end(tmp_path) -> None:
    out = tmp_path / "out.json"
    summary = run(tmp_path / "nope.json", out)
    assert summary["total_metrics"] == 6
    assert summary["alerts"] >= 1
    assert out.exists()
