"""Tests for Plugin Style Transformer."""
import pytest
from project import (UppercasePlugin, FilterEmptyPlugin, StripWhitespacePlugin,
                     get_plugin, list_plugins, run_plugins, register_plugin, TransformPlugin)

def test_uppercase_plugin():
    records = [{"name": "alice", "age": 30}]
    result = UppercasePlugin().transform(records)
    assert result[0]["name"] == "ALICE"
    assert result[0]["age"] == 30

def test_filter_empty_plugin():
    records = [{"a": "x"}, {"a": "", "b": ""}, {"a": "y"}]
    result = FilterEmptyPlugin().transform(records)
    assert len(result) == 2

def test_strip_whitespace_plugin():
    records = [{"name": "  Alice  "}]
    result = StripWhitespacePlugin().transform(records)
    assert result[0]["name"] == "Alice"

def test_get_plugin_found():
    assert get_plugin("uppercase") is not None

def test_get_plugin_not_found():
    assert get_plugin("nonexistent") is None

def test_list_plugins():
    plugins = list_plugins()
    names = [p["name"] for p in plugins]
    assert "uppercase" in names
    assert "filter_empty" in names

@pytest.mark.parametrize("plugin_name", ["uppercase", "filter_empty", "strip", "sort_by_name"])
def test_all_builtin_plugins_run(plugin_name):
    records = [{"name": "test", "value": "data"}]
    plugin = get_plugin(plugin_name)
    assert plugin is not None
    result = plugin.transform(records)
    assert isinstance(result, list)

def test_run_plugins_chain():
    records = [{"name": "  ALICE  "}, {"name": ""}]
    result, log = run_plugins(records, ["strip", "filter_empty"])
    assert len(result) == 1
    assert result[0]["name"] == "ALICE"

def test_custom_plugin_registration():
    class ReversePlugin(TransformPlugin):
        name = "reverse"
        description = "Reverse record order"
        def transform(self, records):
            return list(reversed(records))
    register_plugin(ReversePlugin)
    assert get_plugin("reverse") is not None
