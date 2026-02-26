"""Level 6 / Project 04 — Upsert Strategy Lab.

Demonstrates INSERT ... ON CONFLICT (upsert) patterns in SQLite for
keeping a table in sync with incoming data without duplicates.

Key concepts:
- INSERT OR REPLACE vs INSERT ... ON CONFLICT DO UPDATE
- UNIQUE constraints as the foundation for upsert
- Tracking update counts vs insert counts
- Comparing strategies: replace-all vs merge-fields
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

    If the SKU already exists, the entire row is deleted and re-inserted.
    This is the bluntest approach: easy to understand but you lose any
    columns that the incoming data doesn't supply.
    """
    conn.execute(PRODUCTS_DDL)
    result = UpsertResult()

    for idx, row in enumerate(rows, start=1):
        try:
            sku = row["sku"].strip()
            # Check whether the row exists before the upsert so we can
            # distinguish inserts from updates.
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
    (and resetting auto-increment side effects). ON CONFLICT DO UPDATE
    modifies only the columns you list, preserving everything else.
    This matters when different systems own different columns.
    """
    conn.execute(PRODUCTS_DDL)
    result = UpsertResult()

    for idx, row in enumerate(rows, start=1):
        try:
            sku = row["sku"].strip()
            existing = conn.execute(
                "SELECT 1 FROM products WHERE sku = ?", (sku,)
            ).fetchone()

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
