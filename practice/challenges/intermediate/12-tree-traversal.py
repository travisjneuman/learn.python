"""
Challenge: Tree Traversal
Difficulty: Intermediate
Concepts: trees, BFS, DFS, queues, stacks, recursion
Time: 40 minutes

Implement BFS (breadth-first search) and DFS (depth-first search) traversals
on a simple tree structure.

The tree is represented by TreeNode objects with a value and a list of children.

Implement:
- `bfs(root)` -- return values in breadth-first order (level by level)
- `dfs_preorder(root)` -- return values in pre-order depth-first order (parent before children)
- `dfs_postorder(root)` -- return values in post-order depth-first order (children before parent)

Examples:
    Tree:       1
              / | \\
             2  3  4
            / \\
           5   6

    bfs:          [1, 2, 3, 4, 5, 6]
    dfs_preorder: [1, 2, 5, 6, 3, 4]
    dfs_postorder:[5, 6, 2, 3, 4, 1]
"""

from collections import deque


class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []


def bfs(root: TreeNode | None) -> list:
    """Return values in breadth-first (level) order. Implement this function."""
    # Hint: Use a queue (collections.deque). Enqueue root, then dequeue and enqueue children.
    pass


def dfs_preorder(root: TreeNode | None) -> list:
    """Return values in pre-order (parent before children) depth-first order. Implement this function."""
    # Hint: Visit the node first, then recursively visit each child.
    pass


def dfs_postorder(root: TreeNode | None) -> list:
    """Return values in post-order (children before parent) depth-first order. Implement this function."""
    # Hint: Recursively visit each child first, then visit the node.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Build tree:
    #       1
    #     / | \
    #    2  3  4
    #   / \
    #  5   6
    tree = TreeNode(1, [
        TreeNode(2, [TreeNode(5), TreeNode(6)]),
        TreeNode(3),
        TreeNode(4),
    ])

    # Test 1: BFS
    assert bfs(tree) == [1, 2, 3, 4, 5, 6], "BFS failed"

    # Test 2: DFS pre-order
    assert dfs_preorder(tree) == [1, 2, 5, 6, 3, 4], "DFS pre-order failed"

    # Test 3: DFS post-order
    assert dfs_postorder(tree) == [5, 6, 2, 3, 4, 1], "DFS post-order failed"

    # Test 4: Single node
    single = TreeNode(42)
    assert bfs(single) == [42], "BFS single node failed"
    assert dfs_preorder(single) == [42], "DFS pre-order single failed"
    assert dfs_postorder(single) == [42], "DFS post-order single failed"

    # Test 5: None root
    assert bfs(None) == [], "BFS None failed"
    assert dfs_preorder(None) == [], "DFS pre-order None failed"
    assert dfs_postorder(None) == [], "DFS post-order None failed"

    # Test 6: Linear chain (1 -> 2 -> 3)
    chain = TreeNode(1, [TreeNode(2, [TreeNode(3)])])
    assert bfs(chain) == [1, 2, 3], "BFS chain failed"
    assert dfs_preorder(chain) == [1, 2, 3], "DFS pre-order chain failed"
    assert dfs_postorder(chain) == [3, 2, 1], "DFS post-order chain failed"

    print("All tests passed!")
