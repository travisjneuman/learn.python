# Level 7 / Project 09 - Contract Version Checker
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- payload version compatibility checks

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/09-contract-version-checker
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
1. Add a `"nullable"` attribute to ContractField so a field can be present but None.
2. Add a `backwards_compatible()` function that checks if new contract is safe to deploy.
3. Re-run script and tests — verify nullable fields and compatibility check work.

## Break it (required)
1. Pass a version string with only two parts (e.g. `"2.1"`) and watch `parse_version` crash.
2. Send a payload where a required field is present but set to `None`.
3. Observe the IndexError or false-positive validation pass.

## Fix it (required)
1. Pad missing version parts with zero (e.g. `"2.1"` becomes `"2.1.0"`).
2. Treat `None` values as missing for required fields in `validate_payload`.
3. Add tests for two-part versions and None-valued required fields.

## Explain it (teach-back)
1. Why is semantic versioning important for API contracts?
2. What happened when the version string had only two parts?
3. How did the padding fix prevent the IndexError?
4. How do real API platforms handle breaking vs non-breaking changes?

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
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../08-ingestion-observability-kit/README.md) | [Home](../../../README.md) | [Next →](../10-multi-source-reconciler/README.md) |
|:---|:---:|---:|
