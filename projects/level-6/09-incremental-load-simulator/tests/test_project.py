"""Tests for Incremental Load Simulator.

Validates watermark tracking, incremental vs full load behavior,
and correct skipping of already-loaded records.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from project import (
    count_events,
    get_watermark,
    incremental_load,
    init_db,
    run,
    set_watermark,
)


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    init_db(c)
    yield c
    c.close()


BATCH_1 = [
    {"id": 1, "name": "event_a", "modified_at": "2025-01-01T10:00:00"},
    {"id": 2, "name": "event_b", "modified_at": "2025-01-01T11:00:00"},
]

BATCH_2 = [
    {"id": 2, "name": "event_b", "modified_at": "2025-01-01T11:00:00"},  # already loaded
    {"id": 3, "name": "event_c", "modified_at": "2025-01-02T09:00:00"},  # new
]


class TestWatermark:
    def test_initial_watermark_is_none(self, conn: sqlite3.Connection) -> None:
        assert get_watermark(conn, "events") is None

    def test_set_and_get(self, conn: sqlite3.Connection) -> None:
        set_watermark(conn, "events", "2025-01-01T12:00:00")
        assert get_watermark(conn, "events") == "2025-01-01T12:00:00"

    def test_update_watermark(self, conn: sqlite3.Connection) -> None:
        set_watermark(conn, "events", "2025-01-01")
        set_watermark(conn, "events", "2025-01-02")
        assert get_watermark(conn, "events") == "2025-01-02"


class TestIncrementalLoad:
    def test_first_load_inserts_all(self, conn: sqlite3.Connection) -> None:
        stats = incremental_load(conn, BATCH_1)
        assert stats.loaded == 2
        assert stats.skipped == 0
        assert count_events(conn) == 2

    def test_second_load_skips_old(self, conn: sqlite3.Connection) -> None:
        incremental_load(conn, BATCH_1)
        stats = incremental_load(conn, BATCH_2)
        assert stats.loaded == 1
        assert stats.skipped == 1
        assert count_events(conn) == 3

    @pytest.mark.parametrize("batch_size", [0, 1, 5])
    def test_various_batch_sizes(self, conn: sqlite3.Connection, batch_size: int) -> None:
        records = [
            {"id": i, "name": f"evt_{i}", "modified_at": f"2025-01-{i+1:02d}T00:00:00"}
            for i in range(batch_size)
        ]
        stats = incremental_load(conn, records)
        assert stats.loaded == batch_size


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    inp = tmp_path / "events.json"
    inp.write_text(json.dumps(BATCH_1), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["loaded"] == 2
    assert summary["skipped"] == 0
    assert summary["previous_watermark"] is None
    assert out.exists()
