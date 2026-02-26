"""Level 1 project: JSON Settings Loader.

Load application settings from a JSON file, merge with defaults,
and validate that required keys are present.

Concepts: json module, dictionary merging, default values, validation.
"""


import argparse
import json
from pathlib import Path


# Default settings that the application uses when no config is provided.
DEFAULTS = {
    "app_name": "MyApp",
    "debug": False,
    "log_level": "INFO",
    "max_retries": 3,
    "timeout_seconds": 30,
    "port": 8080,
}

# Keys that must be present in the final config.
REQUIRED_KEYS = ["app_name", "port"]


def load_json(path: Path) -> dict:
    """Load and parse a JSON file.

    WHY handle JSONDecodeError? -- If the file contains invalid JSON
    (missing commas, unquoted keys), we want a clear error message
    instead of a confusing traceback.
    """
    if not path.exists():
        raise FileNotFoundError(f"Settings file not found: {path}")

    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError as err:
        raise ValueError(f"Invalid JSON in {path}: {err}")


def merge_settings(defaults: dict, overrides: dict) -> dict:
    """Merge overrides into defaults.

    WHY copy first? -- We do not want to modify the original defaults
    dictionary.  Copying it first keeps the original intact.
    """
    merged = dict(defaults)
    for key, value in overrides.items():
        merged[key] = value
    return merged


def validate_settings(settings: dict, required: list[str]) -> list[str]:
    """Check that all required keys are present.

    Returns a list of missing key names (empty if all present).
    """
    missing = []
    for key in required:
        if key not in settings:
            missing.append(key)
    return missing


def settings_diff(defaults: dict, settings: dict) -> list[str]:
    """Show which settings differ from defaults.

    WHY a diff? -- It helps the user see what they have customised
    versus what is still at the default value.
    """
    changes = []
    for key in settings:
        if key in defaults and settings[key] != defaults[key]:
            changes.append(f"  {key}: {defaults[key]} -> {settings[key]}")
    # Also show keys not in defaults (new settings).
    for key in settings:
        if key not in defaults:
            changes.append(f"  {key}: (new) {settings[key]}")
    return changes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="JSON Settings Loader")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="Path to JSON settings file")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        user_settings = load_json(Path(args.input))
    except ValueError as err:
        print(f"ERROR: {err}")
        print("Falling back to defaults.")
        user_settings = {}

    merged = merge_settings(DEFAULTS, user_settings)
    missing = validate_settings(merged, REQUIRED_KEYS)

    print("=== Settings Loader ===\n")
    print("  Final settings:")
    for key, value in sorted(merged.items()):
        print(f"    {key}: {value}")

    if missing:
        print(f"\n  WARNING: Missing required keys: {missing}")

    changes = settings_diff(DEFAULTS, merged)
    if changes:
        print(f"\n  Changes from defaults:")
        for change in changes:
            print(change)
    else:
        print(f"\n  All settings are at defaults.")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    print(f"\n  Merged settings written to {output_path}")


if __name__ == "__main__":
    main()
