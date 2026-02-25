# Level 4 / Project 07 - Duplicate Record Investigator
Home: [README](../../../README.md)

## Focus
- collision analysis and root cause

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/07-duplicate-record-investigator
python project.py --input data/sample_input.csv --output data/duplicates_report.json --keys name,email --threshold 0.8
pytest -q
```

## Expected terminal output
```text
{
  "total_records": 7,
  "duplicate_pairs_found": 3,
  "duplicates": [ ... ]
}
6 passed
```

## Expected artifacts
- `data/duplicates_report.json` — exact and fuzzy duplicate pairs
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--method` flag supporting both `bigram` (current) and `levenshtein` similarity.
2. Add a `--group` mode that clusters duplicates into groups instead of listing pairs.
3. Re-run script and tests — add a parametrized test for the new method.

## Break it (required)
1. Use a very low threshold (0.1) and observe how many false positives appear.
2. Feed it a CSV with only one row — verify no crash on the single-record case.
3. Use key fields that do not exist in the CSV and observe the behavior.

## Fix it (required)
1. Validate that key fields exist in the CSV headers before comparing.
2. Add a warning when the threshold produces more than 50% of records as duplicates.
3. Re-run until all tests pass.

## Explain it (teach-back)
1. What are character bigrams and why are they useful for fuzzy matching?
2. Why does Jaccard similarity use set intersection/union instead of comparing characters directly?
3. What is the time complexity of the nested-loop comparison — how would you optimize it?
4. When would fuzzy matching produce false positives, and how would you handle them?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../06-backup-rotation-tool/README.md) | [Home](../../../README.md) | [Next →](../08-malformed-row-quarantine/README.md) |
|:---|:---:|---:|
