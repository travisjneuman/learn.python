"""Tests for Template Driven Reporter."""

from pathlib import Path

import pytest

from project import (
    RenderResult,
    build_report_context,
    discover_variables,
    render_batch,
    render_file,
    safe_render,
    strict_render,
)


def test_discover_variables() -> None:
    """Should find all $var and ${var} references."""
    text = "Hello $name, your order #${order_id} is ready."
    vars_found = discover_variables(text)
    assert "name" in vars_found
    assert "order_id" in vars_found


def test_discover_no_variables() -> None:
    """Template with no variables should return empty list."""
    assert discover_variables("No variables here.") == []


def test_safe_render_complete() -> None:
    """All variables provided should render successfully."""
    result = safe_render("Hello $name!", {"name": "Alice"})
    assert result.success is True
    assert result.output == "Hello Alice!"
    assert result.missing_variables == []


def test_safe_render_missing() -> None:
    """Missing variables should be left as-is in safe mode."""
    result = safe_render("Hello $name, age $age!", {"name": "Bob"})
    assert result.success is False
    assert "$age" in result.output
    assert "age" in result.missing_variables


def test_strict_render_complete() -> None:
    """Strict render should work when all vars provided."""
    result = strict_render("$greeting $name", {"greeting": "Hi", "name": "Eve"})
    assert result.success is True
    assert result.output == "Hi Eve"


def test_strict_render_missing() -> None:
    """Strict render should fail on missing variables."""
    result = strict_render("$greeting $name", {"greeting": "Hi"})
    assert result.success is False
    assert "name" in result.missing_variables


def test_render_file(tmp_path: Path) -> None:
    """Should load template from file and render."""
    tmpl = tmp_path / "report.txt"
    tmpl.write_text("Report for $company: $total items", encoding="utf-8")
    result = render_file(tmpl, {"company": "Acme", "total": "42"})
    assert "Acme" in result.output
    assert "42" in result.output
    assert result.template_name == "report.txt"


def test_render_file_missing(tmp_path: Path) -> None:
    """Missing template file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        render_file(tmp_path / "nope.txt", {})


def test_render_batch() -> None:
    """Batch should render once per record."""
    template = "Dear $name, your balance is $$${balance}."
    records = [
        {"name": "Alice", "balance": "100"},
        {"name": "Bob", "balance": "200"},
    ]
    results = render_batch(template, records)
    assert len(results) == 2
    assert "Alice" in results[0].output
    assert "Bob" in results[1].output


def test_build_report_context_flat() -> None:
    """Flat dict should pass through unchanged."""
    data = {"name": "Acme", "year": "2024"}
    ctx = build_report_context(data)
    assert ctx["name"] == "Acme"


def test_build_report_context_nested() -> None:
    """Nested dicts should flatten with underscore prefix."""
    data = {"user": {"name": "Alice", "email": "a@b.com"}, "total": 10}
    ctx = build_report_context(data)
    assert ctx["user_name"] == "Alice"
    assert ctx["user_email"] == "a@b.com"
    assert ctx["total"] == 10
