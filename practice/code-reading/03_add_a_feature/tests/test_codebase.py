"""Base tests for the TODO app.

These tests verify existing functionality. Your new feature tests
should not break any of these.

Run with:
    cd practice/code-reading/03_add_a_feature
    python -m pytest tests/
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from codebase import add_todo, remove_todo, toggle_done, list_todos, load_todos, save_todos


def test_add_todo_to_empty_list():
    todos = add_todo([], "Buy milk")
    assert len(todos) == 1
    assert todos[0]["description"] == "Buy milk"
    assert todos[0]["done"] is False
    assert todos[0]["id"] == 1


def test_add_multiple_todos():
    todos = []
    todos = add_todo(todos, "First")
    todos = add_todo(todos, "Second")
    todos = add_todo(todos, "Third")
    assert len(todos) == 3
    assert todos[0]["id"] == 1
    assert todos[1]["id"] == 2
    assert todos[2]["id"] == 3


def test_remove_todo():
    todos = add_todo([], "Task A")
    todos = add_todo(todos, "Task B")
    todos = remove_todo(todos, 1)
    assert len(todos) == 1
    assert todos[0]["description"] == "Task B"


def test_remove_nonexistent_raises():
    todos = add_todo([], "Task A")
    try:
        remove_todo(todos, 999)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_toggle_done():
    todos = add_todo([], "Task A")
    assert todos[0]["done"] is False
    todos = toggle_done(todos, 1)
    assert todos[0]["done"] is True
    todos = toggle_done(todos, 1)
    assert todos[0]["done"] is False


def test_list_todos_empty():
    result = list_todos([])
    assert result == "No todos yet."


def test_list_todos_shows_status():
    todos = add_todo([], "Task A")
    todos = add_todo(todos, "Task B")
    todos = toggle_done(todos, 1)
    output = list_todos(todos)
    assert "[x]" in output
    assert "[ ]" in output
    assert "Task A" in output
    assert "Task B" in output


def test_save_and_load(tmp_path):
    filepath = str(tmp_path / "test_todos.json")
    todos = add_todo([], "Persistent task")
    save_todos(todos, filepath)

    loaded = load_todos(filepath)
    assert len(loaded) == 1
    assert loaded[0]["description"] == "Persistent task"


def test_load_missing_file(tmp_path):
    filepath = str(tmp_path / "nonexistent.json")
    todos = load_todos(filepath)
    assert todos == []
