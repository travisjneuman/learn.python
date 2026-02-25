# Level 9 / Project 01 - Architecture Decision Log
Home: [README](../../../README.md)

## Focus
- Structured ADR (Architecture Decision Record) management
- Observer pattern for status change notifications
- ADR lifecycle: proposed, accepted, deprecated, superseded
- Full-text search across decision records
- JSON persistence and structured querying

## Why this project exists
Architecture decisions are the most expensive decisions in software engineering — yet
most teams make them informally and forget the reasoning within months. ADRs capture the
context, alternatives considered, and consequences of each decision. This project builds
a structured ADR system with status tracking, observer notifications, and search — teaching
documentation as a first-class engineering practice used at Spotify, AWS, and Google.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/01-architecture-decision-log
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "adr_count": 3,
  "statuses": {"accepted": 1, "proposed": 1, "superseded": 1},
  "search_results": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with ADR log summary
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `search_by_tag` method that filters ADRs by tag keywords.
2. Add an `export_markdown()` method that renders each ADR as a Markdown document.
3. Add a `--status` CLI filter that lists only ADRs in a given status (proposed, accepted, etc.).

## Break it (required)
1. Try to supersede an ADR that is already deprecated — what status transition occurs?
2. Register an observer callback that raises an exception — does the log still function?
3. Add two ADRs with the same ID — what happens to the internal dictionary?

## Fix it (required)
1. Add status transition validation (e.g. deprecated ADRs cannot be superseded).
2. Wrap observer callbacks in try/except so one bad observer does not break the log.
3. Add a check that rejects duplicate ADR IDs with a descriptive error.

## Explain it (teach-back)
1. What is an Architecture Decision Record (ADR) and why do teams write them?
2. How does the Observer pattern notify subscribers when an ADR changes status?
3. What is the ADR lifecycle: proposed, accepted, deprecated, superseded?
4. How would you integrate this log into a CI pipeline to enforce ADR review?

## Mastery check
You can move on when you can:
- explain the ADR lifecycle and why each status matters,
- add a new ADR end-to-end (create, accept, supersede) without looking at docs,
- describe the Observer pattern and how it decouples event producers from consumers,
- explain why decision records are important for long-lived software projects.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-domain-boundary-enforcer/README.md) |
|:---|:---:|---:|
