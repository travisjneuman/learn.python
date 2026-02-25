"""Tests for Metrics Summary Engine."""
from __future__ import annotations

import json
import pytest
from pathlib import Path

from project import (
    percentile,
    standard_deviation,
    moving_average,
    summarize_metric,
    aggregate_metrics,
    run,
)


# ---------- percentile ----------

@pytest.mark.parametrize("values,p,expected", [
    ([1, 2, 3, 4, 5], 50, 3.0),
    ([1, 2, 3, 4, 5], 0, 1.0),
    ([1, 2, 3, 4, 5], 100, 5.0),
    ([10], 50, 10.0),
    ([10, 20], 50, 15.0),
    ([], 50, 0.0),
])
def test_percentile(values: list[float], p: float, expected: float) -> None:
    assert percentile(values, p) == expected


# ---------- standard deviation ----------

@pytest.mark.parametrize("values,expected", [
    ([10, 10, 10], 0.0),
    ([1, 2, 3, 4, 5], 1.41),
    ([], 0.0),
    ([42], 0.0),
])
def test_standard_deviation(values: list[float], expected: float) -> None:
    assert round(standard_deviation(values), 2) == expected


# ---------- moving average ----------

def test_moving_average_basic() -> None:
    result = moving_average([1, 2, 3, 4, 5], window=3)
    assert len(result) == 5
    assert result[0] == 1.0
    assert result[2] == 2.0  # avg of [1,2,3]
    assert result[4] == 4.0  # avg of [3,4,5]


def test_moving_average_empty() -> None:
    assert moving_average([], 3) == []


def test_moving_average_zero_window() -> None:
    assert moving_average([1, 2, 3], 0) == []


# ---------- summarize_metric ----------

def test_summarize_metric_normal() -> None:
    values = [10, 20, 30, 40, 50]
    result = summarize_metric(values)
    assert result["count"] == 5
    assert result["min"] == 10
    assert result["max"] == 50
    assert result["mean"] == 30.0
    assert "stddev" in result
    assert result["stddev"] > 0


def test_summarize_metric_empty() -> None:
    result = summarize_metric([])
    assert result["count"] == 0
    assert "warning" in result


# ---------- aggregate_metrics ----------

@pytest.mark.parametrize("data,expected_metrics,expected_skip", [
    (
        [
            {"name": "cpu", "value": 50},
            {"name": "cpu", "value": 70},
            {"name": "memory", "value": 80},
        ],
        ["cpu", "memory"],
        False,
    ),
    (
        [{"name": "x", "value": "not_a_number"}],
        [],
        True,
    ),
    (
        [{"name": "y", "value": None}],
        [],
        True,
    ),
])
def test_aggregate_metrics(
    data: list[dict],
    expected_metrics: list[str],
    expected_skip: bool,
) -> None:
    result = aggregate_metrics(data)
    for name in expected_metrics:
        assert name in result
    if not expected_metrics:
        assert len(result) == 0


# ---------- integration: run ----------

def test_run_writes_report(tmp_path: Path) -> None:
    input_data = [
        {"name": "latency", "value": 100},
        {"name": "latency", "value": 200},
        {"name": "latency", "value": 150},
        {"name": "errors", "value": 2},
    ]
    input_file = tmp_path / "metrics.json"
    input_file.write_text(json.dumps(input_data))

    output_file = tmp_path / "out" / "summary.json"
    report = run(input_file, output_file)

    assert output_file.exists()
    assert report["metric_count"] == 2
    assert report["total_entries"] == 4
    assert "latency" in report["metrics"]
    assert report["metrics"]["latency"]["summary"]["count"] == 3
