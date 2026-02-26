"""
NumPy Foundations — Arrays, indexing, broadcasting, and vectorized operations.

This project introduces NumPy, the foundation of Python's scientific computing
ecosystem. You'll learn to work with arrays instead of lists, which is both
faster and more expressive for numerical work.
"""

import numpy as np


# --- 1. Creating Arrays ---

def create_basic_arrays():
    """Create arrays using different NumPy constructors."""
    # From a Python list
    grades = np.array([85, 92, 78, 95, 88])

    # Pre-filled arrays
    zeros = np.zeros(5)            # [0. 0. 0. 0. 0.]
    ones = np.ones((3, 4))         # 3 rows, 4 columns of 1s
    empty = np.empty((2, 3))       # Uninitialized (fast but random values)

    # Ranges
    sequence = np.arange(0, 10, 2)       # [0, 2, 4, 6, 8] — like range() but returns array
    even_spaced = np.linspace(0, 1, 5)   # [0. 0.25 0.5 0.75 1.] — 5 evenly spaced points

    print("=== Creating Arrays ===")
    print(f"Grades:      {grades}")
    print(f"Zeros:       {zeros}")
    print(f"Ones (3x4):\n{ones}")
    print(f"Sequence:    {sequence}")
    print(f"Linspace:    {even_spaced}")
    print()

    return grades, zeros, ones, sequence, even_spaced


# --- 2. Indexing and Slicing ---

def indexing_demo():
    """Show how to access elements in 1D and 2D arrays."""
    # 1D indexing — same as Python lists
    temps = np.array([72, 68, 75, 80, 77, 69, 73])

    print("=== Indexing and Slicing ===")
    print(f"Temperatures:   {temps}")
    print(f"First day:      {temps[0]}")
    print(f"Last day:       {temps[-1]}")
    print(f"Days 2-4:       {temps[1:4]}")

    # 2D indexing — row, column
    matrix = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ])

    print(f"\nMatrix:\n{matrix}")
    print(f"Row 0:          {matrix[0]}")
    print(f"Element [1,2]:  {matrix[1, 2]}")       # Row 1, Column 2 → 6
    print(f"Column 0:       {matrix[:, 0]}")        # All rows, column 0
    print(f"Submatrix:\n{matrix[0:2, 1:3]}")        # Rows 0-1, columns 1-2
    print()

    return temps, matrix


# --- 3. Broadcasting ---

def broadcasting_demo():
    """Demonstrate NumPy's broadcasting rules."""
    prices = np.array([10.0, 20.0, 30.0, 40.0, 50.0])

    # Scalar broadcast: apply 10% discount to all prices
    discounted = prices * 0.9

    # Array broadcast: add different tax rates per item
    tax_rates = np.array([0.05, 0.08, 0.05, 0.10, 0.07])
    with_tax = prices * (1 + tax_rates)

    print("=== Broadcasting ===")
    print(f"Original prices:  {prices}")
    print(f"After 10% off:    {discounted}")
    print(f"Tax rates:        {tax_rates}")
    print(f"With tax:         {with_tax}")

    # 2D broadcasting: normalize each row
    scores = np.array([
        [80, 90, 70],
        [60, 85, 95],
    ])
    row_means = scores.mean(axis=1, keepdims=True)  # Mean per row
    normalized = scores - row_means

    print(f"\nScores:\n{scores}")
    print(f"Row means:    {row_means.flatten()}")
    print(f"Normalized:\n{normalized}")
    print()

    return discounted, with_tax, normalized


# --- 4. Vectorized Operations ---

def vectorized_operations():
    """Show how vectorized operations replace loops."""
    data = np.array([4, 9, 16, 25, 36, 49, 64])

    # These operate on every element — no loop needed
    roots = np.sqrt(data)
    squared = data ** 2
    clipped = np.clip(data, 10, 50)  # Values below 10 → 10, above 50 → 50

    # Boolean indexing — filter without a loop
    large = data[data > 20]

    print("=== Vectorized Operations ===")
    print(f"Data:       {data}")
    print(f"Sqrt:       {roots}")
    print(f"Squared:    {squared}")
    print(f"Clipped:    {clipped}")
    print(f"Where > 20: {large}")
    print()

    return roots, squared, clipped, large


# --- 5. Statistical Summary ---

def statistical_summary(values):
    """Compute descriptive statistics for an array."""
    stats = {
        "count": len(values),
        "mean": float(np.mean(values)),
        "std": float(np.std(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "median": float(np.median(values)),
        "sum": float(np.sum(values)),
    }

    print("=== Statistical Summary ===")
    for key, val in stats.items():
        print(f"  {key:>7}: {val:.2f}")
    print()

    return stats


# --- Main ---

if __name__ == "__main__":
    grades, *_ = create_basic_arrays()
    indexing_demo()
    broadcasting_demo()
    vectorized_operations()
    statistical_summary(grades)
