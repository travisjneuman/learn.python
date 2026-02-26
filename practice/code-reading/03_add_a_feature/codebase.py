"""A simple TODO application with file persistence."""

import json
import os

TODO_FILE = "todos.json"


def load_todos(filepath=TODO_FILE):
    """Load todos from a JSON file. Returns an empty list if the file does not exist."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)


def save_todos(todos, filepath=TODO_FILE):
    """Save the todo list to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(todos, f, indent=2)


def add_todo(todos, description):
    """Add a new todo item. Returns the updated list."""
    todo = {
        "id": max((t["id"] for t in todos), default=0) + 1,
        "description": description,
        "done": False,
    }
    todos.append(todo)
    return todos


def remove_todo(todos, todo_id):
    """Remove a todo by its ID. Returns the updated list.

    Raises ValueError if the ID is not found.
    """
    original_length = len(todos)
    todos = [t for t in todos if t["id"] != todo_id]
    if len(todos) == original_length:
        raise ValueError(f"No todo with id {todo_id}")
    return todos


def toggle_done(todos, todo_id):
    """Toggle the done status of a todo. Returns the updated list.

    Raises ValueError if the ID is not found.
    """
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = not t["done"]
            return todos
    raise ValueError(f"No todo with id {todo_id}")


def list_todos(todos):
    """Return a formatted string listing all todos."""
    if not todos:
        return "No todos yet."
    lines = []
    for t in todos:
        status = "[x]" if t["done"] else "[ ]"
        lines.append(f"  {t['id']}. {status} {t['description']}")
    return "\n".join(lines)


def main():
    """Interactive command loop."""
    todos = load_todos()
    print("TODO App — commands: add, remove, toggle, list, quit")

    while True:
        command = input("\n> ").strip().lower()

        if command == "add":
            desc = input("  Description: ").strip()
            if desc:
                todos = add_todo(todos, desc)
                save_todos(todos)
                print(f"  Added: {desc}")
            else:
                print("  Description cannot be empty.")

        elif command == "remove":
            try:
                todo_id = int(input("  ID to remove: "))
                todos = remove_todo(todos, todo_id)
                save_todos(todos)
                print(f"  Removed todo {todo_id}.")
            except ValueError as e:
                print(f"  Error: {e}")

        elif command == "toggle":
            try:
                todo_id = int(input("  ID to toggle: "))
                todos = toggle_done(todos, todo_id)
                save_todos(todos)
                print(f"  Toggled todo {todo_id}.")
            except ValueError as e:
                print(f"  Error: {e}")

        elif command == "list":
            print(list_todos(todos))

        elif command == "quit":
            print("  Goodbye.")
            break

        else:
            print("  Unknown command. Try: add, remove, toggle, list, quit")


if __name__ == "__main__":
    main()
