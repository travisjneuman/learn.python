"""
Project 02 — Filtering & Grouping

This script demonstrates how to filter rows with boolean indexing,
select data with .loc[], group rows with groupby(), compute aggregations,
and count values — the core operations of data analysis.

Data file: data/students.csv (30 rows with name, subject, grade, age)
"""

import pandas as pd


def load_data(filepath):
    """Load CSV and return a DataFrame."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows from {filepath}")
    return df


def filter_high_grades(df, threshold=80):
    """
    Filter the DataFrame to only include students above a threshold.

    Boolean indexing works like this:
    1. df["grade"] > 80 creates a Series of True/False values (one per row).
    2. df[that_series] keeps only the rows where the value is True.

    This is the pandas equivalent of a WHERE clause in SQL.
    """
    print(f"\n=== Students with grade > {threshold} ===")

    # This creates a boolean Series: True where grade > threshold, False elsewhere.
    mask = df["grade"] > threshold

    # Passing that mask into df[...] keeps only the True rows.
    high_performers = df[mask]

    print(f"Found {len(high_performers)} students with grade above {threshold}")
    print(high_performers)
    return high_performers


def filter_with_loc(df):
    """
    Use .loc[] for label-based filtering.

    .loc[] is more explicit than plain bracket indexing. It accepts
    a boolean mask for rows and column names for columns. This makes
    your intent clearer: "give me these rows and these columns."
    """
    print("\n=== Using .loc[] to filter ===")

    # .loc[row_selector, column_selector]
    # Row selector: boolean mask (which rows to keep)
    # Column selector: list of column names (which columns to show)
    science_students = df.loc[df["subject"] == "Science", ["name", "grade"]]

    print("Science students only:")
    print(science_students)
    return science_students


def count_subjects(df):
    """
    Count how many students are in each subject.

    value_counts() tallies the unique values in a column and sorts them
    by frequency. It is the quickest way to see the distribution of a
    categorical variable.
    """
    print("\n=== Subject counts (value_counts) ===")
    counts = df["subject"].value_counts()
    print(counts)
    return counts


def group_by_subject_mean(df):
    """
    Group rows by subject and calculate the mean grade.

    groupby("subject") splits the DataFrame into groups — one group per
    unique subject. Then ["grade"].mean() computes the average grade
    within each group. This is equivalent to:
        SELECT subject, AVG(grade) FROM students GROUP BY subject
    """
    print("\n=== Group by subject — mean grade ===")
    means = df.groupby("subject")["grade"].mean()
    print(means)
    return means


def group_by_subject_multi_agg(df):
    """
    Apply multiple aggregation functions at once with agg().

    agg() lets you pass a list of function names as strings. pandas
    applies each function to every group and returns a table with one
    column per function. This is more efficient than calling mean(),
    max(), and min() separately.
    """
    print("\n=== Group by subject — multiple aggregations ===")

    # agg() accepts a list of aggregation function names.
    # Each one becomes a column in the result.
    result = df.groupby("subject")["grade"].agg(["mean", "max", "min"])

    # Round the mean for cleaner display.
    result["mean"] = result["mean"].round(2)

    print(result)
    return result


def top_students_per_subject(df):
    """
    Find the highest-scoring student in each subject.

    This combines groupby with idxmax() — a method that returns the
    index (row number) of the maximum value in each group. Then we
    use .loc[] to fetch those rows from the original DataFrame.
    """
    print("\n=== Top students per subject ===")

    # For each subject, find the row index where grade is highest.
    top_indices = df.groupby("subject")["grade"].idxmax()

    # Use those indices to pull the full rows from the original DataFrame.
    top_students = df.loc[top_indices]

    print(top_students[["name", "subject", "grade"]])
    return top_students


def main():
    print("=== Loading student data ===")
    df = load_data("data/students.csv")

    # Step 1: Filter rows using boolean indexing.
    filter_high_grades(df, threshold=80)

    # Step 2: Use .loc[] for more explicit selection.
    filter_with_loc(df)

    # Step 3: Count values in a categorical column.
    count_subjects(df)

    # Step 4: Group by a column and compute the mean.
    group_by_subject_mean(df)

    # Step 5: Apply multiple aggregations at once.
    group_by_subject_multi_agg(df)

    # Step 6: Combine grouping with row lookup.
    top_students_per_subject(df)

    print("\nDone.")


if __name__ == "__main__":
    main()
