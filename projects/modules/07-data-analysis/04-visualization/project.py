"""
Project 04 — Visualization

This script creates four charts from student grade data using matplotlib:
a bar chart, a line chart, a scatter plot, and a combined 2x2 subplot
figure. All charts are saved to data/charts.png.

Data file: data/students.csv (30 rows with name, subject, grade, age)
"""

# IMPORTANT: Set the backend BEFORE importing pyplot.
# "Agg" is a non-interactive backend that renders to files instead of
# opening a window. This is required when running scripts on servers,
# in CI/CD pipelines, or anywhere without a display.
import matplotlib
matplotlib.use("Agg")

# Now it is safe to import pyplot.
# The convention is to import it as "plt".
import matplotlib.pyplot as plt
import pandas as pd


def load_data(filepath):
    """Load CSV and return a DataFrame."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows from {filepath}")
    return df


def create_bar_chart(df):
    """
    Create a bar chart of average grade by subject.

    Bar charts are best for comparing categories. Each bar represents
    one category (subject), and the height represents the value (average grade).
    """
    print("\n=== Chart 1: Bar chart — Average grade by subject ===")

    # Calculate the average grade for each subject.
    avg_by_subject = df.groupby("subject")["grade"].mean()

    # Create a new figure and axes.
    # fig is the overall canvas. ax is the area where the chart is drawn.
    fig, ax = plt.subplots(figsize=(8, 5))

    # Draw the bar chart.
    # avg_by_subject.index gives the subject names (x-axis labels).
    # avg_by_subject.values gives the average grades (bar heights).
    ax.bar(avg_by_subject.index, avg_by_subject.values, color=["#3498db", "#e74c3c", "#2ecc71"])

    # Add labels and title. Always label your axes — a chart without
    # labels is like a sentence without a subject.
    ax.set_title("Average Grade by Subject", fontsize=14, fontweight="bold")
    ax.set_xlabel("Subject")
    ax.set_ylabel("Average Grade")

    # Add the actual values on top of each bar for clarity.
    for i, val in enumerate(avg_by_subject.values):
        ax.text(i, val + 0.5, f"{val:.1f}", ha="center", fontsize=10)

    plt.tight_layout()
    plt.close(fig)

    print("Created bar chart.")
    return fig


def create_line_chart(df):
    """
    Create a line chart of grades over student index.

    Line charts show trends over a sequence. Here the x-axis is just
    the row number (student index), so this shows the spread of grades
    across the data set rather than a time trend.
    """
    print("\n=== Chart 2: Line chart — Grades over student index ===")

    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot grade values. The x-axis defaults to the DataFrame index (0, 1, 2, ...).
    ax.plot(df.index, df["grade"], marker="o", markersize=4, linewidth=1, color="#2c3e50")

    # Add a horizontal line at the mean grade for reference.
    mean_grade = df["grade"].mean()
    ax.axhline(y=mean_grade, color="#e74c3c", linestyle="--", label=f"Mean: {mean_grade:.1f}")

    ax.set_title("Student Grades (ordered by index)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Student Index")
    ax.set_ylabel("Grade")
    ax.legend()

    plt.tight_layout()
    plt.close(fig)

    print("Created line chart.")
    return fig


def create_scatter_plot(df):
    """
    Create a scatter plot of age vs grade.

    Scatter plots reveal relationships between two numeric variables.
    Each dot represents one student, positioned by their age (x) and
    grade (y). If older students tend to score higher, you will see
    the dots trend upward from left to right.
    """
    print("\n=== Chart 3: Scatter plot — Age vs grade ===")

    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot each subject in a different color so we can see patterns per group.
    colors = {"Math": "#3498db", "Science": "#e74c3c", "English": "#2ecc71"}

    for subject, color in colors.items():
        # Filter to just this subject.
        subset = df[df["subject"] == subject]
        ax.scatter(subset["age"], subset["grade"], label=subject, color=color,
                   alpha=0.7, s=60, edgecolors="white", linewidth=0.5)

    ax.set_title("Age vs Grade by Subject", fontsize=14, fontweight="bold")
    ax.set_xlabel("Age")
    ax.set_ylabel("Grade")
    ax.legend()

    plt.tight_layout()
    plt.close(fig)

    print("Created scatter plot.")
    return fig


def create_combined_figure(df):
    """
    Create a 2x2 subplot combining all four chart types.

    subplots(2, 2) creates a grid of 4 axes inside a single figure.
    This is how you build multi-panel figures for reports and presentations.
    The axes are returned as a 2D array: axes[row][col].
    """
    print("\n=== Chart 4: Combined 2x2 subplot ===")

    # Create a 2x2 grid of subplots.
    # figsize controls the overall dimensions in inches.
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Panel 1 (top-left): Bar chart of average grade by subject.
    avg_by_subject = df.groupby("subject")["grade"].mean()
    axes[0][0].bar(avg_by_subject.index, avg_by_subject.values,
                   color=["#3498db", "#e74c3c", "#2ecc71"])
    axes[0][0].set_title("Average Grade by Subject")
    axes[0][0].set_ylabel("Average Grade")

    # Panel 2 (top-right): Line chart of grades.
    axes[0][1].plot(df.index, df["grade"], marker="o", markersize=3,
                    linewidth=1, color="#2c3e50")
    mean_grade = df["grade"].mean()
    axes[0][1].axhline(y=mean_grade, color="#e74c3c", linestyle="--",
                       label=f"Mean: {mean_grade:.1f}")
    axes[0][1].set_title("Grades by Student Index")
    axes[0][1].set_ylabel("Grade")
    axes[0][1].legend(fontsize=8)

    # Panel 3 (bottom-left): Scatter plot of age vs grade.
    colors = {"Math": "#3498db", "Science": "#e74c3c", "English": "#2ecc71"}
    for subject, color in colors.items():
        subset = df[df["subject"] == subject]
        axes[1][0].scatter(subset["age"], subset["grade"], label=subject,
                           color=color, alpha=0.7, s=40)
    axes[1][0].set_title("Age vs Grade")
    axes[1][0].set_xlabel("Age")
    axes[1][0].set_ylabel("Grade")
    axes[1][0].legend(fontsize=8)

    # Panel 4 (bottom-right): Histogram of grade distribution.
    axes[1][1].hist(df["grade"], bins=10, color="#8e44ad", edgecolor="white")
    axes[1][1].set_title("Grade Distribution")
    axes[1][1].set_xlabel("Grade")
    axes[1][1].set_ylabel("Frequency")

    # Add an overall title for the whole figure.
    fig.suptitle("Student Performance Dashboard", fontsize=16, fontweight="bold", y=1.02)

    # tight_layout() adjusts spacing so labels do not overlap.
    plt.tight_layout()

    # Save to a PNG file. dpi controls resolution (dots per inch).
    output_path = "data/charts.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved combined figure to {output_path}")


def main():
    print("=== Loading student data ===")
    df = load_data("data/students.csv")

    # Create each chart individually (for learning purposes).
    create_bar_chart(df)
    create_line_chart(df)
    create_scatter_plot(df)

    # Create the combined 2x2 figure and save it.
    create_combined_figure(df)

    print("\nDone. Open data/charts.png to see all four charts.")


if __name__ == "__main__":
    main()
