"""
Project 05 — Analysis Report

This script runs a complete data analysis pipeline on sales transaction data:
load, clean, analyze (monthly revenue, top products, customer segments),
visualize, and export a summary report.

Data file: data/transactions.csv (200 rows with date, product, quantity,
           price, customer_id)
"""

# Set matplotlib backend before importing pyplot.
# "Agg" renders to files without needing a display window.
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def load_data(filepath):
    """
    Load the transaction CSV.

    This is always the first step. We check the row count to make sure
    the file loaded correctly and nothing got cut off.
    """
    print("=== Step 1: Load transaction data ===")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} transactions from {filepath}")
    return df


def clean_and_prepare(df):
    """
    Parse dates and add calculated columns.

    The date column comes in as strings like "2024-01-15". We convert it
    to proper datetime objects so pandas can do date arithmetic — grouping
    by month, calculating time ranges, etc.

    We also add a revenue column: quantity * price. This is the total
    dollar amount for each transaction.
    """
    print("\n=== Step 2: Clean and prepare ===")

    # Convert the date column from strings to datetime objects.
    # pd.to_datetime() understands many date formats automatically.
    df["date"] = pd.to_datetime(df["date"])

    date_min = df["date"].min().strftime("%Y-%m-%d")
    date_max = df["date"].max().strftime("%Y-%m-%d")
    print(f"Parsed dates. Date range: {date_min} to {date_max}")

    # Add a revenue column: how much money each transaction brought in.
    df["revenue"] = df["quantity"] * df["price"]
    print("Added revenue column (quantity * price)")

    return df


def monthly_revenue(df):
    """
    Calculate total revenue per month.

    dt.to_period("M") converts each date to a monthly period like "2024-01".
    Then we group by that period and sum the revenue. This gives us a
    time series of monthly revenue.
    """
    print("\n=== Step 3: Monthly revenue ===")

    # Create a month column from the date.
    # to_period("M") turns "2024-01-15" into "2024-01".
    df["month"] = df["date"].dt.to_period("M")

    # Group by month and sum the revenue.
    monthly = df.groupby("month")["revenue"].sum()

    # Display each month's revenue.
    for month, rev in monthly.items():
        print(f"{month}    ${rev:,.2f}")

    total = monthly.sum()
    print(f"Total revenue: ${total:,.2f}")

    return monthly


def top_products(df):
    """
    Rank products by total revenue.

    Group by product name, sum the revenue, and sort descending.
    This tells the business which products generate the most money.
    """
    print("\n=== Step 4: Top products by revenue ===")

    product_revenue = df.groupby("product")["revenue"].sum().sort_values(ascending=False)

    for product, rev in product_revenue.items():
        print(f"{product:<25} ${rev:,.2f}")

    return product_revenue


def customer_segments(df):
    """
    Segment customers by purchase frequency.

    Count how many orders each customer made, then group them:
    - One-time buyer: 1 order
    - Occasional: 2-3 orders
    - Regular: 4+ orders

    This kind of segmentation helps businesses understand their
    customer base and tailor marketing strategies.
    """
    print("\n=== Step 5: Customer segments ===")

    # Count orders per customer.
    orders_per_customer = df.groupby("customer_id").size()

    # Define segments based on order count.
    def classify(order_count):
        if order_count == 1:
            return "One-time buyer"
        elif order_count <= 3:
            return "Occasional (2-3)"
        else:
            return "Regular (4+)"

    # Apply the classification to each customer.
    customer_labels = orders_per_customer.apply(classify)

    # Summarize each segment.
    segments = []
    for segment_name in ["One-time buyer", "Occasional (2-3)", "Regular (4+)"]:
        # Get customer IDs in this segment.
        customers_in_segment = customer_labels[customer_labels == segment_name].index
        count = len(customers_in_segment)

        # Calculate average orders for customers in this segment.
        avg_orders = orders_per_customer[customers_in_segment].mean()

        segments.append({
            "segment": segment_name,
            "customers": count,
            "avg_orders": avg_orders
        })

    # Print as a formatted table.
    print(f"{'Segment':<22} {'Customers':>10} {'Avg Orders':>12}")
    for seg in segments:
        print(f"{seg['segment']:<22} {seg['customers']:>10} {seg['avg_orders']:>12.1f}")

    return segments


def create_summary_chart(monthly, product_revenue):
    """
    Create a two-panel summary chart.

    Left panel: monthly revenue trend (bar chart).
    Right panel: product revenue ranking (horizontal bar chart).
    """
    print("\n=== Step 6: Save visualization ===")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left panel: Monthly revenue bar chart.
    # Convert period index to strings for matplotlib compatibility.
    months = [str(m) for m in monthly.index]
    axes[0].bar(months, monthly.values, color="#2980b9", edgecolor="white")
    axes[0].set_title("Monthly Revenue", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Month")
    axes[0].set_ylabel("Revenue ($)")
    axes[0].tick_params(axis="x", rotation=45)

    # Add value labels on top of each bar.
    for i, val in enumerate(monthly.values):
        axes[0].text(i, val + 10, f"${val:,.0f}", ha="center", fontsize=8)

    # Right panel: Product revenue horizontal bar chart.
    # Horizontal bars work better for category labels that might be long.
    axes[1].barh(product_revenue.index, product_revenue.values, color="#27ae60", edgecolor="white")
    axes[1].set_title("Revenue by Product", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Revenue ($)")

    # Invert y-axis so the top product appears at the top.
    axes[1].invert_yaxis()

    fig.suptitle("Sales Analysis Summary", fontsize=15, fontweight="bold")
    plt.tight_layout()

    output_path = "data/summary_chart.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved summary chart to {output_path}")


def export_report(df, monthly, product_revenue, segments):
    """
    Write a plain-text summary report to a file.

    This report is meant to be readable by anyone — no code knowledge
    required. In a real job, this might be emailed to a manager or
    attached to a ticket.
    """
    print("\n=== Step 7: Export report ===")

    lines = []
    lines.append("=" * 60)
    lines.append("SALES ANALYSIS REPORT")
    lines.append("=" * 60)
    lines.append("")

    # Date range.
    date_min = df["date"].min().strftime("%Y-%m-%d")
    date_max = df["date"].max().strftime("%Y-%m-%d")
    lines.append(f"Period: {date_min} to {date_max}")
    lines.append(f"Total transactions: {len(df)}")
    lines.append(f"Total revenue: ${df['revenue'].sum():,.2f}")
    lines.append(f"Average transaction value: ${df['revenue'].mean():,.2f}")
    lines.append("")

    # Monthly revenue.
    lines.append("-" * 40)
    lines.append("MONTHLY REVENUE")
    lines.append("-" * 40)
    for month, rev in monthly.items():
        lines.append(f"  {month}:  ${rev:,.2f}")
    lines.append("")

    # Top products.
    lines.append("-" * 40)
    lines.append("REVENUE BY PRODUCT")
    lines.append("-" * 40)
    for product, rev in product_revenue.items():
        pct = (rev / df["revenue"].sum()) * 100
        lines.append(f"  {product:<25} ${rev:,.2f}  ({pct:.1f}%)")
    lines.append("")

    # Customer segments.
    lines.append("-" * 40)
    lines.append("CUSTOMER SEGMENTS")
    lines.append("-" * 40)
    for seg in segments:
        lines.append(f"  {seg['segment']:<22} {seg['customers']:>3} customers  (avg {seg['avg_orders']:.1f} orders)")
    lines.append("")

    lines.append("=" * 60)
    lines.append("End of report.")
    lines.append("=" * 60)

    # Write to file.
    report_text = "\n".join(lines)
    output_path = "data/report.txt"
    with open(output_path, "w") as f:
        f.write(report_text)

    print(f"Saved report to {output_path}")


def main():
    # Step 1: Load raw data.
    df = load_data("data/transactions.csv")

    # Step 2: Clean and add calculated columns.
    df = clean_and_prepare(df)

    # Step 3: Analyze monthly revenue.
    monthly = monthly_revenue(df)

    # Step 4: Rank products by revenue.
    product_rev = top_products(df)

    # Step 5: Segment customers by purchase frequency.
    segments = customer_segments(df)

    # Step 6: Create a summary visualization.
    create_summary_chart(monthly, product_rev)

    # Step 7: Export a plain-text report.
    export_report(df, monthly, product_rev, segments)

    print("\nDone. Analysis complete.")


if __name__ == "__main__":
    main()
