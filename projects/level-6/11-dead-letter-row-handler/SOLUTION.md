# Solution: Level 6 / Project 11 - Dead Letter Row Handler

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [README](./README.md) hints or re-read the
> relevant [concept docs](../../../concepts/) first.

---

## Complete solution

```python
"""Level 6 / Project 11 — Dead Letter Row Handler.

Routes rows that fail validation or processing to a dead-letter table
instead of dropping them. Failed rows can be inspected and retried.
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

MAIN_DDL = """\
CREATE TABLE IF NOT EXISTS processed (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    payload TEXT NOT NULL,
    status  TEXT NOT NULL DEFAULT 'ok'
);
"""

# WHY a dead-letter table? -- Instead of silently dropping failed rows
# (data loss) or crashing the whole pipeline (one bad row blocks all),
# we route failures to a separate table with the error reason. This
# lets operators inspect what went wrong and retry after fixing the
# root cause — the same idea as a dead-letter queue in messaging.
DEAD_LETTER_DDL = """\
CREATE TABLE IF NOT EXISTS dead_letters (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    payload     TEXT NOT NULL,
    error       TEXT NOT NULL,
    retry_count INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    resolved_at TEXT
);
"""


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(MAIN_DDL)
    conn.execute(DEAD_LETTER_DDL)
    conn.commit()


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_record(record: dict) -> str | None:
    """Return error string if record is invalid, else None.

    WHY return a string instead of raising? -- Returning an error string
    lets the caller decide how to handle it (dead-letter, log, skip)
    without catching exceptions. Exceptions should be for unexpected
    failures, not expected validation results.
    """
    if not record.get("name", "").strip():
        return "missing_name"
    try:
        float(record["value"])
    except (KeyError, ValueError, TypeError):
        return "invalid_value"
    return None


# ---------------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------------


@dataclass
class ProcessResult:
    processed: int = 0
    dead_lettered: int = 0
    errors: list[str] = field(default_factory=list)


def process_records(
    conn: sqlite3.Connection,
    records: list[dict],
) -> ProcessResult:
    """Process each record: valid ones go to 'processed', invalid to dead-letters.

    WHY separate tables for good and bad rows? -- Mixing them in one
    table with a status column works but complicates every downstream
    query (you'd need WHERE status='ok' everywhere). Separate tables
    give clean queries for both the happy path and error investigation.
    """
    result = ProcessResult()

    for rec in records:
        error = validate_record(rec)
        payload = json.dumps(rec)

        if error:
            conn.execute(
                "INSERT INTO dead_letters (payload, error) VALUES (?, ?)",
                (payload, error),
            )
            result.dead_lettered += 1
            result.errors.append(f"{rec.get('name', '?')}: {error}")
            logging.warning("dead_letter name=%s error=%s", rec.get("name"), error)
        else:
            conn.execute(
                "INSERT INTO processed (payload) VALUES (?)", (payload,)
            )
            result.processed += 1

    conn.commit()
    return result


# ---------------------------------------------------------------------------
# Retry logic
# ---------------------------------------------------------------------------


def get_dead_letters(conn: sqlite3.Connection) -> list[dict]:
    """Return all unresolved dead-letter rows.

    WHY filter on resolved_at IS NULL? -- Resolved rows have been
    successfully retried and moved to processed. We only want to
    show (and potentially retry) the ones still pending.
    """
    rows = conn.execute(
        "SELECT id, payload, error, retry_count FROM dead_letters "
        "WHERE resolved_at IS NULL ORDER BY id"
    ).fetchall()
    return [
        {"id": r[0], "payload": json.loads(r[1]), "error": r[2], "retries": r[3]}
        for r in rows
    ]


def retry_dead_letter(conn: sqlite3.Connection, dl_id: int) -> bool:
    """Re-validate a dead-letter row. If it now passes, move to processed.

    WHY increment retry_count on failure? -- Tracks how many times
    we've attempted to reprocess this row. After N retries, you can
    mark it as permanently failed instead of retrying forever.
    """
    row = conn.execute(
        "SELECT payload, retry_count FROM dead_letters WHERE id = ?", (dl_id,)
    ).fetchone()
    if not row:
        return False

    record = json.loads(row[0])
    retries = row[1]

    error = validate_record(record)
    if error is None:
        # WHY move to processed instead of just marking resolved? --
        # The processed table is the "source of truth" for good data.
        # Downstream systems only read from processed, so the row
        # must actually be there.
        conn.execute(
            "INSERT INTO processed (payload) VALUES (?)", (json.dumps(record),)
        )
        conn.execute(
            "UPDATE dead_letters SET resolved_at = datetime('now') WHERE id = ?",
            (dl_id,),
        )
        conn.commit()
        return True

    conn.execute(
        "UPDATE dead_letters SET retry_count = ?, error = ? WHERE id = ?",
        (retries + 1, error, dl_id),
    )
    conn.commit()
    return False


def dead_letter_stats(conn: sqlite3.Connection) -> dict:
    """Return summary stats for the dead-letter table."""
    total = conn.execute("SELECT COUNT(*) FROM dead_letters").fetchone()[0]
    unresolved = conn.execute(
        "SELECT COUNT(*) FROM dead_letters WHERE resolved_at IS NULL"
    ).fetchone()[0]
    return {"total": total, "unresolved": unresolved, "resolved": total - unresolved}


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    records = json.loads(input_path.read_text(encoding="utf-8"))

    conn = sqlite3.connect(db_path)
    try:
        init_db(conn)
        result = process_records(conn, records)
        dl_stats = dead_letter_stats(conn)
        dl_rows = get_dead_letters(conn)
    finally:
        conn.close()

    summary = {
        "input_records": len(records),
        "processed": result.processed,
        "dead_lettered": result.dead_lettered,
        "dead_letter_stats": dl_stats,
        "dead_letters": dl_rows,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("processed=%d dead_lettered=%d", result.processed, result.dead_lettered)
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dead Letter Row Handler — quarantine and retry failed rows"
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
| Separate dead-letter table (not a status column) | Clean queries for both happy path and error investigation; downstream systems never see bad rows | Single table with status column -- simpler schema but every downstream query needs `WHERE status='ok'` |
| Store full payload in dead-letters | Enables retry without re-reading the original input; the row is self-contained | Store only the error and a reference -- saves space but requires the original input to be available for retries |
| retry_count tracking | Enables max-retry policies; prevents infinite retry loops on permanently bad data | No retry tracking -- simpler but risks retrying forever |
| resolved_at timestamp (not deletion) | Preserves the audit trail; you can see when failures were resolved and how many retries it took | Delete resolved rows -- saves space but loses error history |

## Alternative approaches

### Approach B: Error categorization with automatic retry policy

```python
TRANSIENT_ERRORS = {"timeout", "connection_refused", "lock_timeout"}
PERMANENT_ERRORS = {"missing_name", "invalid_value", "schema_mismatch"}

def should_retry(error: str, retry_count: int, max_retries: int = 3) -> bool:
    """Only retry transient errors, and only up to max_retries times."""
    if error in PERMANENT_ERRORS:
        return False  # never retry -- the data itself is bad
    if error in TRANSIENT_ERRORS and retry_count < max_retries:
        return True   # retry -- the error may resolve itself
    return False      # unknown error or max retries exceeded

def retry_all_eligible(conn: sqlite3.Connection, max_retries: int = 3) -> dict:
    """Retry all dead-letter rows that are eligible for retry."""
    dl_rows = get_dead_letters(conn)
    retried = 0
    for dl in dl_rows:
        if should_retry(dl["error"], dl["retries"], max_retries):
            retry_dead_letter(conn, dl["id"])
            retried += 1
    return {"checked": len(dl_rows), "retried": retried}
```

**Trade-off:** Categorizing errors prevents wasting retries on permanently bad data (like missing fields that won't magically appear). But it requires maintaining the error category lists, and new error types default to "no retry" which may be too conservative.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| `value: null` in JSON input | `float(record["value"])` raises `TypeError` on `None`; caught by the except clause but error message says "invalid_value" which is vague | Check for `None` explicitly before `float()` to produce a more specific error like "null_value" |
| Retrying a row that still has the same validation error | `retry_dead_letter` increments `retry_count` but the row stays in dead-letters forever | Implement a max-retry threshold; mark rows as "permanently_failed" after N attempts |
| Deleting the dead_letters table between runs | Any retry or stats query crashes with `OperationalError: no such table` | Always call `init_db()` at the start of every operation; the `IF NOT EXISTS` clause makes it safe |
