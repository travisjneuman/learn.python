"""Level 6 / Project 01 — SQL Connection Simulator.

Teaches SQLite connection management with context managers,
connection pooling simulation, retry logic, and health checks.

Key concepts:
- sqlite3 connect / close lifecycle
- Context managers (with statement) for safe resource cleanup
- Connection pool pattern (reuse instead of recreate)
- Retry with exponential backoff on transient failures
"""

from __future__ import annotations

import argparse
import json
import logging
import random
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MAX_POOL_SIZE = 5
MAX_RETRIES = 3
BASE_BACKOFF_SEC = 0.01  # kept small for fast demo runs


@dataclass
class ConnectionConfig:
    """Immutable connection configuration."""

    db_path: str = ":memory:"
    timeout: float = 5.0
    max_retries: int = MAX_RETRIES
    pool_size: int = MAX_POOL_SIZE


# ---------------------------------------------------------------------------
# Connection pool
# ---------------------------------------------------------------------------


class ConnectionPool:
    """Simple SQLite connection pool.

    Real pools (e.g. SQLAlchemy's QueuePool) are far more capable, but
    this version teaches the core idea: *reuse connections instead of
    creating a new one for every query*.
    """

    def __init__(self, config: ConnectionConfig) -> None:
        self.config = config
        self._pool: list[sqlite3.Connection] = []
        self._created = 0  # total connections ever opened
        self._reused = 0

    # -- public API --------------------------------------------------------

    def acquire(self) -> sqlite3.Connection:
        """Return an existing connection or create a new one."""
        if self._pool:
            self._reused += 1
            logging.info("pool_reuse  total=%d reused=%d", self._created, self._reused)
            return self._pool.pop()

        conn = self._connect_with_retry()
        self._created += 1
        logging.info("pool_create total=%d reused=%d", self._created, self._reused)
        return conn

    def release(self, conn: sqlite3.Connection) -> None:
        """Return a connection to the pool (or close if pool is full)."""
        if len(self._pool) < self.config.pool_size:
            self._pool.append(conn)
        else:
            conn.close()

    def close_all(self) -> None:
        """Drain the pool and close every connection."""
        while self._pool:
            self._pool.pop().close()

    def stats(self) -> dict:
        """Return pool health metrics."""
        return {
            "created": self._created,
            "reused": self._reused,
            "idle": len(self._pool),
            "pool_size": self.config.pool_size,
        }

    # -- internals ---------------------------------------------------------

    def _connect_with_retry(self) -> sqlite3.Connection:
        """Open a connection, retrying on transient errors."""
        last_err: Exception | None = None
        for attempt in range(1, self.config.max_retries + 1):
            try:
                conn = sqlite3.connect(
                    self.config.db_path, timeout=self.config.timeout
                )
                conn.execute("SELECT 1")  # health-check ping
                return conn
            except sqlite3.OperationalError as exc:
                last_err = exc
                wait = BASE_BACKOFF_SEC * (2 ** (attempt - 1))
                logging.warning(
                    "connect_retry attempt=%d wait=%.3fs err=%s",
                    attempt, wait, exc,
                )
                time.sleep(wait)
        raise ConnectionError(
            f"Failed after {self.config.max_retries} retries: {last_err}"
        )


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


def health_check(conn: sqlite3.Connection) -> dict:
    """Run a lightweight ping and return status info."""
    try:
        cur = conn.execute("SELECT sqlite_version()")
        version = cur.fetchone()[0]
        return {"status": "healthy", "sqlite_version": version}
    except sqlite3.Error as exc:
        return {"status": "unhealthy", "error": str(exc)}


# ---------------------------------------------------------------------------
# Demo workload
# ---------------------------------------------------------------------------


def run_demo_queries(pool: ConnectionPool, labels: list[str]) -> list[dict]:
    """Simulate a workload: create a table, insert rows, query them back.

    Each label is inserted; then we query all rows to prove the
    connection works end-to-end.
    """
    conn = pool.acquire()
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS events "
            "(id INTEGER PRIMARY KEY, label TEXT NOT NULL)"
        )
        for label in labels:
            conn.execute("INSERT INTO events (label) VALUES (?)", (label,))
        conn.commit()

        rows = conn.execute("SELECT id, label FROM events ORDER BY id").fetchall()
        return [{"id": r[0], "label": r[1]} for r in rows]
    finally:
        pool.release(conn)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, config: ConnectionConfig | None = None) -> dict:
    """Full demo: read labels → pool → queries → stats → JSON output."""
    config = config or ConnectionConfig()
    pool = ConnectionPool(config)

    # Load labels from input file
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")
    labels = [
        ln.strip()
        for ln in input_path.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]

    rows = run_demo_queries(pool, labels)

    # Second acquire to demonstrate pool reuse
    conn2 = pool.acquire()
    hc = health_check(conn2)
    pool.release(conn2)

    pool.close_all()

    summary = {
        "rows_inserted": len(rows),
        "rows": rows,
        "health": hc,
        "pool_stats": pool.stats(),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("output=%s rows=%d", output_path, len(rows))
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SQL Connection Simulator — connection pooling & retry demo"
    )
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output_summary.json")
    parser.add_argument("--db", default=":memory:", help="SQLite database path")
    parser.add_argument(
        "--pool-size", type=int, default=MAX_POOL_SIZE, help="Max idle connections"
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    args = parse_args()
    config = ConnectionConfig(db_path=args.db, pool_size=args.pool_size)
    summary = run(Path(args.input), Path(args.output), config)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
