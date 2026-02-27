# Level 1 Browser Exercises

Run these Level 1 projects directly in your browser using [Pyodide](https://pyodide.org/) -- no Python installation needed.

Each exercise is a self-contained HTML file with a code editor (CodeMirror), a Run button, and a Check button that validates your solution against automated tests.

## Exercises

| # | Exercise | Concepts | File |
|---|----------|----------|------|
| 01 | [Input Validator Lab](01-input-validator.html) | String methods, validation patterns, dispatcher | `01-input-validator.html` |
| 02 | [Password Strength Checker](02-password-strength.html) | Character classification, scoring, common-password checks | `02-password-strength.html` |
| 05 | [CSV First Reader](05-csv-reader.html) | CSV parsing from strings, numeric detection, column stats | `05-csv-reader.html` |
| 09 | [JSON Settings Loader](09-json-settings.html) | json.loads(), dict merging, config validation | `09-json-settings.html` |
| 14 | [Basic Expense Tracker](14-expense-tracker.html) | Data validation, category aggregation, sorting | `14-expense-tracker.html` |

## How It Works

1. Open any HTML file in a modern browser (Chrome, Firefox, Safari, Edge).
2. Wait for the Python runtime to load (a few seconds on first visit).
3. Read the instructions in the description panel.
4. Write your solution in the code editor.
5. Click **Run** (or press Ctrl+Enter) to see output.
6. Click **Check** to validate your solution against the built-in tests.
7. Your code is auto-saved in localStorage so you can return later.

## Browser Adaptations

These exercises adapt the full project versions for browser use:

- **No file I/O** -- Projects that read CSV or JSON files instead accept string input or pre-built data structures. The same parsing and processing logic applies.
- **No imports needed** -- Standard library modules like `json` are available in Pyodide. File-system modules (`pathlib`, `csv.DictReader` with file handles) are replaced by string-based equivalents.
- **No pytest** -- The Check button runs assertion-based tests inline instead of using pytest.
- **Simplified scope** -- Each exercise focuses on the core functions from the full project. CLI argument parsing and file output are omitted.

## Relationship to Full Projects

Each browser exercise corresponds to a full project in `projects/level-1/`:

| Browser Exercise | Full Project |
|------------------|-------------|
| `01-input-validator.html` | `projects/level-1/01-input-validator-lab/` |
| `02-password-strength.html` | `projects/level-1/02-password-strength-checker/` |
| `05-csv-reader.html` | `projects/level-1/05-csv-first-reader/` |
| `09-json-settings.html` | `projects/level-1/09-json-settings-loader/` |
| `14-expense-tracker.html` | `projects/level-1/14-basic-expense-tracker/` |

The full projects include additional features: file I/O, CLI flags, pytest suites, extension challenges (Alter/Break/Fix), and teach-back questions. Once you complete a browser exercise, try the full version locally for a deeper experience.
