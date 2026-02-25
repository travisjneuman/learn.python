"""Tests for Level 6 Mini Capstone.

Validates the full ETL pipeline: staging, validation, upsert,
dead-letter, lineage, and watermark management.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from project import (
    get_watermark,
    init_db,
    load_to_target,
    run,
    set_watermark,
    stage_records,
    validate_record,
)


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    init_db(c)
    yield c
    c.close()


GOOD_RECORDS = [
    {"key": "evt-1", "name": "signup", "value": 1, "ts": "2025-01-15T08:00:00"},
    {"key": "evt-2", "name": "purchase", "value": 49.99, "ts": "2025-01-15T09:00:00"},
]

BAD_RECORDS = [
    {"key": "", "name": "orphan", "value": 10, "ts": "2025-01-15T10:00:00"},
    {"key": "evt-3", "name": "broken", "value": "not_number", "ts": "2025-01-15T11:00:00"},
]


class TestValidation:
    @pytest.mark.parametrize("rec", GOOD_RECORDS)
    def test_valid_records_pass(self, rec: dict) -> None:
        assert validate_record(rec) is None

    @pytest.mark.parametrize("rec,expected", [
        ({"key": "", "name": "x", "value": 1, "ts": "t"}, "missing_key"),
        ({"key": "k", "name": "x", "value": "bad", "ts": "t"}, "invalid_value"),
        ({"key": "k", "name": "x", "value": 1, "ts": ""}, "missing_timestamp"),
    ])
    def test_invalid_records(self, rec: dict, expected: str) -> None:
        assert validate_record(rec) == expected


class TestPipeline:
    def test_stage_valid_records(self, conn: sqlite3.Connection) -> None:
        result = stage_records(conn, GOOD_RECORDS, watermark=None)
        assert result.staged == 2
        assert result.rejected == 0

    def test_stage_rejects_invalid(self, conn: sqlite3.Connection) -> None:
        result = stage_records(conn, BAD_RECORDS, watermark=None)
        assert result.staged == 0
        assert result.rejected == 2

    def test_load_upserts_to_target(self, conn: sqlite3.Connection) -> None:
        stage_records(conn, GOOD_RECORDS, watermark=None)
        loaded = load_to_target(conn)
        assert loaded == 2
        count = conn.execute("SELECT COUNT(*) FROM target").fetchone()[0]
        assert count == 2

    def test_watermark_filters_old_records(self, conn: sqlite3.Connection) -> None:
        set_watermark(conn, "events_ts", "2025-01-15T08:30:00")
        result = stage_records(conn, GOOD_RECORDS, watermark="2025-01-15T08:30:00")
        # Only evt-2 (09:00) should pass the watermark filter
        assert result.staged == 1


class TestEndToEnd:
    def test_full_run(self, tmp_path) -> None:
        records = GOOD_RECORDS + BAD_RECORDS
        inp = tmp_path / "data.json"
        inp.write_text(json.dumps(records), encoding="utf-8")
        out = tmp_path / "out.json"

        summary = run(inp, out)
        assert summary["staged"] == 2
        assert summary["loaded"] == 2
        assert summary["rejected"] == 2
        assert summary["dead_letters"] == 2
        assert summary["lineage_entries"] >= 4  # at least stage + load for each good record
        assert out.exists()

    def test_idempotent_rerun(self, tmp_path) -> None:
        """Running twice with a persistent DB should not re-process old data."""
        db_path = str(tmp_path / "test.db")
        inp = tmp_path / "data.json"
        inp.write_text(json.dumps(GOOD_RECORDS), encoding="utf-8")
        out = tmp_path / "out.json"

        run(inp, out, db_path=db_path)
        summary2 = run(inp, out, db_path=db_path)
        # Second run should find nothing new (watermark filters all)
        assert summary2["staged"] == 0
