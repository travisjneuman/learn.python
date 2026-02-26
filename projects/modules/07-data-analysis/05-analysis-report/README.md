# Module 07 / Project 05 — Analysis Report

[README](../../../../README.md) · [Module Index](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- Complete analysis pipeline: load, clean, analyze, visualize, export
- Date parsing and monthly grouping with `pd.to_datetime()` and `dt.to_period()`
- Revenue calculations and ranking
- Customer segmentation by purchase frequency
- Exporting a text summary report

## Why this project exists

This project ties together everything you learned in Projects 01 through 04 into a single realistic workflow. In a real job, you would receive a CSV of transaction data and be asked: "What is our monthly revenue trend? Which products sell best? Who are our top customers?" This project teaches you to answer those questions end to end — from raw file to finished report and chart.

## Run

```bash
cd projects/modules/07-data-analysis/05-analysis-report
python project.py
```

## Expected output

```text
=== Step 1: Load transaction data ===
Loaded 200 transactions from data/transactions.csv

=== Step 2: Clean and prepare ===
Parsed dates. Date range: 2024-01-03 to 2024-06-30
Added revenue column (quantity * price)

=== Step 3: Monthly revenue ===
month
2024-01    $849.38
2024-02    $812.42
2024-03    $802.44
2024-04    $786.48
2024-05    $802.44
2024-06    $816.40
Total revenue: $4,869.56

=== Step 4: Top products by revenue ===
product
Bluetooth Speaker    $2,049.59
Wireless Mouse       $1,409.53
Desk Lamp            $1,189.66
Notebook Set           $363.72
...

=== Step 5: Customer segments ===
Segment           Customers  Avg Orders
One-time buyer          25        1.0
Occasional (2-3)        20        2.3
Regular (4+)             5        5.2

=== Step 6: Save visualization ===
Saved summary chart to data/summary_chart.png

=== Step 7: Export report ===
Saved report to data/report.txt

Done. Analysis complete.
```

The exact numbers depend on the transaction data. Open `data/report.txt` for the full summary and `data/summary_chart.png` for the visualization.

## Alter it

1. Add a "day of week" analysis: which weekday has the most sales? (Hint: `df["date"].dt.day_name()`.)
2. Calculate the average order value (total revenue / number of orders) per month.
3. Add a "growth rate" column showing the percentage change in revenue from month to month. (Hint: `pct_change()`.)
4. Create a pie chart showing revenue share by product.

## Break it

1. Change the date column name in the CSV. What error do you get during parsing?
2. Remove the `pd.to_datetime()` call and try to group by month. What happens?
3. Try to save the report to a directory that does not exist. Read the error.

## Fix it

1. Check that the expected columns exist before processing: `if "date" in df.columns`.
2. Always convert date strings to datetime objects before doing date arithmetic.
3. Use `os.makedirs()` to create the output directory if it does not exist.

## Explain it

1. Why do you need `pd.to_datetime()` when pandas already loaded the date column?
2. What does `dt.to_period("M")` do? How is it different from `dt.month`?
3. What is a customer segment? Why would a business care about segmenting customers?
4. Why is it better to save the report as a text file than just print it to the console?

## Mastery check

You can move on when you can:

- Build a complete analysis pipeline from raw CSV to finished report.
- Parse dates and group data by month, week, or day.
- Calculate revenue, rank products, and segment customers.
- Create a summary visualization and save it to a file.
- Export a text report that a non-technical person could read and understand.

---

## Related Concepts

- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [Types and Conversions](../../../../concepts/types-and-conversions.md)
- [Virtual Environments](../../../../concepts/virtual-environments.md)
- [Quiz: Collections Explained](../../../../concepts/quizzes/collections-explained-quiz.py)

## Next

You have completed Module 07. Return to the [Module Index](../README.md) to choose your next module.
