"""Level 6 / Project 05 — Transaction Rollback Drill.

Practices explicit transaction control with commit, rollback, and
savepoints in SQLite.  Demonstrates how partial failures can be
recovered without losing the entire batch.

Key concepts:
- BEGIN / COMMIT / ROLLBACK explicit transaction lifecycle
- SAVEPOINT / RELEASE / ROLLBACK TO for nested recovery
- Why autocommit is dangerous for multi-step operations
- Verifying database state after rollback
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

ACCOUNTS_DDL = """\
CREATE TABLE IF NOT EXISTS accounts (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    balance REAL NOT NULL CHECK(balance >= 0)
);
"""

AUDIT_DDL = """\
CREATE TABLE IF NOT EXISTS audit_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    action     TEXT NOT NULL,
    amount     REAL NOT NULL,
    status     TEXT NOT NULL,
    detail     TEXT
);
"""


@dataclass
class TransferResult:
    success: bool = False
    detail: str = ""


@dataclass
class BatchResult:
    committed: int = 0
    rolled_back: int = 0
    details: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Setup helpers
# ---------------------------------------------------------------------------


def init_db(conn: sqlite3.Connection) -> None:
    """Create tables (idempotent)."""
    conn.execute(ACCOUNTS_DDL)
    conn.execute(AUDIT_DDL)
    conn.commit()


def seed_accounts(conn: sqlite3.Connection, accounts: list[dict]) -> None:
    """Insert starting account balances (for demo purposes)."""
    for acct in accounts:
        conn.execute(
            "INSERT OR IGNORE INTO accounts (id, name, balance) VALUES (?, ?, ?)",
            (acct["id"], acct["name"], acct["balance"]),
        )
    conn.commit()


def get_balance(conn: sqlite3.Connection, account_id: int) -> float:
    """Read current balance for a single account."""
    row = conn.execute(
        "SELECT balance FROM accounts WHERE id = ?", (account_id,)
    ).fetchone()
    if row is None:
        raise ValueError(f"Account {account_id} not found")
    return row[0]


def get_all_accounts(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("SELECT id, name, balance FROM accounts ORDER BY id").fetchall()
    return [{"id": r[0], "name": r[1], "balance": r[2]} for r in rows]


# ---------------------------------------------------------------------------
# Transfer with savepoint
# ---------------------------------------------------------------------------


def transfer(
    conn: sqlite3.Connection,
    from_id: int,
    to_id: int,
    amount: float,
) -> TransferResult:
    """Transfer *amount* between two accounts using a SAVEPOINT.

    If the debit would make the source balance negative, we ROLLBACK
    to the savepoint so neither account is affected, but the outer
    transaction is still alive for other operations.
    """
    # WHY savepoints instead of full rollback? -- A SAVEPOINT creates a
    # nested checkpoint within a transaction. If one transfer fails, we
    # roll back to that savepoint only, leaving other successful transfers
    # intact. Without savepoints, ANY failure would roll back EVERYTHING.
    sp_name = f"sp_transfer_{from_id}_{to_id}"

    conn.execute(f"SAVEPOINT {sp_name}")
    try:
        # Debit source
        conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, from_id),
        )
        # Check constraint: balance >= 0
        new_balance = get_balance(conn, from_id)
        if new_balance < 0:
            raise ValueError(f"Insufficient funds: balance would be {new_balance}")

        # Credit destination
        conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, to_id),
        )

        conn.execute(f"RELEASE {sp_name}")

        # Audit
        conn.execute(
            "INSERT INTO audit_log (account_id, action, amount, status) "
            "VALUES (?, 'transfer_out', ?, 'ok')",
            (from_id, amount),
        )
        return TransferResult(success=True, detail=f"Transferred {amount}")

    except (sqlite3.IntegrityError, ValueError) as exc:
        conn.execute(f"ROLLBACK TO {sp_name}")
        conn.execute(f"RELEASE {sp_name}")
        logging.warning("rollback transfer from=%d to=%d err=%s", from_id, to_id, exc)

        conn.execute(
            "INSERT INTO audit_log (account_id, action, amount, status, detail) "
            "VALUES (?, 'transfer_out', ?, 'rolled_back', ?)",
            (from_id, amount, str(exc)),
        )
        return TransferResult(success=False, detail=str(exc))


# ---------------------------------------------------------------------------
# Batch processor
# ---------------------------------------------------------------------------


def process_batch(
    conn: sqlite3.Connection,
    transfers: list[dict],
) -> BatchResult:
    """Execute a batch of transfers inside a single outer transaction.

    Each transfer uses a savepoint so failures are isolated.
    """
    result = BatchResult()

    for t in transfers:
        tr = transfer(conn, t["from"], t["to"], t["amount"])
        if tr.success:
            result.committed += 1
        else:
            result.rolled_back += 1
        result.details.append(tr.detail)

    conn.commit()  # commit the outer transaction
    return result


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    data = json.loads(input_path.read_text(encoding="utf-8"))
    accounts = data.get("accounts", [])
    transfers = data.get("transfers", [])

    conn = sqlite3.connect(db_path)
    try:
        init_db(conn)
        seed_accounts(conn, accounts)
        result = process_batch(conn, transfers)
        final_accounts = get_all_accounts(conn)
    finally:
        conn.close()

    summary = {
        "committed": result.committed,
        "rolled_back": result.rolled_back,
        "details": result.details,
        "final_accounts": final_accounts,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transaction Rollback Drill — savepoints and recovery"
    )
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/output_summary.json")
    parser.add_argument("--db", default=":memory:")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output), args.db)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
