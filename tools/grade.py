"""
Auto-Grading Test Runner — Pedagogical Feedback

Runs project tests and provides friendly, educational feedback.
Not just pass/fail — explains what went wrong and where to review.

Usage:
    python tools/grade.py projects/level-0/01-terminal-hello/
    python tools/grade.py --level 0
    python tools/grade.py --level 0 --summary
    python tools/grade.py --modules
    python tools/grade.py --all

No external dependencies beyond pytest (already in the project).
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CONFIG_FILE = Path(__file__).parent / "grading_config.json"

# ANSI colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def load_config():
    """Load grading config that maps projects to concepts."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def find_projects(path=None, level=None, modules_only=False, all_projects=False):
    """Find project directories to grade."""
    projects = []
    base = REPO_ROOT / "projects"

    if path:
        target = Path(path)
        if not target.is_absolute():
            target = REPO_ROOT / target
        if target.is_dir():
            projects.append(target)
        return projects

    if all_projects or level is not None:
        # Level projects
        for level_dir in sorted(base.glob("level-*")):
            if level_dir.name == "level-00-absolute-beginner":
                continue  # no tests
            if level is not None:
                level_name = f"level-{level}"
                if level_dir.name != level_name:
                    continue
            for proj_dir in sorted(level_dir.iterdir()):
                if proj_dir.is_dir() and not proj_dir.name.startswith("."):
                    projects.append(proj_dir)

    if all_projects or modules_only:
        # Module projects
        modules_dir = base / "modules"
        if modules_dir.exists():
            for mod_dir in sorted(modules_dir.iterdir()):
                if mod_dir.is_dir() and not mod_dir.name.startswith("."):
                    for proj_dir in sorted(mod_dir.iterdir()):
                        if proj_dir.is_dir() and not proj_dir.name.startswith("."):
                            projects.append(proj_dir)

    if all_projects and not modules_only and level is None:
        # Elite track
        elite = base / "elite-track"
        if elite.exists():
            for proj_dir in sorted(elite.iterdir()):
                if proj_dir.is_dir() and not proj_dir.name.startswith("."):
                    projects.append(proj_dir)

    return projects


def run_tests(project_dir):
    """Run pytest on a project and capture results."""
    test_dir = project_dir / "tests"
    if not test_dir.exists():
        return {"status": "no_tests", "output": "", "passed": 0, "failed": 0, "errors": 0}

    test_files = list(test_dir.glob("test_*.py"))
    if not test_files:
        return {"status": "no_tests", "output": "", "passed": 0, "failed": 0, "errors": 0}

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "--tb=short", str(test_dir)],
            capture_output=True,
            text=True,
            cwd=str(project_dir),
            timeout=30,
        )

        output = result.stdout + result.stderr
        passed = output.count(" PASSED")
        failed = output.count(" FAILED")
        errors = output.count(" ERROR")

        if result.returncode == 0:
            status = "passed"
        elif failed > 0 or errors > 0:
            status = "failed"
        else:
            status = "error"

        return {
            "status": status,
            "output": output,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "output": "Test timed out after 30 seconds", "passed": 0, "failed": 0, "errors": 0}
    except FileNotFoundError:
        return {"status": "error", "output": "pytest not found. Install with: pip install pytest", "passed": 0, "failed": 0, "errors": 0}


def get_concept_hints(project_dir, config):
    """Get concept references for a project from the grading config."""
    # Try to match by relative path
    rel = str(project_dir.relative_to(REPO_ROOT)).replace("\\", "/")
    return config.get(rel, {}).get("concepts", [])


def print_project_result(project_dir, result, config, verbose=False):
    """Print formatted result for a single project."""
    name = project_dir.name
    parent = project_dir.parent.name

    if result["status"] == "no_tests":
        print(f"  {YELLOW}?{RESET} {parent}/{name} — no tests found")
        return

    total = result["passed"] + result["failed"] + result["errors"]
    if total == 0:
        print(f"  {YELLOW}?{RESET} {parent}/{name} — no test results")
        return

    if result["status"] == "passed":
        pct = 100
        print(f"  {GREEN}+{RESET} {parent}/{name} — {GREEN}{result['passed']}/{total} passed ({pct}%){RESET}")
    elif result["status"] == "timeout":
        print(f"  {RED}!{RESET} {parent}/{name} — {RED}timed out{RESET}")
    else:
        pct = result["passed"] / total * 100 if total > 0 else 0
        print(f"  {RED}x{RESET} {parent}/{name} — {RED}{result['passed']}/{total} passed ({pct:.0f}%){RESET}")

        if verbose and result["failed"] > 0:
            # Show failure details
            lines = result["output"].split("\n")
            for line in lines:
                if "FAILED" in line or "AssertionError" in line or "Error" in line:
                    print(f"      {RED}{line.strip()}{RESET}")

            # Show concept hints
            hints = get_concept_hints(project_dir, config)
            if hints:
                print(f"      {CYAN}Review:{RESET}", end="")
                for hint in hints:
                    print(f" {hint}", end="")
                print()


def print_summary(results):
    """Print overall summary."""
    total_projects = len(results)
    passed_projects = sum(1 for r in results.values() if r["status"] == "passed")
    failed_projects = sum(1 for r in results.values() if r["status"] == "failed")
    no_tests = sum(1 for r in results.values() if r["status"] == "no_tests")
    total_tests = sum(r["passed"] + r["failed"] + r["errors"] for r in results.values())
    total_passed = sum(r["passed"] for r in results.values())

    print(f"\n{'='*50}")
    print(f"  {BOLD}Grading Summary{RESET}")
    print(f"{'='*50}")
    print(f"  Projects graded: {total_projects}")
    print(f"  {GREEN}Passed: {passed_projects}{RESET}")
    if failed_projects > 0:
        print(f"  {RED}Failed: {failed_projects}{RESET}")
    if no_tests > 0:
        print(f"  {YELLOW}No tests: {no_tests}{RESET}")
    print()

    if total_tests > 0:
        pct = total_passed / total_tests * 100
        bar_len = 30
        filled = int(bar_len * pct / 100)
        bar = "#" * filled + "-" * (bar_len - filled)
        color = GREEN if pct >= 80 else YELLOW if pct >= 50 else RED
        print(f"  Tests: {total_passed}/{total_tests}")
        print(f"  Score: {color}[{bar}] {pct:.0f}%{RESET}")

    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Auto-grading test runner with pedagogical feedback. "
        "Runs project tests and provides friendly, educational results.",
    )
    parser.add_argument(
        "path", nargs="?", default=None,
        help="path to a specific project directory to grade",
    )
    parser.add_argument(
        "--level", type=str, default=None,
        help="grade all projects in a level (e.g. --level 0)",
    )
    parser.add_argument(
        "--modules", action="store_true",
        help="grade all expansion module projects",
    )
    parser.add_argument(
        "--all", action="store_true", dest="all_projects",
        help="grade every project (levels + modules + elite)",
    )
    parser.add_argument(
        "--summary", action="store_true",
        help="show only the summary, skip individual results",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="show failure details and concept hints",
    )
    args = parser.parse_args()

    config = load_config()

    # Determine what to grade
    projects = []
    if args.all_projects:
        projects = find_projects(all_projects=True)
    elif args.modules:
        projects = find_projects(modules_only=True)
    elif args.level is not None:
        projects = find_projects(level=args.level)
    elif args.path:
        projects = find_projects(path=args.path)

    if not projects:
        print("No projects found to grade.")
        print("Usage: python tools/grade.py projects/level-0/01-terminal-hello/")
        print("       python tools/grade.py --level 0")
        print("       python tools/grade.py --modules")
        print("       python tools/grade.py --all")
        return

    print(f"\n{BOLD}Grading {len(projects)} project(s)...{RESET}\n")

    results = {}
    for proj in projects:
        result = run_tests(proj)
        results[str(proj)] = result
        if not args.summary:
            print_project_result(proj, result, config, verbose=args.verbose)

    print_summary(results)


if __name__ == "__main__":
    main()
