"""Tests for Upsert Strategy Lab.

Validates both upsert strategies, insert/update counting,
and error handling with in-memory SQLite.
"""

from __future__ import annotations

import sqlite3

import pytest

from project import (
    get_all_products,
    upsert_on_conflict,
    upsert_replace,
    PRODUCTS_DDL,
    run,
)


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    c.execute(PRODUCTS_DDL)
    c.commit()
    yield c
    c.close()


SEED = [
    {"sku": "ABC-001", "name": "Widget", "price": "9.99", "stock": "100"},
    {"sku": "ABC-002", "name": "Gadget", "price": "19.99", "stock": "50"},
]

UPDATE = [
    {"sku": "ABC-001", "name": "Widget Pro", "price": "12.99", "stock": "80"},
    {"sku": "ABC-003", "name": "Doohickey", "price": "5.99", "stock": "200"},
]


# ---------------------------------------------------------------------------
# Strategy: ON CONFLICT
# ---------------------------------------------------------------------------


class TestUpsertOnConflict:
    def test_insert_new_rows(self, conn: sqlite3.Connection) -> None:
        result = upsert_on_conflict(conn, SEED)
        assert result.inserted == 2
        assert result.updated == 0
        assert len(get_all_products(conn)) == 2

    def test_update_existing_row(self, conn: sqlite3.Connection) -> None:
        upsert_on_conflict(conn, SEED)
        result = upsert_on_conflict(conn, UPDATE)
        # ABC-001 updated, ABC-003 inserted
        assert result.updated == 1
        assert result.inserted == 1
        products = {p["sku"]: p for p in get_all_products(conn)}
        assert products["ABC-001"]["name"] == "Widget Pro"
        assert products["ABC-001"]["price"] == 12.99

    def test_bad_row_captured_as_error(self, conn: sqlite3.Connection) -> None:
        bad = [{"sku": "X", "name": "Y", "price": "not_a_number", "stock": "1"}]
        result = upsert_on_conflict(conn, bad)
        assert result.errors
        assert result.inserted == 0


# ---------------------------------------------------------------------------
# Strategy: REPLACE
# ---------------------------------------------------------------------------


class TestUpsertReplace:
    def test_replace_overwrites_row(self, conn: sqlite3.Connection) -> None:
        upsert_replace(conn, SEED)
        result = upsert_replace(conn, UPDATE)
        assert result.updated == 1
        assert result.inserted == 1

    @pytest.mark.parametrize("strategy_fn", [upsert_replace, upsert_on_conflict])
    def test_both_strategies_handle_empty_input(
        self, conn: sqlite3.Connection, strategy_fn
    ) -> None:
        result = strategy_fn(conn, [])
        assert result.inserted == 0
        assert result.updated == 0


# ---------------------------------------------------------------------------
# End-to-end
# ---------------------------------------------------------------------------


def test_run_end_to_end(tmp_path) -> None:
    csv_content = "sku,name,price,stock\nA1,Alpha,1.00,10\nA1,Alpha v2,2.00,20\n"
    inp = tmp_path / "input.csv"
    inp.write_text(csv_content, encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out, strategy="on_conflict")
    # First A1 is insert, second A1 is update
    assert summary["inserted"] == 1
    assert summary["updated"] == 1
    assert summary["final_products"] == 1
