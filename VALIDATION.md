# Curriculum Validation

This document explains how the curriculum's structure and integrity are validated, what each check does, and how to run them locally.

---

## CI Pipeline

The GitHub Actions workflow (`.github/workflows/curriculum-checks.yml`) runs two job groups:

### Quick Checks (runs on every manual trigger)

These checks validate the curriculum structure without running full project tests:

| Step | Script | What It Validates |
|------|--------|-------------------|
| Markdown link checks | `tools/check_markdown_links.sh` | All internal markdown links resolve to existing files. No broken cross-references. |
| Root doc contract | `tools/check_root_doc_contract.sh` | Root-level documents (00-15) exist and contain required sections (title, navigation footer, etc.). |
| Level index contract | `tools/check_level_index_contract.sh` | Each level's `README.md` lists all project directories in that level and links resolve correctly. |
| Project README contract | `tools/check_project_readme_contract.sh` | Every project has a `README.md` with required sections: Focus, Run, Alter it, Break it, Fix it, Explain it. |
| Project Python comment/docstring contract | `tools/check_project_python_comment_contract.sh` | Every `project.py` / `exercise.py` has a module-level docstring or comment explaining what it does. |
| Portable path contract | `tools/check_portable_paths.sh` | No hardcoded absolute paths. All paths use `<repo-root>` placeholder or relative references. |
| Elite track contract | `tools/check_elite_track_contract.sh` | Elite track projects have required structure: README, project.py, tests/, architecture docs. |
| Project smoke checks | `projects/run_smoke_checks.sh` | Quick syntax check on all project.py files (imports parse, no syntax errors). |
| Elite smoke checks | `projects/run_elite_smoke_checks.sh` | Same as above but for elite track projects. |

### Full Smoke (quarterly or manual trigger with `full_smoke=true`)

| Step | Script | What It Validates |
|------|--------|-------------------|
| Full curriculum checks | `tools/run_all_curriculum_checks.sh --full` | Runs all quick checks plus full test suites across all 165+ projects. |

---

## What "Pass" Means

A passing CI run means:

- Every markdown file that should exist does exist
- Every internal link points to a real file
- Every project has the required README sections and a commented/docstringed Python file
- No hardcoded machine-specific paths exist in the curriculum
- All Python files parse without syntax errors
- (On full runs) All project test suites pass

It does **not** mean:

- The projects are pedagogically perfect
- Every explanation is maximally clear
- The curriculum covers every possible Python topic

---

## Running Checks Locally

### All quick checks at once

```bash
bash tools/run_all_curriculum_checks.sh
```

### Individual checks

```bash
# Markdown links
bash tools/check_markdown_links.sh

# Root doc structure
bash tools/check_root_doc_contract.sh

# Level index structure
bash tools/check_level_index_contract.sh

# Project README structure
bash tools/check_project_readme_contract.sh

# Python file comments/docstrings
bash tools/check_project_python_comment_contract.sh

# Portable paths (no hardcoded absolutes)
bash tools/check_portable_paths.sh

# Elite track structure
bash tools/check_elite_track_contract.sh
```

### Smoke checks

```bash
# Quick smoke (syntax check all project files)
bash projects/run_smoke_checks.sh

# Elite track smoke
bash projects/run_elite_smoke_checks.sh

# Full smoke (all projects, all tests)
bash projects/run_smoke_checks.sh --full
```

### Code quality

```bash
# Lint all Python files
ruff check .

# Run a specific project's tests
cd projects/level-0/01-terminal-hello-lab
python -m pytest tests/
```

---

## CI Schedule

- **Manual:** Trigger anytime via GitHub Actions "Run workflow" button
- **Quarterly:** Runs automatically on January 1, April 1, July 1, and October 1 at 06:00 UTC
- **Full smoke:** Only runs on the quarterly schedule or when manually triggered with `full_smoke: true`

---

| [← Prev](CONTRIBUTING.md) | [Home](README.md) | [Next →](START_HERE.md) |
|:---|:---:|---:|
