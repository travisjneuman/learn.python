"""
Solution: Batch Processor

Approach: The batch generator collects items into a temporary list. When
the list reaches the batch size, yield it and start a new batch. After
the loop, yield any remaining items. process_batches chains batch() with
func and flattens the results.
"""


def batch(iterable, size: int):
    """Yield successive batches of items from the iterable."""
    current_batch = []
    for item in iterable:
        current_batch.append(item)
        if len(current_batch) == size:
            yield current_batch
            current_batch = []
    # Yield the final partial batch if non-empty
    if current_batch:
        yield current_batch


def process_batches(items: list, size: int, func) -> list:
    """Apply func to each batch and flatten the results."""
    result = []
    for b in batch(items, size):
        result.extend(func(b))
    return result


if __name__ == "__main__":
    assert list(batch([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]
    assert list(batch([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(batch([1, 2], 5)) == [[1, 2]]
    assert list(batch([], 3)) == []

    gen = batch([1, 2, 3], 2)
    assert hasattr(gen, "__next__")

    result = process_batches([1, 2, 3, 4], 2, lambda b: [x * 2 for x in b])
    assert result == [2, 4, 6, 8]

    result = process_batches(["a", "b", "c"], 2, lambda b: [s.upper() for s in b])
    assert result == ["A", "B", "C"]

    assert list(batch([1, 2, 3], 1)) == [[1], [2], [3]]

    print("All tests passed!")
