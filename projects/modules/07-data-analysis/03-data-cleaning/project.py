"""
Project 03 — Data Cleaning

This script loads a messy CSV file with missing values, wrong data types,
and duplicate rows. It cleans the data step by step: detect problems,
fix types, handle missing values, remove duplicates, merge with a
reference table, and save the result.

Data files:
  data/messy_sales.csv  — 50 rows with intentional problems
  data/products.csv     — 10 rows product lookup table
"""

import pandas as pd


def load_messy_data(filepath):
    """
    Load a CSV that we know has problems.

    Even messy data loads fine — pandas just fills missing cells with NaN
    (Not a Number) and guesses at column types. The problems only become
    visible when you inspect the data.
    """
    print("=== Step 1: Load messy data ===")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows from {filepath}")
    return df


def inspect_data(df):
    """
    Check for missing values and incorrect data types.

    isna() returns True for every cell that is NaN (missing).
    isna().sum() counts how many missing values each column has.
    dtypes shows the type pandas guessed for each column.
    """
    print("\n=== Step 2: Inspect the mess ===")

    # Count missing values per column.
    # If a column has 0 missing values, it is complete.
    print("Missing values per column:")
    print(df.isna().sum())

    # Check data types.
    # "object" means pandas treated the column as strings.
    # If quantity shows as "object" instead of "int64", that means
    # some values in the column are not valid numbers.
    print("\nData types:")
    print(df.dtypes)

    return df


def fix_data_types(df):
    """
    Convert columns to their correct types.

    The quantity column contains some non-numeric values like "five" and "three".
    pd.to_numeric() with errors="coerce" converts valid numbers and turns
    invalid ones into NaN. This is safer than astype(int), which would crash.
    """
    print("\n=== Step 3: Fix data types ===")

    # Count how many values will fail conversion.
    # to_numeric with errors="coerce" silently turns bad values into NaN.
    before_nan = df["quantity"].isna().sum()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    after_nan = df["quantity"].isna().sum()
    new_nans = after_nan - before_nan

    print(f"Converted quantity: {new_nans} values could not be converted (set to NaN)")

    return df


def handle_missing_values(df):
    """
    Deal with missing values: drop some rows, fill others.

    Strategy:
    - quantity and price: these are essential for calculations. Drop rows
      where either is missing — we cannot compute totals without them.
    - region: this is useful but not critical. Fill missing values with
      "Unknown" so we keep the row but mark it as incomplete.
    - date: drop rows with missing dates since we need them for time analysis.

    There is no single right answer for missing values. The decision depends
    on what you plan to do with the data and how much data you can afford to lose.
    """
    print("\n=== Step 4: Handle missing values ===")
    print(f"Before: {len(df)} rows")

    # Drop rows where quantity or price is missing.
    # subset= tells dropna to only look at these columns.
    df = df.dropna(subset=["quantity", "price", "date"])
    print(f"After dropping rows with missing quantity, price, or date: {len(df)} rows")

    # Fill missing region with "Unknown" instead of dropping.
    # fillna() replaces NaN with the value you provide.
    missing_regions = df["region"].isna().sum()
    df["region"] = df["region"].fillna("Unknown")
    print(f"Filled {missing_regions} missing region values with \"Unknown\"")

    return df


def remove_duplicates(df):
    """
    Find and remove duplicate rows.

    duplicated() returns True for rows that are exact copies of an earlier row.
    drop_duplicates() removes them, keeping the first occurrence.

    Duplicates can happen when data is exported multiple times, when systems
    retry failed writes, or when merging data from multiple sources.
    """
    print("\n=== Step 5: Remove duplicates ===")

    # Count duplicates before removing.
    dup_count = df.duplicated().sum()
    print(f"Found {dup_count} duplicate rows")

    # Remove duplicates, keeping the first occurrence of each.
    df = df.drop_duplicates()
    print(f"After removing duplicates: {len(df)} rows")

    return df


def merge_with_products(df, products_filepath):
    """
    Merge the sales data with a product reference table.

    pd.merge() combines two DataFrames based on a shared column, like a
    SQL JOIN. Here we join on product_id to add the product_name and
    category columns to our sales data.

    how="left" means: keep all rows from the sales DataFrame, even if
    a product_id does not match anything in the products table.
    """
    print("\n=== Step 6: Merge with product names ===")

    products = pd.read_csv(products_filepath)

    # Merge on the product_id column that both DataFrames share.
    # how="left" keeps all sales rows. If a product_id has no match,
    # the product_name and category columns will be NaN.
    merged = pd.merge(df, products, on="product_id", how="left")

    print(f"After merge: {len(merged)} rows, {len(merged.columns)} columns")
    print(f"New columns: {', '.join(products.columns[1:])}")

    return merged


def save_cleaned_data(df, output_filepath):
    """
    Save the cleaned DataFrame to a new CSV file.

    to_csv() writes a DataFrame back to a CSV file. index=False prevents
    pandas from adding an extra column with row numbers, which you usually
    do not want in your output file.
    """
    print("\n=== Step 7: Save cleaned data ===")
    df.to_csv(output_filepath, index=False)
    print(f"Saved cleaned data to {output_filepath}")


def main():
    # Step 1: Load the messy data.
    df = load_messy_data("data/messy_sales.csv")

    # Step 2: Inspect what is wrong.
    df = inspect_data(df)

    # Step 3: Fix data types (quantity has non-numeric values).
    df = fix_data_types(df)

    # Step 4: Handle missing values (drop some, fill others).
    df = handle_missing_values(df)

    # Step 5: Remove duplicate rows.
    df = remove_duplicates(df)

    # Step 6: Merge with product reference data.
    df = merge_with_products(df, "data/products.csv")

    # Step 7: Save the cleaned result.
    save_cleaned_data(df, "data/cleaned_sales.csv")

    # Final summary.
    print(f"\nDone. Cleaned 51 messy rows down to {len(df)} clean rows.")


if __name__ == "__main__":
    main()
