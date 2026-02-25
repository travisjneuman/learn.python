"""Tests for Filter State Manager.

Covers: filter conditions, state transitions, undo/redo, and data filtering.
"""

from __future__ import annotations

import pytest

from project import (
    FilterCondition,
    FilterOperator,
    FilterState,
    FilterStateManager,
    SortDirection,
    SortSpec,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def sample_records() -> list[dict]:
    return [
        {"name": "Alice", "age": 30, "dept": "eng"},
        {"name": "Bob", "age": 25, "dept": "eng"},
        {"name": "Carol", "age": 35, "dept": "sales"},
        {"name": "Dave", "age": 28, "dept": "sales"},
    ]


@pytest.fixture
def manager() -> FilterStateManager:
    return FilterStateManager()


# --- FilterCondition matching -------------------------------------------

class TestFilterCondition:
    @pytest.mark.parametrize("op,value,record_val,expected", [
        (FilterOperator.EQUALS, "eng", "eng", True),
        (FilterOperator.EQUALS, "eng", "sales", False),
        (FilterOperator.NOT_EQUALS, "eng", "sales", True),
        (FilterOperator.GREATER_THAN, 25, 30, True),
        (FilterOperator.GREATER_THAN, 25, 20, False),
        (FilterOperator.LESS_THAN, 30, 25, True),
        (FilterOperator.CONTAINS, "ali", "Alice", True),
        (FilterOperator.CONTAINS, "xyz", "Alice", False),
        (FilterOperator.IN, ["eng", "ops"], "eng", True),
        (FilterOperator.IN, ["eng", "ops"], "sales", False),
    ])
    def test_matches(self, op, value, record_val, expected) -> None:
        cond = FilterCondition("field", op, value)
        assert cond.matches({"field": record_val}) is expected

    def test_missing_field_returns_false(self) -> None:
        cond = FilterCondition("missing", FilterOperator.EQUALS, "x")
        assert cond.matches({"other": "y"}) is False


# --- FilterState immutability -------------------------------------------

class TestFilterState:
    def test_add_condition_returns_new_state(self) -> None:
        state = FilterState()
        cond = FilterCondition("dept", FilterOperator.EQUALS, "eng")
        new_state = state.add_condition(cond)
        assert len(new_state.conditions) == 1
        assert len(state.conditions) == 0  # original unchanged

    def test_remove_condition_by_field(self) -> None:
        cond1 = FilterCondition("dept", FilterOperator.EQUALS, "eng")
        cond2 = FilterCondition("age", FilterOperator.GREATER_THAN, 25)
        state = FilterState(conditions=(cond1, cond2))
        new_state = state.remove_condition("dept")
        assert len(new_state.conditions) == 1
        assert new_state.conditions[0].field_name == "age"

    def test_apply_filters_records(self, sample_records: list[dict]) -> None:
        state = FilterState().add_condition(
            FilterCondition("dept", FilterOperator.EQUALS, "eng")
        )
        result = state.apply(sample_records)
        assert len(result) == 2
        assert all(r["dept"] == "eng" for r in result)

    def test_apply_sort(self, sample_records: list[dict]) -> None:
        state = FilterState().set_sort(SortSpec("age", SortDirection.ASC))
        result = state.apply(sample_records)
        ages = [r["age"] for r in result]
        assert ages == sorted(ages)

    def test_search_text_filters_across_fields(self, sample_records: list[dict]) -> None:
        state = FilterState().set_search("alice")
        result = state.apply(sample_records)
        assert len(result) == 1
        assert result[0]["name"] == "Alice"


# --- Undo/Redo ----------------------------------------------------------

class TestUndoRedo:
    def test_undo_restores_previous(self, manager: FilterStateManager) -> None:
        original = manager.current
        new_state = original.add_condition(
            FilterCondition("x", FilterOperator.EQUALS, 1)
        )
        manager.apply_state(new_state)
        manager.undo()
        assert manager.current == original

    def test_redo_after_undo(self, manager: FilterStateManager) -> None:
        cond = FilterCondition("x", FilterOperator.EQUALS, 1)
        new_state = manager.current.add_condition(cond)
        manager.apply_state(new_state)
        manager.undo()
        manager.redo()
        assert len(manager.current.conditions) == 1

    def test_new_action_clears_redo(self, manager: FilterStateManager) -> None:
        s1 = manager.current.add_condition(
            FilterCondition("a", FilterOperator.EQUALS, 1)
        )
        manager.apply_state(s1)
        manager.undo()
        assert manager.can_redo
        s2 = manager.current.add_condition(
            FilterCondition("b", FilterOperator.EQUALS, 2)
        )
        manager.apply_state(s2)
        assert not manager.can_redo

    def test_undo_empty_raises(self, manager: FilterStateManager) -> None:
        with pytest.raises(RuntimeError, match="Nothing to undo"):
            manager.undo()

    def test_redo_empty_raises(self, manager: FilterStateManager) -> None:
        with pytest.raises(RuntimeError, match="Nothing to redo"):
            manager.redo()
