# Module 07 / Project 04 — Visualization

[README](../../../../README.md) · [Module Index](../README.md)

## Focus

- matplotlib basics: `figure()`, `plot()`, `bar()`, `scatter()`
- Adding titles, axis labels, and legends
- Creating multi-panel figures with `subplots()`
- Saving figures to files with `savefig()`
- Using the Agg backend for non-interactive environments

## Why this project exists

Numbers in a table are hard to interpret. A chart makes patterns, outliers, and trends visible at a glance. This project teaches you how to create four common chart types with matplotlib — the standard Python plotting library. You will also learn how to combine multiple charts into a single figure and save the result to a file, which is how charts are shared in reports and presentations.

## Run

```bash
cd projects/modules/07-data-analysis/04-visualization
python project.py
```

## Expected output

```text
=== Loading student data ===
Loaded 30 rows from data/students.csv

=== Chart 1: Bar chart — Average grade by subject ===
Created bar chart.

=== Chart 2: Line chart — Grades over student index ===
Created line chart.

=== Chart 3: Scatter plot — Age vs grade ===
Created scatter plot.

=== Chart 4: Combined 2x2 subplot ===
Saved combined figure to data/charts.png

Done. Open data/charts.png to see all four charts.
```

After running, open `data/charts.png` to see the four charts arranged in a 2x2 grid.

## Alter it

1. Change the bar chart colors. Try `color="coral"` or `color=["#e74c3c", "#3498db", "#2ecc71"]`.
2. Add a horizontal line to the line chart at the class average: `ax.axhline(y=mean_grade, color="red", linestyle="--")`.
3. Change the scatter plot to use different colors per subject. (Hint: loop through subjects and plot each one separately with a label.)
4. Add a histogram of all grades as a fifth chart. Change the subplot grid to 2x3 or 3x2.

## Break it

1. Remove the `matplotlib.use("Agg")` line and run on a machine with no display. What error do you get?
2. Try creating a subplot grid of 2x2 but only fill 3 panels. What does the empty panel look like?
3. Pass a non-existent column name to the plot function. Read the error.

## Fix it

1. Always set the backend before importing pyplot: `matplotlib.use("Agg")` must come before `import matplotlib.pyplot as plt`.
2. Hide unused subplot panels with `ax.set_visible(False)`.
3. Check that columns exist before plotting: `if column_name in df.columns`.

## Explain it

1. What is the difference between `plt.plot()` and `ax.plot()`? When would you use each?
2. What does `matplotlib.use("Agg")` do? Why is it needed in scripts that save to files?
3. What is a "figure" vs an "axes" in matplotlib? How do they relate?
4. Why does `savefig()` need to be called before `plt.show()`?

## Mastery check

You can move on when you can:

- Create a bar chart, line chart, and scatter plot from a DataFrame.
- Add titles, axis labels, and a legend to any chart.
- Create a multi-panel figure with `subplots()`.
- Save a figure to a PNG file.
- Explain the difference between figure, axes, and plot.

---

## Related Concepts

- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Types and Conversions](../../../../concepts/types-and-conversions.md)
- [Quiz: Collections Explained](../../../../concepts/quizzes/collections-explained-quiz.py)

## Next

[Project 05 — Analysis Report](../05-analysis-report/)
