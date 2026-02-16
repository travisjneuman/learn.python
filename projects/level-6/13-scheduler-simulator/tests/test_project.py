from pathlib import Path

from project import load_lines


def test_load_lines_reads_non_empty_lines(tmp_path: Path):
    sample = tmp_path / "sample.txt"
    sample.write_text("alpha\n\n beta \n", encoding="utf-8")
    lines = load_lines(sample)
    assert lines == ["alpha", "beta"]


def test_load_lines_missing_file_raises(tmp_path: Path):
    missing = tmp_path / "missing.txt"
    try:
        load_lines(missing)
    except FileNotFoundError:
        assert True
        return
    assert False, "Expected FileNotFoundError"
