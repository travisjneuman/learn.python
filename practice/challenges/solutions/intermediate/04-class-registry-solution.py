"""
Solution: Class Registry

Approach: The register decorator adds the class to a module-level dictionary
keyed by class name, then returns the class unchanged. The create function
looks up the class and instantiates it. This is the foundation of many
plugin and factory patterns in Python.
"""

_registry: dict[str, type] = {}


def register(cls: type) -> type:
    """Store the class in the global registry keyed by its __name__."""
    _registry[cls.__name__] = cls
    return cls


def create(class_name: str, *args, **kwargs):
    """Look up a registered class by name and instantiate it."""
    if class_name not in _registry:
        raise KeyError(f"Class '{class_name}' is not registered")
    return _registry[class_name](*args, **kwargs)


def get_registry() -> dict[str, type]:
    return dict(_registry)


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

    reg = get_registry()
    assert "Dog" in reg and "Cat" in reg and "Parrot" in reg

    assert create("Dog").speak() == "Woof"
    assert create("Cat").speak() == "Meow"
    assert create("Parrot", phrase="Hello!").speak() == "Hello!"

    try:
        create("Fish")
        assert False
    except KeyError:
        pass

    assert Dog.__name__ == "Dog"
    print("All tests passed!")
