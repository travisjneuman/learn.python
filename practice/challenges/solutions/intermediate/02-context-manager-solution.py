"""
Solution: Context Manager for File Backup

Approach: On __enter__, copy the file to a .bak backup. On __exit__, check
whether an exception occurred. If so, restore the original from the backup.
In all cases, remove the backup file to clean up.
"""

import os
import shutil


class FileBackup:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.backup_path = filepath + ".bak"

    def __enter__(self) -> str:
        # Create the backup copy
        shutil.copy2(self.filepath, self.backup_path)
        return self.filepath

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            # An exception occurred -- restore from backup
            shutil.copy2(self.backup_path, self.filepath)

        # Always clean up the backup file
        if os.path.exists(self.backup_path):
            os.remove(self.backup_path)

        # Return False to let exceptions propagate
        return False


if __name__ == "__main__":
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
        tmp.write("original content")
        tmp_path = tmp.name

    backup_path = tmp_path + ".bak"

    with FileBackup(tmp_path) as path:
        assert os.path.exists(backup_path)
        with open(path, "w") as f:
            f.write("modified content")
    assert not os.path.exists(backup_path)
    with open(tmp_path) as f:
        assert f.read() == "modified content"

    with open(tmp_path, "w") as f:
        f.write("original content")

    try:
        with FileBackup(tmp_path) as path:
            with open(path, "w") as f:
                f.write("bad content")
            raise ValueError("something went wrong")
    except ValueError:
        pass
    assert not os.path.exists(backup_path)
    with open(tmp_path) as f:
        assert f.read() == "original content"

    os.unlink(tmp_path)
    print("All tests passed!")
