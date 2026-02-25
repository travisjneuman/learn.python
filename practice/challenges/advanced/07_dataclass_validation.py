"""
Challenge 07: Dataclass Validation
Difficulty: Level 6
Topic: Dataclasses with __post_init__ validation

Build dataclasses that validate their fields automatically on construction
using __post_init__. This is a stepping stone toward libraries like Pydantic.

Concepts: @dataclass, __post_init__, field(), type checking at runtime.
Review: concepts/classes-and-objects.md

Instructions:
    1. Implement `Email` — validates format (contains @ and a dot after @).
    2. Implement `DateRange` — validates start < end.
    3. Implement `User` — combines both with age validation.
"""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Email:
    """An email address with basic format validation.

    Validation in __post_init__:
    - Strip whitespace from address.
    - Must contain exactly one "@".
    - The part after "@" must contain at least one ".".
    - Raise ValueError with a descriptive message on failure.
    """

    address: str

    def __post_init__(self) -> None:
        # YOUR CODE HERE
        ...


@dataclass
class DateRange:
    """A date range where start must be strictly before end.

    Raise ValueError if start >= end.
    """

    start: date
    end: date

    def __post_init__(self) -> None:
        # YOUR CODE HERE
        ...

    @property
    def days(self) -> int:
        """Return the number of days in the range (end - start)."""
        # YOUR CODE HERE
        ...


@dataclass
class User:
    """A user with validated fields.

    Validation:
    - name must be non-empty after stripping whitespace.
    - age must be between 0 and 150 (inclusive).
    - email is an Email instance (construct from string in __post_init__
      if a plain string is passed).
    - tags defaults to an empty list (use field(default_factory=...)).

    Store the Email object (not the raw string) in self.email.
    """

    name: str
    age: int
    email: Email | str
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # YOUR CODE HERE
        ...


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Email ---
    e = Email("  user@example.com  ")
    assert e.address == "user@example.com"

    for bad in ["noatsign", "two@@ats.com", "no-dot@localhost", "@.com", ""]:
        try:
            Email(bad)
            assert False, f"Should have rejected {bad!r}"
        except ValueError:
            pass

    # --- DateRange ---
    dr = DateRange(date(2024, 1, 1), date(2024, 1, 31))
    assert dr.days == 30

    try:
        DateRange(date(2024, 6, 1), date(2024, 1, 1))
        assert False, "Should reject start >= end"
    except ValueError:
        pass

    try:
        DateRange(date(2024, 1, 1), date(2024, 1, 1))
        assert False, "Should reject start == end"
    except ValueError:
        pass

    # --- User ---
    u = User("Alice", 30, "alice@example.com")
    assert isinstance(u.email, Email)
    assert u.email.address == "alice@example.com"
    assert u.tags == []

    u2 = User("Bob", 25, Email("bob@test.org"), tags=["admin"])
    assert u2.tags == ["admin"]

    # Bad name
    try:
        User("  ", 25, "a@b.com")
        assert False, "Empty name should fail"
    except ValueError:
        pass

    # Bad age
    for bad_age in [-1, 151, 200]:
        try:
            User("X", bad_age, "x@y.com")
            assert False, f"Age {bad_age} should fail"
        except ValueError:
            pass

    # Bad email propagates
    try:
        User("X", 25, "not-an-email")
        assert False, "Bad email should fail"
    except ValueError:
        pass

    print("All tests passed.")
