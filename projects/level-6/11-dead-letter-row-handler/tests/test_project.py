"""Tests for Dead Letter Row Handler.

Validates record processing, dead-letter routing, retry logic,
and statistics using in-memory SQLite.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from project import (
    dead_letter_stats,
    get_dead_letters,
    init_db,
    process_records,
    retry_dead_letter,
    run,
    validate_record,
)


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    init_db(c)
    yield c
    c.close()


class TestValidation:
    @pytest.mark.parametrize("rec", [
        {"name": "alpha", "value": 10},
        {"name": "beta", "value": "3.14"},
        {"name": "gamma", "value": 0},
    ])
    def test_valid_records(self, rec: dict) -> None:
        assert validate_record(rec) is None

    @pytest.mark.parametrize("rec,expected", [
        ({"name": "", "value": 1}, "missing_name"),
        ({"name": "x", "value": "abc"}, "invalid_value"),
        ({"name": "x"}, "invalid_value"),
    ])
    def test_invalid_records(self, rec: dict, expected: str) -> None:
        assert validate_record(rec) == expected


class TestProcessing:
    def test_valid_go_to_processed(self, conn: sqlite3.Connection) -> None:
        records = [{"name": "a", "value": 1}, {"name": "b", "value": 2}]
        result = process_records(conn, records)
        assert result.processed == 2
        assert result.dead_lettered == 0

    def test_invalid_go_to_dead_letter(self, conn: sqlite3.Connection) -> None:
        records = [{"name": "", "value": 1}, {"name": "ok", "value": "bad"}]
        result = process_records(conn, records)
        assert result.processed == 0
        assert result.dead_lettered == 2

    def test_mixed_batch(self, conn: sqlite3.Connection) -> None:
        records = [
            {"name": "good", "value": 10},
            {"name": "", "value": 5},  # bad
        ]
        result = process_records(conn, records)
        assert result.processed == 1
        assert result.dead_lettered == 1


class TestRetry:
    def test_retry_still_invalid(self, conn: sqlite3.Connection) -> None:
        process_records(conn, [{"name": "", "value": 1}])
        dls = get_dead_letters(conn)
        assert len(dls) == 1
        success = retry_dead_letter(conn, dls[0]["id"])
        assert success is False

    def test_stats(self, conn: sqlite3.Connection) -> None:
        process_records(conn, [
            {"name": "ok", "value": 1},
            {"name": "", "value": 1},
        ])
        stats = dead_letter_stats(conn)
        assert stats["total"] == 1
        assert stats["unresolved"] == 1


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    records = [
        {"name": "alpha", "value": 100},
        {"name": "beta", "value": "not_a_number"},
        {"name": "", "value": 50},
    ]
    inp = tmp_path / "data.json"
    inp.write_text(json.dumps(records), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["processed"] == 1
    assert summary["dead_lettered"] == 2
    assert out.exists()
