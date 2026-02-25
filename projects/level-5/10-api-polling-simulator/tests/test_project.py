"""Tests for API Polling Simulator."""
from __future__ import annotations

import json
import pytest
from pathlib import Path

from project import MockAPI, calculate_backoff, poll_with_backoff, run


# ---------- MockAPI ----------

def test_mock_api_success() -> None:
    api = MockAPI(failure_rate=0.0, seed=1)
    result = api.get_status()
    assert result["status"] == "ok"
    assert "value" in result
    assert result["call_number"] == 1


def test_mock_api_always_fails() -> None:
    api = MockAPI(failure_rate=1.0, seed=1)
    with pytest.raises(ConnectionError):
        api.get_status()


def test_mock_api_failure_rate_clamped() -> None:
    api = MockAPI(failure_rate=2.0)  # should be clamped to 1.0
    assert api.failure_rate == 1.0


# ---------- calculate_backoff ----------

@pytest.mark.parametrize("attempt,base,max_d,expected_max", [
    (0, 0.1, 5.0, 0.2),    # 0.1 * 2^0 = 0.1, +10% jitter <= 0.11
    (1, 0.1, 5.0, 0.3),    # 0.1 * 2^1 = 0.2, +10% jitter <= 0.22
    (10, 0.1, 5.0, 6.0),   # capped at max_delay=5.0, +10% jitter <= 5.5
])
def test_calculate_backoff(
    attempt: int,
    base: float,
    max_d: float,
    expected_max: float,
) -> None:
    delay = calculate_backoff(attempt, base, max_d, jitter=True)
    assert 0 < delay <= expected_max


def test_calculate_backoff_no_jitter() -> None:
    delay = calculate_backoff(2, 0.1, 5.0, jitter=False)
    assert delay == pytest.approx(0.4)  # 0.1 * 2^2 = 0.4


# ---------- poll_with_backoff ----------

@pytest.mark.parametrize("failure_rate,expect_all_success", [
    (0.0, True),
    (1.0, False),
])
def test_poll_success_and_failure(failure_rate: float, expect_all_success: bool) -> None:
    api = MockAPI(failure_rate=failure_rate, seed=42)
    results, errors = poll_with_backoff(api, max_polls=5, base_delay=0.001)
    if expect_all_success:
        assert len(results) == 5 and len(errors) == 0
    else:
        assert len(errors) > 0


def test_poll_stops_on_max_retries() -> None:
    api = MockAPI(failure_rate=1.0, seed=1)
    results, errors = poll_with_backoff(
        api, max_polls=10, max_retries=3, base_delay=0.001,
    )
    assert len(errors) == 3
    assert len(results) == 0


# ---------- integration: run ----------

def test_run_writes_report(tmp_path: Path) -> None:
    output = tmp_path / "results.json"
    report = run(output, max_polls=5, failure_rate=0.0, seed=1)
    assert report["successful"] == 5
    assert report["failed"] == 0
    assert output.exists()
    saved = json.loads(output.read_text())
    assert saved["successful"] == 5
    assert "success_rate" in saved


def test_run_with_failures(tmp_path: Path) -> None:
    output = tmp_path / "results.json"
    report = run(output, max_polls=5, failure_rate=0.5, seed=42)
    assert report["total_polls_attempted"] <= 5
    assert report["successful"] + report["failed"] == report["total_polls_attempted"]
