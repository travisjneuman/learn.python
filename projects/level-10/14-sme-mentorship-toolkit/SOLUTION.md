# Solution: Level 10 / Project 14 - SME Mentorship Toolkit

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""SME Mentorship Toolkit -- Match mentors to mentees, track progress, generate reports."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


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
    name: str
    level: SkillLevel


@dataclass
class Person:
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
    years_experience: int = 5
    max_mentees: int = 3


@dataclass
class Mentee(Person):
    goals: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class MatchResult:
    mentor_id: str
    mentee_id: str
    compatibility_score: float
    matched_skills: list[str]
    experience_gap: int


@dataclass
class Milestone:
    milestone_id: str
    title: str
    mentee_id: str
    mentor_id: str
    status: MilestoneStatus = MilestoneStatus.PLANNED
    notes: str = ""


# WHY four scoring dimensions? -- Skill overlap alone misses important factors.
# A mentor who matches on skills but has zero availability is useless. A mentor
# whose skill level equals the mentee's cannot teach them. The four dimensions
# (overlap, experience, availability, level gap) produce realistic compatibility
# scores that account for real-world mentorship dynamics.
def compute_compatibility(mentor: Mentor, mentee: Mentee) -> MatchResult:
    mentor_skills = mentor.skill_names
    mentee_skills = mentee.skill_names
    goal_skills = set(mentee.goals)

    # WHY union of mentee skills and goals? -- A mentee might want to learn
    # a skill they do not yet have (goals) or improve one they already started
    # (skills). The union ensures both cases are matched.
    matched = mentor_skills & (mentee_skills | goal_skills)

    # Skill overlap score (0-40)
    overlap_score = min(len(matched) * 10, 40)

    # Experience delta bonus (mentors should be more experienced)
    exp_gap = mentor.years_experience
    exp_score = min(exp_gap * 3, 30)

    # WHY min of both availabilities? -- Mentorship is limited by the less
    # available person. A mentor with 10 hours and a mentee with 1 hour
    # can only meet for 1 hour.
    avail_score = min(mentor.availability_hours_per_week, mentee.availability_hours_per_week) * 5
    avail_score = min(avail_score, 20)

    # Level gap bonus -- mentor should be significantly more skilled
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
    def __init__(self, mentors: list[Mentor], mentees: list[Mentee]) -> None:
        self._mentors = mentors
        self._mentees = mentees

    # WHY greedy matching instead of global optimization? -- Greedy is O(M*N)
    # and easy to explain: each mentee gets the best available mentor. Global
    # optimization (Hungarian algorithm) is O(N^3) and may produce non-obvious
    # pairings. For most organizations (< 100 people), greedy is sufficient.
    def match_all(self) -> list[MatchResult]:
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
        results = [compute_compatibility(m, mentee) for m in self._mentors]
        return max(results, key=lambda r: r.compatibility_score) if results else None


class ProgressTracker:
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Weighted multi-factor compatibility scoring | Skill overlap alone misses availability and level gaps; four factors produce realistic match quality | Single-factor matching (skills only) -- simple but produces poor pairings where mentor and mentee cannot meet |
| Greedy matching algorithm | O(M*N), easy to explain, sufficient for organizations under 100 people | Hungarian algorithm -- globally optimal O(N^3) but produces non-obvious pairings that are hard to justify to participants |
| Capacity constraints via `max_mentees` | Prevents mentor overload; spreading mentees across mentors ensures quality time for each | Unconstrained matching -- one expert gets all mentees, burns out, and quality drops |
| Separate ProgressTracker from matching | Matching is a one-time assignment; progress tracking is ongoing; separating concerns makes each independently testable | Combined Mentorship class -- mixes assignment and tracking, making both harder to test |
| SkillLevel as Enum with integer values | Enables arithmetic for level gap calculation while preventing invalid values like "level 99" | Raw integers -- no validation, no self-documentation |

## Alternative approaches

### Approach B: Hungarian algorithm for global optimal matching

```python
from scipy.optimize import linear_sum_assignment
import numpy as np

def optimal_match(mentors: list[Mentor], mentees: list[Mentee]) -> list[MatchResult]:
    """Use the Hungarian algorithm for globally optimal assignment."""
    cost_matrix = np.zeros((len(mentees), len(mentors)))
    for i, mentee in enumerate(mentees):
        for j, mentor in enumerate(mentors):
            result = compute_compatibility(mentor, mentee)
            # Negate because Hungarian minimizes cost, but we want max compatibility
            cost_matrix[i, j] = -result.compatibility_score

    row_idx, col_idx = linear_sum_assignment(cost_matrix)
    return [compute_compatibility(mentors[j], mentees[i])
            for i, j in zip(row_idx, col_idx)]
```

**Trade-off:** The Hungarian algorithm finds the globally optimal assignment, which may improve overall match quality by 10-20% compared to greedy. However, it requires scipy as a dependency, ignores capacity constraints (each mentor gets exactly one mentee), and produces results that are harder to explain to participants. For small organizations, greedy with capacity constraints is simpler and "good enough."

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Mentee with goals no mentor can fulfill | Low compatibility score (only experience and availability contribute); mentee gets a poor match | Add a minimum compatibility threshold (e.g., 30); leave unmatched mentees on a waitlist |
| All mentors at max capacity | Mentee gets no match (empty candidates list); `match_all` silently skips them | Return unmatched mentees in the result so the caller can surface the issue |
| Completing a non-existent milestone ID | `complete_milestone` returns `False` silently | Check the return value and surface a warning or raise an error |
