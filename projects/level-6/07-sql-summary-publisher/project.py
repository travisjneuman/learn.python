"""Level 6 / Project 07 — SQL Summary Publisher.

Runs aggregate queries against a SQLite database and publishes the
results as a formatted summary report (JSON + human-readable text).

Key concepts:
- GROUP BY with aggregate functions (COUNT, SUM, AVG, MIN, MAX)
- Subqueries for derived statistics
- Formatting query results into report sections
- Publishing summaries to both JSON and text outputs
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema & seed
# ---------------------------------------------------------------------------

SALES_DDL = """\
CREATE TABLE IF NOT EXISTS sales (
    id       INTEGER PRIMARY KEY,
    region   TEXT NOT NULL,
    product  TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    revenue  REAL NOT NULL,
    sale_date TEXT NOT NULL
);
"""


def seed_sales(conn: sqlite3.Connection, rows: list[dict]) -> int:
    """Insert sales rows (idempotent via IGNORE on PK)."""
    conn.execute(SALES_DDL)
    inserted = 0
    for r in rows:
        try:
            conn.execute(
                "INSERT OR IGNORE INTO sales (region, product, quantity, revenue, sale_date) "
                "VALUES (?, ?, ?, ?, ?)",
                (r["region"], r["product"], int(r["quantity"]), float(r["revenue"]), r["sale_date"]),
            )
            inserted += 1
        except (KeyError, ValueError) as exc:
            logging.warning("skip bad row: %s", exc)
    conn.commit()
    return inserted


# ---------------------------------------------------------------------------
# Aggregate queries
# ---------------------------------------------------------------------------


@dataclass
class SummaryReport:
    """Structured container for all summary sections."""

    total_sales: int = 0
    total_revenue: float = 0.0
    by_region: list[dict] = field(default_factory=list)
    by_product: list[dict] = field(default_factory=list)
    top_sale: dict = field(default_factory=dict)


def build_summary(conn: sqlite3.Connection) -> SummaryReport:
    """Run aggregate queries and assemble a SummaryReport."""
    report = SummaryReport()

    # Overall totals
    row = conn.execute(
        "SELECT COUNT(*), COALESCE(SUM(revenue), 0) FROM sales"
    ).fetchone()
    report.total_sales = row[0]
    report.total_revenue = round(row[1], 2)

    # By region
    for r in conn.execute(
        "SELECT region, COUNT(*) AS cnt, SUM(revenue) AS rev, AVG(revenue) AS avg_rev "
        "FROM sales GROUP BY region ORDER BY rev DESC"
    ).fetchall():
        report.by_region.append({
            "region": r[0],
            "count": r[1],
            "revenue": round(r[2], 2),
            "avg_revenue": round(r[3], 2),
        })

    # By product
    for r in conn.execute(
        "SELECT product, SUM(quantity) AS qty, SUM(revenue) AS rev "
        "FROM sales GROUP BY product ORDER BY rev DESC"
    ).fetchall():
        report.by_product.append({
            "product": r[0],
            "quantity": r[1],
            "revenue": round(r[2], 2),
        })

    # Top single sale
    top = conn.execute(
        "SELECT region, product, revenue, sale_date FROM sales ORDER BY revenue DESC LIMIT 1"
    ).fetchone()
    if top:
        report.top_sale = {
            "region": top[0], "product": top[1],
            "revenue": top[2], "date": top[3],
        }

    return report


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------


def format_text_report(report: SummaryReport) -> str:
    """Render the summary as a human-readable text block."""
    lines = [
        "=== SALES SUMMARY REPORT ===",
        f"Total sales: {report.total_sales}",
        f"Total revenue: ${report.total_revenue:,.2f}",
        "",
        "--- By Region ---",
    ]
    for r in report.by_region:
        lines.append(
            f"  {r['region']:<12} sales={r['count']}  revenue=${r['revenue']:>10,.2f}  "
            f"avg=${r['avg_revenue']:>8,.2f}"
        )

    lines.append("")
    lines.append("--- By Product ---")
    for p in report.by_product:
        lines.append(f"  {p['product']:<12} qty={p['quantity']}  revenue=${p['revenue']:>10,.2f}")

    if report.top_sale:
        lines.append("")
        lines.append("--- Top Sale ---")
        lines.append(
            f"  {report.top_sale['product']} in {report.top_sale['region']} "
            f"— ${report.top_sale['revenue']:,.2f} on {report.top_sale['date']}"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    """Load sales data, build summary, write JSON + text reports."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    sales_data = json.loads(input_path.read_text(encoding="utf-8"))

    conn = sqlite3.connect(db_path)
    try:
        inserted = seed_sales(conn, sales_data)
        report = build_summary(conn)
    finally:
        conn.close()

    summary_dict = {
        "rows_loaded": inserted,
        "total_sales": report.total_sales,
        "total_revenue": report.total_revenue,
        "by_region": report.by_region,
        "by_product": report.by_product,
        "top_sale": report.top_sale,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary_dict, indent=2), encoding="utf-8")

    text_path = output_path.with_suffix(".txt")
    text_path.write_text(format_text_report(report), encoding="utf-8")

    logging.info("published summary: %d sales, $%.2f revenue", report.total_sales, report.total_revenue)
    return summary_dict


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SQL Summary Publisher — aggregate queries to formatted reports"
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
