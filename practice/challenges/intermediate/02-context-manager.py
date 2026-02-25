"""
Challenge: Context Manager for File Backup
Difficulty: Intermediate
Concepts: context managers, __enter__/__exit__, file I/O, os module
Time: 30 minutes

Write a context manager class called `FileBackup` that:
- On enter: creates a backup copy of a file (appending .bak to the name).
- Yields/returns the original file path so the caller can modify it.
- On normal exit: removes the backup file.
- On exception: restores the original file from the backup, then removes the backup.

You may use the `os` and `shutil` modules.

Examples:
    with FileBackup("data.txt") as path:
        # data.txt.bak exists as a backup
        with open(path, "w") as f:
            f.write("new content")
    # If no error: backup deleted, new content kept
    # If error: original content restored from backup
"""

import os
import shutil


class FileBackup:
    """Context manager that backs up a file and restores on error. Implement this class."""

    def __init__(self, filepath: str):
        # Hint: Store the filepath and compute the backup path (.bak suffix).
        pass

    def __enter__(self) -> str:
        # Hint: Copy the file to the backup path and return the original path.
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # Hint: If exc_type is not None, restore from backup. Always clean up the backup file.
        pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    import tempfile

    # Setup: create a temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
        tmp.write("original content")
        tmp_path = tmp.name

    backup_path = tmp_path + ".bak"

    # Test 1: Normal exit -- new content kept, backup removed
    with FileBackup(tmp_path) as path:
        assert os.path.exists(backup_path), "Backup should exist during context"
        with open(path, "w") as f:
            f.write("modified content")
    assert not os.path.exists(backup_path), "Backup should be removed after normal exit"
    with open(tmp_path) as f:
        assert f.read() == "modified content", "Modified content should be kept"

    # Reset file
    with open(tmp_path, "w") as f:
        f.write("original content")

    # Test 2: Exception exit -- original content restored
    try:
        with FileBackup(tmp_path) as path:
            with open(path, "w") as f:
                f.write("bad content")
            raise ValueError("something went wrong")
    except ValueError:
        pass
    assert not os.path.exists(backup_path), "Backup should be removed after exception"
    with open(tmp_path) as f:
        assert f.read() == "original content", "Original content should be restored after exception"

    # Cleanup
    os.unlink(tmp_path)
    print("All tests passed!")
