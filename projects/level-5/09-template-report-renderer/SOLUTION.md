# Template Report Renderer — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 5 / Project 09 — Template Report Renderer.

Renders reports from simple templates with data binding.
Uses a custom mini-template engine with {{variable}} placeholders,
{{#each items}} loops, and {{#if condition}} blocks.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- template rendering helpers ----------

# WHY process in this specific order (if -> each -> variables)? --
# IF blocks must resolve first so falsy sections are removed before
# EACH expansion. EACH blocks go next because they may introduce new
# placeholders. Variables go last to substitute everything remaining.


def render_variables(template: str, data: dict) -> str:
    """Replace {{key}} placeholders with values from *data*."""
    def replacer(match: re.Match) -> str:
        key = match.group(1).strip()
        # WHY: Support dotted paths like {{config.max_retries}} so
        # nested data structures can be referenced without flattening.
        value = resolve_dotted_key(key, data)
        if value is None:
            # WHY: Show {{MISSING:key}} instead of silently swallowing
            # the placeholder. This makes missing data visible in output.
            logging.warning("Missing template variable: '%s'", key)
            return f"{{{{MISSING:{key}}}}}"
        return str(value)

    # WHY: The regex matches {{word}} and {{word.word}} patterns.
    # \w+ matches one or more word characters; (?:\.\w+)* allows
    # optional dot-separated segments for nested keys.
    return re.sub(r"\{\{(\w+(?:\.\w+)*)\}\}", replacer, template)


def resolve_dotted_key(key: str, data: dict) -> object | None:
    """Resolve a dotted key path like 'config.timeout' against nested dicts."""
    parts = key.split(".")
    current: object = data
    for part in parts:
        # WHY: Check isinstance(dict) at each level so we do not crash
        # if a middle segment resolves to a non-dict value.
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def render_each_blocks(template: str, data: dict) -> str:
    """Process {{#each items}}...{{/each}} blocks."""
    # WHY: re.DOTALL makes . match newlines so multi-line blocks work.
    # (.*?) is non-greedy to match the closest {{/each}} tag.
    pattern = r"\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}"

    def replacer(match: re.Match) -> str:
        key = match.group(1)
        block = match.group(2)
        items = data.get(key, [])

        # WHY: If the data is not a list, skip the block rather than
        # crashing. This handles misconfigured templates gracefully.
        if not isinstance(items, list):
            logging.warning("{{#each %s}} data is not a list — skipping block", key)
            return ""

        rendered_parts: list[str] = []
        for item in items:
            if isinstance(item, dict):
                # WHY: Dict items can use their own keys as placeholders
                # inside the block, e.g., {{name}} for each employee.
                rendered_parts.append(render_variables(block, item))
            else:
                # WHY: Scalar items (strings, numbers) use {{this}} as
                # the placeholder, following Handlebars convention.
                rendered_parts.append(block.replace("{{this}}", str(item)))

        return "".join(rendered_parts)

    return re.sub(pattern, replacer, template, flags=re.DOTALL)


def is_truthy(value: object) -> bool:
    """Determine whether a template value is truthy.

    WHY: Python's default truthiness rules are mostly right, but template
    engines need to treat the string "false" as falsy (a common value in
    config files). This custom function handles that edge case.
    """
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.lower() not in ("", "false", "0", "no")
    if isinstance(value, list):
        return len(value) > 0
    return True


def render_if_blocks(template: str, data: dict) -> str:
    """Process {{#if key}}...{{/if}} conditional blocks."""
    pattern = r"\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}"

    def replacer(match: re.Match) -> str:
        key = match.group(1)
        block = match.group(2)
        value = data.get(key)
        # WHY: If truthy, render the block with variable substitution.
        # If falsy, return empty string to remove the entire block.
        if is_truthy(value):
            return render_variables(block, data)
        return ""

    return re.sub(pattern, replacer, template, flags=re.DOTALL)

# ---------- full render pipeline ----------

def render_template(template: str, data: dict) -> str:
    """Full render pipeline: if-blocks -> each-blocks -> variables.

    WHY this order? IF blocks first removes conditional sections.
    EACH blocks next expands loops (which may introduce new variables).
    Variables last substitutes all remaining placeholders.
    """
    result = render_if_blocks(template, data)
    result = render_each_blocks(result, data)
    result = render_variables(result, data)
    return result

# ---------- pipeline ----------

def run(template_path: Path, data_path: Path, output_path: Path) -> dict:
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    if not data_path.exists():
        raise FileNotFoundError(f"Data not found: {data_path}")

    template = template_path.read_text(encoding="utf-8")
    data = json.loads(data_path.read_text(encoding="utf-8"))

    rendered = render_template(template, data)
    line_count = len(rendered.splitlines())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    logging.info("Report rendered: %d lines written", line_count)

    return {
        "lines_written": line_count,
        "output_length": len(rendered),
        "template": str(template_path),
        "data_keys": list(data.keys()),
    }

# ---------- CLI ----------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render reports from templates with data")
    parser.add_argument("--template", default="data/report_template.txt")
    parser.add_argument("--data", default="data/report_data.json")
    parser.add_argument("--output", default="data/rendered_report.txt")
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.template), Path(args.data), Path(args.output))
    print(f"Report rendered: {report['lines_written']} lines written")

if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Processing order: if -> each -> variables | IF blocks must resolve first so that falsy sections are removed before EACH expands loops inside them. Variables go last because EACH blocks may introduce new placeholders (e.g., `{{name}}` inside a loop). |
| `{{MISSING:key}}` for undefined variables | Silently swallowing missing variables produces output that looks correct but is wrong. Making missing data visible ensures errors are caught during review. |
| Custom `is_truthy` function | Python's built-in truthiness treats `"false"` as `True` (non-empty string). Template engines commonly receive config strings like `"false"` and need to treat them as falsy. |
| Dotted key resolution | Nested data like `{"config": {"timeout": 30}}` is common in JSON. Supporting `{{config.timeout}}` avoids requiring the user to flatten their data before rendering. |

## Alternative Approaches

### Using Python's built-in `string.Template`

```python
from string import Template

template = Template("Hello, $name! You have $count items.")
rendered = template.safe_substitute(name="Alice", count=5)
```

`string.Template` is simple and built-in, but it only supports `$variable` substitution with no loops or conditionals. For reports that need iteration and conditional sections, a custom engine or Jinja2 is required.

### Using Jinja2

```python
from jinja2 import Template

template = Template("{% for item in items %}{{ item.name }}{% endfor %}")
rendered = template.render(items=[{"name": "Alice"}, {"name": "Bob"}])
```

Jinja2 is the production standard for Python templating. It supports inheritance, filters, macros, and auto-escaping. Building a mini-engine first helps you understand what Jinja2 does under the hood.

## Common Pitfalls

1. **Forgetting `re.DOTALL` for multi-line blocks** — Without `re.DOTALL`, the `.` in `(.*?)` does not match newlines, so multi-line `{{#each}}` or `{{#if}}` blocks fail silently by matching nothing.
2. **Greedy regex matching** — Using `(.*)` instead of `(.*?)` matches the first `{{#each}}` to the *last* `{{/each}}`, swallowing everything in between. Non-greedy `(.*?)` matches to the closest closing tag.
3. **Nested blocks of the same type** — The simple regex approach does not handle `{{#if a}}...{{#if b}}...{{/if}}...{{/if}}`. The inner `{{/if}}` matches the outer opening tag. Production template engines use recursive descent parsers to handle nesting.
