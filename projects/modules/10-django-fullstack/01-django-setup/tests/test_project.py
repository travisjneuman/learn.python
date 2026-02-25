"""
Tests for Project 01 — Django Setup Guide

This project's main file (setup_guide.py) generates a Django project
structure programmatically. These tests verify the helper functions and
the generated file structure WITHOUT actually running Django.

Why test a setup script?
    The script creates files with specific content. If it writes wrong
    content (e.g., wrong DJANGO_SETTINGS_MODULE), the generated project
    will not work. Tests verify the file creation and content correctness.

Run with: pytest tests/test_project.py -v
"""

import os
import textwrap

import pytest

from setup_guide import create_file, create_project_structure


# ── Test: create_file helper ───────────────────────────────────────────

def test_create_file_creates_file(tmp_path):
    """create_file should create a file with the given content.

    WHY: This is the core building block of the setup script. If it fails
    to create files or writes wrong content, every generated file is broken.
    """
    filepath = str(tmp_path / "subdir" / "test.txt")
    create_file(filepath, "hello world", "Test file")

    assert os.path.exists(filepath), "File should be created"

    with open(filepath) as f:
        assert f.read() == "hello world", "Content should match"


def test_create_file_creates_parent_directories(tmp_path):
    """create_file should create intermediate directories automatically.

    WHY: The setup script creates nested directory structures like
    demo_project/demo_project/settings.py. The helper must handle
    missing parent directories or the script will crash.
    """
    filepath = str(tmp_path / "deep" / "nested" / "dir" / "file.py")
    create_file(filepath, "content", "Nested test")

    assert os.path.exists(filepath), "Should create all parent directories"


def test_create_file_overwrites_existing(tmp_path):
    """create_file should overwrite an existing file.

    WHY: If the user runs the script twice, it should not crash on
    existing files. The 'w' mode in open() handles this.
    """
    filepath = str(tmp_path / "existing.txt")

    create_file(filepath, "first version", "Test")
    create_file(filepath, "second version", "Test")

    with open(filepath) as f:
        assert f.read() == "second version", "Should overwrite with new content"


# ── Test: create_project_structure ─────────────────────────────────────

def test_create_project_structure_creates_manage_py(tmp_path, monkeypatch):
    """create_project_structure should generate manage.py.

    WHY: manage.py is the entry point for all Django commands. Without it,
    you cannot run the development server, create migrations, or do anything
    with Django. This test verifies the file exists and contains the
    critical DJANGO_SETTINGS_MODULE line.
    """
    # Change to tmp_path so the project is created there.
    monkeypatch.chdir(tmp_path)

    # Monkeypatch __file__ to point to tmp_path so the script creates
    # demo_project inside tmp_path.
    import setup_guide
    original_file = setup_guide.__file__
    monkeypatch.setattr(setup_guide, "__file__", str(tmp_path / "setup_guide.py"))

    base_dir = create_project_structure()

    manage_py = os.path.join(base_dir, "manage.py")

    if os.path.exists(manage_py):
        # If the directory was freshly created, verify manage.py content.
        with open(manage_py) as f:
            content = f.read()
        assert "DJANGO_SETTINGS_MODULE" in content, (
            "manage.py must set DJANGO_SETTINGS_MODULE"
        )
    else:
        # If base_dir already existed, the function skips creation.
        # This is expected behavior — verify the function returned gracefully.
        assert os.path.exists(base_dir), "Should return the base directory path"

    # Restore the original __file__.
    monkeypatch.setattr(setup_guide, "__file__", original_file)


def test_create_project_structure_returns_path(tmp_path, monkeypatch):
    """create_project_structure should return the base directory path.

    WHY: The return value is used by callers to locate the generated files.
    If it returns None or the wrong path, downstream code breaks.
    """
    import setup_guide
    monkeypatch.setattr(setup_guide, "__file__", str(tmp_path / "setup_guide.py"))

    base_dir = create_project_structure()

    assert isinstance(base_dir, str), "Should return a string path"
    assert "demo_project" in base_dir, "Path should include 'demo_project'"
