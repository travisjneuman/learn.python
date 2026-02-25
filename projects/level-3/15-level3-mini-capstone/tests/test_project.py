"""Tests for Level 3 Mini Capstone — Project Health Dashboard."""

from pathlib import Path

import pytest

from project import (
    DirectoryMetrics,
    FileMetrics,
    HealthReport,
    analyse_directory,
    analyse_python_file,
    calculate_score,
    check_large_files,
    check_missing_readme,
    check_missing_tests,
    format_report_text,
    generate_report,
)


@pytest.fixture
def sample_project(tmp_path: Path) -> Path:
    """Create a minimal project structure."""
    (tmp_path / "README.md").write_text("# My Project\n", encoding="utf-8")
    (tmp_path / "main.py").write_text(
        "def hello():\n    return 'hi'\n\ndef bye():\n    return 'bye'\n",
        encoding="utf-8",
    )
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_main.py").write_text(
        "def test_hello():\n    assert True\n",
        encoding="utf-8",
    )
    return tmp_path


def test_analyse_python_file(tmp_path: Path) -> None:
    """Should count lines, functions, and classes."""
    f = tmp_path / "example.py"
    f.write_text(
        "# comment\n\ndef func_a():\n    pass\n\nclass MyClass:\n    pass\n",
        encoding="utf-8",
    )
    metrics = analyse_python_file(f)
    assert metrics.lines == 7
    assert metrics.functions == 1
    assert metrics.classes == 1
    assert metrics.comment_lines == 1
    assert metrics.blank_lines == 2


def test_analyse_directory(sample_project: Path) -> None:
    """Should find all Python files recursively."""
    metrics = analyse_directory(sample_project)
    assert metrics.total_files >= 2  # main.py + test_main.py
    assert metrics.total_functions >= 2


def test_analyse_directory_not_a_dir(tmp_path: Path) -> None:
    """Non-directory should raise NotADirectoryError."""
    f = tmp_path / "file.txt"
    f.write_text("hi", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        analyse_directory(f)


def test_check_large_files() -> None:
    """Should flag files over the line limit."""
    files = [
        FileMetrics("small.py", "/s.py", 50, 5, 5, 40, 3, 0),
        FileMetrics("big.py", "/b.py", 500, 50, 50, 400, 20, 5),
    ]
    issues = check_large_files(files, max_lines=300)
    assert len(issues) == 1
    assert issues[0].file == "big.py"


def test_check_missing_readme_present(sample_project: Path) -> None:
    """Project with README should have no issues."""
    issues = check_missing_readme(sample_project)
    assert len(issues) == 0


def test_check_missing_readme_absent(tmp_path: Path) -> None:
    """Project without README should be flagged."""
    issues = check_missing_readme(tmp_path)
    assert len(issues) == 1


def test_check_missing_tests_present(sample_project: Path) -> None:
    """Project with tests should have no issues."""
    issues = check_missing_tests(sample_project)
    assert len(issues) == 0


def test_check_missing_tests_absent(tmp_path: Path) -> None:
    """Project without tests should be flagged."""
    issues = check_missing_tests(tmp_path)
    assert len(issues) == 1


def test_calculate_score_perfect() -> None:
    """No issues should give 100/A."""
    score, grade = calculate_score([])
    assert score == 100
    assert grade == "A"


def test_calculate_score_with_issues() -> None:
    """Issues should reduce the score."""
    from project import HealthIssue
    issues = [
        HealthIssue("warning", "size", "too big"),
        HealthIssue("warning", "docs", "no readme"),
    ]
    score, grade = calculate_score(issues)
    assert score == 80
    assert grade == "B"


def test_generate_report(sample_project: Path) -> None:
    """Full report should include metrics and score."""
    report = generate_report(sample_project)
    assert report.score > 0
    assert report.grade in ("A", "B", "C", "D", "F")
    assert report.metrics.total_files >= 2


def test_format_report_text() -> None:
    """Text format should contain key information."""
    report = HealthReport(
        project_path="/test",
        metrics=DirectoryMetrics("test", 5, 100, 80, 10, 2, 20.0),
        score=90,
        grade="A",
    )
    text = format_report_text(report)
    assert "90/100" in text
    assert "Grade: A" in text
