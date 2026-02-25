# Module 07 / Project 02 — Filtering & Grouping

[README](../../../../README.md) · [Module Index](../README.md)

## Focus

- Boolean indexing to filter rows
- `.loc[]` for label-based selection
- `groupby()` and aggregation functions (`mean`, `max`, `min`)
- `agg()` for multiple aggregations at once
- `value_counts()` to count occurrences

## Why this project exists

Loading data is only the first step. Real analysis requires answering questions: "Which students scored above 80?" or "What is the average grade per subject?" This project teaches you how to filter rows based on conditions and group rows to compute summary statistics — the two most common operations in data analysis.

## Run

```bash
cd projects/modules/07-data-analysis/02-filtering-grouping
python project.py
```

## Expected output

```text
=== Loading student data ===
Loaded 30 rows from data/students.csv

=== Students with grade > 80 ===
Found 17 students with grade above 80
        name  subject  grade  age
0  Alice Chen     Math     92   17
...

=== Using .loc[] to filter ===
Science students only:
...

=== Subject counts (value_counts) ===
subject
Math       10
Science    10
English    10
Name: count, dtype: int64

=== Group by subject — mean grade ===
subject
English    80.555556
Math       79.300000
Science    79.100000
Name: grade, dtype: float64

=== Group by subject — multiple aggregations ===
            mean   max  min
subject
English    80.56  95.0   59
Math       79.30  96.0   54
Science    79.10  93.0   65

=== Top students per subject ===
...

Done.
```

## Alter it

1. Change the filter threshold from 80 to 90. How many students remain?
2. Filter for students who are both older than 16 AND scored above 85. (Hint: combine two conditions with `&`.)
3. Group by `age` instead of `subject`. What does the mean grade per age tell you?
4. Add `"std"` to the aggregation list to see the standard deviation per subject.

## Break it

1. Try filtering with `df["grade"] > 80 and df["age"] > 16`. What error do you get? Why can you not use `and` here?
2. Use `groupby()` on a column that does not exist. Read the error.
3. Pass an invalid aggregation function name to `agg()`. What happens?

## Fix it

1. Replace `and` with `&` and wrap each condition in parentheses: `(df["grade"] > 80) & (df["age"] > 16)`.
2. Check if the column exists before grouping: `if "subject" in df.columns`.
3. Use only valid aggregation names: `"mean"`, `"max"`, `"min"`, `"sum"`, `"count"`, `"std"`.

## Explain it

1. What is boolean indexing? How does `df[df["grade"] > 80]` work internally?
2. What is the difference between `df["grade"]` and `df.loc[:, "grade"]`?
3. What does `groupby()` return before you call an aggregation function on it?
4. Why does pandas use `&` instead of `and` for combining conditions?

## Mastery check

You can move on when you can:

- Filter a DataFrame by any condition, including combined conditions, from memory.
- Group data by a column and compute mean, max, min, and count.
- Use `agg()` to apply multiple aggregation functions in one call.
- Use `value_counts()` to see the distribution of a categorical column.

---

## Related Concepts

- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [Functions Explained](../../../../concepts/functions-explained.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Quiz: Collections Explained](../../../../concepts/quizzes/collections-explained-quiz.py)

## Next

[Project 03 — Data Cleaning](../03-data-cleaning/)
