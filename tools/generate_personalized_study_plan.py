"""Generate a personalized study plan from learner constraints.

Produces a markdown study plan based on experience level, available hours,
learning mode, and goals. The logic is intentionally explicit and deterministic
so learners can read, modify, and understand every recommendation rule.

Usage:
    python tools/generate_personalized_study_plan.py \\
        --hours-per-week 10 --learning-mode hybrid \\
        --confidence medium --experience beginner --goal full_stack

    python tools/generate_personalized_study_plan.py \\
        --hours-per-week 5 --learning-mode play \\
        --confidence low --experience zero --goal automation \\
        --output my-plan.md
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PlanInput:
    """Normalized learner profile used for deterministic recommendations."""

    hours_per_week: int
    learning_mode: str
    confidence: str
    experience: str
    goal: str
    stuck_area: str


def parse_args() -> argparse.Namespace:
    """Parse CLI options for learner profile inputs."""
    parser = argparse.ArgumentParser(description="Generate personalized study plan")
    parser.add_argument("--hours-per-week", type=int, required=True)
    parser.add_argument("--learning-mode", choices=["play", "structured", "hybrid"], required=True)
    parser.add_argument("--confidence", choices=["low", "medium", "high"], required=True)
    parser.add_argument(
        "--experience", choices=["zero", "beginner", "intermediate", "advanced"], required=True
    )
    parser.add_argument("--goal", choices=["automation", "full_stack", "elite"], required=True)
    parser.add_argument("--stuck-area", default="none")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def build_profile(args: argparse.Namespace) -> PlanInput:
    """Build validated profile object and enforce minimum safe bounds."""
    if args.hours_per_week < 2:
        raise ValueError("hours-per-week must be at least 2")
    return PlanInput(
        hours_per_week=args.hours_per_week,
        learning_mode=args.learning_mode,
        confidence=args.confidence,
        experience=args.experience,
        goal=args.goal,
        stuck_area=args.stuck_area,
    )


def recommend_doc_start(experience: str) -> str:
    """Pick the safest starting doc based on experience estimate."""
    mapping = {
        # Zero/beginner learners always start at roadmap to preserve fundamentals.
        "zero": "01_ROADMAP.md",
        "beginner": "01_ROADMAP.md",
        # Intermediate learners can still benefit from glossary/setup checks.
        "intermediate": "02_GLOSSARY.md",
        # Advanced learners can start at quality/architecture layers if desired.
        "advanced": "09_QUALITY_TOOLING.md",
    }
    return mapping[experience]


def recommend_project_start(experience: str) -> str:
    """Map experience estimate to project ladder starting level."""
    mapping = {
        "zero": "projects/level-0/README.md",
        "beginner": "projects/level-1/README.md",
        "intermediate": "projects/level-3/README.md",
        "advanced": "projects/level-6/README.md",
    }
    return mapping[experience]


def recommend_weekly_pattern(profile: PlanInput) -> str:
    """Generate pacing guidance from hours and confidence."""
    if profile.hours_per_week <= 5:
        return "3 sessions/week x 60-90 minutes + 1 short review"
    if profile.hours_per_week <= 10:
        return "4 sessions/week x 90-120 minutes + 1 review block"
    return "5+ sessions/week with one deep project/refactor day"


def recommend_priority_chain(goal: str) -> list[str]:
    """Return key doc anchors based on learner end-goal."""
    base = [
        "01_ROADMAP.md",
        "03_SETUP_ALL_PLATFORMS.md",
        "04_FOUNDATIONS.md",
        "09_QUALITY_TOOLING.md",
    ]
    if goal == "automation":
        return base + ["05_AUTOMATION_FILES_EXCEL.md", "06_SQL.md", "11_CHECKLISTS.md"]
    if goal == "full_stack":
        return base + [
            "06_SQL.md",
            "07_MONITORING_API_INTEGRATION.md",
            "08_DASHBOARDS.md",
            "21_FULL_STACK_MASTERY_PATH.md",
        ]
    return base + [
        "21_FULL_STACK_MASTERY_PATH.md",
        "26_ZERO_TO_MASTER_PLAYBOOK.md",
        "36_ELITE_ENGINEERING_TRACK.md",
        "46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md",
    ]


def remediation_actions(stuck_area: str) -> list[str]:
    """Map stuck area to concrete recovery actions."""
    key = stuck_area.lower().strip()
    mapping: dict[str, list[str]] = {
        "setup": [
            "Re-run 03_SETUP_ALL_PLATFORMS.md from Step 1 with expected outputs.",
            "Use one clean folder and rebuild .venv/test baseline.",
        ],
        "testing": [
            "Run one project and break one test intentionally.",
            "Use traceback-first debugging protocol from 04_FOUNDATIONS.md.",
        ],
        "sql": [
            "Re-run idempotency drills in 06_SQL.md before adding features.",
            "Validate row counts across reruns.",
        ],
        "focus": [
            "Switch to 25-minute micro-sessions for one week.",
            "End each session with one runnable success artifact.",
        ],
        "none": ["Continue current plan and run weekly review discipline."],
    }
    return mapping.get(key, ["Use 34_FAILURE_RECOVERY_ATLAS.md and capture one root cause note."])


def render_markdown(profile: PlanInput) -> str:
    """Render final markdown plan for learner execution."""
    start_doc = recommend_doc_start(profile.experience)
    start_project = recommend_project_start(profile.experience)
    weekly_pattern = recommend_weekly_pattern(profile)
    priorities = recommend_priority_chain(profile.goal)
    actions = remediation_actions(profile.stuck_area)

    lines: list[str] = []
    lines.append("# Personalized Python Mastery Plan")
    lines.append("")
    lines.append("## Learner profile")
    lines.append(f"- Hours/week: {profile.hours_per_week}")
    lines.append(f"- Learning mode: {profile.learning_mode}")
    lines.append(f"- Confidence: {profile.confidence}")
    lines.append(f"- Experience: {profile.experience}")
    lines.append(f"- Goal: {profile.goal}")
    lines.append(f"- Current stuck area: {profile.stuck_area}")
    lines.append("")
    lines.append("## Starting point")
    lines.append(f"- Start doc: `{start_doc}`")
    lines.append(f"- Start projects index: `{start_project}`")
    lines.append(f"- Weekly pattern: {weekly_pattern}")
    lines.append("")
    lines.append("## Priority doc chain")
    for item in priorities:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("## If blocked")
    for action in actions:
        lines.append(f"- {action}")
    lines.append("")
    lines.append("## Execution rules")
    lines.append("- Do not skip break/fix drills.")
    lines.append("- Keep one active project at a time when behind schedule.")
    lines.append("- Re-run this diagnostic every 4 weeks.")

    return "\n".join(lines) + "\n"


def main() -> int:
    """Entry point for CLI execution."""
    args = parse_args()
    profile = build_profile(args)
    plan_md = render_markdown(profile)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(plan_md, encoding="utf-8")
        print(f"personalized plan written: {out_path}")
    else:
        print(plan_md)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
