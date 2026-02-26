# Setting Up Python on Linux

[← Back to Platform Selector](./03_SETUP_ALL_PLATFORMS.md) | [Home](./README.md)

Other platforms: [Windows](./03_SETUP_WINDOWS.md) | [macOS](./03_SETUP_MACOS.md)

---

## Step 1 — Install Python

We recommend **Python 3.13+** for the best experience. Python 3.13 has dramatically better error messages that explain what went wrong in plain English, making debugging much easier for beginners.

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

**Fedora:**

```bash
sudo dnf install -y python3 python3-pip
```

**Arch:**

```bash
sudo pacman -S python python-pip
```

Verify the install:

```bash
python3 --version
python3 -c "print('hello from python')"
```

Expected output:

```
Python 3.x.x
hello from python
```

## Step 2 — Install an editor

**Option A (recommended): VS Code**

Install [VS Code](https://code.visualstudio.com/), then add these extensions:

- [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

**Option B (absolute beginners): Thonny**

[Thonny](https://thonny.org/) is a Python IDE designed for beginners. It comes with Python built in, has a simple interface, and includes a debugger that lets you step through code line by line. If VS Code feels overwhelming, start with Thonny and switch to VS Code later.

## Step 3 — Create your learning folder

```bash
mkdir -p "$HOME/python_sme/projects" "$HOME/python_sme/templates" "$HOME/python_sme/notes"
```

## Step 4 — Install uv (recommended package manager)

**uv** is a modern, fast replacement for pip and venv. It is used throughout this curriculum.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

Expected output: `uv x.x.x` (version number).

> **If you prefer pip:** All `uv` commands in this curriculum have pip equivalents. Replace `uv venv` with `python3 -m venv .venv` and `uv pip install` with `pip install`. Everything else stays the same.

## Step 5 — Create first project and virtual environment

```bash
cd "$HOME/python_sme/projects"
mkdir -p hello_sme
cd hello_sme
uv venv
source .venv/bin/activate
python --version
```

Expected output:

- Prompt starts with `(.venv)`.
- Python version prints.

> **pip fallback:** Replace `uv venv` with `python3 -m venv .venv`.

## Step 6 — Install pytest and run sanity checks

```bash
uv pip install pytest
pytest --version
```

> **pip fallback:** Replace `uv pip install pytest` with `python -m pip install pytest`.

Expected output: pytest version is displayed.

## Step 7 — Create first script and first test

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

```
Hello, Future Python SME
1 passed
```

## Step 8 — Credential handling

Do not embed database credentials in scripts. Use environment variables:

```bash
export APP_DB_HOST="your-sql-host"
export APP_DB_NAME="your_db"
export APP_DB_USER="your_sql_login"
```

Rules: keep passwords/tokens out of source code. Keep `.env` and secret files in `.gitignore`. Prefer approved enterprise secret storage when available. Use least privilege and read-only credentials first.

## Expected output

After completing this guide you should have:

- A working `hello_sme` project with `hello.py`, `test_hello.py`, and `.venv`.
- `python hello.py` succeeds.
- `pytest -q` succeeds.
- You can explain your credential safety rules.

## Troubleshooting

- **`python3` not found:** Reopen terminal. Confirm install finished. Reinstall Python for your distro.
- **Missing `venv` module:** Install the OS package `python3-venv` (Ubuntu/Debian: `sudo apt install python3-venv`).
- **`uv` not found:** Re-run the install command from Step 4. Or fall back to pip.
- **`pytest` not found:** Confirm venv is active. Run `uv pip install pytest` (or `pip install pytest`).
- **Permission denied on install:** Use `sudo` for system-level packages. Never use `sudo pip install` — always use a virtual environment.

## Break/fix drills

1. Deactivate venv and run `pytest` to see failure mode.
2. Rename `test_hello.py` to `hello_test.py` and observe discovery behavior.
3. Intentionally misspell `assert` and read the traceback.
4. Switch interpreter in VS Code, then switch back to the project venv.
5. Add a fake credential directly in code, then remove it and replace with env var access.

## Primary Sources

- [Using Python on Unix](https://docs.python.org/3/using/unix.html)
- [venv](https://docs.python.org/3/library/venv.html)
- [VS Code Python tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)

## Optional Resources

- [Thonny](https://thonny.org/) (beginner-friendly Python IDE)
- [Automate the Boring Stuff](https://automatetheboringstuff.com/3e/)
- [Python Tutor](https://pythontutor.com/)

---

| [← Platform Selector](./03_SETUP_ALL_PLATFORMS.md) | [Home](./README.md) | [Next →](./04_FOUNDATIONS.md) |
|:---|:---:|---:|
