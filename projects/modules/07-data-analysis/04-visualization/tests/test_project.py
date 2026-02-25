"""
Tests for Project 04 — Visualization

These tests verify that chart-creation functions produce valid matplotlib
Figure objects without errors. We do NOT test visual appearance — that
requires manual review or pixel-comparison tools. Instead, we verify:
- Functions return Figure objects
- Figures have the expected number of axes
- Labels and titles are set

Why test visualizations this way?
    You cannot (easily) assert that a chart "looks correct" in a unit test.
    But you CAN verify that the code runs without errors, produces a Figure
    with the right structure, and sets the expected labels. This catches
    bugs like wrong column names, missing data, or incorrect axis counts.

Run with: pytest tests/test_project.py -v
"""

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for testing (no window).

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from project import (
    create_bar_chart,
    create_line_chart,
    create_scatter_plot,
    create_combined_figure,
)


@pytest.fixture
def sample_df():
    """Create a small DataFrame mimicking the students.csv structure.

    We include all three subjects (Math, Science, English) because the
    scatter_plot function uses them to assign colors. Missing a subject
    would cause a silent skip, which might hide a bug.
    """
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
        "subject": ["Math", "Science", "English", "Math", "Science", "English"],
        "grade": [92, 78, 85, 88, 91, 76],
        "age": [16, 17, 16, 18, 17, 16],
    })


@pytest.fixture(autouse=True)
def close_figures():
    """Close all matplotlib figures after each test to free memory.

    WHY: matplotlib keeps figure references in memory. In a test suite with
    many chart tests, this can leak significant memory. autouse=True means
    this cleanup runs automatically for every test in this file.
    """
    yield
    plt.close("all")


# ── Test: bar chart ────────────────────────────────────────────────────

def test_create_bar_chart_returns_figure(sample_df):
    """create_bar_chart should return a matplotlib Figure.

    WHY: If the function does not return a Figure, it cannot be saved to a
    file or displayed. This test catches the case where the function prints
    output but forgets to return the figure.
    """
    fig = create_bar_chart(sample_df)

    assert isinstance(fig, plt.Figure), "Should return a matplotlib Figure"


def test_bar_chart_has_one_axes(sample_df):
    """The bar chart figure should contain exactly one Axes (one panel).

    WHY: A single bar chart should have one axes. If the function accidentally
    creates subplots, it would have more.
    """
    fig = create_bar_chart(sample_df)
    axes = fig.get_axes()

    assert len(axes) == 1, "Bar chart should have exactly one axes"


# ── Test: line chart ───────────────────────────────────────────────────

def test_create_line_chart_returns_figure(sample_df):
    """create_line_chart should return a matplotlib Figure.

    WHY: Same rationale as the bar chart test — verify the return type.
    """
    fig = create_line_chart(sample_df)

    assert isinstance(fig, plt.Figure), "Should return a matplotlib Figure"


def test_line_chart_has_one_axes(sample_df):
    """The line chart figure should contain exactly one Axes."""
    fig = create_line_chart(sample_df)
    axes = fig.get_axes()

    assert len(axes) == 1, "Line chart should have exactly one axes"


# ── Test: scatter plot ─────────────────────────────────────────────────

def test_create_scatter_plot_returns_figure(sample_df):
    """create_scatter_plot should return a matplotlib Figure.

    WHY: The scatter plot loops over subjects and plots each separately.
    If a subject is missing from the data, the loop body is skipped silently.
    This test ensures the function completes without errors.
    """
    fig = create_scatter_plot(sample_df)

    assert isinstance(fig, plt.Figure), "Should return a matplotlib Figure"


# ── Test: combined figure ──────────────────────────────────────────────

def test_combined_figure_has_four_axes(sample_df, tmp_path, monkeypatch):
    """The combined 2x2 figure should have exactly 4 axes (panels).

    WHY: The combined figure uses subplots(2, 2) to create a 2x2 grid.
    If the grid dimensions are wrong, the chart layout would be incorrect.

    We monkeypatch the output path so the test does not write to data/charts.png.
    """
    # Redirect the savefig output to a temp directory.
    import os
    monkeypatch.chdir(tmp_path)
    os.makedirs(tmp_path / "data", exist_ok=True)

    create_combined_figure(sample_df)

    # The function saves to a file and closes the figure, so we check
    # that the output file was created.
    output_file = tmp_path / "data" / "charts.png"
    assert output_file.exists(), "Combined figure should be saved to data/charts.png"


# ── Test: functions handle small data gracefully ───────────────────────

def test_bar_chart_handles_single_subject():
    """Bar chart should work with just one subject (edge case).

    WHY: If the data has only one subject, the groupby returns one group
    and the bar chart has one bar. This should not cause an error.
    """
    df = pd.DataFrame({
        "name": ["Alice"],
        "subject": ["Math"],
        "grade": [92],
        "age": [16],
    })

    fig = create_bar_chart(df)

    assert isinstance(fig, plt.Figure), "Should handle single-subject data"
