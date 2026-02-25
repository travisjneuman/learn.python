"""
Solution: Matrix Transpose

Approach: Create a new matrix where the element at position [i][j] in the
original becomes [j][i] in the result. The result has as many rows as the
original has columns, and vice versa. Nested list comprehensions make this
concise.
"""


def transpose(matrix: list[list]) -> list[list]:
    if not matrix or not matrix[0]:
        return []

    rows = len(matrix)
    cols = len(matrix[0])

    # Build the transposed matrix: new row j contains column j from the original.
    result = []
    for j in range(cols):
        new_row = []
        for i in range(rows):
            new_row.append(matrix[i][j])
        result.append(new_row)
    return result


if __name__ == "__main__":
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transpose([[1, 4], [2, 5], [3, 6]]) == [[1, 2, 3], [4, 5, 6]]
    assert transpose([[1]]) == [[1]]
    assert transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
    assert transpose([[1, 2, 3]]) == [[1], [2], [3]]
    print("All tests passed!")
