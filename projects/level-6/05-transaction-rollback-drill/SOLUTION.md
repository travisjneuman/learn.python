# Solution: Level 6 / Project 05 - Transaction Rollback Drill

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [README](./README.md) hints or re-read the
> relevant [concept docs](../../../concepts/) first.

---

## Complete solution

```python
"""Level 6 / Project 05 — Transaction Rollback Drill.

Practices explicit transaction control with commit, rollback, and
savepoints in SQLite. Demonstrates how partial failures can be
recovered without losing the entire batch.
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

# WHY CHECK(balance >= 0)? -- This is a database-level safety net. Even
# if the application code has a bug, the DB will refuse to store a
# negative balance. Defense in depth: validate in code AND in the schema.
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
    """Insert starting account balances (for demo purposes).

    WHY INSERT OR IGNORE? -- Makes seeding idempotent. Running the demo
    twice with a persistent database won't fail on duplicate PKs.
    """
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

    WHY savepoints instead of full rollback? -- A SAVEPOINT creates a
    nested checkpoint within a transaction. If one transfer fails, we
    roll back to that savepoint only, leaving other successful transfers
    intact. Without savepoints, ANY failure would roll back EVERYTHING.
    """
    sp_name = f"sp_transfer_{from_id}_{to_id}"

    conn.execute(f"SAVEPOINT {sp_name}")
    try:
        # WHY debit first? -- If debit fails (insufficient funds), we
        # haven't touched the destination account yet. This ordering
        # means a rollback only needs to undo one UPDATE, not two.
        conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, from_id),
        )
        # WHY check balance in Python after the UPDATE? -- The CHECK
        # constraint would also catch this, but catching it here lets
        # us produce a specific error message before the constraint fires.
        new_balance = get_balance(conn, from_id)
        if new_balance < 0:
            raise ValueError(f"Insufficient funds: balance would be {new_balance}")

        # Credit destination
        conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, to_id),
        )

        # WHY RELEASE? -- RELEASE marks the savepoint as successful.
        # The changes become part of the outer transaction (not yet
        # committed to disk -- that happens with the outer COMMIT).
        conn.execute(f"RELEASE {sp_name}")

        # Audit the success
        conn.execute(
            "INSERT INTO audit_log (account_id, action, amount, status) "
            "VALUES (?, 'transfer_out', ?, 'ok')",
            (from_id, amount),
        )
        return TransferResult(success=True, detail=f"Transferred {amount}")

    except (sqlite3.IntegrityError, ValueError) as exc:
        # WHY ROLLBACK TO + RELEASE? -- ROLLBACK TO undoes everything
        # since the savepoint was created. RELEASE then removes the
        # savepoint name so it can be reused. The outer transaction
        # remains alive for other transfers.
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

    WHY one outer transaction for the batch? -- Wrapping the batch in a
    single transaction means either all successes are committed together,
    or (if the outer commit fails) nothing is. Individual savepoints
    handle per-transfer rollbacks within that boundary.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| SAVEPOINT per transfer | Isolates each transfer so one failure does not roll back the entire batch | Full transaction per transfer -- safe but slow (disk flush after each commit) |
| CHECK constraint on balance | Database-level guard against negative balances; catches bugs even if Python validation is bypassed | Python-only validation -- faster but leaves a gap if someone executes SQL directly |
| Debit-before-credit ordering | If debit fails, credit never executes, minimizing the rollback surface | Credit-first -- would temporarily create money out of thin air before the debit |
| Audit log for both successes and failures | Full traceability; operators can see why a transfer was rolled back | Log only failures -- simpler but loses the complete picture |

## Alternative approaches

### Approach B: All-or-nothing batch rollback

```python
def process_batch_atomic(conn: sqlite3.Connection, transfers: list[dict]) -> BatchResult:
    """Roll back the ENTIRE batch if any single transfer fails."""
    result = BatchResult()
    conn.execute("BEGIN")
    try:
        for t in transfers:
            from_id, to_id, amount = t["from"], t["to"], t["amount"]
            conn.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (amount, from_id),
            )
            bal = get_balance(conn, from_id)
            if bal < 0:
                raise ValueError(f"Account {from_id} insufficient funds")
            conn.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (amount, to_id),
            )
            result.committed += 1
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        result.committed = 0
        result.rolled_back = len(transfers)
    return result
```

**Trade-off:** Guarantees the batch is fully consistent (all succeed or none do), which is correct for scenarios like payroll where partial application is worse than none. The savepoint approach is better when transfers are independent and partial success is acceptable.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Self-transfer (from_id == to_id) | The same account is debited and credited; balance stays the same but the audit log records a meaningless transaction | Add a guard: `if from_id == to_id: raise ValueError("self-transfer")` |
| Forgetting to RELEASE after ROLLBACK TO | The savepoint name remains active; subsequent savepoints with the same name cause confusing behavior | Always pair `ROLLBACK TO sp` with `RELEASE sp` |
| Removing SAVEPOINT logic (plain autocommit) | A mid-batch failure leaves the database in a half-committed state: some transfers applied, others not, with no way to recover | Never rely on autocommit for multi-step operations; always use explicit transactions |
