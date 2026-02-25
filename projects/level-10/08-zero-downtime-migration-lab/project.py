"""Zero-Downtime Migration Lab — Database migration patterns that avoid downtime.

Architecture: Models migrations as a state machine with phases: PENDING -> EXPANDING
-> MIGRATING -> CONTRACTING -> COMPLETE. Each phase is a reversible step. The
expand-migrate-contract pattern ensures the old schema remains functional throughout
the migration, so reads/writes continue uninterrupted.

Design rationale: Traditional "stop the world" migrations cause downtime. The
expand-contract pattern adds new columns/tables first (expand), backfills data
(migrate), then removes old columns (contract). At every phase, both old and new
code paths work — enabling zero-downtime rollout.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class MigrationPhase(Enum):
    PENDING = auto()
    EXPANDING = auto()
    MIGRATING = auto()
    CONTRACTING = auto()
    COMPLETE = auto()
    ROLLED_BACK = auto()


class ColumnType(Enum):
    TEXT = "TEXT"
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    TIMESTAMP = "TIMESTAMP"
    JSON = "JSON"


@dataclass(frozen=True)
class Column:
    """Schema column definition."""
    name: str
    col_type: ColumnType
    nullable: bool = True
    default: str | None = None


@dataclass
class Table:
    """In-memory table representation for migration simulation."""
    name: str
    columns: dict[str, Column] = field(default_factory=dict)
    rows: list[dict[str, Any]] = field(default_factory=list)

    def add_column(self, col: Column) -> None:
        if col.name in self.columns:
            raise ValueError(f"Column '{col.name}' already exists in '{self.name}'")
        self.columns[col.name] = col
        for row in self.rows:
            row[col.name] = col.default

    def drop_column(self, col_name: str) -> None:
        if col_name not in self.columns:
            raise ValueError(f"Column '{col_name}' not found in '{self.name}'")
        del self.columns[col_name]
        for row in self.rows:
            row.pop(col_name, None)

    def insert(self, data: dict[str, Any]) -> None:
        row = {}
        for col_name, col in self.columns.items():
            if col_name in data:
                row[col_name] = data[col_name]
            elif col.nullable or col.default is not None:
                row[col_name] = col.default
            else:
                raise ValueError(f"Missing required column: {col_name}")
        self.rows.append(row)

    @property
    def row_count(self) -> int:
        return len(self.rows)

    @property
    def column_names(self) -> list[str]:
        return list(self.columns.keys())


# ---------------------------------------------------------------------------
# Migration step definitions
# ---------------------------------------------------------------------------

@dataclass
class MigrationStep:
    """A single migration operation (expand, migrate, or contract)."""
    phase: MigrationPhase
    description: str
    forward_fn: str  # Description of forward operation
    rollback_fn: str  # Description of rollback operation
    executed: bool = False
    rolled_back: bool = False


@dataclass
class MigrationPlan:
    """Complete migration plan with ordered steps."""
    migration_id: str
    title: str
    steps: list[MigrationStep] = field(default_factory=list)
    current_phase: MigrationPhase = MigrationPhase.PENDING

    @property
    def progress_pct(self) -> float:
        if not self.steps:
            return 0.0
        executed = sum(1 for s in self.steps if s.executed and not s.rolled_back)
        return (executed / len(self.steps)) * 100

    @property
    def is_complete(self) -> bool:
        return self.current_phase == MigrationPhase.COMPLETE


# ---------------------------------------------------------------------------
# Migration executor (state machine)
# ---------------------------------------------------------------------------

class MigrationError(Exception):
    """Raised when a migration step fails."""


class MigrationExecutor:
    """Executes migration plans using the expand-migrate-contract pattern.

    State transitions:
    PENDING -> EXPANDING -> MIGRATING -> CONTRACTING -> COMPLETE
    Any phase can transition to ROLLED_BACK.
    """

    PHASE_ORDER = [
        MigrationPhase.PENDING,
        MigrationPhase.EXPANDING,
        MigrationPhase.MIGRATING,
        MigrationPhase.CONTRACTING,
        MigrationPhase.COMPLETE,
    ]

    def __init__(self, table: Table) -> None:
        self._table = table
        self._history: list[dict[str, str]] = []

    @property
    def history(self) -> list[dict[str, str]]:
        return list(self._history)

    def execute_plan(self, plan: MigrationPlan) -> MigrationPlan:
        """Execute all steps in order. Rolls back on failure."""
        for step in plan.steps:
            try:
                self._execute_step(plan, step)
            except MigrationError:
                self._rollback_plan(plan)
                return plan
        plan.current_phase = MigrationPhase.COMPLETE
        self._log(plan.migration_id, "COMPLETE", "Migration finished successfully")
        return plan

    def _execute_step(self, plan: MigrationPlan, step: MigrationStep) -> None:
        """Execute a single step and advance phase."""
        plan.current_phase = step.phase
        self._log(plan.migration_id, step.phase.name, step.description)
        step.executed = True

    def _rollback_plan(self, plan: MigrationPlan) -> None:
        """Roll back all executed steps in reverse order."""
        for step in reversed(plan.steps):
            if step.executed and not step.rolled_back:
                step.rolled_back = True
                self._log(plan.migration_id, "ROLLBACK", f"Rolled back: {step.description}")
        plan.current_phase = MigrationPhase.ROLLED_BACK

    def _log(self, migration_id: str, phase: str, message: str) -> None:
        self._history.append({"migration_id": migration_id, "phase": phase, "message": message})


# ---------------------------------------------------------------------------
# Expand-Migrate-Contract builder
# ---------------------------------------------------------------------------

def build_add_column_migration(
    migration_id: str,
    table: Table,
    new_column: Column,
    old_column: str | None = None,
    transform_fn: str = "direct_copy",
) -> MigrationPlan:
    """Build a standard expand-migrate-contract plan for adding a column."""
    steps = [
        MigrationStep(
            MigrationPhase.EXPANDING,
            f"Add column '{new_column.name}' (nullable) to '{table.name}'",
            f"ALTER TABLE {table.name} ADD COLUMN {new_column.name} {new_column.col_type.value}",
            f"ALTER TABLE {table.name} DROP COLUMN {new_column.name}",
        ),
        MigrationStep(
            MigrationPhase.MIGRATING,
            f"Backfill '{new_column.name}' from '{old_column or 'default'}'",
            f"UPDATE {table.name} SET {new_column.name} = transform({old_column or 'default'})",
            f"UPDATE {table.name} SET {new_column.name} = NULL",
        ),
    ]

    if old_column:
        steps.append(MigrationStep(
            MigrationPhase.CONTRACTING,
            f"Drop old column '{old_column}' from '{table.name}'",
            f"ALTER TABLE {table.name} DROP COLUMN {old_column}",
            f"ALTER TABLE {table.name} ADD COLUMN {old_column}",
        ))

    return MigrationPlan(migration_id=migration_id, title=f"Add {new_column.name}", steps=steps)


def build_rename_column_migration(
    migration_id: str,
    table: Table,
    old_name: str,
    new_name: str,
    col_type: ColumnType,
) -> MigrationPlan:
    """Build expand-migrate-contract plan for renaming a column."""
    new_col = Column(new_name, col_type, nullable=True)
    return build_add_column_migration(migration_id, table, new_col, old_column=old_name)


# ---------------------------------------------------------------------------
# Safety checks
# ---------------------------------------------------------------------------

def validate_migration_safety(plan: MigrationPlan) -> list[str]:
    """Check a plan for common safety issues. Returns list of warnings."""
    warnings: list[str] = []
    if not plan.steps:
        warnings.append("Migration plan has no steps")
    has_expand = any(s.phase == MigrationPhase.EXPANDING for s in plan.steps)
    has_contract = any(s.phase == MigrationPhase.CONTRACTING for s in plan.steps)
    if has_contract and not has_expand:
        warnings.append("Contracting without expanding — data loss risk")
    if len(plan.steps) > 10:
        warnings.append("Migration has many steps — consider splitting")
    return warnings


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

def main() -> None:
    users = Table("users", {
        "id": Column("id", ColumnType.INTEGER, nullable=False),
        "username": Column("username", ColumnType.TEXT, nullable=False),
        "email": Column("email", ColumnType.TEXT),
    })
    users.insert({"id": 1, "username": "alice", "email": "alice@example.com"})
    users.insert({"id": 2, "username": "bob", "email": "bob@example.com"})

    new_col = Column("display_name", ColumnType.TEXT, nullable=True, default="")
    plan = build_add_column_migration("MIG-001", users, new_col, old_column=None)

    warnings = validate_migration_safety(plan)
    if warnings:
        for w in warnings:
            print(f"WARNING: {w}")

    executor = MigrationExecutor(users)
    executor.execute_plan(plan)

    print(f"Migration: {plan.title}")
    print(f"Phase: {plan.current_phase.name}")
    print(f"Progress: {plan.progress_pct:.0f}%")
    print(f"\nHistory ({len(executor.history)} entries):")
    for entry in executor.history:
        print(f"  [{entry['phase']}] {entry['message']}")


if __name__ == "__main__":
    main()
