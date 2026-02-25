"""
Solution: Plugin Loader

Approach: Use importlib.util to dynamically load a Python file as a module
without it being on sys.path. Validate that the loaded module has both a
`name` attribute (str) and a `run` attribute (callable). For loading a
directory, list .py files and attempt to load each, skipping any that fail
validation.
"""

import importlib.util
import os
from collections import namedtuple

PluginInfo = namedtuple("PluginInfo", ["name", "module", "filepath"])


def load_plugin(filepath: str) -> PluginInfo:
    """Load a Python file as a plugin module and validate it."""
    # Create a module spec from the file path
    module_name = os.path.splitext(os.path.basename(filepath))[0]
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    if spec is None or spec.loader is None:
        raise ValueError(f"Cannot load module from {filepath}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Validate required attributes
    if not hasattr(module, "name") or not isinstance(module.name, str):
        raise ValueError(f"Plugin at {filepath} missing 'name' string attribute")
    if not hasattr(module, "run") or not callable(module.run):
        raise ValueError(f"Plugin at {filepath} missing callable 'run' function")

    return PluginInfo(name=module.name, module=module, filepath=filepath)


def load_plugins(directory: str) -> list[PluginInfo]:
    """Load all valid .py plugins from a directory, skipping invalid ones."""
    plugins = []
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".py"):
            continue
        filepath = os.path.join(directory, filename)
        try:
            plugin = load_plugin(filepath)
            plugins.append(plugin)
        except ValueError:
            # Skip invalid plugins
            continue
    return plugins


def run_plugin(plugin: PluginInfo, *args, **kwargs):
    """Execute a plugin's run function and return the result."""
    return plugin.module.run(*args, **kwargs)


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        plugin_a = os.path.join(tmpdir, "greeter.py")
        with open(plugin_a, "w") as f:
            f.write('name = "greeter"\n\ndef run(who="World"):\n    return f"Hello, {who}!"\n')

        plugin_b = os.path.join(tmpdir, "adder.py")
        with open(plugin_b, "w") as f:
            f.write('name = "adder"\n\ndef run(a, b):\n    return a + b\n')

        plugin_c = os.path.join(tmpdir, "broken.py")
        with open(plugin_c, "w") as f:
            f.write('name = "broken"\n\nx = 42\n')

        readme = os.path.join(tmpdir, "README.txt")
        with open(readme, "w") as f:
            f.write("Not a plugin\n")

        p = load_plugin(plugin_a)
        assert p.name == "greeter"
        assert p.filepath == plugin_a

        assert run_plugin(p) == "Hello, World!"
        assert run_plugin(p, "Alice") == "Hello, Alice!"

        p2 = load_plugin(plugin_b)
        assert run_plugin(p2, 3, 4) == 7

        try:
            load_plugin(plugin_c)
            assert False
        except ValueError:
            pass

        plugins = load_plugins(tmpdir)
        names = {p.name for p in plugins}
        assert "greeter" in names
        assert "adder" in names
        assert "broken" not in names
        assert len(plugins) == 2

    print("All tests passed!")
