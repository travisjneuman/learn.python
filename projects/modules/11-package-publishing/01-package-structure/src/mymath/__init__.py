"""
mymath — A simple math utilities package.

This __init__.py file does two things:
1. It marks the "mymath" directory as a Python package.
2. It controls what gets imported when someone writes "import mymath".

Without this file, Python would not recognize "mymath" as a package,
and "import mymath" would fail.
"""

# The version string. This is the single source of truth for the version.
# Some tools read this to determine the package version.
__version__ = "0.1.0"

# Import key functions so users can do:
#   from mymath import add, subtract
# instead of:
#   from mymath.calculator import add, subtract
from mymath.calculator import add, subtract, multiply, divide
from mymath.statistics import mean, median, mode
