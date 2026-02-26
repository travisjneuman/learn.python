# Level 2 / Project 14 - Anomaly Flagger
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/collections-explained.md) | **This project** | — | [Quiz](../../../concepts/quizzes/collections-explained-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | [Diagram](../../../concepts/diagrams/collections-explained.md) | [Browser](../../../browser/level-2.html) |

<!-- modality-hub-end -->

**Estimated time:** 45 minutes

## Focus
- threshold and outlier tagging

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/14-anomaly-flagger
python project.py data/sample_input.txt
python project.py data/sample_input.txt --z-threshold 3.0
python project.py data/sample_input.txt --iqr-factor 3.0
pytest -q
```

## Expected terminal output
```text
Dataset: 20 values, mean=52.85, std_dev=48.62
Anomalies found: 2
14 passed
```

## Expected artifacts
- Anomaly report on stdout
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--method` flag to use only z-score or only IQR detection.
2. Add a visual indicator (e.g. asterisks) showing where anomalies fall.
3. Output the "cleaned" dataset with anomalies removed.

## Break it (required) — Core
1. Feed a dataset with all identical values — does z-score divide by zero?
2. Feed a dataset with fewer than 4 values — does IQR work?
3. Feed a dataset with only 1 value — what stats are meaningful?

## Fix it (required) — Core
1. Guard against zero std_dev in z_score calculation.
2. Return empty anomalies list when dataset is too small for IQR.
3. Handle single-value datasets gracefully in statistics.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. What is a z-score and what does |z| > 2 mean practically?
2. How does the IQR method differ from z-score for skewed data?
3. Why might the same value be flagged by one method but not the other?
4. Where is anomaly detection used in real systems (monitoring, fraud, QA)?

## Mastery check
You can move on when you can:
- calculate mean and standard deviation by hand for a small dataset,
- explain when z-score fails (non-normal distributions),
- describe why IQR is more robust to outliers than mean-based methods,
- implement percentile calculation from scratch.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../13-validation-rule-engine/README.md) | [Home](../../../README.md) | [Next →](../15-level2-mini-capstone/README.md) |
|:---|:---:|---:|
