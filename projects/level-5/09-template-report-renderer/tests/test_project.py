"""Tests for Template Report Renderer."""
from __future__ import annotations

import json
import pytest
from pathlib import Path

from project import (
    render_variables,
    render_each_blocks,
    render_if_blocks,
    render_template,
    is_truthy,
    resolve_dotted_key,
    run,
)


# ---------- render_variables ----------

@pytest.mark.parametrize("template,data,expected", [
    ("Hello {{name}}!", {"name": "Alice"}, "Hello Alice!"),
    ("Count: {{n}}", {"n": 42}, "Count: 42"),
    ("Hello {{name}}!", {}, "Hello {{MISSING:name}}!"),
])
def test_render_variables(template: str, data: dict, expected: str) -> None:
    assert render_variables(template, data) == expected


# ---------- resolve_dotted_key ----------

def test_resolve_dotted_key_simple() -> None:
    assert resolve_dotted_key("name", {"name": "Alice"}) == "Alice"


def test_resolve_dotted_key_nested() -> None:
    data = {"config": {"timeout": 30}}
    assert resolve_dotted_key("config.timeout", data) == 30


def test_resolve_dotted_key_missing() -> None:
    assert resolve_dotted_key("missing.path", {"other": 1}) is None


# ---------- render_each_blocks ----------

def test_render_each_with_dicts() -> None:
    template = "Items:{{#each items}}\n- {{name}}{{/each}}"
    data = {"items": [{"name": "A"}, {"name": "B"}]}
    result = render_each_blocks(template, data)
    assert "- A" in result and "- B" in result


def test_render_each_with_scalars() -> None:
    template = "{{#each tags}}[{{this}}]{{/each}}"
    data = {"tags": ["python", "data"]}
    result = render_each_blocks(template, data)
    assert "[python]" in result and "[data]" in result


# ---------- is_truthy ----------

@pytest.mark.parametrize("value,expected", [
    (True, True),
    (False, False),
    (1, True),
    (0, False),
    ("yes", True),
    ("false", False),
    ("", False),
    (None, False),
    ([1], True),
    ([], False),
])
def test_is_truthy(value: object, expected: bool) -> None:
    assert is_truthy(value) == expected


# ---------- render_if_blocks ----------

def test_render_if_truthy_shows_block() -> None:
    template = "{{#if show}}VISIBLE{{/if}}"
    assert render_if_blocks(template, {"show": True}) == "VISIBLE"


def test_render_if_falsy_hides_block() -> None:
    template = "{{#if show}}VISIBLE{{/if}}"
    assert render_if_blocks(template, {"show": False}) == ""
    assert render_if_blocks(template, {}) == ""


# ---------- full render pipeline ----------

@pytest.mark.parametrize("data,expected_fragment", [
    ({"title": "Report", "count": 5}, "Report"),
    ({"title": "Test", "items": [{"x": "A"}]}, "Item: A"),
])
def test_render_template(data: dict, expected_fragment: str) -> None:
    template = "Title: {{title}}\n{{#each items}}Item: {{x}}\n{{/each}}"
    result = render_template(template, data)
    assert expected_fragment in result


# ---------- integration: run ----------

def test_run_writes_rendered_output(tmp_path: Path) -> None:
    tpl = tmp_path / "tpl.txt"
    tpl.write_text("Hello {{name}}, you have {{count}} items.", encoding="utf-8")
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps({"name": "Alice", "count": 3}), encoding="utf-8")
    output = tmp_path / "out.txt"
    result = run(tpl, data_file, output)
    assert output.read_text(encoding="utf-8") == "Hello Alice, you have 3 items."
    assert result["lines_written"] == 1
