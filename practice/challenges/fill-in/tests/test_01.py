"""Tests for Fill-In Challenge #1 — List Filtering."""

from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

_spec = spec_from_file_location("ex01", Path(__file__).parent.parent / "01_list_filter.py")
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)

filter_positive = _mod.filter_positive
filter_long_words = _mod.filter_long_words
filter_by_key = _mod.filter_by_key
unique_sorted = _mod.unique_sorted


class TestFilterPositive:
    def test_mixed(self):
        assert filter_positive([3, -1, 0, 7, -5, 2]) == [3, 7, 2]

    def test_all_negative(self):
        assert filter_positive([-1, -2, -3]) == []

    def test_all_positive(self):
        assert filter_positive([1, 2, 3]) == [1, 2, 3]

    def test_empty(self):
        assert filter_positive([]) == []

    def test_zero_excluded(self):
        assert filter_positive([0]) == []


class TestFilterLongWords:
    def test_basic(self):
        assert filter_long_words(["hi", "hello", "hey", "howdy"], 4) == ["hello", "howdy"]

    def test_exact_length(self):
        assert filter_long_words(["abc", "ab", "abcd"], 3) == ["abc", "abcd"]

    def test_empty(self):
        assert filter_long_words([], 5) == []

    def test_none_match(self):
        assert filter_long_words(["a", "bb"], 10) == []


class TestFilterByKey:
    def test_basic(self):
        data = [{"name": "Alice", "role": "admin"}, {"name": "Bob", "role": "user"}]
        assert filter_by_key(data, "role", "admin") == [{"name": "Alice", "role": "admin"}]

    def test_no_match(self):
        data = [{"name": "Alice", "role": "user"}]
        assert filter_by_key(data, "role", "admin") == []

    def test_multiple_matches(self):
        data = [{"x": 1}, {"x": 1}, {"x": 2}]
        assert filter_by_key(data, "x", 1) == [{"x": 1}, {"x": 1}]


class TestUniqueSorted:
    def test_integers(self):
        assert unique_sorted([3, 1, 2, 3, 1]) == [1, 2, 3]

    def test_strings(self):
        assert unique_sorted(["banana", "apple", "banana", "cherry"]) == ["apple", "banana", "cherry"]

    def test_empty(self):
        assert unique_sorted([]) == []

    def test_already_unique(self):
        assert unique_sorted([5, 3, 1]) == [1, 3, 5]
