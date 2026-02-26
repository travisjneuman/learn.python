# Solution: Level 1 / Project 09 - JSON Settings Loader

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: JSON Settings Loader.

Load application settings from a JSON file, merge with defaults,
and validate that required keys are present.

Concepts: json module, dictionary merging, default values, validation.
"""


import argparse
import json
from pathlib import Path


# WHY DEFAULTS at module level: Default settings are configuration
# data, not logic.  Defining them at the top makes them visible,
# editable, and documentable.  Real applications often load defaults
# from a separate file or environment.
DEFAULTS = {
    "app_name": "MyApp",
    "debug": False,
    "log_level": "INFO",
    "max_retries": 3,
    "timeout_seconds": 30,
    "port": 8080,
}

# WHY REQUIRED_KEYS: Some settings have no sensible default and must
# be provided by the user.  Validating required keys early prevents
# confusing errors later when the application tries to use a missing value.
REQUIRED_KEYS = ["app_name", "port"]


# WHY load_json: This function handles two things that can go wrong
# with JSON files: the file might not exist, and the content might
# not be valid JSON.  Handling both in one place keeps the caller clean.
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
        # WHY json.loads (with 's'): loads() parses a string.
        # json.load() (no 's') reads from a file object directly.
        # Using loads() after read_text() gives us more control over
        # encoding and error handling.
        return json.loads(text)
    except json.JSONDecodeError as err:
        # WHY re-raise as ValueError: The caller does not need to
        # know about JSONDecodeError (a json-module-specific exception).
        # ValueError is more general and the message includes context.
        raise ValueError(f"Invalid JSON in {path}: {err}")


# WHY merge_settings: The merge pattern (defaults + overrides) is how
# every configuration system works.  User settings override defaults;
# anything the user does not specify keeps its default value.
def merge_settings(defaults: dict, overrides: dict) -> dict:
    """Merge overrides into defaults.

    WHY copy first? -- We do not want to modify the original defaults
    dictionary.  Copying it first keeps the original intact.
    """
    # WHY dict(defaults): This creates a shallow copy.  Without the
    # copy, merged[key] = value would modify the DEFAULTS dict itself,
    # which would affect all future calls.  This is a common mutation bug.
    merged = dict(defaults)
    for key, value in overrides.items():
        # WHY simple assignment: User values override defaults.
        # If the user sets "port": 9090, it replaces the default 8080.
        merged[key] = value
    return merged


# WHY validate_settings: Checking required keys before the application
# starts prevents cryptic KeyError crashes later.  A missing "port"
# would crash when the server tries to bind, which is much harder
# to debug than an upfront "missing required key: port" message.
def validate_settings(settings: dict, required: list[str]) -> list[str]:
    """Check that all required keys are present.

    Returns a list of missing key names (empty if all present).
    """
    # WHY return a list: Returning all missing keys at once lets the
    # user fix them all, rather than fixing one, re-running, and
    # discovering the next one.
    missing = []
    for key in required:
        if key not in settings:
            missing.append(key)
    return missing


# WHY settings_diff: Showing what changed from defaults helps users
# understand their current configuration.  "Did I set debug to True,
# or is that the default?" — the diff answers this question.
def settings_diff(defaults: dict, settings: dict) -> list[str]:
    """Show which settings differ from defaults."""
    changes = []
    for key in settings:
        if key in defaults and settings[key] != defaults[key]:
            changes.append(f"  {key}: {defaults[key]} -> {settings[key]}")
    # WHY track new keys: Settings not in defaults are custom additions.
    # Showing them separately makes it clear they are not overrides.
    for key in settings:
        if key not in defaults:
            changes.append(f"  {key}: (new) {settings[key]}")
    return changes


# WHY parse_args: Standard argparse for flexible file paths.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="JSON Settings Loader")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="Path to JSON settings file")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


# WHY main: The main function demonstrates a common real-world
# pattern: try to load user settings, fall back to defaults on error,
# merge, validate, display, and save.
def main() -> None:
    args = parse_args()

    # WHY try/except with fallback: If the settings file is broken,
    # the application can still start with defaults rather than
    # crashing completely.  This is the "fail gracefully" pattern.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `dict(defaults)` copy before merge | Prevents mutating the module-level DEFAULTS dict, which would silently corrupt future calls | `defaults.update(overrides)` — mutates in place, which is a common and subtle bug |
| `json.loads()` (string) instead of `json.load()` (file) | Reading the file first with `read_text()` gives us control over encoding; then parsing the string separately isolates the two failure modes | `json.load(open(...))` — combines file I/O and parsing, making error handling less clear |
| Return list of missing keys from `validate_settings()` | Shows all missing keys at once so the user can fix them all in one pass | Raise exception on first missing key — user has to fix one, re-run, discover the next |
| Fallback to defaults on bad JSON | Application starts with safe defaults rather than crashing; the user sees a warning and can fix their config | Crash with traceback — appropriate for development, hostile for end users |

## Alternative approaches

### Approach B: Using dictionary unpacking for merge

```python
def merge_settings_unpacking(defaults: dict, overrides: dict) -> dict:
    """Merge using the {**a, **b} syntax."""
    # WHY unpacking: The ** operator spreads dict items into a new dict.
    # When both dicts have the same key, the second dict wins.
    # This is a concise, Pythonic one-liner for shallow merging.
    return {**defaults, **overrides}
```

**Trade-off:** Dictionary unpacking (`{**defaults, **overrides}`) is more concise and Pythonic. The explicit loop version in the primary solution shows exactly what is happening: iterate keys, assign values. The loop approach is better for learning because you can step through it mentally. Use unpacking once you understand the mechanics.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Invalid JSON (missing comma, trailing comma) | `json.loads()` raises JSONDecodeError, caught and re-raised as ValueError with the filename in the message | The try/except in `load_json()` handles this; main() falls back to defaults |
| Empty settings file | `json.loads("")` raises JSONDecodeError; caught by the same error handling | Treat empty files as `{}` for a seamless fallback to all defaults |
| Missing required key after merge | `validate_settings()` returns the missing key names; main() prints a WARNING | The validation step happens after merge, so defaults cover most cases |
| Nested JSON settings (e.g., `{"database": {"host": "..."}}`) | The shallow merge replaces the entire nested dict if the user provides it, rather than merging nested keys | For nested configs, use a recursive merge function or a library like `deepmerge` (Level 3+) |

## Key takeaways

1. **The "defaults + overrides" merge pattern is universal.** Every web framework (Django settings, Flask config), CLI tool (git config), and cloud service (Terraform variables) uses this pattern: define sensible defaults, let the user override what they need.
2. **Never mutate shared data structures.** Copying the defaults dict before merging prevents a subtle bug where calling `merge_settings()` twice would accumulate overrides from both calls. This "defensive copy" pattern applies everywhere you pass dicts between functions.
3. **`json.loads()` vs `json.load()` — know the difference.** `loads()` parses a string, `load()` reads from a file object. You will encounter both in real code: `loads()` when data comes from an API response or `read_text()`, and `load()` when reading directly from `open()`.
