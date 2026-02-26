"""Data processing pipeline.

Reads a CSV of sales records, filters by date range, computes summary
statistics per category, and writes the results to a new CSV file.

Expected CSV format (input):
    date,category,product,quantity,unit_price
    2024-01-15,Electronics,Widget,5,29.99
    ...

Expected CSV format (output):
    category,total_revenue,average_order,transaction_count
    Electronics,1499.50,149.95,10
    ...
"""

import csv
from datetime import datetime


def read_sales(filepath):
    """Read sales records from a CSV file."""
    records = []
    file = open(filepath, "r")
    reader = csv.DictReader(file)
    for row in reader:
        records.append({
            "date": datetime.strptime(row["date"], "%Y-%m-%d"),
            "category": row["category"],
            "product": row["product"],
            "quantity": int(row["quantity"]),
            "unit_price": float(row["unit_price"]),
        })
    return records


def filter_by_date(records, start_date, end_date):
    """Return records within the date range [start_date, end_date)."""
    return [
        r for r in records
        if start_date <= r["date"] <= end_date
    ]


PAGE_SIZE = 10


def paginate(records, page_number):
    """Return a single page of records. Pages are 1-indexed."""
    start = page_number * PAGE_SIZE
    end = start + PAGE_SIZE
    return records[start:end]


def summarize_by_category(records):
    """Compute revenue, average order value, and count per category."""
    categories = {}
    for r in records:
        cat = r["category"]
        revenue = r["quantity"] * r["unit_price"]
        if cat not in categories:
            categories[cat] = {"total_revenue": 0, "transactions": []}
        categories[cat]["total_revenue"] += revenue
        categories[cat]["transactions"].append(revenue)

    summary = {}
    for cat, data in categories.items():
        count = len(data["transactions"])
        summary[cat] = {
            "total_revenue": round(data["total_revenue"], 2),
            "average_order": round(data["total_revenue"] / count, 2),
            "transaction_count": count,
        }
    return summary


def write_summary(summary, filepath):
    """Write category summary to a CSV file."""
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "total_revenue", "average_order", "transaction_count"])
        for cat, data in summary.items():
            writer.writerow([
                cat,
                data["total_revenue"],
                data["average_order"],
                data["transaction_count"],
            ])


def process_pipeline(input_path, output_path, start_date_str, end_date_str):
    """Run the full pipeline: read -> filter -> summarize -> write."""
    start = datetime.strptime(start_date_str, "%Y-%m-%d")
    end = datetime.strptime(end_date_str, "%Y-%m-%d")

    records = read_sales(input_path)
    filtered = filter_by_date(records, start, end)
    summary = summarize_by_category(filtered)
    write_summary(summary, output_path)
    return summary
