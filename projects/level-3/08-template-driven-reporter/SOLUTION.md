# Template Driven Reporter — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Template Driven Reporter."""

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
    """Result of rendering a template.

    WHY: capturing metadata (which variables were used, which were
    missing) lets the caller validate templates and show diagnostics
    without re-parsing.
    """
    template_name: str
    output: str
    variables_used: list[str] = field(default_factory=list)
    missing_variables: list[str] = field(default_factory=list)
    success: bool = True


def discover_variables(template_text: str) -> list[str]:
    """Find all ${variable} or $variable references in a template.

    WHY: knowing which variables a template expects BEFORE rendering
    lets you validate the data context and warn about missing values
    instead of producing broken output.
    """
    # WHY: string.Template.pattern is the compiled regex that Template
    # uses internally. Reusing it guarantees we find exactly the same
    # variables that substitute() would look for.
    pattern = string.Template.pattern
    variables: list[str] = []

    for match in pattern.finditer(template_text):
        # WHY: Template supports two syntaxes: $name and ${name}.
        # The regex has separate groups for each — "named" and "braced".
        name = match.group("named") or match.group("braced")
        if name and name not in variables:
            variables.append(name)

    logger.debug("Discovered variables: %s", variables)
    return variables


def safe_render(template_text: str, context: dict) -> RenderResult:
    """Render a template with safe substitution.

    WHY: safe_substitute leaves missing variables as-is ($name)
    instead of raising KeyError. This is useful for previewing
    templates or handling optional fields.
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
    """Render a template with strict substitution.

    WHY: strict mode (substitute, not safe_substitute) catches
    missing variables immediately. Use this when ALL variables
    must be provided — like generating invoices or contracts.
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


def render_file(template_path: Path, context: dict,
                strict: bool = False) -> RenderResult:
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

    WHY: batch rendering is the core use case for templates —
    generating invoices, emails, or reports from a list of records.
    One template, many datasets.
    """
    results: list[RenderResult] = []
    for i, record in enumerate(records):
        result = safe_render(template_text, record)
        result.template_name = f"record_{i}"
        results.append(result)
    return results


def build_report_context(data: dict) -> dict:
    """Build a flat context dict from nested data.

    WHY: string.Template only supports flat $variable references,
    not dotted paths like $user.name. Flattening one level
    converts {"user": {"name": "X"}} to {"user_name": "X"} so
    the template can use $user_name.
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
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "render":
        data = json.loads(Path(args.data).read_text(encoding="utf-8"))
        # WHY: auto-flatten nested data only when nesting is detected.
        context = (build_report_context(data)
                   if any(isinstance(v, dict) for v in data.values())
                   else data)
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| `string.Template` instead of f-strings | f-strings execute arbitrary Python code inside `{}`, making them dangerous with untrusted input. `string.Template` only does variable substitution — safe for user-provided templates. |
| Two render modes: safe and strict | `safe_substitute` is forgiving (good for previews), `substitute` is strict (good for production output). Different use cases need different trade-offs. |
| `discover_variables` as a standalone function | Pre-flight validation: check which variables a template needs before attempting to render. Prevents surprises at render time. |
| Flattening nested data to one level | `string.Template` cannot handle `$user.name` syntax. Flattening is the simplest bridge between nested JSON and flat template variables. |
| `RenderResult` with metadata | Tracking which variables were used vs missing lets the caller generate diagnostics without re-parsing the template. |

## Alternative Approaches

### Using Jinja2 for templates

```python
from jinja2 import Environment, BaseLoader

env = Environment(loader=BaseLoader())
template = env.from_string("Hello {{ user.name }}, you have {{ count }} items.")
output = template.render(user={"name": "Alice"}, count=5)
```

**Trade-off:** Jinja2 supports conditionals, loops, filters, and nested access — far more powerful than `string.Template`. But it is a third-party dependency and introduces a full template language. `string.Template` is in the standard library and covers the 80% case (simple variable substitution) with zero dependencies.

## Common Pitfalls

1. **Confusing `substitute` and `safe_substitute`** — `substitute` raises `KeyError` on missing variables; `safe_substitute` leaves them as `$variable` in the output. Using the wrong one either crashes your program or silently produces incomplete output.

2. **Dollar signs in template text** — A literal `$` in the template (e.g., "Price: $50") confuses the parser. Use `$$` to escape a literal dollar sign: `"Price: $$50"` renders as `"Price: $50"`.

3. **Nested data without flattening** — Passing `{"user": {"name": "Alice"}}` directly to Template and using `$user` renders as the string representation of the dict: `"{'name': 'Alice'}"`. Always flatten or use a template engine that supports nested access.
