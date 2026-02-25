# Module 07 / Project 03 — Data Cleaning

[README](../../../../README.md) · [Module Index](../README.md)

## Focus

- Detecting missing values with `isna()` and `isna().sum()`
- Handling missing values with `fillna()` and `dropna()`
- Converting data types with `astype()` and `pd.to_numeric()`
- Finding and removing duplicates with `duplicated()` and `drop_duplicates()`
- Merging DataFrames with `pd.merge()`

## Why this project exists

Real-world data is messy. CSV files from production systems have missing values, wrong data types, duplicate rows, and inconsistencies. Before you can analyze data, you must clean it. This project walks you through a realistic cleaning workflow: detect problems, fix them step by step, merge in reference data, and save the cleaned result. These skills are used in every data analysis job.

## Run

```bash
cd projects/modules/07-data-analysis/03-data-cleaning
python project.py
```

## Expected output

```text
=== Step 1: Load messy data ===
Loaded 51 rows from data/messy_sales.csv

=== Step 2: Inspect the mess ===
Missing values per column:
order_id      0
product_id    0
quantity      4
price         4
date          2
region        3
dtype: int64

Data types:
order_id       int64
product_id    object
quantity      object   <-- should be numeric!
price        float64
date          object
region        object
dtype: object

=== Step 3: Fix data types ===
Converted quantity: 2 values could not be converted (set to NaN)

=== Step 4: Handle missing values ===
Before: 51 rows
After dropping rows with missing quantity or price: 43 rows
Filled 2 missing region values with "Unknown"

=== Step 5: Remove duplicates ===
Found 1 duplicate rows
After removing duplicates: 42 rows

=== Step 6: Merge with product names ===
After merge: 42 rows, 8 columns
New columns: product_name, category

=== Step 7: Save cleaned data ===
Saved cleaned data to data/cleaned_sales.csv

Done. Cleaned 51 messy rows down to 42 clean rows.
```

## Alter it

1. Instead of dropping rows with missing `quantity`, fill them with the median quantity. How does the row count change?
2. Fill missing `region` values with the most common region instead of "Unknown". (Hint: `df["region"].mode()[0]`.)
3. After merging, group by `category` and count how many orders each category has.
4. Add a new calculated column: `total = quantity * price`.

## Break it

1. Try `df["quantity"].astype(int)` before cleaning the non-numeric values. What error do you get?
2. Merge on a column name that does not exist in one of the DataFrames. Read the error.
3. Call `dropna()` with no arguments. How many rows survive? Why is this usually too aggressive?

## Fix it

1. Use `pd.to_numeric(df["quantity"], errors="coerce")` instead of `astype(int)`. The `errors="coerce"` flag turns unparseable values into NaN instead of crashing.
2. Check that the merge column exists in both DataFrames before merging.
3. Use `dropna(subset=["quantity", "price"])` to only drop rows where specific columns are missing, not every column.

## Explain it

1. What is the difference between `fillna()` and `dropna()`? When would you use each?
2. What does `errors="coerce"` do in `pd.to_numeric()`? Why is it useful for messy data?
3. What is a merge/join? How is `pd.merge()` similar to a SQL JOIN?
4. Why should you check for duplicates before analyzing data?

## Mastery check

You can move on when you can:

- Detect missing values in any column and decide whether to fill or drop them.
- Convert a column from string to numeric, handling unparseable values gracefully.
- Find and remove duplicate rows.
- Merge two DataFrames on a shared column.
- Explain the cleaning decisions you made and why.

---

## Related Concepts

- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Types and Conversions](../../../../concepts/types-and-conversions.md)
- [Quiz: Collections Explained](../../../../concepts/quizzes/collections-explained-quiz.py)

## Next

[Project 04 — Visualization](../04-visualization/)
