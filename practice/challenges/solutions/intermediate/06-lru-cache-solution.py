"""
Solution: LRU Cache

Approach: Use collections.OrderedDict which maintains insertion order and
supports move_to_end in O(1). On get, move the key to the end (most recent).
On put, add/update the key at the end. If over capacity, pop the first item
(least recently used). This achieves O(1) for both operations.
"""

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        # Move to end to mark as most recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value) -> None:
        if key in self.cache:
            # Update existing key and move to end
            self.cache.move_to_end(key)
            self.cache[key] = value
        else:
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                # Evict the least recently used (first item)
                self.cache.popitem(last=False)


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    assert cache.get(1) == "a"
    assert cache.get(2) == "b"

    cache.put(3, "c")
    assert cache.get(1) == -1
    assert cache.get(3) == "c"

    cache2 = LRUCache(2)
    cache2.put(1, "a")
    cache2.put(2, "b")
    cache2.get(1)
    cache2.put(3, "c")
    assert cache2.get(2) == -1
    assert cache2.get(1) == "a"

    cache3 = LRUCache(2)
    cache3.put(1, "a")
    cache3.put(1, "b")
    assert cache3.get(1) == "b"

    cache4 = LRUCache(1)
    cache4.put(1, "a")
    cache4.put(2, "b")
    assert cache4.get(1) == -1
    assert cache4.get(2) == "b"

    print("All tests passed!")
