# Virtual Environments

A virtual environment is an isolated Python installation. Each project gets its own set of packages, so they don't conflict with each other.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | [Videos](videos/virtual-environments.md) | [Quiz](quizzes/virtual-environments-quiz.py) | [Flashcards](../practice/flashcards/README.md) | [Diagrams](diagrams/virtual-environments.md) |

<!-- modality-hub-end -->

## Visualize It

See how Python finds packages via `sys.path` — the key to understanding environments:
[Open in Python Tutor](https://pythontutor.com/render.html#code=import%20sys%0Afor%20p%20in%20sys.path%5B%3A3%5D%3A%0A%20%20%20%20print%28p%29%0A%0Aimport%20os%0Aprint%28os.name%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

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

## Practice

- [Expansion Modules](../projects/modules/README.md)
- [Level 2 / 03 Data Cleaning Pipeline](../projects/level-2/03-data-cleaning-pipeline/README.md)
- [Level 2 / 15 Level2 Mini Capstone](../projects/level-2/15-level2-mini-capstone/README.md)
- [Level 3 / 10 Dependency Boundary Lab](../projects/level-3/10-dependency-boundary-lab/README.md)
- [Level 6 / 11 Dead Letter Row Handler](../projects/level-6/11-dead-letter-row-handler/README.md)
- [Level 6 / 15 Level6 Mini Capstone](../projects/level-6/15-level6-mini-capstone/README.md)
- [Level 7 / 08 Ingestion Observability Kit](../projects/level-7/08-ingestion-observability-kit/README.md)
- [Level 9 / 08 Change Impact Analyzer](../projects/level-9/08-change-impact-analyzer/README.md)
- [Module: 04 Fastapi Web / 03 Database Backed](../projects/modules/04-fastapi-web/03-database-backed/README.md)
- [Module: 07 Data Analysis / 05 Analysis Report](../projects/modules/07-data-analysis/05-analysis-report/README.md)
- [Module: 09 Docker Deployment / 01 First Dockerfile](../projects/modules/09-docker-deployment/01-first-dockerfile/README.md)

**Quick check:** [Take the quiz](quizzes/virtual-environments-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](decorators-explained.md) | [Home](../README.md) | [Next →](../05_AUTOMATION_FILES_EXCEL.md) |
|:---|:---:|---:|
