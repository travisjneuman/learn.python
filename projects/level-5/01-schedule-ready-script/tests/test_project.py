"""Tests for Schedule Ready Script."""

from datetime import datetime, timezone
from pathlib import Path
import pytest

from project import is_within_time_window, is_skip_day, acquire_lock, release_lock, do_work, run


@pytest.mark.parametrize(
    "hour, start, end, expected",
    [
        (10, 8, 18, True),    # within window
        (6, 8, 18, False),    # before window
        (20, 8, 18, False),   # after window
        (23, 22, 6, True),    # overnight window, late night
        (3, 22, 6, True),     # overnight window, early morning
        (12, 22, 6, False),   # overnight window, midday
    ],
)
def test_is_within_time_window(hour: int, start: int, end: int, expected: bool) -> None:
    now = datetime(2025, 1, 15, hour, 0, tzinfo=timezone.utc)
    assert is_within_time_window(now, start, end) == expected


def test_is_skip_day() -> None:
    # Wednesday = weekday 2
    wed = datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc)
    assert is_skip_day(wed, [2]) is True
    assert is_skip_day(wed, [0, 6]) is False


def test_acquire_and_release_lock(tmp_path: Path) -> None:
    lock = tmp_path / ".lock"
    assert acquire_lock(lock) is True
    assert acquire_lock(lock) is False  # already locked
    release_lock(lock)
    assert acquire_lock(lock) is True  # available again


def test_do_work(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_text("hello\nworld\n", encoding="utf-8")
    output_file = tmp_path / "output.json"
    result = do_work(input_file, output_file)
    assert result["processed"] == 2
    assert output_file.exists()


def test_run_outside_window(tmp_path: Path) -> None:
    now = datetime(2025, 1, 15, 3, 0, tzinfo=timezone.utc)
    result = run(
        tmp_path / "in.txt", tmp_path / "out.json", tmp_path / ".lock",
        now=now, start_hour=8, end_hour=18,
    )
    assert result["status"] == "skipped"
    assert result["reason"] == "outside_time_window"


def test_run_full_success(tmp_path: Path) -> None:
    input_file = tmp_path / "data.txt"
    input_file.write_text("line1\nline2\n", encoding="utf-8")
    result = run(
        input_file, tmp_path / "out.json", tmp_path / ".lock",
        now=datetime(2025, 1, 15, 12, 0, tzinfo=timezone.utc),
    )
    assert result["status"] == "completed"
    assert result["processed"] == 2
