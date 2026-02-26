"""Python replacement for check_elite_track_contract.sh

Verifies that elite-track projects have the required structure:
README with proper headings, project.py with docstring, test file,
and sample input data. Works on Windows without bash or ripgrep.

Usage:
    python tools/check_elite_track_contract.py
"""

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
ELITE_DIR = ROOT_DIR / "projects" / "elite-track"

EXPECTED_PROJECTS = [
    "01-algorithms-complexity-lab",
    "02-concurrent-job-system",
    "03-distributed-cache-simulator",
    "04-secure-auth-gateway",
    "05-performance-profiler-workbench",
    "06-event-driven-architecture-lab",
    "07-observability-slo-platform",
    "08-policy-compliance-engine",
    "09-open-source-maintainer-simulator",
    "10-staff-engineer-capstone",
]

REQUIRED_HEADINGS = [
    "## Run (copy/paste)",
    "## Expected terminal output",
    "## Expected artifacts",
    "## Alter it (required)",
    "## Break it (required)",
    "## Fix it (required)",
    "## Explain it (teach-back)",
    "## Mastery check",
    "## Next",
]


def first_non_empty_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def count_comment_lines(text: str) -> int:
    return sum(1 for line in text.splitlines() if re.match(r"^\s*#", line))


def check() -> bool:
    fail = False

    # Elite index README
    elite_readme = ELITE_DIR / "README.md"
    if not elite_readme.exists():
        print("missing elite track index: projects/elite-track/README.md")
        return False

    index_text = elite_readme.read_text(encoding="utf-8", errors="replace")
    index_lines = index_text.splitlines()

    non_blank = [line.strip() for line in index_lines if line.strip()]
    if len(non_blank) < 2 or non_blank[1] != "Home: [README](../../README.md)":
        print("bad elite track home link")
        fail = True

    for slug in EXPECTED_PROJECTS:
        # Check index link
        link_pattern = f"- [{slug}](./{slug}/README.md)"
        if link_pattern not in index_text:
            print(f"missing elite index link: {slug}")
            fail = True

        project_dir = ELITE_DIR / slug
        readme = project_dir / "README.md"
        script = project_dir / "project.py"
        test_file = project_dir / "tests" / "test_project.py"
        input_file = project_dir / "data" / "sample_input.txt"

        # Required files
        for p in [readme, script, test_file, input_file]:
            if not p.exists():
                print(f"missing elite file: {p.relative_to(ROOT_DIR).as_posix()}")
                fail = True

        # README checks
        if readme.exists():
            content = readme.read_text(encoding="utf-8", errors="replace")
            lines = content.splitlines()
            non_blank_r = [line.strip() for line in lines if line.strip()]
            if len(non_blank_r) < 2 or non_blank_r[1] != "Home: [README](../../../README.md)":
                print(f"bad elite project home link: {readme.relative_to(ROOT_DIR).as_posix()}")
                fail = True

            for heading in REQUIRED_HEADINGS:
                if heading not in content:
                    print(
                        f"missing heading '{heading}' in "
                        f"{readme.relative_to(ROOT_DIR).as_posix()}"
                    )
                    fail = True

            repo_root_note = (
                "Use `<repo-root>` as the folder containing this repository's `README.md`."
            )
            if repo_root_note not in content:
                print(
                    f"missing <repo-root> note in "
                    f"{readme.relative_to(ROOT_DIR).as_posix()}"
                )
                fail = True

        # project.py checks
        if script.exists():
            text = script.read_text(encoding="utf-8", errors="replace")
            first = first_non_empty_line(text)
            if not first.startswith('"""'):
                print(
                    f"missing module docstring at top: "
                    f"{script.relative_to(ROOT_DIR).as_posix()}"
                )
                fail = True

            comments = count_comment_lines(text)
            if comments < 6:
                print(
                    f"too few comment lines in "
                    f"{script.relative_to(ROOT_DIR).as_posix()}: {comments} (min 6)"
                )
                fail = True

        # test_project.py checks
        if test_file.exists():
            text = test_file.read_text(encoding="utf-8", errors="replace")
            first = first_non_empty_line(text)
            if not first.startswith('"""'):
                print(
                    f"missing test module docstring at top: "
                    f"{test_file.relative_to(ROOT_DIR).as_posix()}"
                )
                fail = True

    if fail:
        print("elite track contract check failed")
        return False

    print("elite track contract verified")
    return True


def main() -> None:
    success = check()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
