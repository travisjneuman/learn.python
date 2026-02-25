"""
Tests for Project 04 — Property-Based Testing (test_project.py)

Additional property-based tests that complement test_properties.py.
These use standard pytest assertions to verify the same properties
that Hypothesis tests with random inputs. Both approaches are valuable:
Hypothesis finds unexpected edge cases; explicit tests document known ones.

What is a property?
    A property is something that is ALWAYS true about a function, regardless
    of the specific input. For example: sorting a list twice gives the same
    result as sorting once. Testing properties is more powerful than testing
    specific examples because it covers infinite inputs.

Run with: pytest tests/test_project.py -v
"""

import pytest

from project import sort_list, reverse_string, encode_decode_json, merge_dicts


# ── sort_list properties ───────────────────────────────────────────────

def test_sort_list_idempotent():
    """Sorting a sorted list should produce the same list (idempotent).

    WHY: Idempotent means "applying the operation twice gives the same result
    as applying it once." If sorting is not idempotent, something is wrong
    with the sort implementation.
    """
    original = [5, 2, 8, 1, 9]
    sorted_once = sort_list(original)
    sorted_twice = sort_list(sorted_once)

    assert sorted_once == sorted_twice, "sort(sort(x)) should equal sort(x)"


def test_sort_list_preserves_length():
    """Sorting should not add or remove elements.

    WHY: A buggy sort might skip elements or duplicate them. Checking
    length preservation catches these bugs.
    """
    original = [3, 1, 4, 1, 5, 9]
    result = sort_list(original)

    assert len(result) == len(original), "Sorted list should have same length"


def test_sort_list_preserves_elements():
    """Sorting should contain the same elements as the original.

    WHY: The sorted list should be a permutation of the original. Checking
    that both lists have the same elements (with same counts) verifies this.
    """
    original = [3, 1, 4, 1, 5]
    result = sort_list(original)

    assert sorted(original) == result, "Should contain same elements"


def test_sort_list_is_ordered():
    """Every element in the sorted list should be <= the next one.

    WHY: This is the definition of sorted order. Testing it directly is
    more robust than comparing to a known output.
    """
    result = sort_list([5, 2, 8, 1, 9, 3])

    for i in range(len(result) - 1):
        assert result[i] <= result[i + 1], f"Element {i} should be <= element {i+1}"


def test_sort_list_does_not_modify_original():
    """sort_list should return a new list, not modify the original.

    WHY: Functions that modify their inputs are harder to reason about and
    test. sorted() returns a new list, and this test verifies that behavior
    is preserved.
    """
    original = [3, 1, 2]
    sort_list(original)

    assert original == [3, 1, 2], "Original list should be unchanged"


# ── reverse_string properties ──────────────────────────────────────────

def test_reverse_string_involution():
    """Reversing a string twice should give back the original (involution).

    WHY: reverse(reverse(x)) == x is a fundamental property. If it fails,
    the reverse function is losing or reordering characters.
    """
    text = "Hello, World!"
    assert reverse_string(reverse_string(text)) == text


def test_reverse_string_preserves_length():
    """Reversing should not change the string's length.

    WHY: A reverse that truncates or pads would produce wrong results.
    """
    text = "Python"
    assert len(reverse_string(text)) == len(text)


def test_reverse_string_first_becomes_last():
    """The first character of the original should be the last of the reversed.

    WHY: This property follows directly from the definition of reversal.
    It catches implementations that shift characters without fully reversing.
    """
    text = "abcde"
    reversed_text = reverse_string(text)

    assert reversed_text[-1] == text[0], "First char should become last"
    assert reversed_text[0] == text[-1], "Last char should become first"


def test_reverse_string_empty():
    """Reversing an empty string should return an empty string.

    WHY: Edge case. An implementation that indexes into the string without
    checking emptiness might crash.
    """
    assert reverse_string("") == ""


# ── encode_decode_json properties ──────────────────────────────────────

def test_encode_decode_roundtrip_dict():
    """Encoding then decoding a dict should return the original.

    WHY: Roundtrip integrity is the fundamental property of serialization.
    If encode/decode loses data, the serialization format is broken.
    """
    data = {"name": "Alice", "scores": [95, 87], "active": True}
    assert encode_decode_json(data) == data


def test_encode_decode_roundtrip_list():
    """Encoding then decoding a list should return the original.

    WHY: Lists are a basic JSON type. This test verifies that list
    elements (including nested structures) survive the roundtrip.
    """
    data = [1, "two", 3.0, None, True]
    assert encode_decode_json(data) == data


def test_encode_decode_roundtrip_primitives():
    """Encoding then decoding primitive values should preserve them.

    WHY: JSON supports strings, numbers, booleans, and null. Each
    should survive the roundtrip without type coercion.
    """
    assert encode_decode_json("hello") == "hello"
    assert encode_decode_json(42) == 42
    assert encode_decode_json(3.14) == pytest.approx(3.14)
    assert encode_decode_json(True) is True
    assert encode_decode_json(None) is None


# ── merge_dicts properties ─────────────────────────────────────────────

def test_merge_dicts_contains_all_keys():
    """The merged dict should contain all keys from both inputs.

    WHY: If a key from either input is missing in the result, the merge
    is dropping data.
    """
    a = {"x": 1, "y": 2}
    b = {"y": 20, "z": 30}
    result = merge_dicts(a, b)

    assert set(result.keys()) == {"x", "y", "z"}, "Should have all keys from both dicts"


def test_merge_dicts_b_wins_on_conflict():
    """When both dicts have the same key, dict_b's value should win.

    WHY: This is the documented behavior ({**a, **b} means b overrides a).
    If the order is reversed, values from a would incorrectly win.
    """
    a = {"shared": "from_a"}
    b = {"shared": "from_b"}
    result = merge_dicts(a, b)

    assert result["shared"] == "from_b", "dict_b should override dict_a"


def test_merge_dicts_unique_keys_preserved():
    """Keys unique to dict_a should keep their original values.

    WHY: Only shared keys should be overridden. Unique keys in dict_a
    must survive the merge unchanged.
    """
    a = {"only_in_a": 42}
    b = {"only_in_b": 99}
    result = merge_dicts(a, b)

    assert result["only_in_a"] == 42, "Unique key from a should be preserved"
    assert result["only_in_b"] == 99, "Unique key from b should be preserved"


def test_merge_dicts_empty_inputs():
    """Merging with empty dicts should work correctly.

    WHY: Edge cases with empty inputs can cause unexpected behavior.
    Merging with an empty dict should return the other dict's contents.
    """
    assert merge_dicts({}, {"a": 1}) == {"a": 1}
    assert merge_dicts({"a": 1}, {}) == {"a": 1}
    assert merge_dicts({}, {}) == {}
