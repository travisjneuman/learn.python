# Solution: Level 1 / Project 14 - Basic Expense Tracker

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: Basic Expense Tracker.

Read expenses from a CSV file, categorise them, compute totals and
averages, and produce a spending summary report.

Concepts: csv module, dict aggregation, basic financial calculations.
"""


import argparse
import csv
from pathlib import Path


# WHY parse_expense: This function is the data gateway — it converts
# raw CSV strings into validated, typed Python data.  Catching bad
# data here keeps all downstream code clean and trustworthy.
def parse_expense(row: dict[str, str]) -> dict[str, object]:
    """Parse a single CSV row into a structured expense record."""
    # WHY check required fields: A CSV row missing "amount" would cause
    # a confusing KeyError later.  Validating upfront gives a clear
    # error message: "Missing required field: amount".
    required = ["date", "category", "amount", "description"]
    for key in required:
        if key not in row or not row[key].strip():
            raise ValueError(f"Missing required field: {key}")

    # WHY float conversion: CSV values are always strings.  We need
    # numeric amounts for arithmetic (sum, average, comparison).
    amount = float(row["amount"])
    # WHY reject negatives: Expense tracking assumes all amounts are
    # money spent.  Negative amounts would reduce totals, which does
    # not make sense in this context.  Refunds should be handled
    # separately in a real accounting system.
    if amount < 0:
        raise ValueError(f"Negative amount not allowed: {amount}")

    return {
        "date": row["date"].strip(),
        # WHY .lower(): Normalising "Food", "food", "FOOD" to "food"
        # ensures all variants aggregate into one category.  Without
        # this, you would get three separate category entries.
        "category": row["category"].strip().lower(),
        # WHY round to 2: Money should always be displayed to exactly
        # 2 decimal places.  round() prevents floating-point noise.
        "amount": round(amount, 2),
        "description": row["description"].strip(),
    }


# WHY load_expenses: Separates file I/O from parsing.  parse_expense()
# can be tested with plain dicts; this function handles the CSV file.
def load_expenses(path: Path) -> list[dict[str, object]]:
    """Load expenses from a CSV file with headers."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    expenses = []
    # WHY newline="": Standard CSV reading practice to prevent
    # double-interpretation of line endings on Windows.
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append(parse_expense(row))
    return expenses


# WHY total_by_category: Knowing where money goes is the primary
# purpose of expense tracking.  Grouping by category answers "how
# much did I spend on food this month?" — the most common question.
def total_by_category(expenses: list[dict[str, object]]) -> dict[str, float]:
    """Sum expenses per category."""
    totals: dict[str, float] = {}
    for exp in expenses:
        cat = exp["category"]
        # WHY round after addition: Floating-point addition can
        # accumulate tiny errors (10.0 + 8.0 might give 18.000000001).
        # Rounding after each addition prevents this drift.
        totals[cat] = round(totals.get(cat, 0) + exp["amount"], 2)
    return totals


# WHY overall_stats: Summary statistics give a quick financial overview
# without needing to read every line item.  "Total $450, average $15,
# biggest expense $85" tells you a lot in one line.
def overall_stats(expenses: list[dict[str, object]]) -> dict[str, float]:
    """Compute total, average, min, and max across all expenses."""
    # WHY guard against empty: With no expenses, sum/min/max would
    # crash.  Returning zero values lets the caller display a clean
    # "no expenses" message.
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


# WHY top_expenses: Identifying big-ticket items helps prioritise
# budget cuts.  "Your 3 biggest expenses were..." is actionable
# information for financial planning.
def top_expenses(expenses: list[dict[str, object]], n: int = 3) -> list[dict[str, object]]:
    """Return the N largest expenses."""
    # WHY sorted with reverse=True: sorted() returns a new list
    # without modifying the original.  reverse=True puts the largest
    # amounts first.  [:n] takes only the top N.
    sorted_exp = sorted(expenses, key=lambda e: e["amount"], reverse=True)
    return sorted_exp[:n]


# WHY format_report: A human-readable report with categories, totals,
# and top expenses is the end product of expense tracking.
def format_report(
    category_totals: dict[str, float],
    stats: dict[str, float],
    top: list[dict[str, object]],
) -> str:
    """Format a human-readable expense report."""
    lines = ["=== Expense Report ===", ""]

    lines.append("  By Category:")
    # WHY sort by total descending: The largest spending category
    # appears first, drawing attention to where most money goes.
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


# WHY write_summary_csv: CSV output can be opened in spreadsheets
# (Excel, Google Sheets) for further analysis and charting.  This
# makes the tool useful beyond the terminal.
def write_summary_csv(
    path: Path,
    cat_totals: dict[str, float],
    stats: dict[str, float],
) -> None:
    """Write the expense summary as a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["Category", "Total"])
        for cat, total in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([cat, f"{total:.2f}"])

        writer.writerow([])
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total", f"{stats['total']:.2f}"])
        writer.writerow(["Average", f"{stats['average']:.2f}"])
        writer.writerow(["Min", f"{stats['min']:.2f}"])
        writer.writerow(["Max", f"{stats['max']:.2f}"])
        writer.writerow(["Count", stats["count"]])


# WHY parse_args: The --top flag lets users control how many top
# expenses to show, which is a practical customisation.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Basic Expense Tracker")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="CSV file with date,category,amount,description")
    parser.add_argument("--output", default="data/summary.csv")
    parser.add_argument("--top", type=int, default=3,
                        help="Number of top expenses to show")
    return parser.parse_args()


# WHY main: Full pipeline — load, aggregate, report, save.
def main() -> None:
    args = parse_args()

    expenses = load_expenses(Path(args.input))
    cat_totals = total_by_category(expenses)
    stats = overall_stats(expenses)
    top = top_expenses(expenses, args.top)

    print(format_report(cat_totals, stats, top))

    output_path = Path(args.output)
    write_summary_csv(output_path, cat_totals, stats)
    print(f"\n  Summary CSV saved to {output_path}")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Validate and reject negative amounts | Expenses are money spent; negative amounts would distort totals and averages | Allow negatives for refunds — makes sense in full accounting but adds complexity at Level 1 |
| Normalise categories to lowercase | Prevents "Food" and "food" from creating separate groups; all variants aggregate together | Case-sensitive categories — would require users to be consistent, which they never are |
| CSV output for the summary | Spreadsheet-compatible format that users can open in Excel for charts and further analysis | JSON output — machine-readable but not spreadsheet-friendly for non-developers |
| Separate `overall_stats()` from `total_by_category()` | Different concerns: one groups by category, the other computes aggregate statistics; separating makes each testable | One function that does both — harder to test and modify independently |

## Alternative approaches

### Approach B: Using `defaultdict` for category totals

```python
from collections import defaultdict

def total_by_category_defaultdict(expenses: list[dict]) -> dict[str, float]:
    """Sum expenses per category using defaultdict."""
    # WHY defaultdict: Automatically creates a new entry with default
    # value 0.0 when a key is accessed for the first time.  Eliminates
    # the need for .get(cat, 0).
    totals = defaultdict(float)
    for exp in expenses:
        totals[exp["category"]] += exp["amount"]
    # WHY dict(): Convert back to a regular dict for JSON serialisation
    # and consistent return types.
    return {k: round(v, 2) for k, v in totals.items()}
```

**Trade-off:** `defaultdict` eliminates the `.get(key, 0)` boilerplate and is cleaner for accumulation patterns. The manual approach teaches the underlying mechanism. Once you are comfortable with `defaultdict`, prefer it for any accumulation-into-dict pattern.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Negative amount like `-5.00` | `parse_expense()` raises `ValueError("Negative amount not allowed: -5.0")` | The explicit negativity check catches this at parse time |
| Missing category field (empty string) | `parse_expense()` raises `ValueError("Missing required field: category")` because `not row[key].strip()` catches empty strings | The required-field loop checks both missing keys and empty values |
| CSV with no data rows (headers only) | `load_expenses()` returns `[]`, `overall_stats([])` returns zero values, report shows nothing | The `if not expenses` guard in `overall_stats()` prevents ZeroDivisionError |
| Floating-point accumulation error | `round()` after each addition in `total_by_category()` prevents drift like `18.000000001` | Rounding is applied at every arithmetic step |

## Key takeaways

1. **Always validate financial data at the input boundary.** Catching negative amounts, missing fields, and non-numeric values in `parse_expense()` means every downstream function can trust the data. This "validate early, trust later" pattern is how real financial systems work.
2. **Category normalisation is essential for aggregation.** Without `.lower().strip()`, you would get separate totals for "Food", "food", "FOOD", and " Food ". This normalisation step applies to any grouping operation — tags, statuses, labels, etc.
3. **This project is a simplified version of real personal finance apps.** Mint, YNAB, and bank statements all parse transactions, categorise them, and compute spending summaries. The same CSV-parse-aggregate-report pipeline scales from a script to a full application with a database and web interface.
