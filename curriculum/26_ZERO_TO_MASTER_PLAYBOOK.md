# 26 - Zero-to-Master Playbook (Literal Step-by-Step)
Home: [README](../README.md)

Path placeholder: `<repo-root>` means the folder containing this repository's `README.md`.

This is the highest-detail execution layer in this repository. Follow it exactly.

## Who this is for
- Absolute beginners.
- Learners who need exact actions, not abstract advice.
- Learners targeting expert-level Python capability.

## What this playbook gives you
- One deterministic path from beginner to expert.
- One repeatable daily operating loop.
- One repeatable weekly recovery and improvement loop.

## Non-negotiable operating rules
1. Do not skip the `Next` sequence.
2. Do not skip break/fix drills.
3. Do not move to harder levels if current mastery checks fail.
4. Do not count reading as progress unless code was run.
5. Do not trust memory; keep written root-cause notes.

## Step 0 - Environment baseline (copy/paste)
Run this once from repo root.

Windows PowerShell:
```powershell
cd <repo-root>
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pytest ruff black
python --version
pytest --version
```

macOS/Linux:
```bash
cd <repo-root>
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest ruff black
python --version
pytest --version
```

Android (Termux, companion path):
```bash
cd /data/data/com.termux/files/home
pkg update -y
pkg install -y python
mkdir -p learn.python && cd learn.python
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest ruff black
python --version
pytest --version
```

iOS (Pyto/Pythonista, companion path):
- Run `print("hello from python")` in app console.
- Follow the first month labs in app folders.
- Move to desktop path before SQL drivers, enterprise integrations, and deployment phases.

Expected output (example):
```text
Python 3.11.x (or newer)
pytest X.Y.Z
```

Platform rule:
- Windows, macOS, Linux, Android, and iOS are all supported for fundamentals.
- Windows/macOS/Linux are the required platforms for the full enterprise path.

## Step 1 - Master path map
1. [27_DAY_0_TO_DAY_30_BOOTSTRAP.md](./27_DAY_0_TO_DAY_30_BOOTSTRAP.md)
2. [28_LEVEL_0_TO_2_DEEP_GUIDE.md](./28_LEVEL_0_TO_2_DEEP_GUIDE.md)
3. [29_LEVEL_3_TO_5_DEEP_GUIDE.md](./29_LEVEL_3_TO_5_DEEP_GUIDE.md)
4. [30_LEVEL_6_TO_8_DEEP_GUIDE.md](./30_LEVEL_6_TO_8_DEEP_GUIDE.md)
5. [31_LEVEL_9_TO_10_AND_BEYOND.md](./31_LEVEL_9_TO_10_AND_BEYOND.md)
6. [32_DAILY_SESSION_SCRIPT.md](./32_DAILY_SESSION_SCRIPT.md)
7. [33_WEEKLY_REVIEW_TEMPLATE.md](./33_WEEKLY_REVIEW_TEMPLATE.md)
8. [34_FAILURE_RECOVERY_ATLAS.md](./34_FAILURE_RECOVERY_ATLAS.md)
9. [35_CAPSTONE_BLUEPRINTS.md](./35_CAPSTONE_BLUEPRINTS.md)

## Step 2 - The mastery execution loop (copy/paste template)
Use this loop for every project at every level:

```bash
# 1) go to project
cd <repo-root>/projects/level-0/01-terminal-hello-lab

# 2) run baseline
python project.py --input data/sample_input.txt --output data/output_summary.json

# 3) run tests
pytest -q

# 4) run quality checks
ruff check .
black --check .
```

Expected output (example):
```text
... output_summary.json created ...
2 passed
All checks passed!
would reformat 0 files
```

## Step 3 - Evidence capture (required)
For each session, save:
1. Project path.
2. What you changed.
3. What you broke.
4. Root cause.
5. Fix.
6. Verification output (`pytest`, script output, or both).

Suggested note template:
```markdown
## Session YYYY-MM-DD
- Project:
- Change made:
- Failure induced:
- Root cause:
- Fix:
- Verification command(s):
- Verification output summary:
```

## Step 4 - Promotion criteria between levels
You may move up only when all are true:
- You can run baseline script without help.
- You can write and pass at least one new test.
- You can induce one failure and recover safely.
- You can explain the failure and fix in plain English.

## Time model
- Minimum progress: 6 hrs/week.
- Recommended: 8-10 hrs/week.
- Accelerated: 12+ hrs/week.

## Primary Sources
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Python docs](https://docs.python.org/3/)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)

## Optional Resources
- [Automate the Boring Stuff](https://automatetheboringstuff.com/3e/)
- [Exercism Python](https://exercism.org/tracks/python)

---

| [← Prev](25_INFINITY_MASTERY_LOOP.md) | [Home](../README.md) | [Next →](27_DAY_0_TO_DAY_30_BOOTSTRAP.md) |
|:---|:---:|---:|
