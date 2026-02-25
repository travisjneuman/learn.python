"""
Tests for Project 03 — Data Cleaning

These tests verify each step of the data cleaning pipeline: type conversion,
missing value handling, duplicate removal, and merging. Each test uses a
small inline DataFrame with known problems so we can predict the outcome.

Why test data cleaning?
    Cleaning functions are where most data bugs hide. A wrong coerce, a
    forgotten fillna, or a merge on the wrong column can silently corrupt
    your analysis. Tests catch these issues before they propagate.

Run with: pytest tests/test_project.py -v
"""

import pandas as pd
import pytest

from project import (
    fix_data_types,
    handle_missing_values,
    remove_duplicates,
    merge_with_products,
)


# ── Fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def messy_df():
    """Create a small DataFrame with intentional problems.

    Problems included:
    - quantity has a non-numeric value ("five") in row 2
    - region is missing (NaN) in row 1
    - price is missing in row 3
    - rows 0 and 4 are exact duplicates
    """
    return pd.DataFrame({
        "date": ["2024-01-01", "2024-01-02", "2024-01-03", None, "2024-01-01"],
        "product_id": [1, 2, 3, 4, 1],
        "quantity": ["10", "20", "five", "15", "10"],
        "price": [9.99, 19.99, 14.99, None, 9.99],
        "region": ["East", None, "West", "East", "East"],
    })


@pytest.fixture
def products_df(tmp_path):
    """Create a temporary products CSV for merge testing.

    Returns the path to the CSV file, which merge_with_products expects.
    """
    products = pd.DataFrame({
        "product_id": [1, 2, 3],
        "product_name": ["Widget", "Gadget", "Doohickey"],
        "category": ["Tools", "Electronics", "Tools"],
    })
    csv_path = tmp_path / "products.csv"
    products.to_csv(csv_path, index=False)
    return str(csv_path)


# ── Test: fix_data_types converts non-numeric values ───────────────────

def test_fix_data_types_converts_valid_numbers(messy_df):
    """fix_data_types should convert numeric strings to actual numbers.

    WHY: pd.to_numeric with errors='coerce' silently turns invalid values
    into NaN instead of crashing. This test verifies that valid numbers
    like '10' and '20' are converted correctly.
    """
    result = fix_data_types(messy_df)

    # '10' should become 10.0, '20' should become 20.0
    assert result["quantity"].iloc[0] == 10.0
    assert result["quantity"].iloc[1] == 20.0


def test_fix_data_types_coerces_invalid_to_nan(messy_df):
    """fix_data_types should turn non-numeric values like 'five' into NaN.

    WHY: The whole point of errors='coerce' is to handle bad data gracefully.
    If coercion does not work, the column stays as strings and all math on
    it would fail silently or produce wrong results.
    """
    result = fix_data_types(messy_df)

    # 'five' cannot be converted, so it should become NaN.
    assert pd.isna(result["quantity"].iloc[2]), "'five' should become NaN"


# ── Test: handle_missing_values drops and fills correctly ──────────────

def test_handle_missing_values_drops_rows_with_missing_essentials():
    """handle_missing_values should drop rows where quantity, price, or date is NaN.

    WHY: The cleaning strategy says these columns are essential for
    calculations. If a row is missing any of them, it should be dropped.
    """
    df = pd.DataFrame({
        "date": ["2024-01-01", "2024-01-02", None],
        "product_id": [1, 2, 3],
        "quantity": [10.0, None, 5.0],
        "price": [9.99, 19.99, 14.99],
        "region": ["East", "West", "East"],
    })

    result = handle_missing_values(df)

    # Row 1 (missing quantity) and row 2 (missing date) should be dropped.
    assert len(result) == 1, "Only 1 row should survive (row 0)"


def test_handle_missing_values_fills_missing_region():
    """handle_missing_values should fill missing region with 'Unknown'.

    WHY: The strategy says region is useful but not critical. Filling with
    'Unknown' keeps the row while marking it as incomplete. Dropping it
    would lose valuable data.
    """
    df = pd.DataFrame({
        "date": ["2024-01-01", "2024-01-02"],
        "product_id": [1, 2],
        "quantity": [10.0, 20.0],
        "price": [9.99, 19.99],
        "region": [None, "West"],
    })

    result = handle_missing_values(df)

    assert result["region"].iloc[0] == "Unknown", "Missing region should be filled"
    assert result["region"].iloc[1] == "West", "Existing region should be unchanged"


# ── Test: remove_duplicates keeps first occurrence ─────────────────────

def test_remove_duplicates_removes_exact_copies():
    """remove_duplicates should remove rows that are exact copies of earlier rows.

    WHY: Duplicate rows inflate counts and sums. This test verifies that
    drop_duplicates() is applied and keeps only the first occurrence.
    """
    df = pd.DataFrame({
        "date": ["2024-01-01", "2024-01-02", "2024-01-01"],
        "product_id": [1, 2, 1],
        "quantity": [10, 20, 10],
        "price": [9.99, 19.99, 9.99],
        "region": ["East", "West", "East"],
    })

    result = remove_duplicates(df)

    assert len(result) == 2, "Duplicate row should be removed, leaving 2 unique rows"


def test_remove_duplicates_keeps_non_duplicates():
    """remove_duplicates should not remove rows that are different.

    WHY: If the deduplication logic is too aggressive (e.g., using a subset
    of columns instead of all columns), it might incorrectly remove rows
    that only share some values.
    """
    df = pd.DataFrame({
        "product_id": [1, 1],
        "quantity": [10, 20],  # Different quantities = different rows
        "price": [9.99, 9.99],
        "region": ["East", "East"],
    })

    result = remove_duplicates(df)

    assert len(result) == 2, "Rows with different quantities are NOT duplicates"


# ── Test: merge_with_products adds product info ────────────────────────

def test_merge_adds_product_name(products_df):
    """merge_with_products should add product_name and category columns.

    WHY: The merge (SQL JOIN) enriches sales data with product details.
    If the merge key is wrong or the join type is incorrect, product info
    would be missing or rows would be duplicated.
    """
    sales = pd.DataFrame({
        "date": ["2024-01-01"],
        "product_id": [1],
        "quantity": [10],
        "price": [9.99],
        "region": ["East"],
    })

    result = merge_with_products(sales, products_df)

    assert "product_name" in result.columns, "Merge should add product_name column"
    assert "category" in result.columns, "Merge should add category column"
    assert result["product_name"].iloc[0] == "Widget", "Product 1 should be Widget"


def test_merge_left_join_keeps_unmatched_rows(products_df):
    """Left join should keep sales rows even if product_id has no match.

    WHY: A left join preserves all rows from the left (sales) table.
    If we accidentally used an inner join, unmatched rows would disappear
    and we would lose sales data.
    """
    sales = pd.DataFrame({
        "date": ["2024-01-01"],
        "product_id": [999],  # No matching product
        "quantity": [5],
        "price": [1.99],
        "region": ["North"],
    })

    result = merge_with_products(sales, products_df)

    assert len(result) == 1, "Left join should keep the sales row even with no match"
    assert pd.isna(result["product_name"].iloc[0]), "Unmatched product should be NaN"
