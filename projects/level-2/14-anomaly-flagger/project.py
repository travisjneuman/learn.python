"""Level 2 project: Anomaly Flagger.

Heavily commented beginner-friendly script:
- detect statistical anomalies in numeric datasets,
- use z-score and IQR (interquartile range) methods,
- flag outliers and generate anomaly reports.

Skills practiced: list comprehensions, sorting with key, try/except,
nested data structures, enumerate, sets, math operations.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def mean(values: list[float]) -> float:
    """Calculate the arithmetic mean (average).

    Sum of all values divided by count.
    Returns 0.0 for empty lists to avoid ZeroDivisionError.
    """
    if not values:
        return 0.0
    return sum(values) / len(values)


def std_dev(values: list[float]) -> float:
    """Calculate the population standard deviation.

    Standard deviation measures how spread out values are.
    A small std_dev means values cluster near the mean.
    A large std_dev means values are spread far apart.
    """
    if len(values) < 2:
        return 0.0

    avg = mean(values)
    # Variance is the average of squared differences from the mean.
    variance = sum((x - avg) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def z_score(value: float, values: list[float]) -> float:
    """Calculate the z-score of a value relative to a dataset.

    Z-score tells you how many standard deviations a value is
    from the mean.  |z| > 2 is unusual, |z| > 3 is very unusual.

    Returns 0.0 if std_dev is 0 (all values are identical).
    """
    avg = mean(values)
    sd = std_dev(values)
    if sd == 0:
        return 0.0
    return (value - avg) / sd


def percentile(values: list[float], p: float) -> float:
    """Calculate the p-th percentile using linear interpolation.

    p should be between 0 and 100.
    """
    if not values:
        return 0.0

    sorted_vals = sorted(values)
    n = len(sorted_vals)

    # Index position for the desired percentile.
    idx = (p / 100) * (n - 1)
    lower = int(idx)
    upper = min(lower + 1, n - 1)
    fraction = idx - lower

    return sorted_vals[lower] + fraction * (sorted_vals[upper] - sorted_vals[lower])


def iqr_bounds(values: list[float], factor: float = 1.5) -> tuple[float, float]:
    """Calculate the IQR-based anomaly boundaries.

    IQR (Interquartile Range) = Q3 - Q1.
    Lower bound = Q1 - factor * IQR
    Upper bound = Q3 + factor * IQR

    Values outside these bounds are considered anomalies.
    factor=1.5 catches mild outliers, factor=3.0 catches extreme ones.
    """
    q1 = percentile(values, 25)
    q3 = percentile(values, 75)
    iqr = q3 - q1

    return (q1 - factor * iqr, q3 + factor * iqr)


def detect_anomalies_zscore(
    values: list[float], threshold: float = 2.0
) -> list[dict]:
    """Detect anomalies using z-score method.

    Any value with |z-score| > threshold is flagged.
    Returns a list of anomaly dicts with index, value, and z-score.
    """
    anomalies: list[dict] = []

    for idx, value in enumerate(values):
        z = z_score(value, values)
        if abs(z) > threshold:
            anomalies.append({
                "index": idx,
                "value": value,
                "z_score": round(z, 3),
                "method": "z-score",
            })

    return anomalies


def detect_anomalies_iqr(
    values: list[float], factor: float = 1.5
) -> list[dict]:
    """Detect anomalies using IQR method.

    Values below (Q1 - factor*IQR) or above (Q3 + factor*IQR) are flagged.
    """
    if len(values) < 4:
        return []

    lower, upper = iqr_bounds(values, factor)
    anomalies: list[dict] = []

    for idx, value in enumerate(values):
        if value < lower or value > upper:
            direction = "below" if value < lower else "above"
            anomalies.append({
                "index": idx,
                "value": value,
                "direction": direction,
                "bounds": {"lower": round(lower, 2), "upper": round(upper, 2)},
                "method": "iqr",
            })

    return anomalies


def analyse_dataset(
    values: list[float],
    z_threshold: float = 2.0,
    iqr_factor: float = 1.5,
) -> dict:
    """Run both anomaly detection methods and return a full report.

    Combines z-score and IQR results with dataset statistics.
    """
    z_anomalies = detect_anomalies_zscore(values, threshold=z_threshold)
    iqr_anomalies = detect_anomalies_iqr(values, factor=iqr_factor)

    # Use sets to find values flagged by both methods.
    z_indices = {a["index"] for a in z_anomalies}
    iqr_indices = {a["index"] for a in iqr_anomalies}
    both_indices = z_indices & iqr_indices  # Set intersection.

    return {
        "statistics": {
            "count": len(values),
            "mean": round(mean(values), 2),
            "std_dev": round(std_dev(values), 2),
            "min": min(values) if values else 0,
            "max": max(values) if values else 0,
            "q1": round(percentile(values, 25), 2),
            "median": round(percentile(values, 50), 2),
            "q3": round(percentile(values, 75), 2),
        },
        "z_score_anomalies": z_anomalies,
        "iqr_anomalies": iqr_anomalies,
        "flagged_by_both": sorted(both_indices),
        "total_anomalies": len(z_indices | iqr_indices),
    }


def load_values(path: Path) -> list[float]:
    """Load numeric values from a file (one number per line)."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    values: list[float] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            values.append(float(stripped))
        except ValueError:
            continue  # Skip non-numeric lines.

    return values


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Anomaly flagger")
    parser.add_argument("input", help="Path to data file (one number per line)")
    parser.add_argument(
        "--z-threshold", type=float, default=2.0, help="Z-score threshold"
    )
    parser.add_argument(
        "--iqr-factor", type=float, default=1.5, help="IQR factor"
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: load data, detect anomalies, print report."""
    args = parse_args()
    values = load_values(Path(args.input))

    report = analyse_dataset(
        values, z_threshold=args.z_threshold, iqr_factor=args.iqr_factor
    )

    print(f"Dataset: {report['statistics']['count']} values, "
          f"mean={report['statistics']['mean']}, "
          f"std_dev={report['statistics']['std_dev']}")

    print(f"\nAnomalies found: {report['total_anomalies']}")

    if report["z_score_anomalies"]:
        print(f"\nZ-score anomalies (|z| > {args.z_threshold}):")
        for a in report["z_score_anomalies"]:
            print(f"  index={a['index']}, value={a['value']}, z={a['z_score']}")

    if report["iqr_anomalies"]:
        print(f"\nIQR anomalies (factor={args.iqr_factor}):")
        for a in report["iqr_anomalies"]:
            print(f"  index={a['index']}, value={a['value']}, {a['direction']}")

    if report["flagged_by_both"]:
        print(f"\nFlagged by BOTH methods: indices {report['flagged_by_both']}")


if __name__ == "__main__":
    main()
