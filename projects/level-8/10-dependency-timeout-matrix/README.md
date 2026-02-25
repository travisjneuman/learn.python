# Level 8 / Project 10 - Dependency Timeout Matrix
Home: [README](../../../README.md)

## Focus
- Per-dependency timeout configuration with `concurrent.futures`
- Matrix-style testing across multiple timeout values
- Retry logic with configurable attempt counts
- Health status classification: healthy, degraded, timeout, error
- Optimal timeout analysis from matrix results

## Why this project exists
Microservice systems depend on many external services — authentication, databases, caches,
search indices, notification services — each with different latency profiles. Setting one
global timeout (e.g. 30 seconds) is either too generous for fast services or too aggressive
for slow ones. This project builds a dependency manager that tests per-service timeouts
across a matrix of values, identifies the minimum viable timeout for each dependency, and
recommends optimal settings — preventing the cascading failures that bring down entire
distributed systems.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/10-dependency-timeout-matrix
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "matrix": {"dependencies": [...], "matrix": [...]},
  "analysis": {"auth-service": {"min_passing_timeout": 0.05, ...}, ...}
}
7 passed
```

## Expected artifacts
- Console JSON output with timeout matrix and analysis
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--parallel` flag that checks all dependencies concurrently using `ThreadPoolExecutor`.
2. Add exponential backoff to the retry logic (instead of fixed-interval retries).
3. Add a `criticality` field to `DependencyConfig` and sort the matrix output by it.

## Break it (required)
1. Set `timeout_seconds=0` for a dependency — does the check handle instant timeouts?
2. Configure a dependency with `max_retries=-1` — does it retry forever?
3. Pass a `health_check` function that hangs indefinitely — does the timeout work?

## Fix it (required)
1. Validate that `timeout_seconds > 0` and `max_retries >= 0` in `DependencyConfig`.
2. Add a hard upper limit on retries to prevent infinite loops.
3. Add a test for the exponential backoff behavior.

## Explain it (teach-back)
1. Why do microservices need explicit timeout configuration for each dependency?
2. How does `ThreadPoolExecutor` enable concurrent timeout checks?
3. What is the difference between a connection timeout and a read timeout?
4. Why is a timeout matrix critical for understanding cascading failures?

## Mastery check
You can move on when you can:
- explain why every network call needs a timeout (and what happens without one),
- describe cascading failures and how timeouts prevent them,
- add a new dependency with custom health check and timeout without looking at docs,
- explain retry strategies: fixed, linear, exponential backoff, and jitter.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Collections Explained](../../../concepts/collections-explained.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../09-graceful-degradation-engine/README.md) | [Home](../../../README.md) | [Next →](../11-synthetic-monitor-runner/README.md) |
|:---|:---:|---:|
