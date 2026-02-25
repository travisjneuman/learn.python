"""Level 3 project: Template Driven Reporter.

Renders reports from string templates and data contexts,
similar to how Jinja2 works but using Python's string.Template.

Skills practiced: string.Template, dataclasses, typing basics,
logging, file I/O, separation of data and presentation.
"""

from __future__ import annotations

import argparse
import json
import logging
import string
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class TemplateVar:
    """A variable expected by a template."""
    name: str
    required: bool = True
    default: str = ""


@dataclass
class RenderResult:
    """Result of rendering a template."""
    template_name: str
    output: str
    variables_used: list[str] = field(default_factory=list)
    missing_variables: list[str] = field(default_factory=list)
    success: bool = True


def discover_variables(template_text: str) -> list[str]:
    """Find all ${variable} or $variable references in a template.

    Uses string.Template's pattern to extract variable names.
    """
    pattern = string.Template.pattern
    variables: list[str] = []

    for match in pattern.finditer(template_text):
        # The named group captures ${name}, braced captures $name.
        name = match.group("named") or match.group("braced")
        if name and name not in variables:
            variables.append(name)

    logger.debug("Discovered variables: %s", variables)
    return variables


def safe_render(template_text: str, context: dict) -> RenderResult:
    """Render a template with safe substitution (missing vars stay as-is).

    Returns a RenderResult with metadata about what happened.
    """
    expected = discover_variables(template_text)
    missing = [v for v in expected if v not in context]

    tmpl = string.Template(template_text)
    output = tmpl.safe_substitute(context)

    return RenderResult(
        template_name="inline",
        output=output,
        variables_used=[v for v in expected if v in context],
        missing_variables=missing,
        success=len(missing) == 0,
    )


def strict_render(template_text: str, context: dict) -> RenderResult:
    """Render a template with strict substitution (missing vars raise).

    Catches the error and returns it in the result.
    """
    expected = discover_variables(template_text)
    tmpl = string.Template(template_text)

    try:
        output = tmpl.substitute(context)
        return RenderResult(
            template_name="inline",
            output=output,
            variables_used=expected,
            success=True,
        )
    except (KeyError, ValueError) as exc:
        missing = [v for v in expected if v not in context]
        return RenderResult(
            template_name="inline",
            output="",
            variables_used=[v for v in expected if v in context],
            missing_variables=missing,
            success=False,
        )


def render_file(template_path: Path, context: dict, strict: bool = False) -> RenderResult:
    """Load a template from a file and render it."""
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    text = template_path.read_text(encoding="utf-8")
    render_fn = strict_render if strict else safe_render
    result = render_fn(text, context)
    result.template_name = template_path.name
    return result


def render_batch(
    template_text: str,
    records: list[dict],
    separator: str = "\n---\n",
) -> list[RenderResult]:
    """Render one template for each record in a list.

    Useful for generating bulk reports (invoices, emails, etc.).
    """
    results: list[RenderResult] = []
    for i, record in enumerate(records):
        result = safe_render(template_text, record)
        result.template_name = f"record_{i}"
        results.append(result)
    return results


def build_report_context(data: dict) -> dict:
    """Build a flat context dict from nested data.

    Flattens one level: {"user": {"name": "X"}} -> {"user_name": "X"}
    """
    flat: dict = {}
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                flat[f"{key}_{sub_key}"] = sub_value
        else:
            flat[key] = value
    return flat


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(description="Template-driven reporter")

    sub = parser.add_subparsers(dest="command")

    render = sub.add_parser("render", help="Render a template with data")
    render.add_argument("template", help="Path to template file")
    render.add_argument("data", help="Path to JSON data file")
    render.add_argument("--strict", action="store_true", help="Strict mode")

    discover = sub.add_parser("discover", help="List variables in a template")
    discover.add_argument("template", help="Path to template file")

    batch = sub.add_parser("batch", help="Render template for each record")
    batch.add_argument("template", help="Path to template file")
    batch.add_argument("data", help="Path to JSON array of records")

    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    """Entry point."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "render":
        data = json.loads(Path(args.data).read_text(encoding="utf-8"))
        context = build_report_context(data) if any(isinstance(v, dict) for v in data.values()) else data
        result = render_file(Path(args.template), context, strict=args.strict)
        print(result.output)
        if result.missing_variables:
            logger.warning("Missing variables: %s", result.missing_variables)

    elif args.command == "discover":
        text = Path(args.template).read_text(encoding="utf-8")
        variables = discover_variables(text)
        for var in variables:
            print(f"  ${var}")

    elif args.command == "batch":
        template_text = Path(args.template).read_text(encoding="utf-8")
        records = json.loads(Path(args.data).read_text(encoding="utf-8"))
        results = render_batch(template_text, records)
        for result in results:
            print(result.output)
            print("---")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
