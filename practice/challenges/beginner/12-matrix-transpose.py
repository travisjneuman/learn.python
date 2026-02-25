"""
Challenge: Matrix Transpose
Difficulty: Beginner
Concepts: nested lists, 2D indexing, list comprehension
Time: 20 minutes

Transpose a 2D matrix (list of lists). Rows become columns and columns become rows.
The input matrix will always be rectangular (all rows have the same length).

Examples:
    >>> transpose([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]
    >>> transpose([[1]])
    [[1]]
"""


def transpose(matrix: list[list]) -> list[list]:
    """Transpose a 2D matrix. Implement this function."""
    # Hint: The element at row i, column j moves to row j, column i.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: 2x3 matrix
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]], "2x3 matrix failed"
    # Test 2: 3x2 matrix
    assert transpose([[1, 4], [2, 5], [3, 6]]) == [[1, 2, 3], [4, 5, 6]], "3x2 matrix failed"
    # Test 3: 1x1 matrix
    assert transpose([[1]]) == [[1]], "1x1 matrix failed"
    # Test 4: Square matrix
    assert transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]], "Square matrix failed"
    # Test 5: Single row
    assert transpose([[1, 2, 3]]) == [[1], [2], [3]], "Single row failed"
    print("All tests passed!")
