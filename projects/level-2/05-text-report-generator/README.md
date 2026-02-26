# Level 2 / Project 05 - Text Report Generator
Home: [README](../../../README.md)

## Before You Start

Recall these prerequisites before diving in:
- Can you use `zip()` to pair two lists together?
- Can you group items from a list into a dictionary of lists?

## Focus
- build readable reports from records

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/05-text-report-generator
python project.py data/sample_input.txt --group department --value salary
python project.py data/sample_input.txt --json
pytest -q
```

## Expected terminal output
```text
============================================================
  Data Report
============================================================
Total records: 10
Breakdown by department: ...
9 passed
```

## Expected artifacts
- Formatted text report on stdout
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--sort-by` flag to sort groups by total, mean, or count.
2. Add a "Bottom 5" section alongside the "Top 5" section.
3. Add a `--output` flag to save the report to a file.

## Break it (required)
1. Feed a CSV where the salary column has some non-numeric values (e.g. "N/A").
2. Feed a CSV with mismatched column counts (some rows have more/fewer fields).
3. Use a group field that does not exist in the header.

## Fix it (required)
1. Ensure `extract_numeric` handles "N/A" and blank values without crashing.
2. Handle rows with missing fields by padding with empty strings.
3. Show "UNKNOWN" when a group field is missing from a record.

## Explain it (teach-back)
1. How does `zip(headers, values)` pair headers with values?
2. Why is `sorted(groups.keys())` used instead of iterating `groups` directly?
3. What does `dict.get(key, default)` do differently from `dict[key]`?
4. When would you choose text reports over JSON output?

## Mastery check
You can move on when you can:
- explain how `zip` works with unequal-length lists,
- write a `group_by` function from memory,
- add a new statistic (e.g. median) to the report,
- format output with consistent column alignment.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Text Report Generator. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to group records by a field value. Can you show me how to build a dictionary of lists from a flat list, using a different example like grouping students by grade?"
- "Can you explain how `zip(headers, values)` works when the lists have different lengths?"

---

| [← Prev](../04-error-safe-divider/README.md) | [Home](../../../README.md) | [Next →](../06-records-deduplicator/README.md) |
|:---|:---:|---:|
