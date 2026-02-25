# Module 07 — Data Analysis

[README](../../../README.md) · Modules: [Index](../README.md)

## Overview

This module teaches you how to load, clean, explore, and visualize data using Python's most popular data analysis libraries: pandas and matplotlib. You will work with CSV files containing realistic data sets — student grades, messy sales records, and transaction logs — progressively building up to a complete analysis pipeline.

Every project uses local CSV files so you do not need a database or internet connection. By the end you will be able to take a raw data file, clean it, answer questions about it, produce charts, and export a summary report.

## Prerequisites

Complete **Level 2** before starting this module. You should be comfortable with:

- Functions and return values
- Reading and writing files
- Dictionaries and lists
- Basic testing with pytest
- Running scripts from the command line

## Learning objectives

By the end of this module you will be able to:

1. Load CSV data into a pandas DataFrame and explore its shape, types, and summary statistics.
2. Filter rows with boolean indexing, group data, and compute aggregations.
3. Detect and handle missing values, fix data types, remove duplicates, and merge DataFrames.
4. Create bar charts, line charts, scatter plots, and multi-panel figures with matplotlib.
5. Build a complete analysis pipeline: load, clean, analyze, visualize, and export a report.

## Projects

| # | Project | What you learn |
|---|---------|----------------|
| 01 | [Pandas Basics](./01-pandas-basics/) | DataFrame, read_csv, head(), describe(), info(), shape, dtypes |
| 02 | [Filtering & Grouping](./02-filtering-grouping/) | Boolean indexing, .loc[], groupby(), agg(), value_counts() |
| 03 | [Data Cleaning](./03-data-cleaning/) | isna(), fillna(), dropna(), dtype conversion, duplicates, merge |
| 04 | [Visualization](./04-visualization/) | matplotlib bar, line, scatter, subplots, labels, saving figures |
| 05 | [Analysis Report](./05-analysis-report/) | Full pipeline — load, clean, analyze, visualize, export summary |

Work through them in order. Each project builds on the previous one.

## Setup

Create a virtual environment and install dependencies before starting:

```bash
cd projects/modules/07-data-analysis
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

See [concepts/virtual-environments.md](../../../concepts/virtual-environments.md) for a full explanation of virtual environments.

## Dependencies

This module requires three packages (listed in `requirements.txt`):

- **pandas** — the workhorse of data analysis in Python. It gives you the DataFrame, a spreadsheet-like structure you can filter, group, and transform with one-liners.
- **matplotlib** — the standard plotting library. You can create bar charts, line charts, scatter plots, histograms, and complex multi-panel figures.
- **openpyxl** — an Excel file engine that pandas uses under the hood when reading or writing `.xlsx` files. We install it so pandas has full Excel support available if you want to experiment.

## A note on data analysis workflow

Real data analysis follows a predictable cycle:

1. **Load** — read the raw data from a file or database.
2. **Explore** — look at shape, types, summary stats, and sample rows.
3. **Clean** — fix missing values, wrong types, duplicates, and inconsistencies.
4. **Analyze** — filter, group, aggregate, and compute the numbers you need.
5. **Visualize** — create charts that make patterns visible.
6. **Report** — export findings so others can act on them.

This module walks you through each step across five projects, then combines them all in the final project.
