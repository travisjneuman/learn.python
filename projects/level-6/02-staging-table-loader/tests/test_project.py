"""Tests for Staging Table Loader.

Uses in-memory SQLite and temporary CSV files so tests run fast
and leave no side-effects on disk.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from project import (
    LoadResult,
    count_staged,
    create_staging_table,
    load_csv,
    load_rows,
    run,
    validate_row,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

CSV_HEADER = "timestamp,level,source,message\n"


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    create_staging_table(c)
    yield c
    c.close()


def _write_csv(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "input.csv"
    p.write_text(CSV_HEADER + body, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidation:
    @pytest.mark.parametrize(
        "row",
        [
            {"timestamp": "2025-01-01", "level": "INFO", "source": "app", "message": "ok"},
            {"timestamp": "2025-06-15", "level": "error", "source": "db", "message": "fail"},
        ],
    )
    def test_valid_rows_pass(self, row: dict) -> None:
        assert validate_row(row, 1) is None

    @pytest.mark.parametrize(
        "row,expected_fragment",
        [
            ({"timestamp": "", "level": "INFO", "source": "a", "message": "b"}, "missing_field=timestamp"),
            ({"timestamp": "t", "level": "BOGUS", "source": "a", "message": "b"}, "bad_level=BOGUS"),
            ({"timestamp": "t", "level": "INFO", "source": "", "message": "b"}, "missing_field=source"),
        ],
    )
    def test_invalid_rows_rejected(self, row: dict, expected_fragment: str) -> None:
        err = validate_row(row, 1)
        assert err is not None
        assert expected_fragment in err


# ---------------------------------------------------------------------------
# CSV loading
# ---------------------------------------------------------------------------


def test_load_csv_parses_rows(tmp_path: Path) -> None:
    p = _write_csv(tmp_path, "2025-01-01,INFO,app,started\n2025-01-02,WARN,db,slow\n")
    rows = load_csv(p)
    assert len(rows) == 2
    assert rows[0]["source"] == "app"


def test_load_csv_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_csv(tmp_path / "nope.csv")


# ---------------------------------------------------------------------------
# Database loading
# ---------------------------------------------------------------------------


def test_load_rows_accepts_valid(conn: sqlite3.Connection) -> None:
    rows = [
        {"timestamp": "2025-01-01", "level": "INFO", "source": "web", "message": "hit"},
        {"timestamp": "2025-01-02", "level": "ERROR", "source": "api", "message": "500"},
    ]
    result = load_rows(conn, rows)
    assert result.accepted == 2
    assert result.rejected == 0
    assert count_staged(conn) == 2


def test_load_rows_rejects_invalid(conn: sqlite3.Connection) -> None:
    rows = [
        {"timestamp": "2025-01-01", "level": "INFO", "source": "web", "message": "ok"},
        {"timestamp": "", "level": "INFO", "source": "web", "message": "bad"},  # missing ts
    ]
    result = load_rows(conn, rows)
    assert result.accepted == 1
    assert result.rejected == 1
    assert len(result.errors) == 1


# ---------------------------------------------------------------------------
# End-to-end
# ---------------------------------------------------------------------------


def test_run_end_to_end(tmp_path: Path) -> None:
    csv_path = _write_csv(
        tmp_path,
        "2025-01-01,INFO,app,boot\n2025-01-02,CRITICAL,db,down\n,INFO,x,bad\n",
    )
    out = tmp_path / "out.json"
    summary = run(csv_path, out)

    assert summary["accepted"] == 2
    assert summary["rejected"] == 1
    assert out.exists()
