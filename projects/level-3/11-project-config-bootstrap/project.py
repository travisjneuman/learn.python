"""Level 3 project: Project Config Bootstrap.

Loads configuration from multiple sources (defaults, file, environment)
with proper precedence and validation.

Skills practiced: dataclasses, typing, os.environ, JSON config files,
logging, argparse, environment variable handling.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


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
    """Metadata about where a config value came from."""
    field: str
    value: str
    source: str  # "default", "file", "env", "cli"


def load_defaults() -> dict:
    """Return the default configuration as a dict."""
    defaults = asdict(AppConfig())
    logger.debug("Loaded defaults: %d fields", len(defaults))
    return defaults


def load_from_file(path: Path) -> dict:
    """Load configuration from a JSON file.

    Returns empty dict if file doesn't exist.
    """
    if not path.exists():
        logger.warning("Config file not found: %s", path)
        return {}

    data = json.loads(path.read_text(encoding="utf-8"))
    logger.info("Loaded %d settings from %s", len(data), path)
    return data


def load_from_env(prefix: str = "APP_") -> dict:
    """Load configuration from environment variables.

    Looks for vars like APP_DEBUG, APP_PORT, APP_LOG_LEVEL.
    Converts the env var name to the config field name:
    APP_LOG_LEVEL -> log_level
    """
    config: dict = {}

    for key, value in os.environ.items():
        if key.startswith(prefix):
            field_name = key[len(prefix):].lower()
            config[field_name] = value
            logger.debug("Loaded from env: %s=%s", field_name, value)

    return config


def coerce_value(value: str, target_type: type) -> object:
    """Convert a string value to the target type.

    Handles bool, int, float, str.
    """
    if target_type is bool:
        return value.lower() in ("true", "1", "yes", "on")
    if target_type is int:
        return int(value)
    if target_type is float:
        return float(value)
    return value


def merge_configs(*sources: dict) -> dict:
    """Merge multiple config dicts with later sources taking precedence.

    merge_configs(defaults, file_config, env_config, cli_config)
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

    Precedence: defaults < file < env < CLI
    Returns the config and a trace of where each value came from.
    """
    defaults = load_defaults()
    file_config = load_from_file(config_file) if config_file else {}
    env_config = load_from_env(env_prefix)
    cli_config = cli_overrides or {}

    merged = merge_configs(defaults, file_config, env_config, cli_config)

    # Track sources for debugging.
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
        sources.append(ConfigSource(field_name, str(merged.get(field_name, "")), src))

    # Coerce types to match AppConfig fields.
    type_hints = AppConfig.__dataclass_fields__
    for field_name, field_obj in type_hints.items():
        if field_name in merged and isinstance(merged[field_name], str):
            merged[field_name] = coerce_value(merged[field_name], field_obj.type)

    # Build the final dataclass.
    valid_fields = {k: v for k, v in merged.items() if k in type_hints}
    config = AppConfig(**valid_fields)

    logger.info("Config built: %s", asdict(config))
    return config, sources


def validate_config(config: AppConfig) -> list[str]:
    """Validate a config for common issues."""
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
    """Build CLI parser."""
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
    """Entry point."""
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
        Path(args.output).write_text(json.dumps(defaults, indent=2), encoding="utf-8")
        print(f"Default config written to {args.output}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
