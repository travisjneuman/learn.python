# Template Driven Reporter — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 20 minutes attempting it independently.

## Thinking Process

This project solves a common real-world problem: you have data (JSON) and a template (text with placeholders), and you need to combine them to produce a report. Think of it like mail merge -- the same letter template gets filled in with different customer names and addresses.

The key design question is: what happens when a placeholder in the template has no matching data? You have two options. **Safe mode** leaves the placeholder as-is (the report shows `$company_name` literally). **Strict mode** raises an error because something is missing. Both are useful in different contexts -- safe mode for drafts, strict mode for production.

Before coding, think about the data flow: the template file contains `$variable` placeholders, the data file contains the values, and your code combines them. But what if the data is nested (e.g., `{"company": {"name": "Acme"}}`)? The template engine expects flat keys like `$company_name`, so you need a flattening step. This separation of concerns -- loading, flattening, rendering -- keeps each piece simple.

## Step 1: Discover Variables in a Template

**What to do:** Write a function that finds all `$variable` and `${variable}` placeholders in a template string.

**Why:** Before rendering, you need to know what the template expects. This lets you validate that the data provides everything, and it lets users inspect a template without rendering it.

```python
import string

def discover_variables(template_text: str) -> list[str]:
    pattern = string.Template.pattern
    variables = []

    for match in pattern.finditer(template_text):
        name = match.group("named") or match.group("braced")
        if name and name not in variables:
            variables.append(name)

    return variables
```

`string.Template.pattern` is a compiled regex that Python uses internally to find `$variable` and `${variable}` patterns. By reusing it, you get exactly the same matching behavior as the Template class itself.

**Predict:** What is the difference between `$variable` and `${variable}` in a template? When would you need the braced form? (Hint: what happens with `$variable_name` vs `${variable}_name`?)

## Step 2: Render with Safe Substitution

**What to do:** Write a `safe_render()` function that fills in placeholders but leaves missing ones intact, and returns metadata about what happened.

**Why:** Safe mode is forgiving -- it produces output even with incomplete data. The `RenderResult` dataclass tracks which variables were used and which were missing, so the caller can decide what to do about gaps.

```python
@dataclass
class RenderResult:
    template_name: str
    output: str
    variables_used: list[str] = field(default_factory=list)
    missing_variables: list[str] = field(default_factory=list)
    success: bool = True

def safe_render(template_text: str, context: dict) -> RenderResult:
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
```

**Predict:** If a template contains `Hello $name, your order $order_id is ready` and the context only has `{"name": "Alice"}`, what does the output look like? What does `missing_variables` contain?

## Step 3: Render with Strict Substitution

**What to do:** Write a `strict_render()` function that raises an error when any variable is missing.

**Why:** In production, you want to know immediately if data is incomplete rather than sending out a report with raw `$variable` placeholders. Strict mode catches these problems.

```python
def strict_render(template_text: str, context: dict) -> RenderResult:
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
    except (KeyError, ValueError):
        missing = [v for v in expected if v not in context]
        return RenderResult(
            template_name="inline",
            output="",
            variables_used=[v for v in expected if v in context],
            missing_variables=missing,
            success=False,
        )
```

The difference is `tmpl.substitute()` vs `tmpl.safe_substitute()`. The first raises `KeyError` on missing variables; the second quietly skips them.

**Predict:** Why does the function catch the error and return a `RenderResult` with `success=False` instead of letting the `KeyError` propagate? Think about what the caller needs.

## Step 4: Flatten Nested Data

**What to do:** Write a `build_report_context()` function that converts nested dicts into flat keys: `{"user": {"name": "Alice"}}` becomes `{"user_name": "Alice"}`.

**Why:** `string.Template` only supports flat key-value pairs -- it cannot handle `$user.name` or `$user[name]`. Flattening nested data with underscore-joined keys bridges this gap.

```python
def build_report_context(data: dict) -> dict:
    flat = {}
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                flat[f"{key}_{sub_key}"] = sub_value
        else:
            flat[key] = value
    return flat
```

**Predict:** This function flattens one level of nesting. What happens if the data has two levels, like `{"company": {"address": {"city": "NYC"}}}`? What would you need to change?

## Step 5: Batch Rendering

**What to do:** Write a `render_batch()` function that renders the same template for each record in a list.

**Why:** This is the mail-merge use case: one invoice template, many customers. Each record becomes its own rendered output.

```python
def render_batch(template_text, records, separator="\n---\n"):
    results = []
    for i, record in enumerate(records):
        result = safe_render(template_text, record)
        result.template_name = f"record_{i}"
        results.append(result)
    return results
```

**Predict:** If one record is missing a variable but others are not, does the entire batch fail? How does safe mode handle this differently than strict mode would?

## Step 6: Wire Up the CLI with Subcommands

**What to do:** Build a CLI with three subcommands: `render` (single template + data), `discover` (list variables), and `batch` (template + array of records).

**Why:** Each subcommand serves a different workflow. `discover` is for inspecting templates. `render` is for single reports. `batch` is for bulk generation.

```python
def main():
    if args.command == "render":
        data = json.loads(Path(args.data).read_text(encoding="utf-8"))
        context = build_report_context(data) if any(isinstance(v, dict) for v in data.values()) else data
        result = render_file(Path(args.template), context, strict=args.strict)
        print(result.output)

    elif args.command == "discover":
        text = Path(args.template).read_text(encoding="utf-8")
        for var in discover_variables(text):
            print(f"  ${var}")

    elif args.command == "batch":
        template_text = Path(args.template).read_text(encoding="utf-8")
        records = json.loads(Path(args.data).read_text(encoding="utf-8"))
        for result in render_batch(template_text, records):
            print(result.output)
            print("---")
```

**Predict:** Why does the `render` command check `if any(isinstance(v, dict) for v in data.values())`? What would happen if it always flattened?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Using f-strings instead of `string.Template` | F-strings are more familiar | Templates separate data from presentation; f-strings mix them |
| Forgetting to flatten nested data | Template expects `$company_name` but data has `{"company": {"name": ...}}` | Call `build_report_context()` when data has nested dicts |
| Not handling `$$` escape | `$$` is how Template represents a literal dollar sign | This is built-in behavior; just be aware of it |
| Using `substitute` when you want `safe_substitute` | Both look similar | `substitute` raises on missing vars; `safe_substitute` leaves them |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
12 passed
```

Test from the command line:

```bash
python project.py render report_template.txt report_data.json
python project.py discover report_template.txt
python project.py batch invoice_template.txt customers.json
```

## What You Learned

- **`string.Template`** provides safe text rendering with `$variable` placeholders. Unlike f-strings, the template and data are kept separate, which is essential for user-editable templates.
- **`safe_substitute` vs `substitute`** is a fundamental design choice: graceful degradation vs fail-fast. Pick based on whether incomplete output is acceptable.
- **Separating data from presentation** (the template pattern) appears everywhere: email templates, report generators, web frameworks (Jinja2), and configuration file rendering.
