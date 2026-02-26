# Anomaly Flagger — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Anomaly Flagger — complete annotated solution."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def mean(values: list[float]) -> float:
    """Calculate the arithmetic mean (average)."""
    # WHY: Guard against empty lists. sum([]) is 0 but len([]) is 0,
    # so division would raise ZeroDivisionError.
    if not values:
        return 0.0
    return sum(values) / len(values)


def std_dev(values: list[float]) -> float:
    """Calculate the population standard deviation.

    Measures how spread out values are from the mean.
    """
    # WHY: Standard deviation is undefined for fewer than 2 values.
    # A single value has no spread — returning 0 is mathematically correct
    # (zero variance).
    if len(values) < 2:
        return 0.0

    avg = mean(values)
    # WHY: Variance is the average of squared differences from the mean.
    # Squaring ensures positive and negative deviations do not cancel out.
    # sqrt(variance) gives us standard deviation in the original units.
    variance = sum((x - avg) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def z_score(value: float, values: list[float]) -> float:
    """Calculate how many standard deviations a value is from the mean.

    |z| > 2 is unusual, |z| > 3 is very unusual.
    """
    avg = mean(values)
    sd = std_dev(values)
    # WHY: If std_dev is 0, all values are identical. No value can be
    # an outlier in a dataset where everything is the same.
    if sd == 0:
        return 0.0
    return (value - avg) / sd


def percentile(values: list[float], p: float) -> float:
    """Calculate the p-th percentile using linear interpolation."""
    if not values:
        return 0.0

    sorted_vals = sorted(values)
    n = len(sorted_vals)

    # WHY: Linear interpolation gives a smooth percentile estimate.
    # For p=25 with 10 values, idx = 0.25 * 9 = 2.25, meaning the
    # 25th percentile is 25% of the way between sorted_vals[2] and sorted_vals[3].
    idx = (p / 100) * (n - 1)
    lower = int(idx)
    upper = min(lower + 1, n - 1)
    fraction = idx - lower

    return sorted_vals[lower] + fraction * (sorted_vals[upper] - sorted_vals[lower])


def iqr_bounds(values: list[float], factor: float = 1.5) -> tuple[float, float]:
    """Calculate IQR-based anomaly boundaries.

    IQR = Q3 - Q1. Values outside [Q1 - factor*IQR, Q3 + factor*IQR] are anomalies.
    """
    q1 = percentile(values, 25)
    q3 = percentile(values, 75)
    # WHY: The IQR (interquartile range) measures spread of the middle 50%.
    # Unlike standard deviation, it is not affected by extreme outliers,
    # making it more robust for skewed distributions.
    iqr = q3 - q1

    return (q1 - factor * iqr, q3 + factor * iqr)


def detect_anomalies_zscore(
    values: list[float], threshold: float = 2.0
) -> list[dict]:
    """Detect anomalies using z-score method."""
    anomalies: list[dict] = []

    for idx, value in enumerate(values):
        z = z_score(value, values)
        # WHY: abs(z) > threshold catches both high and low outliers.
        # A z-score of -3 (unusually low) is just as anomalous as +3
        # (unusually high).
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
    """Detect anomalies using IQR method."""
    # WHY: IQR needs at least 4 values to compute meaningful quartiles.
    # With fewer values, Q1 and Q3 are too close together and almost
    # everything would be flagged.
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
    """Run both anomaly detection methods and return a full report."""
    z_anomalies = detect_anomalies_zscore(values, threshold=z_threshold)
    iqr_anomalies = detect_anomalies_iqr(values, factor=iqr_factor)

    # WHY: Set intersection finds values flagged by BOTH methods.
    # An anomaly detected by two independent methods is a much stronger
    # signal than one flagged by only one method.
    z_indices = {a["index"] for a in z_anomalies}
    iqr_indices = {a["index"] for a in iqr_anomalies}
    both_indices = z_indices & iqr_indices

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
        # WHY: Set union counts total unique anomaly indices across both methods.
        "total_anomalies": len(z_indices | iqr_indices),
    }


def load_values(path: Path) -> list[float]:
    """Load numeric values from a file (one number per line)."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    values: list[float] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        # WHY: Skip blank lines and comment lines (starting with #).
        # This makes the input format flexible and self-documenting.
        if not stripped or stripped.startswith("#"):
            continue
        try:
            values.append(float(stripped))
        except ValueError:
            continue

    return values


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Anomaly flagger")
    parser.add_argument("input", help="Path to data file (one number per line)")
    parser.add_argument("--z-threshold", type=float, default=2.0, help="Z-score threshold")
    parser.add_argument("--iqr-factor", type=float, default=1.5, help="IQR factor")
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Two detection methods (z-score + IQR) | Z-score assumes normally distributed data and is sensitive to extreme outliers. IQR is robust to skewed distributions. Using both gives a more complete picture and lets users see where the methods agree. |
| Set intersection for "flagged by both" | An anomaly detected by two independent methods is a much stronger signal. Set intersection (`&`) efficiently finds these overlapping indices in O(n) time. |
| Manual statistics instead of `statistics` module | Building mean, std_dev, and percentile from scratch teaches the math. In production, use `statistics.mean()`, `statistics.stdev()`, and `numpy.percentile()`. |
| Population std_dev (dividing by N, not N-1) | Population std_dev uses all data points. Sample std_dev (dividing by N-1) is used when your data is a sample of a larger population. For anomaly detection on a complete dataset, population std_dev is appropriate. |
| Configurable thresholds | Different domains need different sensitivity. Server response times might use z-threshold=3 (flag only extreme outliers), while medical data might use z-threshold=1.5 (flag anything unusual). |

## Alternative Approaches

### Using `numpy` and `scipy` for statistical analysis

```python
import numpy as np
from scipy import stats

values = np.array([10, 12, 11, 200, 13, 11])
z_scores = np.abs(stats.zscore(values))
anomalies = np.where(z_scores > 2)[0]  # Indices where |z| > 2

q1, q3 = np.percentile(values, [25, 75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
iqr_anomalies = np.where((values < lower) | (values > upper))[0]
```

NumPy and SciPy compute statistics on entire arrays at once (vectorized operations), which is orders of magnitude faster than Python loops for large datasets. The manual approach here teaches the underlying algorithms.

### Using a sliding window for time-series anomaly detection

For time-ordered data (like server metrics), a global mean/std_dev may not be meaningful because the baseline changes over time. A sliding window computes statistics over the last N values and flags deviations from the recent trend, not the global average.

## Common Pitfalls

1. **Division by zero when all values are identical** — If every value is 50, std_dev is 0, and computing `(value - mean) / std_dev` divides by zero. The `if sd == 0: return 0.0` guard in `z_score()` prevents this crash.

2. **IQR on very small datasets** — With only 3 values, Q1 and Q3 are essentially the min and max, making the IQR nearly the full data range. The `if len(values) < 4: return []` guard prevents meaningless anomaly detection on tiny datasets.

3. **Confusing population vs sample standard deviation** — Dividing by `N` gives population std_dev; dividing by `N-1` gives sample std_dev (Bessel's correction). Using the wrong one changes the threshold sensitivity. For this project, population std_dev is correct because we are analyzing the entire dataset, not estimating from a sample.
