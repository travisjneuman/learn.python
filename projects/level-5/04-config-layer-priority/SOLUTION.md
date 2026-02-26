# Config Layer Priority — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
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

# WHY: Hard-coded defaults ensure the application always has valid
# configuration, even when no config file or env vars are provided.
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
        # WHY: Missing config file is not an error — it just means
        # "use defaults." This makes the script work out of the box.
        logging.info("No config file at %s — using defaults only", path)
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        # WHY: A corrupt config file should not crash the app. Log the
        # error and fall back to defaults so the service stays up.
        logging.warning("Invalid config file %s: %s", path, exc)
        return {}


def load_env_config(prefix: str = "APP_") -> dict:
    """Load configuration from environment variables.

    Only variables starting with the prefix are included.
    The prefix is stripped and the key is lowercased.
    """
    env_config: dict = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            # WHY: Strip the prefix and lowercase so APP_PORT=9090
            # maps to the "port" config key, matching DEFAULT_CONFIG.
            config_key = key[len(prefix):].lower()
            env_config[config_key] = value
    return env_config


def coerce_types(config: dict, defaults: dict) -> dict:
    """Coerce string config values to match the default's type.

    WHY: Environment variables are always strings. If the default for
    "port" is int 8080 and APP_PORT="9090", we must convert "9090" to
    int 9090 or downstream code that does `port + 1` will crash.
    """
    coerced = dict(config)
    for key, value in coerced.items():
        if key in defaults and isinstance(value, str):
            default_type = type(defaults[key])
            if default_type == bool:
                # WHY: bool("false") is True in Python because any non-empty
                # string is truthy. We need explicit string matching.
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

    WHY this priority order? -- This follows the twelve-factor app
    convention: defaults are the baseline, config files customize
    per deployment, and environment variables are highest priority
    because they can be set per-container without modifying files.
    """
    merged = dict(defaults)
    merged.update(file_config)
    merged.update(env_config)
    # WHY: Coerce after merging so env var strings are converted
    # to the types expected by the rest of the application.
    return coerce_types(merged, defaults)


def get_config_sources(
    resolved: dict, defaults: dict, file_config: dict, env_config: dict,
) -> dict[str, str]:
    """Track where each config value came from (for debugging).

    WHY: When debugging "why is port 9090 instead of 8080?", knowing
    that the value came from an environment variable vs the config file
    saves significant investigation time.
    """
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Priority order: env > file > defaults | Follows the twelve-factor app convention used by Docker, Kubernetes, and Heroku. Env vars can be changed at deploy time without rebuilding or editing files. |
| Prefix-based env var filtering (`APP_`) | Prevents collisions with system environment variables like `PATH`, `HOME`, or `USER`. Every app uses its own prefix namespace. |
| Type coercion against defaults | Env vars are always strings. Without coercion, `APP_PORT=9090` would set port to the string `"9090"`, breaking any code that expects an integer. |
| Source tracking per key | When debugging a misconfigured production system, knowing which layer a value came from ("was this set in the config file or an env var?") dramatically speeds up root cause analysis. |

## Alternative Approaches

### Using a dataclass for typed configuration

```python
from dataclasses import dataclass, field

@dataclass
class AppConfig:
    app_name: str = "myapp"
    debug: bool = False
    port: int = 8080
    log_level: str = "INFO"

    @classmethod
    def from_layers(cls, file_config: dict, env_config: dict):
        merged = {}
        for f in dataclasses.fields(cls):
            merged[f.name] = env_config.get(f.name, file_config.get(f.name, f.default))
        return cls(**merged)
```

Dataclasses provide type safety and IDE autocomplete. The downside is that adding a new config key requires modifying the class definition, whereas the dict-based approach handles arbitrary keys.

## Common Pitfalls

1. **Boolean coercion from strings** — `bool("false")` is `True` in Python because any non-empty string is truthy. You must explicitly check for string values like `"true"`, `"1"`, or `"yes"` to correctly convert env var booleans.
2. **Missing prefix on env vars** — Setting `PORT=9090` instead of `APP_PORT=9090` means the variable is ignored by the prefix filter. This is a common deployment mistake that silently falls back to the default.
3. **Config file overriding env vars** — If you accidentally apply layers in the wrong order (file after env), the config file wins over environment variables, breaking the twelve-factor contract.
