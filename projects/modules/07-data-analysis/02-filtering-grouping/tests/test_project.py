"""
Tests for Project 02 — Filtering & Grouping

These tests verify boolean filtering, .loc[] selection, value_counts(),
groupby(), and multi-aggregation using small inline DataFrames.

Why test data analysis functions?
    Even though pandas does the heavy lifting, your functions add logic on
    top (thresholds, column choices, aggregation strategies). Tests verify
    that YOUR logic is correct, not that pandas works.

Run with: pytest tests/test_project.py -v
"""

import pandas as pd
import pytest

from project import (
    filter_high_grades,
    filter_with_loc,
    count_subjects,
    group_by_subject_mean,
    group_by_subject_multi_agg,
    top_students_per_subject,
)


@pytest.fixture
def sample_df():
    """Create a small DataFrame mimicking students.csv.

    This dataset is carefully designed so we know the expected results:
    - 2 students above grade 80 (Alice=92, Diana=95)
    - 2 Math students, 1 Science, 1 English
    - Top per subject: Alice (Math), Bob (Science), Diana (English)
    """
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "subject": ["Math", "Science", "Math", "English"],
        "grade": [92, 78, 75, 95],
        "age": [16, 17, 16, 18],
    })


# ── Test: filter_high_grades returns correct rows ──────────────────────

def test_filter_high_grades_default_threshold(sample_df):
    """filter_high_grades(df, 80) should return only students above 80.

    WHY: Boolean indexing is the primary way to filter data in pandas.
    Getting the threshold comparison wrong (>= vs >, wrong column) would
    silently return wrong results. This test catches those mistakes.
    """
    result = filter_high_grades(sample_df, threshold=80)

    assert len(result) == 2, "Should find exactly 2 students above grade 80"
    assert set(result["name"]) == {"Alice", "Diana"}, (
        "Alice (92) and Diana (95) should be the high performers"
    )


def test_filter_high_grades_custom_threshold(sample_df):
    """filter_high_grades with a high threshold should return fewer rows.

    WHY: The threshold parameter should actually be used — this test verifies
    that changing the threshold changes the output. A hardcoded filter would
    fail this test.
    """
    result = filter_high_grades(sample_df, threshold=93)

    assert len(result) == 1, "Only Diana (95) is above 93"
    assert result.iloc[0]["name"] == "Diana"


# ── Test: filter_with_loc selects Science students ─────────────────────

def test_filter_with_loc_returns_science_only(sample_df):
    """filter_with_loc should return only Science students with name and grade.

    WHY: .loc[] is more explicit than bracket indexing. This test verifies
    both the row filter (subject == 'Science') and the column selection
    (only 'name' and 'grade' columns).
    """
    result = filter_with_loc(sample_df)

    assert len(result) == 1, "Only Bob studies Science"
    assert list(result.columns) == ["name", "grade"], (
        "Should return only name and grade columns"
    )
    assert result.iloc[0]["name"] == "Bob"


# ── Test: count_subjects tallies correctly ─────────────────────────────

def test_count_subjects_returns_correct_counts(sample_df):
    """count_subjects should count students per subject.

    WHY: value_counts() is the quickest way to see the distribution of a
    categorical variable. This test verifies the counts match our known data.
    """
    counts = count_subjects(sample_df)

    assert counts["Math"] == 2, "Math has 2 students (Alice, Charlie)"
    assert counts["Science"] == 1, "Science has 1 student (Bob)"
    assert counts["English"] == 1, "English has 1 student (Diana)"


# ── Test: group_by_subject_mean computes correct averages ──────────────

def test_group_by_subject_mean_values(sample_df):
    """group_by_subject_mean should return the average grade per subject.

    WHY: groupby + mean is the pandas equivalent of SQL's GROUP BY + AVG.
    An incorrect grouping column or aggregation function would give wrong
    numbers. We verify against hand-calculated averages.
    """
    means = group_by_subject_mean(sample_df)

    # Math average: (92 + 75) / 2 = 83.5
    assert means["Math"] == pytest.approx(83.5), "Math mean should be 83.5"
    # Science average: 78 / 1 = 78.0
    assert means["Science"] == pytest.approx(78.0), "Science mean should be 78.0"
    # English average: 95 / 1 = 95.0
    assert means["English"] == pytest.approx(95.0), "English mean should be 95.0"


# ── Test: group_by_subject_multi_agg returns mean, max, min ────────────

def test_group_by_subject_multi_agg_columns(sample_df):
    """group_by_subject_multi_agg should return a table with mean, max, min.

    WHY: agg() with multiple functions is a powerful pattern. This test
    verifies that all three aggregation columns are present and that max/min
    are correct for the Math group (which has 2 students).
    """
    result = group_by_subject_multi_agg(sample_df)

    assert "mean" in result.columns, "Result should have a 'mean' column"
    assert "max" in result.columns, "Result should have a 'max' column"
    assert "min" in result.columns, "Result should have a 'min' column"

    # Math: max=92, min=75
    assert result.loc["Math", "max"] == 92
    assert result.loc["Math", "min"] == 75


# ── Test: top_students_per_subject finds the best in each ─────────────

def test_top_students_per_subject(sample_df):
    """top_students_per_subject should find the highest-scoring student per subject.

    WHY: Combining groupby with idxmax is a common pattern for finding
    "the best X in each category." This test verifies the combination works
    end-to-end.
    """
    result = top_students_per_subject(sample_df)

    # Convert to a dict of subject -> name for easy checking.
    top_by_subject = dict(zip(result["subject"], result["name"]))

    assert top_by_subject["Math"] == "Alice", "Alice has the highest Math grade (92)"
    assert top_by_subject["Science"] == "Bob", "Bob is the only Science student"
    assert top_by_subject["English"] == "Diana", "Diana is the only English student"
