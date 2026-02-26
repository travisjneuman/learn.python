# Solution: Level 6 / Project 03 - Idempotency Key Builder

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [README](./README.md) hints or re-read the
> relevant [concept docs](../../../concepts/) first.

---

## Complete solution

```python
"""Level 6 / Project 03 — Idempotency Key Builder.

Generates deterministic idempotency keys for data operations and stores
them in SQLite so that duplicate processing is detected and skipped.
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

    WHY SHA-256? -- We need a fixed-length, deterministic hash so the same
    inputs always produce the same key. SHA-256 has a vanishingly small
    collision probability (2^-128 for birthday attacks) and produces a
    clean 64-char hex string that fits in any TEXT column.

    WHY the pipe separator? -- Without it, build_key("ab", "cd") and
    build_key("abc", "d") would both hash "abcd" and collide. The pipe
    creates unambiguous boundaries: "ab|cd" != "abc|d".
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

    WHY INSERT OR IGNORE? -- This pushes duplicate detection to the
    database layer (the PRIMARY KEY constraint), which is atomic and
    race-condition-free. We check rowcount to know whether the insert
    actually happened (1 = new, 0 = duplicate already existed).
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

    WHY derive the key from source+action only? -- These two fields
    uniquely identify the logical operation. Other fields (like a
    description) may vary between retries but the operation itself is
    the same. Keying on the stable fields prevents re-execution.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| SHA-256 hash for idempotency keys | Fixed-length, deterministic, collision-resistant; fits cleanly in a TEXT PRIMARY KEY | Raw string concatenation -- variable length, readable, but bloats the index and risks collisions without a separator |
| Pipe separator between key parts | Prevents ambiguous boundaries (`"ab|cd"` != `"abc|d"`) | No separator -- simpler but creates silent hash collisions on boundary-shifted inputs |
| `INSERT OR IGNORE` for dedup | Atomic duplicate detection at the DB level; no race conditions between check-and-insert | Check-then-insert (SELECT then INSERT) -- two queries with a race window; another process could insert between them |
| Storing the full payload alongside the key | Enables auditing: you can inspect what data was originally processed for a given key | Key-only storage -- saves space but loses traceability |

## Alternative approaches

### Approach B: In-memory set for dedup (no database)

```python
def process_with_set(operations: list[dict]) -> ProcessResult:
    """Deduplicate using a Python set -- no database needed."""
    seen: set[str] = set()
    result = ProcessResult()
    for op in operations:
        key = build_key(op.get("source", ""), op.get("action", ""))
        if key in seen:
            result.skipped += 1
        else:
            seen.add(key)
            result.processed += 1
    return result
```

**Trade-off:** Much faster (no disk I/O) and simpler, but the dedup state is lost when the process exits. The SQLite approach persists keys across runs, which is essential for idempotency in systems that restart (cron jobs, serverless functions, crash recovery).

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Removing the pipe separator from `build_key` | `build_key("ab", "cd")` and `build_key("abc", "d")` both hash `"abcd"` and produce the same key -- silent data loss | Always use an unambiguous delimiter; test with boundary-shifted inputs |
| Missing `source` or `action` fields in input | `op.get("source", "unknown")` silently defaults, so unrelated operations with missing fields all hash to the same key | Validate required fields before calling `build_key`; raise or reject if missing |
| Using MD5 instead of SHA-256 | MD5 is cryptographically broken (known collision attacks) and not suitable where collision resistance matters | Stick with SHA-256; the performance difference is negligible for this use case |
