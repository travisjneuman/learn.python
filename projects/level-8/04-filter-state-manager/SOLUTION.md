# Solution: Level 8 / Project 04 - Filter State Manager

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Filter State Manager -- manage complex filter state with history and undo."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

class FilterOperator(Enum):
    EQUALS = "eq"
    NOT_EQUALS = "neq"
    GREATER_THAN = "gt"
    LESS_THAN = "lt"
    CONTAINS = "contains"
    IN = "in"


class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"


# WHY frozen=True? -- Filter conditions are stored in undo/redo history.
# If they were mutable, changing a condition after an undo would silently
# corrupt the history stack. Frozen dataclasses raise AttributeError on
# any mutation attempt, enforcing the Command pattern's rule that past
# states must remain untouched.
@dataclass(frozen=True)
class FilterCondition:
    field_name: str
    operator: FilterOperator
    value: Any

    def matches(self, record: dict[str, Any]) -> bool:
        actual = record.get(self.field_name)
        if actual is None:
            return False
        if self.operator == FilterOperator.EQUALS:
            return actual == self.value
        if self.operator == FilterOperator.NOT_EQUALS:
            return actual != self.value
        if self.operator == FilterOperator.GREATER_THAN:
            return actual > self.value
        if self.operator == FilterOperator.LESS_THAN:
            return actual < self.value
        if self.operator == FilterOperator.CONTAINS:
            # WHY case-insensitive? -- Text search in UIs is almost always
            # case-insensitive. Users type "urgent" and expect to find "Urgent".
            return str(self.value).lower() in str(actual).lower()
        if self.operator == FilterOperator.IN:
            return actual in self.value
        return False

    def to_dict(self) -> dict[str, Any]:
        return {"field": self.field_name, "operator": self.operator.value, "value": self.value}


@dataclass(frozen=True)
class SortSpec:
    field_name: str
    direction: SortDirection = SortDirection.ASC


# WHY frozen=True + tuple for conditions? -- FilterState is an immutable
# snapshot. Using tuple (not list) for conditions means the state is fully
# hashable and safely comparable. Every method returns a NEW FilterState
# instead of mutating, which is what makes undo/redo possible.
@dataclass(frozen=True)
class FilterState:
    conditions: tuple[FilterCondition, ...] = ()
    sort: SortSpec | None = None
    search_text: str = ""
    page: int = 1
    page_size: int = 25

    def add_condition(self, condition: FilterCondition) -> FilterState:
        # WHY page=1 on every filter change? -- Changing filters alters
        # the result set. Staying on page 5 after a filter change might
        # show an empty page because fewer results match. Resetting to
        # page 1 is the standard UX pattern.
        return FilterState(
            conditions=self.conditions + (condition,),
            sort=self.sort, search_text=self.search_text,
            page=1, page_size=self.page_size,
        )

    def remove_condition(self, field_name: str) -> FilterState:
        remaining = tuple(c for c in self.conditions if c.field_name != field_name)
        return FilterState(
            conditions=remaining, sort=self.sort,
            search_text=self.search_text, page=1, page_size=self.page_size,
        )

    def set_sort(self, sort: SortSpec | None) -> FilterState:
        return FilterState(
            conditions=self.conditions, sort=sort,
            search_text=self.search_text, page=1, page_size=self.page_size,
        )

    def set_search(self, text: str) -> FilterState:
        return FilterState(
            conditions=self.conditions, sort=self.sort,
            search_text=text, page=1, page_size=self.page_size,
        )

    def apply(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result = records
        # WHY text search first? -- Broad filters (text search) reduce
        # the dataset size early, making subsequent per-condition filtering faster.
        if self.search_text:
            query = self.search_text.lower()
            result = [r for r in result if any(query in str(v).lower() for v in r.values())]
        for cond in self.conditions:
            result = [r for r in result if cond.matches(r)]
        if self.sort:
            reverse = self.sort.direction == SortDirection.DESC
            result = sorted(result, key=lambda r: r.get(self.sort.field_name, ""), reverse=reverse)
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "conditions": [c.to_dict() for c in self.conditions],
            "sort": {"field": self.sort.field_name, "direction": self.sort.direction.value}
                   if self.sort else None,
            "search_text": self.search_text,
            "page": self.page, "page_size": self.page_size,
        }


# --- State manager with undo/redo --------------------------------------

class FilterStateManager:
    """WHY the Command pattern? -- Every state change pushes the previous
    state onto the undo stack. This gives full undo/redo without storing
    diffs or deltas. Since FilterState is immutable, we can safely hold
    references to past states without worrying about them being modified."""

    def __init__(self, initial: FilterState | None = None) -> None:
        self._current = initial or FilterState()
        self._undo_stack: list[FilterState] = []
        self._redo_stack: list[FilterState] = []

    @property
    def current(self) -> FilterState:
        return self._current

    @property
    def can_undo(self) -> bool:
        return len(self._undo_stack) > 0

    @property
    def can_redo(self) -> bool:
        return len(self._redo_stack) > 0

    @property
    def history_depth(self) -> int:
        return len(self._undo_stack)

    def apply_state(self, new_state: FilterState) -> None:
        self._undo_stack.append(self._current)
        self._current = new_state
        # WHY clear redo stack? -- A new action after an undo creates a
        # new timeline branch. The old redo history is no longer reachable,
        # same as how text editors behave.
        self._redo_stack.clear()

    def undo(self) -> FilterState:
        if not self.can_undo:
            raise RuntimeError("Nothing to undo")
        self._redo_stack.append(self._current)
        self._current = self._undo_stack.pop()
        return self._current

    def redo(self) -> FilterState:
        if not self.can_redo:
            raise RuntimeError("Nothing to redo")
        self._undo_stack.append(self._current)
        self._current = self._redo_stack.pop()
        return self._current

    def reset(self) -> FilterState:
        self.apply_state(FilterState())
        return self._current

    def status(self) -> dict[str, Any]:
        return {
            "current_state": self._current.to_dict(),
            "undo_depth": len(self._undo_stack),
            "redo_depth": len(self._redo_stack),
        }


# --- CLI demo -----------------------------------------------------------

def run_demo() -> dict[str, Any]:
    manager = FilterStateManager()
    state = manager.current
    state = state.add_condition(FilterCondition("status", FilterOperator.EQUALS, "active"))
    manager.apply_state(state)
    state = state.add_condition(FilterCondition("priority", FilterOperator.GREATER_THAN, 3))
    manager.apply_state(state)
    state = state.set_sort(SortSpec("created_at", SortDirection.DESC))
    manager.apply_state(state)
    state = state.set_search("urgent")
    manager.apply_state(state)
    manager.undo()
    manager.undo()
    manager.redo()

    sample_data = [
        {"id": 1, "status": "active", "priority": 5, "title": "urgent fix"},
        {"id": 2, "status": "active", "priority": 2, "title": "minor update"},
        {"id": 3, "status": "closed", "priority": 8, "title": "urgent patch"},
        {"id": 4, "status": "active", "priority": 7, "title": "feature request"},
    ]
    filtered = manager.current.apply(sample_data)
    return {
        "status": manager.status(),
        "filtered_results": filtered,
        "filtered_count": len(filtered),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Filter state manager with undo/redo")
    parser.add_argument("--demo", action="store_true", default=True)
    parser.parse_args(argv)
    print(json.dumps(run_demo(), indent=2, default=str))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Frozen dataclasses for state | Immutability prevents history corruption; every change creates a new snapshot | Mutable state with deep copy -- works but relies on discipline; one missed copy corrupts history |
| Tuple for conditions (not list) | Tuples are hashable and immutable, matching the frozen dataclass contract | Frozenset -- loses insertion order, which matters for filter display |
| Page resets to 1 on every filter change | Prevents showing an empty page when the result set shrinks | Keep current page -- confusing UX when filters eliminate all results on that page |
| Redo stack cleared on new action | Standard UX: a new action after undo starts a new timeline | Keep redo history -- creates a confusing tree-shaped undo model |

## Alternative approaches

### Approach B: Event-sourced filter state

```python
@dataclass
class FilterEvent:
    action: str  # "add_condition", "remove_condition", "set_sort", etc.
    payload: dict[str, Any]
    timestamp: float

class EventSourcedFilterManager:
    def __init__(self):
        self._events: list[FilterEvent] = []
        self._cursor = 0  # current position in event log

    def apply(self, action: str, payload: dict) -> FilterState:
        self._events = self._events[:self._cursor]  # truncate future
        self._events.append(FilterEvent(action, payload, time.time()))
        self._cursor += 1
        return self._replay()

    def undo(self) -> FilterState:
        self._cursor = max(0, self._cursor - 1)
        return self._replay()

    def _replay(self) -> FilterState:
        """Rebuild state by replaying events up to cursor."""
        state = FilterState()
        for event in self._events[:self._cursor]:
            state = self._apply_event(state, event)
        return state
```

**Trade-off:** Event sourcing stores the actions that led to the current state rather than snapshots. It uses less memory (events are small) and gives a full audit trail, but replay cost grows linearly with history length. Use it when you need audit logging or when states are very large.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Mutating a list inside FilterCondition.value | `frozen=True` only protects attribute assignment; list contents can still change | Deep-copy values on construction, or document that values must be immutable |
| Calling undo() on an empty stack | RuntimeError -- correct, but the UI should check `can_undo` first | Expose `can_undo` / `can_redo` properties for the UI to disable buttons |
| Undo, then new action, then redo | Redo stack is cleared -- the old redo states are gone forever | This is intentional (standard behaviour), but users may be surprised |
