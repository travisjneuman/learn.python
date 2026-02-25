# 27 - Day 0 to Day 30 Bootstrap (Absolute Beginner Survival Plan)
Home: [README](../README.md)

Path placeholder: `<repo-root>` means the folder containing this repository's `README.md`.

This plan is a literal first-month script. Execute, verify, log, repeat.

## Day 0 (setup your learning system)
1. Read [README.md](../README.md).
2. Create one notes folder (example: `study-notes/`).
3. Block 4 sessions/week in your calendar.
4. Commit to this rule: no session ends without running code.

## Days 1-3 (terminal + Python confidence)
Use commands exactly as written.

Windows PowerShell:
```powershell
cd <repo-root>
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -c "print('hello from python')"
```

macOS/Linux:
```bash
cd <repo-root>
python3 -m venv .venv
source .venv/bin/activate
python --version
python -c "print('hello from python')"
```

Android (Termux):
```bash
pkg update -y
pkg install -y python
python --version
python -c "print('hello from python')"
```

iOS (Pyto/Pythonista):
```python
print("hello from python")
```

Expected output:
```text
Python 3.11.x (or newer)
hello from python
```

Platform rule for this 30-day bootstrap:
- You can complete Days 0 to 30 on Windows, macOS, Linux, Android, or iOS.
- For later enterprise phases (SQL drivers, SolarWinds ingestion, deployment), switch to Windows/macOS/Linux.

## Days 4-7 (first script + first test)
```bash
cd <repo-root>/projects/level-0/01-terminal-hello-lab
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

Expected output:
```text
... "project_title": "Terminal Hello Lab" ...
2 passed
```

If `pytest` fails:
1. Read the first failing test name.
2. Read the traceback line in `project.py`.
3. Fix one issue only.
4. Re-run `pytest -q`.

## Week 2 (level 0 completion pattern)
Repeat this cycle for each level-0 project:

```bash
# example project; change folder for each project
cd <repo-root>/projects/level-0/02-calculator-basics
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

Break/fix drill:
1. Change one assumption in input or code.
2. Confirm behavior changes.
3. Fix and restore deterministic output.

Expected result by end of week:
- At least 5 completed level-0 projects.

## Week 3 (level 1 progression)
For each level-1 project:
1. Run baseline script.
2. Add one tiny validation improvement.
3. Add one test.
4. Re-run full test set.

Command template:
```bash
cd <repo-root>/projects/level-1/01-input-validator-lab
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

Expected result by end of week:
- You can explain `if`, loops, and functions in plain English.

## Week 4 (level 2 mini-capstone behavior)
For each level-2 project:
1. Run baseline.
2. Add one transform rule.
3. Add one failure test.
4. Verify rerun safety.

Command template:
```bash
cd <repo-root>/projects/level-2/01-dictionary-lookup-service
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

Expected result by end of week:
- You can build and stabilize a small pipeline-like script.

## End-of-month gate (must pass)
You pass month one only when you can do this without docs:
1. Create/activate `.venv`.
2. Run one project script.
3. Run tests.
4. Break behavior intentionally.
5. Fix and explain root cause in writing.

## Primary Sources
- [Using Python on Windows](https://docs.python.org/3/using/windows.html)
- [venv](https://docs.python.org/3/library/venv.html)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)

## Optional Resources
- [Python Tutor](https://pythontutor.com/)
- [Automate the Boring Stuff](https://automatetheboringstuff.com/3e/)

---

| [← Prev](26_ZERO_TO_MASTER_PLAYBOOK.md) | [Home](../README.md) | [Next →](28_LEVEL_0_TO_2_DEEP_GUIDE.md) |
|:---|:---:|---:|
