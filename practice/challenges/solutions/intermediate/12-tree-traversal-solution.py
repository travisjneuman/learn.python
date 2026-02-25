"""
Solution: Tree Traversal

Approach:
- BFS uses a queue (deque). Start with root, dequeue a node, enqueue its children.
  This processes nodes level by level.
- DFS pre-order visits the node first, then recurses into children.
- DFS post-order recurses into children first, then visits the node.
"""

from collections import deque


class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []


def bfs(root: TreeNode | None) -> list:
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.value)
        # Enqueue all children for next-level processing
        for child in node.children:
            queue.append(child)

    return result


def dfs_preorder(root: TreeNode | None) -> list:
    if root is None:
        return []

    # Visit node first, then children
    result = [root.value]
    for child in root.children:
        result.extend(dfs_preorder(child))
    return result


def dfs_postorder(root: TreeNode | None) -> list:
    if root is None:
        return []

    # Visit children first, then node
    result = []
    for child in root.children:
        result.extend(dfs_postorder(child))
    result.append(root.value)
    return result


if __name__ == "__main__":
    tree = TreeNode(1, [
        TreeNode(2, [TreeNode(5), TreeNode(6)]),
        TreeNode(3),
        TreeNode(4),
    ])

    assert bfs(tree) == [1, 2, 3, 4, 5, 6]
    assert dfs_preorder(tree) == [1, 2, 5, 6, 3, 4]
    assert dfs_postorder(tree) == [5, 6, 2, 3, 4, 1]

    single = TreeNode(42)
    assert bfs(single) == [42]
    assert dfs_preorder(single) == [42]
    assert dfs_postorder(single) == [42]

    assert bfs(None) == []
    assert dfs_preorder(None) == []
    assert dfs_postorder(None) == []

    chain = TreeNode(1, [TreeNode(2, [TreeNode(3)])])
    assert bfs(chain) == [1, 2, 3]
    assert dfs_preorder(chain) == [1, 2, 3]
    assert dfs_postorder(chain) == [3, 2, 1]

    print("All tests passed!")
