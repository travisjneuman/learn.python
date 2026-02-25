"""
Progress Dashboard — Automated Learning Tracker

Scans the repository to show your learning progress based on actual work done
(files created, tests passing, notes written).

Usage:
    python tools/progress.py                    # show overall progress
    python tools/progress.py --detail level-0   # detailed view for a level
    python tools/progress.py --streak           # show practice streak
    python tools/progress.py --next             # recommend what to work on next

No external dependencies — uses only Python standard library.
"""

import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PROJECTS_DIR = REPO_ROOT / "projects"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def check_project_status(project_dir):
    """Check the completion status of a single project."""
    status = {
        "exists": project_dir.exists(),
        "has_code": False,
        "has_tests": False,
        "tests_pass": None,
        "has_notes": False,
        "has_alterations": False,
    }

    if not status["exists"]:
        return status

    # Check for code files
    py_files = list(project_dir.glob("*.py"))
    status["has_code"] = len(py_files) > 0

    # Check for test files
    test_dir = project_dir / "tests"
    test_files = list(test_dir.glob("test_*.py")) if test_dir.exists() else []
    status["has_tests"] = len(test_files) > 0

    # Check for notes
    notes = project_dir / "notes.md"
    if notes.exists():
        content = notes.read_text(encoding="utf-8", errors="replace").strip()
        # Check if notes have actual content beyond the template
        status["has_notes"] = len(content) > 50

    return status


def get_level_dirs():
    """Get all level directories in order."""
    levels = []

    # Level 00
    l00 = PROJECTS_DIR / "level-00-absolute-beginner"
    if l00.exists():
        levels.append(("Level 00 (Absolute Beginner)", l00))

    # Levels 0-10
    for i in range(11):
        d = PROJECTS_DIR / f"level-{i}"
        if d.exists():
            levels.append((f"Level {i}", d))

    # Elite track
    elite = PROJECTS_DIR / "elite-track"
    if elite.exists():
        levels.append(("Elite Track", elite))

    return levels


def get_module_dirs():
    """Get all module directories."""
    modules = []
    modules_dir = PROJECTS_DIR / "modules"
    if modules_dir.exists():
        for d in sorted(modules_dir.iterdir()):
            if d.is_dir() and not d.name.startswith(".") and d.name != "README.md":
                # Clean up module name
                name = d.name.replace("-", " ").title()
                modules.append((name, d))
    return modules


def get_project_subdirs(level_dir):
    """Get project subdirectories within a level or module."""
    projects = []
    for d in sorted(level_dir.iterdir()):
        if d.is_dir() and not d.name.startswith("."):
            projects.append(d)
    return projects


def print_progress_bar(completed, total, width=30, label=""):
    """Print a colored progress bar."""
    if total == 0:
        return

    pct = completed / total * 100
    filled = int(width * pct / 100)
    bar = "#" * filled + "-" * (width - filled)

    if pct >= 80:
        color = GREEN
    elif pct >= 40:
        color = YELLOW
    else:
        color = RED

    print(f"  {color}[{bar}]{RESET} {completed}/{total} ({pct:.0f}%) {label}")


def show_overview():
    """Show high-level progress across all levels and modules."""
    print(f"\n{BOLD}{'='*55}")
    print(f"  Python Mastery — Learning Progress Dashboard")
    print(f"{'='*55}{RESET}\n")

    total_projects = 0
    total_with_code = 0
    total_with_notes = 0

    # Levels
    print(f"  {BOLD}Main Curriculum{RESET}\n")
    for name, level_dir in get_level_dirs():
        projects = get_project_subdirs(level_dir)
        with_code = sum(1 for p in projects if check_project_status(p)["has_code"])
        total_projects += len(projects)
        total_with_code += with_code
        print_progress_bar(with_code, len(projects), label=name)

    # Modules
    print(f"\n  {BOLD}Expansion Modules{RESET}\n")
    for name, mod_dir in get_module_dirs():
        projects = get_project_subdirs(mod_dir)
        with_code = sum(1 for p in projects if check_project_status(p)["has_code"])
        total_projects += len(projects)
        total_with_code += with_code
        print_progress_bar(with_code, len(projects), label=name)

    # Practice tools
    print(f"\n  {BOLD}Practice Tools{RESET}\n")

    flashcard_state = REPO_ROOT / "practice" / "flashcards" / ".review-state.json"
    if flashcard_state.exists():
        with open(flashcard_state) as f:
            state = json.load(f)
        sessions = state.get("sessions", 0)
        cards = len(state.get("cards", {}))
        print(f"  Flashcards: {sessions} sessions, {cards} cards reviewed")
    else:
        print(f"  {DIM}Flashcards: not started yet{RESET}")

    quiz_dir = REPO_ROOT / "concepts" / "quizzes"
    if quiz_dir.exists():
        quiz_count = len(list(quiz_dir.glob("*-quiz.py")))
        print(f"  Concept quizzes: {quiz_count} available")

    challenge_dir = REPO_ROOT / "practice" / "challenges"
    if challenge_dir.exists():
        beginner = len(list((challenge_dir / "beginner").glob("*.py"))) if (challenge_dir / "beginner").exists() else 0
        intermediate = len(list((challenge_dir / "intermediate").glob("*.py"))) if (challenge_dir / "intermediate").exists() else 0
        print(f"  Coding challenges: {beginner} beginner, {intermediate} intermediate")

    # Overall
    print(f"\n  {BOLD}Overall{RESET}")
    print_progress_bar(total_with_code, total_projects, label="All projects")
    print()


def show_detail(level_name):
    """Show detailed progress for a specific level or module."""
    # Find the matching directory
    target = None
    for name, d in get_level_dirs() + get_module_dirs():
        if level_name.lower() in name.lower() or level_name.lower() in d.name.lower():
            target = (name, d)
            break

    if not target:
        print(f"Level/module '{level_name}' not found.")
        return

    name, level_dir = target
    projects = get_project_subdirs(level_dir)

    print(f"\n{BOLD}{name}{RESET} — {level_dir.relative_to(REPO_ROOT)}\n")

    for proj in projects:
        status = check_project_status(proj)
        indicators = []

        if status["has_code"]:
            indicators.append(f"{GREEN}code{RESET}")
        else:
            indicators.append(f"{DIM}code{RESET}")

        if status["has_tests"]:
            indicators.append(f"{GREEN}tests{RESET}")
        else:
            indicators.append(f"{DIM}tests{RESET}")

        if status["has_notes"]:
            indicators.append(f"{GREEN}notes{RESET}")
        else:
            indicators.append(f"{DIM}notes{RESET}")

        status_str = " | ".join(indicators)
        completed = status["has_code"] and status["has_notes"]
        marker = f"{GREEN}+{RESET}" if completed else f"{YELLOW}~{RESET}" if status["has_code"] else f"{DIM}-{RESET}"

        print(f"  {marker} {proj.name:40s} [{status_str}]")

    print()


def show_streak():
    """Show practice streak based on git commit history."""
    print(f"\n{BOLD}Practice Streak{RESET}\n")

    try:
        result = subprocess.run(
            ["git", "log", "--format=%ai", "--since=30 days ago"],
            capture_output=True, text=True,
            cwd=str(REPO_ROOT),
        )
        if result.returncode != 0:
            print("  Could not read git history.")
            return

        # Extract unique dates
        dates = set()
        for line in result.stdout.strip().split("\n"):
            if line:
                date_str = line.split()[0]
                dates.add(date_str)

        today = datetime.now().date()

        # Calculate current streak
        streak = 0
        check_date = today
        while str(check_date) in dates:
            streak += 1
            check_date -= timedelta(days=1)

        # Show last 30 days as a heatmap
        print(f"  Last 30 days (# = commit day, - = no commits):\n")
        row = "  "
        for i in range(29, -1, -1):
            d = today - timedelta(days=i)
            if str(d) in dates:
                row += f"{GREEN}#{RESET}"
            else:
                row += f"{DIM}-{RESET}"
        print(row)
        print()

        if streak > 0:
            print(f"  Current streak: {GREEN}{BOLD}{streak} day(s){RESET}")
        else:
            print(f"  Current streak: {RED}0 days{RESET} — commit today to start!")

        print(f"  Active days (last 30): {len(dates)}")
        print()

    except FileNotFoundError:
        print("  Git is not available.")


def show_next():
    """Recommend what to work on next."""
    print(f"\n{BOLD}Recommended Next Steps{RESET}\n")

    # Find the first level with incomplete projects
    for name, level_dir in get_level_dirs():
        projects = get_project_subdirs(level_dir)
        incomplete = [p for p in projects if not check_project_status(p)["has_code"]]
        if incomplete:
            print(f"  {CYAN}Continue:{RESET} {name}")
            print(f"  Next project: {incomplete[0].name}")
            print(f"  Path: {incomplete[0].relative_to(REPO_ROOT)}")
            print()

            # Suggest diagnostic if starting a new level
            diag_file = REPO_ROOT / "tools" / "diagnostics" / f"{level_dir.name}-diagnostic.json"
            if diag_file.exists() and len(incomplete) == len(projects):
                print(f"  {YELLOW}Tip:{RESET} Take the diagnostic first:")
                print(f"  python tools/diagnose.py {level_dir.name}")
                print()

            # Suggest flashcard review
            print(f"  {YELLOW}Before starting, review flashcards:{RESET}")
            print(f"  python practice/flashcards/review-runner.py")
            print()
            return

    print(f"  {GREEN}All main curriculum levels complete!{RESET}")
    print()

    # Check modules
    for name, mod_dir in get_module_dirs():
        projects = get_project_subdirs(mod_dir)
        incomplete = [p for p in projects if not check_project_status(p)["has_code"]]
        if incomplete:
            print(f"  {CYAN}Try a module:{RESET} {name}")
            print(f"  Next project: {incomplete[0].name}")
            print(f"  Path: {incomplete[0].relative_to(REPO_ROOT)}")
            print()
            return

    print(f"  {GREEN}All projects complete! You're a Python master!{RESET}")
    print()


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if "--streak" in args:
        show_streak()
        return

    if "--next" in args:
        show_next()
        return

    if "--detail" in args:
        idx = args.index("--detail")
        if idx + 1 < len(args):
            show_detail(args[idx + 1])
        else:
            print("Usage: python tools/progress.py --detail <level-name>")
        return

    show_overview()


if __name__ == "__main__":
    main()
