"""
Challenge: Validate Schema
Difficulty: Intermediate
Concepts: recursion, dictionaries, type checking, nested structures
Time: 40 minutes

Write a function that validates a data dictionary against a schema.
The schema is a dict where:
- Keys are field names.
- Values are either:
  - A Python type (int, str, float, bool, list) -- the field must be that type.
  - A nested dict -- the field must be a dict matching that sub-schema.
  - A tuple (type, "required") -- the field is required and must be that type.
  - A tuple (type, "optional") -- the field is optional but must be the correct type if present.

By default (bare type, no tuple), fields are required.

Return a list of error strings. An empty list means validation passed.

Examples:
    schema = {"name": (str, "required"), "age": (int, "required")}
    validate({"name": "Alice", "age": 30}, schema)  # []
    validate({"name": "Alice"}, schema)  # ["Missing required field: age"]
"""


def validate(data: dict, schema: dict) -> list[str]:
    """Validate data against schema. Return list of error strings. Implement this function."""
    # Hint: Iterate over schema keys. For each, check presence and type. Recurse for nested dicts.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Valid data
    schema1 = {"name": (str, "required"), "age": (int, "required")}
    assert validate({"name": "Alice", "age": 30}, schema1) == [], "Valid data failed"

    # Test 2: Missing required field
    errors = validate({"name": "Alice"}, schema1)
    assert any("age" in e for e in errors), "Missing required field not detected"

    # Test 3: Wrong type
    errors = validate({"name": "Alice", "age": "thirty"}, schema1)
    assert any("age" in e for e in errors), "Wrong type not detected"

    # Test 4: Optional field absent is OK
    schema2 = {"name": (str, "required"), "email": (str, "optional")}
    assert validate({"name": "Alice"}, schema2) == [], "Optional absent should be OK"

    # Test 5: Optional field with wrong type
    errors = validate({"name": "Alice", "email": 123}, schema2)
    assert any("email" in e for e in errors), "Optional wrong type not detected"

    # Test 6: Nested schema
    schema3 = {
        "user": {
            "name": (str, "required"),
            "age": (int, "required"),
        }
    }
    assert validate({"user": {"name": "Bob", "age": 25}}, schema3) == [], "Nested valid failed"
    errors = validate({"user": {"name": "Bob"}}, schema3)
    assert len(errors) > 0, "Nested missing field not detected"

    # Test 7: Bare type defaults to required
    schema4 = {"name": str, "count": int}
    assert validate({"name": "X", "count": 5}, schema4) == [], "Bare type valid failed"
    errors = validate({"name": "X"}, schema4)
    assert any("count" in e for e in errors), "Bare type missing field not detected"

    print("All tests passed!")
