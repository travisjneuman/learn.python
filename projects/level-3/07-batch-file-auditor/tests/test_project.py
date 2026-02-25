"""Tests for Batch File Auditor."""

from pathlib import Path

import pytest

from project import (
    AuditIssue,
    FileInfo,
    check_empty_files,
    check_large_files,
    check_naming_convention,
    check_no_extension,
    run_audit,
    scan_directory,
)


@pytest.fixture
def sample_dir(tmp_path: Path) -> Path:
    """Create a directory with various files for testing."""
    (tmp_path / "readme.md").write_text("# Hello", encoding="utf-8")
    (tmp_path / "data.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    (tmp_path / "empty.txt").write_text("", encoding="utf-8")
    (tmp_path / "notes").write_text("no extension", encoding="utf-8")
    return tmp_path


def test_scan_directory(sample_dir: Path) -> None:
    """Should find all files in directory."""
    files = scan_directory(sample_dir)
    assert len(files) == 4
    names = {f.name for f in files}
    assert "readme.md" in names
    assert "empty.txt" in names


def test_scan_directory_with_pattern(sample_dir: Path) -> None:
    """Pattern should filter files."""
    files = scan_directory(sample_dir, "*.md")
    assert len(files) == 1
    assert files[0].name == "readme.md"


def test_scan_not_a_directory(tmp_path: Path) -> None:
    """Non-directory should raise NotADirectoryError."""
    f = tmp_path / "file.txt"
    f.write_text("hi", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        scan_directory(f)


def test_check_empty_files() -> None:
    """Should flag empty files."""
    files = [
        FileInfo("a.txt", "/a.txt", 100, ".txt", False),
        FileInfo("b.txt", "/b.txt", 0, ".txt", True),
    ]
    issues = check_empty_files(files)
    assert len(issues) == 1
    assert issues[0].file == "b.txt"


def test_check_large_files() -> None:
    """Should flag files over the size limit."""
    files = [
        FileInfo("small.txt", "/s.txt", 100, ".txt", False),
        FileInfo("big.dat", "/b.dat", 5_000_000, ".dat", False),
    ]
    issues = check_large_files(files, max_bytes=1_000_000)
    assert len(issues) == 1
    assert issues[0].file == "big.dat"


def test_check_naming_convention() -> None:
    """Should flag files with spaces or special characters."""
    files = [
        FileInfo("good_file.txt", "/g.txt", 10, ".txt", False),
        FileInfo("Bad File!.txt", "/b.txt", 10, ".txt", False),
    ]
    issues = check_naming_convention(files)
    assert len(issues) == 1
    assert issues[0].file == "Bad File!.txt"


def test_check_no_extension() -> None:
    """Should flag files without extensions."""
    files = [
        FileInfo("readme.md", "/r.md", 10, ".md", False),
        FileInfo("Makefile", "/M", 10, "", False),
    ]
    issues = check_no_extension(files)
    assert len(issues) == 1
    assert issues[0].file == "Makefile"


def test_run_audit_integration(sample_dir: Path) -> None:
    """Full audit should combine all checks."""
    report = run_audit(sample_dir)
    assert report.total_files == 4
    assert any(i.check == "empty_file" for i in report.issues)
    assert any(i.check == "no_extension" for i in report.issues)
    assert "by_severity" in report.summary
