"""Tests for Zero-Downtime Migration Lab.

Covers table operations, migration phases, expand-migrate-contract pattern,
rollback behavior, and safety validation.
"""
from __future__ import annotations

import pytest

from project import (
    Column,
    ColumnType,
    MigrationExecutor,
    MigrationPhase,
    MigrationPlan,
    MigrationStep,
    Table,
    build_add_column_migration,
    build_rename_column_migration,
    validate_migration_safety,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def users_table() -> Table:
    t = Table("users", {
        "id": Column("id", ColumnType.INTEGER, nullable=False),
        "name": Column("name", ColumnType.TEXT),
    })
    t.insert({"id": 1, "name": "alice"})
    t.insert({"id": 2, "name": "bob"})
    return t


# ---------------------------------------------------------------------------
# Table operations
# ---------------------------------------------------------------------------

class TestTable:
    def test_add_column_populates_default(self, users_table: Table) -> None:
        users_table.add_column(Column("active", ColumnType.BOOLEAN, default="true"))
        assert "active" in users_table.column_names
        assert users_table.rows[0]["active"] == "true"

    def test_drop_column_removes_data(self, users_table: Table) -> None:
        users_table.drop_column("name")
        assert "name" not in users_table.column_names
        assert "name" not in users_table.rows[0]

    def test_duplicate_column_raises(self, users_table: Table) -> None:
        with pytest.raises(ValueError, match="already exists"):
            users_table.add_column(Column("id", ColumnType.INTEGER))

    def test_drop_nonexistent_raises(self, users_table: Table) -> None:
        with pytest.raises(ValueError, match="not found"):
            users_table.drop_column("nonexistent")

    def test_insert_missing_required_raises(self) -> None:
        t = Table("strict", {"id": Column("id", ColumnType.INTEGER, nullable=False)})
        with pytest.raises(ValueError, match="Missing required"):
            t.insert({})


# ---------------------------------------------------------------------------
# Migration plan building
# ---------------------------------------------------------------------------

class TestMigrationPlanBuilder:
    def test_add_column_plan_has_two_steps(self, users_table: Table) -> None:
        col = Column("email", ColumnType.TEXT)
        plan = build_add_column_migration("M1", users_table, col)
        assert len(plan.steps) == 2
        assert plan.steps[0].phase == MigrationPhase.EXPANDING

    def test_rename_plan_has_three_steps(self, users_table: Table) -> None:
        plan = build_rename_column_migration("M2", users_table, "name", "display_name", ColumnType.TEXT)
        assert len(plan.steps) == 3
        assert plan.steps[2].phase == MigrationPhase.CONTRACTING

    def test_progress_starts_at_zero(self, users_table: Table) -> None:
        col = Column("email", ColumnType.TEXT)
        plan = build_add_column_migration("M1", users_table, col)
        assert plan.progress_pct == 0.0


# ---------------------------------------------------------------------------
# Migration execution
# ---------------------------------------------------------------------------

class TestMigrationExecutor:
    def test_successful_migration_completes(self, users_table: Table) -> None:
        col = Column("email", ColumnType.TEXT)
        plan = build_add_column_migration("M1", users_table, col)
        executor = MigrationExecutor(users_table)
        result = executor.execute_plan(plan)
        assert result.is_complete
        assert result.progress_pct == 100.0

    def test_history_records_all_phases(self, users_table: Table) -> None:
        col = Column("email", ColumnType.TEXT)
        plan = build_add_column_migration("M1", users_table, col)
        executor = MigrationExecutor(users_table)
        executor.execute_plan(plan)
        assert len(executor.history) >= 3  # steps + COMPLETE

    def test_empty_plan_completes_immediately(self, users_table: Table) -> None:
        plan = MigrationPlan(migration_id="M0", title="Empty")
        executor = MigrationExecutor(users_table)
        result = executor.execute_plan(plan)
        assert result.is_complete


# ---------------------------------------------------------------------------
# Safety validation
# ---------------------------------------------------------------------------

class TestSafetyValidation:
    def test_empty_plan_warns(self) -> None:
        plan = MigrationPlan(migration_id="M0", title="Empty")
        warnings = validate_migration_safety(plan)
        assert any("no steps" in w for w in warnings)

    def test_contract_without_expand_warns(self) -> None:
        plan = MigrationPlan(migration_id="M1", title="Bad", steps=[
            MigrationStep(MigrationPhase.CONTRACTING, "Drop column", "", ""),
        ])
        warnings = validate_migration_safety(plan)
        assert any("Contracting without expanding" in w for w in warnings)

    def test_valid_plan_no_warnings(self, users_table: Table) -> None:
        col = Column("email", ColumnType.TEXT)
        plan = build_add_column_migration("M1", users_table, col)
        warnings = validate_migration_safety(plan)
        assert len(warnings) == 0
