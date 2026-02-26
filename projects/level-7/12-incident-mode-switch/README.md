# Level 7 / Project 12 - Incident Mode Switch
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- degraded mode controls during incidents

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/12-incident-mode-switch
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
... output_summary.json written ...
2 passed
```

## Expected artifacts
- `data/output_summary.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add an `auto_recover` feature: if all active stages succeed, automatically transition back to normal.
2. Add a `duration()` method to IncidentEvent that calculates how long the system stayed in each mode.
3. Re-run script and tests — verify auto-recovery and duration tracking work.

## Break it (required)
1. Attempt an invalid transition (e.g. maintenance to degraded) and observe the rejection.
2. Pass an unknown mode string (e.g. `"panic"`) and watch the ValueError from the Enum.
3. Capture the error and confirm the system stays in its previous valid mode.

## Fix it (required)
1. Wrap the `Mode(target)` conversion in a try/except to handle unknown mode strings gracefully.
2. Return a clear error message listing valid modes when an invalid one is provided.
3. Add tests for unknown mode strings and all invalid transition paths.

## Explain it (teach-back)
1. Why does limiting mode transitions prevent accidental state corruption?
2. What happened when an invalid mode string was passed?
3. How did the try/except with a helpful message improve operability?
4. How do real incident management systems (PagerDuty, OpsGenie) model severity levels?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../11-pipeline-feature-flags/README.md) | [Home](../../../README.md) | [Next →](../13-service-account-policy-check/README.md) |
|:---|:---:|---:|
