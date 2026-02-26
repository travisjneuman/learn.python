"""Solution for Fill-In Challenge #6 — Error Handler."""


def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def safe_key_access(data, *keys):
    current = data
    for key in keys:
        try:
            current = current[key]
        except (KeyError, TypeError):
            return None
    return current


def process_records(records):
    successes = []
    errors = []
    for record in records:
        name = record["name"]
        try:
            score = float(record["score"])
            successes.append({"name": name, "score": score})
        except (ValueError, TypeError) as e:
            errors.append({"name": name, "error": str(e)})
    return successes, errors
