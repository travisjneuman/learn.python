"""Tests for SME Mentorship Toolkit.

Covers matching algorithm, compatibility scoring, progress tracking,
and milestone management.
"""
from __future__ import annotations

import pytest

from project import (
    MentorMatcher,
    Mentee,
    Mentor,
    Milestone,
    MilestoneStatus,
    ProgressTracker,
    Skill,
    SkillLevel,
    compute_compatibility,
)


@pytest.fixture
def python_mentor() -> Mentor:
    return Mentor("M1", "Alice", [Skill("python", SkillLevel.EXPERT), Skill("sql", SkillLevel.ADVANCED)],
                  years_experience=10, max_mentees=2)


@pytest.fixture
def python_mentee() -> Mentee:
    return Mentee("E1", "Carol", [Skill("python", SkillLevel.BEGINNER)], goals=["python", "sql"])


@pytest.fixture
def js_mentor() -> Mentor:
    return Mentor("M2", "Bob", [Skill("javascript", SkillLevel.EXPERT)], years_experience=8)


# ---------------------------------------------------------------------------
# Compatibility scoring
# ---------------------------------------------------------------------------

class TestCompatibility:
    def test_matching_skills_increase_score(self, python_mentor: Mentor, python_mentee: Mentee) -> None:
        result = compute_compatibility(python_mentor, python_mentee)
        assert result.compatibility_score > 50
        assert "python" in result.matched_skills

    def test_no_overlap_low_score(self, js_mentor: Mentor, python_mentee: Mentee) -> None:
        result = compute_compatibility(js_mentor, python_mentee)
        assert result.compatibility_score < compute_compatibility(
            Mentor("M3", "X", [Skill("python", SkillLevel.EXPERT)], years_experience=10),
            python_mentee,
        ).compatibility_score

    def test_experience_gap_recorded(self, python_mentor: Mentor, python_mentee: Mentee) -> None:
        result = compute_compatibility(python_mentor, python_mentee)
        assert result.experience_gap == 10


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

class TestMentorMatcher:
    def test_match_all_assigns_mentees(self, python_mentor: Mentor, js_mentor: Mentor) -> None:
        mentees = [
            Mentee("E1", "Carol", goals=["python"]),
            Mentee("E2", "Dave", goals=["javascript"]),
        ]
        matcher = MentorMatcher([python_mentor, js_mentor], mentees)
        matches = matcher.match_all()
        assert len(matches) == 2

    def test_respects_max_mentees(self) -> None:
        mentor = Mentor("M1", "Alice", [Skill("python", SkillLevel.EXPERT)],
                        years_experience=5, max_mentees=1)
        mentees = [
            Mentee("E1", "Carol", goals=["python"]),
            Mentee("E2", "Dave", goals=["python"]),
        ]
        matcher = MentorMatcher([mentor], mentees)
        matches = matcher.match_all()
        assert len(matches) == 1

    def test_match_single(self, python_mentor: Mentor, python_mentee: Mentee) -> None:
        matcher = MentorMatcher([python_mentor], [])
        result = matcher.match_single(python_mentee)
        assert result is not None
        assert result.mentor_id == "M1"

    def test_match_single_no_mentors(self, python_mentee: Mentee) -> None:
        matcher = MentorMatcher([], [])
        assert matcher.match_single(python_mentee) is None


# ---------------------------------------------------------------------------
# Progress tracking
# ---------------------------------------------------------------------------

class TestProgressTracker:
    def test_initial_completion_zero(self) -> None:
        tracker = ProgressTracker()
        assert tracker.completion_rate == 0.0

    def test_complete_milestone(self) -> None:
        tracker = ProgressTracker()
        tracker.add_milestone(Milestone("MS-1", "Task 1", "E1", "M1"))
        tracker.complete_milestone("MS-1")
        assert tracker.completion_rate == 100.0

    def test_partial_completion(self) -> None:
        tracker = ProgressTracker()
        tracker.add_milestone(Milestone("MS-1", "Task 1", "E1", "M1"))
        tracker.add_milestone(Milestone("MS-2", "Task 2", "E1", "M1"))
        tracker.complete_milestone("MS-1")
        assert tracker.completion_rate == 50.0

    def test_milestones_for_pair(self) -> None:
        tracker = ProgressTracker()
        tracker.add_milestone(Milestone("MS-1", "T1", "E1", "M1"))
        tracker.add_milestone(Milestone("MS-2", "T2", "E2", "M2"))
        pair = tracker.milestones_for_pair("M1", "E1")
        assert len(pair) == 1

    def test_report_structure(self) -> None:
        tracker = ProgressTracker()
        tracker.add_milestone(Milestone("MS-1", "T1", "E1", "M1"))
        report = tracker.report()
        assert "total_milestones" in report
        assert "completion_rate" in report
        assert "by_status" in report
