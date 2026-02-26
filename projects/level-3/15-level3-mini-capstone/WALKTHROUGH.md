# Level 3 Mini Capstone: Project Health Dashboard — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This capstone combines every Level 3 skill into one tool, so spend at least 30 minutes attempting it independently.

## Thinking Process

This capstone builds a tool that real developers actually use: a project health checker. It scans a directory, collects metrics about the code (file sizes, function counts, structural issues), and produces a scored report. The idea is that you can run this against any Python project and get a quick summary of its quality.

Break the problem into layers. The bottom layer is **file analysis** -- reading individual `.py` files and counting lines, functions, and classes. The middle layer is **health checks** -- rules that flag potential problems (files too large, missing README, no tests). The top layer is **scoring and reporting** -- turning issues into a numerical score and a human-readable report.

Each layer uses dataclasses to pass structured data up to the next layer. `FileMetrics` flows into `DirectoryMetrics`, health check functions produce `HealthIssue` instances, and everything feeds into a `HealthReport`. This is the Level 3 pattern at its best: typed data models flowing through composable functions.

## Step 1: Define the Data Models

**What to do:** Create dataclasses for `FileMetrics`, `DirectoryMetrics`, `HealthIssue`, and `HealthReport`.

**Why:** Having four distinct data models might seem like overkill for a small project, but it pays off immediately. Each function knows exactly what it receives and produces. There is no ambiguity about what `metrics["lines"]` means -- it is `metrics.lines` on a typed dataclass.

```python
@dataclass
class FileMetrics:
    name: str
    path: str
    lines: int
    blank_lines: int
    comment_lines: int
    code_lines: int
    functions: int
    classes: int

@dataclass
class HealthIssue:
    severity: str  # "error", "warning", "info"
    category: str
    message: str
    file: str = ""

@dataclass
class HealthReport:
    project_path: str
    metrics: DirectoryMetrics
    issues: list[HealthIssue] = field(default_factory=list)
    score: int = 100
    grade: str = "A"
```

**Predict:** Why does `HealthReport` start with `score: int = 100` instead of 0? What does this tell you about the scoring approach?

## Step 2: Analyse a Single Python File

**What to do:** Write a function that reads a `.py` file and counts total lines, blank lines, comment lines, code lines, function definitions, and class definitions.

**Why:** This is the foundation of all metrics. By analyzing one file at a time, you keep the function simple and testable. Directory analysis just calls this function for each file.

```python
def analyse_python_file(path: Path) -> FileMetrics:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    blank = sum(1 for l in lines if not l.strip())
    comments = sum(1 for l in lines if l.strip().startswith("#"))
    code = len(lines) - blank - comments

    functions = sum(1 for l in lines if l.strip().startswith("def "))
    classes = sum(1 for l in lines if l.strip().startswith("class "))

    return FileMetrics(
        name=path.name, path=str(path),
        lines=len(lines), blank_lines=blank,
        comment_lines=comments, code_lines=code,
        functions=functions, classes=classes,
    )
```

**Predict:** This counts `code_lines` as `total - blank - comments`. Is a docstring (a triple-quoted string) counted as code or something else? Is that correct?

## Step 3: Analyse a Directory

**What to do:** Write a function that scans all matching files in a directory using `rglob()` and aggregates their metrics.

**Why:** `rglob()` recursively finds files matching a pattern, which means nested packages are included automatically. The function wraps each file analysis in a `try/except` so one bad file does not crash the entire scan.

```python
def analyse_directory(root: Path, pattern: str = "*.py") -> DirectoryMetrics:
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    files = []
    for path in sorted(root.rglob(pattern)):
        if path.is_file():
            try:
                metrics = analyse_python_file(path)
                files.append(metrics)
            except Exception as exc:
                logger.warning("Could not analyse %s: %s", path, exc)

    total_lines = sum(f.lines for f in files)
    return DirectoryMetrics(
        name=root.name,
        total_files=len(files),
        total_lines=total_lines,
        total_code_lines=sum(f.code_lines for f in files),
        total_functions=sum(f.functions for f in files),
        total_classes=sum(f.classes for f in files),
        avg_file_size=round(total_lines / len(files), 1) if files else 0,
        files=files,
    )
```

**Predict:** What happens if the directory has `.pyc` files or binary files? Would `read_text()` crash on them? How does the `rglob("*.py")` pattern protect against this?

## Step 4: Implement Health Checks

**What to do:** Write several small check functions, each returning a list of `HealthIssue` instances for a specific concern.

**Why:** Each check is independent and composable. You can add new checks without modifying existing ones, and you can enable or disable checks per project. This is the same pattern linting tools like `ruff` and `pylint` use.

```python
def check_large_files(files, max_lines=300):
    return [
        HealthIssue("warning", "size",
                     f"{f.name} has {f.lines} lines (limit: {max_lines})", f.name)
        for f in files if f.lines > max_lines
    ]

def check_missing_readme(root):
    for name in ["README.md", "README.txt", "README.rst", "readme.md"]:
        if (root / name).exists():
            return []
    return [HealthIssue("warning", "documentation", "No README file found")]

def check_missing_tests(root):
    test_files = list(root.rglob("test_*.py")) + list(root.rglob("*_test.py"))
    if not test_files:
        return [HealthIssue("warning", "testing", "No test files found")]
    return []
```

**Predict:** Each check returns a list. Why a list instead of a single issue or None? (Hint: what if `check_large_files` finds three files over the limit?)

## Step 5: Calculate the Health Score

**What to do:** Write a function that converts a list of issues into a numerical score (0-100) and a letter grade.

**Why:** A single number makes it easy to track health over time and to set thresholds ("fail the build if score drops below 70").

```python
def calculate_score(issues):
    score = 100
    for issue in issues:
        if issue.severity == "error":
            score -= 20
        elif issue.severity == "warning":
            score -= 10
        elif issue.severity == "info":
            score -= 2

    score = max(0, min(100, score))

    if score >= 90: grade = "A"
    elif score >= 80: grade = "B"
    elif score >= 70: grade = "C"
    elif score >= 60: grade = "D"
    else: grade = "F"

    return score, grade
```

**Predict:** If a project has 2 errors and 3 warnings, what is its score and grade? What about 6 warnings?

## Step 6: Assemble the Report

**What to do:** Write `generate_report()` to orchestrate everything: scan the directory, run all health checks, calculate the score, and return a `HealthReport`.

**Why:** This is the same pipeline pattern from the Level 2 capstone, but now with typed dataclasses instead of plain dicts. Each step produces a clean output that feeds into the next.

```python
def generate_report(root: Path) -> HealthReport:
    metrics = analyse_directory(root)

    issues = []
    issues.extend(check_large_files(metrics.files))
    issues.extend(check_missing_readme(root))
    issues.extend(check_missing_tests(root))
    issues.extend(check_long_functions(metrics.files))

    score, grade = calculate_score(issues)

    return HealthReport(
        project_path=str(root),
        metrics=metrics,
        issues=issues,
        score=score,
        grade=grade,
    )
```

**Predict:** Why does this function use `issues.extend(...)` instead of `issues.append(...)`? What would go wrong with `append`?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Using `append` instead of `extend` for issue lists | Each check returns a list; append would nest lists | `extend` adds each item; `append` adds the list itself |
| Division by zero in `avg_file_size` | Empty directory has no files | Guard with `if files else 0` |
| Not catching file read errors | Binary files or permission issues | Wrap `analyse_python_file` in `try/except` |
| Mutable default in dataclass | `list` as default value is shared | Always use `field(default_factory=list)` |

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
python project.py report .
python project.py report . --json
python project.py scan . --pattern "*.py"
```

## What You Learned

- **Composable health checks** (small functions that return lists of issues) are the same pattern used by real linters and CI tools. Each check is independent, testable, and can be added or removed without affecting others.
- **Dataclasses as data flow containers** replace the plain dicts from Level 2. They provide type safety, auto-generated methods, and better IDE support.
- **Scored reporting** turns qualitative observations ("there are some big files") into a quantitative metric (score: 70/100, grade: C) that can be tracked and automated.
