# Level 4 / Project 02 - Excel Input Health Check
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-4.html) |

<!-- modality-hub-end -->

**Estimated time:** 45 minutes

## Focus
- tabular input quality scoring

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/02-excel-input-health-check
python project.py --input data/sample_input.csv --output data/health_report.json
pytest -q
```

## Expected terminal output
```text
{
  "file": "data/sample_input.csv",
  "status": "WARN",
  "headers": { ... },
  "completeness": { "short_rows": [6], ... }
}
6 passed
```

## Expected artifacts
- `data/health_report.json` — structured quality report
- Passing tests
- Updated `notes.md`

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a function that scores the quality of a list of records based on completeness.

**Step 1: Define what "quality" means.** Count how many fields are empty or missing in each record.

```python
def score_completeness(records, required_fields):
    total_checks = len(records) * len(required_fields)
    if total_checks == 0:
        return {"score": 1.0, "missing": []}

    missing = []
    for i, record in enumerate(records):
        for field in required_fields:
            value = record.get(field, "")
            if not str(value).strip():
                missing.append({"row": i, "field": field})

    score = 1.0 - (len(missing) / total_checks)
    return {"score": round(score, 3), "missing": missing}
```

**Step 2: Interpret the score.** 1.0 means every field is filled. 0.5 means half are missing. 0.0 means everything is empty.

**Step 3: Add thresholds.** `PASS` if score >= 0.95, `WARN` if >= 0.8, `FAIL` otherwise.

**The thought process:** Define measurable quality criteria. Score them numerically. Set thresholds for actionable categories. This is the same pattern the health check project uses.

## Design First
Before writing code, sketch your approach in `notes.md`:
- What functions or classes do you need?
- What data structures will you use?
- What's the flow from input to output?
- What could go wrong?

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. What additional quality check would catch problems the current tool misses?
2. Can you make the tool support more than one input format?
3. Write a test to verify your new check works.

## Break it (required) — Core
1. Create messy input data — what quality issues does the tool miss?
2. What happens with files that use unexpected encodings?
3. Try extreme cases (huge headers, wildly inconsistent rows) — where does it struggle?

## Fix it (required) — Core
1. Add a safeguard so the report stays manageable even with very messy input.
2. Handle the encoding issue you discovered.
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `detect_delimiter` use the *minimum* count across rows instead of the *average*?
2. What is the difference between `check_headers` and `check_row_completeness` — could they be merged?
3. Why does the health check return early when encoding fails instead of continuing?
4. How would you extend this to support Excel `.xlsx` files?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Excel Input Health Check. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to detect whether a CSV uses commas or tabs as delimiters. Can you explain `csv.Sniffer` with a simple example?"
- "Can you explain how to calculate a completeness score for tabular data?"

---

| [← Prev](../01-schema-validator-engine/README.md) | [Home](../../../README.md) | [Next →](../03-robust-csv-ingestor/README.md) |
|:---|:---:|---:|
