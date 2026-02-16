# 03 — Setup on Windows 11 (Step-by-step, zero-experience)

## Goal
By the end, you can:
- run Python
- create an isolated environment (venv)
- install a library with pip
- run a script from VS Code
- run a test with pytest

---

## Step 1 — Install Python
1. Go to the official Python site and download the latest stable Python. citeturn0search1
2. Run the installer.
3. **Important**: check **“Add Python to PATH”**.
4. Finish install.

### Verify Python works
Open **PowerShell** and run:
- `python --version`
- `python -c "print('hello')"`

If `python` is not recognized, PATH wasn’t set. Fix by reinstalling Python and checking that box.

---

## Step 2 — Install VS Code + Extensions
1. Install VS Code.
2. In VS Code → Extensions, install:
   - **Python** (Microsoft)
   - **Pylance** (Microsoft)
   - **Black Formatter** (Microsoft)
   - **Ruff** (VS Code extension) citeturn0search14

---

## Step 3 — Create your learning workspace folder
Create a folder (anywhere) like:
- `C:\Users\<you>\Documents\python_sme\`

Inside it create:
- `projects\`
- `templates\`
- `notes\`

---

## Step 4 — Your first project (Hello + venv)
Create a project folder:
- `projects\hello_sme\`

Open it in VS Code.

### Create a virtual environment
Open VS Code terminal (PowerShell) and run:
- `python -m venv .venv` citeturn0search5

### Activate it
PowerShell:
- `.\.venv\Scripts\Activate.ps1`

You should see `(.venv)` appear at the start of your terminal prompt.

### Upgrade pip inside the venv
- `python -m pip install --upgrade pip` citeturn0search9

---

## Step 5 — Install pytest (your first dependency)
- `python -m pip install pytest` citeturn2search2

---

## Step 6 — Create the files
Create `hello.py`:
```python
print("Hello, Future SME")
```

Create a test file: `test_hello.py`:
```python
def test_sanity():
    assert 1 + 1 == 2
```

Run:
- `python hello.py`
- `pytest`

If both work, you are ready.

---

## Step 7 — Recommended VS Code settings (minimal)
In VS Code Settings:
- Set default formatter to **Black**
- Enable format on save
- Enable Ruff linting

(You’ll configure this more in **[09_QUALITY_TOOLING.md](./09_QUALITY_TOOLING.md)**.)

Next: **[04_FOUNDATIONS.md](./04_FOUNDATIONS.md)**
