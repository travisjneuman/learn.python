# Level 8 / Project 14 - User Journey Tracer
Home: [README](../../../README.md)

## Focus
- Event stream processing and session reconstruction
- Session splitting by inactivity timeout gaps
- Funnel analysis with stage-to-stage conversion rates
- Drop-off detection to identify UX bottlenecks
- Group-by aggregation patterns for analytics

## Why this project exists
Understanding how users flow through a system is essential for debugging, optimization,
and product analytics. Why do 40% of users abandon checkout at the payment step? Where
do new users get stuck during onboarding? This project builds a journey tracer that
reconstructs user sessions from raw event streams, identifies drop-off points, and
computes conversion funnels — the same pattern used by Amplitude, Mixpanel, and
custom product analytics systems.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/14-user-journey-tracer
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "journeys_count": 5,
  "funnel": {"stages": [...], "conversion_rates": [...]},
  "drop_off_points": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with journey analysis and funnel data
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `session_timeout_minutes` parameter to `reconstruct_journeys` that splits sessions by inactivity.
2. Add drop-off analysis: for each funnel stage, report what percentage of users left.
3. Add a `--user` filter flag that traces only a specific user's journeys.

## Break it (required)
1. Pass events with unsorted timestamps — does `reconstruct_journeys` produce correct sessions?
2. Create a funnel with stages not present in any events — what does `analyze_funnel` return?
3. Pass an empty event list — does the journey reconstruction handle it gracefully?

## Fix it (required)
1. Sort events by timestamp inside `reconstruct_journeys` before grouping.
2. Return 0% conversion for funnel stages with no matching events.
3. Add a test for empty input and unsorted timestamps.

## Explain it (teach-back)
1. What is a user journey and how does event-based tracing reconstruct it?
2. How does funnel analysis measure conversion between stages?
3. Why does session splitting use a timeout gap between events?
4. How do analytics platforms like Amplitude or Mixpanel implement similar journey tracing?

## Mastery check
You can move on when you can:
- explain user journeys, sessions, and funnel analysis with examples,
- add a new funnel stage and trace it through real event data,
- describe the difference between session-based and user-based analytics,
- explain how drop-off rates help identify UX problems in a product.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../13-sla-breach-detector/README.md) | [Home](../../../README.md) | [Next →](../15-level8-mini-capstone/README.md) |
|:---|:---:|---:|
