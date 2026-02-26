"""
Progress Dashboard — Automated Learning Tracker

Scans the repository to show your learning progress based on actual work done
(files created, tests passing, notes written).

Usage:
    python tools/progress.py                    # show overall progress
    python tools/progress.py --detail level-0   # detailed view for a level
    python tools/progress.py --streak           # show practice streak
    python tools/progress.py --next             # recommend what to work on next
    python tools/progress.py --history          # show progress over time
    python tools/progress.py --level 3          # filter to a specific level
    python tools/progress.py --export csv       # export progress as CSV

No external dependencies — uses only Python standard library.
"""

import csv
import io
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PROJECTS_DIR = REPO_ROOT / "projects"
DATA_DIR = REPO_ROOT / "data"
PROGRESS_JSON = DATA_DIR / "progress.json"

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
        "test_pass_count": 0,
        "test_total_count": 0,
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

    # Run tests if they exist and count pass/fail
    if status["has_tests"]:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_dir), "-v", "--tb=no", "-q"],
                capture_output=True, text=True, timeout=30,
                cwd=str(project_dir),
            )
            # Parse pytest output for pass/fail counts
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if "passed" in line or "failed" in line:
                    import re
                    passed = re.search(r"(\d+) passed", line)
                    failed = re.search(r"(\d+) failed", line)
                    p = int(passed.group(1)) if passed else 0
                    f = int(failed.group(1)) if failed else 0
                    status["test_pass_count"] = p
                    status["test_total_count"] = p + f
                    status["tests_pass"] = f == 0 and p > 0
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass

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


def extract_level_number(level_dir):
    """Extract the numeric level from a level directory, or None."""
    name = level_dir.name
    if name == "level-00-absolute-beginner":
        return -1
    if name.startswith("level-"):
        try:
            return int(name.split("-")[1])
        except (ValueError, IndexError):
            pass
    if name == "elite-track":
        return 99
    return None


def determine_project_status(status_dict):
    """Determine overall status string for a project."""
    if not status_dict["has_code"]:
        return "not_started"
    if status_dict["has_code"] and status_dict["has_notes"]:
        return "completed"
    return "in_progress"


def get_last_modified(project_dir):
    """Get the most recent modification time of .py files in a project."""
    latest = None
    for f in project_dir.rglob("*.py"):
        mtime = f.stat().st_mtime
        if latest is None or mtime > latest:
            latest = mtime
    if latest:
        return datetime.fromtimestamp(latest).isoformat()
    return None


def save_progress_json(scan_data):
    """Save scan results to data/progress.json with history."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    history = []
    if PROGRESS_JSON.exists():
        try:
            with open(PROGRESS_JSON, encoding="utf-8") as f:
                existing = json.load(f)
            history = existing.get("history", [])
        except (json.JSONDecodeError, KeyError):
            pass

    history.append(scan_data)

    # Keep last 100 scans to avoid unbounded growth
    if len(history) > 100:
        history = history[-100:]

    with open(PROGRESS_JSON, "w", encoding="utf-8") as f:
        json.dump({"history": history}, f, indent=2)


def build_scan_data(level_filter=None):
    """Build a full scan of all projects, optionally filtered to a level number."""
    scan = {
        "timestamp": datetime.now().isoformat(),
        "projects": [],
    }

    all_dirs = get_level_dirs() + get_module_dirs()

    for name, level_dir in all_dirs:
        level_num = extract_level_number(level_dir)

        # Apply level filter if requested
        if level_filter is not None and level_num != level_filter:
            continue

        projects = get_project_subdirs(level_dir)
        for proj in projects:
            status = check_project_status(proj)
            scan["projects"].append({
                "name": proj.name,
                "level": name,
                "level_dir": level_dir.name,
                "path": str(proj.relative_to(REPO_ROOT)),
                "status": determine_project_status(status),
                "last_modified": get_last_modified(proj),
                "test_pass_count": status["test_pass_count"],
                "test_total_count": status["test_total_count"],
                "has_code": status["has_code"],
                "has_tests": status["has_tests"],
                "has_notes": status["has_notes"],
            })

    summary_total = len(scan["projects"])
    summary_completed = sum(1 for p in scan["projects"] if p["status"] == "completed")
    summary_in_progress = sum(1 for p in scan["projects"] if p["status"] == "in_progress")
    scan["summary"] = {
        "total": summary_total,
        "completed": summary_completed,
        "in_progress": summary_in_progress,
        "not_started": summary_total - summary_completed - summary_in_progress,
    }

    return scan


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


def show_overview(level_filter=None):
    """Show high-level progress across all levels and modules."""
    print(f"\n{BOLD}{'='*55}")
    print(f"  Python Mastery — Learning Progress Dashboard")
    print(f"{'='*55}{RESET}\n")

    total_projects = 0
    total_with_code = 0
    total_with_notes = 0

    # Levels
    if level_filter is None:
        print(f"  {BOLD}Main Curriculum{RESET}\n")
    for name, level_dir in get_level_dirs():
        level_num = extract_level_number(level_dir)
        if level_filter is not None and level_num != level_filter:
            continue

        projects = get_project_subdirs(level_dir)
        with_code = sum(1 for p in projects if check_project_status(p)["has_code"])
        total_projects += len(projects)
        total_with_code += with_code
        print_progress_bar(with_code, len(projects), label=name)

    # Modules (skip if filtering to a specific level)
    if level_filter is None:
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

    # Save scan data
    scan = build_scan_data(level_filter=level_filter)
    save_progress_json(scan)
    print(f"  {DIM}Progress saved to data/progress.json{RESET}\n")


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


def show_history():
    """Show progress over time from saved scan history."""
    print(f"\n{BOLD}Progress History{RESET}\n")

    if not PROGRESS_JSON.exists():
        print("  No history yet. Run a scan first: python tools/progress.py")
        print()
        return

    with open(PROGRESS_JSON, encoding="utf-8") as f:
        data = json.load(f)

    history = data.get("history", [])
    if not history:
        print("  No history entries found.")
        print()
        return

    print(f"  {'Date':20s} {'Completed':>10s} {'In Progress':>12s} {'Not Started':>12s} {'Total':>6s}")
    print(f"  {'-'*62}")

    for entry in history[-20:]:  # Show last 20 scans
        ts = entry.get("timestamp", "unknown")
        try:
            dt = datetime.fromisoformat(ts)
            date_str = dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            date_str = ts[:16]

        summary = entry.get("summary", {})
        completed = summary.get("completed", 0)
        in_progress = summary.get("in_progress", 0)
        not_started = summary.get("not_started", 0)
        total = summary.get("total", 0)

        print(f"  {date_str:20s} {GREEN}{completed:>10d}{RESET} {YELLOW}{in_progress:>12d}{RESET} {DIM}{not_started:>12d}{RESET} {total:>6d}")

    # Show trend if we have at least 2 entries
    if len(history) >= 2:
        first = history[0].get("summary", {}).get("completed", 0)
        last = history[-1].get("summary", {}).get("completed", 0)
        delta = last - first
        if delta > 0:
            print(f"\n  {GREEN}+{delta} projects completed since first scan{RESET}")
        elif delta == 0:
            print(f"\n  {YELLOW}No change in completed projects since first scan{RESET}")

    print()


def export_csv(level_filter=None):
    """Export current progress as CSV to stdout."""
    scan = build_scan_data(level_filter=level_filter)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "project_name", "level", "level_dir", "path", "status",
        "last_modified", "test_pass_count", "test_total_count",
        "has_code", "has_tests", "has_notes",
    ])

    for proj in scan["projects"]:
        writer.writerow([
            proj["name"],
            proj["level"],
            proj["level_dir"],
            proj["path"],
            proj["status"],
            proj["last_modified"] or "",
            proj["test_pass_count"],
            proj["test_total_count"],
            proj["has_code"],
            proj["has_tests"],
            proj["has_notes"],
        ])

    print(output.getvalue())


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Progress dashboard. Scans the repository to show learning "
        "progress based on actual work done (files created, tests passing, notes written).",
    )
    parser.add_argument(
        "--detail", type=str, default=None, metavar="LEVEL",
        help="show detailed progress for a specific level or module (e.g. level-0)",
    )
    parser.add_argument(
        "--streak", action="store_true",
        help="show your practice streak from git commit history",
    )
    parser.add_argument(
        "--next", action="store_true",
        help="recommend what to work on next",
    )
    parser.add_argument(
        "--history", action="store_true",
        help="show progress over time from previous scans",
    )
    parser.add_argument(
        "--level", type=int, default=None, metavar="N",
        help="filter to a specific level number (0-10)",
    )
    parser.add_argument(
        "--export", type=str, default=None, metavar="FORMAT",
        choices=["csv"],
        help="export progress data (supported: csv)",
    )
    args = parser.parse_args()

    if args.history:
        show_history()
        return

    if args.export == "csv":
        export_csv(level_filter=args.level)
        return

    if args.streak:
        show_streak()
        return

    if args.next:
        show_next()
        return

    if args.detail is not None:
        show_detail(args.detail)
        return

    show_overview(level_filter=args.level)


if __name__ == "__main__":
    main()
