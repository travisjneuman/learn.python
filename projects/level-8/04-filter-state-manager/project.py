"""Filter State Manager — manage complex filter state with history and undo.

Design rationale:
    Dashboard and search UIs maintain complex filter states: date ranges,
    multi-select dropdowns, text queries, sort orders. This project builds
    a filter state manager with undo/redo, serialization, and conflict
    detection — patterns used in every non-trivial frontend application.

Concepts practised:
    - dataclasses with frozen=True for immutable snapshots
    - command pattern (undo/redo stack)
    - deep copy for state isolation
    - JSON serialization of filter state
    - type-safe filter operations
"""

from __future__ import annotations

import argparse
import copy
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

class FilterOperator(Enum):
    """Comparison operators for filter conditions."""
    EQUALS = "eq"
    NOT_EQUALS = "neq"
    GREATER_THAN = "gt"
    LESS_THAN = "lt"
    CONTAINS = "contains"
    IN = "in"


class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass(frozen=True)
class FilterCondition:
    """A single filter condition — immutable for safe history tracking."""
    field_name: str
    operator: FilterOperator
    value: Any

    def matches(self, record: dict[str, Any]) -> bool:
        """Test whether a record satisfies this condition."""
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
            return str(self.value).lower() in str(actual).lower()
        if self.operator == FilterOperator.IN:
            return actual in self.value
        return False

    def to_dict(self) -> dict[str, Any]:
        return {
            "field": self.field_name,
            "operator": self.operator.value,
            "value": self.value,
        }


@dataclass(frozen=True)
class SortSpec:
    """Sort specification."""
    field_name: str
    direction: SortDirection = SortDirection.ASC


@dataclass(frozen=True)
class FilterState:
    """Complete immutable snapshot of all active filters and sort order."""
    conditions: tuple[FilterCondition, ...] = ()
    sort: SortSpec | None = None
    search_text: str = ""
    page: int = 1
    page_size: int = 25

    def add_condition(self, condition: FilterCondition) -> FilterState:
        """Return a new state with the condition added."""
        return FilterState(
            conditions=self.conditions + (condition,),
            sort=self.sort,
            search_text=self.search_text,
            page=1,  # reset to page 1 when filters change
            page_size=self.page_size,
        )

    def remove_condition(self, field_name: str) -> FilterState:
        """Return a new state without conditions on field_name."""
        remaining = tuple(c for c in self.conditions if c.field_name != field_name)
        return FilterState(
            conditions=remaining,
            sort=self.sort,
            search_text=self.search_text,
            page=1,
            page_size=self.page_size,
        )

    def set_sort(self, sort: SortSpec | None) -> FilterState:
        return FilterState(
            conditions=self.conditions, sort=sort,
            search_text=self.search_text, page=1,
            page_size=self.page_size,
        )

    def set_search(self, text: str) -> FilterState:
        return FilterState(
            conditions=self.conditions, sort=self.sort,
            search_text=text, page=1, page_size=self.page_size,
        )

    def apply(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filter and sort records according to current state."""
        result = records

        # Apply text search across all string fields
        if self.search_text:
            query = self.search_text.lower()
            result = [
                r for r in result
                if any(query in str(v).lower() for v in r.values())
            ]

        # Apply structured conditions
        for cond in self.conditions:
            result = [r for r in result if cond.matches(r)]

        # Apply sort
        if self.sort:
            reverse = self.sort.direction == SortDirection.DESC
            result = sorted(
                result,
                key=lambda r: r.get(self.sort.field_name, ""),  # type: ignore[union-attr]
                reverse=reverse,
            )

        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "conditions": [c.to_dict() for c in self.conditions],
            "sort": {"field": self.sort.field_name, "direction": self.sort.direction.value}
                   if self.sort else None,
            "search_text": self.search_text,
            "page": self.page,
            "page_size": self.page_size,
        }


# --- State manager with undo/redo --------------------------------------

class FilterStateManager:
    """Manages filter state transitions with full undo/redo capability.

    Uses the command pattern: every state change pushes the previous
    state onto the undo stack. Undo pops from undo to redo.
    """

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
        """Transition to a new state, pushing current onto undo stack."""
        self._undo_stack.append(self._current)
        self._current = new_state
        self._redo_stack.clear()  # new action invalidates redo history

    def undo(self) -> FilterState:
        """Revert to the previous state."""
        if not self.can_undo:
            raise RuntimeError("Nothing to undo")
        self._redo_stack.append(self._current)
        self._current = self._undo_stack.pop()
        return self._current

    def redo(self) -> FilterState:
        """Re-apply the last undone state."""
        if not self.can_redo:
            raise RuntimeError("Nothing to redo")
        self._undo_stack.append(self._current)
        self._current = self._redo_stack.pop()
        return self._current

    def reset(self) -> FilterState:
        """Reset to default state, preserving undo history."""
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
    """Demonstrate filter state management with undo/redo."""
    manager = FilterStateManager()

    # Build up filters step by step
    state = manager.current
    state = state.add_condition(
        FilterCondition("status", FilterOperator.EQUALS, "active")
    )
    manager.apply_state(state)

    state = state.add_condition(
        FilterCondition("priority", FilterOperator.GREATER_THAN, 3)
    )
    manager.apply_state(state)

    state = state.set_sort(SortSpec("created_at", SortDirection.DESC))
    manager.apply_state(state)

    state = state.set_search("urgent")
    manager.apply_state(state)

    # Undo twice
    manager.undo()
    manager.undo()

    # Redo once
    manager.redo()

    # Apply filters to sample data
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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Filter state manager with undo/redo")
    parser.add_argument("--demo", action="store_true", default=True, help="Run demo")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    output = run_demo()
    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
