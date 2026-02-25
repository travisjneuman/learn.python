"""Level 1 project: Basic Expense Tracker.

Read expenses from a CSV file, categorise them, compute totals and
averages, and produce a spending summary report.

Concepts: csv module, dict aggregation, basic financial calculations.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def parse_expense(row: dict[str, str]) -> dict[str, object]:
    """Parse a single CSV row into a structured expense record.

    WHY validate here? -- Catching bad data at the parse step keeps
    downstream code simple.  Each expense needs a date, category,
    amount, and description.
    """
    required = ["date", "category", "amount", "description"]
    for key in required:
        if key not in row or not row[key].strip():
            raise ValueError(f"Missing required field: {key}")

    amount = float(row["amount"])
    if amount < 0:
        raise ValueError(f"Negative amount not allowed: {amount}")

    return {
        "date": row["date"].strip(),
        "category": row["category"].strip().lower(),
        "amount": round(amount, 2),
        "description": row["description"].strip(),
    }


def load_expenses(path: Path) -> list[dict[str, object]]:
    """Load expenses from a CSV file with headers.

    WHY csv.DictReader? -- DictReader maps each row to a dict keyed
    by the header names, so we can access fields by name instead of
    index.  This is more readable and resilient to column reordering.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    expenses = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append(parse_expense(row))
    return expenses


def total_by_category(expenses: list[dict[str, object]]) -> dict[str, float]:
    """Sum expenses per category.

    WHY group by category? -- Knowing where money goes is the primary
    purpose of expense tracking.  This is the core aggregation.
    """
    totals: dict[str, float] = {}
    for exp in expenses:
        cat = exp["category"]
        totals[cat] = round(totals.get(cat, 0) + exp["amount"], 2)
    return totals


def overall_stats(expenses: list[dict[str, object]]) -> dict[str, float]:
    """Compute total, average, min, and max across all expenses.

    WHY separate function? -- Statistics are useful independently of
    category breakdowns.  Keeping them separate makes testing easier.
    """
    if not expenses:
        return {"total": 0.0, "average": 0.0, "min": 0.0, "max": 0.0, "count": 0}

    amounts = [exp["amount"] for exp in expenses]
    total = round(sum(amounts), 2)
    return {
        "total": total,
        "average": round(total / len(amounts), 2),
        "min": min(amounts),
        "max": max(amounts),
        "count": len(amounts),
    }


def top_expenses(expenses: list[dict[str, object]], n: int = 3) -> list[dict[str, object]]:
    """Return the N largest expenses.

    WHY top-N? -- Identifying big-ticket items helps prioritise
    budget cuts.  Sorting + slicing is the standard pattern.
    """
    sorted_exp = sorted(expenses, key=lambda e: e["amount"], reverse=True)
    return sorted_exp[:n]


def format_report(
    category_totals: dict[str, float],
    stats: dict[str, float],
    top: list[dict[str, object]],
) -> str:
    """Format a human-readable expense report."""
    lines = ["=== Expense Report ===", ""]

    lines.append("  By Category:")
    for cat, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"    {cat:<20} ${total:>10.2f}")

    lines.append("")
    lines.append(f"  Total:   ${stats['total']:>10.2f}")
    lines.append(f"  Average: ${stats['average']:>10.2f}")
    lines.append(f"  Min:     ${stats['min']:>10.2f}")
    lines.append(f"  Max:     ${stats['max']:>10.2f}")
    lines.append(f"  Count:   {stats['count']}")

    if top:
        lines.append("")
        lines.append("  Top Expenses:")
        for exp in top:
            lines.append(f"    ${exp['amount']:>8.2f}  {exp['category']:<15} {exp['description']}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Basic Expense Tracker")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="CSV file with date,category,amount,description")
    parser.add_argument("--output", default="data/output.json")
    parser.add_argument("--top", type=int, default=3,
                        help="Number of top expenses to show")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    expenses = load_expenses(Path(args.input))
    cat_totals = total_by_category(expenses)
    stats = overall_stats(expenses)
    top = top_expenses(expenses, args.top)

    print(format_report(cat_totals, stats, top))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_data = {
        "category_totals": cat_totals,
        "stats": stats,
        "top_expenses": top,
    }
    output_path.write_text(json.dumps(output_data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
