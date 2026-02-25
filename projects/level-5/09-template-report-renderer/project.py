"""Level 5 / Project 09 — Template Report Renderer.

Renders reports from simple templates with data binding.
Uses a custom mini-template engine with {{variable}} placeholders,
{{#each items}} loops, and {{#if condition}} blocks.

Concepts practiced:
- Regular expression matching and substitution
- Recursive template rendering for nested structures
- Truthiness evaluation for conditional blocks
- Structured report generation from templates
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path


# ---------- logging ----------

def configure_logging() -> None:
    """Set up logging so rendering progress is traceable."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


# ---------- template rendering helpers ----------

# The rendering pipeline processes blocks in order:
#   1. {{#if key}} conditional blocks (removed if falsy)
#   2. {{#each items}} loop blocks (expanded for each item)
#   3. {{variable}} simple substitution (leftover placeholders)


def render_variables(template: str, data: dict) -> str:
    """Replace ``{{key}}`` placeholders with values from *data*.

    Missing keys are replaced with ``{{MISSING:key}}`` so the output
    clearly shows which data was expected but not provided.
    """
    def replacer(match: re.Match) -> str:
        key = match.group(1).strip()
        # Support dotted paths like {{config.max_retries}}
        value = resolve_dotted_key(key, data)
        if value is None:
            logging.warning("Missing template variable: '%s'", key)
            return f"{{{{MISSING:{key}}}}}"
        return str(value)

    return re.sub(r"\{\{(\w+(?:\.\w+)*)\}\}", replacer, template)


def resolve_dotted_key(key: str, data: dict) -> object | None:
    """Resolve a dotted key path like 'config.timeout' against nested dicts.

    Returns None if any segment of the path is missing.
    """
    parts = key.split(".")
    current: object = data
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def render_each_blocks(template: str, data: dict) -> str:
    """Process ``{{#each items}}...{{/each}}`` blocks.

    Each loop iteration substitutes item fields into the block body.
    For non-dict items (strings, numbers) use ``{{this}}`` inside the
    block to reference the item value.
    """
    pattern = r"\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}"

    def replacer(match: re.Match) -> str:
        key = match.group(1)
        block = match.group(2)
        items = data.get(key, [])

        if not isinstance(items, list):
            logging.warning("{{#each %s}} data is not a list — skipping block", key)
            return ""

        rendered_parts: list[str] = []
        for item in items:
            if isinstance(item, dict):
                rendered_parts.append(render_variables(block, item))
            else:
                # Scalar items: replace {{this}} with the string value.
                rendered_parts.append(block.replace("{{this}}", str(item)))

        return "".join(rendered_parts)

    return re.sub(pattern, replacer, template, flags=re.DOTALL)


def is_truthy(value: object) -> bool:
    """Determine whether a template value is truthy.

    Falsy values: None, False, 0, empty string, empty list, "false".
    Everything else is truthy.
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
    """Process ``{{#if key}}...{{/if}}`` conditional blocks.

    If the key's value is truthy the block content is rendered;
    otherwise the entire block (including delimiters) is removed.
    """
    pattern = r"\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}"

    def replacer(match: re.Match) -> str:
        key = match.group(1)
        block = match.group(2)
        value = data.get(key)
        if is_truthy(value):
            return render_variables(block, data)
        return ""

    return re.sub(pattern, replacer, template, flags=re.DOTALL)


# ---------- full render pipeline ----------


def render_template(template: str, data: dict) -> str:
    """Full render pipeline: if-blocks -> each-blocks -> variables.

    Processing order matters:
    - IF blocks are resolved first so that falsy sections are removed
      before EACH expansion.
    - EACH blocks are expanded next, generating repeated sections.
    - Finally, remaining {{variable}} placeholders are substituted.
    """
    result = render_if_blocks(template, data)
    result = render_each_blocks(result, data)
    result = render_variables(result, data)
    return result


# ---------- pipeline ----------


def run(template_path: Path, data_path: Path, output_path: Path) -> dict:
    """Load template and data, render, and write the report."""
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
    """Parse command-line arguments for the report renderer."""
    parser = argparse.ArgumentParser(
        description="Render reports from templates with data",
    )
    parser.add_argument("--template", default="data/report_template.txt", help="Template file")
    parser.add_argument("--data", default="data/report_data.json", help="Data JSON file")
    parser.add_argument("--output", default="data/rendered_report.txt", help="Output path")
    return parser.parse_args()


def main() -> None:
    """Entry point: configure logging, parse args, render the report."""
    configure_logging()
    args = parse_args()
    report = run(Path(args.template), Path(args.data), Path(args.output))
    print(f"Report rendered: {report['lines_written']} lines written")


if __name__ == "__main__":
    main()
