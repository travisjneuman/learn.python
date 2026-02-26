# Solution: Level 6 / Project 06 - Query Performance Checker

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [README](./README.md) hints or re-read the
> relevant [concept docs](../../../concepts/) first.

---

## Complete solution

```python
"""Level 6 / Project 06 — Query Performance Checker.

Runs SQL queries against a SQLite database, captures EXPLAIN QUERY PLAN
output, measures execution time, and suggests indexes for slow queries.
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema & seed data
# ---------------------------------------------------------------------------

ORDERS_DDL = """\
CREATE TABLE IF NOT EXISTS orders (
    id         INTEGER PRIMARY KEY,
    customer   TEXT NOT NULL,
    product    TEXT NOT NULL,
    amount     REAL NOT NULL,
    created_at TEXT NOT NULL
);
"""


def seed_orders(conn: sqlite3.Connection, count: int = 500) -> None:
    """Insert *count* deterministic orders for benchmarking.

    WHY deterministic data? -- Using modular arithmetic (i % len) instead
    of random values makes the results reproducible across runs. You can
    predict exactly how many "alice" or "widget" rows exist, which makes
    it easy to verify query results.
    """
    conn.execute(ORDERS_DDL)
    existing = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    if existing >= count:
        return

    customers = ["alice", "bob", "charlie", "diana", "eve"]
    products = ["widget", "gadget", "bolt", "nut", "spring"]

    rows = []
    for i in range(count):
        rows.append((
            i + 1,
            customers[i % len(customers)],
            products[i % len(products)],
            round(10.0 + (i % 50) * 1.5, 2),
            f"2025-01-{(i % 28) + 1:02d}",
        ))

    # WHY executemany here but row-by-row elsewhere? -- Seed data is
    # trusted and uniform; no validation needed. executemany is 5-10x
    # faster for bulk inserts because it batches the I/O.
    conn.executemany(
        "INSERT OR IGNORE INTO orders (id, customer, product, amount, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Query plan analysis
# ---------------------------------------------------------------------------


@dataclass
class QueryReport:
    """Analysis report for a single query."""
    sql: str
    plan_lines: list[str] = field(default_factory=list)
    elapsed_ms: float = 0.0
    uses_index: bool = False
    suggestion: str = ""


def explain_query(conn: sqlite3.Connection, sql: str) -> list[str]:
    """Run EXPLAIN QUERY PLAN and return the textual plan lines.

    WHY EXPLAIN QUERY PLAN? -- It reveals how SQLite will execute the
    query without actually running it. The output tells you whether
    SQLite does a full table SCAN (reads every row) or uses an INDEX
    (jumps directly to matching rows). This is the single most important
    tool for SQL performance diagnosis.
    """
    rows = conn.execute(f"EXPLAIN QUERY PLAN {sql}").fetchall()
    # WHY row[-1]? -- EXPLAIN QUERY PLAN returns tuples where the last
    # element is the human-readable description string. The earlier
    # elements are internal IDs we don't need for analysis.
    return [row[-1] for row in rows]


def analyze_query(conn: sqlite3.Connection, sql: str) -> QueryReport:
    """Time a query, capture its plan, and suggest improvements."""
    plan_lines = explain_query(conn, sql)
    uses_index = any("USING INDEX" in line or "USING COVERING INDEX" in line for line in plan_lines)

    # WHY perf_counter? -- time.time() has ~15ms resolution on Windows.
    # perf_counter() uses the OS high-resolution timer, giving
    # sub-microsecond precision needed for fast queries.
    start = time.perf_counter()
    conn.execute(sql).fetchall()
    elapsed_ms = (time.perf_counter() - start) * 1000

    suggestion = ""
    if not uses_index:
        sql_upper = sql.upper()
        if "WHERE" in sql_upper:
            suggestion = "Consider adding an index on the filtered column(s)."
        elif "ORDER BY" in sql_upper:
            suggestion = "Consider adding an index on the ORDER BY column(s)."

    return QueryReport(
        sql=sql,
        plan_lines=plan_lines,
        elapsed_ms=round(elapsed_ms, 3),
        uses_index=uses_index,
        suggestion=suggestion,
    )


# ---------------------------------------------------------------------------
# Index helper
# ---------------------------------------------------------------------------


def create_index(conn: sqlite3.Connection, table: str, column: str) -> str:
    """Create a single-column index and return the DDL used.

    WHY IF NOT EXISTS? -- Makes the operation idempotent. Running the
    script twice won't crash on "index already exists" errors.
    """
    idx_name = f"idx_{table}_{column}"
    ddl = f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table} ({column})"
    conn.execute(ddl)
    conn.commit()
    return ddl


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

DEFAULT_QUERIES = [
    "SELECT * FROM orders WHERE customer = 'alice'",
    "SELECT * FROM orders WHERE amount > 50 ORDER BY created_at",
    "SELECT customer, SUM(amount) FROM orders GROUP BY customer",
    "SELECT * FROM orders WHERE product = 'widget' AND amount > 30",
]


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    """Seed data, run queries, analyze plans, optionally add indexes.

    WHY before/after comparison? -- Showing the query plan and timing
    both before and after adding indexes makes the impact visible.
    This is how you learn to identify which queries benefit from indexes.
    """
    conn = sqlite3.connect(db_path)
    try:
        seed_orders(conn)

        if input_path.exists():
            queries = [
                ln.strip()
                for ln in input_path.read_text(encoding="utf-8").splitlines()
                if ln.strip() and not ln.strip().startswith("#")
            ]
        else:
            queries = DEFAULT_QUERIES

        # Analyze BEFORE indexes
        reports_before: list[dict] = []
        for sql in queries:
            r = analyze_query(conn, sql)
            reports_before.append({
                "sql": r.sql, "plan": r.plan_lines,
                "elapsed_ms": r.elapsed_ms, "uses_index": r.uses_index,
                "suggestion": r.suggestion,
            })

        # Add indexes on commonly filtered columns
        indexes_created = []
        for col in ("customer", "product", "amount"):
            ddl = create_index(conn, "orders", col)
            indexes_created.append(ddl)

        # Analyze AFTER indexes
        reports_after: list[dict] = []
        for sql in queries:
            r = analyze_query(conn, sql)
            reports_after.append({
                "sql": r.sql, "plan": r.plan_lines,
                "elapsed_ms": r.elapsed_ms, "uses_index": r.uses_index,
            })

    finally:
        conn.close()

    summary = {
        "queries_analyzed": len(queries),
        "indexes_created": indexes_created,
        "before": reports_before,
        "after": reports_after,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("analyzed %d queries, created %d indexes", len(queries), len(indexes_created))
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query Performance Checker — EXPLAIN QUERY PLAN & index suggestions"
    )
    parser.add_argument("--input", default="data/sample_input.txt")
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
| Before/after comparison in a single run | Shows the concrete impact of indexes on the same queries with the same data | Separate scripts -- harder to compare and more error-prone |
| `time.perf_counter()` for timing | Sub-microsecond precision; not affected by system clock adjustments | `time.time()` -- coarse resolution (~15ms on Windows), can be skewed by NTP |
| Deterministic seed data | Reproducible benchmarks; you can predict row counts and verify results | Random data -- more realistic but results vary between runs, complicating tests |
| Single-column indexes first | Simplest optimization; covers most WHERE clauses on individual columns | Composite indexes -- more powerful but harder to reason about for beginners |

## Alternative approaches

### Approach B: Composite index for multi-column queries

```python
def create_composite_index(conn: sqlite3.Connection, table: str, columns: list[str]) -> str:
    """Create a multi-column index covering compound WHERE clauses."""
    col_str = ", ".join(columns)
    idx_name = f"idx_{table}_{'_'.join(columns)}"
    ddl = f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table} ({col_str})"
    conn.execute(ddl)
    conn.commit()
    return ddl

# Usage: create_composite_index(conn, "orders", ["product", "amount"])
# Benefits: SELECT * FROM orders WHERE product='widget' AND amount > 30
# can use a single index scan instead of two separate scans.
```

**Trade-off:** Composite indexes are more efficient for multi-column queries but take more disk space, slow down INSERT/UPDATE operations, and the column order matters (leftmost prefix rule). Start with single-column indexes and add composites only when profiling shows the need.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Indexing a column never used in WHERE | The index wastes disk space and slows writes without improving any query | Only index columns that appear in WHERE, JOIN, or ORDER BY clauses of actual queries |
| Passing invalid SQL to `explain_query` | `conn.execute(f"EXPLAIN QUERY PLAN {sql}")` raises `OperationalError` and crashes the analysis | Wrap `analyze_query` in try/except and return an error report instead of crashing |
| Benchmarking with too few rows | SQLite's query planner may choose a full scan even with an index if the table is tiny (the overhead of using the index exceeds the scan cost) | Seed at least 500+ rows for meaningful performance comparisons |
