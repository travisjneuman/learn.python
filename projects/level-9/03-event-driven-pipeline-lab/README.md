# Level 9 / Project 03 - Event Driven Pipeline Lab
Home: [README](../../../README.md)

## Focus
- Event sourcing with append-only immutable event store
- Projections that materialize views from event streams
- Observer pattern for event subscriber notifications
- Temporal queries to reconstruct state at any point in time
- CQRS concepts: command and query separation

## Why this project exists
Traditional CRUD systems overwrite data — once a record changes, the previous state is
gone. Event sourcing preserves the full history by storing every state change as an
immutable event. You can replay events to rebuild any view, audit every change, and answer
"what did the system look like at 3pm last Tuesday?" This project builds an event store
with projections that materialize views from events — the foundational pattern behind
CQRS, audit trails, and financial ledger systems.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/03-event-driven-pipeline-lab
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "events_stored": 8,
  "projections": {"order_totals": {...}, "user_activity": {...}},
  "temporal_query": {...}
}
7 passed
```

## Expected artifacts
- Console JSON output with event store and projection data
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `replay_from(event_id)` method that re-emits events from a specific point in the log.
2. Add a new projection (e.g. `RevenueProjection`) that sums order totals by currency.
3. Add event versioning — include a `schema_version` field and handle version migration.

## Break it (required)
1. Append an event with a duplicate `event_id` — does the store reject it?
2. Subscribe a callback that modifies the event store during processing — what happens?
3. Query events with a time range where `start > end` — does `query_by_time_range` handle it?

## Fix it (required)
1. Add uniqueness validation on `event_id` in the event store.
2. Make event delivery use a snapshot of subscribers to avoid mutation during iteration.
3. Add a guard for invalid time ranges that returns an empty list.

## Explain it (teach-back)
1. What is event sourcing and how does it differ from traditional CRUD?
2. What is a projection and why do you rebuild state from events instead of storing it directly?
3. Why must events be immutable (frozen dataclass) in an event-sourced system?
4. How does temporal querying let you reconstruct system state at any point in time?

## Mastery check
You can move on when you can:
- explain event sourcing, CQRS, and projections with concrete examples,
- add a new event type and projection without modifying existing code,
- describe the tradeoff between event sourcing and traditional state management,
- explain why append-only logs enable temporal queries and audit trails.

## Mastery Check
- [ ] Can you explain the architectural trade-offs in your solution?
- [ ] Could you refactor this for a completely different use case?
- [ ] Can you identify at least two alternative approaches and explain why you chose yours?
- [ ] Could you debug this without print statements, using only breakpoint()?

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../02-domain-boundary-enforcer/README.md) | [Home](../../../README.md) | [Next →](../04-observability-slo-pack/README.md) |
|:---|:---:|---:|
