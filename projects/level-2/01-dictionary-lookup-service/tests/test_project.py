"""Tests for Dictionary Lookup Service.

Covers:
- Loading a dictionary from file
- Exact and fuzzy lookups
- Batch lookups with ordering
- Statistics computation
- Error handling for missing files
"""

from pathlib import Path

import pytest

from project import batch_lookup, dictionary_stats, load_dictionary, lookup


@pytest.fixture
def sample_dict_file(tmp_path: Path) -> Path:
    """Create a temporary dictionary file."""
    content = (
        "python = A high-level programming language\n"
        "java = A compiled object-oriented language\n"
        "javascript = A dynamic language for the web\n"
        "rust = A systems language focused on safety\n"
        "go = A compiled language by Google\n"
    )
    p = tmp_path / "dict.txt"
    p.write_text(content, encoding="utf-8")
    return p


def test_load_dictionary_parses_key_value_pairs(sample_dict_file: Path) -> None:
    """Verify that key=value lines are parsed correctly."""
    d = load_dictionary(sample_dict_file)
    assert d["python"] == "A high-level programming language"
    assert len(d) == 5


def test_load_dictionary_skips_invalid_lines(tmp_path: Path) -> None:
    """Lines without '=' should be silently ignored."""
    p = tmp_path / "partial.txt"
    p.write_text("valid = yes\nno equals here\nalso_valid = sure\n", encoding="utf-8")
    d = load_dictionary(p)
    assert len(d) == 2
    assert "valid" in d


def test_lookup_found(sample_dict_file: Path) -> None:
    """An exact match should return found=True with the definition."""
    d = load_dictionary(sample_dict_file)
    result = lookup(d, "Python")  # case-insensitive
    assert result["found"] is True
    assert "programming language" in result["definition"]
    assert result["suggestions"] == []


def test_lookup_not_found_with_suggestions(sample_dict_file: Path) -> None:
    """A near-miss should return found=False with suggestions."""
    d = load_dictionary(sample_dict_file)
    result = lookup(d, "pythn")  # close to "python"
    assert result["found"] is False
    assert result["definition"] is None
    assert "python" in result["suggestions"]


@pytest.mark.parametrize(
    "term,expected_found",
    [("java", True), ("RUST", True), ("haskell", False)],
)
def test_lookup_parametrized(
    sample_dict_file: Path, term: str, expected_found: bool
) -> None:
    """Verify lookups across multiple terms."""
    d = load_dictionary(sample_dict_file)
    result = lookup(d, term)
    assert result["found"] is expected_found


def test_batch_lookup_preserves_order(sample_dict_file: Path) -> None:
    """Batch results should keep the original query index."""
    d = load_dictionary(sample_dict_file)
    results = batch_lookup(d, ["go", "missing", "java"])
    assert [r["index"] for r in results] == [0, 1, 2]
    assert results[0]["found"] is True
    assert results[1]["found"] is False


def test_dictionary_stats(sample_dict_file: Path) -> None:
    """Stats should report counts and sorted keys."""
    d = load_dictionary(sample_dict_file)
    stats = dictionary_stats(d)
    assert stats["total_entries"] == 5
    assert isinstance(stats["unique_first_letters"], list)


def test_load_dictionary_missing_file(tmp_path: Path) -> None:
    """A missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_dictionary(tmp_path / "nope.txt")
