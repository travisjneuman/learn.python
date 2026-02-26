# Solution: Level 0 / Project 09 - Daily Checklist Writer

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: Daily Checklist Writer.

Enter tasks interactively, format them as a numbered checklist,
and optionally save to a file.

Concepts: writing files, string formatting, lists, loops, open().
"""


def format_checklist(title: str, tasks: list) -> str:
    """Format tasks into a printable checklist with checkboxes.

    WHY number the tasks? -- Numbering makes it easy to refer to
    a specific task ('have you done item 3?') and gives the learner
    a sense of progress as they work through the list.
    """
    # WHY check for empty tasks: An empty checklist should show a clear
    # message instead of just a title with nothing under it.  The user
    # needs to know the list is empty, not that something broke.
    if not tasks:
        return f"{title}\n(no tasks)"

    lines = [title, "=" * len(title), ""]

    # WHY enumerate with start=1: Humans count from 1.  "Task 0" would
    # confuse a non-programmer.
    for i, task in enumerate(tasks, start=1):
        # WHY [ ] checkbox: This is a common plain-text convention used
        # in Markdown (GitHub issues, README files) and todo.txt.  The
        # square brackets create a visual checkbox that can be mentally
        # "checked off" as [x].
        lines.append(f"  {i}. [ ] {task}")

    lines.append("")
    lines.append(f"Total tasks: {len(tasks)}")
    # WHY "\n".join(): Building a list of lines and joining them is
    # cleaner than concatenating strings with +=.
    return "\n".join(lines)


def checklist_summary(tasks: list) -> dict:
    """Build a summary of the checklist.

    WHY track completed/remaining? -- Even though all tasks start as
    incomplete, the data structure is ready for future enhancement.
    A real checklist app would toggle items between completed and
    remaining.
    """
    return {
        "total_tasks": len(tasks),
        "tasks": tasks,
        "completed": 0,
        "remaining": len(tasks),
    }


if __name__ == "__main__":
    print("=== Daily Checklist Writer ===")
    title = input("Checklist title (or press Enter for 'Daily Checklist'): ")
    # WHY default title: If the user presses Enter without typing, we
    # use a sensible default.  This pattern avoids blank titles.
    if not title.strip():
        title = "Daily Checklist"

    print(f"\nEnter your tasks one at a time. Type 'done' when finished.\n")

    tasks = []
    while True:
        # WHY len(tasks) + 1: Shows the next task number as the user
        # types, giving immediate feedback about list position.
        task = input(f"  Task {len(tasks) + 1}: ")
        if task.strip().lower() == "done":
            break
        # WHY strip and check: We strip whitespace and only add non-empty
        # tasks.  This prevents blank items from cluttering the checklist.
        if task.strip():
            tasks.append(task.strip())

    checklist = format_checklist(title, tasks)
    print(f"\n{checklist}")

    # WHY ask to save: Not every user wants a file.  Asking first gives
    # control and teaches the pattern of conditional file writing.
    save = input("\nSave to file? (y/n): ").strip().lower()
    if save in ("y", "yes"):
        filename = input("File name (e.g. my_checklist.txt): ").strip()
        if not filename:
            filename = "checklist.txt"
        # WHY "w" mode: "w" (write) creates a new file or overwrites an
        # existing one.  For a checklist, we want a fresh file each time.
        #
        # WHY encoding="utf-8": Ensures the file can be read on any OS
        # without encoding issues.
        with open(filename, "w", encoding="utf-8") as f:
            f.write(checklist)
        print(f"Checklist saved to {filename}")
    else:
        print("Not saved. Goodbye!")
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `format_checklist()` returns a string instead of printing directly | Returning a string makes the function testable (assert on the result) and reusable (save to file, send as email, etc.) | Print inside the function — ties it to terminal output, cannot reuse for file writing |
| `[ ]` checkbox format | Standard plain-text convention used in Markdown, GitHub, and todo.txt. Universally recognised | `- [ ]` (Markdown style) — more specific to GitHub but less universal. `* ` bullet — no checkbox semantics |
| Title underline uses `"=" * len(title)` | The underline automatically matches the title width, looking professional regardless of title length | Hard-code a fixed-width underline — looks wrong when the title is shorter or longer |
| `checklist_summary()` includes `completed: 0` | The data structure is ready for a future enhancement where users can mark tasks complete. Designing for extensibility from the start | Omit it — simpler now but requires restructuring later |

## Alternative approaches

### Approach B: Writing directly to a file without interactive input

```python
def write_checklist_from_list(title: str, tasks: list, filepath: str) -> None:
    """Create a checklist file from a pre-built task list.

    Useful when tasks come from another source (a file, database, or API)
    rather than interactive input.
    """
    checklist = format_checklist(title, tasks)

    from pathlib import Path
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(checklist, encoding="utf-8")

# Usage:
# tasks = ["Review notes", "Complete exercise", "Read documentation"]
# write_checklist_from_list("Morning Tasks", tasks, "data/morning.txt")
```

**Trade-off:** This approach separates data collection from output generation. It works well when tasks come from a file or database rather than user input. The interactive version in the primary solution is better for learning because it practices `input()`, loops, and conditional logic. In a real application, you would likely have both: an interactive mode and a programmatic mode.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| User enters no tasks (types "done" immediately) | `format_checklist()` returns `"title\n(no tasks)"` — clear message, no crash | Already handled by the `if not tasks` check |
| User enters tasks with only whitespace | The `if task.strip()` check skips blank entries, so they never make it into the list | Already handled |
| User enters 100+ tasks | Numbering still works because `enumerate()` handles any count. But numbers might misalign if some are 2-digit and others 3-digit | For Level 0 this is fine. Could add right-justified numbering like the file reader project |
| File write fails (read-only directory, disk full) | `open()` raises `PermissionError` or `OSError`. The program crashes with a traceback | Wrap the file write in try/except and show a friendly error message |
| User enters a filename with path separators (e.g. `"../../../etc/hosts"`) | Python creates/overwrites the file at that path — potentially dangerous | Validate the filename: reject paths containing `/` or `\`, or write to a fixed directory |

## Key takeaways

1. **Writing files uses the same `with open(...)` pattern as reading, but with `"w"` mode.** `"w"` creates or overwrites, `"a"` appends, `"r"` reads. Always use `with` to ensure the file gets closed properly. This is the pattern for writing logs, reports, exports, and configs.
2. **Functions that return strings are more flexible than functions that print.** A returned string can be printed, saved to a file, sent over a network, or tested with assertions. A `print()` call does only one thing. This is why `format_checklist()` returns instead of printing.
3. **Default values prevent blank or broken output.** Giving the title a default ("Daily Checklist"), skipping blank tasks, and handling empty lists all make the program robust without complex error handling.
4. **`enumerate()` replaces manual counter variables.** Instead of `i = 1; for task in tasks: ...; i += 1`, you write `for i, task in enumerate(tasks, start=1)`. Fewer variables means fewer bugs. You will use `enumerate()` in almost every project.
