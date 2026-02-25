# Level 8 / Project 09 - Graceful Degradation Engine
Home: [README](../../../README.md)

## Focus
- Circuit breaker pattern: closed, open, half-open state machine
- Sliding window error-rate calculation with `collections.deque`
- Service tier degradation: full, reduced, minimal, offline
- Feature flags tied to degradation tiers
- Recovery testing with half-open state and request limits

## Why this project exists
Production systems must degrade gracefully rather than fail completely. When a database
slows down, the right response is not a 500 error page — it is disabling non-essential
features (search, recommendations, exports) while keeping core functionality alive. This
project implements a circuit-breaker-style degradation engine that monitors error rates
and progressively reduces service quality — the same pattern used by Netflix, AWS, and
every major cloud platform to maintain availability during partial outages.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/09-graceful-degradation-engine
python project.py --window 20
pytest -q
```

## Expected terminal output
```text
{
  "final_status": {"circuit_state": "closed", "service_tier": "full", ...},
  "timeline": [
    {"step": 0, "circuit_state": "closed", "service_tier": "full", ...},
    ...
  ]
}
7 passed
```

## Expected artifacts
- Console JSON output with degradation timeline
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `HALF_OPEN` state to the circuit breaker that lets a single request through to test recovery.
2. Add a `recovery_time_seconds` parameter that controls how long the circuit stays open before testing.
3. Add per-tier feature lists (e.g. tier DEGRADED disables search but keeps core reads).

## Break it (required)
1. Set `failure_threshold=0` — does the engine immediately open the circuit?
2. Record successes rapidly after failures — does the sliding window correctly age out old entries?
3. Set `window_size=0` on `SlidingWindowTracker` — what happens to error rate calculation?

## Fix it (required)
1. Validate that `failure_threshold > 0` and `window_size > 0` in `__init__`.
2. Add a guard for division by zero in error rate calculation when the window is empty.
3. Add a test for the HALF_OPEN to CLOSED recovery transition.

## Explain it (teach-back)
1. What is the circuit breaker pattern and how does it differ from simple retry logic?
2. How does the sliding window tracker calculate error rate and why is it time-based?
3. What are service tiers (FULL, DEGRADED, MINIMAL) and how do real systems use them?
4. Why is graceful degradation preferable to a complete outage?

## Mastery check
You can move on when you can:
- draw the state machine for CLOSED to OPEN to HALF_OPEN to CLOSED,
- explain why sliding windows are better than cumulative counters for error rates,
- describe a real-world degradation scenario (e.g. Netflix disabling recommendations),
- add a new tier with specific feature restrictions without modifying existing tiers.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../08-fault-injection-harness/README.md) | [Home](../../../README.md) | [Next →](../10-dependency-timeout-matrix/README.md) |
|:---|:---:|---:|
