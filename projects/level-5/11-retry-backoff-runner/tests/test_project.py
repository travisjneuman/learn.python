"""Tests for Retry Backoff Runner."""
from __future__ import annotations

import json
import pytest
from pathlib import Path

from project import (
    compute_delay,
    retry_with_backoff,
    create_flaky_function,
    run,
)


# ---------- compute_delay ----------

@pytest.mark.parametrize("attempt,base,factor,max_d,expected", [
    (1, 0.1, 2.0, 10.0, 0.1),    # 0.1 * 2^0
    (2, 0.1, 2.0, 10.0, 0.2),    # 0.1 * 2^1
    (3, 0.1, 2.0, 10.0, 0.4),    # 0.1 * 2^2
    (10, 0.1, 2.0, 5.0, 5.0),    # capped at max_delay
])
def test_compute_delay_no_jitter(
    attempt: int, base: float, factor: float, max_d: float, expected: float,
) -> None:
    result = compute_delay(attempt, base, factor, max_d, jitter=False)
    assert result == pytest.approx(expected)


def test_compute_delay_with_jitter() -> None:
    delay = compute_delay(1, 1.0, 2.0, 60.0, jitter=True)
    assert 0.5 <= delay <= 1.0  # jitter scales by 0.5-1.0


# ---------- retry_with_backoff ----------

def test_retry_succeeds_first_try() -> None:
    result, log = retry_with_backoff(lambda: "ok", max_retries=3, base_delay=0.001)
    assert result == "ok"
    assert len(log) == 1
    assert log[0]["status"] == "success"


def test_retry_succeeds_after_failures() -> None:
    func = create_flaky_function(fail_count=2)
    result, log = retry_with_backoff(func, max_retries=5, base_delay=0.001, jitter=False)
    assert result["result"] == "success"
    assert len(log) == 3  # 2 failures + 1 success


def test_retry_exhausts_retries() -> None:
    func = create_flaky_function(fail_count=10)
    with pytest.raises(ConnectionError):
        retry_with_backoff(func, max_retries=3, base_delay=0.001, jitter=False)


def test_retry_validates_parameters() -> None:
    with pytest.raises(ValueError, match="max_retries"):
        retry_with_backoff(lambda: None, max_retries=0)
    with pytest.raises(ValueError, match="base_delay"):
        retry_with_backoff(lambda: None, base_delay=-1)


def test_retry_log_tracks_delays() -> None:
    func = create_flaky_function(fail_count=2)
    _, log = retry_with_backoff(func, max_retries=5, base_delay=0.01, jitter=False)
    failed_entries = [e for e in log if e["status"] == "failed"]
    assert all("delay_seconds" in e for e in failed_entries)


# ---------- integration: run ----------

@pytest.mark.parametrize("fail_count,max_retries,expected_status", [
    (0, 3, "success"),
    (2, 5, "success"),
    (10, 3, "failed"),
])
def test_run_scenarios(
    tmp_path: Path, fail_count: int, max_retries: int, expected_status: str,
) -> None:
    output = tmp_path / "report.json"
    report = run(output, max_retries=max_retries, fail_count=fail_count)
    assert report["status"] == expected_status
    assert output.exists()
    saved = json.loads(output.read_text())
    assert saved["status"] == expected_status
