"""Solution for Fill-In Challenge #2 — Dictionary Builder."""


def zip_to_dict(keys, values):
    if len(keys) != len(values):
        raise ValueError("keys and values must have the same length")
    return dict(zip(keys, values))


def invert_dict(d):
    return {v: k for k, v in d.items()}


def merge_dicts(dict_a, dict_b):
    result = dict(dict_a)
    result.update(dict_b)
    return result


def group_by(items, key_func):
    groups = {}
    for item in items:
        key = key_func(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups
