"""
Challenge 04: Metaclass Registry
Difficulty: Level 8
Topic: Auto-registering plugin system via metaclasses

Build a metaclass that automatically registers every subclass of a base class
into a central registry dict. This is a real pattern used in plugin systems,
serialization frameworks, and web frameworks.

Concepts: type(), __init_subclass__, metaclasses, class registries.
Review: concepts/classes-and-objects.md

Instructions:
    1. Implement `RegistryMeta` — a metaclass that maintains a class-level
       dict called `_registry` mapping class names to class objects.
    2. Implement `PluginBase` using RegistryMeta. The base class itself should
       NOT appear in the registry.
    3. Any class that inherits from PluginBase should be auto-registered.
    4. Implement `get_plugin` to look up a plugin by name.
"""


class RegistryMeta(type):
    """Metaclass that auto-registers subclasses.

    When a new class is created with this metaclass:
    - If it has no `_registry` attribute, initialize one (empty dict).
    - If the class has a base that uses RegistryMeta (i.e. it is a subclass,
      not the root), add it to _registry with key = class __name__.
    """

    # YOUR CODE HERE
    ...


class PluginBase(metaclass=RegistryMeta):
    """Base class for all plugins. Should NOT be in the registry itself."""

    @classmethod
    def get_plugin(cls, name: str) -> type:
        """Return the registered plugin class with the given *name*.

        Raises KeyError if not found.
        """
        # YOUR CODE HERE
        ...

    @classmethod
    def list_plugins(cls) -> list[str]:
        """Return sorted list of registered plugin names."""
        # YOUR CODE HERE
        ...


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Define some plugins
    class AudioPlugin(PluginBase):
        pass

    class VideoPlugin(PluginBase):
        pass

    class SubtitlePlugin(PluginBase):
        pass

    # PluginBase itself should NOT be registered
    assert "PluginBase" not in PluginBase._registry, "Base class should not be registered"

    # All subclasses should be registered
    assert PluginBase.get_plugin("AudioPlugin") is AudioPlugin
    assert PluginBase.get_plugin("VideoPlugin") is VideoPlugin
    assert PluginBase.get_plugin("SubtitlePlugin") is SubtitlePlugin

    # list_plugins
    assert PluginBase.list_plugins() == [
        "AudioPlugin",
        "SubtitlePlugin",
        "VideoPlugin",
    ]

    # KeyError for unknown
    try:
        PluginBase.get_plugin("NonExistent")
        assert False, "Should have raised KeyError"
    except KeyError:
        pass

    # Subclass of a subclass should also register
    class AdvancedAudioPlugin(AudioPlugin):
        pass

    assert PluginBase.get_plugin("AdvancedAudioPlugin") is AdvancedAudioPlugin

    print("All tests passed.")
