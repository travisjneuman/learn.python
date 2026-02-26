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


def grade_with_detail(project_dir):
    """Run pytest and return detailed per-test results with partial credit.

    Runs pytest with JSON output to capture individual test outcomes.
    Reports "X/Y tests passing" with test names and descriptions of
    what each failing test expected.

    Args:
        project_dir: Path to the project directory.

    Returns:
        A dict with keys:
            score: float percentage (0-100)
            passed: int count of passing tests
            total: int count of total tests
            tests: list of dicts with {name, status, message}
    """
    test_dir = Path(project_dir) / "tests"
    if not test_dir.exists():
        return {"score": 0.0, "passed": 0, "total": 0, "tests": []}

    test_files = list(test_dir.glob("test_*.py"))
    if not test_files:
        return {"score": 0.0, "passed": 0, "total": 0, "tests": []}

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "--tb=line", str(test_dir)],
            capture_output=True,
            text=True,
            cwd=str(project_dir),
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return {"score": 0.0, "passed": 0, "total": 0, "tests": [{"name": "ALL", "status": "timeout", "message": "Tests timed out after 30 seconds"}]}
    except FileNotFoundError:
        return {"score": 0.0, "passed": 0, "total": 0, "tests": [{"name": "ALL", "status": "error", "message": "pytest not found"}]}

    output = result.stdout + result.stderr
    tests = []
    passed_count = 0
    total_count = 0

    for line in output.split("\n"):
        if " PASSED" in line or " FAILED" in line or " ERROR" in line:
            total_count += 1
            # Extract test name: "tests/test_foo.py::test_bar PASSED"
            parts = line.strip().split(" ")
            test_path = parts[0] if parts else "unknown"
            test_name = test_path.split("::")[-1] if "::" in test_path else test_path

            if " PASSED" in line:
                passed_count += 1
                tests.append({"name": test_name, "status": "passed", "message": ""})
            elif " FAILED" in line:
                tests.append({"name": test_name, "status": "failed", "message": ""})
            elif " ERROR" in line:
                tests.append({"name": test_name, "status": "error", "message": ""})

    # Extract failure details from tb=line output
    for line in output.split("\n"):
        line = line.strip()
        if line.startswith("FAILED") or ("assert" in line.lower() and "Error" not in line):
            # Match failure messages to tests
            for test in tests:
                if test["status"] == "failed" and not test["message"]:
                    test["message"] = line
                    break

    score = (passed_count / total_count * 100) if total_count > 0 else 0.0

    # Print friendly report
    print(f"\n  {BOLD}Detailed Grade: {passed_count}/{total_count} tests passing ({score:.0f}%){RESET}")
    for test in tests:
        if test["status"] == "passed":
            print(f"    {GREEN}PASS{RESET} {test['name']}")
        elif test["status"] == "failed":
            print(f"    {RED}FAIL{RESET} {test['name']}")
            if test["message"]:
                print(f"         {YELLOW}{test['message']}{RESET}")
        else:
            print(f"    {RED}ERR {RESET} {test['name']}")
            if test["message"]:
                print(f"         {YELLOW}{test['message']}{RESET}")

    return {"score": score, "passed": passed_count, "total": total_count, "tests": tests}


def check_style(file_path):
    """Run ruff on a file and return a style score.

    Runs `ruff check` via subprocess, counts violations by category,
    and returns a score out of 100 with deductions per violation type.

    Args:
        file_path: Path to the Python file to check.

    Returns:
        A dict with keys:
            score: int style score (100 minus deductions)
            violations: int total violation count
            by_category: dict mapping rule codes to counts
            details: list of violation description strings
    """
    target = Path(file_path)
    if not target.exists():
        print(f"  {RED}File not found: {file_path}{RESET}")
        return {"score": 0, "violations": 0, "by_category": {}, "details": []}

    try:
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "check", "--output-format=text", str(target)],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except subprocess.TimeoutExpired:
        return {"score": 0, "violations": 0, "by_category": {}, "details": ["ruff timed out"]}
    except FileNotFoundError:
        print(f"  {YELLOW}ruff not found. Install with: pip install ruff{RESET}")
        return {"score": 100, "violations": 0, "by_category": {}, "details": []}

    output = result.stdout.strip()
    if not output or result.returncode == 0:
        print(f"  {GREEN}Style: 100/100 — No issues found{RESET}")
        return {"score": 100, "violations": 0, "by_category": {}, "details": []}

    # Parse ruff output lines like: "file.py:1:1: E401 ..."
    by_category = {}
    details = []
    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Extract rule code (e.g., E401, F841, W291)
        parts = line.split(":")
        if len(parts) >= 4:
            msg = parts[3].strip()
            code = msg.split(" ")[0] if msg else "unknown"
            category = code[0] if code else "?"
            by_category[category] = by_category.get(category, 0) + 1
            details.append(line)

    total_violations = sum(by_category.values())

    # Deduction schedule: 3 points per violation, minimum score 0
    deduction_per_violation = 3
    score = max(0, 100 - total_violations * deduction_per_violation)

    # Friendly output
    color = GREEN if score >= 80 else YELLOW if score >= 50 else RED
    print(f"  {color}Style: {score}/100 — {total_violations} issue(s) found{RESET}")
    if by_category:
        category_names = {"E": "errors", "W": "warnings", "F": "pyflakes", "I": "isort", "N": "naming", "C": "convention"}
        for cat, count in sorted(by_category.items()):
            label = category_names.get(cat, cat)
            print(f"    {cat}: {count} {label}")

    return {"score": score, "violations": total_violations, "by_category": by_category, "details": details}


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

        # Award XP for passing projects
        if result["status"] == "passed":
            try:
                from xp_tracker import award_xp
                xp = award_xp("project_completion", proj.name)
                if xp:
                    print(f"    {GREEN}+{xp} XP{RESET}")
            except Exception:
                pass
            try:
                from streak_tracker import record_activity
                record_activity("grade")
            except Exception:
                pass

    print_summary(results)


if __name__ == "__main__":
    main()
