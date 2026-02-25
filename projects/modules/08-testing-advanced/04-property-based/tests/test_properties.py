"""
Tests for Project 04 — Property-Based Testing

These tests use the Hypothesis library to test PROPERTIES of functions
rather than specific examples. Instead of "sort [3,1,2] and expect [1,2,3]",
we test "for ANY list of integers, sorting twice gives the same result
as sorting once."

Hypothesis generates hundreds of random inputs (including edge cases like
empty lists, single elements, negative numbers, very large numbers) and
checks that the property holds for all of them. If it finds a failure,
it "shrinks" the input to the simplest example that still fails.

Run with: pytest tests/test_properties.py -v
"""

from hypothesis import given, settings
import hypothesis.strategies as st

from project import sort_list, reverse_string, encode_decode_json, merge_dicts


# ── sort_list properties ────────────────────────────────────────────────

# WHY: Idempotency means "doing it twice is the same as doing it once."
# This is a fundamental property of sorting — if a list is already sorted,
# sorting it again should not change anything. This catches bugs where
# sorting accidentally reorders equal elements or modifies the list.

@given(st.lists(st.integers()))
def test_sort_is_idempotent(lst):
    """Sorting an already-sorted list should produce the same list."""
    sorted_once = sort_list(lst)
    sorted_twice = sort_list(sorted_once)
    assert sorted_once == sorted_twice


# WHY: Sorting should never add or remove elements. This catches bugs
# where the implementation accidentally drops duplicates or adds extras.

@given(st.lists(st.integers()))
def test_sort_preserves_length(lst):
    """Sorting should not change the number of elements."""
    assert len(sort_list(lst)) == len(lst)


# WHY: The definition of "sorted" is that each element is <= the next.
# This is the most direct property we can test — it checks the actual
# correctness of the sort, not just side effects.

@given(st.lists(st.integers()))
def test_sort_elements_are_ordered(lst):
    """Every element in the sorted list should be <= the next element."""
    result = sort_list(lst)
    for i in range(len(result) - 1):
        assert result[i] <= result[i + 1]


# ── reverse_string properties ──────────────────────────────────────────

# WHY: Reversing a string twice should give back the original. This is
# called an "involution" — a function that is its own inverse.
# Hypothesis will test this with empty strings, single characters,
# Unicode, and all sorts of inputs you might not think of.

@given(st.text())
def test_reverse_twice_is_original(s):
    """Reversing a string twice should produce the original string."""
    assert reverse_string(reverse_string(s)) == s


# WHY: Like sorting, reversing should not change the length.
# This catches subtle bugs with multi-byte Unicode characters where
# a naive reversal might corrupt the string.

@given(st.text())
def test_reverse_preserves_length(s):
    """Reversing should not change the string length."""
    assert len(reverse_string(s)) == len(s)


# ── encode_decode_json properties ───────────────────────────────────────

# WHY: The most important property of serialization is the roundtrip:
# encoding then decoding should give back exactly what you started with.
# We limit inputs to JSON-compatible types because JSON cannot represent
# all Python types (no sets, no tuples, no custom objects).

# This strategy generates JSON-compatible data structures:
# strings, ints, floats, bools, None, and nested lists/dicts of those.
json_values = st.recursive(
    # Base case: simple JSON-compatible values.
    st.none() | st.booleans() | st.integers() | st.text(),
    # Recursive case: lists and dicts containing the above.
    lambda children: st.lists(children) | st.dictionaries(st.text(), children),
    # Limit nesting depth so tests stay fast.
    max_leaves=10,
)


@given(json_values)
def test_encode_decode_roundtrip(data):
    """Encoding to JSON and decoding back should produce the original value."""
    result = encode_decode_json(data)
    assert result == data


# ── merge_dicts properties ──────────────────────────────────────────────

# WHY: When merging two dicts, every key from both inputs should appear
# in the result. This catches bugs where keys are accidentally dropped.

@given(
    st.dictionaries(st.text(min_size=1), st.integers()),
    st.dictionaries(st.text(min_size=1), st.integers()),
)
def test_merge_dicts_contains_all_keys(dict_a, dict_b):
    """The merged dict should contain every key from both inputs."""
    result = merge_dicts(dict_a, dict_b)

    # Every key from dict_a should be in the result.
    for key in dict_a:
        assert key in result

    # Every key from dict_b should be in the result.
    for key in dict_b:
        assert key in result


# WHY: The specification says dict_b wins on conflicts. This property
# checks that for every key in dict_b, the merged result has dict_b's
# value (not dict_a's). This is the core contract of the merge function.

@given(
    st.dictionaries(st.text(min_size=1), st.integers()),
    st.dictionaries(st.text(min_size=1), st.integers()),
)
def test_merge_dicts_second_wins_on_conflict(dict_a, dict_b):
    """For keys present in both dicts, dict_b's value should win."""
    result = merge_dicts(dict_a, dict_b)

    # Every value from dict_b should appear in the result.
    for key, value in dict_b.items():
        assert result[key] == value

    # Values from dict_a should appear only if the key is NOT in dict_b.
    for key, value in dict_a.items():
        if key not in dict_b:
            assert result[key] == value
