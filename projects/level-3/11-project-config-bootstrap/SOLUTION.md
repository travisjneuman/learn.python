# Project Config Bootstrap — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Project Config Bootstrap."""

from __future__ import annotations

import argparse
import json
import logging
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


# WHY: a dataclass defines the configuration SCHEMA with types
# and defaults in one place. This is the single source of truth
# for what the application expects.
@dataclass
class AppConfig:
    """Application configuration with typed fields."""
    app_name: str = "myapp"
    debug: bool = False
    log_level: str = "INFO"
    host: str = "localhost"
    port: int = 8000
    database_url: str = "sqlite:///app.db"
    secret_key: str = ""
    max_retries: int = 3
    timeout_seconds: float = 30.0


@dataclass
class ConfigSource:
    """Metadata about where a config value came from.

    WHY: when debugging "why is port 5000 instead of 8000?",
    knowing the source (file, env, default) is invaluable.
    """
    field: str
    value: str
    source: str  # "default", "file", "env", "cli"


def load_defaults() -> dict:
    """Return the default configuration as a dict.

    WHY: defaults come from the AppConfig dataclass itself.
    asdict() converts it to a plain dict for merging.
    """
    defaults = asdict(AppConfig())
    logger.debug("Loaded defaults: %d fields", len(defaults))
    return defaults


def load_from_file(path: Path) -> dict:
    """Load configuration from a JSON file.

    WHY: returns empty dict (not raises) if file is missing.
    Config files are optional — the app works with defaults alone.
    """
    if not path.exists():
        logger.warning("Config file not found: %s", path)
        return {}

    data = json.loads(path.read_text(encoding="utf-8"))
    logger.info("Loaded %d settings from %s", len(data), path)
    return data


def load_from_env(prefix: str = "APP_") -> dict:
    """Load configuration from environment variables.

    WHY: environment variables are the standard way to configure
    applications in containers and CI/CD. The prefix (APP_) prevents
    collision with system variables.
    """
    config: dict = {}

    for key, value in os.environ.items():
        if key.startswith(prefix):
            # WHY: strip the prefix and lowercase to match field names.
            # APP_LOG_LEVEL -> log_level
            field_name = key[len(prefix):].lower()
            config[field_name] = value
            logger.debug("Loaded from env: %s=%s", field_name, value)

    return config


def coerce_value(value: str, target_type: type) -> object:
    """Convert a string value to the target type.

    WHY: environment variables and CLI args are always strings.
    "8000" needs to become int(8000) and "true" needs to become
    bool(True) before assignment to a typed dataclass.
    """
    if target_type is bool:
        # WHY: bool("false") is True in Python (non-empty string).
        # We need explicit mapping of common truthy/falsy strings.
        return value.lower() in ("true", "1", "yes", "on")
    if target_type is int:
        return int(value)
    if target_type is float:
        return float(value)
    return value


def merge_configs(*sources: dict) -> dict:
    """Merge multiple config dicts with later sources taking precedence.

    WHY: the precedence order (defaults < file < env < CLI) is a
    standard pattern. Each layer can override values from the
    previous layer. Empty strings are skipped to prevent blanking
    out good defaults.
    """
    merged: dict = {}
    for source in sources:
        for key, value in source.items():
            if value is not None and value != "":
                merged[key] = value
    return merged


def build_config(
    config_file: Optional[Path] = None,
    env_prefix: str = "APP_",
    cli_overrides: Optional[dict] = None,
) -> tuple[AppConfig, list[ConfigSource]]:
    """Build final configuration from all sources.

    WHY: this function implements the full precedence chain:
    defaults < file < env < CLI. The caller gets both the final
    config AND a trace of where each value came from.
    """
    defaults = load_defaults()
    file_config = load_from_file(config_file) if config_file else {}
    env_config = load_from_env(env_prefix)
    cli_config = cli_overrides or {}

    merged = merge_configs(defaults, file_config, env_config, cli_config)

    # WHY: track which source "won" for each field. This is metadata
    # for debugging — "port=5000 came from the config file".
    sources: list[ConfigSource] = []
    for field_name in asdict(AppConfig()).keys():
        if field_name in cli_config:
            src = "cli"
        elif field_name in env_config:
            src = "env"
        elif field_name in file_config:
            src = "file"
        else:
            src = "default"
        sources.append(ConfigSource(
            field_name, str(merged.get(field_name, "")), src))

    # WHY: coerce string values to the correct types. Environment
    # variables are always strings, so "8000" must become int(8000).
    type_hints = AppConfig.__dataclass_fields__
    for field_name, field_obj in type_hints.items():
        if field_name in merged and isinstance(merged[field_name], str):
            merged[field_name] = coerce_value(
                merged[field_name], field_obj.type)

    # WHY: filter to only valid fields so unknown keys in the config
    # file do not cause TypeError when constructing AppConfig.
    valid_fields = {k: v for k, v in merged.items() if k in type_hints}
    config = AppConfig(**valid_fields)

    logger.info("Config built: %s", asdict(config))
    return config, sources


def validate_config(config: AppConfig) -> list[str]:
    """Validate a config for common issues.

    WHY: catching invalid values early (before the app starts
    listening on port -1) prevents confusing runtime errors.
    """
    issues: list[str] = []

    if config.port < 1 or config.port > 65535:
        issues.append(f"Invalid port: {config.port}")

    if config.debug and not config.secret_key:
        issues.append("Debug mode with empty secret_key is risky")

    if config.timeout_seconds <= 0:
        issues.append(f"Timeout must be positive: {config.timeout_seconds}")

    if config.max_retries < 0:
        issues.append(f"max_retries cannot be negative: {config.max_retries}")

    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project config bootstrap")

    sub = parser.add_subparsers(dest="command")

    show = sub.add_parser("show", help="Show resolved configuration")
    show.add_argument("--config-file", help="Path to config JSON file")
    show.add_argument("--env-prefix", default="APP_")

    validate = sub.add_parser("validate", help="Validate configuration")
    validate.add_argument("--config-file", help="Path to config JSON file")

    generate = sub.add_parser("generate", help="Generate a default config file")
    generate.add_argument("output", help="Output file path")

    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "show":
        config_file = Path(args.config_file) if args.config_file else None
        config, sources = build_config(config_file, args.env_prefix)
        print(json.dumps(asdict(config), indent=2))
        print("\nSources:")
        for s in sources:
            print(f"  {s.field}: {s.value} (from {s.source})")

    elif args.command == "validate":
        config_file = Path(args.config_file) if args.config_file else None
        config, _ = build_config(config_file)
        issues = validate_config(config)
        if issues:
            for issue in issues:
                print(f"  [WARNING] {issue}")
        else:
            print("Configuration is valid.")

    elif args.command == "generate":
        defaults = asdict(AppConfig())
        Path(args.output).write_text(
            json.dumps(defaults, indent=2), encoding="utf-8")
        print(f"Default config written to {args.output}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Precedence chain: defaults < file < env < CLI | Industry standard. Defaults ensure the app always works. Files customise deployments. Env vars handle containers/CI. CLI flags override everything for one-off runs. |
| `coerce_value` with explicit bool handling | `bool("false")` is `True` in Python (non-empty string is truthy). Explicit string matching prevents this trap for environment variables. |
| `ConfigSource` tracing | When port is 5000 and you expected 8000, knowing "it came from the config file" immediately points you to the right place. |
| `validate_config` as a separate step | Validation is distinct from loading. You might want to load a config, display it, and THEN validate — or skip validation for debugging. |
| Filter unknown keys with `valid_fields` | A config file with a typo ("prot" instead of "port") should be ignored or warned about, not crash with `TypeError: unexpected keyword argument`. |

## Alternative Approaches

### Using `pydantic-settings` for config

```python
from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    app_name: str = "myapp"
    debug: bool = False
    port: int = 8000

    class Config:
        env_prefix = "APP_"
```

**Trade-off:** Pydantic-settings handles file loading, env vars, type coercion, and validation automatically in a few lines. But it is a third-party dependency and hides the mechanics. Understanding the manual approach makes pydantic-settings feel transparent instead of magical.

## Common Pitfalls

1. **`bool("false")` is `True`** — This is the most common config bug. Any non-empty string is truthy in Python. The `coerce_value` function handles this correctly by checking against a list of known truthy strings ("true", "1", "yes", "on").

2. **Environment variables leaking between tests** — If test A sets `APP_PORT=9000` and test B does not clean it up, test B reads the wrong port. Use pytest's `monkeypatch.setenv` which auto-reverts after each test.

3. **Config file overwriting defaults with empty strings** — If the JSON file has `{"secret_key": ""}`, the merge function should NOT overwrite the default with an empty string. The `merge_configs` function skips empty strings for this reason.
