"""Level 6 / Project 03 — Idempotency Key Builder.

Generates deterministic idempotency keys for data operations and stores
them in SQLite so that duplicate processing is detected and skipped.

Key concepts:
- hashlib for deterministic hashing (SHA-256)
- UNIQUE constraints to enforce idempotency at the database level
- INSERT OR IGNORE to silently skip duplicates
- Separating key generation from storage for testability
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sqlite3
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

KEYS_DDL = """\
CREATE TABLE IF NOT EXISTS idempotency_keys (
    idem_key   TEXT PRIMARY KEY,
    payload    TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


# ---------------------------------------------------------------------------
# Key generation
# ---------------------------------------------------------------------------


def build_key(*parts: str) -> str:
    """Create a deterministic SHA-256 hex key from ordered string parts.

    Using a separator that cannot appear in normal data (the pipe
    character) prevents accidental collisions like
    build_key("ab", "cd") == build_key("abc", "d").
    """
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------


def init_table(conn: sqlite3.Connection) -> None:
    """Create the idempotency table if it doesn't exist."""
    conn.execute(KEYS_DDL)
    conn.commit()


def store_if_new(conn: sqlite3.Connection, key: str, payload: str) -> bool:
    """Attempt to insert *key*.  Return True if new, False if duplicate.

    INSERT OR IGNORE silently skips when the PRIMARY KEY already exists.
    We check rowcount to know whether the insert actually happened.
    """
    cur = conn.execute(
        "INSERT OR IGNORE INTO idempotency_keys (idem_key, payload) VALUES (?, ?)",
        (key, payload),
    )
    conn.commit()
    return cur.rowcount == 1


def key_exists(conn: sqlite3.Connection, key: str) -> bool:
    """Check whether an idempotency key has already been recorded."""
    row = conn.execute(
        "SELECT 1 FROM idempotency_keys WHERE idem_key = ?", (key,)
    ).fetchone()
    return row is not None


def all_keys(conn: sqlite3.Connection) -> list[dict]:
    """Return every stored key as a list of dicts (for diagnostics)."""
    rows = conn.execute(
        "SELECT idem_key, payload, created_at FROM idempotency_keys ORDER BY created_at"
    ).fetchall()
    return [{"key": r[0], "payload": r[1], "created_at": r[2]} for r in rows]


# ---------------------------------------------------------------------------
# Processing pipeline
# ---------------------------------------------------------------------------


@dataclass
class ProcessResult:
    processed: int = 0
    skipped: int = 0


def process_operations(
    conn: sqlite3.Connection,
    operations: list[dict],
) -> ProcessResult:
    """For each operation dict, build an idempotency key and store-or-skip.

    Each operation must have at least 'source' and 'action' fields.
    The key is derived from those fields so the same operation submitted
    twice results in one stored record.
    """
    result = ProcessResult()
    for op in operations:
        source = op.get("source", "unknown")
        action = op.get("action", "unknown")
        key = build_key(source, action)

        if store_if_new(conn, key, json.dumps(op)):
            result.processed += 1
            logging.info("new key=%s source=%s action=%s", key[:12], source, action)
        else:
            result.skipped += 1
            logging.info("dup key=%s source=%s action=%s", key[:12], source, action)

    return result


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    """Read operations from a JSON file, de-duplicate, and write summary."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    operations = json.loads(input_path.read_text(encoding="utf-8"))

    conn = sqlite3.connect(db_path)
    try:
        init_table(conn)
        result = process_operations(conn, operations)
        stored = all_keys(conn)
    finally:
        conn.close()

    summary = {
        "total_input": len(operations),
        "processed": result.processed,
        "skipped": result.skipped,
        "stored_keys": len(stored),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("idempotency processed=%d skipped=%d", result.processed, result.skipped)
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Idempotency Key Builder — deterministic dedup with SQLite"
    )
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/output_summary.json")
    parser.add_argument("--db", default=":memory:")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output), db_path=args.db)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
