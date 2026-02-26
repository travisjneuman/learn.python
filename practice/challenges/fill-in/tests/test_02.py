"""Tests for Fill-In Challenge #2 — Dictionary Builder."""

from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import pytest

_spec = spec_from_file_location("ex02", Path(__file__).parent.parent / "02_dict_builder.py")
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)

zip_to_dict = _mod.zip_to_dict
invert_dict = _mod.invert_dict
merge_dicts = _mod.merge_dicts
group_by = _mod.group_by


class TestZipToDict:
    def test_basic(self):
        assert zip_to_dict(["a", "b", "c"], [1, 2, 3]) == {"a": 1, "b": 2, "c": 3}

    def test_empty(self):
        assert zip_to_dict([], []) == {}

    def test_mismatched_raises(self):
        with pytest.raises(ValueError):
            zip_to_dict(["a", "b"], [1])


class TestInvertDict:
    def test_basic(self):
        assert invert_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}

    def test_empty(self):
        assert invert_dict({}) == {}

    def test_string_values(self):
        assert invert_dict({"x": "y"}) == {"y": "x"}


class TestMergeDicts:
    def test_no_conflict(self):
        assert merge_dicts({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

    def test_conflict(self):
        assert merge_dicts({"a": 1, "b": 2}, {"b": 3, "c": 4}) == {"a": 1, "b": 3, "c": 4}

    def test_empty(self):
        assert merge_dicts({}, {"a": 1}) == {"a": 1}


class TestGroupBy:
    def test_by_first_letter(self):
        result = group_by(["ant", "bee", "ape", "bat"], lambda w: w[0])
        assert result == {"a": ["ant", "ape"], "b": ["bee", "bat"]}

    def test_by_length(self):
        result = group_by(["a", "bb", "c", "dd"], len)
        assert result == {1: ["a", "c"], 2: ["bb", "dd"]}

    def test_empty(self):
        assert group_by([], lambda x: x) == {}
