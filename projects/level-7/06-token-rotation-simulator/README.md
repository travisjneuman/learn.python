# Level 7 / Project 06 - Token Rotation Simulator
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- credential lifecycle simulation

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/06-token-rotation-simulator
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
1. Add a `grace_period` parameter so old tokens remain valid for N seconds after rotation.
2. Add a `list_active()` method that returns all non-revoked, non-expired tokens.
3. Re-run script and tests — verify grace period and listing work correctly.

## Break it (required)
1. Call `rotate()` when no token has been generated yet (empty manager).
2. Set `ttl_seconds` to 0 so tokens expire immediately upon creation.
3. Observe that `is_valid` returns False for brand-new tokens.

## Fix it (required)
1. Have `rotate()` call `generate()` if no current token exists instead of crashing.
2. Validate that `ttl_seconds > 0` in the TokenManager constructor.
3. Add tests for rotating with no current token and for zero-TTL edge case.

## Explain it (teach-back)
1. Why is token rotation important for API security?
2. What happened when rotate was called without an existing token?
3. How did the constructor validation prevent zero-TTL tokens?
4. How does the audit trail help in a real security incident investigation?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../05-polling-cadence-manager/README.md) | [Home](../../../README.md) | [Next →](../07-stale-data-detector/README.md) |
|:---|:---:|---:|
