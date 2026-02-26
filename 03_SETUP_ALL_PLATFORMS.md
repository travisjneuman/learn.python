# 03 - Setting Up Python
Home: [README](./README.md)

## Who this is for
- Absolute beginners with zero coding experience.
- Learners using Windows, macOS, or Linux.
- Learners who want exact copy/paste setup steps and expected results.

## What you will build
- A working Python workspace.
- A virtual environment (`.venv`).
- A first script and a first passing test.
- Safe credential habits for SQL-auth workflows.

## Prerequisites
- One device with internet access.
- Permission to install apps on your device.
- 45 to 90 minutes for first-time setup.
- For database labs later in this plan: database credentials (SQLite works locally with no setup; PostgreSQL for production practice).

## Step-by-step lab pack

### Choose your platform

| Platform | Guide |
|----------|-------|
| **Windows** | [Windows Setup](./03_SETUP_WINDOWS.md) |
| **macOS** | [macOS Setup](./03_SETUP_MACOS.md) |
| **Linux** | [Linux Setup](./03_SETUP_LINUX.md) |

Each guide walks you through the complete setup: installing Python, choosing an editor, creating a project folder, setting up a virtual environment, running your first script, and running your first test.

### Mobile learners (Android/iOS)

Mobile devices are fine for early fundamentals but you will need a desktop or laptop for advanced work (drivers, ETL jobs, dashboards, CI).

**Android (Termux):**
Install [Termux](https://termux.dev/en/), then run `pkg install -y python` and follow the Linux guide — most commands are identical.

**iOS:**
Use a Python app such as [Pyto](https://pyto.app/) or [Pythonista](https://www.omz-software.com/pythonista/). These apps have built-in editors and consoles. Virtual environments are not fully supported on iOS — treat it as a learning-only path and transition to desktop before enterprise phases.

## Expected output
- A working `hello_sme` project with:
  - `hello.py`
  - `test_hello.py`
  - `.venv`
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
- `python` or `python3` not found: reopen terminal, confirm install finished, reinstall and ensure PATH/shell setup.
- See platform-specific troubleshooting in each guide: [Windows](./03_SETUP_WINDOWS.md#troubleshooting) | [macOS](./03_SETUP_MACOS.md#troubleshooting) | [Linux](./03_SETUP_LINUX.md#troubleshooting)

## Mastery check
You pass setup when you can:
- set up a fresh folder from scratch,
- create and activate an isolated environment,
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
- [Thonny](https://thonny.org/) (beginner-friendly Python IDE)
- [Termux docs](https://termux.dev/en/)
- [Pyto](https://pyto.app/)
- [Pythonista](https://www.omz-software.com/pythonista/)
- [Automate the Boring Stuff](https://automatetheboringstuff.com/3e/)
- [Python Tutor](https://pythontutor.com/)

## Next

[Next: concepts/what-is-a-variable.md →](./concepts/what-is-a-variable.md)
