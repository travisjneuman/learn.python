"""Tests for Anomaly Flagger.

Covers:
- Statistical calculations (mean, std_dev, percentile)
- Z-score anomaly detection
- IQR anomaly detection
- Full dataset analysis
- File loading
"""

from pathlib import Path

import pytest

from project import (
    analyse_dataset,
    detect_anomalies_iqr,
    detect_anomalies_zscore,
    iqr_bounds,
    load_values,
    mean,
    percentile,
    std_dev,
    z_score,
)


def test_mean_basic() -> None:
    """Mean of [1, 2, 3, 4, 5] should be 3.0."""
    assert mean([1, 2, 3, 4, 5]) == 3.0


def test_mean_empty() -> None:
    """Mean of empty list should be 0.0."""
    assert mean([]) == 0.0


def test_std_dev_identical() -> None:
    """Identical values should have std_dev of 0."""
    assert std_dev([5, 5, 5, 5]) == 0.0


def test_std_dev_basic() -> None:
    """Known dataset should produce expected std_dev."""
    sd = std_dev([2, 4, 4, 4, 5, 5, 7, 9])
    assert abs(sd - 2.0) < 0.01


def test_z_score_at_mean() -> None:
    """A value at the mean should have z-score of 0."""
    values = [10, 20, 30, 40, 50]
    assert z_score(30, values) == 0.0


def test_percentile_median() -> None:
    """50th percentile should be the median."""
    values = [1, 2, 3, 4, 5]
    assert percentile(values, 50) == 3.0


@pytest.mark.parametrize(
    "p,expected",
    [(0, 1.0), (25, 2.0), (75, 4.0), (100, 5.0)],
)
def test_percentile_values(p: float, expected: float) -> None:
    """Known percentiles for [1,2,3,4,5]."""
    assert percentile([1, 2, 3, 4, 5], p) == expected


def test_detect_anomalies_zscore() -> None:
    """Extreme values should be flagged by z-score."""
    values = [10, 11, 12, 10, 11, 12, 10, 100]  # 100 is the outlier
    anomalies = detect_anomalies_zscore(values, threshold=2.0)
    indices = [a["index"] for a in anomalies]
    assert 7 in indices  # 100 should be flagged


def test_detect_anomalies_iqr() -> None:
    """Extreme values should be flagged by IQR."""
    values = [10, 11, 12, 10, 11, 12, 10, 100]
    anomalies = detect_anomalies_iqr(values, factor=1.5)
    indices = [a["index"] for a in anomalies]
    assert 7 in indices


def test_analyse_dataset() -> None:
    """Full analysis should detect anomalies and report stats."""
    values = [10, 11, 12, 10, 11, 12, 10, 11, 100, 11]
    report = analyse_dataset(values)
    assert report["statistics"]["count"] == 10
    assert report["total_anomalies"] >= 1


def test_load_values(tmp_path: Path) -> None:
    """Load should read one number per line, skip comments."""
    p = tmp_path / "data.txt"
    p.write_text("# header\n10\n20\n30\nbad\n40\n", encoding="utf-8")
    values = load_values(p)
    assert values == [10.0, 20.0, 30.0, 40.0]


def test_load_values_missing(tmp_path: Path) -> None:
    """Missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_values(tmp_path / "nope.txt")
