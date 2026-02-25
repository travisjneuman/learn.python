"""Tests for Idempotency Key Builder.

Validates key generation determinism, duplicate detection, and
the end-to-end processing pipeline using in-memory SQLite.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from project import (
    all_keys,
    build_key,
    init_table,
    key_exists,
    process_operations,
    run,
    store_if_new,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    init_table(c)
    yield c
    c.close()


# ---------------------------------------------------------------------------
# Key generation
# ---------------------------------------------------------------------------


class TestBuildKey:
    def test_deterministic(self) -> None:
        """Same inputs always produce the same key."""
        assert build_key("a", "b") == build_key("a", "b")

    def test_order_matters(self) -> None:
        """Different ordering produces a different key."""
        assert build_key("a", "b") != build_key("b", "a")

    @pytest.mark.parametrize(
        "parts_a,parts_b",
        [
            (("ab", "cd"), ("abc", "d")),
            (("x", "y", "z"), ("xy", "z")),
        ],
    )
    def test_no_accidental_collision(self, parts_a: tuple, parts_b: tuple) -> None:
        """Pipe separator prevents naive concatenation collisions."""
        assert build_key(*parts_a) != build_key(*parts_b)


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------


class TestStorage:
    def test_store_new_key(self, conn: sqlite3.Connection) -> None:
        assert store_if_new(conn, "key1", "payload1") is True
        assert key_exists(conn, "key1") is True

    def test_duplicate_returns_false(self, conn: sqlite3.Connection) -> None:
        store_if_new(conn, "key1", "payload1")
        assert store_if_new(conn, "key1", "payload1") is False

    def test_all_keys_returns_stored(self, conn: sqlite3.Connection) -> None:
        store_if_new(conn, "k1", "p1")
        store_if_new(conn, "k2", "p2")
        keys = all_keys(conn)
        assert len(keys) == 2


# ---------------------------------------------------------------------------
# Processing pipeline
# ---------------------------------------------------------------------------


def test_process_deduplicates(conn: sqlite3.Connection) -> None:
    ops = [
        {"source": "web", "action": "login"},
        {"source": "web", "action": "login"},  # duplicate
        {"source": "api", "action": "fetch"},
    ]
    result = process_operations(conn, ops)
    assert result.processed == 2
    assert result.skipped == 1


# ---------------------------------------------------------------------------
# End-to-end
# ---------------------------------------------------------------------------


def test_run_end_to_end(tmp_path) -> None:
    ops = [
        {"source": "cron", "action": "backup"},
        {"source": "cron", "action": "backup"},
        {"source": "user", "action": "export"},
    ]
    input_file = tmp_path / "ops.json"
    input_file.write_text(json.dumps(ops), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(input_file, out)
    assert summary["processed"] == 2
    assert summary["skipped"] == 1
    assert summary["stored_keys"] == 2
    assert out.exists()
