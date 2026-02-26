# Module 07 / Project 01 — Pandas Basics

[README](../../../../README.md) · [Module Index](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | [Walkthrough](./WALKTHROUGH.md) | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- Loading CSV data with `pd.read_csv()`
- Exploring a DataFrame: `head()`, `tail()`, `shape`, `dtypes`, `info()`, `describe()`
- Selecting columns by name
- Sorting rows with `sort_values()`

## Why this project exists

Before you can analyze data, you need to know how to load it and look at it. This project teaches you how to get a CSV file into a pandas DataFrame and use built-in methods to understand what the data looks like — how many rows, what columns exist, what types the values are, and what the basic statistics tell you. These exploration steps are the first thing every data analyst does with a new data set.

## Run

```bash
cd projects/modules/07-data-analysis/01-pandas-basics
python project.py
```

## Expected output

```text
=== Loading student data ===
Loaded 30 rows and 4 columns from data/students.csv

=== First 5 rows (head) ===
        name  subject  grade  age
0  Alice Chen     Math     92   17
1  Bob Martinez  Science   78   16
2  Carol Johnson  English   85   17
3    David Kim     Math     67   16
4    Eva Patel  Science     91   18

=== Shape ===
Rows: 30, Columns: 4

=== Column types (dtypes) ===
name       object
subject    object
grade       int64
age         int64
dtype: object

=== Summary statistics (describe) ===
            grade        age
count  30.000000  30.000000
mean   80.100000  17.000000
...

=== Selecting just name and grade columns ===
(first 5 rows)
            name  grade
0     Alice Chen     92
1   Bob Martinez     78
...

=== Sorted by grade (highest first) ===
(first 10 rows)
          name  subject  grade  age
18   Sam Turner     Math     96   17
...

Done.
```

The exact numbers will match the CSV data. The `...` sections are abbreviated here — your output will show all rows and statistics.

## Alter it

1. Change `head()` to `head(10)` and see what happens. Try `tail(3)`.
2. Sort by `age` instead of `grade`. What happens when two students have the same age?
3. Select three columns instead of two. What does `df[["name", "subject", "grade"]]` return?
4. Try `df["grade"].mean()` and `df["grade"].max()` — what do they return?

## Break it

1. Change the filename in `read_csv()` to a file that does not exist. What error do you get?
2. Try selecting a column that does not exist: `df["score"]`. Read the error message.
3. Remove the `import pandas as pd` line. What happens?

## Fix it

1. Wrap `read_csv()` in a try/except that catches `FileNotFoundError` and prints a friendly message.
2. Before selecting a column, check if it exists: `if "score" in df.columns`.
3. Put the import back.

## Explain it

1. What is a DataFrame? How is it different from a list of dictionaries?
2. What does `describe()` tell you that `info()` does not?
3. Why does `dtypes` show `object` for the name and subject columns instead of `string`?
4. What is the difference between `df["grade"]` (one column) and `df[["grade"]]` (double brackets)?

## Mastery check

You can move on when you can:

- Load any CSV file into a DataFrame from memory.
- Use `head()`, `shape`, `dtypes`, `info()`, and `describe()` to explore a new data set.
- Select one or more columns from a DataFrame.
- Sort a DataFrame by any column, ascending or descending.

---

## Related Concepts

- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [Types and Conversions](../../../../concepts/types-and-conversions.md)
- [What is a Variable](../../../../concepts/what-is-a-variable.md)
- [Quiz: Collections Explained](../../../../concepts/quizzes/collections-explained-quiz.py)

## Next

[Project 02 — Filtering & Grouping](../02-filtering-grouping/)
