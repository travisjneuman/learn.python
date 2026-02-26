# Level 8 / Project 04 - Filter State Manager
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Immutable filter state with `frozen=True` dataclasses
- Command pattern for undo/redo state transitions
- Multi-operator filtering (equals, contains, greater-than, in)
- State serialization and search-text filtering
- Page-reset semantics when filters change

## Why this project exists
Dashboard and search UIs maintain complex filter states: date ranges, multi-select dropdowns,
text queries, sort orders. Users expect to undo a filter change instantly — yet the filter
itself must also apply correctly to data. This project builds a `FilterStateManager` with
undo/redo, immutable snapshots, and multi-operator filtering — the same state-management
pattern used in every non-trivial React, Vue, or Angular application.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/04-filter-state-manager
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "status": {"current_state": {...}, "undo_depth": 3, "redo_depth": 1},
  "filtered_results": [...],
  "filtered_count": 2
}
7 passed
```

## Expected artifacts
- Console JSON output showing filter state after undo/redo
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `clear_all()` method to `FilterState` that returns a blank state while preserving `page_size`.
2. Implement a `max_history` parameter in `FilterStateManager` that caps the undo stack size.
3. Add a `to_query_string()` method that serialises filter state as URL query parameters.

## Break it (required)
1. Call `undo()` when the undo stack is empty — does it raise `RuntimeError`?
2. Add a condition, undo, then add a different condition — verify the redo stack was cleared.
3. Create two `FilterState` objects and mutate a list inside `value` — does `frozen=True` protect deep objects?

## Fix it (required)
1. Add deep-copy protection so that list values inside `FilterCondition` cannot be mutated externally.
2. Add a `history_depth` limit that evicts the oldest undo entry when the cap is exceeded.
3. Add a test proving that `page` resets to 1 whenever a condition is added or removed.

## Explain it (teach-back)
1. Why does `FilterState` use `frozen=True` and tuples instead of mutable lists?
2. How does the command pattern (undo/redo stack) differ from event sourcing?
3. Why does adding a filter reset the page number to 1?
4. What is the difference between shallow and deep immutability, and why does it matter here?

## Mastery check
You can move on when you can:
- explain the command pattern and how undo/redo stacks work,
- add a new filter operator end-to-end without breaking existing tests,
- describe why immutable state snapshots prevent subtle UI bugs,
- implement undo/redo for any state-management scenario from scratch.

## Mastery Check
- [ ] Can you explain the architectural trade-offs in your solution?
- [ ] Could you refactor this for a completely different use case?
- [ ] Can you identify at least two alternative approaches and explain why you chose yours?
- [ ] Could you debug this without print statements, using only breakpoint()?

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Types Explained](../../../concepts/types-explained.md)
- [Quiz: Collections](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../03-pagination-stress-lab/README.md) | [Home](../../../README.md) | [Next →](../05-export-governance-check/README.md) |
|:---|:---:|---:|
