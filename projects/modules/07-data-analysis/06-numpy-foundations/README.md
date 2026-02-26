# Module 07 / Project 06 — NumPy Foundations

[README](../../../../README.md) · [Module Index](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- Creating arrays with `np.array()`, `np.zeros()`, `np.arange()`, `np.linspace()`
- Indexing and slicing: 1D and 2D arrays
- Broadcasting: adding a scalar to an array, combining arrays of different shapes
- Vectorized operations: element-wise math without loops
- Basic statistics: `mean()`, `std()`, `sum()`, `min()`, `max()` along axes

## Why this project exists

NumPy is the foundation of Python's data science ecosystem. Pandas, matplotlib, scikit-learn, and TensorFlow all build on NumPy arrays. Understanding how arrays work — especially broadcasting and vectorized operations — is essential before moving to any data science library. This project teaches you to think in arrays instead of loops, which is both faster and more readable.

## Prerequisites

- Module 07 Projects 01-05 (pandas basics through analysis reports)
- Comfortable with lists, loops, and functions

## Run

```bash
cd projects/modules/07-data-analysis/06-numpy-foundations
pip install -r requirements.txt
python project.py
```

## Tests

```bash
pytest tests/
```

## Alter it

- Create a 3D array and practice slicing along each axis
- Use `np.where()` to replace values conditionally
- Try `np.concatenate()` and `np.stack()` to combine arrays

## Break it

- What happens when you broadcast arrays of incompatible shapes?
- What if you index past the end of an array?
- What happens with integer overflow in NumPy vs plain Python?

## Explain it

- Why are vectorized operations faster than Python loops?
- What does "broadcasting" mean and when does it work?
- When would you use `np.linspace()` vs `np.arange()`?
