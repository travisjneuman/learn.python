# Refactoring 02 — Monolithic Report

Open `messy.py`. This is a monthly sales report generator. It reads a CSV file, filters data by month, computes statistics, formats a text report, and writes it to a file.

The entire pipeline is one 90-line function. It works, but it violates every principle of clean code.

## Your mission

Split `generate_report()` into small, focused functions. Each function should do one thing. The tests in `tests/test_messy.py` must pass before and after every change.

## Refactoring goals

1. **Decompose into functions.** Extract at least these:
   - `read_csv(filepath)` — reads and returns raw rows
   - `filter_by_month(rows, year, month)` — returns matching rows
   - `compute_statistics(rows)` — returns totals, averages, top products
   - `format_report(stats, year, month)` — returns formatted text
   - `write_report(text, filepath)` — writes to file

2. **Add logging.** Replace silent processing with `logging` module calls at key stages (reading, filtering, computing, writing). Use `logging.info()`, not `print()`.

3. **Make output format configurable.** The report format is currently hardcoded. Refactor so the caller can choose between plain text (current format) and a simple CSV summary format.

4. **Add type hints and docstrings** to all new functions.

## Process

Do not attempt all changes at once. Follow this sequence:

```
1. Run tests (baseline)
2. Extract read_csv() -> tests pass
3. Extract filter_by_month() -> tests pass
4. Extract compute_statistics() -> tests pass
5. Extract format_report() -> tests pass
6. Extract write_report() -> tests pass
7. Add logging -> tests pass
8. Add format option -> add new tests -> all pass
```

## What you are practicing

- Decomposing a monolith into focused functions
- Maintaining backward compatibility during refactoring
- Adding logging to a pipeline
- Making code configurable without over-engineering
