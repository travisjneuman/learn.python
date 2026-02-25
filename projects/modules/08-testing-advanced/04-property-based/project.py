"""
Project 04 — Property-Based Testing

Functions that should work correctly for ANY valid input, not just the
specific examples you think of. This makes them ideal candidates for
property-based testing with Hypothesis.

A "property" is something that is always true about a function's behavior:
- Sorting a list twice gives the same result as sorting once (idempotent)
- Reversing a string twice gives back the original (involution)
- Encoding then decoding gives back the original (roundtrip)

These properties hold regardless of the specific input, which is why
Hypothesis can test them with hundreds of randomly generated inputs.
"""

import json


def sort_list(lst):
    """
    Sort a list of comparable elements in ascending order.

    Returns a new sorted list. Does not modify the original.

    Properties to test:
    - Idempotent: sort(sort(x)) == sort(x)
    - Length preserved: len(sort(x)) == len(x)
    - Ordered: every element is <= the next one
    - Elements preserved: same elements, same counts
    """
    # sorted() returns a new list. It does not modify the original.
    # This is important — functions that do not modify their inputs
    # are easier to test and reason about.
    return sorted(lst)


def reverse_string(s):
    """
    Reverse a string.

    Returns the string with characters in reverse order.

    Properties to test:
    - Involution: reverse(reverse(x)) == x
    - Length preserved: len(reverse(x)) == len(x)
    - First character becomes last: reverse(x)[0] == x[-1] (for non-empty x)
    """
    # Python's slice notation [::-1] reverses any sequence.
    # The -1 step means "go backwards through the whole thing."
    return s[::-1]


def encode_decode_json(data):
    """
    Encode data to a JSON string and decode it back.

    This is a roundtrip operation: encode then decode should give back
    the original data (for JSON-compatible types).

    Properties to test:
    - Roundtrip: decode(encode(x)) == x (for JSON-compatible x)
    - Encode produces a string: isinstance(encode(x), str)

    Note: JSON only supports strings, numbers, booleans, null, lists,
    and dicts. Python tuples become lists, and dict keys must be strings.
    """
    # json.dumps converts a Python object to a JSON string.
    encoded = json.dumps(data)

    # json.loads converts a JSON string back to a Python object.
    decoded = json.loads(encoded)

    return decoded


def merge_dicts(dict_a, dict_b):
    """
    Merge two dictionaries. If both have the same key, dict_b's value wins.

    Returns a new dictionary containing all keys from both inputs.

    Properties to test:
    - All keys from both dicts are in the result
    - Values from dict_b override dict_a for shared keys
    - Keys unique to dict_a keep their original values
    - Result length is <= len(a) + len(b)
    """
    # The ** operator unpacks a dictionary. When used in a dict literal,
    # later values override earlier ones for the same key.
    # So {**a, **b} takes all of a, then overlays all of b on top.
    return {**dict_a, **dict_b}


# ── Demo ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Property-Based Testing Demo")
    print("=" * 40)

    # sort_list demo
    print("\n--- sort_list ---")
    original = [5, 2, 8, 1, 9, 3]
    sorted_once = sort_list(original)
    sorted_twice = sort_list(sorted_once)
    print(f"  Original:     {original}")
    print(f"  Sorted once:  {sorted_once}")
    print(f"  Sorted twice: {sorted_twice}")
    print(f"  Idempotent?   {sorted_once == sorted_twice}")

    # reverse_string demo
    print("\n--- reverse_string ---")
    text = "Hello, World!"
    reversed_once = reverse_string(text)
    reversed_twice = reverse_string(reversed_once)
    print(f"  Original:      '{text}'")
    print(f"  Reversed once: '{reversed_once}'")
    print(f"  Reversed twice:'{reversed_twice}'")
    print(f"  Involution?    {text == reversed_twice}")

    # encode_decode_json demo
    print("\n--- encode_decode_json ---")
    data = {"name": "Alice", "scores": [95, 87, 92], "active": True}
    roundtrip = encode_decode_json(data)
    print(f"  Original:  {data}")
    print(f"  Roundtrip: {roundtrip}")
    print(f"  Equal?     {data == roundtrip}")

    # merge_dicts demo
    print("\n--- merge_dicts ---")
    a = {"x": 1, "y": 2, "z": 3}
    b = {"y": 20, "z": 30, "w": 40}
    merged = merge_dicts(a, b)
    print(f"  Dict A:  {a}")
    print(f"  Dict B:  {b}")
    print(f"  Merged:  {merged}")
    print(f"  B wins?  y={merged['y']}, z={merged['z']}")
