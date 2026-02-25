"""
Challenge 12: Generic Repository
Difficulty: Level 7
Topic: Generic repository pattern with TypeVar

Build a type-safe in-memory repository using generics. The repository stores
objects that have an `id` attribute and provides CRUD operations.

Concepts: TypeVar, Generic, Protocol, bound type variables.
Review: concepts/types-and-conversions.md, concepts/classes-and-objects.md

Instructions:
    1. Define `HasId` protocol — any object with an `id: str` attribute.
    2. Implement `Repository[T]` — generic CRUD container.
    3. Implement `filtered_repo` — create a new repo from filtered items.
"""

from typing import Generic, Protocol, TypeVar, runtime_checkable


@runtime_checkable
class HasId(Protocol):
    """Protocol for objects that have a string id."""

    @property
    def id(self) -> str:
        ...


T = TypeVar("T", bound=HasId)


class Repository(Generic[T]):
    """A generic in-memory repository for objects with an `id` attribute.

    Supports: add, get, get_all, update, delete, count, contains.
    """

    def __init__(self) -> None:
        self._store: dict[str, T] = {}

    def add(self, item: T) -> None:
        """Add an item. Raise ValueError if an item with the same id exists."""
        # YOUR CODE HERE
        ...

    def get(self, item_id: str) -> T:
        """Return the item with *item_id*. Raise KeyError if not found."""
        # YOUR CODE HERE
        ...

    def get_all(self) -> list[T]:
        """Return all items sorted by id."""
        # YOUR CODE HERE
        ...

    def update(self, item: T) -> None:
        """Replace the item with matching id. Raise KeyError if not found."""
        # YOUR CODE HERE
        ...

    def delete(self, item_id: str) -> None:
        """Remove the item with *item_id*. Raise KeyError if not found."""
        # YOUR CODE HERE
        ...

    def count(self) -> int:
        """Return the number of items in the repository."""
        # YOUR CODE HERE
        ...

    def contains(self, item_id: str) -> bool:
        """Return True if an item with *item_id* exists."""
        # YOUR CODE HERE
        ...


def filtered_repo(
    source: Repository[T], predicate: "Callable[[T], bool]"
) -> Repository[T]:
    """Create a new Repository containing only items matching *predicate*."""
    # YOUR CODE HERE
    ...


# Need Callable for the type hint above
from collections.abc import Callable


# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------
class User:
    def __init__(self, id: str, name: str, active: bool = True) -> None:
        self._id = id
        self.name = name
        self.active = active

    @property
    def id(self) -> str:
        return self._id

    def __repr__(self) -> str:
        return f"User({self.id!r}, {self.name!r})"


class Product:
    def __init__(self, id: str, price: float) -> None:
        self._id = id
        self.price = price

    @property
    def id(self) -> str:
        return self._id


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Basic CRUD ---
    repo: Repository[User] = Repository()
    assert repo.count() == 0

    alice = User("1", "Alice")
    bob = User("2", "Bob", active=False)
    repo.add(alice)
    repo.add(bob)
    assert repo.count() == 2
    assert repo.contains("1")
    assert repo.get("1").name == "Alice"

    # Duplicate add
    try:
        repo.add(User("1", "Duplicate"))
        assert False, "Should reject duplicate id"
    except ValueError:
        pass

    # Update
    updated_alice = User("1", "Alice Updated")
    repo.update(updated_alice)
    assert repo.get("1").name == "Alice Updated"

    # Update non-existent
    try:
        repo.update(User("99", "Ghost"))
        assert False, "Should reject update for missing id"
    except KeyError:
        pass

    # Delete
    repo.delete("2")
    assert repo.count() == 1
    assert not repo.contains("2")

    try:
        repo.delete("99")
        assert False, "Should reject delete for missing id"
    except KeyError:
        pass

    # get_all sorted
    repo.add(User("3", "Charlie"))
    repo.add(User("2", "Bob2"))
    all_users = repo.get_all()
    assert [u.id for u in all_users] == ["1", "2", "3"]

    # --- filtered_repo ---
    full_repo: Repository[User] = Repository()
    full_repo.add(User("a", "Active1", active=True))
    full_repo.add(User("b", "Inactive", active=False))
    full_repo.add(User("c", "Active2", active=True))

    active_repo = filtered_repo(full_repo, lambda u: u.active)
    assert active_repo.count() == 2
    assert active_repo.contains("a")
    assert not active_repo.contains("b")

    # --- Different type (Product) ---
    prod_repo: Repository[Product] = Repository()
    prod_repo.add(Product("p1", 9.99))
    prod_repo.add(Product("p2", 19.99))
    assert prod_repo.get("p1").price == 9.99

    print("All tests passed.")
