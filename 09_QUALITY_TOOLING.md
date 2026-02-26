# 09 - Quality and Tooling (From Script Writer to Team-Trusted Engineer)
Home: [README](./README.md)

## Who this is for
- Learners who can code basics and now need reliability and repeatability.
- Anyone preparing to share tools with teammates.

## What you will build
- A reusable Python project template.
- A quality workflow: format, lint, test, run, release.
- Operational logging and runbook standards.

## Prerequisites
- Foundations complete from [04_FOUNDATIONS.md](./04_FOUNDATIONS.md).
- Working local Python environment.

## Step-by-step lab pack

### Step 1 - Standard project skeleton
```text
my_tool/
  pyproject.toml
  README.md
  requirements.txt
  src/
    my_tool/
      __init__.py
      main.py
      logic.py
      io_excel.py
      io_sql.py
      io_sw.py
  tests/
    test_logic.py
```

### Step 2 - Configure pyproject.toml
Set standards for:
- Ruff checks,
- Black formatting,
- pytest defaults.

### Step 3 - Install and run tooling
```bash
python -m pip install ruff black pytest
ruff check .
black .
pytest -q
```

### Step 4 - Logging baseline
- structured run log per execution,
- summary counts,
- clear failure traces,
- stable log path.

### Step 5 - Runbook minimum
Every tool must include:
- how to run,
- required input format,
- output locations,
- failure handling,
- support owner.

### Step 6 - Quality gates before team release
Must pass before sharing:
- linter clean,
- format clean,
- tests passing,
- one end-to-end sample run,
- README run instructions validated by another person.

## Expected output
- Repeatable project template ready for all capstones.
- Consistent quality process for every script/tool.

## Break/fix drills
1. Introduce lint errors and fix them.
2. Break a test and isolate regression quickly.
3. Simulate missing input file and verify safe failure.

## Troubleshooting
- tooling conflicts:
  - centralize config in `pyproject.toml`.
- flaky tests:
  - remove hidden dependencies on file order/time.
- unreadable logs:
  - enforce stable message format and include run id.

## Mastery check
Move forward when you can:
- bootstrap a new project in under 30 minutes,
- pass all quality gates,
- hand project to another engineer who can run it.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: intentionally violate style and quality rules, then recover.
- Build: apply full template to a new mini-tool.
- Dissect: compare two project structures and justify one.
- Teach-back: explain why each quality gate prevents production pain.

## Troubleshooting matrix (common failures)
| Problem | Likely cause | First fix |
|---|---|---|
| `ModuleNotFoundError` | wrong venv/interpreter | activate `.venv`, reinstall package |
| `ruff` fails | unused imports or style issues | run `ruff check . --fix` then review |
| tests fail only on rerun | hidden state in files/data | isolate test data and clean temp outputs |
| logs missing | logger not initialized early | initialize logging before main workflow |

## Primary Sources
- [Ruff docs](https://docs.astral.sh/ruff/)
- [Black docs](https://black.readthedocs.io/en/stable/)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [Writing pyproject.toml](https://packaging.python.org/guides/writing-pyproject-toml/)

## Optional Resources
- [Pro Git Book](https://git-scm.com/book/en/v2.html)
- [GitHub Git basics](https://docs.github.com/en/get-started/getting-started-with-git)

## Next

[Next: concepts/errors-and-debugging.md →](./concepts/errors-and-debugging.md)
