# Solution: Level 6 / Project 14 - SQL Runbook Generator

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [README](./README.md) hints or re-read the
> relevant [concept docs](../../../concepts/) first.

---

## Complete solution

```python
"""Level 6 / Project 14 — SQL Runbook Generator.

Generates operational SQL runbooks from templates and parameters.
A runbook is a sequence of SQL statements with documentation that
an operator can execute step-by-step.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sqlite3
import string
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

# WHY store runbook history? -- When an operator runs a maintenance
# script, the audit trail records exactly which SQL was executed and
# with what parameters. If something goes wrong, you can trace back
# to the exact runbook version that caused the issue.
RUNBOOK_DDL = """\
CREATE TABLE IF NOT EXISTS runbook_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    steps       TEXT NOT NULL,
    params_used TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(RUNBOOK_DDL)
    conn.commit()


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

# WHY a template registry? -- Centralizing SQL templates in a dict makes
# them discoverable, versionable, and testable. New templates can be
# added without touching the generation logic, and each template's
# steps are self-documenting with titles and descriptions.
BUILTIN_TEMPLATES: dict[str, list[dict]] = {
    "table_maintenance": [
        {
            "title": "Analyze table statistics",
            "sql": "ANALYZE ${table_name};",
            "description": "Update SQLite query planner statistics for ${table_name}.",
        },
        {
            "title": "Check row count",
            "sql": "SELECT COUNT(*) AS row_count FROM ${table_name};",
            "description": "Verify row count is within expected range.",
        },
        {
            "title": "Vacuum database",
            "sql": "VACUUM;",
            "description": "Reclaim unused space and defragment the database file.",
        },
    ],
    "data_cleanup": [
        {
            "title": "Identify orphaned rows",
            "sql": "SELECT * FROM ${table_name} WHERE ${fk_column} NOT IN (SELECT id FROM ${parent_table});",
            "description": "Find rows referencing non-existent parent records.",
        },
        {
            "title": "Delete orphaned rows",
            "sql": "DELETE FROM ${table_name} WHERE ${fk_column} NOT IN (SELECT id FROM ${parent_table});",
            "description": "Remove orphaned rows found in previous step.",
        },
    ],
}


# ---------------------------------------------------------------------------
# Runbook generation
# ---------------------------------------------------------------------------


@dataclass
class RunbookStep:
    title: str
    sql: str
    description: str


@dataclass
class Runbook:
    name: str
    steps: list[RunbookStep] = field(default_factory=list)
    params: dict = field(default_factory=dict)


def render_template(template_str: str, params: dict) -> str:
    """Safely substitute parameters into a template string.

    WHY string.Template instead of f-strings? -- string.Template uses
    ${var} syntax and raises KeyError for missing parameters instead of
    silently leaving placeholders. This fail-fast behavior catches
    configuration errors before SQL is executed.
    """
    tmpl = string.Template(template_str)
    return tmpl.substitute(params)


def generate_runbook(
    template_name: str,
    params: dict,
    custom_templates: dict | None = None,
) -> Runbook:
    """Generate a runbook from a named template and parameters.

    WHY validate template_name early? -- If the template does not exist,
    we want a clear error message listing available templates, not a
    cryptic KeyError deep in the rendering code.
    """
    templates = custom_templates or BUILTIN_TEMPLATES

    if template_name not in templates:
        available = ", ".join(templates.keys())
        raise ValueError(f"Unknown template '{template_name}'. Available: {available}")

    steps = []
    for step_tmpl in templates[template_name]:
        steps.append(RunbookStep(
            title=render_template(step_tmpl["title"], params),
            sql=render_template(step_tmpl["sql"], params),
            description=render_template(step_tmpl["description"], params),
        ))

    return Runbook(name=f"{template_name}", steps=steps, params=params)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_sql(sql: str) -> list[str]:
    """Basic SQL validation checks. Returns list of warnings.

    WHY warn instead of block? -- Some dangerous operations (like DROP
    TABLE) are legitimate in a maintenance runbook. We surface warnings
    so the operator can make an informed decision rather than silently
    blocking valid use cases.
    """
    warnings: list[str] = []

    dangerous = ["DROP TABLE", "DROP DATABASE", "TRUNCATE"]
    for pattern in dangerous:
        if pattern in sql.upper():
            warnings.append(f"Dangerous operation detected: {pattern}")

    # WHY check for unresolved variables? -- A leftover ${var} in the
    # generated SQL means a parameter was missed. Executing it would
    # cause a syntax error at best or target the wrong table at worst.
    if re.search(r"\$\{?\w+\}?", sql):
        warnings.append("Unresolved template variable found in SQL")

    return warnings


# ---------------------------------------------------------------------------
# History
# ---------------------------------------------------------------------------


def save_runbook(conn: sqlite3.Connection, runbook: Runbook) -> int:
    """Save a generated runbook to the history table."""
    steps_json = json.dumps([
        {"title": s.title, "sql": s.sql, "description": s.description}
        for s in runbook.steps
    ])
    cur = conn.execute(
        "INSERT INTO runbook_history (name, steps, params_used) VALUES (?, ?, ?)",
        (runbook.name, steps_json, json.dumps(runbook.params)),
    )
    conn.commit()
    return cur.lastrowid


def get_runbook_history(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        "SELECT id, name, created_at FROM runbook_history ORDER BY id DESC"
    ).fetchall()
    return [{"id": r[0], "name": r[1], "created_at": r[2]} for r in rows]


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------


def format_runbook(runbook: Runbook) -> str:
    """Render a runbook as a human-readable text document.

    WHY include step numbers and warnings? -- An operator executing a
    runbook needs to know which step they are on and any risks before
    running the SQL. Numbered steps and inline warnings make this safe.
    """
    lines = [
        f"{'=' * 60}",
        f"RUNBOOK: {runbook.name}",
        f"Parameters: {json.dumps(runbook.params)}",
        f"{'=' * 60}",
        "",
    ]
    for i, step in enumerate(runbook.steps, 1):
        lines.append(f"Step {i}: {step.title}")
        lines.append(f"  Description: {step.description}")
        lines.append(f"  SQL: {step.sql}")
        warnings = validate_sql(step.sql)
        if warnings:
            for w in warnings:
                lines.append(f"  WARNING: {w}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    config = json.loads(input_path.read_text(encoding="utf-8"))

    conn = sqlite3.connect(db_path)
    try:
        init_db(conn)

        runbooks_generated = []
        for req in config.get("runbooks", []):
            rb = generate_runbook(req["template"], req.get("params", {}))
            save_runbook(conn, rb)
            text = format_runbook(rb)
            runbooks_generated.append({
                "name": rb.name,
                "steps": len(rb.steps),
                "text": text,
            })

        history = get_runbook_history(conn)
    finally:
        conn.close()

    summary = {
        "runbooks_generated": len(runbooks_generated),
        "runbooks": runbooks_generated,
        "history": history,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("generated %d runbooks", len(runbooks_generated))
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SQL Runbook Generator — templated operational procedures"
    )
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/output_summary.json")
    parser.add_argument("--db", default=":memory:")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output), args.db)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `string.Template` for substitution | Raises `KeyError` for missing params (fail-fast); `${var}` syntax is clear and safe | f-strings -- evaluated at definition time, not suitable for runtime templates; Jinja2 -- powerful but a heavy dependency |
| Runbook history in SQLite | Creates an audit trail of exactly which SQL was generated and with what parameters; queryable | File-based history -- harder to query; no atomicity guarantees |
| Warn-not-block for dangerous SQL | Some dangerous operations are legitimate in maintenance contexts; warnings let operators make informed decisions | Hard-block dangerous patterns -- safer but would prevent valid maintenance runbooks |
| Template registry as a dict | Easy to extend with new templates; templates are self-documenting with title/description/sql per step | Templates in separate files -- more scalable for large orgs but overkill for this learning project |

## Alternative approaches

### Approach B: Parameterized query execution (not just generation)

```python
def execute_runbook(conn: sqlite3.Connection, runbook: Runbook) -> list[dict]:
    """Actually execute each SQL step and capture results.

    WARNING: Only use this with trusted, validated runbooks.
    """
    results = []
    for i, step in enumerate(runbook.steps, 1):
        warnings = validate_sql(step.sql)
        if any("Dangerous" in w for w in warnings):
            results.append({"step": i, "status": "skipped", "reason": "dangerous SQL"})
            continue
        try:
            cur = conn.execute(step.sql)
            rows = cur.fetchall() if cur.description else []
            results.append({"step": i, "status": "ok", "rows_affected": cur.rowcount, "rows": rows})
        except sqlite3.Error as exc:
            results.append({"step": i, "status": "error", "error": str(exc)})
    conn.commit()
    return results
```

**Trade-off:** Execution mode turns the generator into a full automation tool. But executing generated SQL requires extreme caution: you need confirmation prompts, dry-run mode, and rollback capability. The generation-only approach is safer for learning and forces the operator to review each step before running it.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| SQL injection in template parameters (e.g., `table_name = "users; DROP TABLE users"`) | `string.Template` blindly substitutes the value; the generated SQL contains the injected command | Run `validate_sql()` on the rendered output; in production, use allowlists for table/column names |
| Missing template parameter (e.g., no `table_name` in params) | `string.Template.substitute()` raises `KeyError` with the missing key name | Catch `KeyError` in `generate_runbook` and report which parameters the template requires |
| Requesting a non-existent template name | `generate_runbook` raises `ValueError` listing available templates | The current code already handles this gracefully with a clear error message |
