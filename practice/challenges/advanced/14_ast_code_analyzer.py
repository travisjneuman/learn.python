"""
Challenge 14: AST Code Analyzer
Difficulty: Level 9
Topic: Use the ast module to analyze Python source code

Build tools that parse Python source code into an AST and extract useful
information without executing the code. This is how linters, type checkers,
and code formatters work under the hood.

Concepts: ast.parse, ast.walk, ast.NodeVisitor, static analysis.
Review: concepts/how-imports-work.md

Instructions:
    1. Implement `count_functions` — count function definitions in source.
    2. Implement `list_imports` — extract all imported module names.
    3. Implement `find_classes` — extract class names and their method names.
    4. Implement `complexity_score` — simple cyclomatic complexity estimate.
"""

import ast


def count_functions(source: str) -> int:
    """Return the number of function definitions (def and async def) in *source*.

    Count top-level and nested functions. Methods inside classes count too.
    """
    # YOUR CODE HERE
    ...


def list_imports(source: str) -> list[str]:
    """Return a sorted list of unique module names imported in *source*.

    Handle both `import X` and `from X import Y` forms.
    For `from X.Y import Z`, return "X.Y" (the module, not the name).
    """
    # YOUR CODE HERE
    ...


def find_classes(source: str) -> dict[str, list[str]]:
    """Return a dict mapping class names to sorted lists of their method names.

    Only include direct methods (def inside the class body), not nested classes
    or functions inside methods.
    """
    # YOUR CODE HERE
    ...


def complexity_score(source: str) -> int:
    """Estimate cyclomatic complexity of *source*.

    Start at 1 (base complexity), then add 1 for each:
    - if / elif (ast.If)
    - for loop (ast.For, ast.AsyncFor)
    - while loop (ast.While)
    - except handler (ast.ExceptHandler)
    - boolean operator 'and' / 'or' (ast.BoolOp — each BoolOp adds
      len(node.values) - 1)

    Walk the entire AST (all nesting levels).
    """
    # YOUR CODE HERE
    ...


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- count_functions ---
    src1 = '''
def foo():
    pass

async def bar():
    def inner():
        pass

class MyClass:
    def method(self):
        pass
'''
    assert count_functions(src1) == 4, f"Got {count_functions(src1)}"
    assert count_functions("x = 1") == 0

    # --- list_imports ---
    src2 = '''
import os
import sys
from pathlib import Path
from os.path import join, exists
import os  # duplicate
from collections.abc import Callable
'''
    imports = list_imports(src2)
    assert imports == ["collections.abc", "os", "os.path", "pathlib", "sys"], \
        f"Got {imports}"
    assert list_imports("x = 1") == []

    # --- find_classes ---
    src3 = '''
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass

    def eat(self):
        pass

class Dog(Animal):
    def speak(self):
        return "woof"

    def fetch(self):
        pass
'''
    classes = find_classes(src3)
    assert classes == {
        "Animal": ["__init__", "eat", "speak"],
        "Dog": ["fetch", "speak"],
    }, f"Got {classes}"

    # --- complexity_score ---
    simple = "x = 1\ny = 2"
    assert complexity_score(simple) == 1

    branchy = '''
def process(x):
    if x > 0:
        for i in range(x):
            if i % 2 == 0:
                pass
    elif x < 0:
        while x < 0:
            x += 1
    try:
        risky()
    except ValueError:
        pass
    except TypeError:
        pass
'''
    # 1 (base) + 1 (if) + 1 (for) + 1 (inner if) + 1 (elif) + 1 (while)
    # + 1 (except ValueError) + 1 (except TypeError) = 8
    assert complexity_score(branchy) == 8, f"Got {complexity_score(branchy)}"

    bool_ops = '''
if a and b and c:
    pass
if x or y:
    pass
'''
    # 1 (base) + 1 (first if) + 2 (and with 3 values -> 2) + 1 (second if)
    # + 1 (or with 2 values -> 1) = 6
    assert complexity_score(bool_ops) == 6, f"Got {complexity_score(bool_ops)}"

    print("All tests passed.")
