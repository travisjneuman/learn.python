"""
Challenge 10: Descriptor Protocol
Difficulty: Level 8
Topic: Build a custom descriptor for validated attributes

Descriptors power Python's property(), classmethod(), and staticmethod().
In this challenge you will build your own descriptor that validates
attribute values on set.

Concepts: __get__, __set__, __set_name__, descriptor protocol.
Review: concepts/classes-and-objects.md

Instructions:
    1. Implement `Validated` — a descriptor that runs a validator function
       on every assignment.
    2. Implement `RangeChecked` — a descriptor for numeric ranges.
    3. Use them in a `Config` class.
"""

from collections.abc import Callable
from typing import Any


class Validated:
    """A descriptor that validates values using a provided function.

    Usage:
        class Foo:
            name = Validated(validator=lambda v: isinstance(v, str) and len(v) > 0,
                             error_msg="name must be a non-empty string")

    The validator is called with the new value and must return True/False.
    On False, raise ValueError with the error_msg.
    Store values in the instance's __dict__ using the attribute name.
    """

    def __init__(self, validator: Callable[[Any], bool], error_msg: str) -> None:
        self.validator = validator
        self.error_msg = error_msg
        self.attr_name: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        # YOUR CODE HERE
        ...

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        # YOUR CODE HERE (return the descriptor itself if obj is None)
        ...

    def __set__(self, obj: Any, value: Any) -> None:
        # YOUR CODE HERE
        ...


class RangeChecked:
    """A descriptor that ensures a numeric value is within [min_val, max_val].

    Raise ValueError if the value is outside the range.
    Raise TypeError if the value is not int or float.
    """

    def __init__(self, min_val: float, max_val: float) -> None:
        self.min_val = min_val
        self.max_val = max_val
        self.attr_name: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        # YOUR CODE HERE
        ...

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        # YOUR CODE HERE
        ...

    def __set__(self, obj: Any, value: Any) -> None:
        # YOUR CODE HERE
        ...


class Config:
    """Application config using descriptors for validation.

    Attributes:
        app_name: non-empty string
        port: integer between 1 and 65535
        debug: boolean only
    """

    app_name = Validated(
        validator=lambda v: isinstance(v, str) and len(v.strip()) > 0,
        error_msg="app_name must be a non-empty string",
    )
    port = RangeChecked(min_val=1, max_val=65535)
    debug = Validated(
        validator=lambda v: isinstance(v, bool),
        error_msg="debug must be a boolean",
    )

    def __init__(self, app_name: str, port: int, debug: bool = False) -> None:
        self.app_name = app_name
        self.port = port
        self.debug = debug


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Basic Validated descriptor ---
    cfg = Config("MyApp", 8080)
    assert cfg.app_name == "MyApp"
    assert cfg.port == 8080
    assert cfg.debug is False

    cfg.debug = True
    assert cfg.debug is True

    # Invalid app_name
    try:
        cfg.app_name = ""
        assert False, "Empty app_name should fail"
    except ValueError:
        pass

    try:
        cfg.app_name = "   "
        assert False, "Whitespace-only app_name should fail"
    except ValueError:
        pass

    # Invalid debug
    try:
        cfg.debug = 1  # not a bool
        assert False, "Non-bool debug should fail"
    except ValueError:
        pass

    # --- RangeChecked ---
    cfg.port = 443
    assert cfg.port == 443

    try:
        cfg.port = 0
        assert False, "Port 0 should fail"
    except ValueError:
        pass

    try:
        cfg.port = 70000
        assert False, "Port 70000 should fail"
    except ValueError:
        pass

    try:
        cfg.port = "80"  # type: ignore[assignment]
        assert False, "String port should fail"
    except TypeError:
        pass

    # Multiple instances should not share state
    cfg2 = Config("Other", 3000, debug=True)
    assert cfg2.app_name == "Other"
    assert cfg.app_name == "MyApp"

    # Class-level access returns the descriptor
    assert isinstance(Config.__dict__["app_name"], Validated)

    print("All tests passed.")
