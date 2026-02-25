"""Tests for Reusable Utils Library."""

import pytest

from project import (
    ValidationResult,
    camel_to_snake,
    chunk,
    clamp,
    flatten,
    group_by,
    percentage,
    safe_divide,
    slugify,
    snake_to_camel,
    truncate,
    unique_ordered,
    validate_email,
    validate_url,
)


# --- String utils ---

@pytest.mark.parametrize("text,expected", [
    ("Hello World!", "hello-world"),
    ("  My Blog Post  ", "my-blog-post"),
    ("already-a-slug", "already-a-slug"),
    ("UPPER CASE", "upper-case"),
    ("special!@#chars", "specialchars"),
])
def test_slugify(text: str, expected: str) -> None:
    assert slugify(text) == expected


def test_truncate_short() -> None:
    assert truncate("Hi", 10) == "Hi"


def test_truncate_long() -> None:
    assert truncate("Hello World", 8) == "Hello..."


def test_truncate_custom_suffix() -> None:
    assert truncate("Hello World", 8, suffix="~") == "Hello W~"


@pytest.mark.parametrize("snake,camel", [
    ("my_variable", "myVariable"),
    ("hello_world_test", "helloWorldTest"),
    ("single", "single"),
])
def test_snake_to_camel(snake: str, camel: str) -> None:
    assert snake_to_camel(snake) == camel


@pytest.mark.parametrize("camel,snake", [
    ("myVariable", "my_variable"),
    ("helloWorldTest", "hello_world_test"),
    ("single", "single"),
])
def test_camel_to_snake(camel: str, snake: str) -> None:
    assert camel_to_snake(camel) == snake


# --- Number utils ---

def test_clamp() -> None:
    assert clamp(15, 0, 10) == 10
    assert clamp(-5, 0, 10) == 0
    assert clamp(5, 0, 10) == 5


def test_safe_divide() -> None:
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(10, 0) == 0.0
    assert safe_divide(10, 0, default=-1) == -1


def test_percentage() -> None:
    assert percentage(25, 100) == 25.0
    assert percentage(1, 3) == 33.3
    assert percentage(5, 0) == 0.0


# --- Collection utils ---

def test_chunk() -> None:
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert chunk([1, 2], 5) == [[1, 2]]


def test_chunk_invalid_size() -> None:
    with pytest.raises(ValueError):
        chunk([1], 0)


def test_flatten() -> None:
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]
    assert flatten([[1], 2, [3]]) == [1, 2, 3]


def test_unique_ordered() -> None:
    assert unique_ordered([3, 1, 2, 1, 3]) == [3, 1, 2]
    assert unique_ordered([]) == []


def test_group_by() -> None:
    items = [{"type": "a", "v": 1}, {"type": "b", "v": 2}, {"type": "a", "v": 3}]
    groups = group_by(items, "type")
    assert len(groups["a"]) == 2
    assert len(groups["b"]) == 1


# --- Validation utils ---

def test_validate_email_valid() -> None:
    result = validate_email("user@example.com")
    assert result.valid is True


def test_validate_email_invalid() -> None:
    result = validate_email("not-an-email")
    assert result.valid is False
    assert len(result.errors) > 0


def test_validate_url_valid() -> None:
    result = validate_url("https://example.com")
    assert result.valid is True


def test_validate_url_invalid() -> None:
    result = validate_url("ftp://bad")
    assert result.valid is False
