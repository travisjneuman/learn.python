# Level 2 / Project 12 - CSV to JSON Converter
Home: [README](../../../README.md)

**Estimated time:** 40 minutes

## Focus
- format conversion and schema checks

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/12-csv-to-json-converter
python project.py data/sample_input.txt --pretty
python project.py data/sample_input.txt --format columns
python project.py data/sample_input.txt --no-types
python project.py data/sample_input.txt --output data/output.json
pytest -q
```

## Expected terminal output
```text
[{"name": "Alice Johnson", "age": 30, "department": "Engineering", ...}, ...]
11 passed
```

## Expected artifacts
- JSON output on stdout or file
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--columns` flag to select only specific columns: `--columns name,age`.
2. Add row-count validation — log rows with mismatched column counts.
3. Add a `--schema` output that shows detected types per column.

## Break it (required) — Core
1. Feed a CSV with quoted fields containing commas (e.g. `"Smith, Jr"`).
2. Feed a file with inconsistent column counts per row.
3. Feed a value like `"123abc"` — does type inference misfire?

## Fix it (required) — Core
1. Add basic quoted-field handling for CSV values.
2. Pad short rows and truncate long rows to match header length.
3. Ensure `infer_type` only converts when the entire value is numeric.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does type inference try int before float?
2. What is the difference between "array of objects" and "columnar" JSON formats?
3. How does `zip(headers, values)` elegantly build record dicts?
4. When would you choose JSON over CSV for data storage?

## Mastery check
You can move on when you can:
- explain how `zip` pairs two lists element-by-element,
- implement type inference logic from memory,
- convert between objects and columnar JSON formats,
- describe edge cases in CSV parsing (quotes, escapes, encodings).

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../11-retry-loop-practice/README.md) | [Home](../../../README.md) | [Next →](../13-validation-rule-engine/README.md) |
|:---|:---:|---:|
