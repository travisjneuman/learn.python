# Infrastructure, Tooling & DX Audit

**Auditor:** infra-auditor (Claude Opus 4.6)
**Date:** 2026-02-25
**Scope:** CI/CD, tools, shell scripts, MkDocs, browser exercises, flashcards, progress tracking, quizzes, badges, onboarding, navigation, git setup, pyproject.toml

---

## Executive Summary

The infrastructure is remarkably comprehensive for a learning curriculum. The tooling suite includes 13 Python scripts, 7 shell scripts, a MkDocs documentation site, Pyodide browser exercises, an SM-2 spaced repetition engine, SVG badge generation, and a multi-layered CI pipeline. Quality is generally high, with good error handling, clear documentation, and cross-platform awareness.

**Key strengths:** Dual Python/shell CI checks for cross-platform support; well-structured MkDocs nav; polished browser exercise UX; thorough contract verification.

**Key gaps:** No `pyproject.toml` at repo root; shell scripts require ripgrep (not always available in CI); navigation chain mismatch between `check_root_docs.py` and `rebuild_navigation.py`; no test execution in CI; `grading_config.json` references stale project paths; Pyodide version pinned at v0.25.1 (outdated).

**Priority fixes:** 8 high, 12 medium, 9 low.

---

## 1. CI/CD Audit

### 1.1 curriculum-checks.yml

**Strengths:**
- Runs on push, PR, schedule (quarterly), and manual dispatch
- Good separation: `quick-checks` job for every commit, `full-smoke` conditionally
- Uses `uv` for fast package installation
- Syntax check via `py_compile` catches import-free errors

**Issues:**

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 1 | HIGH | **No pytest execution in CI.** The `quick-checks` job installs ruff but never installs or runs pytest. The 165 projects with tests are never validated in CI. | Add `uv pip install pytest --system` and a step: `pytest projects/ --ignore=projects/level-00-absolute-beginner -x --timeout=10` |
| 2 | HIGH | **Shell scripts require ripgrep.** CI installs `uv` and `ruff` but not `rg`. The `check_markdown_links.sh` etc. will fail unless ripgrep happens to be pre-installed on the runner. Ubuntu runners do NOT include ripgrep by default. | Either: (a) add `sudo apt-get install -y ripgrep` step, or (b) switch CI to use the Python equivalents (`check_markdown_links.py`, etc.) which have no external dependencies |
| 3 | MEDIUM | **Python syntax check uses shell `find` with pipe.** The `while read f; do python -c "import py_compile..." done` pattern fails silently on filenames with spaces and is slower than `compileall`. | Replace with: `python -m compileall -q . --exclude='.venv\|PythonBootcamp'` |
| 4 | LOW | **No caching.** The workflow installs `uv` and `ruff` from scratch on every run. | Add `actions/cache` for pip/uv to speed up CI by ~30s |
| 5 | LOW | **No markdown linting.** Structural checks are thorough, but there is no spell check or prose linting. | Consider `cspell` or `markdownlint` for catching typos in 50+ docs |

### 1.2 deploy-docs.yml

**Strengths:**
- Clean GitHub Pages deployment with artifact upload
- Path filtering (only triggers on `.md` / `mkdocs.yml` changes)
- Proper `concurrency` group prevents parallel deploys
- `--strict` build catches broken internal references

**Issues:**

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 6 | MEDIUM | **Missing `pymdown-extensions` pinning.** `pip install mkdocs-material "mkdocs-material[imaging]" pymdown-extensions` does not pin versions. A breaking change in any package will fail the build. | Pin: `mkdocs-material==9.x.x pymdown-extensions==10.x.x` (or use a `requirements-docs.txt`) |
| 7 | LOW | **No build cache.** MkDocs builds from scratch every time. | Cache the pip install step |

---

## 2. Tool Quality Audit

### 2.1 progress.py -- Rating: A-

Well-structured, clear ANSI output, good argparse interface. No external dependencies.

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 8 | MEDIUM | **`flashcard_state` path inconsistency.** `progress.py` reads from `practice/flashcards/.review-state.json`, but `spaced_repetition.py` writes to `data/flashcard_progress.json`. These are two separate state files for two separate systems, but `progress.py` only reports on the simpler one. | Either: merge the systems, or have `progress.py` report on both state files |
| 9 | LOW | **`show_next()` references `practice/flashcards/review-runner.py`** but that file's actual behavior may differ from `spaced_repetition.py`. The two flashcard runners could confuse learners. | Consolidate or clearly differentiate in the `--next` output |
| 10 | LOW | **No Windows ANSI detection.** ANSI codes work in modern Windows Terminal but not in older cmd.exe. | Add a check for Windows and enable VT processing, or use `colorama` (though "no deps" is a valid design choice) |

### 2.2 grade.py -- Rating: A-

Solid test runner with pedagogical feedback. Good timeout handling (30s).

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 11 | MEDIUM | **`grading_config.json` has stale paths.** References `projects/level-0/01-terminal-hello` but actual project is `01-terminal-hello-lab`. Similar issues for level-1 through level-5 entries. The config maps old names that no longer match the filesystem. | Regenerate `grading_config.json` to match current project directory names |

### 2.3 diagnose.py -- Rating: A

Clean interactive quiz runner. Good topic-based scoring and threshold-based recommendations. Only 5 diagnostic files exist (gate-a, level-0 through level-3), so levels 4-10 have no diagnostics.

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 12 | MEDIUM | **Only 5 of 12+ levels have diagnostics.** Levels 4-10, elite track, and modules have none. | Generate diagnostic JSON for at least levels 4-6 to cover the mid-curriculum |

### 2.4 spaced_repetition.py -- Rating: A

Excellent SM-2 implementation. Clean state management, good stats display, proper `--reset` confirmation.

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 13 | LOW | **`main()` uses manual `sys.argv` parsing instead of argparse.** Every other tool uses argparse. | Refactor to argparse for consistency (low priority, current parsing works) |

### 2.5 generate_badges.py -- Rating: B+

Generates clean SVG badges with proper ARIA labels.

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 14 | LOW | **SVG text positioning uses heuristic character widths.** The `estimate_text_width()` function approximates character widths, which can result in slightly misaligned text for certain label/message combinations. | Acceptable for generated badges; shields.io has the same challenge |
| 15 | LOW | **`--preview` flag uses `sys.argv` check instead of argparse.** | Minor inconsistency; refactor if other flags are added |

### 2.6 generate_personalized_study_plan.py -- Rating: A

Clean dataclass-based design, explicit mapping logic, good argparse validation.

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 16 | LOW | **`recommend_project_start("zero")` points to `projects/level-0/README.md`.** For someone with zero experience, `projects/level-00-absolute-beginner/README.md` would be more appropriate. | Update the `"zero"` entry to point to level-00 |

### 2.7 rebuild_navigation.py -- Rating: A-

Comprehensive navigation chain builder covering main chain, level-00, levels 0-10, and elite track.

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 17 | HIGH | **Navigation chain mismatch with `check_root_docs.py`.** The `NEXT_CHAIN` in `check_root_docs.py` has `04_FOUNDATIONS.md -> 09_QUALITY_TOOLING.md`, but `rebuild_navigation.py`'s `MAIN_CHAIN` inserts concepts and project READMEs between foundations docs. The validator and the builder disagree on what "next" means because the builder creates a richer interleaved chain while the validator checks a simpler doc-only chain. This means the validator may report false positives/negatives after running `rebuild_navigation.py`. | Synchronize the two chain definitions, or have `check_root_docs.py` read from the same `MAIN_CHAIN` source as `rebuild_navigation.py` |
| 18 | MEDIUM | **Module project navigation not built.** `rebuild_navigation.py` handles level-00, levels 0-10, and elite track, but does not build navigation for the 56 expansion module projects. | Add module chains to the script |

### 2.8 add_crossrefs.py -- Rating: A-

Idempotent cross-reference linker. Good keyword matching with level-baseline fallbacks.

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 19 | LOW | **Concept matching can be noisy.** Keywords like "file", "path", "loop" match very broadly. A project named "config-layer-priority" matches "layer" nowhere but might match "file" from unrelated README content. | Consider adding a minimum keyword count threshold (e.g., 2+ keyword matches required) |

### 2.9 check_markdown_links.py -- Rating: A

Clean, focused. Only checks `./relative.md` links. Does not check anchor links (#section) or bare URLs.

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 20 | MEDIUM | **Does not check `../` relative links.** Only matches `](./path.md)` pattern. Links like `](../README.md)` are not verified. | Extend the regex: `r"\]\((\.\.?/[^)]+\.md)\)"` |

### 2.10 run_all_checks.py -- Rating: B+

Runner that imports and executes check scripts. The `sys.exit` mocking approach works but is fragile.

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 21 | MEDIUM | **Only runs 4 of the 7+ check scripts.** Missing: `check_level_index_contract`, `check_project_python_comment_contract`, `check_elite_track_contract`. These exist as `.sh` files but have no `.py` equivalents. | Write Python equivalents for the missing 3 checks, or add them to the runner |
| 22 | LOW | **`sys.exit` mocking can catch `SystemExit` from unexpected sources.** The try/except catches all SystemExit exceptions, not just the check's intentional one. | Use `subprocess.run([sys.executable, str(script_path)])` instead for cleaner isolation |

---

## 3. Shell Script Health

### General Assessment

All 7 shell scripts follow the same pattern: `set -euo pipefail`, `command -v rg` guard, `ROOT_DIR` resolution. Consistent and well-structured.

**Cross-platform issues:**

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 23 | HIGH | **All shell scripts require ripgrep (`rg`).** This is not a standard tool on many systems (Windows, some Linux distros, some CI runners). The Python equivalents exist for 4 of 7 scripts, but 3 have no Python equivalent (`check_level_index_contract.sh`, `check_project_python_comment_contract.sh`, `check_elite_track_contract.sh`). | Write Python equivalents for the remaining 3 scripts |
| 24 | MEDIUM | **No Windows support.** Shell scripts cannot run on Windows without WSL or Git Bash. The Python equivalents partially solve this, but CI still calls the `.sh` versions. | Switch CI to use Python scripts exclusively, or add a conditional that uses Python on Windows |
| 25 | LOW | **`check_portable_paths.sh` checks both `.md` and `.py` files**, but the Python equivalent `check_portable_paths.py` only checks `.md` files. | Add `.py` file scanning to the Python version |

### Individual Script Notes

- **`check_project_python_comment_contract.sh`**: Well-designed. Checks docstring presence and minimum comment density. The `awk` usage is correct.
- **`check_elite_track_contract.sh`**: Thorough. Validates file existence, home links, headings, docstrings, and comment density.
- **`check_level_index_contract.sh`**: Good. Validates project link count (15 per level), link targets exist, next/return links present.
- **`run_all_curriculum_checks.sh`**: Clean orchestrator. `--full` flag for extended smoke tests is well-implemented.

---

## 4. MkDocs Configuration

### Rating: A-

**Strengths:**
- Comprehensive nav covering all 50+ docs, concepts, projects, practice, and guides
- Material theme with light/dark mode, search, code copy, edit links
- Good `not_in_nav` and `exclude_docs` configuration
- Mermaid diagram support via `pymdownx.superfences`
- Social plugin for Open Graph cards

**Issues:**

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 26 | MEDIUM | **`docs_dir: .` means the entire repo is the docs directory.** This works but means MkDocs processes every file in the repo, including Python scripts, JSON data, etc. The `exclude_docs` pattern helps but is a blocklist approach. | Acceptable for now, but consider a dedicated `docs/` directory if build times grow |
| 27 | MEDIUM | **No `minify` plugin.** The site could be smaller with HTML/CSS minification. | Add `mkdocs-minify-plugin` for production builds |
| 28 | LOW | **Module projects not individually linked in nav.** The nav only links to `projects/modules/README.md`, not individual module directories. Learners must navigate through the README to find specific modules. | Consider expanding the Modules section in nav to list each module |
| 29 | LOW | **Missing `navigation.tabs` feature.** With 234 nav entries, the sidebar is very long. Tabs would group top-level sections. | Add `navigation.tabs` to features for better UX at scale |

---

## 5. Browser Exercises (Pyodide)

### Rating: A-

**Strengths:**
- Tokyo Night-inspired dark theme, clean and readable
- All 15 Level 00 exercises implemented with descriptions and starter code
- CodeMirror editor with Python syntax highlighting, Ctrl+Enter to run
- `input()` patched to use browser `prompt()` dialog
- Loading overlay during Pyodide initialization
- Mobile-responsive with `@media (max-width: 600px)`
- Prev/Next navigation between exercises

**Issues:**

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 30 | HIGH | **Pyodide v0.25.1 is outdated.** Current version is v0.27.x (as of early 2026). Pinning to an old version means missing bug fixes and Python 3.12+ support. | Update `pyodide.js` URL to latest stable: `https://cdn.jsdelivr.net/pyodide/v0.27.0/full/pyodide.js` |
| 31 | MEDIUM | **No local state persistence.** Exercise progress is not saved. If a learner edits code and refreshes, their work is lost. | Add `localStorage` save/restore for each exercise's code |
| 32 | MEDIUM | **No syntax error highlighting.** Errors are shown in the output panel but not highlighted in the editor. | Consider adding CodeMirror lint addon for real-time error feedback |
| 33 | LOW | **`input()` uses browser `prompt()` dialog.** This is functional but jarring UX. A better approach would be an inline input field in the output panel. | Low priority; `prompt()` works and learners will transition to terminal quickly |
| 34 | LOW | **`back-link` in `index.html` points to `../projects/level-00-absolute-beginner/README.md`.** This works locally but may break on the MkDocs site since `browser/` is not a standard docs path. | Verify this link works in the deployed MkDocs site |

---

## 6. Flashcard System

### Rating: A

**Two runners exist:** `practice/flashcards/review-runner.py` (simple) and `tools/spaced_repetition.py` (SM-2). This is intentional but could confuse learners.

- 16 flashcard decks covering levels 00-10 and 4 modules
- SM-2 implementation is correct and well-documented
- Stats display shows interval buckets, per-deck breakdown, next review time
- `--reset` requires explicit "yes" confirmation

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 35 | MEDIUM | **Two separate flashcard runners with different state files.** `review-runner.py` uses `.review-state.json` and `spaced_repetition.py` uses `data/flashcard_progress.json`. A learner who uses both will have split progress. | Either deprecate one, or have `spaced_repetition.py` migrate/import from the simpler state file |
| 36 | LOW | **Missing flashcard decks for 8 of 12 modules.** Only web-scraping, fastapi, databases, and django modules have cards. | Generate decks for cli-tools, rest-apis, async-python, data-analysis, testing-advanced, docker-deployment, package-publishing, cloud-deployment |

---

## 7. Quiz System

### Rating: A-

- 19 concept quizzes covering all concept docs
- Shared `_quiz_helpers.py` with robust answer normalization (handles `b`, `B`, `b)`, `(b)`, `option b`, etc.)
- Good pedagogical design: explanations after every answer, score summary with review recommendations

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 37 | LOW | **Quizzes import from `_quiz_helpers` using bare import.** This requires the working directory to be `concepts/quizzes/` or the directory to be on `sys.path`. Running from repo root (`python concepts/quizzes/what-is-a-variable-quiz.py`) will fail with `ModuleNotFoundError`. | Add `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` to each quiz, or convert to a package with `__init__.py` |
| 38 | LOW | **No quiz for newer concepts.** `modern-python-tooling.md` has no matching quiz. | Add `modern-python-tooling-quiz.py` |

---

## 8. Badge System

### Rating: B+

- 15 SVG badges with green-to-gold gradient
- Proper ARIA labels for accessibility
- `badges/README.md` auto-generated with usage instructions

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 39 | LOW | **No dynamic/earned badge system.** Badges are static SVGs, not tied to actual progress. A learner can display a "Level 10" badge without completing Level 10. | Consider generating personalized badges from `progress.py` data (future feature) |

---

## 9. Onboarding Friction

### Walkthrough: New Learner Experience

**Path tested:** README -> GETTING_STARTED.md -> START_HERE.md -> Setup -> First exercise

**Findings:**

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 40 | HIGH | **`GETTING_STARTED.md` and `START_HERE.md` overlap.** GETTING_STARTED says "start with START_HERE.md", and START_HERE says "install Python" then do exercises. But GETTING_STARTED also has its own reading order that starts with START_HERE. A new learner sees two "start here" documents. | Merge into one: make START_HERE.md the canonical entry point, and GETTING_STARTED.md the "how to use the curriculum" guide (which it mostly is). Remove the duplication in reading order. |
| 41 | MEDIUM | **`GETTING_STARTED.md` nav link says "Next -> START_HERE.md" but START_HERE says "Next -> 00_COMPUTER_LITERACY_PRIMER.md".** The nav chain goes: README -> GETTING_STARTED -> START_HERE -> 00_PRIMER. But the main chain in `rebuild_navigation.py` goes: README -> START_HERE -> 00_PRIMER. GETTING_STARTED is not in the main chain. | Either add GETTING_STARTED to the main chain or remove its Prev/Next nav links |
| 42 | LOW | **No mention of browser exercises in START_HERE.md.** A true beginner who cannot install Python could use the Pyodide browser exercises immediately. | Add a "Can't install Python yet?" note with link to `browser/index.html` |

---

## 10. Navigation Chain Audit

### Main Chain (rebuild_navigation.py)

The `MAIN_CHAIN` in `rebuild_navigation.py` contains 77 entries, interleaving docs, concepts, and project index READMEs. This creates a rich learning path but diverges from the simpler doc-only chain that `check_root_docs.py` validates.

**Spot-checked links:**
- README.md -> START_HERE.md: Correct
- START_HERE.md -> 00_COMPUTER_LITERACY_PRIMER.md: Correct
- 04_FOUNDATIONS.md -> concepts/how-loops-work.md: Correct (but `check_root_docs.py` expects 04 -> 09)
- curriculum/50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md -> README.md (wraps around): Correct

### Internal Project Chains

**Level 0 internal chain spot-check:**
- level-0/README.md -> 01-terminal-hello-lab/README.md -> 02-calculator-basics/README.md: Correct
- 15-level0-mini-toolkit/README.md -> level-0/README.md (wraps back): Correct

### Issues Found

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 43 | HIGH | **Two competing chain definitions.** `check_root_docs.py` defines a `NEXT_CHAIN` dict that says `04_FOUNDATIONS.md -> 09_QUALITY_TOOLING.md`. But `rebuild_navigation.py` puts concepts and project READMEs between them. Running `rebuild_navigation.py` will cause `check_root_docs.py` to fail because the actual "Next" link in `04_FOUNDATIONS.md` now points to `concepts/how-loops-work.md`, not `09_QUALITY_TOOLING.md`. | Make `check_root_docs.py` derive its expected chain from the same `MAIN_CHAIN` list, or update its `NEXT_CHAIN` to match the current navigation. |

---

## 11. Git Setup

### .gitignore -- Rating: A

Covers `__pycache__/`, `*.pyc`, `.venv/`, `.env`, `.ipynb_checkpoints`, flashcard review state, personal learning workspace, and MkDocs build output. Clean and appropriate.

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 44 | LOW | **No `.gitattributes` file.** For a cross-platform repo used by beginners, setting `* text=auto` would prevent line ending issues. | Add `.gitattributes` with `* text=auto` and `*.py text eol=lf` |
| 45 | LOW | **Missing `data/` from .gitignore.** The `spaced_repetition.py` writes to `data/flashcard_progress.json`. If a learner commits this, it adds personal progress data to the repo. | Add `data/flashcard_progress.json` or `data/` to `.gitignore` |

---

## 12. pyproject.toml -- Should It Exist?

**Verdict: Yes.** The repo root should have a `pyproject.toml` for three reasons:

1. **Ruff configuration.** CI runs `ruff check .` but there is no `ruff.toml` or `[tool.ruff]` config. Default ruff settings may flag false positives in student code.

2. **Standardized tool runner.** A `[project.scripts]` section could expose `progress`, `grade`, `diagnose` as proper CLI commands after `pip install -e .`.

3. **Dependency declaration.** Currently there is no single file listing all dependencies (pytest, ruff, etc.). A `pyproject.toml` with optional dependency groups would help:

```toml
[project]
name = "learn-python"
version = "1.0.0"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = ["pytest", "ruff"]
docs = ["mkdocs-material", "pymdown-extensions"]
tools = ["pytest"]  # needed by grade.py

[tool.ruff]
line-length = 120
exclude = ["PythonBootcamp/", "projects/level-00-absolute-beginner/"]

[tool.ruff.lint]
select = ["E", "F", "I"]
# Be lenient on student code
ignore = ["E501"]

[tool.pytest.ini_options]
testpaths = ["projects"]
```

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 46 | HIGH | **No `pyproject.toml` at repo root.** No centralized tool configuration, no dependency declaration, no ruff config. | Create `pyproject.toml` with ruff config, optional deps, and pytest config |

---

## Summary of All Recommendations

### High Priority (fix before next release)

| # | Area | Issue | Effort |
|---|------|-------|--------|
| 1 | CI | No pytest execution in CI | 15 min |
| 2 | CI | Shell scripts need ripgrep not installed in CI | 15 min |
| 17 | Tools | Navigation chain mismatch between validator and builder | 1 hour |
| 23 | Shell | 3 shell scripts have no Python equivalents | 2 hours |
| 30 | Browser | Pyodide v0.25.1 outdated | 5 min |
| 40 | Onboarding | GETTING_STARTED.md and START_HERE.md overlap | 30 min |
| 43 | Navigation | Two competing chain definitions | 1 hour |
| 46 | Config | No pyproject.toml at repo root | 30 min |

### Medium Priority (improve in next iteration)

| # | Area | Issue | Effort |
|---|------|-------|--------|
| 3 | CI | py_compile via find+pipe is fragile | 10 min |
| 6 | CI | Unpinned MkDocs dependencies | 15 min |
| 8 | Tools | Flashcard state file inconsistency | 30 min |
| 11 | Tools | grading_config.json has stale paths | 30 min |
| 12 | Tools | Only 5 of 12+ levels have diagnostics | 2 hours |
| 18 | Tools | Module navigation not built | 1 hour |
| 20 | Tools | check_markdown_links.py misses ../ links | 15 min |
| 21 | Tools | run_all_checks.py only runs 4 of 7 checks | 1 hour |
| 24 | Shell | No Windows support in CI shell scripts | 30 min |
| 27 | MkDocs | No minify plugin | 10 min |
| 31 | Browser | No localStorage persistence for exercise code | 1 hour |
| 35 | Flashcards | Two separate runners with split state | 1 hour |
| 41 | Onboarding | GETTING_STARTED nav chain inconsistency | 15 min |

### Low Priority (polish)

| # | Area | Issue | Effort |
|---|------|-------|--------|
| 4 | CI | No pip caching | 10 min |
| 9 | Tools | Two flashcard runner commands in --next output | 10 min |
| 10 | Tools | No Windows ANSI detection | 15 min |
| 13 | Tools | spaced_repetition.py uses manual argv parsing | 20 min |
| 16 | Tools | Study plan points zero-experience to level-0 not level-00 | 5 min |
| 25 | Shell | Python portable path check misses .py files | 10 min |
| 28 | MkDocs | Modules not individually linked in nav | 20 min |
| 32 | Browser | No syntax error highlighting in editor | 1 hour |
| 36 | Flashcards | Missing decks for 8 modules | 2 hours |
| 37 | Quizzes | Quiz import requires specific working directory | 15 min |
| 38 | Quizzes | No quiz for modern-python-tooling | 30 min |
| 39 | Badges | No dynamic/earned badge system | 2 hours |
| 42 | Onboarding | No browser exercise mention in START_HERE | 5 min |
| 44 | Git | No .gitattributes file | 5 min |
| 45 | Git | data/ not in .gitignore | 5 min |

---

## Appendix: File Inventory

### Python Tools (13 files)
- `tools/progress.py` -- Progress dashboard
- `tools/grade.py` -- Auto-grading test runner
- `tools/diagnose.py` -- Diagnostic assessments
- `tools/spaced_repetition.py` -- SM-2 flashcard engine
- `tools/generate_personalized_study_plan.py` -- Study plan generator
- `tools/generate_badges.py` -- SVG badge generator
- `tools/rebuild_navigation.py` -- Navigation chain builder
- `tools/add_crossrefs.py` -- Cross-reference linker
- `tools/check_markdown_links.py` -- Link validator
- `tools/check_root_docs.py` -- Root doc contract checker
- `tools/check_project_contract.py` -- Project README contract checker
- `tools/check_portable_paths.py` -- Portable path checker
- `tools/run_all_checks.py` -- CI check runner

### Shell Scripts (8 files)
- `tools/check_markdown_links.sh`
- `tools/check_root_doc_contract.sh`
- `tools/check_level_index_contract.sh`
- `tools/check_project_readme_contract.sh`
- `tools/check_project_python_comment_contract.sh`
- `tools/check_portable_paths.sh`
- `tools/check_elite_track_contract.sh`
- `tools/run_all_curriculum_checks.sh`

### Other Infrastructure
- `.github/workflows/curriculum-checks.yml`
- `.github/workflows/deploy-docs.yml`
- `mkdocs.yml`
- `browser/index.html`, `browser/exercise.html`
- `badges/` (15 SVGs + README)
- `concepts/quizzes/_quiz_helpers.py` + 19 quiz scripts
- `tools/diagnostics/` (5 JSON diagnostic files)
- `tools/grading_config.json`
- `practice/flashcards/` (16 card decks + review-runner.py)
