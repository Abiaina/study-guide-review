## **1. Big-O Complexity Cheat Sheet**

| Operation (Python)          | Time Complexity | Notes / Helpers                               |
| --------------------------- | --------------- | --------------------------------------------- |
| Indexing (list\[i])         | O(1)            | Direct access                                 |
| Append (list.append)        | O(1) amortized  | Occasionally reallocates                      |
| Insert / Pop (at end)       | O(1)            | Good for stack ops                            |
| Insert / Pop (at beginning) | O(n)            | Use `collections.deque` for O(1)              |
| Search (in list)            | O(n)            | Linear scan                                   |
| Dictionary / Set lookup     | O(1) average    | Hash-based                                    |
| Sorting (sorted, list.sort) | O(n log n)      | Timsort (optimized for partially sorted data) |
| Heap push/pop (`heapq`)     | O(log n)        | Priority queue                                |

👉 **Helper libraries in Python**

* `collections.deque` → O(1) pops/appends at both ends.
* `collections.Counter` → Fast frequency counting.
* `collections.defaultdict` → Cleaner hash maps with default values.
* `heapq` → Priority queue implementation.
* `bisect` → Binary search on sorted arrays.

---

## **2. Strings & Arrays**

### Common Patterns

* **Two pointers**: Used for palindromes, merging sorted arrays, sliding windows.
* **Sliding window**: Substring/array problems (`longest substring`, `max sum subarray`).
* **Prefix sums**: Range queries, subarray sums.
* **Hash maps (dict)**: Fast lookup for duplicates, anagrams, substrings.

### Practice Problems

1. Reverse a string → O(n).
2. Check palindrome (ignore punctuation, spaces).
3. Longest substring without repeating characters (sliding window).
4. Two Sum (hash map, O(n)).
5. Maximum subarray (Kadane’s algorithm, O(n)).

---



Compare Core Data Structures 
| Operation         | List            | Dict                       | Set            | Queue/Deque           |
| ----------------- | --------------- | -------------------------- | -------------- | --------------------- |
| `len()`           | ✅               | ✅                          | ✅              | ✅                     |
| `in` (membership) | O(n)            | O(1)                       | O(1)           | O(n)                  |
| `pop()`           | End only (O(1)) | By key (O(1) avg)          | Arbitrary O(1) | Left/right O(1)       |
| `clear()`         | ✅               | ✅                          | ✅              | ✅                     |
| `sorted()`        | ✅               | On `.items()` (O(n log n)) | ✅              | Convert to list first |
| Iteration         | `for x in list` | `for k,v in dict.items()`  | `for x in set` | `for x in deque`      |

---

# 📘 Arrays & Lists (Python Focus)

### Key Properties

| Feature       | Python `list`             | Python `array` (from `array` module) |
| ------------- | ------------------------- | ------------------------------------ |
| Storage       | Dynamic, heterogeneous    | Homogeneous (all same typecode)      |
| Typical Usage | General-purpose container | Numeric data, memory-efficient       |
| Resize        | Automatic                 | Automatic                            |
| Indexing      | O(1)                      | O(1)                                 |
| Insert/Delete | O(n) (shifts elements)    | O(n)                                 |
| Iteration     | O(n)                      | O(n)                                 |

---

### Common Operations

| Operation           | Python `list` Example             | Notes                          |
| ------------------- | --------------------------------- | ------------------------------ |
| **Create**          | `nums = [1,2,3]`                  | Literal syntax                 |
| **Iterate**         | `for x in nums: print(x)`         | Sequential traversal           |
| **Index**           | `nums[0]` → `1`                   | O(1)                           |
| **Slice**           | `nums[1:3]` → `[2,3]`             | Returns new list               |
| **Add (append)**    | `nums.append(4)`                  | O(1) amortized                 |
| **Insert**          | `nums.insert(1, 10)`              | O(n), shifts                   |
| **Delete (by val)** | `nums.remove(2)`                  | First match only               |
| **Delete (by idx)** | `del nums[0]`                     | Shifts                         |
| **Pop**             | `nums.pop()` → last el            | O(1) for end                   |
| **Sort**            | `nums.sort()`                     | In-place, Timsort (O(n log n)) |
| **Reverse**         | `nums.reverse()`                  | In-place                       |
| **Special**         | `len(nums), sum(nums), max(nums)` | Common helpers                 |

---

### Example Snippets

#### Iterating

```python
nums = [1, 2, 3, 4]
for x in nums:
    print(x)
```

#### Adding & Removing

```python
nums.append(5)       # [1,2,3,4,5]
nums.insert(2, 10)   # [1,2,10,3,4,5]
nums.remove(3)       # removes first '3'
popped = nums.pop()  # removes last element, returns it
```

#### Sorting

```python
nums.sort()          # ascending
nums.sort(reverse=True)  # descending
sorted_copy = sorted(nums)  # returns new list
```

#### Pseudocode (for clarity)

```text
function insert(list, index, value):
    shift elements right from index
    place value at index
```

---


# 📘 Dictionaries (Python `dict`)

### Key Properties

* Key-value store (hash table under the hood).
* Keys must be **hashable** (immutable types: str, int, tuple).
* Average-case operations: O(1) lookup, insert, delete.
* Worst-case O(n) (rare, due to hash collisions).

---

### Common Operations

| Operation          | Example                  | Notes                      |
| ------------------ | ------------------------ | -------------------------- |
| **Create**         | `d = {"a": 1, "b": 2}`   | Literal syntax             |
| **Iterate keys**   | `for k in d:`            | Same as `d.keys()`         |
| **Iterate values** | `for v in d.values():`   | Values only                |
| **Iterate items**  | `for k, v in d.items():` | Key + value                |
| **Access**         | `d["a"]` → `1`           | KeyError if missing        |
| **Safe access**    | `d.get("c", 0)`          | Returns default if missing |
| **Add / Update**   | `d["c"] = 3`             | Insert or overwrite        |
| **Delete by key**  | `del d["a"]`             | Key must exist             |
| **Pop**            | `d.pop("a", None)`       | Optional default           |
| **Clear**          | `d.clear()`              | Remove all items           |
| **Check key**      | `"a" in d`               | Membership test            |
| **Length**         | `len(d)`                 | Number of pairs            |

---

### Special Methods

* `.keys()` → view of all keys (iterable).
* `.values()` → view of all values.
* `.items()` → iterable of `(key, value)` tuples.
* `.update({...})` → bulk add/update.
* `.popitem()` → remove *last* inserted (Python ≥ 3.7 keeps insertion order).

---

### Example Snippets

#### Iteration

```python
d = {"a": 1, "b": 2, "c": 3}

for k in d:                # keys
    print(k)

for v in d.values():       # values
    print(v)

for k, v in d.items():     # key-value pairs
    print(k, v)
```

#### Adding & Removing

```python
d["d"] = 4            # add
d.update({"e": 5})    # bulk add/update
del d["a"]            # delete
d.pop("b", None)      # delete with default
```

#### Sorting

```python
# sort by key
print(sorted(d.items()))    # [('c', 3), ('d', 4), ('e', 5)]

# sort by value
print(sorted(d.items(), key=lambda x: x[1]))
```

---

# 📘 Sets (`set` in Python)

### Key Properties

* Unordered, unique elements only.
* Backed by hash table → O(1) avg lookup/insert/delete.
* No duplicates, no indexing.

### Common Operations

| Operation        | Example         | Notes                     |         |
| ---------------- | --------------- | ------------------------- | ------- |
| **Create**       | `s = {1, 2, 3}` | Or `set([1,2,3])`         |         |
| **Iterate**      | `for x in s:`   | Order not guaranteed      |         |
| **Add**          | `s.add(4)`      | Insert element            |         |
| **Remove**       | `s.remove(2)`   | KeyError if missing       |         |
| **Discard**      | `s.discard(2)`  | Safe remove               |         |
| **Pop**          | `s.pop()`       | Removes arbitrary element |         |
| **Clear**        | `s.clear()`     | Remove all                |         |
| **Check**        | `3 in s`        | Membership test           |         |
| **Union**        | \`s1            | s2\`                      | Combine |
| **Intersection** | `s1 & s2`       | Common elements           |         |
| **Difference**   | `s1 - s2`       | Unique to s1              |         |

### Special Methods

* `.update(iterable)` → bulk add.
* `.issubset()`, `.issuperset()`.
* `.symmetric_difference()`.

### Examples

```python
s = {1, 2, 3}
s.add(4)             # {1,2,3,4}
s.remove(2)          # {1,3,4}
print(3 in s)        # True
print(s.union({5}))  # {1,3,4,5}
```

---

# 📘 Stacks (LIFO)

### Key Properties

* Last In, First Out (LIFO).
* Implement with `list` or `collections.deque`.

### Common Operations

| Operation   | Example           | Notes       |
| ----------- | ----------------- | ----------- |
| **Push**    | `stack.append(x)` | O(1)        |
| **Pop**     | `stack.pop()`     | O(1)        |
| **Peek**    | `stack[-1]`       | Look at top |
| **Iterate** | `for x in stack:` |             |

### Example

```python
stack = []
stack.append(1)
stack.append(2)
top = stack.pop()  # 2
```

---

# 📘 Queues (FIFO)

### Key Properties

* First In, First Out (FIFO).
* Use `collections.deque` for O(1) operations.

### Common Operations

| Operation   | Example       | Notes         |
| ----------- | ------------- | ------------- |
| **Enqueue** | `q.append(x)` | Add to right  |
| **Dequeue** | `q.popleft()` | Remove left   |
| **Peek**    | `q[0]`        | Front element |
| **Iterate** | `for x in q:` |               |

### Example

```python
from collections import deque
q = deque([1, 2])
q.append(3)        # [1,2,3]
front = q.popleft() # 1
```

---

# 📘 Heaps / Priority Queues (`heapq`)

### Key Properties

* Min-heap by default in Python.
* O(log n) insert/remove, O(1) peek min.
* Useful for scheduling, Dijkstra’s shortest path, top-K problems.

### Common Operations

| Operation     | Example                               | Notes            |
| ------------- | ------------------------------------- | ---------------- |
| **Create**    | `heap = [3,1,4]; heapq.heapify(heap)` | O(n)             |
| **Push**      | `heapq.heappush(heap, 2)`             | O(log n)         |
| **Pop (min)** | `heapq.heappop(heap)`                 | O(log n)         |
| **Peek**      | `heap[0]`                             | Smallest element |
| **Max-Heap**  | `heapq.heappush(heap, -val)`          | Store negatives  |

### Example

```python
import heapq
heap = [3, 1, 4]
heapq.heapify(heap)
heapq.heappush(heap, 2)
print(heapq.heappop(heap)) # 1
```