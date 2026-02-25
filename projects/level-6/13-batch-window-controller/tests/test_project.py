"""Tests for Batch Window Controller.

Validates window creation, overlap detection, gap detection,
and status transitions using in-memory SQLite.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from project import (
    Window,
    create_window,
    detect_gaps,
    detect_overlaps,
    get_all_windows,
    init_db,
    run,
    update_status,
)


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    init_db(c)
    yield c
    c.close()


class TestWindowManagement:
    def test_create_window(self, conn: sqlite3.Connection) -> None:
        wid = create_window(conn, "2025-01-01T00:00", "2025-01-01T06:00")
        assert wid > 0

    def test_invalid_range_raises(self, conn: sqlite3.Connection) -> None:
        with pytest.raises(ValueError, match="end_ts must be after"):
            create_window(conn, "2025-01-02", "2025-01-01")

    def test_status_transitions(self, conn: sqlite3.Connection) -> None:
        wid = create_window(conn, "2025-01-01T00:00", "2025-01-01T06:00")
        update_status(conn, wid, "running")
        update_status(conn, wid, "completed")
        wins = get_all_windows(conn)
        assert wins[0].status == "completed"

    @pytest.mark.parametrize("bad_status", ["invalid", "done", ""])
    def test_invalid_status_raises(self, conn: sqlite3.Connection, bad_status: str) -> None:
        wid = create_window(conn, "2025-01-01T00:00", "2025-01-01T06:00")
        with pytest.raises(ValueError):
            update_status(conn, wid, bad_status)


class TestOverlapDetection:
    def test_no_overlap(self) -> None:
        wins = [
            Window(start_ts="2025-01-01T00:00", end_ts="2025-01-01T06:00"),
            Window(start_ts="2025-01-01T06:00", end_ts="2025-01-01T12:00"),
        ]
        assert detect_overlaps(wins) == []

    def test_overlap_detected(self) -> None:
        wins = [
            Window(start_ts="2025-01-01T00:00", end_ts="2025-01-01T08:00"),
            Window(start_ts="2025-01-01T06:00", end_ts="2025-01-01T12:00"),
        ]
        overlaps = detect_overlaps(wins)
        assert len(overlaps) == 1


class TestGapDetection:
    def test_no_gaps(self) -> None:
        wins = [
            Window(start_ts="2025-01-01T00:00", end_ts="2025-01-01T12:00"),
            Window(start_ts="2025-01-01T12:00", end_ts="2025-01-02T00:00"),
        ]
        gaps = detect_gaps(wins, "2025-01-01T00:00", "2025-01-02T00:00")
        assert gaps == []

    def test_gap_found(self) -> None:
        wins = [
            Window(start_ts="2025-01-01T00:00", end_ts="2025-01-01T06:00"),
            Window(start_ts="2025-01-01T12:00", end_ts="2025-01-01T18:00"),
        ]
        gaps = detect_gaps(wins, "2025-01-01T00:00", "2025-01-02T00:00")
        # Gap from 06:00 to 12:00, and from 18:00 to next day
        assert len(gaps) == 2


def test_run_end_to_end(tmp_path) -> None:
    config = {
        "range_start": "2025-01-01T00:00",
        "range_end": "2025-01-02T00:00",
        "windows": [
            {"start": "2025-01-01T00:00", "end": "2025-01-01T08:00", "status": "completed"},
            {"start": "2025-01-01T06:00", "end": "2025-01-01T14:00"},
        ],
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["windows_created"] == 2
    assert summary["overlaps_found"] == 1
    assert out.exists()
