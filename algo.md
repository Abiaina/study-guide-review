# Dynamic Programming (DP)

## How to recognize DP

* Overlapping subproblems (you’d recompute the same thing).
* Optimal substructure (optimal answer composed of optimal sub-answers).

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

**State**: `dp[i]` = ways to reach step `i`.
**Transition**: `dp[i] = dp[i-1] + dp[i-2]`.
**Base**: `dp[0]=1`, `dp[1]=1`.

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

* If `s[i-1]==t[j-1]`: `dp[i][j] = dp[i-1][j-1]`
* Else `1 + min(insert, delete, replace)` → `1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])`
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

* Skip item i: `dp[i-1][w]`
* Take item i (if weight fits): `value[i-1] + dp[i-1][w - weight[i-1]]`
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

* **Local choice** that can be proven to lead to a global optimum (often via **exchange argument**).
* Sorting + one pass + occasional heap are common patterns.

## Principles

* Prove correctness: if an optimal solution exists, you can “exchange” its first choice with the greedy choice without hurting optimality.
* If you can’t argue that, consider DP instead.

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