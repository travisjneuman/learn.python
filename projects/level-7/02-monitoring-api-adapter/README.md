# Level 7 / Project 02 - Monitoring API Adapter
Home: [README](../../../README.md)

## Focus
- api call abstraction and result normalization

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/02-monitoring-api-adapter
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
Extend this project in a meaningful way — add a feature that addresses a real use case.

## Break it (required)
Introduce a subtle bug and see if your tests catch it. If they don't, write a test that would.

## Fix it (required)
Review your code critically — is there a design pattern that would improve it?

## Explain it (teach-back)
Could you explain the architectural trade-offs to a colleague?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

## Mastery Check
- [ ] Can you explain the architectural trade-offs in your solution?
- [ ] Could you refactor this for a completely different use case?
- [ ] Can you identify at least two alternative approaches and explain why you chose yours?
- [ ] Could you debug this without print statements, using only breakpoint()?

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../01-api-query-adapter/README.md) | [Home](../../../README.md) | [Next →](../03-unified-cache-writer/README.md) |
|:---|:---:|---:|
