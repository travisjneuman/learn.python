# Curriculum Tools

Scripts that support the learn.python curriculum. Learner tools help you track progress and find your starting point. Maintainer tools keep the curriculum's cross-references and navigation links consistent.

**Prerequisites:** Python 3.11+, pytest (for `grade.py`). Shell-based checks additionally require ripgrep (`rg`) and bash; Python equivalents work on any platform.

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

### spaced_repetition.py

Flashcard review engine using the SM-2 spaced repetition algorithm for optimal long-term retention.

```bash
python tools/spaced_repetition.py                  # review due cards
python tools/spaced_repetition.py --level 0        # review level 0 only
python tools/spaced_repetition.py --review         # spaced repetition mode (default)
python tools/spaced_repetition.py --random         # random/casual practice
python tools/spaced_repetition.py --stats          # show review statistics
python tools/spaced_repetition.py --due            # show count of due cards
python tools/spaced_repetition.py --reset          # reset all progress
```

Uses a 0-5 quality rating scale to compute easiness factors and review intervals. Progress is stored in `data/flashcard_progress.json`. Works with the same flashcard decks as `practice/flashcards/review-runner.py` but uses the more sophisticated SM-2 scheduling algorithm.

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

### generate_badges.py

Generates shields.io-style SVG badges for each curriculum level.

```bash
python tools/generate_badges.py              # generate all badges to badges/
python tools/generate_badges.py --preview    # list badge paths without generating
```

Creates 15 SVG badges (levels 00-10, elite, modules, complete) with a color gradient from green (beginner) to gold (elite). Use in your GitHub profile or README.

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

### Python CI checks (cross-platform)

Python replacements for the shell-based checks. These work on Windows, macOS, and Linux without requiring bash or ripgrep.

#### run_all_checks.py

Runs all Python-based contract checks in sequence.

```bash
python tools/run_all_checks.py
python tools/run_all_checks.py --verbose
```

#### Individual Python checks

| Script | What it verifies |
|--------|-----------------|
| `check_markdown_links.py` | All relative markdown links (`./path.md`) resolve to existing files |
| `check_root_docs.py` | Root docs (00-15) and curriculum docs (16-50) have required sections, home links, next-chain links, and source sections |
| `check_project_contract.py` | All 165 project READMEs have required headings (Run, Expected output, Alter/Break/Fix, Mastery check, etc.) and portable path notes |
| `check_portable_paths.py` | No markdown file contains user-specific absolute paths (`/Users/...` or `C:\Users\...`) |

```bash
python tools/check_markdown_links.py
python tools/check_portable_paths.py
python tools/check_root_docs.py
python tools/check_project_contract.py
```

### Shell-based CI checks (original)

These scripts validate structural contracts across the curriculum. They require bash and ripgrep.

#### run_all_curriculum_checks.sh

Runs all 9 contract checks in sequence. Pass `--full` to include extended smoke tests.

```bash
bash tools/run_all_curriculum_checks.sh
bash tools/run_all_curriculum_checks.sh --full
```

#### Individual shell checks

| Script | What it verifies |
|--------|-----------------|
| `check_markdown_links.sh` | All relative markdown links (`./path.md`) resolve to existing files |
| `check_root_doc_contract.sh` | Root docs (00-15) and curriculum docs (16-50) have required sections, home links, next-chain links, and source sections |
| `check_level_index_contract.sh` | Each level index (level-0 through level-10) lists exactly 15 projects with valid links and next/return navigation |
| `check_project_readme_contract.sh` | All 165 project READMEs have required headings (Run, Expected output, Alter/Break/Fix, Mastery check, etc.) and portable path notes |
| `check_project_python_comment_contract.sh` | All 165 `project.py` files start with a docstring and have minimum comment density; same for test files |
| `check_portable_paths.sh` | No markdown file contains user-specific absolute paths (`/Users/...` or `C:\Users\...`) |
| `check_elite_track_contract.sh` | Elite track projects have all required files (`project.py`, `tests/`, `data/`) and README headings |

All checks exit 0 on success and non-zero on failure, making them suitable for CI pipelines.
