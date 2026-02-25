# Virtual Environments

A virtual environment is an isolated Python installation. Each project gets its own set of packages, so they don't conflict with each other.

## Why virtual environments matter

Without virtual environments:

```
Project A needs requests 2.28
Project B needs requests 2.31
→ Installing one breaks the other!
```

With virtual environments:

```
Project A → .venv/ → requests 2.28 (isolated)
Project B → .venv/ → requests 2.31 (isolated)
→ Both work fine!
```

## Creating a virtual environment

```bash
# Navigate to your project folder.
cd my_project

# Create a virtual environment named ".venv".
python -m venv .venv
```

This creates a `.venv/` folder containing a private copy of the Python interpreter and pip.

## Activating it

You must activate the environment before using it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (Git Bash)
source .venv/Scripts/activate
```

When activated, your terminal prompt changes:

```
(.venv) $ python --version
```

## Installing packages

With the environment activated, pip installs packages into `.venv/` only:

```bash
pip install requests
pip install flask
pip install pandas
```

## requirements.txt

Save your project's dependencies:

```bash
# Save current packages.
pip freeze > requirements.txt

# Install from requirements file (on another machine or in CI).
pip install -r requirements.txt
```

Example `requirements.txt`:

```
requests>=2.31
flask>=3.0
pandas>=2.2
```

## Deactivating

```bash
deactivate
```

## The workflow

Every time you start a new project:

```bash
# 1. Create the project folder.
mkdir my_project && cd my_project

# 2. Create a virtual environment.
python -m venv .venv

# 3. Activate it.
source .venv/bin/activate    # or .venv\Scripts\activate on Windows

# 4. Install packages.
pip install requests flask

# 5. Save dependencies.
pip freeze > requirements.txt

# 6. Work on your project...

# 7. When done, deactivate.
deactivate
```

## .gitignore

Never commit the `.venv/` folder to git. Add it to `.gitignore`:

```
.venv/
venv/
```

Other developers recreate it from `requirements.txt`.

## Common mistakes

**Installing globally:**
```bash
pip install requests    # Without activating venv → installs globally!
```
Always check your prompt for `(.venv)` before installing.

**Committing .venv to git:**
The `.venv/` folder is large and machine-specific. Only commit `requirements.txt`.

**Wrong Python version:**
```bash
python3 -m venv .venv    # Use python3 explicitly if needed
```

## Related exercises

- [Expansion Modules](../projects/modules/README.md) (each module uses a virtual environment)
