# Level 9 / Project 12 - Incident Postmortem Generator
Home: [README](../../../README.md)

## Focus
- Builder pattern for structured document assembly
- Blameless postmortem structure: summary, timeline, root cause, actions
- Severity classification based on impact metrics
- Quality scoring heuristics for postmortem completeness
- Action item tracking with owners and due dates

## Why this project exists
Blameless postmortems are essential for learning from failures — yet most teams skip
them or produce low-quality reports that gather dust. The difference between a useful
postmortem and a useless one is structure: a clear timeline, honest root cause analysis,
and actionable follow-ups with owners. This project takes raw incident data and generates
a structured postmortem document with severity classification, quality scoring, and action
item tracking — teaching the systematic approach to incident learning used by Google,
Etsy, and every mature SRE organization.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/12-incident-postmortem-generator
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "incident_id": "INC-2025-042",
  "severity": "SEV1",
  "quality_score": 85,
  "sections": ["summary", "timeline", "root_cause", "actions"],
  "action_items": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with postmortem document and quality score
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `render_markdown()` method that outputs the postmortem as a formatted Markdown document.
2. Add action item due-date validation — flag overdue items in the report.
3. Add a `--template` flag that uses a custom section ordering.

## Break it (required)
1. Generate a postmortem with no timeline entries — does the timeline section handle it?
2. Create an `ImpactSummary` with negative `affected_users` — does the severity score handle it?
3. Pass action items with empty `owner` fields — how does the quality score respond?

## Fix it (required)
1. Validate that `affected_users >= 0` and `duration_minutes >= 0` in `ImpactSummary`.
2. Show a "no timeline recorded" message instead of an empty section.
3. Add a test that verifies quality score penalizes missing action item owners.

## Explain it (teach-back)
1. What is a blameless postmortem and why is the "blameless" part important?
2. How does the quality scoring heuristic incentivize thorough documentation?
3. Why are contributing factors separate from root cause?
4. How do organizations like Google use postmortems to prevent recurring incidents?

## Mastery check
You can move on when you can:
- explain the structure of a blameless postmortem (summary, timeline, root cause, actions),
- generate a complete postmortem from raw incident data and interpret the quality score,
- describe why action items with owners and due dates are critical for follow-through,
- add a new section (e.g. customer communication) to the generator.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../11-recovery-time-estimator/README.md) | [Home](../../../README.md) | [Next →](../13-platform-cost-estimator/README.md) |
|:---|:---:|---:|
