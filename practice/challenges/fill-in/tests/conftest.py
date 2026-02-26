"""Configure test imports to find exercise files."""

import sys
from pathlib import Path

# Add the fill-in directory to the path so tests can import exercises
sys.path.insert(0, str(Path(__file__).parent.parent))
