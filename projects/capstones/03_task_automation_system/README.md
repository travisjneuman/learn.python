# Capstone 03 — Task Automation System

## Brief

Build a system that watches a directory for new files and processes them according to configurable rules. Think of it as a personal automation engine: files arrive, rules fire, actions happen.

## Requirements

### Core (must have)

- **Directory watching:** Monitor a specified directory for new or modified files.
- **Rule engine:** Define rules that match files by pattern (extension, name prefix, size, etc.) and trigger actions.
- **Built-in actions:** Implement at least these actions:
  - **Move:** Move the file to a target directory
  - **Rename:** Rename the file according to a pattern (e.g., add date prefix)
  - **Transform:** For text files, apply a transformation (e.g., convert to uppercase, strip whitespace, convert CSV to JSON)
  - **Log:** Write a log entry recording what happened
- **Configuration:** Rules are defined in a configuration file (JSON or YAML), not hardcoded. The user should be able to add rules without editing Python code.
- **Logging:** All actions are logged with timestamps. The user can see what the system did and when.

### Stretch (pick at least one)

- **Plugin architecture:** Actions are dynamically loaded from a `plugins/` directory. Anyone can add a new action by dropping a Python file into the plugins folder.
- **Notification:** Send a desktop notification or write to a webhook when a rule fires.
- **Dry-run mode:** A mode that shows what the system would do without actually doing it.
- **Rule priority and conflict resolution:** When multiple rules match the same file, process them in priority order and handle conflicts.

## Constraints

- Python 3.11+. Use `watchdog` for directory monitoring or implement polling with `os.listdir()`.
- Must not lose or corrupt files. If a transform fails, the original file must remain intact.
- Must include tests for the rule matching logic and the built-in actions.

## Deliverables

- Working application code
- Tests (`python -m pytest tests/`)
- A sample configuration file with at least 3 rules
- Filled-out `notes.md` with your design decisions
- A `requirements.txt` listing any external packages

## Architecture decisions are yours

This project rewards careful upfront design. The rule engine, the action system, and the file watcher are three distinct concerns. How you connect them matters. Fill out `notes.md` before you start coding.
