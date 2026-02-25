"""Tests for Duplicate Record Investigator."""

from pathlib import Path
import pytest

from project import bigrams, jaccard_similarity, find_duplicates, run


def test_bigrams_basic() -> None:
    result = bigrams("hello")
    assert "he" in result
    assert "lo" in result


@pytest.mark.parametrize(
    "a, b, min_expected",
    [
        ("hello", "hello", 1.0),
        ("hello", "hallo", 0.3),  # similar but not identical
        ("abc", "xyz", 0.0),       # completely different
        ("", "", 1.0),             # both empty
    ],
)
def test_jaccard_similarity(a: str, b: str, min_expected: float) -> None:
    score = jaccard_similarity(a, b)
    assert score >= min_expected


def test_find_exact_duplicates() -> None:
    rows = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"},
        {"name": "Alice", "email": "alice@example.com"},
    ]
    dupes = find_duplicates(rows, ["name", "email"])
    assert len(dupes) == 1
    assert dupes[0]["match_type"] == "exact"


def test_find_fuzzy_duplicates() -> None:
    rows = [
        {"name": "Jonathan Smith", "email": "jon@example.com"},
        {"name": "Johnathan Smith", "email": "jon@example.com"},
    ]
    dupes = find_duplicates(rows, ["name"], threshold=0.7)
    assert len(dupes) == 1
    assert dupes[0]["match_type"] == "fuzzy"


def test_no_duplicates() -> None:
    rows = [
        {"name": "Alice", "email": "a@x.com"},
        {"name": "Bob", "email": "b@x.com"},
    ]
    dupes = find_duplicates(rows, ["name", "email"])
    assert len(dupes) == 0


def test_run_integration(tmp_path: Path) -> None:
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "name,email\nAlice,a@x.com\nAlice,a@x.com\nBob,b@x.com\n",
        encoding="utf-8",
    )
    output = tmp_path / "report.json"
    report = run(csv_file, output, ["name", "email"])
    assert output.exists()
    assert report["duplicate_pairs_found"] == 1
