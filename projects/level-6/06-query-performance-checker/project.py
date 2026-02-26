"""Level 6 / Project 06 — Query Performance Checker.

Runs SQL queries against a SQLite database, captures EXPLAIN QUERY PLAN
output, measures execution time, and suggests indexes for slow queries.

Key concepts:
- EXPLAIN QUERY PLAN to inspect how SQLite executes a query
- CREATE INDEX to speed up filtered / sorted queries
- Timing queries with time.perf_counter for sub-millisecond precision
- Interpreting scan types: SCAN TABLE vs SEARCH TABLE USING INDEX
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
    """Insert *count* deterministic orders for benchmarking."""
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
    query: whether it does a full table SCAN (slow) or uses an INDEX
    (fast). This is the single most important tool for SQL optimization.
    """
    rows = conn.execute(f"EXPLAIN QUERY PLAN {sql}").fetchall()
    return [row[-1] for row in rows]


def analyze_query(conn: sqlite3.Connection, sql: str) -> QueryReport:
    """Time a query, capture its plan, and suggest improvements."""
    plan_lines = explain_query(conn, sql)
    uses_index = any("USING INDEX" in line or "USING COVERING INDEX" in line for line in plan_lines)

    start = time.perf_counter()
    conn.execute(sql).fetchall()
    elapsed_ms = (time.perf_counter() - start) * 1000

    suggestion = ""
    if not uses_index:
        # Try to identify which column might benefit from an index.
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
    """Create a single-column index and return the DDL used."""
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
    """Seed data, run queries, analyze plans, optionally add indexes."""
    conn = sqlite3.connect(db_path)
    try:
        seed_orders(conn)

        # Load custom queries from file, fall back to defaults
        if input_path.exists():
            queries = [
                ln.strip()
                for ln in input_path.read_text(encoding="utf-8").splitlines()
                if ln.strip() and not ln.strip().startswith("#")
            ]
        else:
            queries = DEFAULT_QUERIES

        reports_before: list[dict] = []
        for sql in queries:
            r = analyze_query(conn, sql)
            reports_before.append({
                "sql": r.sql,
                "plan": r.plan_lines,
                "elapsed_ms": r.elapsed_ms,
                "uses_index": r.uses_index,
                "suggestion": r.suggestion,
            })

        # Add indexes on commonly filtered columns
        indexes_created = []
        for col in ("customer", "product", "amount"):
            ddl = create_index(conn, "orders", col)
            indexes_created.append(ddl)

        reports_after: list[dict] = []
        for sql in queries:
            r = analyze_query(conn, sql)
            reports_after.append({
                "sql": r.sql,
                "plan": r.plan_lines,
                "elapsed_ms": r.elapsed_ms,
                "uses_index": r.uses_index,
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
