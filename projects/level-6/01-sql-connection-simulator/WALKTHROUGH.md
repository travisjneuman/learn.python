# SQL Connection Simulator — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) | [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. The goal is to build a connection pool for SQLite that reuses connections instead of creating new ones for every query, with retry logic for transient failures. If you can write a class that manages a list of connections and hands them out on request, you are already most of the way there.

## Thinking Process

The core problem here is resource management. Every time you open a database connection, there is overhead: memory allocation, file handles, and (in real databases) network handshakes. If your application makes hundreds of queries per second, opening and closing a connection for each one wastes enormous time. The solution is a pool: keep a small number of connections alive and reuse them.

Think of it like a library lending desk. Instead of buying a new book every time someone wants to read, the library keeps books on shelves and lends them out. When a reader finishes, the book goes back on the shelf for the next person. Your `ConnectionPool` is that lending desk. `acquire()` lends a connection out, and `release()` puts it back on the shelf.

The second challenge is handling failures gracefully. Databases can be temporarily unavailable (locked, restarting, overloaded). Rather than crashing immediately, your code should retry a few times with increasing delays between attempts. This is called exponential backoff: wait 10ms, then 20ms, then 40ms. The increasing gaps give the database time to recover without hammering it with rapid-fire retry attempts.

## Step 1: Define the Configuration

**What to do:** Create a `ConnectionConfig` dataclass that holds all the settings your pool needs: the database path, timeout, number of retries, and pool size.

**Why:** Centralizing configuration in a dataclass means you can pass one object around instead of four separate arguments. It also makes testing easier because you can create different configs for different scenarios.

```python
from dataclasses import dataclass

MAX_POOL_SIZE = 5
MAX_RETRIES = 3
BASE_BACKOFF_SEC = 0.01

@dataclass
class ConnectionConfig:
    db_path: str = ":memory:"
    timeout: float = 5.0
    max_retries: int = MAX_RETRIES
    pool_size: int = MAX_POOL_SIZE
```

**Predict:** What happens if you set `pool_size` to 0? Would connections still work, or would every connection be immediately closed after use?

## Step 2: Build the Connection Pool Class

**What to do:** Create a `ConnectionPool` class with an internal list `_pool` to hold idle connections and counters to track how many connections were created vs. reused.

**Why:** The pool is the heart of this project. The `_pool` list acts as a stack: connections are appended when released and popped when acquired. This last-in-first-out pattern keeps recently-used connections warm.

```python
class ConnectionPool:
    def __init__(self, config: ConnectionConfig) -> None:
        self.config = config
        self._pool: list[sqlite3.Connection] = []
        self._created = 0
        self._reused = 0
```

**Predict:** Why use a list as a stack (append/pop) rather than a queue (append/pop from front)? Think about which connection is most likely to still be valid.

## Step 3: Implement acquire() and release()

**What to do:** Write `acquire()` to check the pool first (reuse if possible, create if empty) and `release()` to return connections to the pool (or close them if the pool is full).

**Why:** This is where the performance gain comes from. The first call to `acquire()` creates a new connection. When you `release()` it, the connection goes into the pool. The next `acquire()` finds it there and reuses it — no creation overhead.

```python
def acquire(self) -> sqlite3.Connection:
    if self._pool:
        self._reused += 1
        return self._pool.pop()
    conn = self._connect_with_retry()
    self._created += 1
    return conn

def release(self, conn: sqlite3.Connection) -> None:
    if len(self._pool) < self.config.pool_size:
        self._pool.append(conn)
    else:
        conn.close()
```

**Predict:** What would happen if `release()` never checked the pool size and just always appended? How many open connections could you end up with?

## Step 4: Add Retry Logic with Exponential Backoff

**What to do:** Write `_connect_with_retry()` that attempts to connect up to `max_retries` times. On each failure, wait longer before trying again (exponential backoff). After the connection succeeds, run `SELECT 1` to verify it actually works.

**Why:** Databases can be temporarily locked or slow to start. A single failed attempt does not mean the database is permanently down. Exponential backoff avoids flooding a struggling server with retries while still recovering quickly from brief glitches.

```python
def _connect_with_retry(self) -> sqlite3.Connection:
    last_err = None
    for attempt in range(1, self.config.max_retries + 1):
        try:
            conn = sqlite3.connect(self.config.db_path, timeout=self.config.timeout)
            conn.execute("SELECT 1")  # health-check ping
            return conn
        except sqlite3.OperationalError as exc:
            last_err = exc
            wait = BASE_BACKOFF_SEC * (2 ** (attempt - 1))
            time.sleep(wait)
    raise ConnectionError(f"Failed after {self.config.max_retries} retries: {last_err}")
```

**Predict:** If `BASE_BACKOFF_SEC` is 0.01, what are the wait times for attempts 1, 2, and 3? (Calculate: 0.01 * 2^0, 0.01 * 2^1, 0.01 * 2^2.)

## Step 5: Write the Demo Workload

**What to do:** Create a function that acquires a connection, creates a table, inserts rows, queries them back, and releases the connection. Then acquire a second connection to demonstrate that the pool reuses the first one.

**Why:** This proves the pool works end-to-end. The second `acquire()` call should show a reused connection (not a newly created one) in the pool stats.

```python
def run_demo_queries(pool: ConnectionPool, labels: list[str]) -> list[dict]:
    conn = pool.acquire()
    try:
        conn.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, label TEXT NOT NULL)")
        for label in labels:
            conn.execute("INSERT INTO events (label) VALUES (?)", (label,))
        conn.commit()
        rows = conn.execute("SELECT id, label FROM events ORDER BY id").fetchall()
        return [{"id": r[0], "label": r[1]} for r in rows]
    finally:
        pool.release(conn)
```

**Predict:** Why is `pool.release(conn)` inside a `finally` block instead of after the return statement? What would happen if an exception occurred during the INSERT?

## Step 6: Wire Up the Orchestrator and CLI

**What to do:** Write a `run()` function that reads labels from an input file, runs the demo queries, performs a health check, and writes a JSON summary. Add `argparse` for CLI arguments.

**Why:** The orchestrator ties everything together and proves the system works as a whole. The JSON output gives you concrete evidence of what happened: how many rows were inserted, whether the health check passed, and how many connections were created vs. reused.

```python
def run(input_path: Path, output_path: Path, config: ConnectionConfig | None = None) -> dict:
    config = config or ConnectionConfig()
    pool = ConnectionPool(config)
    labels = [ln.strip() for ln in input_path.read_text().splitlines() if ln.strip()]
    rows = run_demo_queries(pool, labels)

    conn2 = pool.acquire()     # should be a pool REUSE
    hc = health_check(conn2)
    pool.release(conn2)
    pool.close_all()

    summary = {"rows_inserted": len(rows), "rows": rows, "health": hc, "pool_stats": pool.stats()}
    output_path.write_text(json.dumps(summary, indent=2))
    return summary
```

**Predict:** Look at the pool stats after running. `created` should be 1 and `reused` should be 1. Why not `created: 2`?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Forgetting to call `conn.commit()` after INSERTs | SQLite defaults to autocommit off for DML statements, so changes are invisible without an explicit commit | Always call `conn.commit()` after writes, or use `conn.execute()` with DDL (which auto-commits) |
| Not closing connections on error | If an exception occurs between `acquire()` and `release()`, the connection leaks | Wrap the usage in `try/finally` so `release()` always runs |
| Using `time.sleep()` with large values in retry logic | Copy-pasting production-style backoff values (1s, 2s, 4s) makes tests painfully slow | Use a small `BASE_BACKOFF_SEC` (e.g., 0.01) for demos and tests |
| Returning a closed connection to the pool | If you manually close a connection and then release it, the next acquire gets a broken connection | Check connection health before returning it to the pool (the "Fix it" exercise) |

## Testing Your Solution

```bash
pytest -q
```

You should see 8+ tests pass. The tests verify connection creation, pool reuse, retry behavior, health checks, and the full end-to-end pipeline.

## What You Learned

- **Connection pooling** reduces overhead by reusing database connections instead of creating new ones for every query. The pattern applies to any expensive resource: HTTP connections, thread pools, GPU memory.
- **Exponential backoff** is the standard approach for retrying transient failures. It prevents retry storms from overwhelming a recovering service.
- **Context managers and try/finally** ensure resources are always cleaned up, even when exceptions occur. Leaked connections are one of the most common causes of production database outages.
