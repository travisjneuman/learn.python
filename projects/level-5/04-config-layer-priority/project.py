"""Level 5 / Project 04 — Config Layer Priority.

Implements layered configuration: environment variables override
config file values, which override hard-coded defaults. This is the
standard pattern in twelve-factor apps.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path

def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# ---------- config layers ----------

DEFAULT_CONFIG: dict = {
    "app_name": "myapp",
    "debug": False,
    "port": 8080,
    "log_level": "INFO",
    "max_retries": 3,
    "timeout_seconds": 30,
    "database_url": "sqlite:///default.db",
}


def load_file_config(path: Path) -> dict:
    """Load configuration from a JSON file. Returns empty dict if missing."""
    if not path.exists():
        logging.info("No config file at %s — using defaults only", path)
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        logging.warning("Invalid config file %s: %s", path, exc)
        return {}


def load_env_config(prefix: str = "APP_") -> dict:
    """Load configuration from environment variables.

    Only variables starting with the prefix are included.
    The prefix is stripped and the key is lowercased.
    Example: APP_PORT=9090 becomes {"port": "9090"}
    """
    env_config: dict = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            config_key = key[len(prefix):].lower()
            env_config[config_key] = value
    return env_config


def coerce_types(config: dict, defaults: dict) -> dict:
    """Coerce string config values to match the default's type.

    Environment variables are always strings, so we need to convert
    them to match the expected type (int, bool, etc.).
    """
    coerced = dict(config)
    for key, value in coerced.items():
        if key in defaults and isinstance(value, str):
            default_type = type(defaults[key])
            if default_type == bool:
                coerced[key] = value.lower() in ("true", "1", "yes")
            elif default_type == int:
                try:
                    coerced[key] = int(value)
                except ValueError:
                    logging.warning("Cannot coerce '%s'='%s' to int", key, value)
            elif default_type == float:
                try:
                    coerced[key] = float(value)
                except ValueError:
                    logging.warning("Cannot coerce '%s'='%s' to float", key, value)
    return coerced


def resolve_config(
    defaults: dict,
    file_config: dict,
    env_config: dict,
) -> dict:
    """Merge config layers: defaults < file < environment.

    Higher-priority layers override lower ones.
    """
    merged = dict(defaults)
    merged.update(file_config)
    merged.update(env_config)
    return coerce_types(merged, defaults)


def get_config_sources(
    resolved: dict, defaults: dict, file_config: dict, env_config: dict,
) -> dict[str, str]:
    """Track where each config value came from (for debugging)."""
    sources: dict[str, str] = {}
    for key in resolved:
        if key in env_config:
            sources[key] = "environment"
        elif key in file_config:
            sources[key] = "file"
        elif key in defaults:
            sources[key] = "default"
        else:
            sources[key] = "unknown"
    return sources

# ---------- runner ----------

def run(config_path: Path, output_path: Path, env_prefix: str = "APP_") -> dict:
    file_config = load_file_config(config_path)
    env_config = load_env_config(env_prefix)
    resolved = resolve_config(DEFAULT_CONFIG, file_config, env_config)
    sources = get_config_sources(resolved, DEFAULT_CONFIG, file_config, env_config)

    report = {"config": resolved, "sources": sources, "layers": {
        "defaults_used": len([s for s in sources.values() if s == "default"]),
        "file_overrides": len([s for s in sources.values() if s == "file"]),
        "env_overrides": len([s for s in sources.values() if s == "environment"]),
    }}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Config resolved: %s", report["layers"])
    return report

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Layered configuration resolver")
    parser.add_argument("--config", default="data/config.json")
    parser.add_argument("--output", default="data/resolved_config.json")
    parser.add_argument("--prefix", default="APP_")
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.config), Path(args.output), args.prefix)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
