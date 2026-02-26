"""SME Mentorship Toolkit — Match mentors to mentees, track progress, generate reports.

Architecture: Uses a weighted matching algorithm where mentors and mentees declare
skill areas and goals. The matcher computes compatibility scores based on skill
overlap, experience delta, and availability. A ProgressTracker records milestones
and produces mentorship effectiveness reports.

Design rationale: Ad-hoc mentorship often fails because pairings are suboptimal
or progress is invisible. By formalizing skill matching and milestone tracking,
organizations can measure mentorship ROI and ensure knowledge transfer happens
systematically rather than by chance.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

# WHY integer values on SkillLevel? -- The numeric values enable arithmetic:
# experience_delta = mentor.level.value - mentee.level.value. A delta of 1-2
# is ideal (close enough to empathize, far enough to teach). Delta 0 means
# peer pairing, delta 3+ may cause communication gaps. The matching algorithm
# uses these numbers to compute compatibility scores.
class SkillLevel(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


class MilestoneStatus(Enum):
    PLANNED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()


@dataclass(frozen=True)
class Skill:
    """A skill with proficiency level."""
    name: str
    level: SkillLevel


@dataclass
class Person:
    """Base for mentors and mentees."""
    person_id: str
    name: str
    skills: list[Skill] = field(default_factory=list)
    availability_hours_per_week: float = 2.0

    @property
    def skill_names(self) -> set[str]:
        return {s.name for s in self.skills}

    def skill_level(self, skill_name: str) -> SkillLevel | None:
        for s in self.skills:
            if s.name == skill_name:
                return s.level
        return None


@dataclass
class Mentor(Person):
    """A mentor with years of experience."""
    years_experience: int = 5
    max_mentees: int = 3


@dataclass
class Mentee(Person):
    """A mentee with learning goals."""
    goals: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class MatchResult:
    """Result of matching a mentor-mentee pair."""
    mentor_id: str
    mentee_id: str
    compatibility_score: float
    matched_skills: list[str]
    experience_gap: int


@dataclass
class Milestone:
    """A trackable mentorship milestone."""
    milestone_id: str
    title: str
    mentee_id: str
    mentor_id: str
    status: MilestoneStatus = MilestoneStatus.PLANNED
    notes: str = ""


# ---------------------------------------------------------------------------
# Matching algorithm
# ---------------------------------------------------------------------------

def compute_compatibility(mentor: Mentor, mentee: Mentee) -> MatchResult:
    """Compute how well a mentor matches a mentee based on skill overlap and goals."""
    mentor_skills = mentor.skill_names
    mentee_skills = mentee.skill_names
    goal_skills = set(mentee.goals)

    # Skills the mentor has that align with mentee goals
    matched = mentor_skills & (mentee_skills | goal_skills)

    # Skill overlap score (0-40)
    overlap_score = min(len(matched) * 10, 40)

    # Experience delta bonus (mentors should be more experienced)
    exp_gap = mentor.years_experience
    exp_score = min(exp_gap * 3, 30)

    # Availability alignment (0-20)
    avail_score = min(mentor.availability_hours_per_week, mentee.availability_hours_per_week) * 5
    avail_score = min(avail_score, 20)

    # Level gap bonus — mentor should be significantly more skilled
    level_bonus = 0.0
    for skill_name in matched:
        m_level = mentor.skill_level(skill_name)
        e_level = mentee.skill_level(skill_name)
        if m_level and e_level and m_level.value > e_level.value:
            level_bonus += (m_level.value - e_level.value) * 5
    level_bonus = min(level_bonus, 20)

    total = overlap_score + exp_score + avail_score + level_bonus

    return MatchResult(
        mentor_id=mentor.person_id,
        mentee_id=mentee.person_id,
        compatibility_score=round(total, 1),
        matched_skills=sorted(matched),
        experience_gap=exp_gap,
    )


class MentorMatcher:
    """Matches mentees with the best available mentors."""

    def __init__(self, mentors: list[Mentor], mentees: list[Mentee]) -> None:
        self._mentors = mentors
        self._mentees = mentees

    def match_all(self) -> list[MatchResult]:
        """Greedy matching: each mentee gets the best available mentor."""
        assignments: dict[str, int] = {m.person_id: 0 for m in self._mentors}
        results: list[MatchResult] = []

        for mentee in self._mentees:
            candidates: list[MatchResult] = []
            for mentor in self._mentors:
                if assignments[mentor.person_id] < mentor.max_mentees:
                    candidates.append(compute_compatibility(mentor, mentee))

            if candidates:
                best = max(candidates, key=lambda r: r.compatibility_score)
                results.append(best)
                assignments[best.mentor_id] += 1

        return results

    def match_single(self, mentee: Mentee) -> MatchResult | None:
        """Find the best mentor for a single mentee."""
        results = [compute_compatibility(m, mentee) for m in self._mentors]
        return max(results, key=lambda r: r.compatibility_score) if results else None


# ---------------------------------------------------------------------------
# Progress tracker
# ---------------------------------------------------------------------------

class ProgressTracker:
    """Tracks milestones and computes mentorship effectiveness."""

    def __init__(self) -> None:
        self._milestones: list[Milestone] = []

    def add_milestone(self, milestone: Milestone) -> None:
        self._milestones.append(milestone)

    def complete_milestone(self, milestone_id: str) -> bool:
        for m in self._milestones:
            if m.milestone_id == milestone_id:
                m.status = MilestoneStatus.COMPLETED
                return True
        return False

    def milestones_for_pair(self, mentor_id: str, mentee_id: str) -> list[Milestone]:
        return [m for m in self._milestones
                if m.mentor_id == mentor_id and m.mentee_id == mentee_id]

    @property
    def completion_rate(self) -> float:
        if not self._milestones:
            return 0.0
        done = sum(1 for m in self._milestones if m.status == MilestoneStatus.COMPLETED)
        return (done / len(self._milestones)) * 100

    def report(self) -> dict[str, Any]:
        by_status: dict[str, int] = {}
        for s in MilestoneStatus:
            by_status[s.name.lower()] = sum(1 for m in self._milestones if m.status == s)
        return {
            "total_milestones": len(self._milestones),
            "completion_rate": f"{self.completion_rate:.0f}%",
            "by_status": by_status,
        }


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

def main() -> None:
    mentors = [
        Mentor("M1", "Alice", [Skill("python", SkillLevel.EXPERT), Skill("sql", SkillLevel.ADVANCED)],
               years_experience=10, max_mentees=2),
        Mentor("M2", "Bob", [Skill("javascript", SkillLevel.EXPERT), Skill("react", SkillLevel.ADVANCED)],
               years_experience=8),
    ]
    mentees = [
        Mentee("E1", "Carol", [Skill("python", SkillLevel.BEGINNER)], goals=["python", "sql"]),
        Mentee("E2", "Dave", [Skill("javascript", SkillLevel.INTERMEDIATE)], goals=["react"]),
        Mentee("E3", "Eve", [Skill("python", SkillLevel.INTERMEDIATE)], goals=["python"]),
    ]

    matcher = MentorMatcher(mentors, mentees)
    matches = matcher.match_all()

    print("Matches:")
    for m in matches:
        print(f"  {m.mentee_id} -> {m.mentor_id} (score: {m.compatibility_score}, skills: {m.matched_skills})")

    tracker = ProgressTracker()
    tracker.add_milestone(Milestone("MS-001", "Complete Python basics", "E1", "M1"))
    tracker.add_milestone(Milestone("MS-002", "Build first React component", "E2", "M2"))
    tracker.complete_milestone("MS-001")

    print(f"\n{json.dumps(tracker.report(), indent=2)}")


if __name__ == "__main__":
    main()
