"""
Challenge: Class Registry
Difficulty: Intermediate
Concepts: decorators, classes, global state, factory pattern
Time: 35 minutes

Implement a class registry system using a decorator. The `register` decorator
should store classes in a global registry dict keyed by their class name.
The `create` function looks up a class by name and instantiates it.

Examples:
    @register
    class Dog:
        def speak(self):
            return "Woof"

    @register
    class Cat:
        def speak(self):
            return "Meow"

    pet = create("Dog")
    pet.speak()  # "Woof"
"""

# Global registry -- maps class names to class objects
_registry: dict[str, type] = {}


def register(cls: type) -> type:
    """Decorator that registers a class in the global registry. Implement this."""
    # Hint: Add cls to _registry using cls.__name__ as the key, then return cls.
    pass


def create(class_name: str, *args, **kwargs):
    """Create an instance of a registered class by name. Raise KeyError if not found. Implement this."""
    # Hint: Look up the class in _registry and call it with the given arguments.
    pass


def get_registry() -> dict[str, type]:
    """Return a copy of the current registry."""
    return dict(_registry)


# --- Tests (do not modify) ---
if __name__ == "__main__":
    _registry.clear()

    @register
    class Dog:
        def speak(self):
            return "Woof"

    @register
    class Cat:
        def speak(self):
            return "Meow"

    @register
    class Parrot:
        def __init__(self, phrase="Polly wants a cracker"):
            self.phrase = phrase

        def speak(self):
            return self.phrase

    # Test 1: Registry has all classes
    reg = get_registry()
    assert "Dog" in reg and "Cat" in reg and "Parrot" in reg, "Registry missing classes"

    # Test 2: Create instances
    dog = create("Dog")
    assert dog.speak() == "Woof", "Dog.speak() failed"

    cat = create("Cat")
    assert cat.speak() == "Meow", "Cat.speak() failed"

    # Test 3: Create with arguments
    parrot = create("Parrot", phrase="Hello!")
    assert parrot.speak() == "Hello!", "Parrot with args failed"

    # Test 4: Unknown class raises KeyError
    try:
        create("Fish")
        assert False, "Should raise KeyError for unregistered class"
    except KeyError:
        pass

    # Test 5: Decorator preserves class
    assert Dog.__name__ == "Dog", "Class name not preserved"

    print("All tests passed!")
