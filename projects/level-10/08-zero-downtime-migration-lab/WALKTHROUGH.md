# Zero-Downtime Migration Lab — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This project teaches the expand-migrate-contract pattern used by every major tech company to change database schemas without downtime. Spend at least 30 minutes attempting it independently.

## Thinking Process

Imagine a production database serving 50,000 requests per minute. You need to rename the `name` column to `display_name`. The naive approach -- `ALTER TABLE users RENAME COLUMN name TO display_name` -- breaks every query that references `name` during the split second the rename happens. In a high-traffic system, that split second means hundreds of failed requests.

The expand-migrate-contract pattern avoids this by splitting the change into three phases. **Expand**: add the new `display_name` column alongside the existing `name` column. Both columns exist, both work. **Migrate**: backfill `display_name` from `name` for all rows, and update the application code to write to both columns. **Contract**: once all code reads from `display_name`, drop the old `name` column. At every phase, the system is fully functional -- old code reads `name`, new code reads `display_name`, and no queries fail.

The code models this as a **state machine** with five phases: `PENDING -> EXPANDING -> MIGRATING -> CONTRACTING -> COMPLETE`. Any phase can transition to `ROLLED_BACK` if something goes wrong. The `MigrationExecutor` processes steps in order, tracks history, and supports rollback. This same pattern is used by real tools like Alembic, Django migrations, and Flyway.

## Step 1: Define the Phase State Machine and Column Types

**What to do:** Create a `MigrationPhase` enum with all six phases and a `ColumnType` enum for supported database column types.

**Why:** The enum enforces that migrations can only be in defined phases. This prevents invalid states like "halfway between expanding and migrating." The separate `ROLLED_BACK` phase is critical -- any migration can fail, and the system must know that a rollback occurred rather than treating it as complete.

```python
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
```

The `auto()` function generates unique values automatically. For `MigrationPhase`, the exact values do not matter -- what matters is that each phase is distinct and comparable.

**Predict:** Why is `ROLLED_BACK` not positioned between specific phases? Can a rollback happen from any phase?

## Step 2: Build the In-Memory Table Simulation

**What to do:** Create `Column` (frozen dataclass), and `Table` with `add_column()`, `drop_column()`, and `insert()` methods.

**Why:** The table simulates a real database table in memory. This lets you practice migration patterns without needing a real database. The `add_column()` method is the key to the expand phase -- it adds a column and backfills all existing rows with the default value.

```python
@dataclass(frozen=True)
class Column:
    name: str
    col_type: ColumnType
    nullable: bool = True
    default: str | None = None


@dataclass
class Table:
    name: str
    columns: dict[str, Column] = field(default_factory=dict)
    rows: list[dict[str, Any]] = field(default_factory=list)

    def add_column(self, col: Column) -> None:
        if col.name in self.columns:
            raise ValueError(f"Column '{col.name}' already exists in '{self.name}'")
        self.columns[col.name] = col
        # Backfill existing rows with the default value
        for row in self.rows:
            row[col.name] = col.default

    def drop_column(self, col_name: str) -> None:
        if col_name not in self.columns:
            raise ValueError(f"Column '{col_name}' not found in '{self.name}'")
        del self.columns[col_name]
        for row in self.rows:
            row.pop(col_name, None)
```

Two critical design decisions:

- **`add_column()` backfills existing rows.** When you add `display_name` to a table with 1,000 rows, all 1,000 rows get the default value. Without this backfill, queries on existing rows would find a missing column.
- **`add_column()` rejects duplicate columns.** If `display_name` already exists, the method raises `ValueError` instead of silently overwriting. The "Fix it" section asks you to make this idempotent (skip silently instead of erroring).

**Predict:** After calling `add_column(Column("display_name", ColumnType.TEXT, default=""))` on a table with 2 rows, what value does each row have for `display_name`?

## Step 3: Define Migration Steps and Plans

**What to do:** Create `MigrationStep` (a single operation with phase, description, and forward/rollback descriptions) and `MigrationPlan` (an ordered list of steps with progress tracking).

**Why:** Each step represents one reversible operation. The forward description says what happens when the step executes; the rollback description says how to undo it. The plan tracks which steps have executed and which have been rolled back, enabling precise progress reporting.

```python
@dataclass
class MigrationStep:
    phase: MigrationPhase
    description: str
    forward_fn: str      # Description of forward operation
    rollback_fn: str     # Description of rollback operation
    executed: bool = False
    rolled_back: bool = False


@dataclass
class MigrationPlan:
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
```

The `progress_pct` property counts only steps that are both executed AND not rolled back. A step that was executed then rolled back does not count toward progress. This accurately reflects the state after a partial rollback.

**Predict:** If a plan has 3 steps and the first 2 are executed but then rolled back, what is `progress_pct`?

## Step 4: Build the Migration Executor

**What to do:** Create `MigrationExecutor` with `execute_plan()`, `_execute_step()`, and `_rollback_plan()` methods. The executor processes steps in order, logs history, and rolls back on failure.

**Why:** The executor is the state machine driver. It walks through each step, advances the phase, and maintains a history log. If any step fails (raises `MigrationError`), it rolls back all previously executed steps in reverse order -- just like a database transaction.

```python
class MigrationExecutor:
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

    def execute_plan(self, plan: MigrationPlan) -> MigrationPlan:
        for step in plan.steps:
            try:
                self._execute_step(plan, step)
            except MigrationError:
                self._rollback_plan(plan)
                return plan
        plan.current_phase = MigrationPhase.COMPLETE
        self._log(plan.migration_id, "COMPLETE", "Migration finished successfully")
        return plan

    def _rollback_plan(self, plan: MigrationPlan) -> None:
        for step in reversed(plan.steps):
            if step.executed and not step.rolled_back:
                step.rolled_back = True
                self._log(plan.migration_id, "ROLLBACK",
                         f"Rolled back: {step.description}")
        plan.current_phase = MigrationPhase.ROLLED_BACK
```

The rollback iterates in **reverse order** using `reversed(plan.steps)`. This is essential: if you expanded then migrated, you must undo the migration before undoing the expansion. Rollback in forward order would try to undo the expansion while migrated data still references the new column.

**Predict:** If the MIGRATING step fails, which steps get rolled back? Just the MIGRATING step, or both EXPANDING and MIGRATING?

## Step 5: Build the Migration Plan Factory and Safety Checks

**What to do:** Write `build_add_column_migration()` that constructs a three-phase plan, and `validate_migration_safety()` that checks for common mistakes.

**Why:** The factory encodes the expand-migrate-contract pattern as a reusable template. The safety validator catches red flags like "contracting without expanding" (which would drop a column that was never added) or overly complex migrations with too many steps.

```python
def build_add_column_migration(
    migration_id: str,
    table: Table,
    new_column: Column,
    old_column: str | None = None,
    transform_fn: str = "direct_copy",
) -> MigrationPlan:
    steps = [
        MigrationStep(
            MigrationPhase.EXPANDING,
            f"Add column '{new_column.name}' (nullable) to '{table.name}'",
            f"ALTER TABLE {table.name} ADD COLUMN {new_column.name} ...",
            f"ALTER TABLE {table.name} DROP COLUMN {new_column.name}",
        ),
        MigrationStep(
            MigrationPhase.MIGRATING,
            f"Backfill '{new_column.name}' from '{old_column or 'default'}'",
            f"UPDATE {table.name} SET {new_column.name} = ...",
            f"UPDATE {table.name} SET {new_column.name} = NULL",
        ),
    ]
    # Only add CONTRACTING step if replacing an old column
    if old_column:
        steps.append(MigrationStep(
            MigrationPhase.CONTRACTING,
            f"Drop old column '{old_column}' from '{table.name}'",
            f"ALTER TABLE {table.name} DROP COLUMN {old_column}",
            f"ALTER TABLE {table.name} ADD COLUMN {old_column}",
        ))
    return MigrationPlan(migration_id=migration_id, title=f"Add {new_column.name}", steps=steps)


def validate_migration_safety(plan: MigrationPlan) -> list[str]:
    warnings: list[str] = []
    if not plan.steps:
        warnings.append("Migration plan has no steps")
    has_expand = any(s.phase == MigrationPhase.EXPANDING for s in plan.steps)
    has_contract = any(s.phase == MigrationPhase.CONTRACTING for s in plan.steps)
    if has_contract and not has_expand:
        warnings.append("Contracting without expanding — data loss risk")
    return warnings
```

The factory conditionally adds the CONTRACTING step. If you are adding a brand-new column (not replacing an old one), there is nothing to contract -- you only expand and migrate. If you are renaming a column, all three phases are needed.

**Predict:** What does `validate_migration_safety()` return for a plan that has a CONTRACTING step but no EXPANDING step? Why is this dangerous?

## Step 6: Run the Demo

**What to do:** Write `main()` that creates a users table, builds a migration plan to add `display_name`, validates safety, executes the plan, and prints the history.

**Why:** The demo shows the full lifecycle: table creation with seed data, migration planning, safety validation, execution, and history review. It proves your code works end-to-end.

```python
def main() -> None:
    users = Table("users", {
        "id": Column("id", ColumnType.INTEGER, nullable=False),
        "username": Column("username", ColumnType.TEXT, nullable=False),
        "email": Column("email", ColumnType.TEXT),
    })
    users.insert({"id": 1, "username": "alice", "email": "alice@example.com"})
    users.insert({"id": 2, "username": "bob", "email": "bob@example.com"})

    new_col = Column("display_name", ColumnType.TEXT, nullable=True, default="")
    plan = build_add_column_migration("MIG-001", users, new_col)

    executor = MigrationExecutor(users)
    executor.execute_plan(plan)

    print(f"Migration: {plan.title}")
    print(f"Phase: {plan.current_phase.name}")
    print(f"Progress: {plan.progress_pct:.0f}%")
```

After execution, the migration should be COMPLETE with 100% progress, and the history should show the EXPANDING and MIGRATING steps.

**Predict:** After the migration completes, does the `users` table have a `display_name` column? What value does each row have for it?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Rollback in forward order | Using `for step in plan.steps` instead of `reversed()` | Always rollback in reverse: undo the most recent change first |
| Contracting before migrating | Steps defined in wrong order | Validate phase ordering: EXPANDING before MIGRATING before CONTRACTING |
| `add_column` crashes on duplicates | Column already exists from a previous partial run | Make `add_column` idempotent: skip if column already exists |
| `drop_column` on non-existent column | Typo in column name or already dropped | Check `col_name in self.columns` before dropping |
| Division by zero in `progress_pct` | Plan has no steps | Guard with `if not self.steps: return 0.0` |

## Testing Your Solution

```bash
pytest -v
```

Expected output:
```text
passed
```

Test from the command line:

```bash
python project.py
```

You should see output showing the migration title, final phase (COMPLETE), progress (100%), and a history log with entries for each step.

## What You Learned

- **The expand-migrate-contract pattern** enables zero-downtime schema changes by ensuring both old and new code paths work at every phase. This is how teams ship database changes to systems that cannot afford any downtime.
- **State machines with rollback** model complex workflows where any step can fail. The key insight is that rollback must happen in reverse order -- you undo the most recent change first, just like popping a stack.
- **Safety validation** catches structural mistakes before execution. Checking for "contracting without expanding" is a static analysis that prevents data loss -- the same principle behind linters and type checkers.
