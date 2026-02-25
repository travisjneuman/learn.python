"""Tests for File Extension Counter."""

from pathlib import Path

from project import count_extensions, count_extensions_from_list, sort_by_count


def test_count_extensions_from_list() -> None:
    paths = ["file.py", "test.py", "data.csv", "readme.md", "config.py"]
    counts = count_extensions_from_list(paths)
    assert counts[".py"] == 3
    assert counts[".csv"] == 1
    assert counts[".md"] == 1


def test_count_extensions_no_extension() -> None:
    paths = ["Makefile", "Dockerfile", "README"]
    counts = count_extensions_from_list(paths)
    assert counts["(no extension)"] == 3


def test_count_extensions_real_dir(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")
    (tmp_path / "c.py").write_text("c", encoding="utf-8")
    counts = count_extensions(tmp_path)
    assert counts[".txt"] == 2
    assert counts[".py"] == 1


def test_sort_by_count() -> None:
    counts = {".py": 5, ".txt": 2, ".md": 8}
    sorted_counts = sort_by_count(counts)
    assert sorted_counts[0] == (".md", 8)
    assert sorted_counts[1] == (".py", 5)
