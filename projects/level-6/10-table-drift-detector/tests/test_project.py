"""Tests for Table Drift Detector.

Validates schema introspection, snapshot management, and drift
detection using in-memory SQLite.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from project import (
    ColumnInfo,
    detect_drift,
    get_latest_snapshot,
    get_table_schema,
    init_tracking_db,
    run,
    save_snapshot,
    schema_to_dict,
)


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    init_tracking_db(c)
    c.execute("CREATE TABLE test_tbl (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
    c.commit()
    yield c
    c.close()


class TestSchemaIntrospection:
    def test_reads_columns(self, conn: sqlite3.Connection) -> None:
        cols = get_table_schema(conn, "test_tbl")
        names = [c.name for c in cols]
        assert "id" in names
        assert "name" in names

    def test_to_dict(self, conn: sqlite3.Connection) -> None:
        cols = get_table_schema(conn, "test_tbl")
        d = schema_to_dict(cols)
        assert "id" in d
        assert d["name"]["type"] == "TEXT"


class TestSnapshots:
    def test_save_and_retrieve(self, conn: sqlite3.Connection) -> None:
        schema = {"id": {"type": "INTEGER"}, "name": {"type": "TEXT"}}
        save_snapshot(conn, "test_tbl", schema)
        latest = get_latest_snapshot(conn, "test_tbl")
        assert latest == schema

    def test_latest_returns_newest(self, conn: sqlite3.Connection) -> None:
        save_snapshot(conn, "test_tbl", {"v": "1"})
        save_snapshot(conn, "test_tbl", {"v": "2"})
        assert get_latest_snapshot(conn, "test_tbl") == {"v": "2"}


class TestDriftDetection:
    def test_no_drift(self) -> None:
        schema = {"id": {"type": "INT", "notnull": True, "pk": True}}
        report = detect_drift(schema, schema, "tbl")
        assert report.has_drift is False

    def test_added_column(self) -> None:
        old = {"id": {"type": "INT", "notnull": True, "pk": True}}
        new = {**old, "email": {"type": "TEXT", "notnull": False, "pk": False}}
        report = detect_drift(old, new, "tbl")
        assert report.has_drift is True
        assert "email" in report.added_columns

    def test_removed_column(self) -> None:
        old = {"id": {"type": "INT"}, "name": {"type": "TEXT"}}
        new = {"id": {"type": "INT"}}
        report = detect_drift(old, new, "tbl")
        assert "name" in report.removed_columns

    @pytest.mark.parametrize(
        "old_type,new_type",
        [("TEXT", "INTEGER"), ("REAL", "TEXT"), ("INTEGER", "BLOB")],
    )
    def test_type_change(self, old_type: str, new_type: str) -> None:
        old = {"col": {"type": old_type}}
        new = {"col": {"type": new_type}}
        report = detect_drift(old, new, "tbl")
        assert len(report.type_changes) == 1
        assert report.type_changes[0]["old_type"] == old_type


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    config = {
        "tables": [
            {
                "name": "users",
                "ddl_steps": [
                    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)"
                ],
            }
        ]
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["tables_checked"] == 1
    assert out.exists()
