"""
Solution: Validate Schema

Approach: Iterate over each key in the schema. Normalize the schema value
into a (type, required/optional) tuple. For nested dicts, recurse. Check
presence for required fields and type correctness for all present fields.
Collect all error messages in a list.
"""


def validate(data: dict, schema: dict) -> list[str]:
    errors = []

    for key, spec in schema.items():
        # Normalize spec into (expected_type, required_flag)
        if isinstance(spec, dict):
            # Nested schema -- the field must be a dict matching the sub-schema
            if key not in data:
                errors.append(f"Missing required field: {key}")
            elif not isinstance(data[key], dict):
                errors.append(f"Field '{key}' expected dict, got {type(data[key]).__name__}")
            else:
                # Recurse into nested schema
                sub_errors = validate(data[key], spec)
                errors.extend(sub_errors)
            continue

        if isinstance(spec, tuple):
            expected_type, required_flag = spec
        else:
            # Bare type defaults to required
            expected_type = spec
            required_flag = "required"

        if key not in data:
            if required_flag == "required":
                errors.append(f"Missing required field: {key}")
            # Optional and absent is fine -- skip type check
            continue

        # Field is present -- check type
        if not isinstance(data[key], expected_type):
            errors.append(
                f"Field '{key}' expected {expected_type.__name__}, "
                f"got {type(data[key]).__name__}"
            )

    return errors


if __name__ == "__main__":
    schema1 = {"name": (str, "required"), "age": (int, "required")}
    assert validate({"name": "Alice", "age": 30}, schema1) == []

    errors = validate({"name": "Alice"}, schema1)
    assert any("age" in e for e in errors)

    errors = validate({"name": "Alice", "age": "thirty"}, schema1)
    assert any("age" in e for e in errors)

    schema2 = {"name": (str, "required"), "email": (str, "optional")}
    assert validate({"name": "Alice"}, schema2) == []

    errors = validate({"name": "Alice", "email": 123}, schema2)
    assert any("email" in e for e in errors)

    schema3 = {
        "user": {
            "name": (str, "required"),
            "age": (int, "required"),
        }
    }
    assert validate({"user": {"name": "Bob", "age": 25}}, schema3) == []
    errors = validate({"user": {"name": "Bob"}}, schema3)
    assert len(errors) > 0

    schema4 = {"name": str, "count": int}
    assert validate({"name": "X", "count": 5}, schema4) == []
    errors = validate({"name": "X"}, schema4)
    assert any("count" in e for e in errors)

    print("All tests passed!")
