# Level 9 / Project 06 - Reliability Scorecard
Home: [README](../../../README.md)

## Focus
- Weighted multi-criteria scoring across reliability dimensions
- Score normalization to a 0-100 scale for different metric types
- Letter grading (A/B/C/D/F) for non-technical stakeholder communication
- Trend analysis comparing current vs previous scoring periods
- Strategy pattern for dimension-specific scoring functions

## Why this project exists
Reliability is multi-dimensional: uptime, mean time to recovery (MTTR), change failure
rate, deployment frequency, and incident response all contribute. A service with 99.99%
uptime but 8-hour MTTR is not truly reliable. This project builds a weighted scorecard
that evaluates reliability across these dimensions, normalizes different units to a
comparable scale, assigns letter grades, and generates improvement recommendations — the
same framework SRE teams use to compare service reliability across an organization.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/06-reliability-scorecard
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "service": "checkout-api",
  "overall_score": 78.5,
  "grade": "B",
  "dimensions": [...],
  "recommendations": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with reliability scorecard
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `trend` field to `DimensionScore` that compares current vs previous period scores.
2. Add a normalizer for boolean metrics (e.g. "has runbook" -> 100 or 0).
3. Add a `--compare` flag that shows side-by-side scores for two services.

## Break it (required)
1. Set all dimension weights to 0 — does the weighted score calculation handle it?
2. Pass a raw value outside the normalizer's expected range (e.g. negative uptime) — what score results?
3. Create a scorecard with zero dimensions — does grading still work?

## Fix it (required)
1. Validate that total weight is > 0 before computing the weighted average.
2. Clamp normalized values to the 0-100 range.
3. Return a default "unscored" grade when there are no dimensions.

## Explain it (teach-back)
1. What is a reliability scorecard and how do SRE teams use them?
2. How does weighted scoring prioritize some dimensions over others?
3. Why is score normalization needed — what problem does it solve?
4. How do letter grades (A/B/C/D/F) help communicate reliability status to non-technical stakeholders?

## Mastery check
You can move on when you can:
- explain weighted scoring and why different reliability dimensions have different weights,
- add a new dimension (e.g. "deployment frequency") with its own normalizer,
- describe how normalization converts different units to a comparable 0-100 scale,
- design a reliability scorecard for a real service with appropriate dimensions and weights.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../05-capacity-planning-model/README.md) | [Home](../../../README.md) | [Next →](../07-canary-rollout-simulator/README.md) |
|:---|:---:|---:|
