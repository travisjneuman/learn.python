# Level 2 / Project 15 - Level 2 Mini Capstone
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/collections-explained.md) | **This project** | [Walkthrough](./WALKTHROUGH.md) | [Quiz](../../../concepts/quizzes/collections-explained-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | [Diagram](../../../concepts/diagrams/collections-explained.md) | [Browser](../../../browser/level-2.html) |

<!-- modality-hub-end -->

**Estimated time:** 45 minutes

## Focus
- small end-to-end validated pipeline

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/15-level2-mini-capstone
python project.py data/sample_input.txt
python project.py data/sample_input.txt --numeric-field salary --threshold 2.0
python project.py data/sample_input.txt --json
pytest -q
```

## Expected terminal output
```text
============================================================
  DATA PIPELINE REPORT
============================================================
Records loaded:    12
Records valid:     10
Records invalid:   2
Anomalies found:   1
10 passed
```

## Expected artifacts
- Pipeline report on stdout
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--rules` flag to load validation rules from a separate JSON file.
2. Add an `--output` flag to save valid records as a new CSV.
3. Add deduplication as a pipeline stage between cleaning and validation.

## Break it (required) — Core
1. Feed a CSV where every record is invalid — does the report handle 0% pass rate?
2. Feed a CSV with no numeric column — does anomaly detection crash?
3. Feed an empty CSV (header only) — does the pipeline handle zero records?

## Fix it (required) — Core
1. Guard against zero-record pass rate calculations.
2. Handle missing numeric fields in anomaly detection gracefully.
3. Add a test for empty/header-only CSV files.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. How do the five pipeline stages (load, clean, validate, analyse, report) connect?
2. Why is each stage a separate function instead of one big function?
3. What Level 2 skills did you combine in this capstone?
4. How would you extend this pipeline for a real data processing job?

## Mastery check
You can move on when you can:
- describe all 5 pipeline stages and what each does,
- add a new pipeline stage without modifying existing ones,
- explain how data flows from raw CSV to final report,
- identify which earlier Level 2 project each stage came from.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Virtual Environments](../../../concepts/virtual-environments.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../14-anomaly-flagger/README.md) | [Home](../../../README.md) | [Next →](../16-markdown-to-html-converter/README.md) |
|:---|:---:|---:|
