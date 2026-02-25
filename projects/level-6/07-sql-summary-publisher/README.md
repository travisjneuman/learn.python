# Level 6 / Project 07 - SQL Summary Publisher
Home: [README](../../../README.md)

## Focus
- daily aggregate publication flow

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/07-sql-summary-publisher
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "total_sales": 7,
  "total_revenue": 1374.10,
  "by_region": [...],
  "by_product": [...],
  "top_sale": {"product": "Widget", "region": "West", "revenue": 299.70}
}
```

## Expected artifacts
- `data/output_summary.json` — aggregate metrics as JSON
- `data/output_summary.txt` — human-readable formatted report
- Passing tests (`pytest -q` → 6+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a "bottom performer" section showing the product with the lowest total revenue.
2. Add a `--min-revenue` filter that excludes sales below a threshold from the summary.
3. Add a date-range filter: `--from` and `--to` flags to limit which sales are included.
4. Re-run script and tests after each change.

## Break it (required)
1. Feed an empty sales array `[]` and observe how the aggregates handle zero rows.
2. Include a sale with a negative revenue value and observe the summary.
3. Feed sales with a region name containing special characters.

## Fix it (required)
1. Add a guard for empty datasets that returns zeroed-out metrics instead of errors.
2. Validate that revenue is non-negative before including in aggregates.
3. Add tests for edge cases.

## Explain it (teach-back)
1. What is the difference between `SUM`, `COUNT`, `AVG`, `MIN`, and `MAX` in SQL?
2. Why do we use `COALESCE` with aggregate functions?
3. What happens if GROUP BY produces zero groups?
4. When would you use a subquery vs a simple GROUP BY?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../06-query-performance-checker/README.md) | [Home](../../../README.md) | [Next →](../08-data-lineage-capture/README.md) |
|:---|:---:|---:|
