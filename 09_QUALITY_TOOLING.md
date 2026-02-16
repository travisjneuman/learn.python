# 09 — Quality + Tooling (What makes you “team-trusted”)

This phase is where you stop being “someone who can script” and start being “someone whose tools we can rely on”.

## Why this matters
A 200-line script that only you can run is not SME-level.
An SME delivers tools that:
- are repeatable to run
- fail safely
- produce logs
- are testable
- are readable by others

---

## 1) Virtual environments + pip (non-negotiable)
- Create venv: `python -m venv .venv` citeturn0search5
- Install in venv: `python -m pip install <pkg>` citeturn0search9

### Requirements file (simple approach)
- Create a `requirements.txt` after installs:
  - `python -m pip freeze > requirements.txt`
- Another machine can replicate:
  - `python -m pip install -r requirements.txt`

---

## 2) pyproject.toml (modern configuration)
`pyproject.toml` is the standard config file used by packaging tools and many dev tools. citeturn2search1turn2search13

You will use it to configure:
- Ruff
- Black
- pytest
- build metadata (later)

---

## 3) Formatting + linting
### Black (formatting)
Black enforces consistent formatting so code reviews focus on logic, not spacing. citeturn0search9

### Ruff (linting)
Ruff is a fast linter/formatter that can replace multiple tools. citeturn0search2turn0search6

Minimum standard:
- Format-on-save
- Ruff check in terminal before you “ship”

---

## 4) Tests with pytest
pytest “Get Started” is your baseline. citeturn2search2

Minimum standard:
- Every project has tests for:
  - parsing
  - transformations
  - “critical business rules”

Tip:
- Keep IO (Excel, SQL, SolarWinds calls) thin
- Put logic into pure functions you can unit test

---

## 5) Logging
Minimum standard:
- A log file for every run
- Summary line at end: counts + output path
- Exceptions logged with traceback

---

## 6) Project template (copy this structure)
```
my_tool/
  pyproject.toml
  README.md
  requirements.txt  (or lock approach later)
  src/
    my_tool/
      __init__.py
      main.py          # CLI entrypoint
      config.py        # load config/env
      logic.py         # pure functions
      io_excel.py      # Excel reads/writes
      io_sql.py        # SQL reads/writes
      io_sw.py         # SolarWinds calls
  tests/
    test_logic.py
```

---

## 7) “Definition of Done” for any tool
A tool is “done” when:
- You can run it from a clean machine using documented steps
- It produces output in a predictable location
- It logs start/end + counts
- It has tests for critical logic
- It fails safely (bad input doesn’t corrupt output)

Next: **[05_AUTOMATION_FILES_EXCEL.md](./05_AUTOMATION_FILES_EXCEL.md)**
