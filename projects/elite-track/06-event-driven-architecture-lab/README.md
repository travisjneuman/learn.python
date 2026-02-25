# Elite Track / Event Driven Architecture Lab
Home: [README](../../../README.md)

## Focus
- elite systems engineering practice with explicit evidence and tradeoffs

## Why this project exists
Simulate event contracts, ordering, idempotency, and replay safety.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/elite-track/06-event-driven-architecture-lab
python project.py --input data/sample_input.txt --output data/output_summary.json --run-id smoke-check
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
1. Add one resilience improvement.
2. Add one observability improvement.
3. Re-run script and tests.

## Break it (required)
1. Remove or corrupt one input line.
2. Confirm behavior fails safely.
3. Capture error and root cause.

## Fix it (required)
1. Add guard/validation logic.
2. Add or update tests.
3. Re-run until deterministic and passing.

## Explain it (teach-back)
1. What tradeoff did you make and why?
2. What failure mode mattered most?
3. How would this design scale in production?

## Mastery check
You can move on when you can:
- explain architecture and failure boundaries,
- run and validate output without docs,
- defend one design tradeoff with evidence.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../05-performance-profiler-workbench/README.md) | [Home](../../../README.md) | [Next →](../07-observability-slo-platform/README.md) |
|:---|:---:|---:|
