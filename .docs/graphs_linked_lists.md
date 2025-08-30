---
title: Complex Data Structures
---

# 📘 Trees

### Key Properties

- A **tree** is a connected graph with no cycles.
- **Binary Tree**: each node has up to 2 children.
- **BST (Binary Search Tree)**: left < root < right.
- **Common Operations**: traversal, insertion, search, min/max, depth/height.

### Traversals

| Traversal   | Order               | Use Case                      |
| ----------- | ------------------- | ----------------------------- |
| Pre-order   | Root → Left → Right | Copy tree, prefix expressions |
| In-order    | Left → Root → Right | Sorted order in BST           |
| Post-order  | Left → Right → Root | Deletion, postfix expressions |
| Level-order | BFS by level        | Shortest paths, levels        |

**Recursive Traversal Pseudocode**

```
inorder(node):
    if node is None: return
    inorder(node.left)
    visit(node)
    inorder(node.right)
```

**Python Examples**

```python
def inorder(root):
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)

def preorder(root):
    if root:
        print(root.val)
        preorder(root.left)
        preorder(root.right)

def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.val)
```

**Level Order BFS**

```python
from collections import deque

def level_order(root):
    if not root: return []
    q = deque([root])
    res = []
    while q:
        node = q.popleft()
        res.append(node.val)
        if node.left: q.append(node.left)
        if node.right: q.append(node.right)
    return res
```

---

# 📘 Graphs

### Key Properties

- **Adjacency List**: `graph = {node: [neighbors]}`
- **Adjacency Matrix**: 2D array, O(n²) space.
- Traversals: BFS (queue), DFS (stack/recursion).
- Applications: shortest paths, connectivity, cycle detection.

### DFS

**Pseudocode**

```
dfs(node):
    if node in visited: return
    mark node visited
    for neighbor in graph[node]:
        dfs(neighbor)
```

**Python**

```python
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    if node in visited: return
    visited.add(node)
    print(node)
    for nei in graph[node]:
        dfs(graph, nei, visited)
```

### BFS

**Pseudocode**

```
bfs(start):
    queue ← [start]
    visited ← {start}
    while queue not empty:
        node = dequeue()
        for neighbor in graph[node]:
            if neighbor not visited:
                mark visited
                enqueue(neighbor)
```

**Python**

```python
from collections import deque

def bfs(graph, start):
    q = deque([start])
    visited = {start}
    while q:
        node = q.popleft()
        print(node)
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                q.append(nei)
```

Great call—here are the **approved-style** sections you asked for, rebuilt with clear tables and code snippets. Per your preference, **comments are above the relevant line(s)** (not inline). Review these, and if they look right I’ll add them to the canvas.

---

# Dictionaries (Python `dict`)

## What to remember

- Average **O(1)** insert/lookup/delete (hash table).
- **Insertion order preserved** (Python 3.7+).
- Use `.get()`, `.setdefault()`, `defaultdict`, `Counter` for common patterns.
- “Sorting” means sorting **views** (keys/items) and producing a **list**.

## Core methods & ops

| Task           | Code                                 | Notes                                      |        |
| -------------- | ------------------------------------ | ------------------------------------------ | ------ |
| Create         | `d = {}` / `dict()`                  | empty dict                                 |        |
| Insert/Update  | `d[k] = v`                           | O(1) avg                                   |        |
| Safe lookup    | `d.get(k, default)`                  | avoids KeyError                            |        |
| Delete         | `del d[k]` / `d.pop(k)`              | KeyError if missing (unless `pop(k, def)`) |        |
| Iterate keys   | `for k in d:` / `for k in d.keys():` | O(n)                                       |        |
| Iterate values | `for v in d.values():`               | O(n)                                       |        |
| Iterate items  | `for k, v in d.items():`             | O(n)                                       |        |
| Exists?        | `k in d`                             | O(1) avg                                   |        |
| Merge          | \`d3 = d1                            | d2\`                                       | Py3.9+ |
| Default init   | `d.setdefault(k, init)`              | avoid if heavy default                     |        |
| Auto-init dict | `defaultdict(list)`                  | from `collections`                         |        |
| Frequency map  | `Counter(iterable)`                  | from `collections`                         |        |

## Add / Remove / Traverse / “Sort”

```python
# --- create empty dict
d = {}

# --- add/update entries
d["a"] = 1
d["b"] = 2
d["a"] = 10  # update

# --- safe lookup with default
value = d.get("c", 0)

# --- remove a key (raises if absent)
del d["b"]

# --- remove with return value (no raise if default provided)
removed = d.pop("missing", None)

# --- traverse keys
for k in d.keys():
    # use k
    pass

# --- traverse values
for v in d.values():
    # use v
    pass

# --- traverse key/value pairs
for k, v in d.items():
    # use k, v
    pass

# --- "sort by key" → list of (k,v)
sorted_by_key = sorted(d.items(), key=lambda kv: kv[0])

# --- "sort by value" → list of (k,v)
sorted_by_value = sorted(d.items(), key=lambda kv: kv[1])

# --- build dict comprehension (e.g., filter)
filtered = {k: v for k, v in d.items() if v > 5}
```

## Helpers (`defaultdict`, `Counter`)

```python
# --- defaultdict for grouping
from collections import defaultdict
groups = defaultdict(list)
for key, value in [("x", 1), ("x", 2), ("y", 9)]:
    # append to auto-created list
    groups[key].append(value)

# --- Counter for frequency
from collections import Counter
freq = Counter("abracadabra")
# freq.most_common() returns sorted (char,count) desc
```

---

# Sets (Python `set`)

## What to remember

- **Unique, unordered** elements; avg **O(1)** membership and add/remove.
- Use set algebra: union `|`, intersection `&`, difference `-`, symmetric diff `^`.
- “Sorting” a set returns a **new list** via `sorted(s)`.

## Core methods & ops

| Task           | Code                           | Notes                     |              |
| -------------- | ------------------------------ | ------------------------- | ------------ |
| Create         | `s = set()` / `{1,2,3}`        | empty or literal          |              |
| Add            | `s.add(x)`                     | O(1) avg                  |              |
| Remove         | `s.remove(x)` / `s.discard(x)` | `remove` raises if absent |              |
| Pop arbitrary  | `s.pop()`                      | removes some element      |              |
| Membership     | `x in s`                       | O(1) avg                  |              |
| Union          | \`s                            | t\`                       | all elements |
| Intersect      | `s & t`                        | common elements           |              |
| Diff           | `s - t`                        | in s, not in t            |              |
| Symmetric diff | `s ^ t`                        | in s or t, not both       |              |
| Sub/Superset   | `s <= t`, `s >= t`             | set relations             |              |
| Sorted view    | `sorted(s)`                    | list result               |              |

## Add / Remove / Traverse / “Sort”

```python
# --- create
s = set()

# --- add
s.add(3)
s.add(1)
s.add(3)  # no effect (unique elements)

# --- remove (raises if missing)
if 2 in s:
    s.remove(2)

# --- discard (safe)
s.discard(100)

# --- traverse (order arbitrary)
for x in s:
    # use x
    pass

# --- "sort" (returns a list)
sorted_list = sorted(s)

# --- algebra examples
t = {1, 2, 4}
u = s | t      # union
i = s & t      # intersection
d = s - t      # difference
x = s ^ t      # symmetric difference
```

## `frozenset` (hashable set)

```python
# --- frozenset can be a dict key or set element
fs = frozenset([1,2,3])
d = {fs: "value"}
```

---

# Trees (Binary Tree + BST specifics)

## What to remember

- Common interviews use a simple `TreeNode(val, left, right)`.
- Traversals: **pre/in/post-order** (DFS), **level-order** (BFS).
- “Sorting” a BST is just **in-order traversal** to a list.
- Insertion/removal examples below assume a **BST**; for general binary trees, “add/remove” is problem-specific.

## Node definition

```python
# --- basic binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

## Add (BST insert)

```python
# --- insert a value into BST
def bst_insert(root, x):
    # empty spot → create node
    if root is None:
        return TreeNode(x)
    # go left if smaller
    if x < root.val:
        root.left = bst_insert(root.left, x)
    # go right if larger
    elif x > root.val:
        root.right = bst_insert(root.right, x)
    # equal: often ignore or store count; here we ignore
    return root
```

## Remove (BST delete)

```python
# --- delete value x from BST
def bst_delete(root, x):
    # base: not found
    if root is None:
        return None
    # search left
    if x < root.val:
        root.left = bst_delete(root.left, x)
        return root
    # search right
    if x > root.val:
        root.right = bst_delete(root.right, x)
        return root
    # found node to delete:
    # case 1: no left → return right
    if root.left is None:
        return root.right
    # case 2: no right → return left
    if root.right is None:
        return root.left
    # case 3: two children → replace with inorder successor
    # find min in right subtree
    succ = root.right
    while succ.left:
        succ = succ.left
    # copy successor value
    root.val = succ.val
    # delete successor node from right subtree
    root.right = bst_delete(root.right, succ.val)
    return root
```

## Traverse (DFS: pre/in/post)

```python
# --- pre-order: N L R
def preorder(root, visit):
    # stop at empty
    if not root:
        return
    # visit node
    visit(root)
    # traverse left
    preorder(root.left, visit)
    # traverse right
    preorder(root.right, visit)

# --- in-order: L N R (sorted order for BST)
def inorder(root, visit):
    if not root:
        return
    inorder(root.left, visit)
    visit(root)
    inorder(root.right, visit)

# --- post-order: L R N
def postorder(root, visit):
    if not root:
        return
    postorder(root.left, visit)
    postorder(root.right, visit)
    visit(root)
```

## “Sort” a BST into a list (in-order)

```python
# --- return ascending values of BST
def bst_to_sorted_list(root):
    res = []
    # helper to collect nodes in-order
    def visit(node):
        res.append(node.val)
    inorder(root, visit)
    return res
```

## Traverse (BFS: level-order)

```python
# --- level-order traversal
from collections import deque

def level_order(root):
    # result collector
    res = []
    # empty tree
    if not root:
        return res
    # init queue with root
    q = deque([root])
    # process queue until empty
    while q:
        # get current level size
        n = len(q)
        # start new level list
        level = []
        # process each node in level
        for _ in range(n):
            node = q.popleft()
            level.append(node.val)
            # push children if present
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        # add level to result
        res.append(level)
    return res
```

## Search (BST)

```python
# --- search value in BST
def bst_search(root, x):
    # walk down until hit None or value
    while root and root.val != x:
        # go right if current < x
        if root.val < x:
            root = root.right
        # otherwise go left
        else:
            root = root.left
    # either node or None
    return root
```

## Depth & Balance

```python
# --- max depth
def maxDepth(root):
    # empty tree depth is 0
    if root is None:
        return 0
    # depth of left subtree
    left = maxDepth(root.left)
    # depth of right subtree
    right = maxDepth(root.right)
    # include current node (+1)
    return 1 + max(left, right)

# --- height-balanced check
def isBalanced(root):
    def dfs(node):
        # height 0 for empty
        if not node:
            return 0
        # compute left/right heights
        L = dfs(node.left)
        R = dfs(node.right)
        # early stop if unbalanced below
        if L == -1 or R == -1:
            return -1
        # check local balance
        if abs(L - R) > 1:
            return -1
        # return height
        return 1 + max(L, R)
    # balanced if not -1
    return dfs(root) != -1
```
