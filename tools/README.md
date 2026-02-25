# Curriculum Tools

Scripts that support the learn.python curriculum. Learner tools help you track progress and find your starting point. Maintainer tools keep the curriculum's cross-references and navigation links consistent.

**Prerequisites:** Python 3.11+, pytest (for `grade.py`), ripgrep (`rg`) and bash (for shell-based checks).

---

## For Learners

### grade.py

Run project tests and get friendly, educational feedback — not just pass/fail.

```bash
python tools/grade.py projects/level-0/01-terminal-hello-lab/
python tools/grade.py --level 0
python tools/grade.py --level 0 --summary
python tools/grade.py --modules
python tools/grade.py --all
python tools/grade.py --all -v        # verbose: show failure details
```

Runs pytest on the target project(s), counts passed/failed tests, prints a score bar, and links failures to concept docs for review. Uses `tools/grading_config.json` for concept hints.

### diagnose.py

Interactive diagnostic assessments that help you find where to start or identify knowledge gaps.

```bash
python tools/diagnose.py              # list available diagnostics
python tools/diagnose.py gate-a       # setup readiness check
python tools/diagnose.py level-0      # terminal/IO readiness
python tools/diagnose.py level-1      # functions readiness
```

Loads question banks from `tools/diagnostics/`, runs a quiz in the terminal, scores by topic, and recommends whether to skip ahead, start the level, or review first.

### progress.py

Visual dashboard that scans the repo to show learning progress based on actual work done.

```bash
python tools/progress.py              # overall progress bars
python tools/progress.py --detail level-0   # per-project breakdown
python tools/progress.py --streak     # 30-day commit heatmap
python tools/progress.py --next       # what to work on next
```

Detects code files, test files, and notes in each project directory. The streak view reads git history to show your practice consistency.

### generate_personalized_study_plan.py

Generates a markdown study plan tailored to your experience, schedule, and goals.

```bash
python tools/generate_personalized_study_plan.py \
    --hours-per-week 10 --learning-mode hybrid \
    --confidence medium --experience beginner --goal full_stack

python tools/generate_personalized_study_plan.py \
    --hours-per-week 5 --learning-mode play \
    --confidence low --experience zero --goal automation \
    --output my-plan.md
```

All arguments are required except `--stuck-area` (defaults to `none`) and `--output` (prints to stdout if omitted). The output includes a starting doc, project ladder entry point, weekly session pattern, priority doc chain, and remediation actions.

---

## For Maintainers

### add_crossrefs.py

Adds "Related Concepts" sections to project READMEs and "Practice This" sections to concept docs.

```bash
python tools/add_crossrefs.py
```

Idempotent — detects existing sections and skips them. Uses keyword matching and level/module mappings to determine which concepts are relevant to each project. Also links to quizzes, flashcards, and coding challenges where available.

### rebuild_navigation.py

Rebuilds the complete prev/home/next navigation chain across every curriculum document.

```bash
python tools/rebuild_navigation.py
```

Strips old navigation sections and writes fresh nav tables to all 50+ root/curriculum docs, 175 project READMEs, and 10 elite-track READMEs. Run this after adding, removing, or reordering documents.

### Shell-based CI checks

These scripts validate structural contracts across the curriculum. They are called individually or as a suite.

#### run_all_curriculum_checks.sh

Runs all 9 contract checks in sequence. Pass `--full` to include extended smoke tests.

```bash
bash tools/run_all_curriculum_checks.sh
bash tools/run_all_curriculum_checks.sh --full
```

#### Individual checks

| Script | What it verifies |
|--------|-----------------|
| `check_markdown_links.sh` | All relative markdown links (`./path.md`) resolve to existing files |
| `check_root_doc_contract.sh` | Root docs (00-15) and curriculum docs (16-50) have required sections, home links, next-chain links, and source sections |
| `check_level_index_contract.sh` | Each level index (level-0 through level-10) lists exactly 15 projects with valid links and next/return navigation |
| `check_project_readme_contract.sh` | All 165 project READMEs have required headings (Run, Expected output, Alter/Break/Fix, Mastery check, etc.) and portable path notes |
| `check_project_python_comment_contract.sh` | All 165 `project.py` files start with a docstring and have minimum comment density; same for test files |
| `check_portable_paths.sh` | No markdown file contains user-specific absolute paths (`/Users/...` or `C:\Users\...`) |
| `check_elite_track_contract.sh` | Elite track projects have all required files (`project.py`, `tests/`, `data/`) and README headings |

```bash
bash tools/check_markdown_links.sh
bash tools/check_portable_paths.sh
# etc.
```

All checks exit 0 on success and non-zero on failure, making them suitable for CI pipelines.
