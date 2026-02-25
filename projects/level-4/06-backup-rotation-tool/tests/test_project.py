"""Tests for Backup Rotation Tool."""

from datetime import datetime, timezone
from pathlib import Path
import pytest

from project import parse_backup_date, classify_backups, run


@pytest.mark.parametrize(
    "filename, expected_date",
    [
        ("backup_2025-01-15_143022.tar.gz", "2025-01-15"),
        ("db_2024-12-31.sql", "2024-12-31"),
        ("no_date_here.zip", None),
        ("backup_9999-99-99.tar", None),  # invalid date
    ],
)
def test_parse_backup_date(filename: str, expected_date: str | None) -> None:
    result = parse_backup_date(filename)
    if expected_date is None:
        assert result is None
    else:
        assert result is not None
        assert result.strftime("%Y-%m-%d") == expected_date


def test_classify_keeps_recent_daily() -> None:
    now = datetime(2025, 1, 20, tzinfo=timezone.utc)
    files = [f"backup_2025-01-{d:02d}.tar.gz" for d in range(10, 21)]
    result = classify_backups(files, now, daily_keep=7, weekly_keep=0, monthly_keep=0)
    assert result["summary"]["keeping"] == 7
    assert result["summary"]["deleting"] == len(files) - 7


def test_classify_weekly_deduplication() -> None:
    """Only one backup per week should be kept in the weekly tier."""
    now = datetime(2025, 2, 1, tzinfo=timezone.utc)
    # Two backups in same week (Jan 27 and Jan 28 are both in week 4)
    files = ["backup_2025-01-27.tar.gz", "backup_2025-01-28.tar.gz"]
    result = classify_backups(files, now, daily_keep=0, weekly_keep=4, monthly_keep=0)
    weekly_kept = [k for k in result["keep"] if k["reason"] == "weekly"]
    assert len(weekly_kept) == 1


def test_classify_unparseable_files() -> None:
    now = datetime(2025, 1, 20, tzinfo=timezone.utc)
    files = ["readme.txt", "notes.md", "backup_2025-01-19.tar.gz"]
    result = classify_backups(files, now, daily_keep=7)
    assert result["summary"]["unparseable"] == 2
    assert result["summary"]["keeping"] >= 1


def test_run_integration(tmp_path: Path) -> None:
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()
    for day in range(1, 16):
        (backup_dir / f"backup_2025-01-{day:02d}.tar.gz").write_text("x")

    output = tmp_path / "report.json"
    now = datetime(2025, 1, 20, tzinfo=timezone.utc)
    report = run(backup_dir, output, now=now, daily=7, weekly=4, monthly=6)

    assert output.exists()
    assert report["summary"]["total"] == 15
    assert report["summary"]["keeping"] + report["summary"]["deleting"] == 15
