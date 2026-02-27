"""Tests for Transaction Rollback Drill.

Verifies savepoint-based transfers: successful transfers, rollback on
insufficient funds, and batch processing with mixed outcomes.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from project import (
    get_all_accounts,
    get_balance,
    init_db,
    process_batch,
    run,
    seed_accounts,
    transfer,
)


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    init_db(c)
    seed_accounts(c, [
        {"id": 1, "name": "Alice", "balance": 100.0},
        {"id": 2, "name": "Bob", "balance": 50.0},
    ])
    yield c
    c.close()


class TestTransfer:
    def test_successful_transfer(self, conn: sqlite3.Connection) -> None:
        result = transfer(conn, from_id=1, to_id=2, amount=30.0)
        conn.commit()
        assert result.success is True
        assert get_balance(conn, 1) == pytest.approx(70.0)
        assert get_balance(conn, 2) == pytest.approx(80.0)

    def test_insufficient_funds_rolls_back(self, conn: sqlite3.Connection) -> None:
        result = transfer(conn, from_id=2, to_id=1, amount=999.0)
        conn.commit()
        assert result.success is False
        # Bob's balance should be unchanged
        assert get_balance(conn, 2) == pytest.approx(50.0)
        assert get_balance(conn, 1) == pytest.approx(100.0)

    @pytest.mark.parametrize("amount", [0.01, 50.0, 100.0])
    def test_edge_amounts(self, conn: sqlite3.Connection, amount: float) -> None:
        """Transfer should succeed for any amount up to the full balance."""
        result = transfer(conn, from_id=1, to_id=2, amount=amount)
        conn.commit()
        assert result.success is True
        assert get_balance(conn, 1) == pytest.approx(100.0 - amount)


class TestBatch:
    def test_mixed_batch(self, conn: sqlite3.Connection) -> None:
        transfers = [
            {"from": 1, "to": 2, "amount": 10.0},   # ok
            {"from": 2, "to": 1, "amount": 999.0},   # fail
            {"from": 1, "to": 2, "amount": 5.0},     # ok
        ]
        result = process_batch(conn, transfers)
        assert result.committed == 2
        assert result.rolled_back == 1
        # Alice: 100 - 10 - 5 = 85, Bob: 50 + 10 + 5 = 65
        assert get_balance(conn, 1) == pytest.approx(85.0)
        assert get_balance(conn, 2) == pytest.approx(65.0)


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    data = {
        "accounts": [
            {"id": 1, "name": "X", "balance": 200.0},
            {"id": 2, "name": "Y", "balance": 100.0},
        ],
        "transfers": [
            {"from": 1, "to": 2, "amount": 50.0},
            {"from": 2, "to": 1, "amount": 9999.0},
        ],
    }
    inp = tmp_path / "input.json"
    inp.write_text(json.dumps(data), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["committed"] == 1
    assert summary["rolled_back"] == 1
