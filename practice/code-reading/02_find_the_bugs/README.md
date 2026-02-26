# Exercise 02 — Find the Bugs

This module (`codebase.py`) is a data processing pipeline that reads sales records from a CSV, filters them by date, summarizes revenue per category, and writes results to a new file.

It looks reasonable. It has docstrings. It runs without crashing on simple inputs.

**It has 4 bugs.** Find and fix all of them.

## Rules

1. Read the code carefully before running anything.
2. For each bug, write down:
   - Which function contains the bug
   - What the bug is
   - What the correct behavior should be
   - Your fix
3. After fixing all 4, run the tests in `tests/test_codebase.py` to verify.

## Hints (read one at a time, only if stuck)

<details>
<summary>Hint 1: Think about resources</summary>
One function opens something but never closes it. What happens if this function is called many times?
</details>

<details>
<summary>Hint 2: Think about indexing</summary>
The paginate function claims to be 1-indexed. Is it really?
</details>

<details>
<summary>Hint 3: Think about whitespace</summary>
CSV data from the real world is messy. What if there are trailing spaces in a column value?
</details>

<details>
<summary>Hint 4: Think about boundaries</summary>
The docstring for filter_by_date says the range is [start, end). Read the code. Does the implementation match that contract?
</details>

## What you are practicing

- Reading code critically (not trusting that it works just because it looks clean)
- Identifying common bug patterns: resource leaks, off-by-one errors, missing input sanitization, contract violations
- Writing fixes and verifying them with tests
