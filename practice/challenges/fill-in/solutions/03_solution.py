"""Solution for Fill-In Challenge #3 — File Reader."""


def parse_csv_line(line):
    return [field.strip() for field in line.split(",")]


def parse_key_value(text):
    result = {}
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        result[key] = value
    return result


def parse_table(lines):
    if not lines:
        return []
    headers = parse_csv_line(lines[0])
    rows = []
    for line in lines[1:]:
        values = parse_csv_line(line)
        rows.append(dict(zip(headers, values)))
    return rows
