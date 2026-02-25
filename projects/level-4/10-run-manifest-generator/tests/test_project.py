"""Tests for Run Manifest Generator."""

from pathlib import Path
import pytest

from project import compute_checksum, scan_files, build_manifest, run


def test_compute_checksum_deterministic(tmp_path: Path) -> None:
    """Same content always produces the same checksum."""
    file_a = tmp_path / "a.txt"
    file_b = tmp_path / "b.txt"
    file_a.write_text("hello world", encoding="utf-8")
    file_b.write_text("hello world", encoding="utf-8")
    assert compute_checksum(file_a) == compute_checksum(file_b)


def test_compute_checksum_differs_for_different_content(tmp_path: Path) -> None:
    file_a = tmp_path / "a.txt"
    file_b = tmp_path / "b.txt"
    file_a.write_text("hello", encoding="utf-8")
    file_b.write_text("world", encoding="utf-8")
    assert compute_checksum(file_a) != compute_checksum(file_b)


def test_scan_files_collects_metadata(tmp_path: Path) -> None:
    (tmp_path / "file1.txt").write_text("abc", encoding="utf-8")
    (tmp_path / "file2.csv").write_text("x,y,z", encoding="utf-8")
    files = scan_files(tmp_path)
    assert len(files) == 2
    assert all("checksum_md5" in f for f in files)
    assert all("size_bytes" in f for f in files)


@pytest.mark.parametrize("file_count", [0, 1, 5])
def test_build_manifest_file_count(tmp_path: Path, file_count: int) -> None:
    for i in range(file_count):
        (tmp_path / f"file_{i}.txt").write_text(f"content {i}", encoding="utf-8")
    manifest = build_manifest("test-run", tmp_path)
    assert manifest["file_count"] == file_count
    assert manifest["run_id"] == "test-run"


def test_scan_files_includes_subdirectories(tmp_path: Path) -> None:
    sub = tmp_path / "subdir"
    sub.mkdir()
    (sub / "nested.txt").write_text("nested", encoding="utf-8")
    files = scan_files(tmp_path)
    assert any("subdir" in f["relative_path"] for f in files)


def test_run_integration(tmp_path: Path) -> None:
    (tmp_path / "data.txt").write_text("test data", encoding="utf-8")
    output = tmp_path / "manifest.json"
    manifest = run(tmp_path, output, run_id="test-123")
    assert output.exists()
    assert manifest["run_id"] == "test-123"
    assert manifest["file_count"] >= 1
