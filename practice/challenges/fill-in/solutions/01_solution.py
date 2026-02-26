"""Solution for Fill-In Challenge #1 — List Filtering."""


def filter_positive(numbers):
    return [n for n in numbers if n > 0]


def filter_long_words(words, min_length):
    return [w for w in words if len(w) >= min_length]


def filter_by_key(records, key, value):
    return [r for r in records if r[key] == value]


def unique_sorted(items):
    return sorted(set(items))
