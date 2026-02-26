# Solution: Level 6 / Project 01 - SQL Connection Simulator

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [README](./README.md) hints or re-read the
> relevant [concept docs](../../../concepts/) first.

---

## Complete solution

```python
"""Level 6 / Project 01 — SQL Connection Simulator.

Teaches SQLite connection management with context managers,
connection pooling simulation, retry logic, and health checks.
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

    WHY pool connections? -- Creating a new database connection for every
    query involves TCP handshakes, authentication, and memory allocation.
    A pool keeps idle connections ready to reuse, cutting per-query
    overhead from milliseconds to microseconds.
    """

    def __init__(self, config: ConnectionConfig) -> None:
        self.config = config
        # WHY a list for the pool? -- A list acts as a LIFO stack; pop()
        # gives the most recently released connection, which is most likely
        # to still be alive and warm in the OS cache.
        self._pool: list[sqlite3.Connection] = []
        self._created = 0
        self._reused = 0

    def acquire(self) -> sqlite3.Connection:
        """Return an existing connection or create a new one."""
        # WHY try the pool first? -- Reusing an idle connection avoids the
        # overhead of sqlite3.connect() entirely. Only when the pool is
        # empty do we pay the cost of opening a new connection.
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
        # WHY check pool_size? -- Without a cap, the pool could grow
        # unboundedly during burst traffic, holding open file descriptors
        # that the OS eventually runs out of.
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

    def _connect_with_retry(self) -> sqlite3.Connection:
        """Open a connection, retrying on transient errors."""
        last_err: Exception | None = None
        for attempt in range(1, self.config.max_retries + 1):
            try:
                conn = sqlite3.connect(
                    self.config.db_path, timeout=self.config.timeout
                )
                # WHY SELECT 1? -- A connection can be "open" but the
                # database might be locked or corrupted. This lightweight
                # query verifies the connection works end-to-end.
                conn.execute("SELECT 1")
                return conn
            except sqlite3.OperationalError as exc:
                last_err = exc
                # WHY exponential backoff? -- A fixed delay hammers a
                # struggling server at constant rate. Doubling the wait
                # gives the server progressively more breathing room.
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
    """Run a lightweight ping and return status info.

    WHY a dedicated health check? -- In production, load balancers and
    monitoring systems poll /health endpoints. This function gives them
    a quick pass/fail signal without running real business queries.
    """
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

    WHY try/finally for pool.release? -- If an exception occurs mid-query,
    the connection must still be returned to the pool. Without finally,
    a leaked connection would exhaust the pool under repeated failures.
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
    """Full demo: read labels -> pool -> queries -> stats -> JSON output.

    WHY a single orchestrator? -- Centralizing the pipeline in one function
    makes the flow visible at a glance and gives tests a single entry
    point to exercise the complete happy path.
    """
    config = config or ConnectionConfig()
    pool = ConnectionPool(config)

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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| LIFO pool (list with pop/append) | Most-recently-used connection is warmest in OS cache and most likely still valid | FIFO queue -- fairer rotation but older connections are more likely stale |
| Exponential backoff on retry | Gives a struggling database progressively more breathing room between attempts | Fixed delay -- simpler but can overwhelm a recovering server |
| `ConnectionConfig` as a dataclass | Groups related settings into one immutable object, easier to pass around and test | Bare kwargs -- flexible but easy to mis-spell or forget a parameter |
| Separate `health_check` function | Decouples monitoring from business logic; can be reused by different callers | Inline check inside `run` -- couples monitoring to the demo workload |

## Alternative approaches

### Approach B: Context manager protocol

```python
class PooledConnection:
    """Use the pool via 'with' blocks for automatic release."""

    def __init__(self, pool: ConnectionPool) -> None:
        self._pool = pool
        self._conn: sqlite3.Connection | None = None

    def __enter__(self) -> sqlite3.Connection:
        self._conn = self._pool.acquire()
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._conn:
            self._pool.release(self._conn)
            self._conn = None

# Usage:
# with PooledConnection(pool) as conn:
#     conn.execute("SELECT ...")
```

**Trade-off:** The context manager guarantees release even if the caller forgets `finally`, which is safer in production code. The manual acquire/release approach used in the primary solution is more explicit and better for learning what happens under the hood.

### Approach C: Thread-safe pool with `queue.Queue`

```python
import queue

class ThreadSafePool:
    def __init__(self, config: ConnectionConfig) -> None:
        self._pool = queue.Queue(maxsize=config.pool_size)

    def acquire(self, timeout: float = 5.0) -> sqlite3.Connection:
        try:
            return self._pool.get(timeout=timeout)
        except queue.Empty:
            return sqlite3.connect(self.config.db_path)
```

**Trade-off:** Required when multiple threads share the pool (e.g., a web server). Adds complexity that is unnecessary for single-threaded scripts like this demo.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Forgetting to release a connection | Pool drains to zero idle connections; every subsequent acquire creates a new connection, defeating the pool's purpose | Always use `try/finally` or a context manager around `acquire()`/`release()` |
| Setting `pool_size=0` | Every released connection gets closed immediately -- the pool becomes a no-op and you pay full connect cost every time | Validate `pool_size >= 1` in `ConnectionConfig.__post_init__` |
| Returning a closed connection to the pool | Next `acquire()` returns a dead connection; the caller's first query raises `ProgrammingError` | Ping the connection (`SELECT 1`) in `release()` before putting it back |
