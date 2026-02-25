"""Level 6 / Project 11 — Dead Letter Row Handler.

Routes rows that fail validation or processing to a dead-letter table
instead of dropping them. Failed rows can be inspected and retried.

Key concepts:
- Dead-letter queue pattern applied to database rows
- Storing error context (reason, timestamp, retry count) alongside data
- Retry logic: re-process dead-letter rows after fixing issues
- Separating "happy path" from error handling
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

    Rules: must have 'name' (non-empty) and 'value' (numeric).
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
    """Process each record: valid ones go to 'processed', invalid to dead-letters."""
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
    """Return all unresolved dead-letter rows."""
    rows = conn.execute(
        "SELECT id, payload, error, retry_count FROM dead_letters "
        "WHERE resolved_at IS NULL ORDER BY id"
    ).fetchall()
    return [
        {"id": r[0], "payload": json.loads(r[1]), "error": r[2], "retries": r[3]}
        for r in rows
    ]


def retry_dead_letter(conn: sqlite3.Connection, dl_id: int) -> bool:
    """Re-validate a dead-letter row.  If it now passes, move to processed.

    Returns True if the retry succeeded.
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
