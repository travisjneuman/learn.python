"""
Project 01 — Pandas Basics

This script loads a CSV file of student grades into a pandas DataFrame
and explores the data using built-in methods: head(), shape, dtypes,
info(), describe(), column selection, and sorting.

Data file: data/students.csv (30 rows with name, subject, grade, age)
"""

# pandas is the core library for data analysis in Python.
# The convention is to import it as "pd" so you type less.
# You installed it with: pip install pandas
import pandas as pd


def load_data(filepath):
    """
    Load a CSV file into a pandas DataFrame.

    pd.read_csv() reads a comma-separated file and returns a DataFrame —
    a table-like structure with labeled columns and numbered rows.
    Think of it as a spreadsheet you can manipulate with code.
    """
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns from {filepath}")
    return df


def explore_head(df):
    """
    Show the first few rows of the DataFrame.

    head() returns the first 5 rows by default. This is the fastest way
    to see what your data looks like after loading it.
    """
    print("\n=== First 5 rows (head) ===")
    print(df.head())


def explore_shape(df):
    """
    Show the dimensions of the DataFrame.

    shape is a tuple (rows, columns). It tells you how big your data set
    is without printing all the data.
    """
    rows, cols = df.shape
    print(f"\n=== Shape ===")
    print(f"Rows: {rows}, Columns: {cols}")


def explore_dtypes(df):
    """
    Show the data type of each column.

    dtypes tells you whether each column holds numbers (int64, float64),
    text (object), dates, or other types. This matters because you cannot
    do math on text columns.

    "object" in pandas usually means the column contains strings.
    """
    print("\n=== Column types (dtypes) ===")
    print(df.dtypes)


def explore_info(df):
    """
    Show a concise summary of the DataFrame.

    info() prints the column names, non-null counts, and data types
    all in one view. It is especially useful for spotting missing values —
    if a column has fewer non-null entries than total rows, some values
    are missing.
    """
    print("\n=== Info ===")
    df.info()


def explore_describe(df):
    """
    Show summary statistics for numeric columns.

    describe() calculates count, mean, std, min, 25%, 50% (median),
    75%, and max for every numeric column. This gives you a quick
    sense of the distribution — are grades clustered around 80?
    Is the youngest student 14 or 18?
    """
    print("\n=== Summary statistics (describe) ===")
    print(df.describe())


def select_columns(df):
    """
    Select specific columns from the DataFrame.

    df["column_name"] returns a single column as a Series.
    df[["col1", "col2"]] returns multiple columns as a new DataFrame.
    Notice the double brackets — the inner list tells pandas which
    columns you want.
    """
    print("\n=== Selecting just name and grade columns ===")
    # Double brackets: pass a list of column names to get a DataFrame back.
    subset = df[["name", "grade"]]
    print("(first 5 rows)")
    print(subset.head())


def sort_by_grade(df):
    """
    Sort the DataFrame by the grade column, highest first.

    sort_values() returns a new DataFrame with rows reordered.
    ascending=False puts the highest values at the top.
    The original DataFrame is not changed.
    """
    print("\n=== Sorted by grade (highest first) ===")
    sorted_df = df.sort_values("grade", ascending=False)
    print("(first 10 rows)")
    print(sorted_df.head(10))


def main():
    print("=== Loading student data ===")

    # Step 1: Load the CSV into a DataFrame.
    # The file path is relative to where you run the script from.
    df = load_data("data/students.csv")

    # Step 2: Explore the data using built-in methods.
    # These are the first things you should do with any new data set.
    explore_head(df)
    explore_shape(df)
    explore_dtypes(df)
    explore_info(df)
    explore_describe(df)

    # Step 3: Select specific columns.
    select_columns(df)

    # Step 4: Sort the data.
    sort_by_grade(df)

    print("\nDone.")


# This pattern means: only run main() when this file is executed directly.
# If someone imports this file, main() will NOT run automatically.
if __name__ == "__main__":
    main()
