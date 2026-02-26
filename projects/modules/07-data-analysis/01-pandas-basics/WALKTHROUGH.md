# Pandas Basics — Step-by-Step Walkthrough

[<- Back to Project README](./README.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 15 minutes attempting it independently. The goal is to load a CSV file into a pandas DataFrame and explore it with built-in methods. If you can call `pd.read_csv()` and print the first five rows, you are on the right track.

## Thinking Process

A DataFrame is a table — rows and columns, like a spreadsheet. The columns have names (like "name", "grade", "age"), and the rows are numbered starting from 0. Everything you do in pandas starts with getting data into a DataFrame and then asking questions about it: how many rows? What are the column types? What is the average grade? Which student scored highest?

The first thing every data analyst does with new data is explore it. You do not jump straight to analysis — you look at the shape, the types, the first few rows, and the basic statistics. This is exactly what this project teaches: the exploration toolkit that you will use before every analysis.

Think of it like unpacking a box. Before you use what is inside, you check what is there, how much of it there is, and whether anything is broken (missing values). `head()` opens the box. `shape` counts the items. `dtypes` labels them. `describe()` gives you a quality report.

## Step 1: Load the CSV File

**What to do:** Import pandas and use `pd.read_csv()` to load a CSV file into a DataFrame.

**Why:** CSV (Comma-Separated Values) is the most common data exchange format. `pd.read_csv()` reads the file, figures out column names from the first row, and creates a DataFrame. After this one line, you have a full table in memory that you can query, filter, sort, and analyze.

```python
import pandas as pd

df = pd.read_csv("data/students.csv")
print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
```

Two details to notice:

- **`import pandas as pd`** is a universal convention. Every pandas tutorial, Stack Overflow answer, and professional codebase uses `pd`.
- **`len(df)`** returns the number of rows. `len(df.columns)` returns the number of columns. The DataFrame knows its own dimensions.

**Predict:** What type is `df`? Run `print(type(df))` to check. What about `df["name"]` — what type is a single column?

## Step 2: Explore with head(), shape, and dtypes

**What to do:** Use the built-in exploration methods to understand the data's structure.

**Why:** These methods answer the first questions you should ask about any dataset. `head()` shows you what the data looks like. `shape` tells you how big it is. `dtypes` tells you what types each column holds — which matters because you cannot do math on text columns.

```python
# See the first 5 rows
print(df.head())

# How many rows and columns?
rows, cols = df.shape
print(f"Rows: {rows}, Columns: {cols}")

# What types are the columns?
print(df.dtypes)
```

Notice that `shape` is a property (no parentheses), while `head()` is a method (with parentheses). `shape` returns a tuple `(rows, columns)` that you can unpack. `dtypes` shows `object` for text columns — pandas uses "object" to mean "string."

**Predict:** What does `df.head(10)` do differently from `df.head()`? What about `df.tail(3)`?

## Step 3: Get Summary Statistics with describe()

**What to do:** Call `df.describe()` to see count, mean, std, min, max, and quartiles for numeric columns.

**Why:** `describe()` gives you a statistical snapshot of every numeric column in one call. It tells you the average grade, the youngest and oldest student, the spread of the data — all in a single table. This is the fastest way to spot anomalies (negative ages, impossible grades, outliers).

```python
print(df.describe())
```

`describe()` only shows numeric columns by default. Text columns (name, subject) are excluded because you cannot calculate a mean of names. If you want to include text columns, call `df.describe(include="all")`.

**Predict:** What is the difference between `describe()` and `info()`? Try both. Which one tells you about missing values?

## Step 4: Select Specific Columns

**What to do:** Use bracket notation to pick specific columns from the DataFrame.

**Why:** You rarely need every column. Selecting just the columns you care about makes the data easier to read and faster to process. Single brackets return a Series (one column). Double brackets return a DataFrame (one or more columns).

```python
# Single column as a Series
grades = df["grade"]

# Multiple columns as a DataFrame
subset = df[["name", "grade"]]
print(subset.head())
```

The double-bracket syntax `df[["name", "grade"]]` passes a list of column names. The outer brackets are the indexing operator; the inner brackets create the list. This is a common stumbling point for beginners.

**Predict:** What error do you get if you write `df["name", "grade"]` (single brackets, no inner list)? Why?

## Step 5: Sort the Data

**What to do:** Use `sort_values()` to reorder rows by a column.

**Why:** Sorting answers questions like "who scored highest?" and "who is youngest?" `sort_values()` returns a new DataFrame with reordered rows — the original is untouched. `ascending=False` puts the highest values at the top.

```python
sorted_df = df.sort_values("grade", ascending=False)
print(sorted_df.head(10))
```

**Predict:** If two students have the same grade, what order are they in? Try sorting by `"age"` and see what happens with tied values. Can you sort by two columns at once?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| `FileNotFoundError` | Wrong path to the CSV file | Run the script from the project directory, or use an absolute path |
| `KeyError: 'score'` | Column name does not exist | Check `df.columns` to see the actual column names |
| `df["name", "grade"]` instead of `df[["name", "grade"]]` | Forgetting the inner list brackets | Double brackets: outer for indexing, inner for the list |
| Thinking `sort_values()` changes `df` | Pandas returns new objects by default | Assign the result: `sorted_df = df.sort_values(...)` |

## Testing Your Solution

There are no pytest tests for this project — run it and verify the output:

```bash
python project.py
```

Expected output:
```text
=== Loading student data ===
Loaded 30 rows and 4 columns from data/students.csv

=== First 5 rows (head) ===
        name  subject  grade  age
0  Alice Chen     Math     92   17
...

=== Shape ===
Rows: 30, Columns: 4
...

Done.
```

The data should match the CSV file. Check that the grade and age columns show as `int64`, and name and subject show as `object`.

## What You Learned

- **`pd.read_csv()`** loads a CSV file into a DataFrame — the fundamental data structure of pandas, like a spreadsheet in code.
- **`head()`, `shape`, `dtypes`, and `describe()`** are the exploration toolkit you use with every new dataset — they answer "what does this data look like?"
- **Column selection** uses single brackets for a Series (`df["col"]`) and double brackets for a DataFrame (`df[["col1", "col2"]]`) — the inner brackets create a list of column names.
- **`sort_values()`** reorders rows by a column and returns a new DataFrame — the original stays unchanged because pandas defaults to returning copies, not modifying in place.
