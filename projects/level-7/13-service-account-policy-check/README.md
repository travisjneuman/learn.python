# Level 7 / Project 13 - Service Account Policy Check
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- account usage compliance checks

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/13-service-account-policy-check
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
1. Add an `"inactive_days"` rule that flags accounts not used within N days.
2. Add a `remediation_suggestion` field to each Violation (e.g. "rotate key" or "reduce permissions").
3. Re-run script and tests — verify new rule and suggestions appear in the compliance report.

## Break it (required)
1. Provide a naming pattern with invalid regex syntax (e.g. `"[invalid"`) and observe the crash.
2. Set `key_created_at` to a timestamp in the far future and see negative key age.
3. Capture the `re.error` or confusing "key is -100 days old" message.

## Fix it (required)
1. Wrap `re.match()` in a try/except for `re.error` and report "invalid pattern" as a violation.
2. Clamp negative key ages to zero (future timestamps mean "just rotated").
3. Add tests for invalid regex patterns and future key timestamps.

## Explain it (teach-back)
1. Why is least-privilege important for service accounts?
2. What happened when the regex pattern was malformed?
3. How did the try/except prevent a full pipeline crash on one bad rule?
4. How do real cloud platforms (AWS IAM, GCP) enforce service account policies?

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

| [← Prev](../12-incident-mode-switch/README.md) | [Home](../../../README.md) | [Next →](../14-cache-backfill-runner/README.md) |
|:---|:---:|---:|
