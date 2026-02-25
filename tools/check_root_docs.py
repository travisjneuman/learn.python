"""
Python replacement for check_root_doc_contract.sh

Verifies that root docs (00-15) and curriculum docs (16-50) have required
sections, home links, next-chain links, and source sections. Works on
Windows without bash or ripgrep.

Usage:
    python tools/check_root_docs.py
"""

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

ROOT_FILES = [
    "README.md",
    "00_COMPUTER_LITERACY_PRIMER.md",
    "01_ROADMAP.md",
    "02_GLOSSARY.md",
    "03_SETUP_ALL_PLATFORMS.md",
    "04_FOUNDATIONS.md",
    "05_AUTOMATION_FILES_EXCEL.md",
    "06_SQL.md",
    "07_MONITORING_API_INTEGRATION.md",
    "08_DASHBOARDS.md",
    "09_QUALITY_TOOLING.md",
    "10_CAPSTONE_PROJECTS.md",
    "11_CHECKLISTS.md",
    "12_SCREENSHOT_CHECKPOINTS.md",
    "13_SAMPLE_DATABASE_SCHEMAS.md",
    "14_NAVIGATION_AND_STUDY_WORKFLOW.md",
    "15_NEXT_LEVEL_EXPANSION_PLAN.md",
]

CURRICULUM_FILES = [
    f"{i:02d}_{name}"
    for i, name in [
        (16, "LEARNER_PROFILE_AND_PLACEMENT.md"),
        (17, "ASSESSMENT_AND_RUBRICS.md"),
        (18, "REMEDIATION_PLAYBOOK.md"),
        (19, "MENTOR_GUIDE.md"),
        (20, "CURRICULUM_CHANGELOG.md"),
        (21, "FULL_STACK_MASTERY_PATH.md"),
        (22, "SPECIALIZATION_TRACKS.md"),
        (23, "RESOURCE_AND_CURRICULUM_MAP.md"),
        (24, "MASTERY_SCORING_AND_GATES.md"),
        (25, "INFINITY_MASTERY_LOOP.md"),
        (26, "ZERO_TO_MASTER_PLAYBOOK.md"),
        (27, "DAY_0_TO_DAY_30_BOOTSTRAP.md"),
        (28, "LEVEL_0_TO_2_DEEP_GUIDE.md"),
        (29, "LEVEL_3_TO_5_DEEP_GUIDE.md"),
        (30, "LEVEL_6_TO_8_DEEP_GUIDE.md"),
        (31, "LEVEL_9_TO_10_AND_BEYOND.md"),
        (32, "DAILY_SESSION_SCRIPT.md"),
        (33, "WEEKLY_REVIEW_TEMPLATE.md"),
        (34, "FAILURE_RECOVERY_ATLAS.md"),
        (35, "CAPSTONE_BLUEPRINTS.md"),
        (36, "ELITE_ENGINEERING_TRACK.md"),
        (37, "QUARTERLY_EXAMS_AND_DEFENSES.md"),
        (38, "SYSTEM_DESIGN_AND_RFCS.md"),
        (39, "PRODUCTION_PLATFORM_LAB.md"),
        (40, "SECURITY_COMPLIANCE_HARDENING.md"),
        (41, "PERFORMANCE_ENGINEERING_LAB.md"),
        (42, "OPEN_SOURCE_CONTRIBUTION_LANE.md"),
        (43, "PUBLIC_PROOF_OF_WORK_PORTFOLIO.md"),
        (44, "SME_INTERVIEW_AND_DEBATE_BANK.md"),
        (45, "MASTERY_TELEMETRY_AND_REMEDIATION.md"),
        (46, "ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md"),
        (47, "DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md"),
        (48, "MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md"),
        (49, "COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md"),
        (50, "CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md"),
    ]
]

# Next-chain mapping for root files
NEXT_CHAIN = {
    "README.md": "00_COMPUTER_LITERACY_PRIMER.md",
    "00_COMPUTER_LITERACY_PRIMER.md": "01_ROADMAP.md",
    "01_ROADMAP.md": "02_GLOSSARY.md",
    "02_GLOSSARY.md": "03_SETUP_ALL_PLATFORMS.md",
    "03_SETUP_ALL_PLATFORMS.md": "04_FOUNDATIONS.md",
    "04_FOUNDATIONS.md": "09_QUALITY_TOOLING.md",
    "09_QUALITY_TOOLING.md": "05_AUTOMATION_FILES_EXCEL.md",
    "05_AUTOMATION_FILES_EXCEL.md": "06_SQL.md",
    "06_SQL.md": "07_MONITORING_API_INTEGRATION.md",
    "07_MONITORING_API_INTEGRATION.md": "08_DASHBOARDS.md",
    "08_DASHBOARDS.md": "10_CAPSTONE_PROJECTS.md",
    "10_CAPSTONE_PROJECTS.md": "11_CHECKLISTS.md",
    "11_CHECKLISTS.md": "12_SCREENSHOT_CHECKPOINTS.md",
    "12_SCREENSHOT_CHECKPOINTS.md": "13_SAMPLE_DATABASE_SCHEMAS.md",
    "13_SAMPLE_DATABASE_SCHEMAS.md": "14_NAVIGATION_AND_STUDY_WORKFLOW.md",
    "14_NAVIGATION_AND_STUDY_WORKFLOW.md": "15_NEXT_LEVEL_EXPANSION_PLAN.md",
    "15_NEXT_LEVEL_EXPANSION_PLAN.md": "curriculum/16_LEARNER_PROFILE_AND_PLACEMENT.md",
}

# Next-chain for curriculum files
CURRICULUM_NEXT_CHAIN = {}
for i in range(len(CURRICULUM_FILES) - 1):
    CURRICULUM_NEXT_CHAIN[CURRICULUM_FILES[i]] = CURRICULUM_FILES[i + 1]
CURRICULUM_NEXT_CHAIN[CURRICULUM_FILES[-1]] = "README.md"

# Required sections for specific docs
REQUIRED_SECTIONS = {
    "01_ROADMAP.md": [
        "Who this is for", "What you will build", "Prerequisites",
        "Step-by-step lab pack", "Expected output", "Break/fix drills",
        "Troubleshooting", "Mastery check",
        "Learning-style options (Play/Build/Dissect/Teach-back)",
    ],
    "02_GLOSSARY.md": [
        "Core programming terms", "Environment and packaging terms",
        "Quality terms", "SQL and data terms", "Monitoring and API terms",
    ],
    "11_CHECKLISTS.md": [
        "Project startup checklist", "Pre-run checklist",
        "Post-run validation checklist", "Incident triage checklist",
        "Release and handoff checklist",
        "Dashboard UX checklist (non-technical users)",
        "SME conversation prep checklist",
        "Screenshot and checkpoint checklist",
    ],
}

# Apply same required sections to docs 03-10 (except 02 and 11 which are special)
for doc in ROOT_FILES:
    num = doc.split("_")[0]
    if num in ("03", "04", "05", "06", "07", "08", "09", "10"):
        REQUIRED_SECTIONS[doc] = REQUIRED_SECTIONS["01_ROADMAP.md"]


def normalize(line: str) -> str:
    return line.replace("\r", "").strip()


def get_second_non_blank_line(lines: list[str]) -> str:
    count = 0
    for line in lines:
        if line.strip():
            count += 1
            if count == 2:
                return normalize(line)
    return ""


def find_last_h2(lines: list[str]) -> str:
    last = ""
    for line in lines:
        stripped = normalize(line)
        if stripped.startswith("## "):
            last = stripped
    return last


def extract_next_link(lines: list[str], prefix: str) -> str:
    """Extract the next link target after the ## Next heading."""
    in_next = False
    for line in lines:
        stripped = normalize(line)
        if stripped == "## Next":
            in_next = True
            continue
        if in_next:
            # Look for markdown link: [text](./target) or [text](../target)
            match = re.search(r"\]\(\.\/" + r"([^)]+)\)", stripped)
            if match:
                return match.group(1)
            match = re.search(r"\]\(\.\.\/" + r"([^)]+)\)", stripped)
            if match:
                return match.group(1)
    return ""


def check() -> bool:
    fail = False

    # Check root files
    for filename in ROOT_FILES:
        path = ROOT_DIR / filename
        if not path.exists():
            print(f"missing root doc: {filename}")
            fail = True
            continue

        content = path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()

        # Home link check (skip README)
        if filename != "README.md":
            home_line = get_second_non_blank_line(lines)
            if home_line != "Home: [README](./README.md)":
                print(f"bad home line: {filename}")
                fail = True

        # Last heading must be ## Next
        last_h2 = find_last_h2(lines)
        if last_h2 != "## Next":
            print(f"last heading is not ## Next: {filename}")
            fail = True

        # Next-chain check
        if filename in NEXT_CHAIN:
            expected = NEXT_CHAIN[filename]
            actual = extract_next_link(lines, "./")
            if not actual:
                print(f"missing next link after ## Next: {filename}")
                fail = True
            elif actual != expected:
                print(
                    f"bad next target in {filename}: "
                    f"expected {expected} got {actual}"
                )
                fail = True

        # Source section checks (skip README and 00_PRIMER)
        if filename not in ("README.md", "00_COMPUTER_LITERACY_PRIMER.md"):
            if "## Primary Sources" not in content:
                print(f"missing Primary Sources: {filename}")
                fail = True
            if "## Optional Resources" not in content:
                print(f"missing Optional Resources: {filename}")
                fail = True

        # Required sections
        if filename in REQUIRED_SECTIONS:
            for section in REQUIRED_SECTIONS[filename]:
                if f"## {section}" not in content:
                    print(f"missing section '{section}' in {filename}")
                    fail = True

    # Check curriculum files
    for filename in CURRICULUM_FILES:
        path = ROOT_DIR / "curriculum" / filename
        if not path.exists():
            print(f"missing curriculum doc: curriculum/{filename}")
            fail = True
            continue

        content = path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()

        home_line = get_second_non_blank_line(lines)
        if home_line != "Home: [README](../README.md)":
            print(f"bad home line: curriculum/{filename}")
            fail = True

        last_h2 = find_last_h2(lines)
        if last_h2 != "## Next":
            print(f"last heading is not ## Next: curriculum/{filename}")
            fail = True

        # Source sections
        if "## Primary Sources" not in content:
            print(f"missing Primary Sources: curriculum/{filename}")
            fail = True
        if "## Optional Resources" not in content:
            print(f"missing Optional Resources: curriculum/{filename}")
            fail = True

        # Next-chain
        if filename in CURRICULUM_NEXT_CHAIN:
            expected = CURRICULUM_NEXT_CHAIN[filename]
            actual = extract_next_link(lines, "./")
            if not actual:
                print(f"missing next link after ## Next: curriculum/{filename}")
                fail = True
            elif actual != expected:
                print(
                    f"bad next target in curriculum/{filename}: "
                    f"expected {expected} got {actual}"
                )
                fail = True

    # Stale reference check
    for md_file in ROOT_DIR.rglob("*.md"):
        if "_archive" in str(md_file):
            continue
        if "PythonBootcamp" in str(md_file):
            continue
        try:
            text = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if "00_README.md" in text:
            print(f"stale 00_README.md reference: {md_file.relative_to(ROOT_DIR)}")
            fail = True

    if fail:
        print("root doc contract check failed")
        return False

    print("root doc contract verified")
    return True


def main() -> None:
    success = check()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
