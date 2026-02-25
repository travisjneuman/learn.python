"""
Tests for Project 01 — Pandas Basics

These tests verify the data exploration functions from project.py using
small inline DataFrames instead of loading CSV files. This makes the tests
self-contained and fast — they do not depend on external data files.

Why inline DataFrames?
    In real data analysis, your data lives in files or databases. But in tests,
    you want full control over the input so you can predict the output. Creating
    small DataFrames directly in Python gives you that control.

Run with: pytest tests/test_project.py -v
"""

import pandas as pd
import pytest

from project import (
    load_data,
    explore_shape,
    select_columns,
    sort_by_grade,
)


# ── Helper: create a small test DataFrame ──────────────────────────────
# This fixture provides a consistent DataFrame for all tests in this file.
# Using a fixture avoids repeating the same setup code in every test.

@pytest.fixture
def sample_df():
    """Create a small DataFrame that mimics the students.csv structure."""
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "subject": ["Math", "Science", "Math", "English"],
        "grade": [92, 78, 85, 95],
        "age": [16, 17, 16, 18],
    })


# ── Test: load_data reads a CSV correctly ──────────────────────────────
# We test load_data by writing a temporary CSV and loading it.
# tmp_path is a built-in pytest fixture that gives us a temporary directory.

def test_load_data_returns_dataframe(tmp_path):
    """load_data should return a DataFrame with the correct number of rows.

    WHY: This verifies that pd.read_csv is called correctly and the function
    returns a proper DataFrame. We use a temporary file so the test does not
    depend on data/students.csv existing.
    """
    # Create a small CSV file in the temporary directory.
    csv_path = tmp_path / "test_students.csv"
    csv_path.write_text("name,subject,grade,age\nAlice,Math,92,16\nBob,Science,78,17\n")

    df = load_data(str(csv_path))

    # Check that we got a DataFrame back with the right shape.
    assert isinstance(df, pd.DataFrame), "load_data should return a DataFrame"
    assert len(df) == 2, "Should have loaded 2 rows from the CSV"
    assert list(df.columns) == ["name", "subject", "grade", "age"]


# ── Test: explore_shape reports correct dimensions ─────────────────────

def test_explore_shape_does_not_modify_data(sample_df):
    """explore_shape should not alter the DataFrame.

    WHY: Exploration functions should be read-only. If they accidentally
    modify the data, downstream analysis could produce wrong results.
    """
    original_shape = sample_df.shape

    # Call the function (it prints output, but we only care about side effects).
    explore_shape(sample_df)

    assert sample_df.shape == original_shape, "explore_shape should not change the DataFrame"


# ── Test: select_columns picks the right columns ──────────────────────

def test_select_columns_returns_name_and_grade(sample_df, capsys):
    """select_columns should display only the name and grade columns.

    WHY: Column selection is one of the most common pandas operations.
    This test verifies that the function selects the correct subset.
    capsys captures printed output so we can verify it contains expected text.
    """
    select_columns(sample_df)
    captured = capsys.readouterr()

    # The function prints the selected columns, so we check the output.
    assert "name" in captured.out, "Output should mention the 'name' column"
    assert "grade" in captured.out, "Output should mention the 'grade' column"


# ── Test: sort_by_grade orders highest first ───────────────────────────

def test_sort_by_grade_highest_first(sample_df, capsys):
    """sort_by_grade should display grades in descending order.

    WHY: Sorting is fundamental in data analysis. Verifying the sort order
    ensures the ascending=False parameter is applied correctly.
    """
    sort_by_grade(sample_df)
    captured = capsys.readouterr()

    # Diana has the highest grade (95), so her name should appear first
    # in the sorted output.
    assert "Diana" in captured.out or "95" in captured.out, (
        "The highest-scoring student should appear in the output"
    )


# ── Test: DataFrame column types ──────────────────────────────────────

def test_dataframe_has_expected_dtypes(sample_df):
    """The DataFrame should have numeric types for grade and age.

    WHY: If pandas reads grade or age as strings (object type), mathematical
    operations like mean() and sort_values() would fail or give wrong results.
    This test catches type-detection problems early.
    """
    assert sample_df["grade"].dtype in ("int64", "int32", "float64"), (
        "grade column should be numeric"
    )
    assert sample_df["age"].dtype in ("int64", "int32", "float64"), (
        "age column should be numeric"
    )
