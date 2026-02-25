# Level 7 / Project 11 - Pipeline Feature Flags
Home: [README](../../../README.md)

## Focus
- runtime toggles for safe rollout

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/11-pipeline-feature-flags
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
1. Add a `time_window` parameter so a flag is only active during specific hours (e.g. 09:00-17:00).
2. Add a `toggle()` method that flips a flag's enabled state and records it in the audit log.
3. Re-run script and tests — verify time-windowed flags and toggle work correctly.

## Break it (required)
1. Create a circular dependency (flag A requires B, flag B requires A) and observe infinite recursion.
2. Set `rollout_pct` to a value above 100 or below 0.
3. Capture the RecursionError or unexpected always-on behavior.

## Fix it (required)
1. Track visited flags during dependency resolution to detect and break circular references.
2. Clamp `rollout_pct` to the 0-100 range in the Flag constructor.
3. Add tests for circular dependencies and out-of-range rollout percentages.

## Explain it (teach-back)
1. Why are feature flags useful for deploying risky pipeline changes?
2. What caused the infinite recursion with circular dependencies?
3. How did the visited-set approach break the cycle?
4. How do real feature flag systems (LaunchDarkly, Unleash) handle rollout percentages?

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
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../10-multi-source-reconciler/README.md) | [Home](../../../README.md) | [Next →](../12-incident-mode-switch/README.md) |
|:---|:---:|---:|
