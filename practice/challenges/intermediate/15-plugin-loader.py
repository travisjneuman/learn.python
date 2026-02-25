"""
Challenge: Plugin Loader
Difficulty: Intermediate
Concepts: importlib, dynamic loading, protocols, duck typing, file I/O
Time: 45 minutes

Build a plugin system that dynamically loads Python modules from a directory.
Each plugin module must define a `name` attribute and a `run()` function.

Implement:
1. `load_plugin(filepath)` -- load a single .py file as a plugin, validate it has
   `name` (str) and `run` (callable), return a PluginInfo namedtuple.
2. `load_plugins(directory)` -- load all .py files from a directory, skip invalid ones.
3. `run_plugin(plugin_info, *args, **kwargs)` -- execute a plugin's run function.

Since we need to test without a real filesystem of plugins, the tests create
temporary plugin files.

Examples:
    plugin = load_plugin("plugins/greeter.py")
    plugin.name       # "greeter"
    run_plugin(plugin) # calls greeter.run()
"""

import importlib.util
import os
from collections import namedtuple

PluginInfo = namedtuple("PluginInfo", ["name", "module", "filepath"])


def load_plugin(filepath: str) -> PluginInfo:
    """Load a Python file as a plugin. Raise ValueError if missing name or run. Implement this."""
    # Hint: Use importlib.util.spec_from_file_location and module_from_spec to load the file.
    pass


def load_plugins(directory: str) -> list[PluginInfo]:
    """Load all valid .py plugins from a directory. Skip invalid ones. Implement this."""
    # Hint: List .py files in the directory, call load_plugin on each, catch ValueError.
    pass


def run_plugin(plugin: PluginInfo, *args, **kwargs):
    """Execute a plugin's run function with the given arguments and return the result."""
    # Hint: Call plugin.module.run(*args, **kwargs).
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    import tempfile

    # Create temporary plugin directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a valid plugin
        plugin_a = os.path.join(tmpdir, "greeter.py")
        with open(plugin_a, "w") as f:
            f.write('name = "greeter"\n\ndef run(who="World"):\n    return f"Hello, {who}!"\n')

        # Create another valid plugin
        plugin_b = os.path.join(tmpdir, "adder.py")
        with open(plugin_b, "w") as f:
            f.write('name = "adder"\n\ndef run(a, b):\n    return a + b\n')

        # Create an invalid plugin (missing run)
        plugin_c = os.path.join(tmpdir, "broken.py")
        with open(plugin_c, "w") as f:
            f.write('name = "broken"\n\nx = 42\n')

        # Create a non-plugin file
        readme = os.path.join(tmpdir, "README.txt")
        with open(readme, "w") as f:
            f.write("Not a plugin\n")

        # Test 1: Load single valid plugin
        p = load_plugin(plugin_a)
        assert p.name == "greeter", "Plugin name failed"
        assert p.filepath == plugin_a, "Plugin filepath failed"

        # Test 2: Run plugin
        result = run_plugin(p)
        assert result == "Hello, World!", "Run plugin default failed"
        result = run_plugin(p, "Alice")
        assert result == "Hello, Alice!", "Run plugin with arg failed"

        # Test 3: Load plugin with arguments
        p2 = load_plugin(plugin_b)
        assert run_plugin(p2, 3, 4) == 7, "Adder plugin failed"

        # Test 4: Invalid plugin raises ValueError
        try:
            load_plugin(plugin_c)
            assert False, "Should raise ValueError for plugin missing run()"
        except ValueError:
            pass

        # Test 5: Load all plugins from directory
        plugins = load_plugins(tmpdir)
        names = {p.name for p in plugins}
        assert "greeter" in names, "greeter not loaded"
        assert "adder" in names, "adder not loaded"
        assert "broken" not in names, "broken should be skipped"
        assert len(plugins) == 2, f"Expected 2 plugins, got {len(plugins)}"

    print("All tests passed!")
