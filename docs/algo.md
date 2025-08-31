---
title: Algorithms
---

# Dynamic Programming (DP)

## How to recognize DP

- Overlapping subproblems (you’d recompute the same thing).
- Optimal substructure (optimal answer composed of optimal sub-answers).

## DP checklist

1. **State**: what does `dp[i]` (or `dp[i][j]`) mean?
2. **Transition**: how to compute it from smaller states?
3. **Base case(s)**: trivial answers.
4. **Order**: iteration order so dependencies are ready.
5. **Answer**: which state(s) hold the final answer?
6. **Space**: can you compress rows/cols to O(1) or O(min(n,m))?

### Template — Top-Down (Memo)

```python
from functools import lru_cache

@lru_cache(None)
def f(args):
    # base case(s)
    # combine recursive calls
    return result
```

### Template — Bottom-Up (Tabulation)

```python
# allocate dp
# set base cases
# iterate in dependency order
# fill dp[i] (or dp[i][j]) using transitions
# return dp[last]
```

---

## Example 1 — Climbing Stairs (1 or 2 steps)

**Problem Understanding**: You're climbing a staircase with n steps. You can climb either 1 or 2 steps at a time. How many different ways can you climb to the top?

**Key Insight**: To reach step `i`, you must have come from either step `i-1` (climbing 1 step) or step `i-2` (climbing 2 steps).

**State**: `dp[i]` = ways to reach step `i`.
**Transition**: `dp[i] = dp[i-1] + dp[i-2]`.
**Base**: `dp[0]=1`, `dp[1]=1`.

**Why This Works**:
- **Step 0**: There's 1 way to be at the ground (do nothing)
- **Step 1**: There's 1 way to reach step 1 (climb 1 step)
- **Step 2**: You can reach it from step 1 (climb 1) or step 0 (climb 2) = 1 + 1 = 2 ways
- **Step 3**: You can reach it from step 2 (climb 1) or step 1 (climb 2) = 2 + 1 = 3 ways

**Pseudocode**

```
# dp[0] means one way to be at ground (do nothing)
dp[0] = 1
# one step has one way
dp[1] = 1

# fill upwards
for i from 2 to n:
    # ways to i are ways from i-1 and i-2
    dp[i] = dp[i-1] + dp[i-2]

# final answer is dp[n]
return dp[n]
```

**Python (O(n) time, O(1) space)**

```python
def climb_stairs(n: int) -> int:
    if n <= 1: return 1
    a, b = 1, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b
```

---

## Example 2 — Coin Change (Minimum coins to make amount)

**State**: `dp[x]` = min coins to form sum `x`.
**Transition**: `dp[x] = min(dp[x - coin] + 1)` for each coin if possible.
**Base**: `dp[0] = 0`; initialize others to `inf`.

**Pseudocode**

```
# dp[0] is zero coins
dp[0] = 0
# initialize other amounts as infinity
for x from 1 to amount:
    dp[x] = +infinity

# compute up to target
for x from 1 to amount:
    # try using each coin
    for coin in coins:
        # only valid if x-coin is reachable
        if x - coin >= 0 and dp[x-coin] != +infinity:
            # choose the best (fewest coins)
            dp[x] = min(dp[x], dp[x-coin] + 1)

# return -1 if impossible
if dp[amount] == +infinity: return -1
return dp[amount]
```

**Python**

```python
def coin_change(coins, amount):
    INF = amount + 1
    dp = [INF]*(amount+1)
    dp[0] = 0
    for x in range(1, amount+1):
        for c in coins:
            if x >= c:
                dp[x] = min(dp[x], dp[x-c] + 1)
    return -1 if dp[amount] == INF else dp[amount]
```

---

## Example 3 — Edit Distance (Levenshtein)

**State**: `dp[i][j]` = min edits to convert `s[:i]` → `t[:j]`.
**Transition**:

- If `s[i-1]==t[j-1]`: `dp[i][j] = dp[i-1][j-1]`
- Else `1 + min(insert, delete, replace)` → `1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])`
  **Base**: `dp[i][0]=i`, `dp[0][j]=j`.

**Pseudocode**

```
# initialize first row/col as inserting or deleting everything
for i from 0..n: dp[i][0] = i
for j from 0..m: dp[0][j] = j

# fill table
for i from 1..n:
    for j from 1..m:
        # if last chars equal, carry diagonal
        if s[i-1] == t[j-1]:
            dp[i][j] = dp[i-1][j-1]
        # otherwise consider insert/delete/replace
        else:
            # insert t[j-1]: dp[i][j-1]
            # delete s[i-1]: dp[i-1][j]
            # replace s[i-1] with t[j-1]: dp[i-1][j-1]
            dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])

# final edit distance
return dp[n][m]
```

**Python**

```python
def edit_distance(s, t):
    n, m = len(s), len(t)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1): dp[i][0] = i
    for j in range(m+1): dp[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])
    return dp[n][m]
```

---

## Example 4 — 0/1 Knapsack (maximize value under weight)

**State**: `dp[i][w]` = best value using first `i` items with capacity `w`.
**Transition**:

- Skip item i: `dp[i-1][w]`
- Take item i (if weight fits): `value[i-1] + dp[i-1][w - weight[i-1]]`
  **Base**: `dp[0][*] = 0`.

**Pseudocode**

```
# no items → value 0
for w from 0..W: dp[0][w] = 0

# fill by items then capacity
for i from 1..n:
    for w from 0..W:
        # start with skipping item
        dp[i][w] = dp[i-1][w]
        # if we can take it, see if better
        if weight[i-1] <= w:
            dp[i][w] = max(dp[i][w],
                           value[i-1] + dp[i-1][w - weight[i-1]])

# optimal value
return dp[n][W]
```

**Python (space-optimized O(W))**

```python
def knapsack_01(weights, values, W):
    dp = [0]*(W+1)
    for i in range(len(weights)):
        w, v = weights[i], values[i]
        for cap in range(W, w-1, -1):
            dp[cap] = max(dp[cap], v + dp[cap - w])
    return dp[W]
```

---

## Example 5 — Longest Increasing Subsequence (LIS)

**State**: `dp[i]` = length of LIS ending at `i`.
**Transition**: `dp[i] = 1 + max(dp[j]) for all j<i with a[j]<a[i]`.
**Base**: `dp[i]=1`.

**Pseudocode (O(n²))**

```
# each element is an LIS of length 1
for i from 0..n-1:
    dp[i] = 1

# extend from earlier smaller elements
for i from 0..n-1:
    for j from 0..i-1:
        # only extend if increasing
        if a[j] < a[i]:
            # choose best prior subsequence
            dp[i] = max(dp[i], dp[j] + 1)

# overall LIS is the maximum dp[i]
return max over dp
```

**Python — O(n log n) patience sorting variant**

```python
import bisect
def lis_length(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails): tails.append(x)
        else: tails[i] = x
    return len(tails)
```

---

# Greedy Algorithms

## How to recognize greedy

- **Local choice** that can be proven to lead to a global optimum (often via **exchange argument**).
- Sorting + one pass + occasional heap are common patterns.

## Principles

- Prove correctness: if an optimal solution exists, you can “exchange” its first choice with the greedy choice without hurting optimality.
- If you can’t argue that, consider DP instead.

---

## Example 1 — Interval Scheduling (max non-overlapping intervals)

**Idea**: sort by earliest finishing time; always pick the meeting that frees you soonest.

**Pseudocode**

```
# sort by end time ascending
sort intervals by end

# take the first interval
count = 0
last_end = -infinity

# scan in order
for each interval [s, e] in intervals:
    # if it doesn't overlap the last taken
    if s >= last_end:
        # take it
        count = count + 1
        # update the boundary
        last_end = e

# chosen count is maximal
return count
```

**Python**

```python
def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])
    cnt, last_end = 0, float('-inf')
    for s, e in intervals:
        if s >= last_end:
            cnt += 1
            last_end = e
    return cnt
```

---

## Example 2 — Meeting Rooms II (minimum rooms)

**Idea**: sort start times; track current meetings ending via a min-heap.

**Python**

```python
import heapq

def min_meeting_rooms(intervals):
    intervals.sort(key=lambda x: x[0])
    heap = []  # end times
    for s, e in intervals:
        if heap and heap[0] <= s:
            heapq.heappop(heap)
        heapq.heappush(heap, e)
    return len(heap)
```

---

## Example 3 — Jump Game II (min jumps to reach end)

**Idea**: greedy expand “current furthest reachable window”.

**Pseudocode**

```
# current window end
end = 0
# furthest reachable in current window
farthest = 0
# jumps taken
jumps = 0

# we don't need to jump from last index
for i from 0 to n-2:
    # extend furthest reach
    farthest = max(farthest, i + nums[i])
    # if we reached the end of the current window
    if i == end:
        # we must jump to extend the window
        jumps = jumps + 1
        # new window end is farthest we can reach now
        end = farthest

# minimal jumps
return jumps
```

---

## Example 4 — Kruskal’s MST (greedy + DSU)

**Idea**: sort edges by weight; add edges if they connect different components.

**Pseudocode**

```
# sort edges by weight ascending
sort edges by weight

# initialize union-find (disjoint set)
make_set for all vertices

# empty total weight
total = 0

# scan edges
for (u, v, w) in edges:
    # only take if it connects different components
    if find(u) != find(v):
        # union the components
        union(u, v)
        # add weight
        total = total + w

# total is the MST weight
return total
```

**Python (DSU helpers)**

```python
class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0]*n
    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        if self.r[ra] < self.r[rb]: ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]: self.r[ra] += 1
        return True
```

---

## Example 5 — Huffman Coding (outline)

**Idea**: greedily combine two least-frequent nodes repeatedly using a min-heap.

**Pseudocode**

```
# build min-heap of (freq, symbol)
heapify(freqs)

# while more than one node
while heap size > 1:
    # remove two smallest trees
    left = heappop()
    right = heappop()
    # merge into new tree
    merged = (left.freq + right.freq, new_internal_node(left, right))
    # push back
    heappush(merged)

# remaining tree is optimal prefix code
return heap[0]
```

---

## Algorithm Patterns & Techniques

### Two Pointers Technique
**When to use**: Array problems, linked lists, string manipulation
**Pattern**: Use two pointers moving at different speeds or directions

#### **Two Pointers - Same Direction (Fast/Slow)**
```python
# Find middle of linked list
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next          # Move 1 step
        fast = fast.next.next     # Move 2 steps
    return slow

# Detect cycle in linked list
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:          # Cycle detected
            return True
    return False
```

#### **Two Pointers - Opposite Directions**
```python
# Two Sum in sorted array
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []

# Valid palindrome
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        # Skip non-alphanumeric characters
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

### Sliding Window Technique
**When to use**: Subarray/substring problems, fixed or variable size windows
**Pattern**: Maintain a window that slides through the array

#### **Fixed Size Window**
```python
# Maximum sum of subarray of size k
def max_sum_subarray_k(nums, k):
    if len(nums) < k:
        return 0
    
    # Calculate sum of first window
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    # Slide window
    for i in range(k, len(nums)):
        window_sum = window_sum - nums[i-k] + nums[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

#### **Variable Size Window**
```python
# Longest substring without repeating characters
def length_of_longest_substring(s):
    char_map = {}
    left = max_length = 0
    
    for right, char in enumerate(s):
        # If character exists, move left pointer
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
        
        char_map[char] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Binary Search Variations
**When to use**: Sorted arrays, searching problems, optimization problems
**Pattern**: Divide search space in half each iteration

#### **Standard Binary Search**
```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

#### **Binary Search on Answer**
```python
# Find minimum capacity to ship packages within D days
def ship_within_days(weights, days):
    def can_ship(capacity):
        current_weight = 0
        days_needed = 1
        
        for weight in weights:
            if current_weight + weight > capacity:
                days_needed += 1
                current_weight = weight
            else:
                current_weight += weight
        
        return days_needed <= days
    
    left, right = max(weights), sum(weights)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_ship(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

#### **Finding Insert Position**
```python
def search_insert(nums, target):
    left, right = 0, len(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left
```

### Graph Algorithms

#### **Depth-First Search (DFS)**
```python
# DFS with recursion
def dfs_recursive(graph, node, visited):
    if node in visited:
        return
    
    visited.add(node)
    print(f"Visiting: {node}")
    
    for neighbor in graph[node]:
        dfs_recursive(graph, neighbor, visited)

# DFS with stack (iterative)
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        
        if node in visited:
            continue
        
        visited.add(node)
        print(f"Visiting: {node}")
        
        # Add unvisited neighbors to stack
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                stack.append(neighbor)
```

#### **Breadth-First Search (BFS)**
```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        node = queue.popleft()
        print(f"Visiting: {node}")
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

#### **Topological Sort (Kahn's Algorithm)**
```python
def topological_sort(graph):
    # Calculate in-degrees
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    # Find nodes with 0 in-degree
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        # Reduce in-degree of neighbors
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all nodes were processed
    return result if len(result) == len(graph) else []
```

### Tree Traversal Patterns

#### **Inorder Traversal (Left -> Root -> Right)**
```python
def inorder_traversal(root):
    result = []
    
    def inorder(node):
        if not node:
            return
        
        inorder(node.left)        # Visit left subtree
        result.append(node.val)    # Visit root
        inorder(node.right)       # Visit right subtree
    
    inorder(root)
    return result

# Iterative version using stack
def inorder_iterative(root):
    result = []
    stack = []
    current = root
    
    while current or stack:
        # Go to leftmost node
        while current:
            stack.append(current)
            current = current.left
        
        # Process current node
        current = stack.pop()
        result.append(current.val)
        
        # Move to right subtree
        current = current.right
    
    return result
```

#### **Level Order Traversal (BFS)**
```python
from collections import deque

def level_order_traversal(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result
```

### String Algorithms

#### **KMP Algorithm for Pattern Matching**
```python
def kmp_search(text, pattern):
    def build_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        
        return lps
    
    if not pattern:
        return 0
    
    lps = build_lps(pattern)
    i = j = 0
    
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return -1
```

#### **Rabin-Karp Algorithm**
```python
def rabin_karp_search(text, pattern):
    if len(pattern) > len(text):
        return -1
    
    # Hash function parameters
    d = 256  # Number of characters in input alphabet
    q = 101  # Prime number
    
    # Calculate hash values
    pattern_hash = 0
    text_hash = 0
    h = 1
    
    # Calculate h = d^(m-1) % q
    for i in range(len(pattern) - 1):
        h = (h * d) % q
    
    # Calculate hash for pattern and first window of text
    for i in range(len(pattern)):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        text_hash = (d * text_hash + ord(text[i])) % q
    
    # Slide the pattern over text one by one
    for i in range(len(text) - len(pattern) + 1):
        if pattern_hash == text_hash:
            # Check if characters match
            if text[i:i+len(pattern)] == pattern:
                return i
        
        # Calculate hash for next window
        if i < len(text) - len(pattern):
            text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + len(pattern)])) % q
            if text_hash < 0:
                text_hash += q
    
    return -1
```

### Dynamic Programming Advanced Patterns

#### **State Compression DP**
```python
# Traveling Salesman Problem with bitmask
def tsp_dp(graph):
    n = len(graph)
    # dp[mask][pos] = minimum cost to visit all cities in mask ending at pos
    dp = [[float('inf')] * n for _ in range(1 << n)]
    
    # Base case: starting from city 0
    dp[1][0] = 0
    
    # Try all possible subsets
    for mask in range(1 << n):
        for pos in range(n):
            if not (mask & (1 << pos)):
                continue
            
            # Try to come from previous city
            prev_mask = mask ^ (1 << pos)
            for prev_pos in range(n):
                if prev_mask & (1 << prev_pos):
                    dp[mask][pos] = min(dp[mask][pos], 
                                      dp[prev_mask][prev_pos] + graph[prev_pos][pos])
    
    # Return to starting city
    result = float('inf')
    for pos in range(1, n):
        result = min(result, dp[(1 << n) - 1][pos] + graph[pos][0])
    
    return result
```

#### **Digit DP**
```python
# Count numbers with digit sum equal to target
def count_numbers_with_digit_sum(n, target):
    def digit_dp(pos, tight, sum_so_far, dp):
        if pos == len(str_n):
            return 1 if sum_so_far == target else 0
        
        if dp[pos][tight][sum_so_far] != -1:
            return dp[pos][tight][sum_so_far]
        
        limit = int(str_n[pos]) if tight else 9
        result = 0
        
        for digit in range(limit + 1):
            new_tight = tight and (digit == limit)
            new_sum = sum_so_far + digit
            
            if new_sum <= target:
                result += digit_dp(pos + 1, new_tight, new_sum, dp)
        
        dp[pos][tight][sum_so_far] = result
        return result
    
    str_n = str(n)
    dp = [[[-1] * (target + 1) for _ in range(2)] for _ in range(len(str_n))]
    return digit_dp(0, True, 0, dp)
```

---

## Algorithm Problem Identification Guide

*Use this guide to quickly identify which algorithm pattern to apply to common problem types. Perfect for interview preparation and flashcard study.*

---

### **Array & String Problems**

#### **Two Pointers Pattern**
**When to use**: Array problems with ordered data or string manipulation
**Key indicators**:
- "Find two numbers that sum to target"
- "Remove duplicates from sorted array"
- "Check if string is palindrome"
- "Merge two sorted arrays"
- "Container with most water"

**Examples**:
```python
# Two Sum in sorted array
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []
```

#### **Sliding Window Pattern**
**When to use**: Subarray/substring problems with fixed or variable size
**Key indicators**:
- "Find longest substring without repeating characters"
- "Maximum sum subarray of size k"
- "Minimum window substring"
- "Longest substring with at most k distinct characters"
- "Find all anagrams in a string"

**Examples**:
```python
# Longest substring without repeating characters
def length_of_longest_substring(s):
    char_map = {}
    left = max_length = 0
    
    for right, char in enumerate(s):
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
        char_map[char] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

#### **Binary Search Pattern**
**When to use**: Sorted arrays, searching problems, optimization
**Key indicators**:
- "Find element in sorted array"
- "Find first/last occurrence"
- "Find minimum/maximum capacity"
- "Search in rotated sorted array"
- "Find peak element"

**Examples**:
```python
# Find minimum capacity to ship packages
def ship_within_days(weights, days):
    def can_ship(capacity):
        current_weight = 0
        days_needed = 1
        for weight in weights:
            if current_weight + weight > capacity:
                days_needed += 1
                current_weight = weight
            else:
                current_weight += weight
        return days_needed <= days
    
    left, right = max(weights), sum(weights)
    while left < right:
        mid = left + (right - left) // 2
        if can_ship(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

---

### **Tree & Graph Problems**

#### **Tree Traversal Pattern**
**When to use**: Tree problems requiring visiting all nodes
**Key indicators**:
- "Inorder/preorder/postorder traversal"
- "Level order traversal"
- "Validate binary search tree"
- "Serialize/deserialize tree"
- "Find lowest common ancestor"

**Examples**:
```python
# Validate Binary Search Tree
def is_valid_bst(root):
    def validate(node, low, high):
        if not node:
            return True
        if node.val <= low or node.val >= high:
            return False
        return (validate(node.left, low, node.val) and 
                validate(node.right, node.val, high))
    
    return validate(root, float('-inf'), float('inf'))
```

#### **Graph Traversal Pattern**
**When to use**: Graph problems requiring visiting nodes/edges
**Key indicators**:
- "Find shortest path"
- "Detect cycle in graph"
- "Topological sort"
- "Number of islands"
- "Clone graph"

**Examples**:
```python
# Detect cycle in directed graph
def has_cycle(graph):
    visited = set()
    rec_stack = set()
    
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(node)
        return False
    
    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    return False
```

---

### **Dynamic Programming Problems**

#### **Classic DP Pattern**
**When to use**: Problems with overlapping subproblems
**Key indicators**:
- "Maximum/minimum value"
- "Count ways to do something"
- "Longest increasing subsequence"
- "Coin change"
- "Climbing stairs"

**Examples**:
```python
# Coin Change - Minimum coins needed
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

#### **Knapsack Pattern**
**When to use**: Problems with choices and constraints
**Key indicators**:
- "Select items with weight/value constraints"
- "Partition equal subset sum"
- "Target sum"
- "0/1 knapsack"
- "Unbounded knapsack"

**Examples**:
```python
# Partition Equal Subset Sum
def can_partition(nums):
    total = sum(nums)
    if total % 2 != 0:
        return False
    
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    
    for num in nums:
        for i in range(target, num - 1, -1):
            dp[i] = dp[i] or dp[i - num]
    
    return dp[target]
```

---

### **Heap & Priority Queue Problems**

#### **Heap Pattern**
**When to use**: Problems requiring k-th element or top-k items
**Key indicators**:
- "Find k-th largest/smallest element"
- "Merge k sorted lists"
- "Top k frequent elements"
- "Median of data stream"
- "Sliding window median"

**Examples**:
```python
# Find K-th Largest Element
def find_kth_largest(nums, k):
    import heapq
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    
    return heap[0]
```

---

### **Backtracking Problems**

#### **Backtracking Pattern**
**When to use**: Problems requiring all possible combinations/permutations
**Key indicators**:
- "Generate all combinations"
- "Find all permutations"
- "N-queens problem"
- "Sudoku solver"
- "Word search"

**Examples**:
```python
# Generate All Permutations
def permute(nums):
    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return
        
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]
    
    result = []
    backtrack(0)
    return result
```

---

### **Quick Decision Tree**

#### **Problem Type → Algorithm Pattern**

**Array/String Problems:**
- **Sum/Pair problems** → Two Pointers
- **Subarray/Substring** → Sliding Window
- **Search in sorted data** → Binary Search
- **Find duplicates** → Hash Set/Map

**Tree Problems:**
- **Traversal** → DFS/BFS
- **Validation** → DFS with constraints
- **Path problems** → DFS with backtracking
- **Level problems** → BFS

**Graph Problems:**
- **Shortest path** → BFS (unweighted) / Dijkstra (weighted)
- **Cycle detection** → DFS with visited tracking
- **Topological sort** → Kahn's algorithm
- **Connected components** → DFS/BFS

**Optimization Problems:**
- **Maximum/Minimum** → Dynamic Programming
- **All combinations** → Backtracking
- **K-th element** → Heap
- **Greedy choice** → Greedy algorithm

---

### **Flashcard Format**

#### **Front Side (Problem Type)**
```
Problem: "Find longest substring without repeating characters"
Input: "abcabcbb"
Expected: 3 (substring "abc")
```

#### **Back Side (Solution Pattern)**
```
Algorithm: Sliding Window
Key Insight: Maintain window with unique characters
Time Complexity: O(n)
Space Complexity: O(min(m, n)) where m is charset size
```

#### **Quick Reference Cards**

**Card 1: Two Pointers**
- **When**: Ordered arrays, palindrome checks
- **Pattern**: Two indices moving in same/opposite directions
- **Complexity**: O(n) time, O(1) space

**Card 2: Sliding Window**
- **When**: Subarray/substring problems
- **Pattern**: Expand window, contract when condition violated
- **Complexity**: O(n) time, O(k) space

**Card 3: Binary Search**
- **When**: Sorted data, optimization problems
- **Pattern**: Divide search space in half
- **Complexity**: O(log n) time, O(1) space

**Card 4: Dynamic Programming**
- **When**: Overlapping subproblems, optimization
- **Pattern**: Build solution from smaller subproblems
- **Complexity**: Varies by problem

**Card 5: Tree Traversal**
- **When**: Tree problems, visiting all nodes
- **Pattern**: DFS (recursive/stack) or BFS (queue)
- **Complexity**: O(n) time, O(h) space

**Card 6: Graph Traversal**
- **When**: Graph problems, path finding
- **Pattern**: DFS/BFS with visited tracking
- **Complexity**: O(V + E) time, O(V) space

---

### **Interview Quick Reference**

#### **30-Second Problem Analysis**

1. **Read the problem** - Identify input/output
2. **Look for keywords** - "longest", "shortest", "k-th", "all"
3. **Check data structure** - Array, String, Tree, Graph
4. **Identify constraints** - Time/space requirements
5. **Choose pattern** - Use decision tree above
6. **Implement** - Apply the chosen algorithm

#### **Common Interview Patterns**

| Problem Type | Algorithm | Time | Space |
|-------------|-----------|------|-------|
| Two Sum | Hash Map | O(n) | O(n) |
| Longest Substring | Sliding Window | O(n) | O(k) |
| Binary Search | Binary Search | O(log n) | O(1) |
| Tree Traversal | DFS/BFS | O(n) | O(h) |
| Shortest Path | BFS | O(V+E) | O(V) |
| Dynamic Programming | DP | Varies | Varies |

*Use this guide to quickly identify algorithm patterns and ace your technical interviews!*
