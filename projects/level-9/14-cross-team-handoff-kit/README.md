# Level 9 / Project 14 - Cross Team Handoff Kit
Home: [README](../../../README.md)

## Focus
- Builder pattern for multi-section document construction
- Completeness scoring heuristics for handoff quality
- Structured sections: architecture, operations, known issues, contacts, runbooks
- Validation for required fields and section completeness
- Template-based text generation for consistent formatting

## Why this project exists
When ownership of a service transfers between teams, critical context gets lost. The new
team discovers undocumented failure modes at 2am during an outage. A well-structured
handoff captures architecture, operational knowledge, known issues, on-call contacts, and
runbooks in a format that a receiving team can actually use. This project builds a handoff
document generator with completeness scoring that incentivizes thorough documentation —
the same structured approach used by platform teams at companies with frequent
organizational changes.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/14-cross-team-handoff-kit
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "service": "payment-api",
  "completeness_score": 92,
  "sections_filled": 5,
  "sections_total": 6,
  "checklist": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with handoff document and completeness score
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `render_markdown()` method that outputs the handoff document as formatted Markdown.
2. Add a `risk_assessment` section that flags critical known issues and untested runbooks.
3. Add a `--checklist` flag that outputs just the transition checklist as a printable list.

## Break it (required)
1. Build a document with no `ServiceOverview.purpose` — how does completeness scoring respond?
2. Add a runbook with empty steps list — does the checklist still mark it as testable?
3. Create a contact with no email — does the serialization handle optional fields?

## Fix it (required)
1. Validate that `ServiceOverview.purpose` is non-empty (warn if blank).
2. Add validation that runbooks must have at least one step.
3. Add a test for the completeness score with partial sections filled.

## Explain it (teach-back)
1. Why are structured handoffs critical when service ownership transfers between teams?
2. How does the builder pattern make document construction flexible and readable?
3. What does completeness scoring incentivize — why not just a simple checklist?
4. How would you integrate this into an organization's service catalog or wiki?

## Mastery check
You can move on when you can:
- explain the builder pattern and why it suits multi-section document construction,
- build a complete handoff document using the fluent API and achieve 90%+ completeness,
- describe what information is most critical during a service ownership transition,
- add a new section (e.g. disaster recovery) to the handoff kit.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Collections Explained](../../../concepts/collections-explained.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../13-platform-cost-estimator/README.md) | [Home](../../../README.md) | [Next →](../15-level9-mini-capstone/README.md) |
|:---|:---:|---:|
