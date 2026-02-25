# Level 2 / Project 03 - Data Cleaning Pipeline
Home: [README](../../../README.md)

## Focus
- standardize text and required fields

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/03-data-cleaning-pipeline
python project.py data/sample_input.txt
python project.py data/sample_input.txt --filter "@.*\."
pytest -q
```

## Expected terminal output
```text
=== Cleaning Stats ===
{"original_count": 10, "cleaned_count": 7, ...}
11 passed
```

## Expected artifacts
- Cleaning stats and cleaned records on stdout
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a cleaning step that normalizes phone numbers (strip dashes/parens).
2. Write rejected records to a separate `quarantine.txt` with reasons.
3. Add a `--dry-run` flag that reports stats without writing output.

## Break it (required)
1. Feed a file where every line is whitespace — does it crash or return empty?
2. Use a bad regex pattern in `--filter` (e.g. `[unclosed`) — what happens?
3. Feed records with mixed encodings — does normalise_case break?

## Fix it (required)
1. Wrap `re.compile` in a try/except for invalid regex patterns.
2. Add a test for all-blank input files.
3. Handle encoding errors gracefully with a `try/except UnicodeDecodeError`.

## Explain it (teach-back)
1. Why does the pipeline run steps in a specific order (strip before dedupe)?
2. How does using a set for deduplication achieve O(1) lookup?
3. What is the difference between `re.search` and `re.match`?
4. Where would you use a data cleaning pipeline in a real data workflow?

## Mastery check
You can move on when you can:
- explain why pipeline step ordering matters,
- describe how sets enable fast deduplication,
- add a new cleaning step without modifying existing ones,
- explain regular expressions used in `filter_by_pattern`.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Virtual Environments](../../../concepts/virtual-environments.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../02-nested-data-flattener/README.md) | [Home](../../../README.md) | [Next →](../04-error-safe-divider/README.md) |
|:---|:---:|---:|
