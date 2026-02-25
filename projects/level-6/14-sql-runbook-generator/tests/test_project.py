"""Tests for SQL Runbook Generator.

Validates template rendering, SQL validation, runbook generation,
and history storage using in-memory SQLite.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from project import (
    format_runbook,
    generate_runbook,
    get_runbook_history,
    init_db,
    render_template,
    run,
    save_runbook,
    validate_sql,
)


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    init_db(c)
    yield c
    c.close()


class TestRenderTemplate:
    def test_substitutes_params(self) -> None:
        result = render_template("SELECT * FROM ${table}", {"table": "users"})
        assert result == "SELECT * FROM users"

    def test_missing_param_raises(self) -> None:
        with pytest.raises(KeyError):
            render_template("SELECT * FROM ${table}", {})

    @pytest.mark.parametrize("params,expected", [
        ({"x": "1", "y": "2"}, "1 and 2"),
        ({"x": "a", "y": "b"}, "a and b"),
    ])
    def test_multiple_params(self, params: dict, expected: str) -> None:
        assert render_template("${x} and ${y}", params) == expected


class TestValidateSQL:
    def test_safe_sql(self) -> None:
        assert validate_sql("SELECT COUNT(*) FROM users") == []

    def test_dangerous_drop(self) -> None:
        warnings = validate_sql("DROP TABLE users;")
        assert any("DROP TABLE" in w for w in warnings)

    def test_unresolved_variable(self) -> None:
        warnings = validate_sql("SELECT * FROM ${table}")
        assert any("Unresolved" in w for w in warnings)


class TestGenerateRunbook:
    def test_builtin_template(self) -> None:
        rb = generate_runbook("table_maintenance", {"table_name": "orders"})
        assert rb.name == "table_maintenance"
        assert len(rb.steps) == 3
        assert "orders" in rb.steps[0].sql

    def test_unknown_template_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown template"):
            generate_runbook("nonexistent", {})


class TestHistory:
    def test_save_and_retrieve(self, conn: sqlite3.Connection) -> None:
        rb = generate_runbook("table_maintenance", {"table_name": "test"})
        save_runbook(conn, rb)
        history = get_runbook_history(conn)
        assert len(history) == 1
        assert history[0]["name"] == "table_maintenance"


def test_format_runbook() -> None:
    rb = generate_runbook("table_maintenance", {"table_name": "events"})
    text = format_runbook(rb)
    assert "RUNBOOK:" in text
    assert "Step 1:" in text
    assert "events" in text


def test_run_end_to_end(tmp_path) -> None:
    config = {
        "runbooks": [
            {"template": "table_maintenance", "params": {"table_name": "sales"}},
        ]
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["runbooks_generated"] == 1
    assert out.exists()
