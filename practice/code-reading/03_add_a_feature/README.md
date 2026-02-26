# Exercise 03 — Add a Feature

This module (`codebase.py`) is a working TODO application. It supports adding, removing, toggling, and listing tasks, with JSON file persistence.

Your job is to understand the existing code and then extend it.

## Step 1 — Read and understand

Before writing any code:
1. Read every function. What data structure represents a todo item?
2. How does persistence work? When are todos saved?
3. What happens if the JSON file does not exist yet?
4. What prevents duplicate IDs?
5. Run the app (`python codebase.py`) and use it for a few minutes.

## Step 2 — Add these features

Add all three features below. For each one, modify the existing code — do not rewrite from scratch.

### Feature A: Priority levels

- Each todo should have a `priority` field: "low", "medium", or "high" (default: "medium")
- The `add` command should ask for priority
- The `list` command should show priority (e.g., `[!]` for high, `[-]` for low, `[ ]` for medium)
- Add a `list high` variant that only shows high-priority items

### Feature B: Due dates

- Each todo should have an optional `due` field (format: `YYYY-MM-DD`, or `None`)
- The `add` command should ask for an optional due date
- The `list` command should show due dates and flag overdue items
- Add a `list overdue` variant that only shows overdue items

### Feature C: Search and filter

- Add a `search <text>` command that finds todos containing the given text (case-insensitive)
- Add a `list done` command that shows only completed items
- Add a `list pending` command that shows only incomplete items

## Step 3 — Write tests

Run the existing tests first: `python -m pytest tests/`

Then add tests for your new features:
- Test adding a todo with priority
- Test adding a todo with a due date
- Test that search finds matching items and excludes non-matching ones
- Test that filter commands return correct subsets

## Rules

- Keep the existing tests passing. Do not break existing functionality.
- Follow the existing code style (function names, data structures, error handling).
- Each todo must remain a dictionary with at minimum `id`, `description`, and `done`.

## What you are practicing

- Reading and understanding unfamiliar code
- Extending code without breaking existing behavior
- Writing tests for new features alongside the code
- Making design decisions within an existing architecture
