# Level 8 / Project 08 - Fault Injection Harness
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Configurable fault injection with decorator and context manager APIs
- Fault types: exception, delay, timeout, data corruption
- Probability-based triggering with seeded RNG for reproducibility
- Scoped fault injection with automatic cleanup
- Statistics tracking: trigger rates, events, interception counts

## Why this project exists
Netflix's Chaos Monkey proved that injecting failures proactively builds more resilient
systems. Error-handling code paths are the least tested in most codebases — they only run
during real outages when stakes are highest. This project creates a configurable fault
injection framework that can introduce exceptions, delays, and data corruption into any
function call, teaching how to test the code paths that rarely execute in normal operation.
This is the foundation of chaos engineering.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/08-fault-injection-harness
python project.py --seed 42
pytest -q
```

## Expected terminal output
```text
{
  "stats": {"calls_intercepted": 40, "faults_triggered": 10, ...},
  "results_sample": [...],
  "corruption_demo": {"original": {...}, "corrupted": {...}}
}
7 passed
```

## Expected artifacts
- Console JSON output showing fault injection stats and corruption demo
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `FaultType.DATA_CORRUPTION` type that calls `corrupt_data` automatically on function return values.
2. Add a `max_triggers` field to `FaultConfig` that limits how many times a rule can fire.
3. Add a `--report` flag that outputs all `FaultEvent` entries as a JSON summary.

## Break it (required)
1. Set `probability` to a value > 1.0 — does `FaultConfig` validation catch it?
2. Use the `scope()` context manager and raise inside it — are temporary rules still cleaned up?
3. Apply the `@inject` decorator to a function that takes `**kwargs` — does `func.__name__` survive?

## Fix it (required)
1. Ensure `scope()` uses a `try/finally` so rules are removed even on exceptions.
2. Use `functools.wraps` in the `inject` decorator to preserve function metadata.
3. Add a test that verifies `max_triggers` stops injection after the limit.

## Explain it (teach-back)
1. What is fault injection and why do teams use it in production (chaos engineering)?
2. How does the `@contextmanager` decorator turn a generator into a context manager?
3. Why does `corrupt_data` check `isinstance(value, bool)` before `isinstance(value, (int, float))`?
4. How would you extend this to inject network-level faults (e.g. packet loss)?

## Mastery check
You can move on when you can:
- explain why `bool` must be checked before `int` in Python's type hierarchy,
- add a new fault type end-to-end (config + injection + test),
- describe the difference between chaos engineering and traditional testing,
- explain how probability-based injection helps find intermittent bugs.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../07-concurrency-queue-simulator/README.md) | [Home](../../../README.md) | [Next →](../09-graceful-degradation-engine/README.md) |
|:---|:---:|---:|
