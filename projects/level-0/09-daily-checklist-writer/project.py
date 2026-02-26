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
    if not tasks:
        return f"{title}\n(no tasks)"

    lines = [title, "=" * len(title), ""]

    for i, task in enumerate(tasks, start=1):
        # [ ] is an unchecked checkbox -- a common plain-text convention.
        lines.append(f"  {i}. [ ] {task}")

    lines.append("")
    lines.append(f"Total tasks: {len(tasks)}")
    return "\n".join(lines)


def checklist_summary(tasks: list) -> dict:
    """Build a summary of the checklist."""
    return {
        "total_tasks": len(tasks),
        "tasks": tasks,
        "completed": 0,
        "remaining": len(tasks),
    }


# This guard means the code below only runs when you execute the file
# directly (python project.py), NOT when another file imports it.
if __name__ == "__main__":
    print("=== Daily Checklist Writer ===")
    title = input("Checklist title (or press Enter for 'Daily Checklist'): ")
    if not title.strip():
        title = "Daily Checklist"

    print(f"\nEnter your tasks one at a time. Type 'done' when finished.\n")

    tasks = []
    while True:
        task = input(f"  Task {len(tasks) + 1}: ")
        if task.strip().lower() == "done":
            break
        if task.strip():
            tasks.append(task.strip())

    # Format and display the checklist.
    checklist = format_checklist(title, tasks)
    print(f"\n{checklist}")

    # Ask if the user wants to save to a file.
    save = input("\nSave to file? (y/n): ").strip().lower()
    if save in ("y", "yes"):
        filename = input("File name (e.g. my_checklist.txt): ").strip()
        if not filename:
            filename = "checklist.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(checklist)
        print(f"Checklist saved to {filename}")
    else:
        print("Not saved. Goodbye!")
