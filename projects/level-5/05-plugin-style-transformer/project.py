"""Level 5 / Project 05 — Plugin-Style Transformer.

Implements a plugin architecture for data transformations. Plugins are
discovered by name, loaded from a registry, and chained together.
New transforms can be added without modifying the core engine.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# ---------- plugin interface ----------

class TransformPlugin:
    """Base class for transform plugins. Subclass and implement transform().

    WHY a base class instead of plain functions? -- The class gives each
    plugin a name and description for discovery, and the shared interface
    (transform method) lets the engine treat all plugins identically.
    This is the Template Method / Strategy pattern.
    """
    name: str = "base"
    description: str = "Base plugin"

    def transform(self, records: list[dict]) -> list[dict]:
        raise NotImplementedError

class UppercasePlugin(TransformPlugin):
    name = "uppercase"
    description = "Convert all string values to uppercase"
    def transform(self, records: list[dict]) -> list[dict]:
        return [{k: v.upper() if isinstance(v, str) else v for k, v in r.items()} for r in records]

class FilterEmptyPlugin(TransformPlugin):
    name = "filter_empty"
    description = "Remove records where all values are empty"
    def transform(self, records: list[dict]) -> list[dict]:
        return [r for r in records if any(str(v).strip() for v in r.values())]

class AddTimestampPlugin(TransformPlugin):
    name = "add_timestamp"
    description = "Add a processed_at field with current ISO timestamp"
    def transform(self, records: list[dict]) -> list[dict]:
        from datetime import datetime, timezone
        ts = datetime.now(timezone.utc).isoformat()
        return [{**r, "processed_at": ts} for r in records]

class SortByFieldPlugin(TransformPlugin):
    name = "sort_by_name"
    description = "Sort records alphabetically by 'name' field"
    def transform(self, records: list[dict]) -> list[dict]:
        return sorted(records, key=lambda r: str(r.get("name", "")).lower())

class StripWhitespacePlugin(TransformPlugin):
    name = "strip"
    description = "Strip whitespace from all string values"
    def transform(self, records: list[dict]) -> list[dict]:
        return [{k: v.strip() if isinstance(v, str) else v for k, v in r.items()} for r in records]

# ---------- plugin registry ----------

# WHY a registry dict? -- Storing plugin classes by name lets users
# specify transforms as strings in a config file ("strip,uppercase")
# without knowing the Python class names. New plugins auto-register
# by calling register_plugin at import time.
PLUGIN_REGISTRY: dict[str, type[TransformPlugin]] = {}

def register_plugin(plugin_class: type[TransformPlugin]) -> None:
    PLUGIN_REGISTRY[plugin_class.name] = plugin_class

def get_plugin(name: str) -> TransformPlugin | None:
    cls = PLUGIN_REGISTRY.get(name)
    return cls() if cls else None

def list_plugins() -> list[dict]:
    return [{"name": cls.name, "description": cls.description} for cls in PLUGIN_REGISTRY.values()]

# Register built-in plugins
for _cls in [UppercasePlugin, FilterEmptyPlugin, AddTimestampPlugin, SortByFieldPlugin, StripWhitespacePlugin]:
    register_plugin(_cls)

# ---------- pipeline ----------

def run_plugins(records: list[dict], plugin_names: list[str]) -> tuple[list[dict], list[dict]]:
    log: list[dict] = []
    current = records
    for name in plugin_names:
        plugin = get_plugin(name)
        if plugin is None:
            log.append({"plugin": name, "status": "not_found"})
            logging.warning("Plugin not found: %s", name)
            continue
        before = len(current)
        current = plugin.transform(current)
        log.append({"plugin": name, "status": "ok", "before": before, "after": len(current)})
        logging.info("Plugin '%s': %d -> %d records", name, before, len(current))
    return current, log

def run(input_path: Path, output_path: Path, plugins: list[str]) -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")
    records = json.loads(input_path.read_text(encoding="utf-8"))
    result, log = run_plugins(records, plugins)
    report = {"input_records": len(records), "output_records": len(result), "plugin_log": log, "data": result}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plugin-style data transformer")
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/transformed.json")
    parser.add_argument("--plugins", default="strip,filter_empty,uppercase", help="Comma-separated plugin names")
    parser.add_argument("--list", action="store_true", help="List available plugins")
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    if args.list:
        for p in list_plugins():
            print(f"  {p['name']}: {p['description']}")
        return
    plugins = [p.strip() for p in args.plugins.split(",")]
    report = run(Path(args.input), Path(args.output), plugins)
    print(json.dumps({"output_records": report["output_records"], "plugin_log": report["plugin_log"]}, indent=2))

if __name__ == "__main__":
    main()
