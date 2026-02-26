"""Monthly sales report generator.

Reads a CSV of daily sales, processes it, and writes a formatted report.
This entire pipeline lives in one massive function. Your job is to split it up.
"""

import csv
import os


def generate_report(input_csv, output_txt, year, month):
    """Generate a monthly sales report. Does everything in one function."""
    # Read CSV
    rows = []
    with open(input_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    # Filter to target month
    filtered = []
    for row in rows:
        parts = row["date"].split("-")
        y = int(parts[0])
        m = int(parts[1])
        if y == year and m == month:
            filtered.append(row)

    if len(filtered) == 0:
        with open(output_txt, "w") as f:
            f.write(f"No sales data for {year}-{month:02d}\n")
        return {"total": 0, "categories": {}, "top_product": None, "daily_average": 0}

    # Calculate totals by category
    cat_totals = {}
    product_totals = {}
    daily_totals = {}
    grand_total = 0

    for row in filtered:
        cat = row["category"].strip()
        product = row["product"].strip()
        date = row["date"]
        amount = int(row["quantity"]) * float(row["unit_price"])

        if cat not in cat_totals:
            cat_totals[cat] = 0
        cat_totals[cat] += amount

        if product not in product_totals:
            product_totals[product] = 0
        product_totals[product] += amount

        if date not in daily_totals:
            daily_totals[date] = 0
        daily_totals[date] += amount

        grand_total += amount

    # Find top product
    top_product = None
    top_amount = 0
    for product, amount in product_totals.items():
        if amount > top_amount:
            top_amount = amount
            top_product = product

    # Calculate daily average
    num_days = len(daily_totals)
    daily_avg = grand_total / num_days if num_days > 0 else 0

    # Sort categories by revenue descending
    sorted_cats = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)

    # Format report
    lines = []
    lines.append("=" * 50)
    lines.append(f"  MONTHLY SALES REPORT — {year}-{month:02d}")
    lines.append("=" * 50)
    lines.append("")
    lines.append(f"  Total Revenue:    ${grand_total:,.2f}")
    lines.append(f"  Daily Average:    ${daily_avg:,.2f}")
    lines.append(f"  Top Product:      {top_product} (${top_amount:,.2f})")
    lines.append(f"  Active Days:      {num_days}")
    lines.append("")
    lines.append("-" * 50)
    lines.append("  REVENUE BY CATEGORY")
    lines.append("-" * 50)
    for cat, total in sorted_cats:
        pct = (total / grand_total * 100) if grand_total > 0 else 0
        bar = "#" * int(pct / 2)
        lines.append(f"  {cat:<20s} ${total:>10,.2f}  ({pct:5.1f}%)  {bar}")
    lines.append("")
    lines.append("-" * 50)
    lines.append("  TOP 5 PRODUCTS")
    lines.append("-" * 50)
    sorted_products = sorted(product_totals.items(), key=lambda x: x[1], reverse=True)
    for i, (product, amount) in enumerate(sorted_products[:5]):
        lines.append(f"  {i + 1}. {product:<20s} ${amount:>10,.2f}")
    lines.append("")
    lines.append("=" * 50)

    # Write report
    with open(output_txt, "w") as f:
        f.write("\n".join(lines))

    return {
        "total": round(grand_total, 2),
        "categories": {cat: round(total, 2) for cat, total in cat_totals.items()},
        "top_product": top_product,
        "daily_average": round(daily_avg, 2),
    }
