# 03 - Setup on Any Platform (Windows, macOS, Linux, Android, iOS)
Home: [README](./README.md)

## Who this is for
- Absolute beginners with zero coding experience.
- Learners using Windows, macOS, Linux, Android, or iOS.
- Learners who want exact copy/paste setup steps and expected results.

## What you will build
- A working Python workspace.
- A virtual environment (`.venv`) on desktop platforms.
- A first script and a first passing test.
- Safe credential habits for SQL-auth workflows.

## Prerequisites
- One device with internet access.
- Permission to install apps on your device.
- 45 to 90 minutes for first-time setup.
- For database labs later in this plan: database credentials (SQLite works locally with no setup; PostgreSQL for production practice).

## Step-by-step lab pack

### Step 0 - Choose your setup path
Use one of these paths:
- Path A (recommended): Windows, macOS, or Linux desktop/laptop.
- Path B (mobile companion): Android or iOS.

Important:
- You can learn basics on mobile.
- For advanced work (drivers, ETL jobs, dashboards, CI), desktop is required.

### Step 1 - Install Python

#### Windows 11
1. Download Python from [Python releases for Windows](https://www.python.org/downloads/windows/).
2. Run installer.
3. Check `Add Python to PATH`.
4. Click `Install Now`.

PowerShell verification:
```powershell
python --version
python -c "print('hello from python')"
```

Expected output:
- `Python 3.x.x`
- `hello from python`

#### macOS
Option 1 (python.org installer):
1. Download from [Python releases for macOS](https://www.python.org/downloads/macos/).
2. Run installer package.

Option 2 (Homebrew, if installed):
```bash
brew install python
```

Terminal verification:
```bash
python3 --version
python3 -c "print('hello from python')"
```

Expected output:
- `Python 3.x.x`
- `hello from python`

#### Linux (Ubuntu/Debian example)
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 --version
python3 -c "print('hello from python')"
```

Expected output:
- `Python 3.x.x`
- `hello from python`

#### Android (mobile companion)
Recommended: [Termux](https://termux.dev/en/).
```bash
pkg update -y
pkg upgrade -y
pkg install -y python
python --version
python -c "print('hello from python')"
```

Expected output:
- `Python 3.x.x`
- `hello from python`

#### iOS (mobile companion)
Use a Python app such as [Pyto](https://pyto.app/) or [Pythonista](https://www.omz-software.com/pythonista/).
1. Install app from App Store.
2. Open app console.
3. Run:
```python
print("hello from python")
```

Expected output:
- `hello from python`

### Step 2 - Install editor and tooling

#### Desktop (Windows/macOS/Linux)
Install VS Code, then add these extensions:
- [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

#### Mobile (Android/iOS)
- Use built-in editor in your Python app.
- Optional: pair with a Bluetooth keyboard.
- Mobile is acceptable for early labs, but switch to desktop by SQL/automation phases.

### Step 3 - Create your base learning folder

#### Windows PowerShell
```powershell
mkdir $HOME\Documents\python_sme
mkdir $HOME\Documents\python_sme\projects
mkdir $HOME\Documents\python_sme\templates
mkdir $HOME\Documents\python_sme\notes
```

#### macOS/Linux
```bash
mkdir -p "$HOME/python_sme/projects" "$HOME/python_sme/templates" "$HOME/python_sme/notes"
```

#### Android (Termux)
```bash
mkdir -p "$HOME/python_sme/projects" "$HOME/python_sme/templates" "$HOME/python_sme/notes"
```

#### iOS
- Create a `python_sme` folder in your Python app workspace.
- Create subfolders: `projects`, `templates`, `notes`.

### Step 4 - Create first project and virtual environment

#### Windows PowerShell
```powershell
cd $HOME\Documents\python_sme\projects
mkdir hello_sme
cd hello_sme
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

Expected output:
- Prompt starts with `(.venv)`.
- Python version prints.

#### macOS/Linux
```bash
cd "$HOME/python_sme/projects"
mkdir -p hello_sme
cd hello_sme
python3 -m venv .venv
source .venv/bin/activate
python --version
```

Expected output:
- Prompt starts with `(.venv)`.
- Python version prints.

#### Android (Termux)
```bash
cd "$HOME/python_sme/projects"
mkdir -p hello_sme
cd hello_sme
python -m venv .venv
source .venv/bin/activate
python --version
```

Expected output:
- Prompt starts with `(.venv)` if your shell prompt supports it.
- Python version prints.

#### iOS
- Some iOS Python apps do not support full `venv` behavior.
- Use a project folder and keep dependencies minimal in early labs.
- Mark iOS path as "learning-only" and move to desktop before enterprise phases.

### Step 5 - Install pytest and run sanity checks

Desktop and Android:
```bash
python -m pip install --upgrade pip
python -m pip install pytest
pytest --version
```

Windows note: same commands work inside activated PowerShell venv.

Expected output:
- pip upgrade completes.
- pytest version is displayed.

### Step 6 - Create first script and first test
Create `hello.py`:
```python
print("Hello, Future Python SME")
```

Create `test_hello.py`:
```python
def test_math_baseline():
    assert 1 + 1 == 2
```

Run:
```bash
python hello.py
pytest -q
```

Expected output:
- `Hello, Future Python SME`
- `1 passed` (or equivalent pytest success line)

### Step 7 - Corporate-safe credential handling starter rules
Do not embed database credentials in scripts.

Use environment variables:

Windows PowerShell:
```powershell
setx APP_DB_HOST "your-sql-host"
setx APP_DB_NAME "your_db"
setx APP_DB_USER "your_sql_login"
```

macOS/Linux/Android shell:
```bash
export APP_DB_HOST="your-sql-host"
export APP_DB_NAME="your_db"
export APP_DB_USER="your_sql_login"
```

Secret handling rules:
- Keep passwords/tokens out of source code.
- Keep `.env` and secret files in `.gitignore`.
- Prefer approved enterprise secret storage when available.
- Use least privilege and read-only creds first.

## Expected output
- A working `hello_sme` project with:
  - `hello.py`
  - `test_hello.py`
  - `.venv` (desktop/Android)
- `python hello.py` succeeds.
- `pytest -q` succeeds.
- You can explain your credential safety rules.

## Break/fix drills
1. Deactivate venv and run `pytest` to see failure mode.
2. Rename `test_hello.py` to `hello_test.py` and observe discovery behavior.
3. Intentionally misspell `assert` and read the traceback.
4. Switch interpreter in editor, then switch back to the project venv.
5. Add a fake credential directly in code, then remove it and replace with env var access.

## Troubleshooting
- `python` or `python3` not found:
  - Reopen terminal.
  - Confirm install finished.
  - Reinstall and ensure PATH/shell setup.
- Windows `Activate.ps1` blocked:
  - Run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- `pytest` not found:
  - Confirm venv is active.
  - Run `python -m pip install pytest`.
- macOS shows old system Python:
  - Use `python3` for install and venv creation.
- Linux missing `venv` module:
  - Install OS package `python3-venv`.
- Android package build failures:
  - Keep to pure-Python packages early.
  - Move heavy data/driver work to desktop.
- iOS package limitations:
  - Treat iOS as fundamentals-only path.
  - Transition to desktop before SQL driver and deployment phases.

## Mastery check
You pass setup when you can:
- set up a fresh folder from scratch,
- create and activate an isolated environment (or equivalent on mobile),
- run one script and one test,
- explain why credentials must not be hardcoded.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: change script output and test assertions to observe behavior.
- Build: follow exact steps and verify each expected output.
- Dissect: explain each command and what changes on disk.
- Teach-back: create a one-page setup guide for a friend on your same OS.

## Primary Sources
- [Using Python on Windows](https://docs.python.org/3/using/windows.html)
- [Using Python on macOS](https://docs.python.org/3/using/mac.html)
- [Using Python on Unix](https://docs.python.org/3/using/unix.html)
- [venv](https://docs.python.org/3/library/venv.html)
- [VS Code Python tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)

## Optional Resources
- [Termux docs](https://termux.dev/en/)
- [Pyto](https://pyto.app/)
- [Pythonista](https://www.omz-software.com/pythonista/)
- [Automate the Boring Stuff](https://automatetheboringstuff.com/3e/)
- [Python Tutor](https://pythontutor.com/)

---

| [← Prev](02_GLOSSARY.md) | [Home](README.md) | [Next →](concepts/what-is-a-variable.md) |
|:---|:---:|---:|
