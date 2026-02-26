# Level 8 / Project 06 - Response Time Profiler
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Context managers and decorators for timing code blocks
- Percentile calculation (p50, p90, p95, p99) with linear interpolation
- Statistical profiling: mean, median, standard deviation
- Bottleneck identification across multiple profiled functions
- `time.perf_counter()` for high-resolution measurements

## Why this project exists
Understanding where time is spent is essential for optimization. A function that runs
in 2ms on average but 200ms at p99 causes intermittent user-visible slowdowns that are
invisible to mean-based monitoring. This project builds a profiling toolkit that measures
function execution times, computes percentile distributions, and identifies bottlenecks —
the same approach used by APM tools like New Relic, Datadog, and Jaeger.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/06-response-time-profiler
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "profiles": [
    {"function": "fast_operation", "calls": 20, "mean_ms": ..., "p99_ms": ...},
    ...
  ],
  "bottleneck": {"function": "slow_operation", ...}
}
7 passed
```

## Expected artifacts
- Console JSON output with profiling reports
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `reset()` method to `ResponseTimeProfiler` that clears all recorded timings.
2. Change `report()` to include a `slowest_operations` list (top 3 by p99).
3. Add a `@profile` class method that works as a decorator without needing an instance reference.

## Break it (required)
1. Call `report()` with no recorded timings — does `percentile()` handle an empty list?
2. Record a negative duration (simulate a clock skew) — what happens to the percentile calculations?
3. Use the context manager but raise an exception inside it — does the timing still get recorded?

## Fix it (required)
1. Add a guard in `percentile()` that returns 0.0 for empty data.
2. Validate that recorded durations are non-negative.
3. Add a test that the context manager records timing even when the block raises.

## Explain it (teach-back)
1. How does `time.perf_counter()` differ from `time.time()` and why is it better for profiling?
2. What is the p95 vs p99 percentile and why do production systems track both?
3. How does the `@profile_function` decorator preserve the original function's name?
4. Why is a context manager useful for profiling blocks of code that aren't single functions?

## Mastery check
You can move on when you can:
- explain the difference between mean, median, p95, and p99 response times,
- profile a real function and interpret the report output,
- describe when p99 matters more than average (tail latency),
- add a new profiling metric (e.g. throughput) without modifying existing code.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../05-export-governance-check/README.md) | [Home](../../../README.md) | [Next →](../07-concurrency-queue-simulator/README.md) |
|:---|:---:|---:|
