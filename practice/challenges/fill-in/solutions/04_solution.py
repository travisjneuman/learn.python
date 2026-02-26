"""Solution for Fill-In Challenge #4 — String Formatter."""


def left_pad(text, width, char=" "):
    if len(text) >= width:
        return text
    return char * (width - len(text)) + text


def format_table_row(columns, widths):
    parts = []
    for col, width in zip(columns, widths):
        parts.append(col.ljust(width))
    return " | ".join(parts)


def build_report(title, rows):
    lines = [f"=== {title} ==="]
    name_width = max((len(name) for name, _ in rows), default=4)
    name_width = max(name_width, 4)  # minimum "Name" header width
    score_width = 5

    lines.append(format_table_row(["Name", "Score"], [name_width, score_width]))
    lines.append("-" * name_width + "-+-" + "-" * score_width)

    for name, score in rows:
        lines.append(format_table_row([name, str(score)], [name_width, score_width]))

    return "\n".join(lines)


def truncate(text, max_length, suffix="..."):
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
