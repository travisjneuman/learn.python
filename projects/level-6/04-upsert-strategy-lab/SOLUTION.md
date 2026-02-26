# Solution: Level 6 / Project 04 - Upsert Strategy Lab

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [README](./README.md) hints or re-read the
> relevant [concept docs](../../../concepts/) first.

---

## Complete solution

```python
"""Level 6 / Project 04 — Upsert Strategy Lab.

Demonstrates INSERT ... ON CONFLICT (upsert) patterns in SQLite for
keeping a table in sync with incoming data without duplicates.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

# WHY sku as PRIMARY KEY? -- SKU (Stock Keeping Unit) is the natural
# business identifier for a product. Making it the PK means SQLite
# enforces uniqueness, and ON CONFLICT can use it as the conflict target.
PRODUCTS_DDL = """\
CREATE TABLE IF NOT EXISTS products (
    sku        TEXT PRIMARY KEY,
    name       TEXT NOT NULL,
    price      REAL NOT NULL,
    stock      INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


@dataclass
class UpsertResult:
    """Tracks how many rows were inserted vs updated."""
    inserted: int = 0
    updated: int = 0
    errors: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_csv(path: Path) -> list[dict]:
    """Parse a CSV with columns: sku, name, price, stock."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------
# Upsert strategies
# ---------------------------------------------------------------------------


def upsert_replace(conn: sqlite3.Connection, rows: list[dict]) -> UpsertResult:
    """Strategy 1: INSERT OR REPLACE — simple but overwrites *all* columns.

    WHY this exists: OR REPLACE is the bluntest upsert. If the SKU exists,
    the entire row is DELETED and re-inserted. This means any columns the
    incoming data doesn't supply are lost (reset to defaults). Simple to
    understand, but dangerous when different systems own different columns.
    """
    conn.execute(PRODUCTS_DDL)
    result = UpsertResult()

    for idx, row in enumerate(rows, start=1):
        try:
            sku = row["sku"].strip()
            # WHY check existence before upsert? -- INSERT OR REPLACE
            # doesn't tell us whether it replaced or inserted. We need
            # the pre-check to accurately count inserts vs updates.
            existing = conn.execute(
                "SELECT 1 FROM products WHERE sku = ?", (sku,)
            ).fetchone()

            conn.execute(
                "INSERT OR REPLACE INTO products (sku, name, price, stock) "
                "VALUES (?, ?, ?, ?)",
                (sku, row["name"].strip(), float(row["price"]), int(row["stock"])),
            )

            if existing:
                result.updated += 1
            else:
                result.inserted += 1
        except (KeyError, ValueError) as exc:
            result.errors.append(f"row={idx} error={exc}")

    conn.commit()
    return result


def upsert_on_conflict(conn: sqlite3.Connection, rows: list[dict]) -> UpsertResult:
    """Strategy 2: INSERT ... ON CONFLICT DO UPDATE — selective merge.

    WHY prefer ON CONFLICT over OR REPLACE? -- OR REPLACE deletes the
    old row and re-inserts, losing any columns not in the incoming data
    (and resetting AUTOINCREMENT side effects). ON CONFLICT DO UPDATE
    modifies only the columns you list, preserving everything else.
    """
    conn.execute(PRODUCTS_DDL)
    result = UpsertResult()

    for idx, row in enumerate(rows, start=1):
        try:
            sku = row["sku"].strip()
            existing = conn.execute(
                "SELECT 1 FROM products WHERE sku = ?", (sku,)
            ).fetchone()

            # WHY list specific columns in SET? -- Only update the fields
            # we have new data for. If another system added a "category"
            # column, ON CONFLICT preserves it. OR REPLACE would wipe it.
            conn.execute(
                "INSERT INTO products (sku, name, price, stock) "
                "VALUES (?, ?, ?, ?) "
                "ON CONFLICT(sku) DO UPDATE SET "
                "  name = excluded.name, "
                "  price = excluded.price, "
                "  stock = excluded.stock, "
                "  updated_at = datetime('now')",
                (sku, row["name"].strip(), float(row["price"]), int(row["stock"])),
            )

            if existing:
                result.updated += 1
            else:
                result.inserted += 1
        except (KeyError, ValueError) as exc:
            result.errors.append(f"row={idx} error={exc}")

    conn.commit()
    return result


def get_all_products(conn: sqlite3.Connection) -> list[dict]:
    """Fetch every product row for inspection."""
    rows = conn.execute(
        "SELECT sku, name, price, stock, updated_at FROM products ORDER BY sku"
    ).fetchall()
    return [
        {"sku": r[0], "name": r[1], "price": r[2], "stock": r[3], "updated_at": r[4]}
        for r in rows
    ]


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(
    input_path: Path,
    output_path: Path,
    db_path: str = ":memory:",
    strategy: str = "on_conflict",
) -> dict:
    """Load CSV, apply chosen upsert strategy, write summary."""
    rows = load_csv(input_path)

    conn = sqlite3.connect(db_path)
    try:
        # WHY a strategy dispatch? -- Lets the caller choose at runtime
        # without duplicating the orchestration logic. Easy to extend
        # with new strategies (e.g., "merge_conditional") later.
        upsert_fn = upsert_on_conflict if strategy == "on_conflict" else upsert_replace
        result = upsert_fn(conn, rows)
        products = get_all_products(conn)
    finally:
        conn.close()

    summary = {
        "strategy": strategy,
        "input_rows": len(rows),
        "inserted": result.inserted,
        "updated": result.updated,
        "errors": result.errors,
        "final_products": len(products),
        "products": products,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("upsert strategy=%s inserted=%d updated=%d", strategy, result.inserted, result.updated)
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upsert Strategy Lab — INSERT ON CONFLICT patterns"
    )
    parser.add_argument("--input", default="data/sample_input.csv")
    parser.add_argument("--output", default="data/output_summary.json")
    parser.add_argument("--db", default=":memory:")
    parser.add_argument(
        "--strategy",
        choices=["replace", "on_conflict"],
        default="on_conflict",
        help="Which upsert strategy to demonstrate",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output), args.db, args.strategy)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Two explicit strategy functions | Makes the behavioral difference between REPLACE and ON CONFLICT visible and testable independently | Single function with a flag -- harder to read and test each path in isolation |
| Pre-check `SELECT 1` before upsert | Lets us accurately count inserts vs updates, which OR REPLACE and ON CONFLICT don't natively expose | Skip counting -- simpler but loses visibility into what changed |
| `excluded.name` syntax in ON CONFLICT | References the values that *would have* been inserted, making the SET clause self-contained | Repeating the bind parameters -- error-prone if you change the VALUES list |
| Strategy selection via CLI `--strategy` | Lets the user compare both approaches on the same data without code changes | Hardcoded strategy -- less educational |

## Alternative approaches

### Approach B: Conditional upsert (only update if newer)

```python
def upsert_if_newer(conn: sqlite3.Connection, rows: list[dict]) -> UpsertResult:
    """Only overwrite if the incoming data has a newer timestamp."""
    result = UpsertResult()
    for row in rows:
        sku = row["sku"].strip()
        conn.execute(
            "INSERT INTO products (sku, name, price, stock, updated_at) "
            "VALUES (?, ?, ?, ?, datetime('now')) "
            "ON CONFLICT(sku) DO UPDATE SET "
            "  name = excluded.name, "
            "  price = excluded.price, "
            "  stock = excluded.stock, "
            "  updated_at = datetime('now') "
            "WHERE excluded.updated_at > products.updated_at",
            (sku, row["name"], float(row["price"]), int(row["stock"])),
        )
    conn.commit()
    return result
```

**Trade-off:** Prevents stale data from overwriting newer data -- essential when multiple sources write to the same table with different latencies. More complex SQL and requires a reliable timestamp in every incoming row.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Non-numeric `price` value (e.g., "free") | `float(row["price"])` raises `ValueError`; the row is counted as an error | Validate data types before the upsert; reject with a clear message |
| Using `OR REPLACE` when another system added a column | The DELETE+INSERT cycle resets the unknown column to its DEFAULT, silently losing data | Prefer `ON CONFLICT DO UPDATE` which only touches the columns you specify |
| Duplicate SKUs with different casing ("ABC-1" vs "abc-1") | SQLite TEXT comparison is case-sensitive by default, so both rows are inserted as separate products | Normalize SKU casing (`.upper()`) before insert, or use `COLLATE NOCASE` on the column |
