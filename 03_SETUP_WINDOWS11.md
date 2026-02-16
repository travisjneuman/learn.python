# 03 - Setup on Windows 11 (Zero Experience, Step-by-Step)
Home: [README](./README.md)

## Who this is for
- First-time Python learners on Windows 11.
- Learners who want exact copy/paste setup steps.
- Anyone who has struggled with Python environment setup before.

## What you will build
- A working local Python workspace.
- A virtual environment (`.venv`).
- A tiny script and test that run successfully.

## Prerequisites
- Windows 11 admin access for installs.
- Internet access for downloads.
- VS Code installed (or permission to install).

## Step-by-step lab pack

### Step 1 - Install Python
1. Download Python from [python.org downloads](https://www.python.org/downloads/windows/).
2. Run installer.
3. Check `Add Python to PATH`.
4. Finish installation.

PowerShell verification:
```powershell
python --version
python -c "print('hello from python')"
```
Expected output:
- Version line (for example `Python 3.x.x`).
- `hello from python`.

### Step 2 - Install VS Code and extensions
Install VS Code and then these extensions:
- [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

### Step 3 - Create your base learning folder
Use File Explorer or PowerShell:
```powershell
mkdir $HOME\Documents\python_sme
mkdir $HOME\Documents\python_sme\projects
mkdir $HOME\Documents\python_sme\templates
mkdir $HOME\Documents\python_sme\notes
```

### Step 4 - Create first project
```powershell
cd $HOME\Documents\python_sme\projects
mkdir hello_sme
cd hello_sme
python -m venv .venv
```
Activate venv:
```powershell
.\.venv\Scripts\Activate.ps1
```
Expected output:
- Terminal prompt starts with `(.venv)`.

### Step 5 - Upgrade pip and install pytest
```powershell
python -m pip install --upgrade pip
python -m pip install pytest
```

### Step 6 - Create first script and test
Create `hello.py`:
```python
print("Hello, Future Python SME")
```

Create `test_hello.py`:
```python
def test_math_baseline():
    assert 1 + 1 == 2
```

Run commands:
```powershell
python hello.py
pytest -q
```
Expected output:
- Script prints greeting.
- pytest reports passing test.

### Step 7 - Corporate-safe credential handling starter rules
Do not store DB credentials directly in scripts.
Use environment variables instead:
```powershell
setx APP_DB_HOST "your-sql-host"
setx APP_DB_NAME "your_db"
setx APP_DB_USER "your_sql_login"
```
For secrets, use your approved enterprise secret process or secure local secret store. Avoid plain text files committed to Git.

## Expected output
- `hello_sme` project with `.venv`, `hello.py`, `test_hello.py`.
- Python commands and pytest run cleanly.
- Basic secure habits for DB credentials are established.

## Break/fix drills
1. Deactivate venv and run `pytest` to see the failure mode.
2. Rename `test_hello.py` to `hello_test.py` and observe discovery behavior.
3. Use a wrong Python interpreter in VS Code and correct it.

## Troubleshooting
- `python not recognized`:
  - Reopen terminal.
  - Confirm PATH.
  - Reinstall Python with PATH checkbox.
- `Activate.ps1 blocked`:
  - Run PowerShell as user and set policy for current user:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- `pytest not found`:
  - Confirm `(.venv)` is active.
  - Run `python -m pip install pytest` again.

## Mastery check
You pass setup when you can:
- create a brand-new folder,
- rebuild venv and install pytest,
- run one script and one test without looking up commands.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: change print messages and test assertions to observe failures.
- Build: follow all setup steps in strict order.
- Dissect: explain each command and what file it changes.
- Teach-back: write a one-page setup guide in your own words.

## Primary Sources
- [Using Python on Windows](https://docs.python.org/3/using/windows.html)
- [venv](https://docs.python.org/3/library/venv.html)
- [VS Code Python tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)

## Optional Resources
- [Automate the Boring Stuff](https://automatetheboringstuff.com/3e/)
- [Python Tutor](https://pythontutor.com/)

## Next
Go to [04_FOUNDATIONS.md](./04_FOUNDATIONS.md).
