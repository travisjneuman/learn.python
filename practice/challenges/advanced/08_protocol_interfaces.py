"""
Challenge 08: Protocol Interfaces
Difficulty: Level 7
Topic: Structural subtyping with Protocol

Use typing.Protocol to define interfaces that any class can satisfy without
explicit inheritance. This is Python's version of "duck typing with teeth."

Concepts: Protocol, runtime_checkable, structural subtyping.
Review: concepts/classes-and-objects.md, concepts/types-and-conversions.md

Instructions:
    1. Define `Drawable` protocol with a `draw(self) -> str` method.
    2. Define `Resizable` protocol with `resize(self, factor: float) -> None`.
    3. Implement `render_all` — accepts any sequence of Drawables.
    4. Implement concrete classes that satisfy the protocols WITHOUT
       inheriting from them.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    """Anything that can be drawn to a string representation."""

    def draw(self) -> str:
        ...


@runtime_checkable
class Resizable(Protocol):
    """Anything that can be resized by a factor."""

    def resize(self, factor: float) -> None:
        ...


def render_all(shapes: list[Drawable]) -> list[str]:
    """Call draw() on each shape and return the list of strings."""
    # YOUR CODE HERE
    ...


class Circle:
    """A circle with a radius.

    draw() returns "Circle(r=<radius>)" with radius rounded to 1 decimal.
    resize() multiplies the radius by factor.
    """

    def __init__(self, radius: float) -> None:
        self.radius = radius

    def draw(self) -> str:
        # YOUR CODE HERE
        ...

    def resize(self, factor: float) -> None:
        # YOUR CODE HERE
        ...


class Rectangle:
    """A rectangle with width and height.

    draw() returns "Rectangle(<width>x<height>)" with values rounded to 1 decimal.
    resize() multiplies both dimensions by factor.
    """

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def draw(self) -> str:
        # YOUR CODE HERE
        ...

    def resize(self, factor: float) -> None:
        # YOUR CODE HERE
        ...


class TextLabel:
    """A text label. Drawable but NOT Resizable.

    draw() returns "Text('<content>')".
    """

    def __init__(self, content: str) -> None:
        self.content = content

    def draw(self) -> str:
        # YOUR CODE HERE
        ...


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    c = Circle(5.0)
    r = Rectangle(3.0, 4.0)
    t = TextLabel("Hello")

    # Protocol checks (runtime_checkable)
    assert isinstance(c, Drawable)
    assert isinstance(c, Resizable)
    assert isinstance(r, Drawable)
    assert isinstance(r, Resizable)
    assert isinstance(t, Drawable)
    assert not isinstance(t, Resizable)

    # draw
    assert c.draw() == "Circle(r=5.0)"
    assert r.draw() == "Rectangle(3.0x4.0)"
    assert t.draw() == "Text('Hello')"

    # resize
    c.resize(2.0)
    assert c.draw() == "Circle(r=10.0)"
    r.resize(0.5)
    assert r.draw() == "Rectangle(1.5x2.0)"

    # render_all
    shapes: list[Drawable] = [Circle(1.0), Rectangle(2.0, 3.0), TextLabel("Hi")]
    rendered = render_all(shapes)
    assert rendered == ["Circle(r=1.0)", "Rectangle(2.0x3.0)", "Text('Hi')"]

    # Verify no inheritance from Protocol
    assert Drawable not in type(c).__mro__
    assert Resizable not in type(c).__mro__

    print("All tests passed.")
