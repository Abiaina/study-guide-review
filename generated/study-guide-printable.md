# DevOps & Backend Study Guide - Complete Edition

*A comprehensive study guide covering DevOps, Chaos Engineering, and Backend Development fundamentals*

*Generated for printing and offline study*

---

## Table of Contents

### Core Fundamentals

- Data Structures Overview

- Algorithms & Data Structures

- Complex Data Structures (Trees, Graphs)

- Searching & Sorting Algorithms

- Sliding Window Algorithms

- Frontend Development

- Programming Languages & Tools


### System Design & Architecture

- System Design Problems

- Data Layer & Databases

- Design Patterns


### DevOps & Cloud

- CI/CD & Infrastructure

- Reliability Engineering (Internet Fundamentals, Observability, Chaos Engineering, Load Testing)


### Security & Compliance

- Security & Compliance


### Quick Reference & Cheat Sheets

- Comprehensive Cheat Sheet


---

# Core Fundamentals

## Data Structures Overview

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

### **Understanding Time Complexities**

**O(1) - Constant Time**
- **Indexing**: Direct memory access using offset calculation
- **Append (amortized)**: Most of the time it's O(1), but occasionally Python needs to reallocate memory and copy elements
- **Dictionary/Set lookup**: Hash function computes memory location directly

**O(n) - Linear Time**
- **Linear search**: Must examine each element until target is found
- **Insert/Delete at beginning**: All elements must shift to make room
- **Sorting**: Timsort is O(n log n) but can be O(n) for nearly sorted data

**O(log n) - Logarithmic Time**
- **Heap operations**: Tree structure allows efficient bubbling up/down
- **Binary search**: Each comparison eliminates half the remaining elements

### **Why "Amortized" O(1) for Append?**

Python lists use **dynamic arrays** that grow exponentially:
- Start with small capacity (e.g., 4 elements)
- When full, allocate 2x capacity and copy elements
- Most appends are O(1), occasional copies are O(n)
- **Average cost**: O(1) per operation over many operations

**Helper libraries in Python**

- `collections.deque` → O(1) pops/appends at both ends.
- `collections.Counter` → Fast frequency counting.
- `collections.defaultdict` → Cleaner hash maps with default values.
- `heapq` → Priority queue implementation.
- `bisect` → Binary search on sorted arrays.

### **Helper Libraries Worked Examples**

#### **collections.deque** - Double-ended queue
```python
from collections import deque

# Create deque
d = deque([1, 2, 3])           # O(n)
d.append(4)                     # O(1) - add to right
d.appendleft(0)                # O(1) - add to left
d.pop()                        # O(1) - remove from right
d.popleft()                    # O(1) - remove from left
d.rotate(1)                    # O(k) - rotate right by k positions
d.rotate(-1)                   # O(k) - rotate left by k positions

# Use cases: sliding window, BFS queue, palindrome checking
```

#### **collections.Counter** - Frequency counting
```python
from collections import Counter

# Count characters in string
freq = Counter("hello")         # Counter({'h': 1, 'e': 1, 'l': 2, 'o': 1})
freq['l']                      # 2
freq.most_common(2)            # [('l', 2), ('h', 1)] - top 2 most common

# Count list elements
nums = [1, 2, 2, 3, 2, 1]
count = Counter(nums)          # Counter({1: 2, 2: 3, 3: 1})

# Counter maintains insertion order (Python 3.7+)
# Keys appear in the order they were first encountered
# This is useful for predictable iteration order

# Arithmetic operations
c1 = Counter(['a', 'b', 'c'])
c2 = Counter(['b', 'c', 'd'])
c1 + c2                        # Counter({'a': 1, 'b': 2, 'c': 2, 'd': 1})
c1 - c2                        # Counter({'a': 1}) - only positive counts

# Converting Counter back to string/iterable
freq = Counter("leetcode")
print(freq)                     # Counter({'e': 3, 't': 1, 'c': 1, 'o': 1, 'd': 1, 'l': 1})

# Back to string using elements()
s = "".join(freq.elements())   # "leetccode" - elements() returns each char count times
print(s)                       # "leetccode"

# elements() returns an iterator with each element repeated by its count
elements_list = list(freq.elements())  # ['l', 'e', 'e', 'e', 't', 'c', 'o', 'd', 'e']
print(elements_list)

# Important: Counter iteration order is NOT sorted by frequency
# Use most_common() for frequency-sorted results
freq = Counter("hello")
print(list(freq))              # ['h', 'e', 'l', 'o'] - insertion order
print(freq.most_common())      # [('l', 2), ('h', 1), ('e', 1), 'o': 1)] - freq order

# CRITICAL: Counter equality (==) ignores insertion order and compares frequencies
# This is why Counter(s) == Counter(t) works for anagram problems!
```

# Use cases: anagram detection, frequency analysis, top-K elements
```

#### **Counter Behavior & Ordering**

```python
from collections import Counter

# Counter maintains insertion order (Python 3.7+)
freq = Counter("hello")
print(freq)                      # Counter({'h': 1, 'e': 1, 'l': 2, 'o': 1})
print(list(freq))                # ['h', 'e', 'l', 'o'] - insertion order
print(list(freq.keys()))         # ['h', 'e', 'l', 'o'] - same as above

# most_common() returns frequency-sorted results
print(freq.most_common())        # [('l', 2), ('h', 1), ('e', 1), ('o', 1)]
print(freq.most_common(2))       # [('l', 2), ('h', 1)] - top 2 by frequency

# Iteration order vs frequency order
for char, count in freq.items():
    print(f"{char}: {count}")    # h: 1, e: 1, l: 2, o: 1 (insertion order)

for char, count in freq.most_common():
    print(f"{char}: {count}")    # l: 2, h: 1, e: 1, o: 1 (frequency order)

# Important for anagram problems
s1, s2 = "hello", "olleh"
c1, c2 = Counter(s1), Counter(s2)
print(c1 == c2)                  # True - same character frequencies (equality ignores order)
print(list(c1) == list(c2))      # False - different insertion order (iteration follows order)

# Key insight: Counter equality compares frequencies, not insertion order
# This is why Counter(s) == Counter(t) works perfectly for anagram problems
```

#### **Counter Equality vs Iteration Order - Critical Distinction**

```python
from collections import Counter

s = "hello"
t = "olleh"

c1 = Counter(s)  # Counter({'h': 1, 'e': 1, 'l': 2, 'o': 1})
c2 = Counter(t)  # Counter({'o': 1, 'l': 2, 'e': 1, 'h': 1})

# EQUALITY COMPARISON (ignores insertion order)
print(c1 == c2)                  # True - same character frequencies
print(dict(c1) == dict(c2))      # True - same underlying dictionary

# ITERATION ORDER (follows insertion order)
print(list(c1))                  # ['h', 'e', 'l', 'o'] - from "hello"
print(list(c2))                  # ['o', 'l', 'e', 'h'] - from "olleh"
print(list(c1) == list(c2))      # False - different insertion order

# WHY THIS MATTERS FOR ANAGRAMS
def isAnagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)  # ✅ Works perfectly!

# The equality operator compares the mathematical content (frequencies),
# not the presentation order (insertion order)

### **Counter Behavior Summary**

| Operation | Behavior | Example | Use Case |
|-----------|----------|---------|----------|
| **`Counter(s) == Counter(t)`** | Compares frequencies, ignores order | `Counter("hello") == Counter("olleh")` → `True` | Anagram problems ✅ |
| **`list(Counter(s))`** | Returns keys in insertion order | `list(Counter("hello"))` → `['h', 'e', 'l', 'o']` | Iteration order |
| **`Counter(s).most_common()`** | Returns frequency-sorted list | `Counter("hello").most_common()` → `[('l', 2), ('h', 1), ...]` | Top-K elements |
| **`dict(Counter(s))`** | Returns underlying dictionary | `dict(Counter("hello"))` → `{'h': 1, 'e': 1, 'l': 2, 'o': 1}` | Dictionary operations |
| **`Counter(s).elements()`** | Returns elements repeated by count | `list(Counter("hello").elements())` → `['h', 'e', 'l', 'l', 'o']` | Convert back to iterable |
| **`"".join(Counter(s).elements())`** | Convert Counter back to string | `"".join(Counter("hello").elements())` → `"hello"` | String reconstruction |

**Key Takeaway**: For anagram problems, use `Counter(s) == Counter(t)` - it works perfectly regardless of insertion order!

#### **Complete Counter Cycle Example**

```python
from collections import Counter

# String → Counter → String cycle
original = "leetcode"
freq = Counter(original)                    # Counter({'e': 3, 't': 1, 'c': 1, 'o': 1, 'd': 1, 'l': 1})
reconstructed = "".join(freq.elements())    # "leetccode" - back to string

print(f"Original: {original}")
print(f"Counter: {freq}")
print(f"Reconstructed: {reconstructed}")

# Note: elements() maintains insertion order, so reconstructed may differ from original
# But the character frequencies are identical!

# Practical use case: Normalize strings for comparison
def normalize_string(s):
    return "".join(sorted(Counter(s).elements()))

s1, s2 = "hello", "olleh"
print(normalize_string(s1))  # "ehllo"
print(normalize_string(s2))  # "ehllo"
print(normalize_string(s1) == normalize_string(s2))  # True
```
```

#### **collections.defaultdict** - Dictionaries with default values
```python
from collections import defaultdict

# Group by key
groups = defaultdict(list)
for item, category in [('apple', 'fruit'), ('banana', 'fruit'), ('carrot', 'veg')]:
    groups[category].append(item)
# Result: {'fruit': ['apple', 'banana'], 'veg': ['carrot']}

# Count with default 0
counts = defaultdict(int)
for char in "hello":
    counts[char] += 1          # No need to check if key exists
# Result: {'h': 1, 'e': 1, 'l': 2, 'o': 1}

# Nested defaultdict
nested = defaultdict(lambda: defaultdict(list))
nested['group1']['subgroup'].append('item')

# Use cases: grouping, counting, nested data structures
```

#### **heapq** - Priority queue operations
```python
import heapq

# Create min-heap
heap = [3, 1, 4, 1, 5]
heapq.heapify(heap)            # O(n) - convert list to heap
heapq.heappush(heap, 2)        # O(log n) - add element
smallest = heapq.heappop(heap) # O(log n) - remove smallest

# Max-heap (store negatives)
max_heap = []
heapq.heappush(max_heap, -5)   # Store -5 for max-heap
largest = -heapq.heappop(max_heap) # Get 5 back

# Top-K elements
def top_k(nums, k):
    return heapq.nlargest(k, nums)  # O(n log k)

# Use cases: Dijkstra's algorithm, top-K problems, scheduling
```

#### **bisect** - Binary search on sorted arrays
```python
import bisect

arr = [1, 3, 5, 7, 9]

# Find insertion point
pos = bisect.bisect_left(arr, 4)   # 2 - where 4 would go
pos = bisect.bisect_right(arr, 5)   # 3 - after last 5

# Insert in sorted order
bisect.insort_left(arr, 4)         # [1, 3, 4, 5, 7, 9]
bisect.insort_right(arr, 5)         # [1, 3, 4, 5, 5, 7, 9]

# Use cases: maintaining sorted lists, range queries, binary search
```

---

## **2. Strings & Arrays**

### Common Patterns

- **Two pointers**: Used for palindromes, merging sorted arrays, sliding windows.
- **Sliding window**: Substring/array problems (`longest substring`, `max sum subarray`).
- **Prefix sums**: Range queries, subarray sums.
- **Hash maps (dict)**: Fast lookup for duplicates, anagrams, substrings.

### Practice Problems

1. Reverse a string → O(n).
2. Check palindrome (ignore punctuation, spaces).
3. Longest substring without repeating characters (sliding window).
4. Two Sum (hash map, O(n)).
5. Maximum subarray (Kadane’s algorithm, O(n)).

### **String Properties & Problem-Solving Approaches**

#### **String Immutability**
- **Strings are immutable** in Python - cannot be modified in place
- **Concatenation**: Use `''.join(parts)` for efficiency in loops
- **Slicing**: Creates new string copies - `s[i:j]` is O(k) where k = j-i
- **Common operations**: `split()`, `join()`, `strip()`, `replace()`, `find()`

#### **String Problem Types & Approaches**

| Problem Type | Approach | Time Complexity | Example Problems |
|-------------|----------|----------------|------------------|
| **Palindrome** | Two pointers from ends | O(n) | Valid Palindrome, Longest Palindromic Substring |
| **Anagram** | Counter or sorted comparison | O(n) | Valid Anagram, Group Anagrams |
| **Substring Search** | Sliding window or KMP | O(n) | Longest Substring Without Repeating Characters |
| **String Matching** | Hash map or trie | O(n) | Ransom Note, Isomorphic Strings |
| **String Manipulation** | Build new string | O(n) | Reverse String, Encode/Decode |

### **String Operations Table**

| Operation | Example | Time Complexity | Space Complexity | Notes |
|-----------|---------|-----------------|------------------|-------|
| **Find** | `s.find("sub")` | O(n) | O(1) | Returns index or -1 |
| **Index** | `s.index("sub")` | O(n) | O(1) | Returns index or raises ValueError |
| **Count** | `s.count("char")` | O(n) | O(1) | Count occurrences |
| **Replace** | `s.replace("old", "new")` | O(n) | O(n) | Returns new string |
| **Split** | `s.split()` | O(n) | O(n) | Returns list of substrings |
| **Join** | `"".join(list)` | O(n) | O(n) | Concatenate list elements |
| **Upper/Lower** | `s.upper()`, `s.lower()` | O(n) | O(n) | Returns new string |
| **Strip** | `s.strip()` | O(n) | O(n) | Remove whitespace |
| **Startswith/Endswith** | `s.startswith("pre")` | O(k) | O(1) | k = length of prefix/suffix |
| **Isalpha/Isdigit** | `s.isalpha()` | O(n) | O(1) | Check character types |
| **Slice** | `s[i:j]` | O(k) | O(k) | k = j-i, creates new string |
| **Membership** | `"sub" in s` | O(n) | O(1) | Check if substring exists |

### **Common Patterns Table**

| Pattern | When to Use | Time Complexity | Space Complexity | Example Problems |
|---------|-------------|-----------------|------------------|-------------------|
| **Two Pointers** | Sorted arrays, palindromes, merging | O(n) | O(1) | Two Sum (sorted), Valid Palindrome |
| **Sliding Window** | Subarray/substring problems | O(n) | O(k) | Longest Substring, Max Sum Subarray |
| **Prefix Sums** | Range queries, subarray sums | O(n) | O(n) | Subarray Sum Equals K |
| **Hash Maps** | Fast lookup, duplicates, anagrams | O(n) | O(n) | Two Sum, Group Anagrams |
| **Binary Search** | Sorted arrays, optimization | O(log n) | O(1) | Search in Rotated Array |

### **Practice Problems & Learning Goals**

**Refer to Week 1 of your study plan for specific problems:**
- **Arrays/Strings/Hash Maps**: 10 problems with direct LeetCode links
- **Must master**: two-pointer, hash map counting, substring search, anagram grouping
- **DFS/BFS**: 4 problems focusing on recursive DFS, iterative BFS with queue, visited set usage
- **Sliding Window**: 3 problems covering fixed window sum, min/max substring, variable window patterns

**Key Learning Objectives:**
1. **String immutability** - understand when to use `join()` vs `+`
2. **Hash map patterns** - frequency counting, anagram detection, two-sum
3. **Two pointer techniques** - palindrome checking, sorted array merging
4. **Sliding window** - longest substring without repeats, max sum subarray
5. **Time/space complexity** - know when each approach is optimal

---

Compare Core Data Structures

| Operation | List | Dict | Set | Queue/Deque |
|-----------|------|------|-----|--------------|
| `len()` | ✅ | ✅ | ✅ | ✅ |
| `in` (membership) | O(n) | O(1) | O(1) | O(n) |
| `pop()` | End only (O(1)) | By key (O(1) avg) | Arbitrary O(1) | Left/right O(1) |
| `clear()` | ✅ | ✅ | ✅ | ✅ |
| `sorted()` | ✅ | On `.items()` (O(n log n)) | ✅ | Convert to list first |
| Iteration | `for x in list` | `for k,v in dict.items()` | `for x in set` | `for x in deque` |

---

# Arrays & Lists (Python Focus)

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
| **Sort (copy)**     | `sorted(nums)`                    | Returns new list, O(n log n)   |
| **Reverse**         | `nums.reverse()`                  | In-place, O(n)                 |
| **Reverse (copy)**  | `nums[::-1]`                      | Returns new list, O(n)         |
| **Clear**           | `nums.clear()`                    | Remove all elements            |
| **Find**            | `nums.index(3)`                   | Returns first index, O(n)      |
| **Count**           | `nums.count(3)`                   | Count occurrences, O(n)        |
| **Enumerate**       | `enumerate(nums)`                 | Index + value pairs, O(n)      |
| **Zip**             | `zip(nums, other)`                | Pair elements, O(min(n,m))     |
| **Range**           | `range(5)`                        | Number sequence, O(n)          |
| **Membership**      | `3 in nums`                       | Check if exists, O(n)          |
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

#### Sorting & Reversing

```python
# In-place sorting (modifies original list)
nums.sort()                    # ascending: [1,2,3,4,5]
nums.sort(reverse=True)        # descending: [5,4,3,2,1]
nums.sort(key=lambda x: x%2)   # custom key: evens first

# Copy sorting (returns new list)
sorted_copy = sorted(nums)     # ascending copy
sorted_desc = sorted(nums, reverse=True)  # descending copy
sorted_custom = sorted(nums, key=len)     # custom key copy

# Reversing
nums.reverse()                 # in-place: [5,4,3,2,1]
reversed_copy = nums[::-1]     # copy: [1,2,3,4,5]
reversed_copy = list(reversed(nums))  # another copy method

# Time/Space Complexity
# sort(): O(n log n) time, O(1) space (in-place)
# sorted(): O(n log n) time, O(n) space (creates copy)
# reverse(): O(n) time, O(1) space (in-place)
# [::-1]: O(n) time, O(n) space (creates copy)
```

#### Helper Functions & Collections

```python
from collections import deque, Counter, defaultdict

# Queue operations (O(1) at both ends)
queue = deque([1, 2, 3])
queue.append(4)        # add to right
queue.appendleft(0)    # add to left
queue.pop()           # remove from right
queue.popleft()       # remove from left

# Frequency counting
freq = Counter([1, 2, 2, 3, 2, 1])  # Counter({1: 2, 2: 3, 3: 1}) - insertion order
most_common = freq.most_common(2)    # [(2, 3), (1, 2)] - frequency order
# Note: Counter maintains insertion order, not frequency order
# Use most_common() to get frequency-sorted results

# Grouping with defaultdict
groups = defaultdict(list)
for item, category in [('a', 'vowel'), ('b', 'consonant'), ('e', 'vowel')]:
    groups[category].append(item)
# Result: {'vowel': ['a', 'e'], 'consonant': ['b']}

# Built-in helpers
nums = [1, 2, 3, 4, 5]
len(nums)              # 5 - length
sum(nums)              # 15 - sum
max(nums)              # 5 - maximum
min(nums)              # 1 - minimum
all(x > 0 for x in nums)  # True - all positive
any(x > 3 for x in nums)  # True - any > 3

# Essential built-ins for problem solving
enumerate(nums)        # [(0,1), (1,2), (2,3), (3,4), (4,5)] - index + value
zip(nums, ['a','b','c'])  # [(1,'a'), (2,'b'), (3,'c')] - pair elements
range(5)               # [0, 1, 2, 3, 4] - number sequence
range(1, 6)            # [1, 2, 3, 4, 5] - start to end
range(0, 10, 2)        # [0, 2, 4, 6, 8] - with step

# Finding elements
nums.index(3)          # 2 - first index of value (raises ValueError if not found)
nums.count(2)          # 1 - count occurrences
3 in nums              # True - membership test

# String operations
s = "hello world"
s.find("world")        # 6 - first index of substring (-1 if not found)
s.rfind("l")           # 9 - last index of substring
s.index("world")       # 6 - first index (raises ValueError if not found)
s.count("l")           # 3 - count occurrences
"world" in s           # True - substring membership
```

---

## **Essential Built-in Functions for Problem Solving**

### **Index & Enumerate Operations**

| Function | Purpose | Time Complexity | Example | Use Cases |
|----------|---------|-----------------|---------|-----------|
| `enumerate(iterable)` | Get index + value pairs | O(n) | `list(enumerate([1,2,3]))` → `[(0,1), (1,2), (2,3)]` | Two pointers, sliding window |
| `list.index(value)` | Find first index of value | O(n) | `[1,2,3].index(2)` → `1` | Search problems |
| `str.find(substring)` | Find substring index | O(n) | `"hello".find("ll")` → `2` | String matching |
| `str.rfind(substring)` | Find last substring index | O(n) | `"hello".rfind("l")` → `3` | Last occurrence |
| `str.index(substring)` | Find substring (raises if not found) | O(n) | `"hello".index("ll")` → `2` | When you need exceptions |

### **Range & Iteration Helpers**

```python
# Range variations
range(5)                    # [0, 1, 2, 3, 4] - 0 to n-1
range(1, 6)                 # [1, 2, 3, 4, 5] - start to end-1
range(0, 10, 2)             # [0, 2, 4, 6, 8] - with step
range(10, 0, -1)            # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1] - reverse

# Enumerate for index + value
nums = [10, 20, 30, 40]
for i, num in enumerate(nums):
    print(f"Index {i}: {num}")  # Index 0: 10, Index 1: 20, etc.

# Zip for pairing
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name} is {age}")  # Alice is 25, Bob is 30, etc.
```

### **Search & Count Operations**

```python
# List operations
nums = [1, 2, 3, 2, 4, 2]
nums.index(2)               # 1 - first occurrence
nums.count(2)               # 3 - count occurrences
2 in nums                   # True - membership test

# String operations
s = "hello world"
s.find("world")             # 6 - first index (-1 if not found)
s.rfind("l")                # 9 - last index
s.index("world")            # 6 - first index (raises if not found)
s.count("l")                # 3 - count occurrences
"world" in s                # True - substring membership

# Safe search patterns
try:
    idx = nums.index(5)     # Will raise ValueError
except ValueError:
    idx = -1                # Handle not found case

# Or use find for strings (returns -1)
idx = s.find("xyz")         # -1 if not found
```

### **Common Problem-Solving Patterns**

```python
# Two pointers with enumerate
def two_sum(nums, target):
    for i, num in enumerate(nums):
        for j in range(i + 1, len(nums)):
            if num + nums[j] == target:
                return [i, j]

# Sliding window with enumerate
def longest_substring(s):
    char_map = {}
    start = 0
    max_len = 0
    
    for end, char in enumerate(s):
        if char in char_map and char_map[char] >= start:
            start = char_map[char] + 1
        char_map[char] = end
        max_len = max(max_len, end - start + 1)
    
    return max_len

# Frequency counting with enumerate
def group_anagrams(strs):
    groups = {}
    for i, s in enumerate(strs):
        key = ''.join(sorted(s))
        if key not in groups:
            groups[key] = []
        groups[key].append(i)  # Store indices instead of strings
    return list(groups.values())
```

### **Additional Useful Built-ins**

```python
# String manipulation
s = "Hello World"
s.upper()               # "HELLO WORLD" - convert to uppercase
s.lower()               # "hello world" - convert to lowercase
s.strip()               # "Hello World" - remove whitespace
s.split()               # ['Hello', 'World'] - split by whitespace
s.split(',')            # ['Hello World'] - split by delimiter
s.replace('l', 'x')     # "Hexxo Worxd" - replace characters
s.startswith('He')      # True - check prefix
s.endswith('ld')        # True - check suffix
s.isalpha()             # False - check if all alphabetic
s.isdigit()             # False - check if all digits
s.isalnum()             # False - check if alphanumeric

# List/Array utilities
nums = [3, 1, 4, 1, 5]
sorted(nums)            # [1, 1, 3, 4, 5] - returns new sorted list
reversed(nums)          # iterator in reverse order
list(reversed(nums))    # [5, 1, 4, 1, 3] - convert to list
nums[::-1]              # [5, 1, 4, 1, 3] - reverse slice (copy)

# Mathematical operations
abs(-5)                 # 5 - absolute value
pow(2, 3)               # 8 - power (2^3)
divmod(10, 3)           # (3, 1) - quotient and remainder
round(3.14159, 2)       # 3.14 - round to 2 decimal places

# Type conversion
int("123")              # 123 - string to int
str(123)                # "123" - int to string
list("hello")           # ['h', 'e', 'l', 'l', 'o'] - string to list
''.join(['h','e','l','l','o'])  # "hello" - list to string

# Boolean operations
bool(0)                 # False - falsy values
bool(1)                 # True - truthy values
bool("")                # False - empty string is falsy
bool("hello")           # True - non-empty string is truthy
```

---

# Dictionaries (Python `dict`)

### Key Properties

- Key-value store (hash table under the hood).
- Keys must be **hashable** (immutable types: str, int, tuple).
- Average-case operations: O(1) lookup, insert, delete.
- Worst-case O(n) (rare, due to hash collisions).

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
| **Merge**          | `d1.update(d2)`          | In-place merge             |
| **Copy**           | `d.copy()`               | Shallow copy               |
| **Set default**    | `d.setdefault(k, v)`      | Set if missing             |
| **Enumerate**      | `enumerate(d.items())`    | Index + key-value pairs    |
| **Zip**            | `zip(d.keys(), d.values())` | Pair keys and values      |

### **Dictionary Operations Complexity**

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|-----------------|------------------|-------|
| **Access** (`d[key]`) | O(1) average | O(1) | KeyError if missing |
| **Safe Access** (`d.get(key)`) | O(1) average | O(1) | Returns None if missing |
| **Insert/Update** (`d[key] = value`) | O(1) average | O(1) | Insert or overwrite |
| **Delete** (`del d[key]`) | O(1) average | O(1) | KeyError if missing |
| **Pop** (`d.pop(key)`) | O(1) average | O(1) | Returns value or default |
| **Membership** (`key in d`) | O(1) average | O(1) | Boolean check |
| **Length** (`len(d)`) | O(1) | O(1) | Number of key-value pairs |
| **Iteration** (`for k in d`) | O(n) | O(1) | Iterate over keys |
| **Items** (`d.items()`) | O(n) | O(n) | Returns view of key-value pairs |
| **Keys** (`d.keys()`) | O(n) | O(n) | Returns view of keys |
| **Values** (`d.values()`) | O(n) | O(n) | Returns view of values |
| **Update** (`d.update(other)`) | O(m) | O(1) | m = size of other dict |
| **Copy** (`d.copy()`) | O(n) | O(n) | Shallow copy |
| **Clear** (`d.clear()`) | O(1) | O(1) | Remove all items |

---

### Special Methods

- `.keys()` → view of all keys (iterable).
- `.values()` → view of all values.
- `.items()` → iterable of `(key, value)` tuples.
- `.update({...})` → bulk add/update.
- `.popitem()` → remove _last_ inserted (Python ≥ 3.7 keeps insertion order).

---

### Example Snippets

#### Iteration & Access

```python
d = {"a": 1, "b": 2, "c": 3}

# Safe access patterns
value = d.get("a", 0)      # Safe access with default
value = d.setdefault("d", 4)  # Set default if missing

# Iteration patterns
for k in d:                # keys only
    print(k)

for v in d.values():       # values only
    print(v)

for k, v in d.items():     # key-value pairs
    print(k, v)

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
filtered = {k: v for k, v in d.items() if v > 1}  # Filter by value
```

#### Adding & Removing

```python
# Single operations
d["d"] = 4            # add/update
d.update({"e": 5, "f": 6})    # bulk add/update
del d["a"]            # delete (raises if missing)
d.pop("b", None)      # delete with default

# Advanced operations
d.setdefault("g", 7)  # set if missing, return value
d.copy()              # shallow copy
```

#### Sorting & Merging

```python
# Sort by key (returns list of tuples)
sorted_by_key = sorted(d.items())    # [('c', 3), ('d', 4), ('e', 5)]

# Sort by value
sorted_by_value = sorted(d.items(), key=lambda x: x[1])

# Sort by custom key
sorted_by_len = sorted(d.items(), key=lambda x: len(x[0]))

# Merging dictionaries
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
d1.update(d2)         # d1 = {"a": 1, "b": 3, "c": 4} (b overwritten)
merged = {**d1, **d2}  # Python 3.5+ unpacking
```

#### Helper Functions & Collections

```python
from collections import defaultdict, Counter

# defaultdict - automatic default values
dd = defaultdict(list)
dd['group1'].append('item1')  # No need to check if key exists

# Counter - frequency counting
freq = Counter(['a', 'b', 'a', 'c', 'b', 'a'])
# Counter({'a': 3, 'b': 2, 'c': 1}) - insertion order maintained
most_common = freq.most_common(2)  # [('a', 3), ('b', 2)] - frequency order

# Convert Counter back to original elements
elements = list(freq.elements())     # ['a', 'a', 'a', 'b', 'b', 'c'] - each element repeated by count
reconstructed = "".join(freq.elements())  # "aaabbc" - back to string

# Note: Counter iteration follows insertion order, not frequency order
# BUT: Counter equality (==) ignores insertion order and compares frequencies
# This makes Counter perfect for anagram problems: Counter(s) == Counter(t)

# Built-in helpers
d = {"a": 1, "b": 2, "c": 3}
len(d)                  # 3 - number of key-value pairs
all(v > 0 for v in d.values())  # True - all values positive
any(v > 2 for v in d.values())  # True - any value > 2
```

---

# Sets (`set` in Python)

### Key Properties

- Unordered, unique elements only.
- Backed by hash table → O(1) avg lookup/insert/delete.
- No duplicates, no indexing.

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

- `.update(iterable)` → bulk add.
- `.issubset()`, `.issuperset()`.
- `.symmetric_difference()`.

### Examples

```python
s = {1, 2, 3}
s.add(4)             # {1,2,3,4}
s.remove(2)          # {1,3,4}
print(3 in s)        # True
print(s.union({5}))  # {1,3,4,5}
```

---

# Stacks (LIFO)

### Key Properties

- Last In, First Out (LIFO).
- Implement with `list` or `collections.deque`.

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

# Queues (FIFO)

### Key Properties

- First In, First Out (FIFO).
- Use `collections.deque` for O(1) operations.

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

# Heaps / Priority Queues (`heapq`)

### Key Properties

- Min-heap by default in Python.
- O(log n) insert/remove, O(1) peek min.
- Useful for scheduling, Dijkstra’s shortest path, top-K problems.

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

---

## Algorithms & Data Structures

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

---

## Complex Data Structures (Trees, Graphs)

### Key Properties

- A **tree** is a connected graph with no cycles.
- **Binary Tree**: each node has up to 2 children.
- **BST (Binary Search Tree)**: left < root < right.
- **Common Operations**: traversal, insertion, search, min/max, depth/height.

### Common Tree Problems
- **Tree Construction**: Build tree from array, string, or other data
- **Tree Validation**: Check if tree is BST, balanced, or symmetric
- **Tree Traversal**: Pre-order, in-order, post-order, level-order
- **Tree Manipulation**: Insert, delete, invert, serialize/deserialize
- **Tree Queries**: Find LCA, path sum, diameter, height

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

## Common Tree Problems & Solutions

### Validate Binary Search Tree

**Problem**: Check if a binary tree is a valid BST.

**Approach**: Use in-order traversal - BST should produce sorted values.

**Python Implementation**:
```python
def is_valid_bst(root):
    def inorder(node, prev):
        if not node:
            return True
        
        # Check left subtree
        if not inorder(node.left, prev):
            return False
        
        # Check current node (should be > previous)
        if prev[0] is not None and node.val <= prev[0]:
            return False
        prev[0] = node.val
        
        # Check right subtree
        return inorder(node.right, prev)
    
    prev = [None]  # Use list to store previous value
    return inorder(root, prev)
```

### Serialize and Deserialize Binary Tree

**Problem**: Convert tree to string and back.

**Approach**: Use pre-order traversal with null markers.

**Python Implementation**:
```python
def serialize(root):
    if not root:
        return "null"
    return str(root.val) + "," + serialize(root.left) + "," + serialize(root.right)

def deserialize(data):
    def build_tree(values):
        if not values or values[0] == "null":
            values.pop(0)
            return None
        
        root = TreeNode(int(values.pop(0)))
        root.left = build_tree(values)
        root.right = build_tree(values)
        return root
    
    values = data.split(",")
    return build_tree(values)
```

### Lowest Common Ancestor (LCA)

**Problem**: Find the lowest common ancestor of two nodes.

**Approach**: Use recursive search - LCA is where paths diverge.

**Python Implementation**:
```python
def lowest_common_ancestor(root, p, q):
    if not root or root == p or root == q:
        return root
    
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    
    if left and right:
        return root  # Found LCA
    return left or right  # Return the one that's not None
```

### Path Sum

**Problem**: Check if there's a path from root to leaf with given sum.

**Approach**: Use DFS with sum tracking.

**Python Implementation**:
```python
def has_path_sum(root, target_sum):
    if not root:
        return False
    
    # Check if we're at a leaf
    if not root.left and not root.right:
        return root.val == target_sum
    
    # Recursively check left and right subtrees
    remaining = target_sum - root.val
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)
```

### Tree Diameter

**Problem**: Find the longest path between any two nodes.

**Approach**: For each node, find the longest path through it.

**Python Implementation**:
```python
def diameter_of_binary_tree(root):
    def height_and_diameter(node):
        if not node:
            return 0, 0
        
        left_height, left_diameter = height_and_diameter(node.left)
        right_height, right_diameter = height_and_diameter(node.right)
        
        # Current height
        current_height = max(left_height, right_height) + 1
        
        # Current diameter (through current node)
        current_diameter = left_height + right_height
        
        # Max diameter (either through current node or in subtrees)
        max_diameter = max(current_diameter, left_diameter, right_diameter)
        
        return current_height, max_diameter
    
    _, diameter = height_and_diameter(root)
    return diameter
```

---

# Graphs

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

---

## Searching & Sorting Algorithms

---

# 📘 Sorting Algorithms

### Key Properties

- Sorting is one of the most common algorithmic primitives.
- Python’s built-in `.sort()` and `sorted()` use **Timsort** (O(n log n), stable, adaptive to partially-sorted input).

### Common Algorithms

| Algorithm      | Time (avg) | Time (worst) | Space    | Stable? | Notes                                  |
| -------------- | ---------- | ------------ | -------- | ------- | -------------------------------------- |
| Bubble Sort    | O(n²)      | O(n²)        | O(1)     | Yes     | Educational, rarely used               |
| Insertion Sort | O(n²)      | O(n²)        | O(1)     | Yes     | Good for small or nearly sorted arrays |
| Merge Sort     | O(n log n) | O(n log n)   | O(n)     | Yes     | Divide & conquer, stable               |
| Quick Sort     | O(n log n) | O(n²)        | O(log n) | No      | In-place, fast in practice             |
| Heap Sort      | O(n log n) | O(n log n)   | O(1)     | No      | Uses heap, in-place                    |

---

### Example: Merge Sort (Divide & Conquer)

**Pseudocode**

```
merge_sort(arr):
    if length <= 1: return arr
    split arr into left and right
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)
    return merge(left_sorted, right_sorted)

merge(left, right):
    result = []
    while both not empty:
        take smaller front element
    append remaining
    return result
```

**Python**

```python
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr)//2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    res, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
    res.extend(left[i:]); res.extend(right[j:])
    return res
```

---

### Example: Quick Sort

```python
def quicksort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)
```

---

# 📘 Searching Algorithms

### Linear Search

- O(n).
- Use when data is unsorted.

```python
def linear_search(arr, target):
    for i, x in enumerate(arr):
        if x == target: return i
    return -1
```

### Binary Search

**What is Binary Search?**
Binary search is an efficient algorithm for finding a target element in a **sorted array**. It works by repeatedly dividing the search interval in half, eliminating half of the remaining elements in each step.

**When to Use Binary Search:**
1. **Array is sorted** (or can be made sorted)
2. **Looking for a specific value** or **finding insertion point**
3. **Need O(log n) time complexity** instead of O(n) linear search
4. **Search space can be divided in half** at each step

**Key Insight**: Each comparison eliminates half of the remaining search space, making it extremely efficient.

**Core Algorithm**:
```
1. Set left = 0, right = n-1
2. While left <= right:
   - mid = (left + right) // 2
   - If arr[mid] == target: return mid
   - If arr[mid] < target: left = mid + 1
   - If arr[mid] > target: right = mid - 1
3. Return -1 (not found)
```

**Why O(log n)?**
- Each iteration eliminates half the remaining elements
- If you start with n elements, after k iterations you have n/2^k elements
- When n/2^k = 1, you've found the element
- Solving: k = log₂(n)

**Python Implementation**:
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Not found

# Example
arr = [1, 3, 5, 7, 9, 11, 13, 15]
target = 7
result = binary_search(arr, target)
print(f"Found {target} at index {result}")  # Output: Found 7 at index 3
```

### Variants of Binary Search

- **First/Last Occurrence**: keep searching left/right after finding target.
- **Search Insert Position**: return index even if not found.
- **Rotated Sorted Array**: check which half is sorted, then recurse/iterate.

---

## Linear Search

- Works on unsorted arrays.
- Scans each element one by one until it finds the target or reaches the end.

**Pseudocode:**

```
# Start from the beginning of the array
for index from 0 to length(arr)-1:

    # Compare current element with the target
    if arr[index] == target:

        # If found, return its position
        return index

# If the loop finishes, target was not found
return -1
```

---

## Binary Search

- Works only on **sorted arrays**.
- Repeatedly halves the search range until the target is found or the search space is empty.

**Pseudocode:**

```
# Initialize search range
left = 0
right = length(arr) - 1

# Continue until the range collapses
while left <= right:

    # Find the middle index
    mid = (left + right) // 2

    # Check if the middle element is the target
    if arr[mid] == target:
        return mid

    # If target is larger, discard left half
    elif arr[mid] < target:
        left = mid + 1

    # If target is smaller, discard right half
    else:
        right = mid - 1

# Target not found
return -1
```

---

## First Occurrence (Binary Search Variant)

- Returns the **first position** of target in a sorted array with duplicates.

**Pseudocode:**

```
# Initialize result as not found
result = -1
left = 0
right = length(arr) - 1

while left <= right:

    # Find the middle index
    mid = (left + right) // 2

    # If target found, store result and continue left
    if arr[mid] == target:
        result = mid
        right = mid - 1

    # If target is larger, move to right half
    elif arr[mid] < target:
        left = mid + 1

    # Otherwise, move to left half
    else:
        right = mid - 1

# Return the first index where target appeared
return result
```

---

## Last Occurrence (Binary Search Variant)

- Returns the **last position** of target in a sorted array with duplicates.

**Pseudocode:**

```
# Initialize result as not found
result = -1
left = 0
right = length(arr) - 1

while left <= right:

    # Find the middle index
    mid = (left + right) // 2

    # If target found, store result and continue right
    if arr[mid] == target:
        result = mid
        left = mid + 1

    # If target is larger, move to right half
    elif arr[mid] < target:
        left = mid + 1

    # Otherwise, move to left half
    else:
        right = mid - 1

# Return the last index where target appeared
return result
```

---

## Search Insert Position

- **What it does:**

  - In a sorted array, return the index of the target if found.
  - If not found, return the index where it _should_ be inserted to keep order.
  - Useful for problems like placing an element in a sorted list.

**Pseudocode:**

```
# Initialize range
left = 0
right = length(arr) - 1

while left <= right:

    # Find midpoint
    mid = (left + right) // 2

    # If exact match found, return position
    if arr[mid] == target:
        return mid

    # If target is larger, search right half
    elif arr[mid] < target:
        left = mid + 1

    # Otherwise, search left half
    else:
        right = mid - 1

# If not found, left is the correct insert position
return left
```

---

## Search in Rotated Sorted Array

- **What it does:**

  - Array is sorted but rotated (e.g., `[4,5,6,7,0,1,2]`).
  - Must first decide which half is sorted, then apply binary search accordingly.
  - Runs in O(log n).

**Pseudocode:**

```
left = 0
right = length(arr) - 1

while left <= right:
    mid = (left + right) // 2

    # If target found
    if arr[mid] == target:
        return mid

    # Check if left half is sorted
    if arr[left] <= arr[mid]:
        # If target is in this range
        if arr[left] <= target < arr[mid]:
            right = mid - 1
        else:
            left = mid + 1

    # Otherwise, right half must be sorted
    else:
        # If target is in this range
        if arr[mid] < target <= arr[right]:
            left = mid + 1
        else:
            right = mid - 1

# Not found
return -1
```

---

## Binary Search on Answer (a.k.a. "Search Space Reduction")

- **What it does:**

  - Used when the solution isn’t an index but a value that can be validated (e.g., minimum capacity, smallest speed, max/min feasible answer).
  - Apply binary search over the **range of possible answers**, checking feasibility with a helper function.

**Pseudocode (general template):**

```
# Search over possible range
left = minimum_possible_value
right = maximum_possible_value

while left < right:
    mid = (left + right) // 2

    # Check if mid is a valid solution
    if is_valid(mid):
        # Try smaller values
        right = mid
    else:
        # Must try larger values
        left = mid + 1

# Final left is the answer
return left
```

**Examples where it’s used:**

- Minimum capacity to ship packages within D days.
- Minimum eating speed (Koko eating bananas problem).
- Maximum minimum distance in placing items.

---

---

## Sliding Window Algorithms

## **What is a Sliding Window?**

A sliding window is a technique for solving array/string problems where you maintain a subset of elements (the "window") that slides through the array to find the optimal solution. Think of it like a camera lens that moves across a scene, focusing on different parts one at a time.

## **Why Use Sliding Window?**

1. **Efficiency**: Often provides O(n) solutions instead of O(n²) brute force approaches
2. **Natural Fit**: Perfect for problems involving contiguous subarrays/substrings
3. **Memory Efficient**: Usually requires only O(1) or O(k) extra space
4. **Pattern Recognition**: Helps identify when problems can be solved with this approach

## **Common Problem Types**

- **Fixed Size**: Find something of a specific size (e.g., subarray of length k)
- **Variable Size**: Find smallest/largest subarray satisfying a condition
- **Contiguous Elements**: Problems where order and adjacency matter
- **Range Queries**: Finding optimal ranges that meet certain criteria

---

## 1. Two Types of Sliding Windows

### Fixed-Size Window
- **Window size stays constant** as it slides
- **Use case**: Find something of a specific size (e.g., subarray of length k)
- **Pattern**: Expand to size k, then slide

### Variable-Size Window
- **Window size changes** based on conditions
- **Use case**: Find smallest/largest subarray satisfying a condition
- **Pattern**: Expand until condition met, then contract

---

## 2. Fixed-Size Window Examples

### Maximum Sum Subarray of Size K

**Problem**: Find the maximum sum of a subarray of size k.

**Approach**: 
1. Calculate sum of first k elements
2. Slide window by subtracting first element and adding next element
3. Keep track of maximum sum

**Pseudocode**:
```
# Calculate sum of first window
window_sum = sum of first k elements
max_sum = window_sum

# Slide window
for i from k to n-1:
    # Remove first element, add new element
    window_sum = window_sum - arr[i-k] + arr[i]
    max_sum = max(max_sum, window_sum)

return max_sum
```

**Python Implementation**:
```python
def max_sum_subarray_k(arr, k):
    if len(arr) < k:
        return 0
    
    # Calculate sum of first window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide window
    for i in range(k, len(arr)):
        # Remove first element, add new element
        window_sum = window_sum - arr[i-k] + arr[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum

# Example
arr = [1, 4, 2, 10, 2, 3, 1, 0, 20]
k = 4
print(max_sum_subarray_k(arr, k))  # Output: 24 (subarray [2, 10, 2, 3])
```

**Time Complexity**: O(n) - each element is added and removed once
**Space Complexity**: O(1) - only using a few variables

---

### First Negative Number in Every Window of Size K

**Problem**: For every window of size k, find the first negative number.

**Approach**: Use a queue to track negative numbers in the current window.

**Python Implementation**:
```python
from collections import deque

def first_negative_in_window(arr, k):
    if len(arr) < k:
        return []
    
    result = []
    neg_queue = deque()
    
    # Process first window
    for i in range(k):
        if arr[i] < 0:
            neg_queue.append(i)
    
    # First window result
    if neg_queue:
        result.append(arr[neg_queue[0]])
    else:
        result.append(0)
    
    # Slide window
    for i in range(k, len(arr)):
        # Remove elements outside current window
        while neg_queue and neg_queue[0] <= i - k:
            neg_queue.popleft()
        
        # Add new negative number
        if arr[i] < 0:
            neg_queue.append(i)
        
        # Result for current window
        if neg_queue:
            result.append(arr[neg_queue[0]])
        else:
            result.append(0)
    
    return result

# Example
arr = [12, -1, -7, 8, -15, 30, 16, 28]
k = 3
print(first_negative_in_window(arr, k))  # Output: [-1, -1, -7, -15, -15, 0]
```

---

## 3. Variable-Size Window Examples

### Longest Substring Without Repeating Characters

**Problem**: Find the length of the longest substring without repeating characters.

**Approach**: 
1. Use two pointers (left and right) to define the window
2. Expand right pointer until we find a duplicate
3. Contract left pointer until no duplicates in window
4. Track maximum window size

**Pseudocode**:
```
left = 0, right = 0
max_length = 0
char_set = empty set

while right < string_length:
    if string[right] not in char_set:
        add string[right] to char_set
        right = right + 1
        max_length = max(max_length, right - left)
    else:
        remove string[left] from char_set
        left = left + 1

return max_length
```

**Python Implementation**:
```python
def longest_substring_no_repeat(s):
    if not s:
        return 0
    
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # If we find a duplicate, contract window from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character and expand window
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Examples
print(longest_substring_no_repeat("abcabcbb"))  # Output: 3 ("abc")
print(longest_substring_no_repeat("bbbbb"))     # Output: 1 ("b")
print(longest_substring_no_repeat("pwwkew"))    # Output: 3 ("wke")
```

**Time Complexity**: O(n) - each character is visited at most twice
**Space Complexity**: O(min(m, n)) where m is charset size

---

### Minimum Window Substring

**Problem**: Find the minimum window in string s that contains all characters from string t.

**Approach**: 
1. Use two pointers to define the window
2. Expand right pointer until all characters from t are found
3. Contract left pointer to find the minimum valid window
4. Track the minimum window found

**Python Implementation**:
```python
from collections import Counter

def min_window_substring(s, t):
    if not s or not t:
        return ""
    
    # Count characters needed from t
    need = Counter(t)
    missing = len(t)
    
    left = 0
    min_start = 0
    min_len = float('inf')
    
    # Expand window with right pointer
    for right in range(len(s)):
        if s[right] in need:
            need[s[right]] -= 1
            if need[s[right]] >= 0:
                missing -= 1
        
        # Contract window from left when all characters found
        while missing == 0:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_start = left
            
            if s[left] in need:
                need[s[left]] += 1
                if need[s[left]] > 0:
                    missing += 1
            left += 1
    
    return s[min_start:min_start + min_len] if min_len != float('inf') else ""

# Examples
print(min_window_substring("ADOBECODEBANC", "ABC"))  # Output: "BANC"
print(min_window_substring("a", "a"))                # Output: "a"
print(min_window_substring("a", "aa"))               # Output: ""
```

**Time Complexity**: O(n) - each character is visited at most twice
**Space Complexity**: O(k) where k is the number of unique characters in t

---

## 4. Advanced Sliding Window Patterns

### Sliding Window with Two Pointers

**Problem**: Find all subarrays with sum equal to target.

**Approach**: Use prefix sum with sliding window.

**Python Implementation**:
```python
def subarray_sum_equals_k(nums, k):
    prefix_sum = {0: 1}  # sum: count
    current_sum = 0
    count = 0
    
    for num in nums:
        current_sum += num
        
        # If current_sum - k exists in prefix_sum, we found a subarray
        if current_sum - k in prefix_sum:
            count += prefix_sum[current_sum - k]
        
        # Update prefix_sum count
        prefix_sum[current_sum] = prefix_sum.get(current_sum, 0) + 1
    
    return count

# Example
nums = [1, 1, 1]
k = 2
print(subarray_sum_equals_k(nums, k))  # Output: 2 ([1,1] and [1,1])
```

### Sliding Window with Monotonic Queue

**Problem**: Find maximum element in each sliding window of size k.

**Approach**: Use a deque to maintain indices of elements in decreasing order.

**Python Implementation**:
```python
from collections import deque

def max_sliding_window(nums, k):
    if not nums or k == 0:
        return []
    
    result = []
    dq = deque()  # Store indices
    
    for i in range(len(nums)):
        # Remove indices outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove smaller elements from back
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        # Add current index
        dq.append(i)
        
        # Add maximum for current window
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Example
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(max_sliding_window(nums, k))  # Output: [3, 3, 5, 5, 6, 7]
```

---

## 5. Common Sliding Window Problems

### Easy Level
- **Maximum Average Subarray I**: Find subarray of size k with maximum average
- **Contains Duplicate II**: Check if array has duplicate within distance k
- **Longest Continuous Increasing Subsequence**: Find longest increasing subarray

### Medium Level
- **Longest Substring with At Most K Distinct Characters**
- **Longest Substring with At Most Two Distinct Characters**
- **Subarray Product Less Than K**
- **Maximum Sum of Two Non-Overlapping Subarrays**

### Hard Level
- **Longest Substring with At Most K Distinct Characters**
- **Minimum Window Substring**
- **Sliding Window Maximum**
- **Longest Substring with At Most Two Distinct Characters**

---

## 6. Sliding Window Template

### Variable Size Window Template
```python
def sliding_window_template(arr):
    left = 0
    result = 0  # or appropriate initial value
    
    for right in range(len(arr)):
        # Expand window (add right element)
        # Update state based on right element
        
        # Contract window (remove left elements) until condition met
        while condition_not_met:
            # Update state based on left element
            left += 1
        
        # Update result
        result = max(result, right - left + 1)  # or appropriate update
    
    return result
```

### Fixed Size Window Template
```python
def fixed_window_template(arr, k):
    if len(arr) < k:
        return 0
    
    # Calculate first window
    window_sum = sum(arr[:k])
    result = window_sum
    
    # Slide window
    for i in range(k, len(arr)):
        window_sum = window_sum - arr[i-k] + arr[i]
        result = max(result, window_sum)  # or appropriate operation
    
    return result
```

---

## 7. When to Use Sliding Window

### Use Sliding Window When:
- **Problem involves contiguous subarrays/substrings**
- **You need to find minimum/maximum length satisfying a condition**
- **You need to find something of a specific size**
- **Problem involves "within k distance" or "at most k elements"

### Alternative Approaches to Consider:
- **Two Pointers**: When you need to find pairs or triplets
- **Binary Search**: When you can determine if a solution exists for a given size
- **Dynamic Programming**: When you need to consider all possible subarrays

---

## 8. Time and Space Complexity

### Time Complexity
- **Most sliding window problems**: O(n) where n is array/string length
- **Each element is processed at most twice** (added once, removed once)
- **Inner while loop**: Amortized O(1) per element

### Space Complexity
- **Usually O(1)** for simple problems
- **O(k)** where k is window size for problems requiring storage
- **O(min(m, n))** where m is charset size for string problems

---

*Sliding window is a powerful technique that can solve many array and string problems efficiently. The key is identifying when to expand and when to contract the window.*

---

## Frontend Development

*Master the fundamentals of modern web development, React best practices, and ace your frontend interviews.*

---

## DOM (Document Object Model)

### What is the DOM?
The DOM is a programming interface for HTML and XML documents. It represents the page as a tree structure where each node represents an object.

### DOM Manipulation Examples

#### Basic DOM Selection
```javascript
// Select elements
const element = document.getElementById('myId');
const elements = document.getElementsByClassName('myClass');
const elements = document.querySelectorAll('.myClass');
const element = document.querySelector('#myId');

// Traverse DOM
const parent = element.parentElement;
const children = element.children;
const nextSibling = element.nextElementSibling;
const prevSibling = element.previousElementSibling;
```

#### Creating and Modifying Elements
```javascript
// Create new element
const newDiv = document.createElement('div');
newDiv.textContent = 'Hello World';
newDiv.className = 'my-class';
newDiv.setAttribute('data-id', '123');

// Append to DOM
document.body.appendChild(newDiv);
element.appendChild(newDiv);

// Remove elements
element.remove();
element.parentNode.removeChild(element);

// Modify content
element.innerHTML = '<span>New content</span>';
element.textContent = 'Plain text content';
element.innerText = 'Text with formatting preserved';
```

#### Event Handling
```javascript
// Add event listener
element.addEventListener('click', function(event) {
    console.log('Clicked!', event);
});

// Remove event listener
const handler = function(event) { console.log('Clicked!'); };
element.addEventListener('click', handler);
element.removeEventListener('click', handler);

// Event delegation
document.addEventListener('click', function(event) {
    if (event.target.matches('.button')) {
        console.log('Button clicked:', event.target);
    }
});
```

### DOM Performance Best Practices
```javascript
// Batch DOM updates
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
    const div = document.createElement('div');
    div.textContent = `Item ${i}`;
    fragment.appendChild(div);
}
document.body.appendChild(fragment);

// Use requestAnimationFrame for animations
function animate() {
    element.style.left = (parseInt(element.style.left) + 1) + 'px';
    requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

---

## React Fundamentals

### Core Concepts

#### JSX
```jsx
{% raw %}
// JSX is syntactic sugar for React.createElement
const element = <h1>Hello, World!</h1>;

// JSX with expressions
const name = 'John';
const element = <h1>Hello, {name}!</h1>;

// JSX with attributes
const element = <div className="container" data-testid="main">Content</div>;

// JSX with children
const element = (
    <div>
        <h1>Title</h1>
        <p>Paragraph</p>
    </div>
);
{% endraw %}
```

#### Components
```jsx
{% raw %}
// Function Component
function Welcome(props) {
    return <h1>Hello, {props.name}!</h1>;
}

// Arrow Function Component
const Welcome = (props) => {
    return <h1>Hello, {props.name}!</h1>;
};

// Class Component
class Welcome extends React.Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}
{% endraw %}
```
{% raw %}

### React Hooks

#### useState
{% endraw %}
```jsx
{% raw %}
import React, { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    const [name, setName] = useState('John');

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>
                Increment
            </button>
            <input 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
            />
        </div>
    );
}
{% endraw %}
```

**Advanced useState Patterns and Best Practices**:

**1. Functional Updates** (When new state depends on previous state):
```jsx
{% raw %}
function Counter() {
    const [count, setCount] = useState(0);
    
    // ❌ Bad: Can lead to stale closures
    const increment = () => setCount(count + 1);
    
    // ✅ Good: Uses functional update
    const increment = () => setCount(prevCount => prevCount + 1);
    
    // ✅ Good: Multiple updates in sequence
    const incrementByThree = () => {
        setCount(prev => prev + 1);
        setCount(prev => prev + 1);
        setCount(prev => prev + 1);
    };
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={increment}>+1</button>
            <button onClick={incrementByThree}>+3</button>
        </div>
    );
}
{% endraw %}
```

**2. Object State Management** (Managing multiple related values):
```jsx
{% raw %}
function UserForm() {
    const [user, setUser] = useState({
        name: '',
        email: '',
        age: ''
    });
    
    // ❌ Bad: Mutating state directly
    const handleChange = (field, value) => {
        user[field] = value; // This mutates the original object!
        setUser(user); // React won't detect the change
    };
    
    // ✅ Good: Creating new object
    const handleChange = (field, value) => {
        setUser(prevUser => ({
            ...prevUser, // Spread previous state
            [field]: value // Update specific field
        }));
    };
    
    return (
        <form>
            <input
                value={user.name}
                onChange={(e) => handleChange('name', e.target.value)}
                placeholder="Name"
            />
            <input
                value={user.email}
                onChange={(e) => handleChange('email', e.target.value)}
                placeholder="Email"
            />
            <input
                value={user.age}
                onChange={(e) => handleChange('age', e.target.value)}
                placeholder="Age"
            />
        </form>
    );
}
{% endraw %}
```

**3. Lazy Initialization** (Expensive initial state):
```jsx
{% raw %}
function ExpensiveComponent() {
    // ❌ Bad: Expensive computation runs on every render
    const [data, setData] = useState(expensiveCalculation());
    
    // ✅ Good: Expensive computation only runs once
    const [data, setData] = useState(() => expensiveCalculation());
    
    function expensiveCalculation() {
        console.log('Running expensive calculation...');
        // Simulate expensive operation
        let result = 0;
        for (let i = 0; i < 1000000; i++) {
            result += Math.sqrt(i);
        }
        return result;
    }
    
    return <div>Result: {data}</div>;
}
{% endraw %}
```

**Common useState Mistakes and Solutions**:

**Mistake 1: Stale Closures in Event Handlers**
```jsx
{% raw %}
function StaleClosureExample() {
    const [count, setCount] = useState(0);
    
    // ❌ Bad: Creates a new function on every render
    const handleClick = () => {
        setTimeout(() => {
            console.log(count); // Always logs the initial value!
        }, 1000);
    };
    
    // ✅ Good: Use functional update
    const handleClick = () => {
        setTimeout(() => {
            setCount(prevCount => {
                console.log(prevCount); // Logs current value
                return prevCount + 1;
            });
        }, 1000);
    };
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={handleClick}>Increment with Delay</button>
        </div>
    );
}
{% endraw %}
```

**Mistake 2: Mutating State Objects**
```jsx
{% raw %}
function MutatingStateExample() {
    const [items, setItems] = useState([1, 2, 3]);
    
    // ❌ Bad: Mutating the array directly
    const addItem = () => {
        items.push(4); // This mutates the original array!
        setItems(items); // React won't detect the change
    };
    
    // ✅ Good: Creating a new array
    const addItem = () => {
        setItems(prevItems => [...prevItems, 4]);
    };
    
    return (
        <div>
            <ul>
                {items.map((item, index) => (
                    <li key={index}>{item}</li>
                ))}
            </ul>
            <button onClick={addItem}>Add Item</button>
        </div>
    );
}
{% endraw %}
```

**Real-world useState Examples**:

**1. Form Management**:
```jsx
{% raw %}
function ContactForm() {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        message: ''
    });
    
    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    
    const handleChange = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
        // Clear error when user starts typing
        if (errors[field]) {
            setErrors(prev => ({ ...prev, [field]: '' }));
        }
    };
    
    const validateForm = () => {
        const newErrors = {};
        if (!formData.firstName) newErrors.firstName = 'First name is required';
        if (!formData.lastName) newErrors.lastName = 'Last name is required';
        if (!formData.email) newErrors.email = 'Email is required';
        if (!formData.email.includes('@')) newErrors.email = 'Invalid email format';
        
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!validateForm()) return;
        
        setIsSubmitting(true);
        try {
            await submitForm(formData);
            // Reset form on success
            setFormData({ firstName: '', lastName: '', email: '', message: '' });
            setErrors({});
        } catch (error) {
            setErrors({ submit: 'Failed to submit form' });
        } finally {
            setIsSubmitting(false);
        }
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <div>
                <input
                    type="text"
                    value={formData.firstName}
                    onChange={(e) => handleChange('firstName', e.target.value)}
                    placeholder="First Name"
                    className={errors.firstName ? 'error' : ''}
                />
                {errors.firstName && <span className="error-text">{errors.firstName}</span>}
            </div>
            
            <div>
                <input
                    type="text"
                    value={formData.lastName}
                    onChange={(e) => handleChange('lastName', e.target.value)}
                    placeholder="Last Name"
                    className={errors.lastName ? 'error' : ''}
                />
                {errors.lastName && <span className="error-text">{errors.lastName}</span>}
            </div>
            
            <div>
                <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleChange('email', e.target.value)}
                    placeholder="Email"
                    className={errors.email ? 'error' : ''}
                />
                {errors.email && <span className="error-text">{errors.email}</span>}
            </div>
            
            <div>
                <textarea
                    value={formData.message}
                    onChange={(e) => handleChange('message', e.target.value)}
                    placeholder="Message"
                />
            </div>
            
            {errors.submit && <div className="error-text">{errors.submit}</div>}
            
            <button type="submit" disabled={isSubmitting}>
                {isSubmitting ? 'Submitting...' : 'Submit'}
            </button>
        </form>
    );
}
{% endraw %}
```

**2. Shopping Cart State**:
```jsx
{% raw %}
function ShoppingCart() {
    const [cart, setCart] = useState([]);
    const [total, setTotal] = useState(0);
    
    const addToCart = (product) => {
        setCart(prevCart => {
            const existingItem = prevCart.find(item => item.id === product.id);
            
            if (existingItem) {
                // Update quantity of existing item
                return prevCart.map(item =>
                    item.id === product.id
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                );
            } else {
                // Add new item
                return [...prevCart, { ...product, quantity: 1 }];
            }
        });
    };
    
    const removeFromCart = (productId) => {
        setCart(prevCart => prevCart.filter(item => item.id !== productId));
    };
    
    const updateQuantity = (productId, newQuantity) => {
        if (newQuantity <= 0) {
            removeFromCart(productId);
            return;
        }
        
        setCart(prevCart =>
            prevCart.map(item =>
                item.id === productId
                    ? { ...item, quantity: newQuantity }
                    : item
            )
        );
    };
    
    // Calculate total whenever cart changes
    useEffect(() => {
        const newTotal = cart.reduce((sum, item) => 
            sum + (item.price * item.quantity), 0
        );
        setTotal(newTotal);
    }, [cart]);
    
    return (
        <div>
            <h2>Shopping Cart ({cart.length} items)</h2>
            {cart.map(item => (
                <div key={item.id} className="cart-item">
                    <span>{item.name}</span>
                    <span>${item.price}</span>
                    <input
                        type="number"
                        min="1"
                        value={item.quantity}
                        onChange={(e) => updateQuantity(item.id, parseInt(e.target.value))}
                    />
                    <button onClick={() => removeFromCart(item.id)}>Remove</button>
                </div>
            ))}
            <div className="cart-total">
                <strong>Total: ${total.toFixed(2)}</strong>
            </div>
        </div>
    );
}
{% endraw %}
```

#### useEffect - Side Effects and Lifecycle Management

**What it does**: `useEffect` lets you perform side effects in function components. It's a combination of `componentDidMount`, `componentDidUpdate`, and `componentWillUnmount` from class components.

**Key Concepts**:
- **Side Effects**: Operations like data fetching, subscriptions, manual DOM mutations, logging
- **Dependency Array**: Controls when the effect runs
- **Cleanup Function**: Runs before the component unmounts or before the effect runs again
- **Timing**: Runs after the browser has painted the DOM

**Basic Usage**:
```jsx
{% raw %}
import React, { useState, useEffect } from 'react';

function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // ComponentDidMount equivalent
        fetchUser(userId);
        
        // ComponentWillUnmount equivalent
        return () => {
            // Cleanup function
            console.log('Component unmounting');
        };
    }, [userId]); // Dependency array

    useEffect(() => {
        // Run on every render
        document.title = user ? `${user.name}'s Profile` : 'Loading...';
    });

    const fetchUser = async (id) => {
        try {
            const response = await fetch(`/api/users/${id}`);
            const userData = await response.json();
            setUser(userData);
        } catch (error) {
            console.error('Error fetching user:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (!user) return <div>User not found</div>;

    return (
        <div>
            <h1>{user.name}</h1>
            <p>{user.email}</p>
        </div>
    );
}
{% endraw %}
```

**useEffect Dependency Array Patterns**:

**1. No Dependencies** (Runs after every render):
```jsx
{% raw %}
function LoggingComponent() {
    const [count, setCount] = useState(0);
    
    // ❌ Bad: Runs on every render, can cause infinite loops
    useEffect(() => {
        console.log('Component rendered');
        // This could trigger another render if it updates state!
    });
    
    // ✅ Good: Only for logging, no state updates
    useEffect(() => {
        console.log('Component rendered, count:', count);
    });
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>Increment</button>
        </div>
    );
}
{% endraw %}
```

**2. Empty Dependencies** (Runs only once on mount):
```jsx
{% raw %}
function SubscriptionComponent() {
    const [data, setData] = useState(null);
    
    useEffect(() => {
        // ✅ Good: Set up subscription only once
        const subscription = subscribeToData((newData) => {
            setData(newData);
        });
        
        // Cleanup: Remove subscription on unmount
        return () => {
            subscription.unsubscribe();
        };
    }, []); // Empty dependency array = run only once
    
    return <div>Data: {data}</div>;
}
{% endraw %}
```

**3. Specific Dependencies** (Runs when dependencies change):
```jsx
{% raw %}
function SearchComponent({ query, filters }) {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    
    useEffect(() => {
        // ✅ Good: Only search when query or filters change
        if (query.trim()) {
            setLoading(true);
            searchAPI(query, filters).then(setResults).finally(() => setLoading(false));
        }
    }, [query, filters]); // Re-run when query or filters change
    
    return (
        <div>
            {loading ? <div>Searching...</div> : (
                <ul>
                    {results.map(result => (
                        <li key={result.id}>{result.title}</li>
                    ))}
                </ul>
            )}
        </div>
    );
}
{% endraw %}
```

**4. Function Dependencies** (Handling function references):
```jsx
{% raw %}
function ParentComponent() {
    const [count, setCount] = useState(0);
    
    // ❌ Bad: Function recreated on every render
    const handleIncrement = () => setCount(count + 1);
    
    // ✅ Good: Memoized function with useCallback
    const handleIncrement = useCallback(() => {
        setCount(prev => prev + 1);
    }, []); // No dependencies needed
    
    return <ChildComponent onIncrement={handleIncrement} />;
}

function ChildComponent({ onIncrement }) {
    useEffect(() => {
        // This effect will only run when onIncrement function reference changes
        console.log('Increment handler changed');
    }, [onIncrement]);
    
    return <button onClick={onIncrement}>Increment</button>;
}
{% endraw %}
```

**Advanced useEffect Patterns**:

**1. Multiple Effects for Different Concerns**:
```jsx
{% raw %}
function ComplexComponent({ userId, theme }) {
    const [user, setUser] = useState(null);
    const [posts, setPosts] = useState([]);
    const [notifications, setNotifications] = useState([]);
    
    // Effect 1: Fetch user data
    useEffect(() => {
        fetchUser(userId).then(setUser);
    }, [userId]);
    
    // Effect 2: Fetch user posts
    useEffect(() => {
        if (user) {
            fetchUserPosts(user.id).then(setPosts);
        }
    }, [user]);
    
    // Effect 3: Set up real-time notifications
    useEffect(() => {
        if (user) {
            const subscription = subscribeToNotifications(user.id, setNotifications);
            return () => subscription.unsubscribe();
        }
    }, [user]);
    
    // Effect 4: Update document title
    useEffect(() => {
        if (user) {
            document.title = `${user.name}'s Dashboard`;
        }
    }, [user]);
    
    // Effect 5: Apply theme
    useEffect(() => {
        document.body.className = `theme-${theme}`;
    }, [theme]);
    
    return (
        <div>
            {/* Component JSX */}
        </div>
    );
}
{% endraw %}
```

**2. Cleanup Functions and AbortController**:
```jsx
{% raw %}
function DataFetchingComponent({ url }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        const abortController = new AbortController();
        
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await fetch(url, {
                    signal: abortController.signal
                });
                const result = await response.json();
                setData(result);
            } catch (error) {
                if (error.name === 'AbortError') {
                    console.log('Fetch aborted');
                } else {
                    console.error('Fetch error:', error);
                }
            } finally {
                setLoading(false);
            }
        };
        
        fetchData();
        
        // Cleanup: Abort fetch if component unmounts or URL changes
        return () => {
            abortController.abort();
        };
    }, [url]);
    
    if (loading) return <div>Loading...</div>;
    return <div>{JSON.stringify(data)}</div>;
}
{% endraw %}
```

**3. Custom Hook with useEffect**:
```jsx
{% raw %}
function useLocalStorage(key, initialValue) {
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error('Error reading from localStorage:', error);
            return initialValue;
        }
    });
    
    const setValue = (value) => {
        try {
            // Allow value to be a function so we have the same API as useState
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error('Error setting localStorage:', error);
        }
    };
    
    return [storedValue, setValue];
}

// Usage
function UserPreferences() {
    const [theme, setTheme] = useLocalStorage('theme', 'light');
    const [language, setLanguage] = useLocalStorage('language', 'en');
    
    return (
        <div>
            <select value={theme} onChange={(e) => setTheme(e.target.value)}>
                <option value="light">Light</option>
                <option value="dark">Dark</option>
            </select>
            
            <select value={language} onChange={(e) => setLanguage(e.target.value)}>
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
            </select>
        </div>
    );
}
{% endraw %}
```

**Common useEffect Mistakes and Solutions**:

**Mistake 1: Missing Dependencies**:
```jsx
{% raw %}
function BuggyComponent({ userId }) {
    const [user, setUser] = useState(null);
    
    // ❌ Bad: Missing userId in dependencies
    useEffect(() => {
        fetchUser(userId).then(setUser);
    }, []); // This will only fetch once, even if userId changes!
    
    // ✅ Good: Include all dependencies
    useEffect(() => {
        fetchUser(userId).then(setUser);
    }, [userId]);
    
    return <div>{user?.name}</div>;
}
{% endraw %}
```

**Mistake 2: Infinite Loops**:
```jsx
{% raw %}
function InfiniteLoopComponent() {
    const [count, setCount] = useState(0);
    
    // ❌ Bad: Updates state in effect with no dependencies
    useEffect(() => {
        setCount(count + 1); // This causes infinite re-renders!
    }); // No dependency array = runs after every render
    
    // ✅ Good: Only update when needed
    useEffect(() => {
        if (count < 10) {
            setCount(prev => prev + 1);
        }
    }, [count]); // Only run when count changes
    
    // ✅ Better: Use a ref to track if it's the first render
    const isFirstRender = useRef(true);
    useEffect(() => {
        if (isFirstRender.current) {
            isFirstRender.current = false;
            setCount(1); // Only set once on mount
        }
    }, []);
    
    return <div>Count: {count}</div>;
}
{% endraw %}
```

**Mistake 3: Forgetting Cleanup**:
```jsx
{% raw %}
function SubscriptionComponent() {
    const [data, setData] = useState(null);
    
    // ❌ Bad: No cleanup, can cause memory leaks
    useEffect(() => {
        const subscription = subscribeToData(setData);
        // Missing return statement for cleanup!
    }, []);
    
    // ✅ Good: Proper cleanup
    useEffect(() => {
        const subscription = subscribeToData(setData);
        return () => subscription.unsubscribe();
    }, []);
    
    return <div>{data}</div>;
}
{% endraw %}
```

**Real-world useEffect Examples**:

**1. API Data Fetching with Loading States**:
```jsx
{% raw %}
function UserDashboard({ userId }) {
    const [user, setUser] = useState(null);
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState({ user: true, posts: true });
    const [error, setError] = useState(null);
    
    // Fetch user data
    useEffect(() => {
        const fetchUser = async () => {
            try {
                setLoading(prev => ({ ...prev, user: true }));
                setError(null);
                
                const response = await fetch(`/api/users/${userId}`);
                if (!response.ok) throw new Error('Failed to fetch user');
                
                const userData = await response.json();
                setUser(userData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(prev => ({ ...prev, user: false }));
            }
        };
        
        fetchUser();
    }, [userId]);
    
    // Fetch user posts (only after user is loaded)
    useEffect(() => {
        if (!user) return;
        
        const fetchPosts = async () => {
            try {
                setLoading(prev => ({ ...prev, posts: true }));
                const response = await fetch(`/api/users/${userId}/posts`);
                const postsData = await response.json();
                setPosts(postsData);
            } catch (err) {
                console.error('Failed to fetch posts:', err);
            } finally {
                setLoading(prev => ({ ...prev, posts: false }));
            }
        };
        
        fetchPosts();
    }, [user, userId]);
    
    // Update document title
    useEffect(() => {
        if (user) {
            document.title = `${user.name}'s Dashboard`;
        }
    }, [user]);
    
    if (loading.user) return <div>Loading user...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!user) return <div>User not found</div>;
    
    return (
        <div>
            <h1>{user.name}'s Dashboard</h1>
            <p>Email: {user.email}</p>
            
            <h2>Posts</h2>
            {loading.posts ? (
                <div>Loading posts...</div>
            ) : (
                <div>
                    {posts.map(post => (
                        <div key={post.id}>
                            <h3>{post.title}</h3>
                            <p>{post.excerpt}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
{% endraw %}
```

**2. Real-time Updates with WebSocket**:
```jsx
{% raw %}
function ChatRoom({ roomId, userId }) {
    const [messages, setMessages] = useState([]);
    const [isConnected, setIsConnected] = useState(false);
    const [newMessage, setNewMessage] = useState('');
    
    // WebSocket connection
    useEffect(() => {
        const ws = new WebSocket(`wss://chat.example.com/room/${roomId}`);
        
        ws.onopen = () => {
            setIsConnected(true);
            console.log('Connected to chat room');
        };
        
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            setMessages(prev => [...prev, message]);
        };
        
        ws.onclose = () => {
            setIsConnected(false);
            console.log('Disconnected from chat room');
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            setIsConnected(false);
        };
        
        // Cleanup: Close connection on unmount
        return () => {
            ws.close();
        };
    }, [roomId]);
    
    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        const chatContainer = document.getElementById('chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }, [messages]);
    
    const sendMessage = () => {
        if (!newMessage.trim() || !isConnected) return;
        
        const message = {
            id: Date.now(),
            text: newMessage,
            userId,
            timestamp: new Date().toISOString()
        };
        
        // Optimistically add message to UI
        setMessages(prev => [...prev, message]);
        setNewMessage('');
        
        // Send to server (in real app, you'd send via WebSocket)
        console.log('Sending message:', message);
    };
    
    return (
        <div>
            <div className="connection-status">
                Status: {isConnected ? 'Connected' : 'Disconnected'}
            </div>
            
            <div id="chat-container" className="messages">
                {messages.map(message => (
                    <div key={message.id} className={`message ${message.userId === userId ? 'own' : 'other'}`}>
                        <span className="user">{message.userId}</span>
                        <span className="text">{message.text}</span>
                        <span className="time">{new Date(message.timestamp).toLocaleTimeString()}</span>
                    </div>
                ))}
            </div>
            
            <div className="input-area">
                <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Type a message..."
                    disabled={!isConnected}
                />
                <button onClick={sendMessage} disabled={!isConnected || !newMessage.trim()}>
                    Send
                </button>
            </div>
        </div>
    );
}
{% endraw %}
```

#### useRef
```jsx
{% raw %}
import React, { useRef, useEffect } from 'react';

function FocusInput() {
    const inputRef = useRef(null);

    useEffect(() => {
        // Focus input on mount
        inputRef.current.focus();
    }, []);

    return (
        <div>
            <input ref={inputRef} type="text" placeholder="Focus me!" />
            <button onClick={() => inputRef.current.focus()}>
                Focus Input
            </button>
        </div>
    );
}
{% endraw %}
```

#### Custom Hooks
```jsx
{% raw %}
// Custom hook for API calls
function useApi(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await fetch(url);
                const result = await response.json();
                setData(result);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [url]);

    return { data, loading, error };
}

// Usage
function UserList() {
    const { data: users, loading, error } = useApi('/api/users');

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <ul>
            {users.map(user => (
                <li key={user.id}>{user.name}</li>
            ))}
        </ul>
    );
}
{% endraw %}
```

---

## React Best Practices

### Component Design

#### Single Responsibility Principle
```jsx
{% raw %}
// ❌ Bad: Component doing too many things
function UserDashboard() {
    const [users, setUsers] = useState([]);
    const [posts, setPosts] = useState([]);
    const [comments, setComments] = useState([]);
    
    // Fetch logic, rendering logic, business logic all mixed
    return (
        <div>
            {/* Complex mixed content */}
        </div>
    );
}

// ✅ Good: Separated concerns
function UserDashboard() {
    return (
        <div>
            <UserList />
            <PostList />
            <CommentList />
        </div>
    );
}

function UserList() {
    const [users, setUsers] = useState([]);
    // Only user-related logic
    return <div>{/* User rendering */}</div>;
}
{% endraw %}
```

#### Props Design
```jsx
{% raw %}
// ❌ Bad: Too many props
function UserCard({ id, name, email, avatar, bio, location, website, twitter, github, linkedin, skills, experience, education, projects, followers, following, createdAt, updatedAt, status, role, permissions, settings, preferences, notifications, theme, language, timezone, currency, units, privacy, security, verification, badges, achievements, level, points, rank, tier, subscription, plan, billing, payment, history, logs, analytics, reports, exports, imports, backups, restores, migrations, updates, patches, hotfixes, releases, versions, builds, deployments, environments, configs, secrets, keys, tokens, sessions, cookies, cache, storage, database, api, endpoints, routes, middleware, validation, sanitization, encryption, hashing, compression, optimization, minification, bundling, transpilation, polyfills, shims, fallbacks, polyfills, shims, fallbacks }) {
    // Component with 100+ props
}

// ✅ Good: Grouped props
function UserCard({ user, actions, theme }) {
    const { name, email, avatar, bio } = user;
    const { onEdit, onDelete, onFollow } = actions;
    const { colors, spacing } = theme;
    
    return <div>{/* Clean component */}</div>;
}

// Usage
<UserCard 
    user={userData}
    actions={{ onEdit, onDelete, onFollow }}
    theme={{ colors: 'dark', spacing: 'compact' }}
/>
{% endraw %}
```

#### Conditional Rendering
```jsx
{% raw %}
// ❌ Bad: Complex nested ternaries
function UserStatus({ user }) {
    return (
        <div>
            {user.isActive ? (
                user.isPremium ? (
                    user.isVerified ? (
                        <span className="premium-verified">Premium Verified</span>
                    ) : (
                        <span className="premium">Premium</span>
                    )
                ) : (
                    user.isVerified ? (
                        <span className="verified">Verified</span>
                    ) : (
                        <span className="active">Active</span>
                    )
                )
            ) : (
                <span className="inactive">Inactive</span>
            )}
        </div>
    );
}

// ✅ Good: Clean conditional rendering
function UserStatus({ user }) {
    if (!user.isActive) {
        return <span className="inactive">Inactive</span>;
    }

    const statusClasses = ['active'];
    if (user.isPremium) statusClasses.push('premium');
    if (user.isVerified) statusClasses.push('verified');

    const statusText = [
        user.isPremium && 'Premium',
        user.isVerified && 'Verified'
    ].filter(Boolean).join(' ') || 'Active';

    return (
        <span className={statusClasses.join(' ')}>
            {statusText}
        </span>
    );
}
{% endraw %}
```

### Performance Optimization

#### React.memo
```jsx
{% raw %}
import React, { memo } from 'react';

const ExpensiveComponent = memo(function ExpensiveComponent({ data, onAction }) {
    // Expensive computation
    const processedData = data.map(item => ({
        ...item,
        processed: item.value * 2 + Math.sqrt(item.value)
    }));

    return (
        <div>
            {processedData.map(item => (
                <div key={item.id}>
                    {item.name}: {item.processed}
                </div>
            ))}
        </div>
    );
});

// Only re-renders if props change
<ExpensiveComponent data={userData} onAction={handleAction} />
{% endraw %}
```

#### useMemo and useCallback
```jsx
{% raw %}
import React, { useState, useMemo, useCallback } from 'react';

function UserDashboard({ users, filters }) {
    const [sortBy, setSortBy] = useState('name');

    // Memoize expensive computation
    const filteredAndSortedUsers = useMemo(() => {
        console.log('Computing filtered users...');
        return users
            .filter(user => {
                if (filters.activeOnly && !user.isActive) return false;
                if (filters.role && user.role !== filters.role) return false;
                return true;
            })
            .sort((a, b) => {
                if (sortBy === 'name') return a.name.localeCompare(b.name);
                if (sortBy === 'email') return a.email.localeCompare(b.email);
                return 0;
            });
    }, [users, filters, sortBy]);

    // Memoize callback functions
    const handleUserAction = useCallback((userId, action) => {
        console.log(`Performing ${action} on user ${userId}`);
        // Action logic
    }, []);

    const handleSort = useCallback((field) => {
        setSortBy(field);
    }, []);

    return (
        <div>
            <div>
                <button onClick={() => handleSort('name')}>Sort by Name</button>
                <button onClick={() => handleSort('email')}>Sort by Email</button>
            </div>
            {filteredAndSortedUsers.map(user => (
                <UserCard 
                    key={user.id} 
                    user={user} 
                    onAction={handleUserAction}
                />
            ))}
        </div>
    );
}
{% endraw %}
```

#### Code Splitting
```jsx
{% raw %}
import React, { Suspense, lazy } from 'react';

// Lazy load components
const UserList = lazy(() => import('./UserList'));
const UserDetails = lazy(() => import('./UserDetails'));
const UserSettings = lazy(() => import('./UserSettings'));

function App() {
    return (
        <Router>
            <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                    <Route path="/users" element={<UserList />} />
                    <Route path="/users/:id" element={<UserDetails />} />
                    <Route path="/users/:id/settings" element={<UserSettings />} />
                </Routes>
            </Suspense>
        </Router>
    );
}
{% endraw %}
```

---

## Component Creation Examples

### Reusable Button Component
```jsx
{% raw %}
import React from 'react';
import PropTypes from 'prop-types';

const Button = React.memo(function Button({ 
    children, 
    variant = 'primary', 
    size = 'medium',
    disabled = false,
    loading = false,
    onClick,
    type = 'button',
    className = '',
    ...props 
}) {
    const baseClasses = 'btn';
    const variantClasses = {
        primary: 'btn-primary',
        secondary: 'btn-secondary',
        danger: 'btn-danger',
        success: 'btn-success',
        warning: 'btn-warning'
    };
    const sizeClasses = {
        small: 'btn-sm',
        medium: 'btn-md',
        large: 'btn-lg'
    };

    const classes = [
        baseClasses,
        variantClasses[variant],
        sizeClasses[size],
        disabled && 'btn-disabled',
        loading && 'btn-loading',
        className
    ].filter(Boolean).join(' ');

    const handleClick = (event) => {
        if (!disabled && !loading && onClick) {
            onClick(event);
        }
    };

    return (
        <button
            type={type}
            className={classes}
            disabled={disabled || loading}
            onClick={handleClick}
            {...props}
        >
            {loading && <span className="spinner" />}
            {children}
        </button>
    );
});

Button.propTypes = {
    children: PropTypes.node.isRequired,
    variant: PropTypes.oneOf(['primary', 'secondary', 'danger', 'success', 'warning']),
    size: PropTypes.oneOf(['small', 'medium', 'large']),
    disabled: PropTypes.bool,
    loading: PropTypes.bool,
    onClick: PropTypes.func,
    type: PropTypes.oneOf(['button', 'submit', 'reset']),
    className: PropTypes.string
};

export default Button;
{% endraw %}
```

### Form Component with Validation
```jsx
{% raw %}
import React, { useState, useCallback } from 'react';

function useForm(initialValues, validationSchema) {
    const [values, setValues] = useState(initialValues);
    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({});

    const handleChange = useCallback((name, value) => {
        setValues(prev => ({ ...prev, [name]: value }));
        
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    }, [errors]);

    const handleBlur = useCallback((name) => {
        setTouched(prev => ({ ...prev, [name]: true }));
        
        // Validate on blur
        if (validationSchema[name]) {
            const error = validationSchema[name](values[name]);
            setErrors(prev => ({ ...prev, [name]: error }));
        }
    }, [values, validationSchema]);

    const validate = useCallback(() => {
        const newErrors = {};
        Object.keys(validationSchema).forEach(field => {
            const error = validationSchema[field](values[field]);
            if (error) newErrors[field] = error;
        });
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    }, [values, validationSchema]);

    const reset = useCallback(() => {
        setValues(initialValues);
        setErrors({});
        setTouched({});
    }, [initialValues]);

    return {
        values,
        errors,
        touched,
        handleChange,
        handleBlur,
        validate,
        reset
    };
}

function LoginForm() {
    const validationSchema = {
        email: (value) => {
            if (!value) return 'Email is required';
            if (!/\S+@\S+\.\S+/.test(value)) return 'Email is invalid';
            return '';
        },
        password: (value) => {
            if (!value) return 'Password is required';
            if (value.length < 6) return 'Password must be at least 6 characters';
            return '';
        }
    };

    const { values, errors, touched, handleChange, handleBlur, validate } = useForm(
        { email: '', password: '' },
        validationSchema
    );

    const handleSubmit = (e) => {
        e.preventDefault();
        if (validate()) {
            console.log('Form submitted:', values);
            // Submit logic
        }
    };

    return (
        <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                    id="email"
                    type="email"
                    value={values.email}
                    onChange={(e) => handleChange('email', e.target.value)}
                    onBlur={() => handleBlur('email')}
                    className={touched.email && errors.email ? 'error' : ''}
                />
                {touched.email && errors.email && (
                    <span className="error-message">{errors.email}</span>
                )}
            </div>

            <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                    id="password"
                    type="password"
                    value={values.password}
                    onChange={(e) => handleChange('password', e.target.value)}
                    onBlur={() => handleBlur('password')}
                    className={touched.password && errors.password ? 'error' : ''}
                />
                {touched.password && errors.password && (
                    <span className="error-message">{errors.password}</span>
                )}
            </div>

            <button type="submit" className="btn btn-primary">
                Login
            </button>
        </form>
    );
}
{% endraw %}
```

---

## Frontend Interview Essentials

### Common Questions & Answers

#### 1. What is the Virtual DOM?
```javascript
// Virtual DOM is a lightweight copy of the actual DOM
// React uses it to optimize rendering performance

// Without Virtual DOM (expensive)
function updateDOM() {
    // Directly manipulate DOM - causes reflows/repaints
    document.getElementById('user-list').innerHTML = newHTML;
}

// With Virtual DOM (efficient)
function ReactUpdate() {
    // React compares Virtual DOM with previous version
    // Only updates what changed
    return (
        <UserList users={updatedUsers} />
    );
}
```

#### 2. Explain React's Component Lifecycle
```jsx
{% raw %}
class ClassComponent extends React.Component {
    // Mounting Phase
    constructor(props) {
        super(props);
        this.state = { data: null };
    }

    static getDerivedStateFromProps(props, state) {
        // Called before render, can update state
        return null;
    }

    componentDidMount() {
        // Component mounted, safe to make API calls
        this.fetchData();
    }

    // Updating Phase
    shouldComponentUpdate(nextProps, nextState) {
        // Return false to prevent re-render
        return this.props.id !== nextProps.id;
    }

    getSnapshotBeforeUpdate(prevProps, prevState) {
        // Capture info before DOM updates
        return { scrollPosition: window.scrollY };
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        // Component updated, can access DOM
        if (snapshot.scrollPosition) {
            window.scrollTo(0, snapshot.scrollPosition);
        }
    }

    // Unmounting Phase
    componentWillUnmount() {
        // Cleanup: remove event listeners, cancel requests
        this.cancelRequest();
    }

    render() {
        return <div>{this.state.data}</div>;
    }
}

// Hooks equivalent
function FunctionalComponent({ id }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // componentDidMount
        fetchData();
        
        // componentWillUnmount
        return () => cleanup();
    }, [id]); // componentDidUpdate equivalent

    return <div>{data}</div>;
}
{% endraw %}
```

#### 3. State Management Patterns
```jsx
{% raw %}
// Local State
function LocalStateExample() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(count + 1)}>{count}</button>;
}

// Lifted State
function Parent() {
    const [sharedState, setSharedState] = useState('');
    return (
        <div>
            <ChildA value={sharedState} onChange={setSharedState} />
            <ChildB value={sharedState} onChange={setSharedState} />
        </div>
    );
}

// Context API
const ThemeContext = React.createContext();

function ThemeProvider({ children }) {
    const [theme, setTheme] = useState('light');
    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}

function ThemedButton() {
    const { theme, setTheme } = useContext(ThemeContext);
    return (
        <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
            Current theme: {theme}
        </button>
    );
}

// Custom Hook for State
function useCounter(initialValue = 0) {
    const [count, setCount] = useState(initialValue);
    
    const increment = useCallback(() => setCount(c => c + 1), []);
    const decrement = useCallback(() => setCount(c => c - 1), []);
    const reset = useCallback(() => setCount(initialValue), [initialValue]);
    
    return { count, increment, decrement, reset };
}
{% endraw %}
```

#### 4. Performance Optimization Techniques
```jsx
{% raw %}
// 1. React.memo for expensive components
const ExpensiveComponent = React.memo(({ data }) => {
    // Only re-renders if props change
    return <div>{/* Expensive rendering */}</div>;
});

// 2. useMemo for expensive calculations
function DataTable({ data, filters }) {
    const filteredData = useMemo(() => {
        return data.filter(item => {
            // Expensive filtering logic
            return filters.every(filter => filter(item));
        });
    }, [data, filters]);

    return <table>{/* Render filtered data */}</table>;
}

// 3. useCallback for stable references
function ParentComponent() {
    const [count, setCount] = useState(0);
    
    const handleClick = useCallback(() => {
        setCount(c => c + 1);
    }, []); // Stable reference, won't cause child re-renders

    return <ChildComponent onClick={handleClick} />;
}

// 4. Lazy loading
const LazyComponent = React.lazy(() => import('./LazyComponent'));

function App() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <LazyComponent />
        </Suspense>
    );
}
{% endraw %}
```

#### 5. Error Boundaries
```jsx
{% raw %}
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        // Log error to service
        console.error('Error caught by boundary:', error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="error-boundary">
                    <h2>Something went wrong</h2>
                    <button onClick={() => window.location.reload()}>
                        Reload Page
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}

// Usage
<ErrorBoundary>
    <ComponentThatMightError />
</ErrorBoundary>
{% endraw %}
```

### CSS-in-JS and Styling
```jsx
{% raw %}
// Styled Components
import styled from 'styled-components';

const Button = styled.button`
    background: ${props => props.primary ? 'blue' : 'white'};
    color: ${props => props.primary ? 'white' : 'blue'};
    padding: 10px 20px;
    border: 2px solid blue;
    border-radius: 4px;
    cursor: pointer;
    
    &:hover {
        background: ${props => props.primary ? 'darkblue' : 'lightblue'};
    }
    
    &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
`;

// CSS Modules
import styles from './Button.module.css';

function Button({ children, variant }) {
    const buttonClass = `${styles.button} ${styles[variant]}`;
    return <button className={buttonClass}>{children}</button>;
}

// CSS-in-JS with emotion
import { css } from '@emotion/react';

const buttonStyle = css`
    background: blue;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    
    &:hover {
        background: darkblue;
    }
`;

function Button({ children }) {
    return <button css={buttonStyle}>{children}</button>;
}
{% endraw %}
```

---

## Key Takeaways

### **DOM Mastery**
- Understand DOM tree structure and traversal
- Use event delegation for performance
- Batch DOM updates to minimize reflows

### **React Best Practices**
- Keep components small and focused
- Use hooks for state and side effects
- Implement proper error boundaries
- Optimize with React.memo, useMemo, useCallback

### **Component Design**
- Single responsibility principle
- Props design with object grouping
- Conditional rendering patterns
- Reusable component libraries

### **Performance**
- Virtual DOM understanding
- Code splitting and lazy loading
- Bundle optimization
- Memory leak prevention

### **Interview Success**
- Explain concepts clearly with examples
- Show understanding of trade-offs
- Demonstrate problem-solving approach
- Know when to use different patterns

*Frontend development is about creating intuitive, performant user experiences. Master these fundamentals and you'll be well-prepared for any frontend role!*

---

## Programming Languages & Tools

*Deep dive into Python, Node.js, Bash scripting, and React with advanced patterns, practical examples, and interview essentials.*

---

## Python Deep Dive

### Advanced Patterns

#### Decorators

**What they are**: Functions that modify or enhance other functions/classes without changing their source code.

**Common use cases**: Logging, timing, authentication, caching, retry logic, and design patterns like singleton.

**Key benefits**: Code reusability, separation of concerns, and clean syntax with the `@` symbol.

```python
# Function decorator - adds timing functionality
def timer(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
    return "Done"

# Class decorator - implements singleton pattern
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Creating database connection...")
```

#### Context Managers

**What they are**: Objects that manage the setup and cleanup of resources automatically using the `with` statement.

**Common use cases**: File handling, database connections, locks, network connections, and any resource that needs proper cleanup.

**Key benefits**: Automatic resource management, exception safety, and cleaner code than try-finally blocks.

```python
# Custom context manager - manages database connections
class DatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None
    
    def __enter__(self):
        print(f"Connecting to {self.host}:{self.port}")
        self.connection = f"Connection to {self.host}:{self.port}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing connection to {self.host}:{self.port}")
        self.connection = None
        if exc_type:
            print(f"Exception occurred: {exc_val}")
        return False  # Don't suppress exceptions

# Usage
with DatabaseConnection("localhost", 5432) as conn:
    print(f"Using connection: {conn}")
    # Database operations here

# Context manager with contextlib - simpler file handling
from contextlib import contextmanager

@contextmanager
def file_handler(filename, mode='r'):
    file = open(filename, mode)
    try:
        yield file
    finally:
        file.close()

# Usage
with file_handler('data.txt', 'w') as f:
    f.write('Hello, World!')
```

#### Async/Await Patterns

**What they are**: Python's way of writing asynchronous, non-blocking code that can handle many concurrent operations efficiently.

**Common use cases**: Web scraping, API calls, database operations, file I/O, and any I/O-bound operations that can benefit from concurrency.

**Key benefits**: Better performance for I/O operations, non-blocking execution, and efficient resource utilization.

```python
import asyncio
import aiohttp

# Basic async function - fetches data from URLs
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Concurrent execution - processes multiple URLs simultaneously
async def process_multiple_urls(urls):
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# Async context manager - manages async resources
class AsyncDatabasePool:
    def __init__(self, max_connections=10):
        self.connections = asyncio.Queue(maxsize=max_connections)
    
    async def __aenter__(self):
        for i in range(max_connections):
            await self.connections.put(f"Connection {i}")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        while not self.connections.empty():
            await self.connections.get()
    
    async def get_connection(self):
        return await self.connections.get()

# Usage
async def main():
    urls = ['http://example.com', 'http://example.org']
    results = await process_multiple_urls(urls)
    
    async with AsyncDatabasePool() as pool:
        conn = await pool.get_connection()
        # Use connection

asyncio.run(main())
```

#### Metaclasses and Descriptors

**What they are**: Advanced Python features that allow you to customize how classes and attributes behave.

**Metaclasses**: Classes that create other classes, allowing you to modify class creation behavior.
**Descriptors**: Objects that customize attribute access, get, set, and delete operations.

**Common use cases**: Design patterns, validation, logging, and framework development.

```python
# Metaclass - implements singleton pattern by controlling class instantiation
class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self):
        print("Creating database...")

# Descriptor - adds validation to class attributes
class ValidatedProperty:
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} must be >= {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} must be <= {self.max_value}")
        instance.__dict__[self.name] = value

class User:
    age = ValidatedProperty(min_value=0, max_value=150)
    score = ValidatedProperty(min_value=0, max_value=100)
    
    def __init__(self, age, score):
        self.age = age
        self.score = score
```

### Python Interview Essentials

#### Common Patterns

**What they are**: Reusable solutions to common software design problems that improve code organization and maintainability.

**Factory Pattern**: Creates objects without specifying their exact class, useful for object creation that depends on runtime conditions.
**Observer Pattern**: Establishes a one-to-many dependency between objects, where one object's state change notifies all dependents.

**Key benefits**: Code reusability, loose coupling, and easier testing and maintenance.

```python
# Factory pattern - creates objects based on type
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        animals = {
            'dog': Dog,
            'cat': Cat
        }
        return animals.get(animal_type, Animal)()

# Observer pattern - notifies multiple objects of state changes
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self, data):
        for observer in self._observers:
            observer.update(data)

class Observer:
    def update(self, data):
        print(f"Received: {data}")

# Usage
subject = Subject()
observer1 = Observer()
observer2 = Observer()
subject.attach(observer1)
subject.attach(observer2)
subject.notify("Hello observers!")
```

#### Performance Optimization

**What they are**: Techniques and Python features that improve code performance, memory usage, and execution speed.

**Key optimizations**: Memory-efficient classes, function memoization, and optimized data structures.

**Common use cases**: High-performance applications, memory-constrained environments, and optimization of frequently called functions.

```python
# __slots__ - reduces memory usage by preventing dynamic attribute creation
class Point:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# lru_cache - memoizes function results to avoid repeated expensive calculations
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# defaultdict - eliminates need for key existence checks
from collections import defaultdict

# Instead of this:
word_count = {}
for word in words:
    if word not in word_count:
        word_count[word] = 0
    word_count[word] += 1

# Use this:
word_count = defaultdict(int)
for word in words:
    word_count[word] += 1
```

---

## Node.js Deep Dive

### Event Loop and Asynchronous Patterns

#### Understanding the Event Loop

**What it is**: Node.js's core mechanism that handles asynchronous operations and determines the order of execution for different types of callbacks.

**Key phases**: Timer callbacks, I/O callbacks, idle/prepare, poll, check, close callbacks, and microtask queues.

**Why it matters**: Understanding the event loop is crucial for writing efficient, non-blocking Node.js applications and debugging timing issues.

```javascript
// Event loop phases - demonstrates execution order
console.log('1. Start');

setTimeout(() => {
    console.log('2. Timer phase');
}, 0);

setImmediate(() => {
    console.log('3. Check phase');
});

process.nextTick(() => {
    console.log('4. Next tick queue');
});

Promise.resolve().then(() => {
    console.log('5. Microtask queue');
});

console.log('6. End');

// Output order: 1, 6, 4, 5, 2, 3
```

#### Streams and Backpressure

**What they are**: Streams are Node.js objects for reading/writing data in chunks, while backpressure is the mechanism that prevents memory issues when data flows faster than it can be processed.

**Key benefits**: Memory efficiency, real-time processing, and built-in flow control for large datasets.

**Common use cases**: File processing, network communication, data transformation pipelines, and handling large files without loading everything into memory.

```javascript
const fs = require('fs');
const { Transform } = require('stream');

// Custom transform stream - converts text to uppercase
class UpperCaseTransform extends Transform {
    constructor() {
        super({ objectMode: true });
    }
    
    _transform(chunk, encoding, callback) {
        const upperChunk = chunk.toString().toUpperCase();
        this.push(upperChunk);
        callback();
    }
}

// File processing with streams - processes data in chunks
const readStream = fs.createReadStream('input.txt', { 
    highWaterMark: 64 * 1024 // 64KB chunks
});

const writeStream = fs.createWriteStream('output.txt');

const transformStream = new UpperCaseTransform();

// Handle backpressure - pauses reading when writing can't keep up
readStream.on('data', (chunk) => {
    const canContinue = writeStream.write(chunk);
    if (!canContinue) {
        readStream.pause();
    }
});

writeStream.on('drain', () => {
    readStream.resume();
});

// Pipe with error handling - creates a processing pipeline
readStream
    .pipe(transformStream)
    .pipe(writeStream)
    .on('error', (err) => {
        console.error('Stream error:', err);
    })
    .on('finish', () => {
        console.log('Processing complete');
    });
```

#### Async Patterns

**What they are**: Advanced patterns for handling asynchronous operations in Node.js, including utility functions for common async scenarios.

**Key patterns**: Promise utilities (delay, timeout, retry), async generators, and worker threads for CPU-intensive tasks.

**Common use cases**: API calls, database operations, file processing, and any operation that requires waiting for external resources.

```javascript
// Promise patterns - utility functions for common async scenarios
class PromiseUtils {
    static delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    static timeout(promise, ms) {
        return Promise.race([
            promise,
            new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Timeout')), ms)
            )
        ]);
    }
    
    static retry(fn, maxAttempts = 3, delay = 1000) {
        return async function(...args) {
            let lastError;
            for (let attempt = 1; attempt <= maxAttempts; attempt++) {
                try {
                    return await fn(...args);
                } catch (error) {
                    lastError = error;
                    if (attempt === maxAttempts) break;
                    await PromiseUtils.delay(delay * attempt);
                }
            }
            throw lastError;
        };
    }
}

// Async generator - yields values asynchronously
async function* asyncGenerator() {
    for (let i = 0; i < 5; i++) {
        await PromiseUtils.delay(100);
        yield i;
    }
}

// Worker threads - offload CPU-intensive tasks to separate threads
const { Worker, isMainThread, parentPort } = require('worker_threads');

if (isMainThread) {
    const worker = new Worker(__filename);
    worker.on('message', (result) => {
        console.log('Result:', result);
    });
    worker.postMessage({ data: [1, 2, 3, 4, 5] });
} else {
    parentPort.on('message', (message) => {
        const result = message.data.reduce((sum, num) => sum + num, 0);
        parentPort.postMessage(result);
    });
}
```

#### Express/Fastify Patterns

**What they are**: Common patterns and middleware implementations for Node.js web frameworks like Express and Fastify.

**Key patterns**: Authentication middleware, error handling, rate limiting, route organization, and request validation.

**Common use cases**: Building REST APIs, web applications, and microservices with proper security and error handling.

```javascript
// Express middleware pattern - modular request processing
const express = require('express');
const app = express();

// Authentication middleware - validates JWT tokens
const authenticate = (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
        return res.status(401).json({ error: 'No token provided' });
    }
    
    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
    } catch (error) {
        res.status(401).json({ error: 'Invalid token' });
    }
};

// Error handling middleware - centralized error processing
const errorHandler = (err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ 
        error: 'Something went wrong!',
        message: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
};

// Rate limiting middleware - prevents API abuse
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP'
});

// Route organization - modular API structure
const userRoutes = require('./routes/users');
const productRoutes = require('./routes/products');

app.use('/api/users', authenticate, userRoutes);
app.use('/api/products', productRoutes);
app.use(errorHandler);

// Fastify example - modern, fast web framework
const fastify = require('fastify')({ logger: true });

// Plugin system - modular feature registration
fastify.register(require('fastify-jwt'), {
    secret: process.env.JWT_SECRET
});

fastify.register(require('fastify-cors'), {
    origin: true
});

// Route with validation - automatic request validation
const userSchema = {
    type: 'object',
    properties: {
        name: { type: 'string', minLength: 1 },
        email: { type: 'string', format: 'email' }
    },
    required: ['name', 'email']
};

fastify.post('/users', {
    schema: {
        body: userSchema
    }
}, async (request, reply) => {
    const { name, email } = request.body;
    // Create user logic
    return { id: 1, name, email };
});
```

### NPM Ecosystem Best Practices

**What they are**: Best practices for managing Node.js projects, dependencies, and development workflows using npm and related tools.

**Key areas**: Script organization, dependency management, security practices, and development tooling.

**Common use cases**: Setting up development environments, managing project dependencies, and automating common development tasks.

```javascript
// Package.json scripts - automate common development tasks
{
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "build": "webpack --mode production",
    "docker:build": "docker build -t myapp .",
    "docker:run": "docker run -p 3000:3000 myapp"
  }
}

// Environment configuration
require('dotenv').config();

const config = {
    port: process.env.PORT || 3000,
    database: {
        url: process.env.DATABASE_URL,
        pool: {
            min: parseInt(process.env.DB_POOL_MIN) || 5,
            max: parseInt(process.env.DB_POOL_MAX) || 20
        }
    },
    redis: {
        url: process.env.REDIS_URL
    }
};

// Dependency injection
class UserService {
    constructor(database, cache) {
        this.database = database;
        this.cache = cache;
    }
    
    async getUser(id) {
        // Check cache first
        const cached = await this.cache.get(`user:${id}`);
        if (cached) return JSON.parse(cached);
        
        // Fetch from database
        const user = await this.database.query('SELECT * FROM users WHERE id = ?', [id]);
        
        // Cache for 5 minutes
        await this.cache.setex(`user:${id}`, 300, JSON.stringify(user));
        
        return user;
    }
}
```

---

## Bash Scripting Deep Dive

### System Administration Scripts

#### Process Management
```bash
#!/bin/bash

# Process monitoring script
monitor_process() {
    local process_name="$1"
    local max_cpu="$2"
    local max_memory="$3"
    
    while true; do
        # Get process info
        local pid=$(pgrep "$process_name")
        if [ -z "$pid" ]; then
            echo "$(date): Process $process_name not found"
            sleep 30
            continue
        fi
        
        # Get CPU and memory usage
        local cpu_usage=$(ps -p "$pid" -o %cpu --no-headers)
        local memory_usage=$(ps -p "$pid" -o %mem --no-headers)
        
        # Check thresholds
        if (( $(echo "$cpu_usage > $max_cpu" | bc -l) )); then
            echo "$(date): High CPU usage: ${cpu_usage}%"
            # Send alert or restart process
        fi
        
        if (( $(echo "$memory_usage > $max_memory" | bc -l) )); then
            echo "$(date): High memory usage: ${memory_usage}%"
            # Send alert or restart process
        fi
        
        sleep 60
    done
}

# Usage
monitor_process "nginx" 80 90
```

#### Log Analysis
```bash
#!/bin/bash

# Log analyzer
analyze_logs() {
    local log_file="$1"
    local output_file="$2"
    
    echo "Log Analysis Report - $(date)" > "$output_file"
    echo "================================" >> "$output_file"
    
    # Top IP addresses
    echo "Top 10 IP Addresses:" >> "$output_file"
    grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" "$log_file" | \
        sort | uniq -c | sort -nr | head -10 >> "$output_file"
    
    echo "" >> "$output_file"
    
    # Top user agents
    echo "Top 10 User Agents:" >> "$output_file"
    grep -oE "Mozilla/[^ ]*" "$log_file" | \
        sort | uniq -c | sort -nr | head -10 >> "$output_file"
    
    echo "" >> "$output_file"
    
    # Error analysis
    echo "Error Analysis:" >> "$output_file"
    grep -i "error\|exception\|fail" "$log_file" | \
        wc -l | xargs echo "Total errors:" >> "$output_file"
    
    # Response time analysis
    echo "Response Time Analysis:" >> "$output_file"
    grep -oE "response_time=[0-9.]+" "$log_file" | \
        sed 's/response_time=//' | \
        awk '{sum+=$1; count++} END {print "Average response time: " sum/count "ms"}' >> "$output_file"
}

# Usage
analyze_logs "/var/log/nginx/access.log" "log_report.txt"
```

#### Backup and Automation
```bash
#!/bin/bash

# Automated backup script
backup_database() {
    local db_name="$1"
    local backup_dir="$2"
    local retention_days="$3"
    
    # Create backup directory
    mkdir -p "$backup_dir"
    
    # Generate backup filename with timestamp
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$backup_dir/${db_name}_${timestamp}.sql"
    
    # Create backup
    if mysqldump -u root -p "$db_name" > "$backup_file"; then
        echo "$(date): Backup created: $backup_file"
        
        # Compress backup
        gzip "$backup_file"
        echo "$(date): Backup compressed: ${backup_file}.gz"
        
        # Clean old backups
        find "$backup_dir" -name "${db_name}_*.sql.gz" -mtime +"$retention_days" -delete
        echo "$(date): Old backups cleaned"
    else
        echo "$(date): Backup failed for $db_name"
        return 1
    fi
}

# System health check
system_health_check() {
    echo "System Health Check - $(date)"
    echo "================================"
    
    # Disk usage
    echo "Disk Usage:"
    df -h | grep -E '^/dev/'
    
    echo ""
    
    # Memory usage
    echo "Memory Usage:"
    free -h
    
    echo ""
    
    # Load average
    echo "Load Average:"
    uptime
    
    echo ""
    
    # Top processes
    echo "Top 5 CPU Processes:"
    ps aux --sort=-%cpu | head -6
    
    echo ""
    
    # Network connections
    echo "Active Network Connections:"
    netstat -tuln | grep LISTEN
}

# Cron job setup
setup_cron_jobs() {
    # Add backup job (daily at 2 AM)
    (crontab -l 2>/dev/null; echo "0 2 * * * /path/to/backup_script.sh") | crontab -
    
    # Add health check job (every 5 minutes)
    (crontab -l 2>/dev/null; echo "*/5 * * * * /path/to/health_check.sh") | crontab -
    
    # Add log rotation job (weekly)
    (crontab -l 2>/dev/null; echo "0 3 * * 0 /path/to/log_rotation.sh") | crontab -
}
```

### DevOps Automation

#### Docker Management
```bash
#!/bin/bash

# Docker container management
docker_cleanup() {
    echo "Cleaning up Docker resources..."
    
    # Remove stopped containers
    docker container prune -f
    
    # Remove unused images
    docker image prune -a -f
    
    # Remove unused volumes
    docker volume prune -f
    
    # Remove unused networks
    docker network prune -f
    
    echo "Docker cleanup completed"
}

# Docker health check
docker_health_check() {
    echo "Docker Health Check"
    echo "=================="
    
    # Check running containers
    echo "Running Containers:"
    docker ps --format "table {% raw %}{{.Names}}{% endraw %}\t{% raw %}{{.Status}}{% endraw %}\t{% raw %}{{.Ports}}{% endraw %}"
    
    echo ""
    
    # Check container resource usage
    echo "Container Resource Usage:"
    docker stats --no-stream --format "table {% raw %}{{.Container}}{% endraw %}\t{% raw %}{{.CPUPerc}}{% endraw %}\t{% raw %}{{.MemUsage}}{% endraw %}"
    
    echo ""
    
    # Check for unhealthy containers
    echo "Unhealthy Containers:"
    docker ps --filter "health=unhealthy" --format "table {% raw %}{{.Names}}{% endraw %}\t{% raw %}{{.Status}}{% endraw %}"
}

# Kubernetes management
k8s_management() {
    # Scale deployment
    scale_deployment() {
        local deployment="$1"
        local replicas="$2"
        kubectl scale deployment "$deployment" --replicas="$replicas"
    }
    
    # Check pod status
    check_pods() {
        kubectl get pods --all-namespaces -o wide
    }
    
    # Check node status
    check_nodes() {
        kubectl get nodes -o wide
    }
    
    # Check resource usage
    check_resources() {
        kubectl top nodes
        kubectl top pods --all-namespaces
    }
}
```

---

## React Deep Dive

### Component Patterns

#### Higher-Order Components (HOC)
```jsx
{% raw %}
// HOC for authentication
const withAuth = (WrappedComponent) => {
    return class extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                isAuthenticated: false,
                user: null,
                loading: true
            };
        }
        
        componentDidMount() {
            this.checkAuth();
        }
        
        checkAuth = async () => {
            try {
                const token = localStorage.getItem('token');
                if (token) {
                    const response = await fetch('/api/verify-token', {
                        headers: { Authorization: `Bearer ${token}` }
                    });
                    if (response.ok) {
                        const user = await response.json();
                        this.setState({ 
                            isAuthenticated: true, 
                            user, 
                            loading: false 
                        });
                    } else {
                        this.setState({ loading: false });
                    }
                } else {
                    this.setState({ loading: false });
                }
            } catch (error) {
                console.error('Auth check failed:', error);
                this.setState({ loading: false });
            }
        };
        
        render() {
            const { isAuthenticated, user, loading } = this.state;
            
            if (loading) {
                return <div>Loading...</div>;
            }
            
            if (!isAuthenticated) {
                return <LoginPage />;
            }
            
            return <WrappedComponent {...this.props} user={user} />;
        }
    };
};

// Usage
const ProtectedDashboard = withAuth(Dashboard);
{% endraw %}
```

#### Render Props Pattern
```jsx
{% raw %}
// Data fetcher with render props
class DataFetcher extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: null,
            loading: false,
            error: null
        };
    }
    
    componentDidMount() {
        this.fetchData();
    }
    
    fetchData = async () => {
        this.setState({ loading: true, error: null });
        try {
            const response = await fetch(this.props.url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            this.setState({ data, loading: false });
        } catch (error) {
            this.setState({ error: error.message, loading: false });
        }
    };
    
    render() {
        return this.props.children(this.state);
    }
}

// Usage
<DataFetcher url="/api/users">
    {({ data, loading, error }) => {
        if (loading) return <div>Loading...</div>;
        if (error) return <div>Error: {error}</div>;
        if (!data) return <div>No data</div>;
        
        return (
            <ul>
                {data.map(user => (
                    <li key={user.id}>{user.name}</li>
                ))}
            </ul>
        );
    }}
</DataFetcher>
{% endraw %}
```

#### Custom Hooks
```jsx
{% raw %}
// Custom hook for API calls
const useApi = (url, options = {}) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    const fetchData = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            setData(result);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [url, JSON.stringify(options)]);
    
    useEffect(() => {
        fetchData();
    }, [fetchData]);
    
    const refetch = useCallback(() => {
        fetchData();
    }, [fetchData]);
    
    return { data, loading, error, refetch };
};

// Custom hook for local storage
const useLocalStorage = (key, initialValue) => {
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error(error);
            return initialValue;
        }
    });
    
    const setValue = useCallback((value) => {
        try {
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error(error);
        }
    }, [key, storedValue]);
    
    return [storedValue, setValue];
};

// Custom hook for form validation
const useFormValidation = (initialValues, validationSchema) => {
    const [values, setValues] = useState(initialValues);
    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({});
    
    const handleChange = useCallback((name, value) => {
        setValues(prev => ({ ...prev, [name]: value }));
        
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    }, [errors]);
    
    const handleBlur = useCallback((name) => {
        setTouched(prev => ({ ...prev, [name]: true }));
        
        // Validate on blur
        if (validationSchema[name]) {
            const error = validationSchema[name](values[name]);
            setErrors(prev => ({ ...prev, [name]: error }));
        }
    }, [values, validationSchema]);
    
    const validate = useCallback(() => {
        const newErrors = {};
        Object.keys(validationSchema).forEach(field => {
            const error = validationSchema[field](values[field]);
            if (error) newErrors[field] = error;
        });
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    }, [values, validationSchema]);
    
    return {
        values,
        errors,
        touched,
        handleChange,
        handleBlur,
        validate
    };
};
{% endraw %}
```

### Performance Optimization

#### React.memo and useMemo
```jsx
{% raw %}
// Optimized component with React.memo
const ExpensiveComponent = React.memo(({ data, onAction }) => {
    // Expensive computation
    const processedData = useMemo(() => {
        console.log('Processing data...');
        return data.map(item => ({
            ...item,
            processed: item.value * 2 + Math.sqrt(item.value)
        }));
    }, [data]);
    
    return (
        <div>
            {processedData.map(item => (
                <div key={item.id}>
                    {item.name}: {item.processed}
                </div>
            ))}
        </div>
    );
});

// Virtual scrolling for large lists
const VirtualList = ({ items, itemHeight, containerHeight }) => {
    const [scrollTop, setScrollTop] = useState(0);
    
    const visibleItemCount = Math.ceil(containerHeight / itemHeight);
    const startIndex = Math.floor(scrollTop / itemHeight);
    const endIndex = Math.min(startIndex + visibleItemCount, items.length);
    
    const visibleItems = items.slice(startIndex, endIndex);
    const totalHeight = items.length * itemHeight;
    const offsetY = startIndex * itemHeight;
    
    return (
        <div 
            style={{ height: containerHeight, overflow: 'auto' }}
            onScroll={(e) => setScrollTop(e.target.scrollTop)}
        >
            <div style={{ height: totalHeight }}>
                <div style={{ transform: `translateY(${offsetY}px)` }}>
                    {visibleItems.map(item => (
                        <div key={item.id} style={{ height: itemHeight }}>
                            {item.content}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};
{% endraw %}
```

#### Code Splitting and Lazy Loading
```jsx
{% raw %}
// Lazy loading components
const LazyDashboard = React.lazy(() => import('./Dashboard'));
const LazySettings = React.lazy(() => import('./Settings'));
const LazyProfile = React.lazy(() => import('./Profile'));

// Route-based code splitting
const App = () => {
    return (
        <Router>
            <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                    <Route path="/dashboard" element={<LazyDashboard />} />
                    <Route path="/settings" element={<LazySettings />} />
                    <Route path="/profile" element={<LazyProfile />} />
                </Routes>
            </Suspense>
        </Router>
    );
};

// Dynamic imports for conditional loading
const useDynamicImport = (importFn, deps) => {
    const [Component, setComponent] = useState(null);
    const [loading, setLoading] = useState(false);
    
    useEffect(() => {
        setLoading(true);
        importFn()
            .then(module => {
                setComponent(() => module.default);
            })
            .catch(error => {
                console.error('Dynamic import failed:', error);
            })
            .finally(() => {
                setLoading(false);
            });
    }, deps);
    
    return { Component, loading };
};

// Usage
const MyComponent = () => {
    const { Component, loading } = useDynamicImport(
        () => import('./HeavyComponent'),
        []
    );
    
    if (loading) return <div>Loading...</div>;
    if (!Component) return <div>Failed to load component</div>;
    
    return <Component />;
};
{% endraw %}
```

### State Management Patterns

#### Context API with useReducer
```jsx
{% raw %}
// Global state management
const initialState = {
    user: null,
    theme: 'light',
    notifications: [],
    loading: false
};

const AppContext = React.createContext();

const appReducer = (state, action) => {
    switch (action.type) {
        case 'SET_USER':
            return { ...state, user: action.payload };
        case 'SET_THEME':
            return { ...state, theme: action.payload };
        case 'ADD_NOTIFICATION':
            return { 
                ...state, 
                notifications: [...state.notifications, action.payload] 
            };
        case 'REMOVE_NOTIFICATION':
            return { 
                ...state, 
                notifications: state.notifications.filter(
                    n => n.id !== action.payload 
                ) 
            };
        case 'SET_LOADING':
            return { ...state, loading: action.payload };
        default:
            return state;
    }
};

const AppProvider = ({ children }) => {
    const [state, dispatch] = useReducer(appReducer, initialState);
    
    const value = {
        ...state,
        setUser: (user) => dispatch({ type: 'SET_USER', payload: user }),
        setTheme: (theme) => dispatch({ type: 'SET_THEME', payload: theme }),
        addNotification: (notification) => 
            dispatch({ type: 'ADD_NOTIFICATION', payload: notification }),
        removeNotification: (id) => 
            dispatch({ type: 'REMOVE_NOTIFICATION', payload: id }),
        setLoading: (loading) => 
            dispatch({ type: 'SET_LOADING', payload: loading })
    };
    
    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    );
};

const useApp = () => {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error('useApp must be used within AppProvider');
    }
    return context;
};
{% endraw %}
```

---

## Key Takeaways

### **Python Mastery**
- **Decorators** for cross-cutting concerns and metaprogramming
- **Context managers** for resource management
- **Async/await** for concurrent programming
- **Metaclasses and descriptors** for advanced patterns

### **Node.js Expertise**
- **Event loop** understanding for performance optimization
- **Streams** for handling large data efficiently
- **Async patterns** for non-blocking operations
- **Express/Fastify** for building scalable APIs

### **Bash Scripting**
- **System administration** automation
- **Process monitoring** and management
- **Log analysis** and reporting
- **DevOps automation** with Docker and Kubernetes

### **React Patterns**
- **Component patterns** (HOC, render props, custom hooks)
- **Performance optimization** (memoization, code splitting)
- **State management** with Context API and useReducer
- **Advanced patterns** for scalable applications

*Master these patterns and you'll be well-prepared for any programming language or framework interview!*

---

# System Design & Architecture

## System Design Problems

## **🔧 Core System Design Concepts**

Before diving into specific problems, let's understand the fundamental concepts that appear throughout system design interviews.

---

### **🌐 WebSockets vs HTTP**

**WebSockets**
- **What**: Full-duplex communication channel over a single TCP connection
- **When to use**: Real-time applications (chat, gaming, live updates)
- **Benefits**: 
  - Persistent connection (no need to reconnect)
  - Bidirectional communication (client ↔ server)
  - Lower latency than HTTP polling
- **Drawbacks**: 
  - More complex to implement
  - Connection management overhead
  - Firewall/proxy issues

**HTTP (REST)**
- **What**: Request-response protocol, stateless
- **When to use**: CRUD operations, API endpoints, traditional web apps
- **Benefits**: 
  - Simple, stateless, cacheable
  - Works everywhere (browsers, mobile, APIs)
  - Easy to scale horizontally
- **Drawbacks**: 
  - Higher latency for real-time updates
  - Server can't push to client
  - Overhead of repeated connections

**Decision Framework**:
- Use **WebSockets** for: Real-time updates, bidirectional communication, low latency
- Use **HTTP** for: CRUD operations, stateless APIs, simple request-response

---

### **🔢 Base62 vs Base64 Encoding**

**Base62 Encoding**
- **What**: Uses 62 characters: A-Z, a-z, 0-9 (no special characters)
- **When to use**: URL shorteners, human-readable IDs, file names
- **Benefits**: 
  - URL-safe (no encoding needed)
  - Human-readable and memorable
  - Shorter than Base64 for same data
- **Example**: `abc123` instead of `YWJjMTIz`

**Base64 Encoding**
- **What**: Uses 64 characters: A-Z, a-z, 0-9, +, / (with padding =)
- **When to use**: Binary data in text, email attachments, API responses
- **Benefits**: 
  - Standard encoding for binary data
  - Efficient for data transfer
  - Widely supported
- **Drawbacks**: 
  - Not URL-safe (requires encoding)
  - Padding characters can cause issues

**Why Base62 for URLs?**
- **URL Safety**: No special characters that need encoding
- **Human Readable**: Easier to type and remember
- **Shorter**: More compact representation
- **No Padding**: Clean URLs without = characters

---

### **⏰ TTL (Time To Live)**

**What is TTL?**
- **Definition**: How long data should be considered valid before expiring
- **Purpose**: Automatic cleanup, cache invalidation, data freshness

**Common TTL Use Cases**:
1. **Cache Expiration**: Redis keys, CDN content
2. **Session Management**: User sessions, authentication tokens
3. **Rate Limiting**: Reset counters after time window
4. **Data Freshness**: Stale data cleanup, temporary data

**TTL Strategies**:
- **Fixed TTL**: Same expiration for all items
- **Variable TTL**: Different expiration based on data type
- **Sliding TTL**: Reset timer on access
- **Exponential TTL**: Increase expiration with usage

**Example Implementation**:
```python
# Redis TTL example
redis.setex("user_session:123", 3600, session_data)  # Expires in 1 hour
redis.expire("cache_key", 300)  # Set TTL to 5 minutes
```

---

### **📨 Message Brokers**

**What is a Message Broker?**
- **Definition**: Middleware that handles communication between different parts of a system
- **Purpose**: Decouple services, handle async processing, ensure message delivery

**Popular Message Brokers**:

**Apache Kafka**
- **Use Case**: High-throughput event streaming, log aggregation
- **Benefits**: 
  - Extremely high throughput (millions of messages/second)
  - Persistent storage, fault-tolerant
  - Horizontal scaling
- **Drawbacks**: 
  - Complex setup, overkill for simple use cases
  - Higher latency than in-memory solutions

**RabbitMQ**
- **Use Case**: Traditional message queuing, complex routing
- **Benefits**: 
  - Rich routing capabilities
  - Easy to set up and use
  - Good for complex workflows
- **Drawbacks**: 
  - Lower throughput than Kafka
  - Less suitable for event streaming

**Redis Pub/Sub**
- **Use Case**: Simple real-time messaging, notifications
- **Benefits**: 
  - Simple to implement
  - Low latency
  - Good for real-time features
- **Drawbacks**: 
  - No persistence
  - No guaranteed delivery
  - Limited scalability

**When to Use Each**:
- **Kafka**: High-volume event streaming, data pipelines
- **RabbitMQ**: Complex message routing, reliable delivery
- **Redis**: Simple real-time features, notifications

---

### **🖥️ Server vs Client Architecture**

**Client-Server Model**:
```
Client (Browser/Mobile) ←→ Server (Backend)
```

**Server Responsibilities**:
- **Business Logic**: Core application logic, data processing
- **Data Storage**: Database operations, file management
- **Authentication**: User verification, session management
- **API Endpoints**: REST/GraphQL interfaces
- **Security**: Input validation, rate limiting, authorization

**Client Responsibilities**:
- **User Interface**: UI rendering, user interactions
- **Data Display**: Presenting server data to users
- **Local State**: Form data, temporary storage
- **Network Requests**: API calls to server
- **Offline Handling**: Local caching, offline functionality

**Modern Variations**:
- **Single Page Application (SPA)**: Client handles routing, server provides APIs
- **Progressive Web App (PWA)**: Client can work offline, sync when online
- **Microservices**: Multiple specialized servers, client aggregates data

---

### **🔴 Redis (Remote Dictionary Server)**

**What is Redis?**
- **Definition**: In-memory data structure store, often used as cache
- **Key Feature**: Data stored in RAM for extremely fast access

**Redis Data Structures**:
1. **Strings**: Simple key-value pairs
   ```python
   redis.set("user:123", "John Doe")
   redis.get("user:123")  # Returns "John Doe"
   ```

2. **Hashes**: Field-value pairs within a key
   ```python
   redis.hset("user:123", "name", "John")
   redis.hset("user:123", "age", "30")
   redis.hgetall("user:123")  # Returns {"name": "John", "age": "30"}
   ```

3. **Lists**: Ordered collections
   ```python
   redis.lpush("queue", "task1")
   redis.rpop("queue")  # Returns "task1"
   ```

4. **Sets**: Unordered unique collections
   ```python
   redis.sadd("online_users", "user1")
   redis.sismember("online_users", "user1")  # Returns True
   ```

5. **Sorted Sets**: Ordered collections with scores
   ```python
   redis.zadd("leaderboard", {"player1": 100, "player2": 200})
   redis.zrevrange("leaderboard", 0, -1)  # Returns ["player2", "player1"]
   ```

**Redis Use Cases**:
- **Caching**: Store frequently accessed data
- **Session Storage**: User sessions, authentication
- **Rate Limiting**: Track request counts
- **Real-time Features**: Pub/Sub, live counters
- **Leaderboards**: Sorted sets for rankings

**Redis Trade-offs**:
- **Pros**: Extremely fast, rich data structures, persistence options
- **Cons**: Memory cost, single-threaded, limited by RAM size

---

### **🔒 Distributed Locks**

**What is a Distributed Lock?**
- **Definition**: Mechanism to ensure only one process can access a resource across multiple servers
- **Problem**: In distributed systems, multiple servers might try to access the same resource simultaneously

**Why Distributed Locks?**
- **Resource Contention**: Prevent multiple processes from modifying the same data
- **Race Conditions**: Ensure atomic operations across servers
- **Data Consistency**: Maintain integrity in distributed environments

**Implementation Strategies**:

**Redis-based Locks**:
```python
import redis
import time

def acquire_lock(lock_name, acquire_timeout=10, lock_timeout=10):
    """Acquire a distributed lock using Redis"""
    end = time.time() + acquire_timeout
    lock_value = str(time.time())
    
    while time.time() < end:
        if redis.set(lock_name, lock_value, ex=lock_timeout, nx=True):
            return lock_value
        time.sleep(0.001)
    return False

def release_lock(lock_name, lock_value):
    """Release a distributed lock"""
    script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    return redis.eval(script, 1, lock_name, lock_value)
```

**Zookeeper-based Locks**:
- **Use Case**: Complex coordination, leader election
- **Benefits**: Strong consistency, automatic cleanup
- **Drawbacks**: Higher latency, more complex setup

**Database-based Locks**:
- **Use Case**: Simple scenarios, when Redis isn't available
- **Benefits**: ACID guarantees, existing infrastructure
- **Drawbacks**: Higher latency, database load

**Lock Properties**:
- **Exclusivity**: Only one process holds the lock
- **Timeout**: Automatic expiration to prevent deadlocks
- **Reentrancy**: Same process can re-acquire lock
- **Fairness**: FIFO ordering of lock requests

---

### **🏗️ System Design Principles**

**1. Scalability**
- **Horizontal**: Add more servers (scale out)
- **Vertical**: Add more resources to existing servers (scale up)
- **Load Balancing**: Distribute traffic across multiple servers

**2. Availability**
- **Redundancy**: Multiple copies of critical components
- **Failover**: Automatic switching to backup systems
- **Health Checks**: Monitor system health and respond to failures

**3. Consistency**
- **Strong Consistency**: All reads see the latest write
- **Eventual Consistency**: Reads may see stale data temporarily
- **CAP Theorem**: Choose 2 out of 3: Consistency, Availability, Partition Tolerance

**4. Performance**
- **Latency**: Response time for individual requests
- **Throughput**: Number of requests handled per second
- **Caching**: Store frequently accessed data in fast storage

**5. Security**
- **Authentication**: Verify user identity
- **Authorization**: Control access to resources
- **Input Validation**: Prevent malicious input
- **Rate Limiting**: Prevent abuse

---

## 1. URL Shortener

**Requirements**
- Shorten long URLs to 6-8 character codes
- Redirect short URLs to original URLs
- Track click analytics
- Handle 100M+ URLs, 1000+ requests/second

**Design**
- **Short URL Generation**: Hash(long URL) → base62 encoding
- **Storage**: Redis for hot URLs, PostgreSQL for persistence
- **Database Schema**:
  ```sql
  urls (id, short_code, long_url, user_id, created_at, expires_at)
  clicks (id, short_code, ip, user_agent, timestamp, referrer)
  ```
- **Key Decisions**: Use hash-based generation (not sequential), TTL for unused URLs

**Trade-offs**
- Hash collisions: Use longer codes or collision resolution
- Analytics: Real-time vs batch processing
- Storage: Keep all URLs vs TTL expiration

---

## 2. Chat Application

**Requirements**
- Real-time messaging between users
- Group chats, direct messages
- Message persistence
- Online/offline status
- Handle 1M+ concurrent users

**Design**
- **Real-time**: WebSocket connections, message broker (Redis Pub/Sub)
- **Storage**: Messages in PostgreSQL, user status in Redis
- **Scaling**: Shard by user_id, use read replicas
- **Architecture**:
  ```
  Client → Load Balancer → WebSocket Server → Message Broker → Storage
  ```

**Trade-offs**
- Message ordering: Global vs per-chat ordering
- Persistence: All messages vs recent only
- Real-time: WebSocket vs Server-Sent Events vs Long Polling

---

## 3. Rate Limiter

**Requirements**
- Limit requests per user/IP
- Support different rate limits (per second, minute, hour)
- Handle distributed systems
- Configurable limits per endpoint

**Design**
- **Token Bucket**: Refill tokens at fixed rate, consume per request
- **Sliding Window**: Track requests in time windows
- **Implementation**: Redis with TTL, distributed locks
- **Storage**: Redis for counters, PostgreSQL for configuration

**Trade-offs**
- Accuracy: Fixed vs sliding windows
- Storage: In-memory vs distributed
- Granularity: Per-user vs per-IP vs per-endpoint

---

## 4. News Feed

**Requirements**
- Personalized feed for each user
- Real-time updates
- Handle 10M+ users, 1000+ posts/second
- Support different content types

**Design**
- **Fan-out on Write**: Pre-compute feeds when posts are created
- **Storage**: User feeds in Redis, posts in PostgreSQL
- **Scoring**: Time decay + engagement metrics
- **Architecture**:
  ```
  Post → Fan-out Workers → User Feed Stores → Aggregation → Client
  ```

**Trade-offs**
- Fan-out: Write vs Read (write for normal users, read for celebrities)
- Feed generation: Real-time vs batch
- Storage: Keep all posts vs TTL expiration

---

## 5. File Storage System

**Requirements**
- Store files up to 1GB
- Support multiple file types
- Handle 1000+ uploads/second
- Global distribution
- Backup and redundancy

**Design**
- **Storage**: Object storage (S3), CDN for distribution
- **Metadata**: PostgreSQL for file info, Redis for caching
- **Upload**: Chunked uploads, resume capability
- **Architecture**:
  ```
  Client → Load Balancer → Upload Service → Object Storage → CDN
  ```

**Trade-offs**
- Consistency: Strong vs eventual
- Storage: Hot vs cold storage tiers
- Backup: Synchronous vs asynchronous replication

---

## 6. Ride Hailing System

**Requirements**
- Match riders with drivers
- Real-time location tracking
- Handle 100K+ concurrent rides
- Support surge pricing
- Payment processing

**Design**
- **Matching**: Geospatial indexing (R-tree), real-time location updates
- **Storage**: PostgreSQL for rides, Redis for active sessions
- **Scaling**: Shard by geographic regions
- **Architecture**:
  ```
  Location Updates → Matching Engine → Driver Assignment → Payment
  ```

**Trade-offs**
- Matching: Real-time vs batch processing
- Location: GPS accuracy vs battery life
- Pricing: Dynamic vs fixed pricing

---

## 7. Notification System

**Requirements**
- Send notifications via email, SMS, push
- Support different notification types
- Handle 1M+ notifications/hour
- Delivery tracking
- Template management

**Design**
- **Queue**: Message broker (RabbitMQ/Kafka) for async processing
- **Templates**: Jinja2/Mustache for dynamic content
- **Delivery**: Multiple providers for redundancy
- **Storage**: PostgreSQL for templates, Redis for delivery status

**Trade-offs**
- Delivery: Synchronous vs asynchronous
- Providers: Single vs multiple for redundancy
- Templates: Dynamic vs static generation

---

## 8. Real-time Analytics

**Requirements**
- Track user events in real-time
- Support complex aggregations
- Handle 100K+ events/second
- Low-latency queries
- Historical data retention

**Design**
- **Streaming**: Apache Kafka for event ingestion
- **Processing**: Apache Flink/Spark for real-time aggregation
- **Storage**: Time-series database (InfluxDB), data warehouse
- **Architecture**:
  ```
  Events → Kafka → Stream Processor → Real-time Store → Query API
  ```

**Trade-offs**
- Latency: Real-time vs near-real-time
- Storage: Raw events vs pre-aggregated
- Processing: Stream vs batch processing

---

## 9. Feature Flags

**Requirements**
- Enable/disable features dynamically
- Support A/B testing
- Handle 10M+ requests/second
- Real-time configuration updates
- Audit trail

**Design**
- **Storage**: Redis for fast lookups, PostgreSQL for configuration
- **Distribution**: Pub/Sub for real-time updates
- **Evaluation**: Client-side vs server-side evaluation
- **Architecture**:
  ```
  Config Changes → Pub/Sub → Feature Service → Client Evaluation
  ```

**Trade-offs**
- Evaluation: Client vs server-side
- Storage: In-memory vs distributed
- Updates: Real-time vs eventual consistency

---

## 10. Video Streaming Platform

**Requirements**
- Stream videos in multiple qualities
- Support live and on-demand content
- Handle 1M+ concurrent viewers
- Global distribution
- Content recommendation

**Design**
- **Encoding**: Multiple bitrates, adaptive streaming (HLS/DASH)
- **Storage**: Object storage for video files, CDN for distribution
- **Streaming**: Edge servers, adaptive bitrate selection
- **Architecture**:
  ```
  Video Upload → Encoding → Storage → CDN → Client Player
  ```

**Trade-offs**
- Quality: Multiple bitrates vs single quality
- Storage: Hot vs cold storage
- Distribution: Global vs regional CDNs

---

## 11. Search Autocomplete

**Requirements**
- Suggest search terms as user types
- Support multiple languages
- Handle 10K+ requests/second
- Fast response (<100ms)
- Personalized suggestions

**Design**
- **Data Structure**: Trie for prefix matching
- **Storage**: In-memory for fast access, Redis for persistence
- **Scoring**: Frequency + recency + personalization
- **Architecture**:
  ```
  Query → Trie Lookup → Scoring → Personalization → Response
  ```

**Trade-offs**
- Accuracy: Global vs personalized suggestions
- Storage: In-memory vs distributed
- Updates: Real-time vs batch updates

---

## 12. API Gateway

**Requirements**
- Route requests to appropriate services
- Handle authentication/authorization
- Rate limiting and throttling
- Request/response transformation
- Load balancing

**Design**
- **Routing**: Path-based routing, service discovery
- **Security**: JWT validation, API key management
- **Scaling**: Horizontal scaling, health checks
- **Architecture**:
  ```
  Client → API Gateway → Authentication → Rate Limiter → Service Router
  ```

**Trade-offs**
- Security: Centralized vs distributed
- Routing: Static vs dynamic configuration
- Scaling: Monolithic vs microservices

---

## Common Patterns & Snippets

### Idempotent Endpoint
```python
def process_request(request_id, data):
    if processed(request_id):
        return get_stored_result(request_id)
    
    result = execute_business_logic(data)
    store_result(request_id, result)
    return result
```

### Retry with Jitter
```python
import random
import time

def retry_with_jitter(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
```

### Outbox Pattern
```python
def process_order(order_data):
    with transaction():
        # Business logic
        order = create_order(order_data)
        
        # Store event in outbox
        outbox_event = OutboxEvent(
            event_type="order_created",
            payload=order.to_dict(),
            status="pending"
        )
        db.session.add(outbox_event)
        db.session.commit()

# Background worker processes outbox
def process_outbox():
    events = OutboxEvent.query.filter_by(status="pending").limit(100)
    for event in events:
        publish_event(event.payload)
        event.status = "sent"
        db.session.commit()
```

---

## Design Decision Framework

### 1. Functional Requirements
- What does the system need to do?
- What are the input/output formats?
- What are the business rules?

### 2. Non-Functional Requirements
- **Scalability**: How many users/requests?
- **Performance**: Response time, throughput?
- **Availability**: Uptime requirements?
- **Consistency**: Data consistency needs?

### 3. Constraints
- **Technical**: Technology stack, team expertise
- **Business**: Budget, timeline, compliance
- **Operational**: Monitoring, maintenance, support

### 4. Trade-offs Analysis
- **Performance vs Scalability**: Optimize for speed vs growth
- **Consistency vs Availability**: CAP theorem choices
- **Complexity vs Maintainability**: Simple vs robust solutions

### 5. Estimation
- **Storage**: Data size, growth rate
- **Bandwidth**: Request/response sizes
- **Compute**: CPU/memory requirements
- **Cost**: Infrastructure and operational costs

---

## Data Layer & Databases

## **📚 Database Fundamentals & Definitions**

Before diving into advanced concepts, let's understand the fundamental database types and terminology.

---

### **🗄️ SQL vs NoSQL: What Are They?**

**SQL (Structured Query Language)**
- **What**: Standard language for managing relational databases
- **Definition**: A programming language designed for managing and querying data in relational database management systems (RDBMS)
- **Key Characteristics**: 
  - Structured, tabular data with predefined schemas
  - ACID compliance for data integrity
  - Strong consistency guarantees
  - Complex queries with JOINs and transactions

**NoSQL (Not Only SQL)**
- **What**: Non-relational database systems designed for specific data models
- **Definition**: Database systems that store and retrieve data in non-tabular form, often optimized for specific use cases
- **Key Characteristics**:
  - Flexible schemas that can evolve over time
  - Often sacrifice ACID for performance and scalability
  - Designed for horizontal scaling
  - Specialized for specific data patterns

---

### **🏗️ Database Categories Explained**

#### **1. Relational Databases (SQL)**
**What They Are**: Databases that organize data into tables with rows and columns, where relationships between data are defined by foreign keys.

**Core Concepts**:
- **Tables**: Collections of related data (e.g., users, orders, products)
- **Rows**: Individual records in a table
- **Columns**: Attributes or fields for each record
- **Relationships**: Connections between tables using foreign keys
- **Schema**: The structure that defines tables, columns, and relationships

**Examples**: PostgreSQL, MySQL, Oracle, SQL Server, SQLite

**When to Use**:
- ✅ **Structured data** with clear relationships
- ✅ **ACID compliance** required (banking, financial systems)
- ✅ **Complex queries** with JOINs and aggregations
- ✅ **Data integrity** is critical
- ❌ **Rapid schema changes** needed
- ❌ **Massive horizontal scaling** required

#### **2. Key-Value Stores (NoSQL)**
**What They Are**: Simple databases that store data as key-value pairs, where each key maps to a single value.

**Core Concepts**:
- **Key**: Unique identifier (usually a string)
- **Value**: Data associated with the key (can be simple or complex)
- **No Schema**: Values can be any type without predefined structure
- **Fast Lookups**: O(1) average time complexity for key-based access

**Examples**: Redis, DynamoDB, Riak, Memcached

**When to Use**:
- ✅ **Simple data models** (user sessions, caching)
- ✅ **High-performance lookups** by key
- ✅ **Session storage** and temporary data
- ✅ **Real-time counters** and simple state
- ❌ **Complex queries** or relationships
- ❌ **Data that needs** complex aggregations

#### **3. Document Databases (NoSQL)**
**What They Are**: Databases that store data in flexible, JSON-like documents that can have different structures.

**Core Concepts**:
- **Documents**: Self-contained data units (usually JSON/BSON)
- **Collections**: Groups of related documents
- **Embedded Data**: Related information can be nested within documents
- **Schema Flexibility**: Documents can have different fields and structures

**Examples**: MongoDB, Couchbase, CouchDB, Firestore

**When to Use**:
- ✅ **Flexible schemas** that evolve over time
- ✅ **Hierarchical data** (nested objects, arrays)
- ✅ **Content management** systems
- ✅ **Product catalogs** with varying attributes
- ❌ **Complex transactions** across documents
- ❌ **Data with many relationships** between entities

#### **4. Column-Family Stores (NoSQL)**
**What They Are**: Databases that store data in columns rather than rows, optimized for reading and writing large amounts of data.

**Core Concepts**:
- **Column Families**: Groups of related columns
- **Wide Rows**: Each row can have many columns
- **Column-Oriented**: Data is stored by column, not by row
- **Time-Series Friendly**: Excellent for data that changes over time

**Examples**: Cassandra, HBase, Bigtable, ScyllaDB

**When to Use**:
- ✅ **Time-series data** (logs, metrics, IoT data)
- ✅ **High write throughput** requirements
- ✅ **Analytics and reporting** workloads
- ✅ **Data warehousing** and large-scale storage
- ❌ **Complex transactions** or relationships
- ❌ **Frequent schema changes**

#### **5. Graph Databases (NoSQL)**
**What They Are**: Databases designed to store and query relationships between entities, treating relationships as first-class citizens.

**Core Concepts**:
- **Nodes**: Entities or objects in the graph
- **Edges**: Relationships between nodes
- **Properties**: Attributes stored on both nodes and edges
- **Traversals**: Navigation through connected data

**Examples**: Neo4j, ArangoDB, Amazon Neptune, OrientDB

**When to Use**:
- ✅ **Complex relationships** between entities
- ✅ **Social networks** and recommendation engines
- ✅ **Fraud detection** and network analysis
- ✅ **Knowledge graphs** and semantic search
- ❌ **Simple CRUD operations** without relationships
- ❌ **Traditional reporting** and analytics

#### **6. Search Engines (Specialized NoSQL)**
**What They Are**: Databases optimized for full-text search, complex queries, and text-based analytics.

**Core Concepts**:
- **Inverted Indexes**: Maps terms to documents containing them
- **Text Analysis**: Tokenization, stemming, and language processing
- **Scoring**: Relevance ranking for search results
- **Aggregations**: Complex analytics on search results

**Examples**: Elasticsearch, OpenSearch, Solr, Algolia

**When to Use**:
- ✅ **Full-text search** requirements
- ✅ **Log analysis** and monitoring
- ✅ **Content search** and discovery
- ✅ **Real-time analytics** on text data
- ❌ **Primary data storage** (use as secondary)
- ❌ **ACID transactions** or strong consistency

---

### **🔄 ACID vs BASE: Transaction Models**

#### **ACID (Traditional SQL)**
**Atomicity**: All operations in a transaction succeed or fail together
**Consistency**: Data moves from one valid state to another
**Isolation**: Concurrent transactions don't interfere with each other
**Durability**: Committed changes survive system failures

**Use Cases**: Banking, financial systems, inventory management, any system where data integrity is critical

#### **BASE (Common in NoSQL)**
**Basically Available**: System guarantees availability over consistency
**Soft State**: Data may change over time due to eventual consistency
**Eventual Consistency**: System will become consistent over time if no new updates occur

**Use Cases**: Social media, content management, real-time analytics, systems where availability is more important than immediate consistency

---

### **📊 CAP Theorem: The Fundamental Trade-off**

**What is CAP Theorem?**
In distributed database systems, you can only guarantee **2 out of 3** properties:

1. **Consistency (C)**: All nodes see the same data at the same time
2. **Availability (A)**: Every request receives a response
3. **Partition Tolerance (P)**: System continues operating despite network failures

**Real-World Implications**:
- **CP Systems**: Choose consistency over availability (banking, financial)
- **AP Systems**: Choose availability over consistency (social media, content)
- **CA Systems**: Only possible in single-node systems (not truly distributed)

---

## 1. Key Theoretical Foundations

### **CAP Theorem**

- A distributed database can only guarantee **two** out of three:

  - **Consistency (C):** every read returns the latest write.
  - **Availability (A):** every request receives a response (even if not the latest).
  - **Partition Tolerance (P):** system continues despite dropped/delayed messages.

**Tradeoffs:**

- **CP (Consistency + Partition Tolerance):** strict correctness, lower availability → banking, financial systems.
- **AP (Availability + Partition Tolerance):** eventual consistency, high availability → social media, caching layers.
- **CA (Consistency + Availability):** only realistic in single-node or non-partitioned systems.

---

### **ACID Transactions**

- **Atomicity** → All or nothing (no partial writes).
- **Consistency** → Data moves from one valid state to another.
- **Isolation** → Transactions don’t interfere with each other.
- **Durability** → Committed changes survive crashes.

**Example (Bank Transfer):**

```
begin transaction
    debit Alice $100
    credit Bob $100
commit
```

If the system crashes mid-way, rollback ensures no partial transfer.

---

### **BASE Model** (common in NoSQL)

- **Basically Available:** system guarantees availability.
- **Soft state:** data may change over time (due to eventual consistency).
- **Eventual consistency:** if no updates occur, replicas converge.

---

## 2. Database Types & Design Choices

| Type                 | Example Systems            | Strengths                                             | Limitations                                   | When to Use                                     |
| -------------------- | -------------------------- | ----------------------------------------------------- | --------------------------------------------- | ----------------------------------------------- |
| **Relational (SQL)** | PostgreSQL, MySQL, Oracle  | Strong consistency, ACID, rich queries (SQL, joins)   | Harder to scale horizontally, schema rigidity | Banking, ERP, analytics with strong correctness |
| **Key-Value**        | Redis, DynamoDB, Riak      | Very fast lookups, simple model                       | No joins, limited query flexibility           | Caching, session stores, user profiles          |
| **Document**         | MongoDB, Couchbase         | Flexible schema, hierarchical docs                    | Joins are weak, eventual consistency common   | CMS, product catalogs, flexible JSON data       |
| **Columnar**         | Cassandra, HBase, Bigtable | Wide-column storage, great for writes and time series | Complex setup, weaker joins                   | Logging, time series, IoT data                  |
| **Graph**            | Neo4j, ArangoDB            | Optimized for relationships (edges)                   | Slower for non-graph workloads                | Social networks, recommendation engines         |

---

## 3. Core Database Concepts

### Indexing

- **B-Tree indexes:** balanced, efficient for range queries.
- **Hash indexes:** O(1) lookups but poor for ranges.
- **Covering indexes:** include all queried columns → avoid table lookups.
- **Tradeoff:** faster reads but slower writes (maintaining index).

### Normalization vs Denormalization

- **Normalization:** reduce redundancy (3NF/BCNF), consistent updates, smaller storage.
- **Denormalization:** duplicate data for faster queries, common in OLAP/NoSQL.

### Scaling Approaches

- **Replication:** copies of data for HA/reads.
- **Sharding:** horizontal partitioning across servers.
- **Caching:** use Redis/Memcached to reduce DB load.
- **Event sourcing / CQRS:** separate read vs write models.

---

## 4. Patterns in System Design Interviews

- **Use SQL** when correctness, transactions, and structured queries matter.
- **Use NoSQL (KV/Doc/Column)** when availability, scale, and flexibility matter.
- **Mix approaches:** e.g., use PostgreSQL for core financial records, Redis for session caching, ElasticSearch for logs/queries.

---

| Type                                  | Example Systems                                           | **CAP Posture (typical)**                          | Strengths                                                               | Limitations                                                             | Common Uses                                             |
| ------------------------------------- | --------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------- |
| **Relational (SQL)**                  | PostgreSQL, MySQL (single-node)                           | **CA\***                                           | Strong consistency on a single node, ACID, rich SQL/joins               | Vertical scaling limits; schema rigidity                                | OLTP, finance, ERP, analytics where correctness matters |
| **Relational (clustered/replicated)** | Postgres w/ sync replicas, Galera/MySQL Group Replication | **CP (sync quorum)** / **AP-ish (async replicas)** | ACID with high correctness; can survive node loss with quorum           | May refuse writes under partition (CP); async replicas risk stale reads | High-integrity systems needing HA                       |
| **Key–Value**                         | **DynamoDB**                                              | **AP (tunable)**                                   | Massive scale, predictable latency; eventual or strong reads selectable | Limited querying/joins; modeling discipline needed                      | Caching, user profiles, session stores                  |
|                                       | **Redis (standalone)**                                    | **CA\***                                           | Extremely fast, simple; great cache                                     | Single-node unless clustered; no durability by default                  | Caching, rate limiting, queues                          |
|                                       | **Redis Cluster**                                         | **AP (tunable)**                                   | Scales horizontally, high throughput                                    | Eventual consistency windows; key-hash slotting constraints             | Distributed cache, pub/sub                              |
| **Document**                          | **MongoDB (replica set)**                                 | **CP (tunable)**                                   | Flexible schema (JSON/BSON), rich queries & indexes                     | Cross-document transactions newer/limited by design                     | Content mgmt, product catalogs                          |
| **Wide-Column**                       | **Cassandra**                                             | **AP**                                             | Writes-first design, linear scalability, multi-DC friendly              | Eventual consistency; complex data modeling                             | Time-series, logging, large-scale writes                |
|                                       | **HBase / Bigtable**                                      | **CP**                                             | Strong consistency, huge tables, range scans                            | Operationally heavier; limited ad-hoc queries                           | Analytics backends, large KV/range workloads            |
| **Search**                            | Elasticsearch, OpenSearch                                 | **AP (tunable)**                                   | Full-text search, aggregations, near-real-time                          | Eventual consistency; not a primary source of truth                     | Search, logs, analytics                                 |
| **Graph**                             | Neo4j, ArangoDB                                           | **CA\*** (single-node) / **CP (cluster)**          | Efficient traversals, relationship-heavy queries                        | Not ideal for wide scans/OLAP                                           | Social graphs, recommendations                          |

\* **CA** is only meaningful when there’s effectively **no partition** (e.g., single-node or same-box). In real distributed settings you must pick between **CP** and **AP** under partitions.
**Tunable** = posture can be adjusted (e.g., quorum reads/writes, read/write concerns).

If you want, I can drop this directly into the Data Layer section and keep going with **indexing strategies, normalization vs. denormalization, replication vs. sharding, and caching**—all in the same reference style.

# Indexing Strategies

### What is an index?

A secondary data structure that lets the database find rows **without scanning the whole table**.

### Common Index Types

| Index              | Best For                                                | Notes                                                           |
| ------------------ | ------------------------------------------------------- | --------------------------------------------------------------- |
| **B-Tree**         | Range scans, ordering (`BETWEEN`, `<`, `>`, `ORDER BY`) | Default in most RDBMS; balanced tree keeps O(log n) lookups     |
| **Hash**           | Exact matches (`=`)                                     | No range scans; O(1) average lookups                            |
| **GIN / GIST**     | Full-text, arrays, geo                                  | Postgres: GIN for inverted (contains), GiST for spatial/nearest |
| **Bitmap**         | Low-cardinality columns                                 | Often used in data warehouses for analytics                     |
| **Covering Index** | Query can be answered by the index alone                | Add **included** columns so base table lookup is avoided        |

### General Rules

- Index **what you filter on**, not what you select.
- **Equality first**, then range: compound indexes should match query predicates’ order (e.g., `WHERE a = ? AND b = ? AND c > ?` → index `(a, b, c)`).
- **High cardinality** columns benefit more (e.g., user_id > gender).
- Too many indexes **slow writes** (each insert/update must update indexes).

### SQL Snippets (PostgreSQL-flavored)

```sql
-- B-Tree (default)
CREATE INDEX idx_users_email ON users(email);

-- Composite index (equality, equality, then range)
CREATE INDEX idx_orders_user_date ON orders(user_id, status, created_at);

-- Partial index (only for active rows)
CREATE INDEX idx_active_users_email ON users(email) WHERE is_active = true;

-- Covering index (include extra columns)
CREATE INDEX idx_orders_lookup ON orders(order_id) INCLUDE (total_amount, status);

-- Full-text (GIN)
CREATE INDEX idx_docs_ft ON docs USING GIN (to_tsvector('english', body));
```

**Gotchas**

- **Leading column** matters in composite indexes. Query must use the leftmost parts to benefit.
- **Function indexes** require the query to use the same function (`LOWER(email)`).
- **Selectivity**: Indexes on low-selectivity columns (e.g., boolean) rarely help.

---

# Normalization vs Denormalization

### Normalization (3NF+)

- **Goal:** eliminate redundancy, maintain consistency.
- **Pros:** smaller data, consistent updates, fewer anomalies.
- **Cons:** more joins; sometimes slower reads.

### Denormalization

- **Goal:** speed reads by duplicating/aggregating data.
- **Pros:** fewer joins, faster read queries.
- **Cons:** write complexity; need **fan-out updates** or **background jobs** to keep in sync.

### When to Use

- **OLTP systems** (high write correctness): normalize first; denormalize selectively with materialized views/caches.
- **OLAP / analytics**: star/snowflake schemas, aggressive denormalization for read speed.

**Pattern**: Start normalized → measure → denormalize **targeted hot paths**.

---

# Replication vs Sharding

### Replication (Copy the same data to multiple nodes)

- **Synchronous:** writes wait for replicas → **CP** flavor (lower availability if replicas unreachable, but consistent).
- **Asynchronous:** leader commits and returns → **AP-ish** (stale reads possible).
- **Use for:** high availability (HA), read scaling (read replicas), DR.

**Terms**

- **Leader-Follower** (Primary-Replica)
- **Multi-leader** (conflict resolution needed)
- **Quorum** (R/W majority votes; tunable consistency)

**Example Read Scaling**

- Send writes to **leader**; send heavy reports to **read replicas**.

### Sharding (Horizontal partitioning; split data across nodes)

- **Key-based** (hash user_id) → even distribution, but hard to do cross-shard joins.
- **Range-based** (by date/id range) → easy range scans, risk hot shards.
- **Directory/Lookup** (custom routing service) → flexible, operationally complex.

**When to Shard**

- Dataset won’t fit on a single node / vertical scaling exhausted.
- Single-node write throughput maxed out.

**Cross-shard Challenges**

- **Joins**: push down computations or pre-aggregate.
- **Transactions**: need 2PC/sagas; prefer **idempotent** operations.
- **Rebalancing**: plan for adding shards (consistent hashing helps).

---

# Caching (and Layers)

### Why Cache?

Reduce latency and database load by serving hot data from memory.

### Types of Caches

| Layer                 | Example                  | Pros                   | Cons                          |
| --------------------- | ------------------------ | ---------------------- | ----------------------------- |
| **Client-side**       | Browser cache            | Zero network hops      | Stale control limited         |
| **CDN/Edge**          | CloudFront, Fastly       | Global low-latency     | Purge/invalidation needed     |
| **Application cache** | In-process LRU           | Ultra fast             | Memory pressure; not shared   |
| **Distributed cache** | Redis, Memcached         | Shared across services | Network hop; consistency risk |
| **Database cache**    | Buffer pool, query cache | Transparent            | DB-specific behavior          |

### Caching Strategies

- **Cache-aside (lazy):** app reads cache, on miss load DB then write cache.

  - Simple; stale possible until TTL expires.

- **Write-through:** write to cache and DB simultaneously.

  - Safer reads; writes slower.

- **Write-back:** write to cache, flush to DB later.

  - Fast writes; risk data loss without durability.

- **Read-through:** cache sits in front of DB transparently.

  - Managed by cache layer/provider.

### Redis Patterns

```python
# Cache-aside (pseudo/Python)
value = redis.get(key)
if value is None:
    value = db.read(key)
    redis.setex(key, ttl_seconds, serialize(value))
return value
```

**Invalidation**

- TTLs on keys, **versioned keys** (`user:123:v42`) to avoid thundering herds.
- **Pub/Sub** or **streams** to broadcast invalidations on updates.

**Gotchas**

- **Stale reads** (eventual consistency).
- **Hot keys** (use sharding or probabilistic caching).
- **Stampede**: use **singleflight**/locks or **randomized TTL** to spread expiries.

---

# Putting It Together — Quick Decision Guide

- **Need strict correctness & joins?** Start with **PostgreSQL** (normalized).
- **Read-heavy & scale-out?** Add **read replicas** (async replication).
- **Global latency?** Add **CDN/edge** and regional **caches** (Redis).
- **Write throughput wall / dataset too large?** **Shard** by user or time.
- **Slow queries?** Add **indexes** (B-Tree for ranges; composite for equality+range; GIN for text/arrays).
- **Analytics?** Denormalize into **warehouse** (star schema) or use **columnar** stores.

---

If you want, I can now fold these sections into your master document and then move on to the **DevOps & Cloud** chapter (Terraform/IaC with CLI & examples, AWS/Azure/GCP core services, CI/CD including Jenkins, Observability with CloudWatch/Splunk/New Relic, Chaos Engineering tools, Containers beyond Docker, Security/HIPAA).

---

## Design Patterns

Design patterns are reusable solutions to common software design problems. They provide a shared vocabulary and help create maintainable, scalable code.

---

## 1. Creational Patterns

### Singleton Pattern

**What it is**: Ensures a class has only one instance and provides global access to it.

**Why Singleton is NOT just a constant**:
- **Constants are static values** that don't change and don't have behavior
- **Singleton is a class instance** that can have state, methods, and complex behavior
- **Constants are created at compile time** and exist throughout program execution
- **Singleton can be lazy-initialized** (only created when first needed)
- **Constants don't maintain state** between operations
- **Singleton can have mutable state** that changes over time
- **Constants can't be mocked** or replaced for testing
- **Singleton can implement interfaces** and be polymorphic

**Real-world analogy**: Think of a **constant** as a street sign (fixed, unchanging) vs. a **Singleton** as a traffic light controller (has state, behavior, and can change over time).

**When to use**: 
- Database connections (needs connection pooling, state management)
- Logger instances (needs to maintain log levels, handlers, state)
- Configuration managers (needs to load config, cache values, handle updates)
- Cache managers (needs to maintain cache state, eviction policies)
- Service locators (needs to manage service instances, lifecycle)
- Thread pools (needs to manage worker threads, queue state)

**Implementation**:
```python
class Singleton:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Prevent multiple initializations
        if not self._initialized:
            self._initialized = True
            self._data = {}
            self._counter = 0
    
    def set_data(self, key, value):
        self._data[key] = value
        self._counter += 1
    
    def get_data(self, key):
        return self._data.get(key)
    
    def get_counter(self):
        return self._counter

# Alternative with decorator
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self):
        self.connection_string = "db://localhost:5432"
        self.connection_pool = []
        self.active_connections = 0
    
    def get_connection(self):
        if not self.connection_pool:
            # Create new connection
            self.active_connections += 1
            return f"Connection_{self.active_connections}"
        return self.connection_pool.pop()
    
    def return_connection(self, connection):
        self.connection_pool.append(connection)
    
    def get_stats(self):
        return {
            'pool_size': len(self.connection_pool),
            'active_connections': self.active_connections
        }

# Thread-safe Singleton (Python 3.7+)
import threading
from typing import Optional

class ThreadSafeSingleton:
    _instance: Optional['ThreadSafeSingleton'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'ThreadSafeSingleton':
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking pattern
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

**Advanced Singleton Patterns**:

**1. Monostate Pattern** (Shared State):
```python
class Monostate:
    _shared_state = {}
    
    def __init__(self):
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self._shared_state['data'] = {}
            self._shared_state['counter'] = 0
    
    def set_data(self, key, value):
        self._shared_state['data'][key] = value
        self._shared_state['counter'] += 1
    
    def get_data(self, key):
        return self._shared_state['data'].get(key)
```

**2. Borg Pattern** (Python-specific):
```python
class Borg:
    _shared_state = {}
    
    def __init__(self):
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self._shared_state['data'] = {}
            self._shared_state['counter'] = 0
```

**3. Singleton Registry** (Multiple Singletons):
```python
class SingletonRegistry:
    _instances = {}
    
    @classmethod
    def get_instance(cls, class_name):
        if class_name not in cls._instances:
            cls._instances[class_name] = type(class_name, (), {})()
        return cls._instances[class_name]
    
    @classmethod
    def clear(cls):
        cls._instances.clear()

# Usage
logger = SingletonRegistry.get_instance('Logger')
cache = SingletonRegistry.get_instance('Cache')
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - ✅ **Guarantees single instance** across the entire application
  - ✅ **Lazy initialization** (only created when first needed)
  - ✅ **Global access point** for shared resources
  - ✅ **Resource management** (connection pooling, caching)
  - ✅ **State persistence** across multiple calls
  - ✅ **Configuration management** (load once, use everywhere)
- **Costs**: 
  - ❌ **Global state** (hard to test and debug)
  - ❌ **Violates single responsibility principle** (manages both creation and behavior)
  - ❌ **Can be difficult to mock** in unit tests
  - ❌ **Tight coupling** (hard to replace or extend)
  - ❌ **Memory leaks** if not properly managed
  - ❌ **Thread safety issues** in multi-threaded environments
- **Use when**: 
  - You need exactly one instance and global access
  - The instance needs to maintain state over time
  - Resource management is critical (connections, caches)
  - Configuration needs to be shared across the application

**Anti-patterns to avoid**:
- **God Object**: Don't make the Singleton do everything
- **Tight Coupling**: Don't force other classes to depend on the Singleton
- **Global Mutable State**: Be careful with shared state that can change
- **Overuse**: Don't use Singleton for every class that should have one instance

**Testing Strategies**:
```python
# Reset Singleton for testing
class TestableSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset the singleton instance (for testing)"""
        cls._instance = None

# In tests
def test_singleton():
    # Reset before each test
    TestableSingleton.reset()
    instance1 = TestableSingleton()
    instance2 = TestableSingleton()
    assert instance1 is instance2
```

**Real-world Examples**:

**1. Database Connection Pool**:
```python
@singleton
class DatabasePool:
    def __init__(self):
        self.connections = []
        self.max_connections = 10
        self.active_connections = 0
    
    def get_connection(self):
        if self.connections:
            return self.connections.pop()
        elif self.active_connections < self.max_connections:
            self.active_connections += 1
            return self._create_connection()
        else:
            raise Exception("No available connections")
    
    def return_connection(self, connection):
        self.connections.append(connection)
    
    def _create_connection(self):
        # Create new database connection
        return f"DB_Connection_{self.active_connections}"
```

**2. Configuration Manager**:
```python
@singleton
class ConfigManager:
    def __init__(self):
        self._config = {}
        self._load_config()
    
    def _load_config(self):
        # Load from file, environment, etc.
        self._config = {
            'database_url': 'postgresql://localhost:5432/mydb',
            'redis_url': 'redis://localhost:6379',
            'log_level': 'INFO',
            'max_workers': 4
        }
    
    def get(self, key, default=None):
        return self._config.get(key, default)
    
    def set(self, key, value):
        self._config[key] = value
        # Could also persist to file/database
    
    def reload(self):
        self._load_config()
```

**3. Logger with State**:
```python
@singleton
class Logger:
    def __init__(self):
        self.log_level = 'INFO'
        self.handlers = []
        self.log_history = []
    
    def set_level(self, level):
        self.log_level = level
    
    def add_handler(self, handler):
        self.handlers.append(handler)
    
    def log(self, level, message):
        if self._should_log(level):
            timestamp = datetime.now()
            log_entry = {'level': level, 'message': message, 'timestamp': timestamp}
            self.log_history.append(log_entry)
            
            for handler in self.handlers:
                handler.handle(log_entry)
    
    def _should_log(self, level):
        levels = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 4}
        return levels.get(level, 0) >= levels.get(self.log_level, 0)
    
    def get_history(self):
        return self.log_history.copy()
```

**When NOT to use Singleton**:
- **Simple configuration**: Use environment variables or config files
- **Stateless utilities**: Use static methods or utility classes
- **Testable code**: Prefer dependency injection
- **Multiple instances needed**: Use factory pattern instead
- **Temporary state**: Use regular objects with proper lifecycle management

---

### Factory Pattern

**What it is**: Creates objects without specifying their exact class.

**When to use**:
- Object creation depends on runtime conditions
- You want to delegate object creation to subclasses
- You want to create families of related objects

**Implementation**:
```python
from abc import ABC, abstractmethod

# Abstract product
class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

# Concrete products
class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

# Factory
class AnimalFactory:
    def create_animal(self, animal_type):
        if animal_type.lower() == "dog":
            return Dog()
        elif animal_type.lower() == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")

# Usage
factory = AnimalFactory()
dog = factory.create_animal("dog")
print(dog.speak())  # Output: Woof!
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Encapsulates object creation logic
  - Easy to add new product types
  - Follows open/closed principle
- **Costs**: 
  - Adds complexity
  - Can lead to many small classes
- **Use when**: Object creation logic is complex or varies

---

### Builder Pattern

**What it is**: Constructs complex objects step by step.

**When to use**:
- Objects with many optional parameters
- Objects that require different construction steps
- Immutable objects

**Implementation**:
```python
class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None
    
    def __str__(self):
        return f"Computer(CPU: {self.cpu}, RAM: {self.ram}, Storage: {self.storage}, GPU: {self.gpu})"

class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()
    
    def set_cpu(self, cpu):
        self.computer.cpu = cpu
        return self
    
    def set_ram(self, ram):
        self.computer.ram = ram
        return self
    
    def set_storage(self, storage):
        self.computer.storage = storage
        return self
    
    def set_gpu(self, gpu):
        self.computer.gpu = gpu
        return self
    
    def build(self):
        return self.computer

# Usage
computer = (ComputerBuilder()
           .set_cpu("Intel i7")
           .set_ram("16GB")
           .set_storage("1TB SSD")
           .set_gpu("RTX 3080")
           .build())
print(computer)
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Fluent interface
  - Immutable objects
  - Clear construction process
- **Costs**: 
  - More code
  - Can be overkill for simple objects
- **Use when**: Objects have many optional parameters or complex construction

---

## 2. Structural Patterns

### Adapter Pattern

**What it is**: Allows incompatible interfaces to work together.

**When to use**:
- Integrating third-party libraries
- Making old code work with new interfaces
- Supporting multiple data formats

**Implementation**:
```python
# Old interface
class OldPaymentSystem:
    def make_payment(self, amount, currency):
        print(f"Paid {amount} {currency} using old system")

# New interface
class PaymentProcessor:
    def process_payment(self, payment_data):
        pass

# Adapter
class PaymentAdapter(PaymentProcessor):
    def __init__(self, old_system):
        self.old_system = old_system
    
    def process_payment(self, payment_data):
        amount = payment_data.get('amount')
        currency = payment_data.get('currency', 'USD')
        self.old_system.make_payment(amount, currency)

# Usage
old_system = OldPaymentSystem()
adapter = PaymentAdapter(old_system)
payment_data = {'amount': 100, 'currency': 'USD'}
adapter.process_payment(payment_data)
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Integrates incompatible systems
  - Reuses existing code
  - Follows open/closed principle
- **Costs**: 
  - Adds complexity
  - Can create tight coupling
- **Use when**: You need to integrate incompatible interfaces

---

### Decorator Pattern

**What it is**: Adds behavior to objects dynamically without changing their class.

**When to use**:
- Adding features to objects at runtime
- Avoiding subclass explosion
- Implementing cross-cutting concerns

**Implementation**:
```python
from abc import ABC, abstractmethod

# Component interface
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass

# Concrete component
class SimpleCoffee(Coffee):
    def cost(self):
        return 2.0
    
    def description(self):
        return "Simple coffee"

# Base decorator
class CoffeeDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee
    
    def cost(self):
        return self._coffee.cost()
    
    def description(self):
        return self._coffee.description()

# Concrete decorators
class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 0.5
    
    def description(self):
        return self._coffee.description() + ", milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 0.2
    
    def description(self):
        return self._coffee.description() + ", sugar"

# Usage
coffee = SimpleCoffee()
coffee_with_milk = MilkDecorator(coffee)
coffee_with_milk_and_sugar = SugarDecorator(coffee_with_milk)

print(f"{coffee_with_milk_and_sugar.description()}: ${coffee_with_milk_and_sugar.cost()}")
# Output: Simple coffee, milk, sugar: $2.7
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Flexible behavior composition
  - Follows single responsibility principle
  - Easy to add new behaviors
- **Costs**: 
  - Can create many small objects
  - Complex object hierarchies
- **Use when**: You need to add behavior dynamically

---

### Facade Pattern

**What it is**: Provides a simplified interface to a complex subsystem.

**When to use**:
- Simplifying complex APIs
- Providing a unified interface to multiple subsystems
- Reducing dependencies between client and subsystem

**Implementation**:
```python
# Complex subsystems
class AudioSystem:
    def turn_on(self):
        print("Audio system on")
    
    def set_volume(self, level):
        print(f"Volume set to {level}")

class VideoSystem:
    def turn_on(self):
        print("Video system on")
    
    def set_resolution(self, resolution):
        print(f"Resolution set to {resolution}")

class LightingSystem:
    def dim_lights(self):
        print("Lights dimmed")

# Facade
class HomeTheaterFacade:
    def __init__(self):
        self.audio = AudioSystem()
        self.video = VideoSystem()
        self.lighting = LightingSystem()
    
    def watch_movie(self):
        print("=== Starting Movie Mode ===")
        self.lighting.dim_lights()
        self.video.turn_on()
        self.video.set_resolution("4K")
        self.audio.turn_on()
        self.audio.set_volume(8)
        print("Movie mode ready!")
    
    def end_movie(self):
        print("=== Ending Movie Mode ===")
        # Turn off systems...

# Usage
theater = HomeTheaterFacade()
theater.watch_movie()
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Simplifies complex interfaces
  - Reduces coupling
  - Easy to use
- **Costs**: 
  - Can become a "god object"
  - Hides complexity
- **Use when**: You need to simplify complex subsystem interactions

---

## 3. Behavioral Patterns

### Observer Pattern

**What it is**: Defines a one-to-many dependency between objects.

**When to use**:
- Event handling systems
- Model-View architectures
- Publish-subscribe systems

**Implementation**:
```python
from abc import ABC, abstractmethod

# Subject interface
class Subject(ABC):
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self, data):
        for observer in self._observers:
            observer.update(data)

# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass

# Concrete subject
class NewsAgency(Subject):
    def publish_news(self, news):
        print(f"Publishing: {news}")
        self.notify(news)

# Concrete observers
class NewsChannel(Observer):
    def __init__(self, name):
        self.name = name
    
    def update(self, news):
        print(f"{self.name} received: {news}")

class NewsWebsite(Observer):
    def __init__(self, url):
        self.url = url
    
    def update(self, news):
        print(f"{self.url} updated with: {news}")

# Usage
agency = NewsAgency()
channel1 = NewsChannel("CNN")
channel2 = NewsChannel("BBC")
website = NewsWebsite("news.com")

agency.attach(channel1)
agency.attach(channel2)
agency.attach(website)

agency.publish_news("Breaking: AI solves all problems!")
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Loose coupling
  - Easy to add/remove observers
  - Supports broadcast communication
- **Costs**: 
  - Can cause memory leaks
  - Order of notifications not guaranteed
  - Can lead to complex update chains
- **Use when**: You need loose coupling between objects

---

### Strategy Pattern

**What it is**: Defines a family of algorithms and makes them interchangeable.

**When to use**:
- Multiple algorithms for the same task
- Algorithm selection at runtime
- Avoiding complex conditional statements

**Implementation**:
```python
from abc import ABC, abstractmethod

# Strategy interface
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# Concrete strategies
class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number):
        self.card_number = card_number
    
    def pay(self, amount):
        print(f"Paid ${amount} using credit card ending in {self.card_number[-4:]}")

class PayPalPayment(PaymentStrategy):
    def __init__(self, email):
        self.email = email
    
    def pay(self, amount):
        print(f"Paid ${amount} using PayPal account {self.email}")

class BitcoinPayment(PaymentStrategy):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
    
    def pay(self, amount):
        print(f"Paid ${amount} using Bitcoin wallet {self.wallet_address[:8]}...")

# Context
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy = None
    
    def add_item(self, item, price):
        self.items.append((item, price))
    
    def set_payment_strategy(self, strategy):
        self.payment_strategy = strategy
    
    def checkout(self):
        total = sum(price for _, price in self.items)
        if self.payment_strategy:
            self.payment_strategy.pay(total)
            self.items.clear()
        else:
            print("Please select a payment method")

# Usage
cart = ShoppingCart()
cart.add_item("Laptop", 999)
cart.add_item("Mouse", 25)

# Choose payment strategy
cart.set_payment_strategy(CreditCardPayment("1234-5678-9012-3456"))
cart.checkout()

cart.add_item("Keyboard", 75)
cart.set_payment_strategy(PayPalPayment("user@example.com"))
cart.checkout()
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Easy to add new algorithms
  - Eliminates conditional statements
  - Follows open/closed principle
- **Costs**: 
  - More classes
  - Can be overkill for simple cases
- **Use when**: You have multiple algorithms for the same task

---

### Command Pattern

**What it is**: Encapsulates a request as an object.

**When to use**:
- Undo/redo functionality
- Queue operations
- Logging requests
- Remote procedure calls

**Implementation**:
```python
from abc import ABC, abstractmethod

# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

# Concrete commands
class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()

class LightOffCommand(Command):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_off()
    
    def undo(self):
        self.light.turn_on()

# Receiver
class Light:
    def __init__(self, location):
        self.location = location
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        print(f"{self.location} light is ON")
    
    def turn_off(self):
        self.is_on = False
        print(f"{self.location} light is OFF")

# Invoker
class RemoteControl:
    def __init__(self):
        self.commands = {}
        self.undo_stack = []
    
    def set_command(self, button, command):
        self.commands[button] = command
    
    def press_button(self, button):
        if button in self.commands:
            command = self.commands[button]
            command.execute()
            self.undo_stack.append(command)
    
    def press_undo(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()

# Usage
living_room_light = Light("Living Room")
kitchen_light = Light("Kitchen")

remote = RemoteControl()
remote.set_command("1", LightOnCommand(living_room_light))
remote.set_command("2", LightOffCommand(living_room_light))
remote.set_command("3", LightOnCommand(kitchen_light))

remote.press_button("1")  # Turn on living room light
remote.press_button("3")  # Turn on kitchen light
remote.press_undo()       # Undo last command
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Supports undo/redo
  - Easy to queue operations
  - Decouples request from execution
- **Costs**: 
  - More classes
  - Can be complex for simple operations
- **Use when**: You need undo/redo or command queuing

---

## 4. Pattern Selection Guidelines

### When to Use Each Pattern

| Pattern | Use When | Avoid When |
|---------|----------|------------|
| **Singleton** | Need single instance, global access | Want testable, flexible code |
| **Factory** | Object creation varies, complex logic | Simple object creation |
| **Builder** | Many optional parameters, immutable objects | Simple objects with few parameters |
| **Adapter** | Integrating incompatible interfaces | Can modify existing code |
| **Decorator** | Adding behavior dynamically | Behavior is fixed |
| **Facade** | Simplifying complex subsystems | Simple, direct interactions |
| **Observer** | Loose coupling, event handling | Tight coupling is acceptable |
| **Strategy** | Multiple algorithms, runtime selection | Single algorithm, compile-time selection |
| **Command** | Undo/redo, queuing, logging | Simple, direct method calls |

### Cost-Benefit Summary

| Pattern | Complexity Cost | Flexibility Benefit | Maintainability Benefit |
|---------|----------------|-------------------|------------------------|
| **Singleton** | Low | Low | Low |
| **Factory** | Medium | High | High |
| **Builder** | Medium | High | Medium |
| **Adapter** | Low | Medium | Medium |
| **Decorator** | Medium | High | High |
| **Facade** | Low | Medium | High |
| **Observer** | Medium | High | Medium |
| **Strategy** | Medium | High | High |
| **Command** | High | High | High |

---

## 5. Anti-Patterns to Avoid

### God Object
- **Problem**: One class does everything
- **Solution**: Break into smaller, focused classes
- **Use**: Single responsibility principle

### Singleton Abuse
- **Problem**: Using singleton for everything
- **Solution**: Consider dependency injection
- **Use**: Only when you truly need one instance

### Over-Engineering
- **Problem**: Using patterns when not needed
- **Solution**: Start simple, add patterns as needed
- **Use**: YAGNI principle (You Aren't Gonna Need It)

---

*Design patterns are tools, not rules. Use them when they solve real problems, not just because they exist. The best pattern is often the simplest one that works.*

---

# DevOps & Cloud

## CI/CD & Infrastructure

The goal here is to be able to “drop in” a minimal but realistic setup during interviews or when spinning up a demo.

## 1) Terraform mini-project (AWS VPC + EC2 + S3, remote state)

### Key Infrastructure Concepts

#### **VPC (Virtual Private Cloud)**
A **VPC** is a logically isolated section of the AWS cloud where you can launch AWS resources in a virtual network that you define. Think of it as your own private data center in the cloud.

**What it provides:**
- **Network isolation** from other AWS customers
- **Custom IP address ranges** (CIDR blocks like 10.0.0.0/16)
- **Subnet configuration** for organizing resources
- **Route tables** for controlling traffic flow
- **Security groups** and **Network ACLs** for access control
- **Internet connectivity** control (public vs private subnets)

**Why it matters:**
- **Security**: Isolates your resources from other AWS customers
- **Compliance**: Required for HIPAA, SOC2, and other security standards
- **Cost control**: Prevents unauthorized resource creation
- **Network design**: Allows you to design your network architecture

#### **Subnets**
**Subnets** are subdivisions of your VPC that allow you to group resources and control network access. They're like different floors or sections in a building.

**Types of Subnets:**
- **Public Subnets**: 
  - Resources can have public IP addresses
  - Direct internet access through Internet Gateway
  - Used for load balancers, bastion hosts
  - **Security risk**: More exposed to internet threats
  
- **Private Subnets**:
  - No public IP addresses assigned
  - Internet access through NAT Gateway (controlled)
  - Used for application servers, databases
  - **Security benefit**: Protected from direct internet access

**Subnet Design Best Practices:**
- **Availability Zones**: Distribute subnets across multiple AZs for high availability
- **CIDR Planning**: Use non-overlapping IP ranges (e.g., 10.0.1.0/24, 10.0.2.0/24)
- **Resource Grouping**: Group similar resources in the same subnet
- **Security**: Use private subnets for sensitive resources

#### **Spot Instances**
**Spot Instances** are AWS EC2 instances that you can bid on and use for up to 90% off the On-Demand price. AWS sells unused capacity at a discount.

**How Spot Instances Work:**
- **Bidding**: You set a maximum price you're willing to pay
- **Availability**: AWS fills your request if spot price ≤ your bid
- **Interruption**: AWS can terminate your instance with 2-minute notice if:
  - Spot price exceeds your bid
  - AWS needs the capacity back
  - Spot capacity is no longer available

**Use Cases:**
- **Batch processing**: Data analysis, video encoding, scientific computing
- **Testing/Development**: Non-critical workloads
- **Cost optimization**: Up to 90% savings vs On-Demand
- **Fault-tolerant applications**: Can handle interruptions

**Spot Instance Strategies:**
- **Diversification**: Use multiple instance types and AZs
- **Bid strategy**: Set bid at On-Demand price for better availability
- **Interruption handling**: Implement graceful shutdown and recovery
- **Fallback**: Use On-Demand instances as backup

#### **Incident Severity Levels (SEV 1-4)**

**SEV-1 (Critical) - "All Hands on Deck"**
- **Definition**: Service completely down, data loss, security breach
- **Response Time**: Immediate (within 5 minutes)
- **Communication**: All stakeholders, status page updates, executive notification
- **Resolution Target**: 1 hour
- **Examples**: 
  - Database corruption
  - Complete service outage
  - Customer data breach
  - Payment system failure

**SEV-2 (High) - "Urgent Response Required"**
- **Definition**: Major feature broken, significant performance degradation
- **Response Time**: Within 15 minutes
- **Communication**: Engineering team, product managers, customer support
- **Resolution Target**: 4 hours
- **Examples**:
  - Core feature unavailable
  - 50%+ performance degradation
  - Multiple customers affected
  - Revenue-impacting issues

**SEV-3 (Medium) - "Normal Priority"**
- **Definition**: Minor feature broken, slight performance impact
- **Response Time**: Within 1 hour
- **Communication**: Engineering team, internal stakeholders
- **Resolution Target**: 24 hours
- **Examples**:
  - Non-critical feature broken
  - Minor performance issues
  - Limited customer impact
  - Cosmetic bugs

**SEV-4 (Low) - "Business Hours"**
- **Definition**: Cosmetic issues, minor bugs, enhancement requests
- **Response Time**: Within 4 hours
- **Communication**: Engineering team
- **Resolution Target**: 1 week
- **Examples**:
  - UI text typos
  - Minor styling issues
  - Enhancement requests
  - Documentation updates

### Multi-Environment Setup
This example shows how to structure Terraform for multiple environments (dev, staging, prod) with shared modules.

**Layout**

```
terraform/
  main.tf
  vpc.tf
  ec2.tf
  s3.tf
  variables.tf
  outputs.tf
  backend.hcl
```

**backend.hcl** (remote state configuration)

**What this file provisions:**
- **Remote State Storage**: Configuration for storing Terraform state files in S3
- **State Locking**: DynamoDB table to prevent multiple people from modifying infrastructure simultaneously
- **Encryption**: Ensures state files are encrypted for security

**Why this matters:**
- **Team Collaboration**: Multiple team members can work on the same infrastructure
- **State Persistence**: State files are stored safely and backed up
- **Security**: Prevents accidental infrastructure changes and protects sensitive information
- **Audit Trail**: Keeps track of who made changes and when

```bash
bucket         = "my-tf-state-bucket"    # S3 bucket to store Terraform state
key            = "envs/dev/terraform.tfstate"  # Path within bucket for this environment
region         = "us-west-2"             # AWS region for the backend
dynamodb_table = "my-tf-locks"           # DynamoDB table for state locking (prevents concurrent modifications)
encrypt        = true                    # Encrypt state files at rest
```

**main.tf** (provider and version configuration)

**What this file provisions:**
- **Terraform Configuration**: Sets version requirements and backend configuration
- **AWS Provider**: Connects Terraform to AWS services
- **Backend Configuration**: Specifies where to store Terraform state files

**Why this matters:**
- **Version Control**: Ensures consistent Terraform behavior across team members
- **Provider Management**: Connects to AWS APIs to create and manage resources
- **State Management**: Backend configuration enables team collaboration and state persistence

```bash
terraform {
  required_version = ">= 1.6.0"         # Minimum Terraform version required
  backend "s3" {}                       # Use S3 backend for remote state (configured via backend.hcl at init-time)
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }  # AWS provider with version constraint
  }
}

provider "aws" {
  region = var.region                    # AWS region for all resources
}
```

**vpc.tf** (networking infrastructure)

**What this file provisions:**
- **VPC**: A private, isolated network environment in AWS
- **Public Subnet**: A network segment where resources can have public IP addresses
- **Internet Gateway**: A connection point between your VPC and the internet

**Why this matters:**
- **Network Isolation**: Keeps your resources separate from other AWS customers
- **Internet Access**: Allows your web servers to be accessible from the internet
- **Security**: Provides a foundation for implementing network security controls

```bash
# Virtual Private Cloud - isolated network environment
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"           # Private IP range: 10.0.0.0 to 10.0.255.255
  tags = { Name = "demo-vpc" }          # Resource tagging for cost tracking and organization
}

# Public subnet in availability zone 'a' - accessible from internet
resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.main.id                    # Associate with our VPC
  cidr_block              = "10.0.1.0/24"                     # Subnet range: 10.0.1.0 to 10.0.1.255
  map_public_ip_on_launch = true                               # Auto-assign public IPs to instances
  availability_zone       = "${var.region}a"                   # Place in first AZ (e.g., us-west-2a)
}

# Internet Gateway - allows VPC to communicate with internet
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id              # Attach to our VPC
}
```

**ec2.tf** (compute and security)

**What this file provisions:**
- **Security Group**: A virtual firewall that controls inbound and outbound traffic to your EC2 instances
- **EC2 Instance**: A virtual server running Amazon Linux with Apache web server
- **AMI Data Source**: Dynamically finds the latest Amazon Linux operating system image

**Why this matters:**
- **Security**: Controls who can access your web server (SSH and HTTP)
- **Compute**: Provides the actual server to run your web application
- **Automation**: Automatically installs and configures the web server software

```bash
# Security Group - firewall rules for EC2 instances
resource "aws_security_group" "web" {
  name   = "web-sg"                     # Security group name
  vpc_id = aws_vpc.main.id             # Associate with our VPC

  # Allow SSH access from anywhere (0.0.0.0/0 = all IPs)
  ingress {
    from_port = 22                      # SSH port
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]        # WARNING: In production, restrict to specific IPs
  }
  
  # Allow HTTP access from anywhere (for web traffic)
  ingress {
    from_port = 80                      # HTTP port
    to_port   = 80
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]        # WARNING: In production, restrict to specific IPs
  }
  
  # Allow all outbound traffic (instances can reach internet)
  egress {
    from_port = 0                       # All ports
    to_port   = 0
    protocol  = "-1"                    # All protocols
    cidr_blocks = ["0.0.0.0/0"]        # All destinations
  }
}

# Data source to get latest Amazon Linux AMI
data "aws_ami" "amazon_linux" {
  most_recent = true                    # Get the newest available
  owners = ["amazon"]                   # Official Amazon AMIs
  filter {
    name = "name"                       # Filter by AMI name
    values = ["al2023-ami-*-x86_64"]   # Amazon Linux 2023, 64-bit
  }
}
```

resource "aws_instance" "web" {
  ami                    = data.aws_ami.amazon_linux.id    # Use the AMI we found earlier
  instance_type          = "t3.micro"                      # Small instance type (1 vCPU, 1 GB RAM)
  subnet_id              = aws_subnet.public_a.id          # Place in our public subnet
  vpc_security_group_ids = [aws_security_group.web.id]     # Apply our security group rules
  
  # User data script runs when instance first boots
  user_data = <<-EOF
              #!/bin/bash
              yum install -y httpd                          # Install Apache web server
              systemctl enable httpd                        # Start Apache on boot
              systemctl start httpd                         # Start Apache now
              echo "hello from terraform" > /var/www/html/index.html  # Create simple webpage
              EOF
  
  tags = { Name = "web" }                                  # Resource tagging
}
```

**s3.tf** (object storage)

**What this file provisions:**
- **S3 Bucket**: A scalable object storage service for storing files, images, and static content
- **Bucket Versioning**: Keeps multiple versions of files, protecting against accidental deletion

**Why this matters:**
- **Scalability**: Can store unlimited amounts of data with high availability
- **Cost-Effective**: Pay only for what you store, no upfront infrastructure costs
- **Data Protection**: Versioning helps recover from accidental deletions or overwrites
- **Static Hosting**: Can serve static websites or store application assets

```bash
# S3 bucket for storing static assets (images, CSS, JS files)
resource "aws_s3_bucket" "assets" {
  bucket = var.bucket_name                                 # Bucket name from variable
  tags = { Name = "assets" }                               # Resource tagging
}

# Enable versioning to keep multiple versions of objects
resource "aws_s3_bucket_versioning" "assets" {
  bucket = aws_s3_bucket.assets.id                         # Reference to our bucket
  versioning_configuration {
    status = "Enabled"                                      # Turn on versioning
  }
}
```

**variables.tf** (input parameters)

**What this file provisions:**
- **Input Variables**: Configurable parameters that can be set when running Terraform
- **Default Values**: Predefined values for common settings like AWS region

**Why this matters:**
- **Flexibility**: Allows the same Terraform code to be used in different environments
- **Reusability**: Variables make your Terraform modules reusable across projects
- **Environment Management**: Different values can be set for dev, staging, and production

```bash
variable "region"      { type = string, default = "us-west-2" }  # AWS region with default
variable "bucket_name" { type = string }                         # Required: S3 bucket name
```

**outputs.tf** (return values)

**What this file provisions:**
- **Output Values**: Information that Terraform displays after creating resources
- **Resource References**: Values that can be used by other Terraform modules or external systems

**Why this matters:**
- **Visibility**: Shows important information like IP addresses and resource names
- **Integration**: Outputs can be used by other tools or scripts
- **Documentation**: Provides a clear summary of what was created
- **Troubleshooting**: Helps verify that resources were created correctly

```bash
output "ec2_public_ip" { value = aws_instance.web.public_ip }   # Public IP of web server
output "s3_bucket"     { value = aws_s3_bucket.assets.bucket }  # Name of S3 bucket
```

**CLI Commands** (deployment workflow)

**What these commands do:**
- **terraform init**: Sets up the working directory and downloads required providers
- **terraform plan**: Shows what changes Terraform will make without actually applying them
- **terraform apply**: Creates, modifies, or destroys infrastructure based on your configuration

**Why this workflow matters:**
- **Safety**: Plan command lets you review changes before they happen
- **Reproducibility**: Same commands work consistently across different environments
- **Automation**: These commands can be integrated into CI/CD pipelines
- **Version Control**: Infrastructure changes are tracked and can be rolled back

```bash
# Initialize Terraform and configure backend
terraform init -backend-config=backend.hcl

# Preview changes before applying
terraform plan -var="bucket_name=my-artifacts-bucket"

# Apply changes and create infrastructure
terraform apply -auto-approve -var="bucket_name=my-artifacts-bucket"
```

### Advanced Terraform Patterns

#### Workspace-based Environment Management

**What this pattern provides:**
- **Environment Isolation**: Separate state files for different environments (dev, staging, prod)
- **State Management**: Each workspace maintains its own infrastructure state
- **Variable Files**: Environment-specific configurations stored in separate files

**Why this matters:**
- **Risk Mitigation**: Changes in dev don't affect production infrastructure
- **Testing**: Can test infrastructure changes safely in isolated environments
- **Team Workflow**: Different teams can work on different environments simultaneously
- **Cost Control**: Prevents accidental resource creation in production

```bash
# Create and switch to dev workspace (isolates state for different environments)
terraform workspace new dev
terraform workspace select dev

# Apply with environment-specific variables
terraform apply -var-file="dev.tfvars"

# Switch to prod workspace (different state, different environment)
terraform workspace select prod
terraform apply -var-file="prod.tfvars"
```

---

## Server Provisioning with Terraform

### What "Server Provisioning" Really Means

**Server provisioning** is everything needed to turn "I need a server/app" into a running, reachable, monitored machine/service.

**The layers you usually provision:**

1. **Compute**: VM/instance, autoscaling group, or node pool
2. **Network**: VPC/VNet, subnets, routes, NAT/IGW, security groups/firewalls
3. **Identity & Access**: IAM roles, instance profiles, KMS keys
4. **Storage**: disks/volumes, buckets, database instances
5. **Connectivity**: load balancers, DNS records, TLS certs
6. **Base Software**: OS image, hardening, runtime (containerd/Docker), agents (telemetry, backups)
7. **Bootstrapping**: cloud-init/user-data to configure on first boot
8. **Observability**: logs/metrics/traces shipping (e.g., OpenTelemetry, CloudWatch/Stackdriver)
9. **Compliance**: tags, cost centers, encryption, backups, retention policies

### Two Philosophies of Server Management

**Mutable Servers ("Pets")**: 
- Create a VM and install stuff on it over time
- **Pros**: Familiar, easy to debug, incremental changes
- **Cons**: Configuration drift, hard to reproduce, manual maintenance

**Immutable Servers ("Cattle")**: 
- Bake a machine image (AMI/Image) with Packer, boot it, never change in place
- **Pros**: Consistent, reproducible, easy to scale, no drift
- **Cons**: More complex tooling, longer deployment times

### Declarative vs. Imperative (Why IaC Matters)

**Imperative Approach**: 
- "Click this, run that script on host X"
- **Problems**: Easy to drift, hard to reproduce, manual errors

**Declarative (IaC)**: 
- "The desired state is: 3 subnets, 2 web VMs, 1 LB"
- **Benefits**: A tool computes the diff and applies changes idempotently, reproducible, reviewable, testable

---

### Terraform in Depth

**What Terraform Does:**
- Talks to cloud/provider APIs (AWS/GCP/Azure, Cloudflare, Datadog, GitHub, Kubernetes, etc.)
- Creates/updates/destroys resources to match your **desired state** written in HCL files
- Tracks reality in **state** so it knows what exists

**Core Concepts:**

- **Provider**: Plugin that knows how to manage a platform (e.g., `hashicorp/aws`)
- **Resource**: A thing to create (e.g., `aws_instance`, `google_compute_network`)
- **Data Source**: Read-only lookup (e.g., latest Ubuntu AMI)
- **Module**: A reusable bundle of resources (your own or from the Registry)
- **Variables/Outputs/Locals**: Inputs, exported values, and computed helpers
- **State**: A JSON map of what Terraform created (store remotely with locking for teams)
- **Plan → Apply**: `terraform plan` shows the diff; `terraform apply` executes it
- **Lifecycle & Meta-args**: `depends_on`, `count`/`for_each`, `lifecycle` hooks

### Typical Workflow (GitOps-friendly)

1. **Author** HCL in a repo (one directory per module/env)
2. **Init** providers/backends: `terraform init`
3. **Validate & Format**: `terraform fmt -check`, `terraform validate`
4. **Plan** in CI, post the diff in PR for review
5. **Apply** after approval from CI (with remote state & locking)
6. **Tag & Document** the change; add runbooks/links to dashboards

### Common Patterns You'll Use

- **Remote Backend** with encryption + locking
- **Separate State Per Environment** (e.g., dev/stage/prod) rather than relying on workspaces alone
- **Module Per Concern**: network, cluster, database, app perimeter, etc.
- **Image Baking** (Packer) + **user_data/cloud-init** for first-boot
- **No or Minimal Provisioners** (use them only when unavoidable)
- **Secrets** via cloud secret managers (don't put them in state)

---

### Technical Terms Explained

**VPC (Virtual Private Cloud)**: A logically isolated section of the cloud where you can launch resources in a virtual network you define.

**Subnet**: A subdivision of your VPC that allows you to group resources and control network access.

**CIDR Block**: A way to specify IP address ranges (e.g., 10.0.0.0/16 means 10.0.0.0 to 10.0.255.255).

**Security Group**: A virtual firewall that controls inbound and outbound traffic to your resources.

**Internet Gateway**: A connection point between your VPC and the internet.

**Route Table**: A set of rules that determine where network traffic is directed.

**AMI (Amazon Machine Image)**: A template that contains the software configuration required to launch an instance.

**Instance Profile**: A container for an IAM role that you can use to pass role information to an EC2 instance when the instance starts.

**Load Balancer**: A device that distributes incoming network traffic across multiple targets.

**DNS (Domain Name System)**: A system that translates human-readable domain names into IP addresses.

**TLS (Transport Layer Security)**: A protocol that provides secure communication over a computer network.

**Autoscaling Group**: A collection of EC2 instances that automatically scales based on demand.

**Node Pool**: A group of nodes within a Kubernetes cluster that share the same configuration.

---

### Technology Distinctions

#### **Terraform vs. Kubernetes vs. Docker**

**Terraform**:
- **Purpose**: Infrastructure as Code tool
- **What it manages**: Cloud resources (VMs, networks, databases, load balancers)
- **When to use**: Setting up the foundation that your applications run on
- **Think of it as**: The "construction crew" that builds your data center

**Kubernetes (K8s)**:
- **Purpose**: Container orchestration platform
- **What it manages**: Containerized applications, their deployment, scaling, and networking
- **When to use**: Managing applications once the infrastructure exists
- **Think of it as**: The "traffic controller" that manages your running applications

**Docker**:
- **Purpose**: Containerization platform
- **What it manages**: Packaging applications and their dependencies into containers
- **When to use**: Creating portable, consistent application packages
- **Think of it as**: The "packaging system" that wraps your applications

#### **Server vs. Microservice**

**Traditional Server**:
- **Architecture**: Monolithic application running on a single server
- **Scaling**: Scale vertically (bigger server) or horizontally (more servers)
- **Deployment**: Deploy entire application at once
- **Example**: A web application with frontend, backend, and database all on one server

**Microservice**:
- **Architecture**: Application broken into small, independent services
- **Scaling**: Scale individual services independently based on demand
- **Deployment**: Deploy services independently
- **Example**: Separate services for user authentication, product catalog, and order processing

---

### End-to-End Example (Concise but Realistic)

Below is a minimal slice of what provisioning with Terraform can look like on AWS: build a tiny network, a security group, and an EC2 instance that installs Docker via cloud-init and serves traffic behind a public IP.

```hcl
terraform {
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
  backend "s3" {
    bucket         = "my-tfstate"
    key            = "dev/web.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" { region = "us-west-2" }

resource "aws_vpc" "main" { cidr_block = "10.0.0.0/16" }

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "igw" { vpc_id = aws_vpc.main.id }

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route { cidr_block = "0.0.0.0/0", gateway_id = aws_internet_gateway.igw.id }
}

resource "aws_route_table_association" "pub_a" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = aws_vpc.main.id
  ingress { from_port = 80 to_port = 80 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  egress  { from_port = 0  to_port = 0  protocol = "-1"   cidr_blocks = ["0.0.0.0/0"] }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  filter { name = "name", values = ["ubuntu/images/hvm-ssd/ubuntu-*-amd64-server-*"] }
}

resource "aws_instance" "web" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.web.id]
  user_data = <<-CLOUD
  #cloud-config
  packages: [docker.io]
  runcmd:
    - systemctl enable --now docker
    - docker run -d -p 80:80 --name hello nginx
  CLOUD
  tags = { Name = "web1" }
}

output "public_ip" { value = aws_instance.web.public_ip }
```

**What this does:**

- Provisions **networking** + a **public subnet** + **routing**
- Opens port **80**
- Boots an **Ubuntu** VM and uses **cloud-init** to install Docker and start **nginx**
- Prints the server's **public IP** so you can test it

**From here you'd usually add:**

- An **ALB** and a **DNS record** (Route53) → users hit `https://app.example.com`
- **TLS cert** (ACM)
- **Autoscaling group** (immutable AMIs baked with Packer)
- **Logging/metrics** pipelines
- Later, swap VMs for a **Kubernetes cluster** (EKS managed by Terraform) and deploy apps as containers

---

### Terraform vs. Configuration Management (Ansible/Chef/etc.)

**Terraform**: Creates cloud resources (VMs, networks, LB, DBs). Think **outside** the box.

**Ansible** (or cloud-init/Packer): Configures what's **inside** the box (packages, files, services).

**Many teams bake images with Packer, provision infra with Terraform, and do in-cluster app deploys with GitOps (Argo CD/Flux).**

---

### Provisioning in a Kubernetes World

**Use Terraform to create the cluster (EKS/GKE/AKS), node groups, VPC/ILB/ALB, IAM, external-dns, ingress controllers, cert-manager scaffolding.**

**Then deploy app manifests/Helm with a GitOps controller. Terraform can still manage certain infra-level K8s objects that must exist early (e.g., storage classes, cluster-wide RBAC), but avoid mixing app lifecycle with infra in the same state to keep blast radius small.**

---

### Good Practices (Battle-tested)

- Remote, locked, encrypted **state** per env (e.g., `dev`, `stage`, `prod`)
- **Small modules** with clear inputs/outputs. Version them
- **Tag everything** (owner, app, env, cost center)
- **Least-privilege IAM** for Terraform and your workloads
- **Policy as code** (OPA/Conftest, Terraform Cloud/Enterprise/Spacelift policies) to prevent risky plans
- **Cost guardrails** (budgets/alerts, quotas)
- **Runbooks & dashboards** linked from your repo

---

### Common Pitfalls

- Manually tweaking resources in the console → **drift** surprises in the next plan
- Renaming resources without `moved {}` or `terraform import` → accidental **destroy/recreate**
- Storing secrets in variables/state → leaks. Use a secret manager
- Overusing `null_resource` and provisioners → fragile. Prefer images/cloud-init/CM tools
- One giant state for everything → slow plans, big blast radius. Split by domain/env

#### Module-based Architecture
```hcl
# modules/vpc/main.tf - Reusable VPC module
module "vpc" {
  source = "../../modules/vpc"                              # Path to module source
  
  environment = var.environment                             # Pass environment name
  vpc_cidr   = var.vpc_cidr                                # Pass VPC CIDR block
  azs         = var.azs                                     # Pass availability zones
}

# modules/vpc/variables.tf - Module input variables
variable "environment" {
  description = "Environment name (dev, staging, prod)"     # Variable documentation
  type        = string                                      # Variable type
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
}

variable "azs" {
  description = "Availability zones"
  type        = list(string)
}
```

#### Security Best Practices
```hcl
# Enable VPC Flow Logs
resource "aws_flow_log" "vpc_flow_log" {
  iam_role_arn    = aws_iam_role.vpc_flow_log_role.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_log_group.arn
  traffic_type    = "ALL"
  vpc_id          = aws_vpc.main.id
}

# Enable VPC Endpoints for private subnets
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids = [aws_route_table.private.id]
}
```

---

## 2) Jenkinsfile (build → test → Docker → push → deploy to K8s)

```groovy
pipeline {
  agent any
  environment {
    APP_NAME = 'example-svc'
    AWS_REGION = 'us-west-2'
    ECR_REPO = "123456789012.dkr.ecr.${AWS_REGION}.amazonaws.com/${APP_NAME}"
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Test') {
      steps {
        sh 'python -m pip install -r requirements.txt'
        sh 'pytest -q'
      }
    }
    stage('Build Image') {
      steps {
        sh 'docker build -t ${APP_NAME}:${BUILD_NUMBER} .'
      }
    }
    stage('Login ECR & Push') {
      steps {
        sh 'aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin 123456789012.dkr.ecr.${AWS_REGION}.amazonaws.com'
        sh 'docker tag ${APP_NAME}:${BUILD_NUMBER} ${ECR_REPO}:${BUILD_NUMBER}'
        sh 'docker push ${ECR_REPO}:${BUILD_NUMBER}'
      }
    }
    stage('Deploy to K8s') {
      steps {
        sh 'kubectl set image deployment/${APP_NAME} ${APP_NAME}=${ECR_REPO}:${BUILD_NUMBER} --record'
      }
    }
  }
}
```

---

## 3) Kubernetes Manifests (Deployment + Service + Ingress)

**deployment.yaml**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-svc
  labels:
    app: example-svc
spec:
  replicas: 2
  selector:
    matchLabels:
      app: example-svc
  template:
    metadata:
      labels:
        app: example-svc
    spec:
      containers:
        - name: example-svc
          image: 123456789012.dkr.ecr.us-west-2.amazonaws.com/example-svc:latest
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet: { path: /healthz, port: 8080 }
            initialDelaySeconds: 3
          livenessProbe:
            httpGet: { path: /livez, port: 8080 }
            initialDelaySeconds: 5
          resources:
            requests: { cpu: "100m", memory: "128Mi" }
            limits: { cpu: "500m", memory: "256Mi" }
```

**service.yaml**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: example-svc
spec:
  selector:
    app: example-svc
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

**ingress.yaml** (requires ingress controller)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-svc
spec:
  rules:
    - host: example.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: example-svc
                port:
                  number: 80
```

**Apply**

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

---

## 4) Prometheus Alerting Rules (examples)

**alert-rules.yaml**

```yaml
groups:
  - name: app.rules
    rules:
      - alert: HighCPU
        expr: avg(rate(container_cpu_usage_seconds_total{container!="",pod=~"example-svc.*"}[5m])) > 0.8
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "High CPU usage on example-svc"
          description: "CPU > 80% for 5m"

      - alert: HighErrorRate
        expr: rate(http_requests_total{job="example-svc",code=~"5.."}[5m]) / rate(http_requests_total{job="example-svc"}[5m]) > 0.05
        for: 10m
        labels: { severity: critical }
        annotations:
          summary: "High 5xx error rate"
          description: ">5% 5xx over 10m"

      - alert: CrashLooping
        expr: increase(kube_pod_container_status_restarts_total{pod=~"example-svc.*"}[10m]) > 3
        for: 10m
        labels: { severity: warning }
        annotations:
          summary: "Pod restarting frequently"
          description: "More than 3 restarts in 10 minutes"
```

> Wire this into Prometheus via `rule_files` and configure Alertmanager receivers (email/Slack/PagerDuty).

---

---

## Reliability Engineering (Internet Fundamentals, Observability, Chaos Engineering, Load Testing)

Reliability engineering combines **observability**, **chaos engineering**, and **load testing** to build systems that are not only performant but also resilient and observable under stress.

---

## 1. Observability (The Three Pillars)

### Metrics
- **Prometheus** → pull-based metrics collection, best with Kubernetes
- **Datadog** → SaaS monitoring platform with agents and integrations
- **CloudWatch Metrics** → AWS-native, integrates with alarms
- **Azure Monitor, GCP Monitoring** → cloud-native equivalents

### Logs
- **CloudWatch Logs** → AWS log storage and queries
- **Splunk** → enterprise log aggregation and search
- **ELK Stack** (Elasticsearch + Logstash + Kibana) → open-source stack
- **Loki** → log aggregation, pairs with Prometheus
- **New Relic Logs** → SaaS, correlated with APM traces

### Traces
- **OpenTelemetry** → vendor-neutral standard, instrument once, export anywhere
- **Jaeger** → CNCF tracing tool
- **Zipkin** → lightweight tracer
- **Datadog APM** → integrated metrics/logs/traces
- **AWS X-Ray** → request tracing in AWS stack

### Visualization
- **Grafana** → dashboards and visualization for time-series metrics
- **Key Concepts**: panels, templating, alerting, plugins
- **Best Practices**: organize by team/service, show SLOs, keep simple

---

## 2. Chaos Engineering & Resiliency

### Principles
- **Define steady state** → measurable normal condition (e.g., "95% of requests < 200ms")
- **Hypothesize** → predict what should happen under failure
- **Inject faults** → simulate failure in controlled way
- **Observe** → measure whether steady state holds
- **Minimize blast radius** → start in staging or small slice of prod
- **Automate rollback** → make failure reversible

### Common Faults to Simulate
- **Compute**: kill random VM/pod, simulate resource starvation
- **Network**: latency injection, packet loss, partition a service
- **Storage**: I/O throttling, disk full
- **Dependencies**: force external API to error or slow
- **Region failure**: simulate cloud AZ/region outage

### Tools & Ecosystem
- **Service-level**: Gremlin, AWS FIS, Chaos Monkey
- **Kubernetes-native**: Chaos Mesh, LitmusChaos, Steadybit
- **Pipeline-integrated**: Harness, Argo Rollouts + chaos hooks

### Resiliency Patterns
- **Circuit breakers**: prevent cascading failures
- **Retries with backoff**: exponential backoff + jitter
- **Bulkheads**: partition threadpools/connection pools
- **Fallbacks**: return degraded response instead of full failure
- **Idempotency**: required under retries/at-least-once messaging

---

## 3. Load Testing & Performance

### Types of Performance Tests
- **Load Testing**: verify system behavior under expected load
- **Stress Testing**: find system limits and breaking points
- **Spike Testing**: sudden load increases to test resilience
- **Endurance Testing**: long-running tests to find memory leaks
- **Scalability Testing**: measure performance as load increases

### Key Metrics
- **Response Time**: P50, P90, P95, P99 percentiles
- **Throughput**: requests per second (RPS)
- **Error Rate**: percentage of failed requests
- **Resource Utilization**: CPU, memory, disk, network
- **Concurrent Users**: number of simultaneous users

### Load Testing Tools
- **JMeter**: open source, extensible, distributed testing
- **Gatling**: Scala-based, high-performance, real-time reports
- **K6**: JavaScript, cloud-native, real-time metrics

---

## 4. Internet Fundamentals & Communication Protocols

### OSI 7-Layer Model
```
Layer 7: Application    - HTTP, HTTPS, FTP, SMTP, DNS
Layer 6: Presentation  - SSL/TLS, data formatting
Layer 5: Session      - NetBIOS, RPC, SQL
Layer 4: Transport    - TCP, UDP
Layer 3: Network      - IP, ICMP, routing
Layer 2: Data Link    - Ethernet, MAC addresses
Layer 1: Physical     - Cables, wireless, hardware
```

### Transport Layer Protocols

#### TCP (Transmission Control Protocol)
- **Connection-oriented**: establishes connection before data transfer
- **Reliable delivery**: guarantees data arrives in order
- **Flow control**: prevents overwhelming receiver
- **Error checking**: detects and retransmits lost packets
- **Use cases**: HTTP, HTTPS, FTP, SSH, database connections

```python
# TCP Socket Example
import socket

# Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)

while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024)
    client_socket.send(b"Hello from TCP server")
    client_socket.close()

# Client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))
client_socket.send(b"Hello server")
response = client_socket.recv(1024)
client_socket.close()
```

#### UDP (User Datagram Protocol)
- **Connectionless**: no connection establishment
- **Unreliable**: no guarantee of delivery or order
- **Fast**: minimal overhead, no connection setup
- **No flow control**: can overwhelm receiver
- **Use cases**: DNS, DHCP, streaming video, gaming, real-time data

```python
# UDP Socket Example
import socket

# Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8080))

while True:
    data, addr = server_socket.recvfrom(1024)
    server_socket.sendto(b"Hello from UDP server", addr)

# Client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(b"Hello server", ('localhost', 8080))
response, addr = client_socket.recvfrom(1024)
client_socket.close()
```

### Application Layer Protocols

#### HTTP/HTTPS
- **HTTP**: stateless, request-response protocol
- **HTTPS**: HTTP over TLS/SSL for encryption
- **Methods**: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- **Status codes**: 2xx (success), 3xx (redirect), 4xx (client error), 5xx (server error)

```python
# HTTP Client Example
import requests

# GET request
response = requests.get('https://api.example.com/users')
users = response.json()

# POST request
new_user = {'name': 'John', 'email': 'john@example.com'}
response = requests.post('https://api.example.com/users', json=new_user)

# With authentication
headers = {'Authorization': 'Bearer token123'}
response = requests.get('https://api.example.com/profile', headers=headers)
```

#### gRPC
- **High-performance**: uses HTTP/2 and Protocol Buffers
- **Strong typing**: interface-first design with code generation
- **Bidirectional streaming**: supports real-time communication
- **Use cases**: microservices, real-time APIs, mobile apps

```protobuf
// user.proto
syntax = "proto3";

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc CreateUser(CreateUserRequest) returns (User);
  rpc StreamUsers(StreamUsersRequest) returns (stream User);
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
}

message GetUserRequest {
  string user_id = 1;
}
```

```python
# gRPC Server Example
import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

class UserServicer(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        # Fetch user logic
        return user_pb2.User(
            id=request.user_id,
            name="John Doe",
            email="john@example.com"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

# gRPC Client Example
import grpc
import user_pb2
import user_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = user_pb2_grpc.UserServiceStub(channel)

request = user_pb2.GetUserRequest(user_id="123")
response = stub.GetUser(request)
print(f"User: {response.name}")
```

#### Apache Kafka
- **Distributed streaming platform**: handles high-throughput, fault-tolerant messaging
- **Pub-sub model**: producers publish to topics, consumers subscribe
- **Partitioning**: topics divided into partitions for scalability
- **Use cases**: log aggregation, stream processing, event sourcing, real-time analytics

```python
# Kafka Producer Example
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send message to topic
producer.send('user-events', {
    'event_type': 'user_created',
    'user_id': '123',
    'timestamp': '2024-01-01T00:00:00Z'
})

producer.flush()

# Kafka Consumer Example
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='user-processor'
)

for message in consumer:
    event = message.value
    print(f"Processing event: {event['event_type']} for user {event['user_id']}")
```

### Protocol Comparison

| Protocol | Reliability | Performance | Use Case | Complexity |
|----------|-------------|-------------|----------|------------|
| **TCP** | ✅ Guaranteed | 🟡 Medium | Reliable data transfer | Low |
| **UDP** | ❌ Best effort | 🟢 High | Real-time, streaming | Low |
| **HTTP** | ✅ Reliable | 🟡 Medium | Web APIs, browsers | Low |
| **gRPC** | ✅ Reliable | 🟢 High | Microservices, streaming | Medium |
| **Kafka** | ✅ Reliable | 🟢 High | Event streaming, logs | High |

### Network Security Fundamentals

#### TLS/SSL Handshake
```
1. Client Hello: Supported ciphers, random number
2. Server Hello: Chosen cipher, random number, certificate
3. Key Exchange: Generate shared secret
4. Finished: Verify handshake integrity
```

#### Firewall Rules
```bash
# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow SSH from specific IP
iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 22 -j ACCEPT

# Block all other incoming
iptables -A INPUT -j DROP
```

#### Network Monitoring
```python
# Network connectivity check
import socket
import subprocess

def check_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def ping_host(host):
    try:
        subprocess.run(['ping', '-c', '1', host], 
                      capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Usage
print(f"Database accessible: {check_port('db.example.com', 5432)}")
print(f"API accessible: {check_port('api.example.com', 443)}")
print(f"Host reachable: {ping_host('example.com')}")
```

---

## 5. Putting It All Together

### Reliability Workflow
1. **Establish Baseline**: Use observability to understand normal system behavior
2. **Define SLOs**: Set service level objectives (availability, latency, error rate)
3. **Load Test**: Verify performance under expected and peak load
4. **Chaos Test**: Inject failures to validate resilience
5. **Monitor & Alert**: Use observability to detect issues during chaos
6. **Iterate**: Improve system based on findings

### Example: E-commerce System Reliability
```
Baseline SLOs:
- 99.9% availability
- P95 latency < 200ms
- Error rate < 1%

Load Testing:
- Simulate Black Friday traffic (10x normal)
- Monitor resource utilization
- Identify bottlenecks

Chaos Testing:
- Kill random database replicas
- Inject network latency
- Simulate payment service failure

Observability:
- Real-time dashboards during tests
- Alert on SLO violations
- Trace request flows to identify issues
```

---

## 5. Practical Examples

### JMeter Load Test with Prometheus Monitoring
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="API Load Test">
      <elementProp name="TestPlan.arguments" elementType="Arguments">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <stringProp name="TestPlan.comments"></stringProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="User Group">
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">10</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">100</stringProp>
        <stringProp name="ThreadGroup.ramp_time">10</stringProp>
        <boolProp name="ThreadGroup.scheduler">false</boolProp>
        <stringProp name="ThreadGroup.duration"></stringProp>
        <stringProp name="ThreadGroup.delay"></stringProp>
      </ThreadGroup>
      <hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="API Request">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
            <collectionProp name="Arguments.arguments"/>
          </elementProp>
          <stringProp name="HTTPSampler.domain">api.example.com</stringProp>
          <stringProp name="HTTPSampler.port">443</stringProp>
          <stringProp name="HTTPSampler.protocol">https</stringProp>
          <stringProp name="HTTPSampler.path">/api/users</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
        </HTTPSamplerProxy>
        <hashTree>
          <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="Response Assertion">
            <collectionProp name="Asserion.test_strings">
              <stringProp name="49586">200</stringProp>
            </collectionProp>
            <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
            <boolProp name="Assertion.assume_success">false</boolProp>
            <intProp name="Assertion.test_type">8</intProp>
          </ResponseAssertion>
          <hashTree/>
        </hashTree>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

### Prometheus Alerting Rules for Load Tests
```yaml
groups:
  - name: load_test.rules
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{job="api",code=~"5.."}[5m]) / rate(http_requests_total{job="api"}[5m]) > 0.05
        for: 10m
        labels: { severity: critical }
        annotations:
          summary: "High 5xx error rate during load test"
          description: ">5% 5xx over 10m"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="api"}[5m])) > 0.5
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "High P95 latency during load test"
          description: "P95 > 500ms for 5m"

      - alert: HighCPU
        expr: avg(rate(container_cpu_usage_seconds_total{container!="",pod=~"api.*"}[5m])) > 0.8
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "High CPU usage during load test"
          description: "CPU > 80% for 5m"
```

### Chaos Experiment with Monitoring
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: pod-kill-with-monitoring
spec:
  appinfo:
    appns: default
    applabel: app=api-service
    appkind: deployment
  annotationCheck: "false"
  engineState: active
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "60"
            - name: CHAOS_INTERVAL
              value: "10"
            - name: FORCE
              value: "false"
          monitor:
            - name: "prometheus"
              url: "http://prometheus:9090"
              queries:
                - name: "error_rate"
                  query: 'rate(http_requests_total{job="api",code=~"5.."}[5m])'
                - name: "latency_p95"
                  query: 'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="api"}[5m]))'
```

---

## 6. Reliability Metrics & SLOs

### Service Level Objectives (SLOs)
- **Availability**: 99.9% uptime (allows ~43 minutes downtime/month)
- **Latency**: P95 < 200ms, P99 < 500ms
- **Error Rate**: < 1% for critical endpoints
- **Throughput**: handle expected peak load + 50% buffer

### Error Budgets
- **Budget = 1 - SLO** (e.g., 99.9% → 0.1% = 43 minutes/month)
- **Burn Rate Alerts**:
  - Fast burn: 2% of budget in 1 hour → page immediately
  - Slow burn: 5% of budget in 6 hours → investigate

### Reliability Scorecard
```
System: E-commerce API
Availability: 99.95% (target: 99.9%) ✅
Latency P95: 180ms (target: <200ms) ✅
Error Rate: 0.8% (target: <1%) ✅
Throughput: 1500 RPS (target: 1000 RPS) ✅

Reliability Grade: A
```

---

## 7. Reliability Testing Schedule

### Daily
- **Health Checks**: automated health checks on all services
- **Metrics Review**: quick review of key metrics and trends

### Weekly
- **Load Testing**: run baseline load tests
- **Chaos Experiments**: small-scale chaos experiments
- **SLO Review**: analyze SLO performance and trends

### Monthly
- **Comprehensive Load Testing**: full system load testing
- **Chaos Day**: coordinated chaos experiments across teams
- **Reliability Review**: comprehensive reliability assessment

### Quarterly
- **Disaster Recovery**: test full disaster recovery procedures
- **Capacity Planning**: review and update capacity plans
- **Tool Evaluation**: assess and update reliability tools

---

## 8. Tools Integration

### Prometheus + Grafana + AlertManager
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

scrape_configs:
  - job_name: 'api-service'
    static_configs:
      - targets: ['api-service:8080']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

### Load Testing in CI/CD
```yaml
# .github/workflows/reliability-test.yml
name: Reliability Testing
on: [push, pull_request]

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Load Test
        run: |
          k6 run load-test.js
        env:
          K6_PROMETHEUS_RW_SERVER_URL: ${{ secrets.PROMETHEUS_URL }}

  chaos-test:
    runs-on: ubuntu-latest
    needs: load-test
    steps:
      - uses: actions/checkout@v3
      - name: Run Chaos Experiment
        run: |
          kubectl apply -f chaos-experiment.yaml
          # Wait and monitor
          kubectl delete -f chaos-experiment.yaml
```

---

## 9. Best Practices

### Observability
- **Instrument Everything**: metrics, logs, and traces for all services
- **Correlate Data**: link metrics, logs, and traces with correlation IDs
- **Set Meaningful Alerts**: alert on symptoms, not causes
- **Document Runbooks**: clear procedures for common issues

### Chaos Engineering
- **Start Small**: begin with simple experiments in non-critical environments
- **Automate Rollback**: ensure experiments can be stopped quickly
- **Measure Impact**: quantify the effect of chaos experiments
- **Learn and Improve**: use findings to improve system resilience

### Load Testing
- **Test Realistic Scenarios**: simulate actual user behavior
- **Monitor During Tests**: observe system behavior under load
- **Test Failure Scenarios**: verify system behavior when components fail
- **Document Baselines**: establish performance baselines for comparison

---

## 10. Common Reliability Patterns

### Circuit Breaker
The **Circuit Breaker** pattern is a reliability design pattern that prevents cascading failures by temporarily stopping requests to a failing service. It works like an electrical circuit breaker - when there are too many failures, it "trips" and stops allowing requests through.

**How it works:**
1. **CLOSED State**: Normal operation - requests pass through to the service
2. **OPEN State**: Service is failing - requests are immediately rejected
3. **HALF_OPEN State**: Testing if service has recovered - limited requests allowed

**When to use:**
- External API calls that might fail
- Database connections that could timeout
- Microservice communication
- Any dependency that could cause cascading failures

```python
import time

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold    # How many failures before opening circuit
        self.recovery_timeout = recovery_timeout      # Seconds to wait before testing recovery
        self.failure_count = 0                       # Current failure count
        self.last_failure_time = 0                   # Timestamp of last failure
        self.state = "CLOSED"                        # Current state: CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        # Check if circuit is OPEN (service failing)
        if self.state == "OPEN":
            # Check if enough time has passed to test recovery
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"             # Try to test if service recovered
            else:
                raise Exception("Circuit breaker is OPEN - service is failing")
        
        try:
            # Attempt to call the actual service
            result = func(*args, **kwargs)
            
            # If we're in HALF_OPEN and call succeeds, close the circuit
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"                 # Service has recovered
                self.failure_count = 0                # Reset failure count
            
            return result
        except Exception as e:
            # Call failed - increment failure count
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            # If we've hit the failure threshold, open the circuit
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"                   # Stop allowing requests
            
            raise e                                  # Re-raise the original exception

# Usage example
def unreliable_api_call():
    # Simulate an API call that sometimes fails
    import random
    if random.random() < 0.3:  # 30% chance of failure
        raise Exception("API call failed")
    return "Success!"

# Create circuit breaker instance
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

# Use it to protect API calls
try:
    result = breaker.call(unreliable_api_call)
    print(f"API call succeeded: {result}")
except Exception as e:
    print(f"API call failed: {e}")
```

### Retry with Exponential Backoff
```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
```

### Health Check Endpoint
```python
from flask import Flask, jsonify
import psutil
import redis

app = Flask(__name__)

@app.route('/health')
def health_check():
    health_status = {
        'status': 'healthy',
        'timestamp': time.time(),
        'checks': {}
    }
    
    # Check CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    health_status['checks']['cpu'] = {
        'status': 'healthy' if cpu_percent < 80 else 'unhealthy',
        'value': cpu_percent
    }
    
    # Check memory usage
    memory_percent = psutil.virtual_memory().percent
    health_status['checks']['memory'] = {
        'status': 'healthy' if memory_percent < 90 else 'unhealthy',
        'value': memory_percent
    }
    
    # Check Redis connection
    try:
        redis_client = redis.Redis(host='localhost', port=6379)
        redis_client.ping()
        health_status['checks']['redis'] = {'status': 'healthy'}
    except:
        health_status['checks']['redis'] = {'status': 'unhealthy'}
    
    # Overall status
    all_healthy = all(check['status'] == 'healthy' for check in health_status['checks'].values())
    health_status['status'] = 'healthy' if all_healthy else 'unhealthy'
    
    return jsonify(health_status), 200 if all_healthy else 503
```

---

## 11. Reliability Checklist

### Pre-Production
- [ ] SLOs defined and documented
- [ ] Monitoring and alerting configured
- [ ] Load testing completed
- [ ] Chaos experiments planned
- [ ] Runbooks documented
- [ ] Rollback procedures tested

### Production
- [ ] Real-time monitoring active
- [ ] Alerts configured and tested
- [ ] Incident response team ready
- [ ] Backup and recovery tested
- [ ] Performance baselines established
- [ ] Reliability metrics tracked

### Continuous Improvement
- [ ] Regular reliability reviews scheduled
- [ ] Post-incident analysis conducted
- [ ] SLOs updated based on findings
- [ ] New chaos experiments planned
- [ ] Tools and processes evaluated
- [ ] Team training conducted

---

*Reliability engineering is not a one-time effort but a continuous process of building, testing, and improving system resilience.*

---

## 12. Production Operations & Incident Response

### Incident Response Framework

#### On-Call Procedures
**Escalation Matrix**
```
Level 1 (PagerDuty): Primary on-call engineer
- Response time: 5 minutes
- Escalation: 15 minutes if no acknowledgment

Level 2: Senior engineer or team lead
- Response time: 15 minutes
- Escalation: 30 minutes if no resolution

Level 3: Engineering manager or architect
- Response time: 30 minutes
- Escalation: 1 hour if no resolution

Level 4: CTO/VP Engineering
- Response time: 1 hour
- Escalation: 2 hours if no resolution
```

**Incident Severity Levels**
```
SEV-1 (Critical): Service completely down, data loss
- Response: Immediate (within 5 minutes)
- Communication: All stakeholders, status page updates
- Resolution target: 1 hour

SEV-2 (High): Major feature broken, significant performance degradation
- Response: Within 15 minutes
- Communication: Engineering team, product managers
- Resolution target: 4 hours

SEV-3 (Medium): Minor feature broken, slight performance impact
- Response: Within 1 hour
- Communication: Engineering team
- Resolution target: 24 hours

SEV-4 (Low): Cosmetic issues, minor bugs
- Response: Within 4 hours
- Communication: Engineering team
- Resolution target: 1 week
```

#### Incident Response Process
```python
# Incident response workflow
class IncidentResponse:
    def __init__(self):
        self.incident_id = None
        self.severity = None
        self.status = "open"
        self.timeline = []
        self.actions_taken = []
    
    def acknowledge(self, engineer, timestamp):
        """Acknowledge incident and assign primary responder"""
        self.primary_responder = engineer
        self.timeline.append({
            "timestamp": timestamp,
            "action": "acknowledged",
            "engineer": engineer
        })
    
    def escalate(self, level, reason, timestamp):
        """Escalate to next level if needed"""
        self.current_level = level
        self.timeline.append({
            "timestamp": timestamp,
            "action": "escalated",
            "level": level,
            "reason": reason
        })
    
    def update_status(self, status, details, timestamp):
        """Update incident status"""
        self.status = status
        self.timeline.append({
            "timestamp": timestamp,
            "action": "status_update",
            "status": status,
            "details": details
        })
    
    def resolve(self, resolution, timestamp):
        """Mark incident as resolved"""
        self.status = "resolved"
        self.resolution = resolution
        self.timeline.append({
            "timestamp": timestamp,
            "action": "resolved",
            "resolution": resolution
        })
```

### Post-Incident Analysis

#### Blameless Post-Mortem Template
```markdown
# Post-Mortem: [Incident Title]

## Incident Summary
- **Date/Time**: [When it started]
- **Duration**: [How long it lasted]
- **Severity**: [SEV-1/2/3/4]
- **Impact**: [Users affected, business impact]

## Timeline
- **Detection**: [When/how was it detected]
- **Response**: [Initial response actions]
- **Escalation**: [When/why escalated]
- **Resolution**: [How it was fixed]

## Root Cause Analysis
- **What happened**: [Technical explanation]
- **Why it happened**: [Root cause]
- **Contributing factors**: [Other factors that played a role]

## Impact Assessment
- **User impact**: [Number of users affected]
- **Business impact**: [Revenue, reputation, etc.]
- **Technical impact**: [System performance, data loss]

## Actions Taken
- **Immediate**: [What was done to fix it]
- **Short-term**: [Actions in next 24-48 hours]
- **Long-term**: [Preventive measures]

## Lessons Learned
- **What went well**: [Positive aspects of response]
- **What could be improved**: [Areas for improvement]
- **What surprised us**: [Unexpected findings]

## Action Items
- [ ] [Action item 1] - [Owner] - [Due date]
- [ ] [Action item 2] - [Owner] - [Due date]
- [ ] [Action item 3] - [Owner] - [Due date]
```

### Performance Debugging at Scale

#### Distributed System Debugging
```python
# Distributed tracing for performance debugging
import opentelemetry
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

class PerformanceDebugger:
    def __init__(self):
        self.tracer = trace.get_tracer(__name__)
    
    def trace_database_query(self, query, params):
        """Trace database query performance"""
        with self.tracer.start_as_current_span("database_query") as span:
            span.set_attribute("db.query", query)
            span.set_attribute("db.params", str(params))
            
            start_time = time.time()
            try:
                result = self.execute_query(query, params)
                duration = time.time() - start_time
                
                span.set_attribute("db.duration", duration)
                span.set_attribute("db.rows_returned", len(result))
                span.set_status(Status(StatusCode.OK))
                
                return result
            except Exception as e:
                span.set_attribute("db.error", str(e))
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise
    
    def trace_api_call(self, endpoint, method):
        """Trace API call performance"""
        with self.tracer.start_as_current_span("api_call") as span:
            span.set_attribute("http.url", endpoint)
            span.set_attribute("http.method", method)
            
            start_time = time.time()
            try:
                response = self.make_api_call(endpoint, method)
                duration = time.time() - start_time
                
                span.set_attribute("http.duration", duration)
                span.set_attribute("http.status_code", response.status_code)
                span.set_status(Status(StatusCode.OK))
                
                return response
            except Exception as e:
                span.set_attribute("http.error", str(e))
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise
```

#### Performance Metrics Collection
```python
# Performance metrics for debugging
import time
import psutil
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class PerformanceMetrics:
    timestamp: float
    cpu_percent: float
    memory_percent: float
    disk_io: Dict[str, float]
    network_io: Dict[str, float]
    response_time: float
    throughput: float

class PerformanceMonitor:
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
    
    def collect_metrics(self, response_time: float, throughput: float):
        """Collect current system performance metrics"""
        metrics = PerformanceMetrics(
            timestamp=time.time(),
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_percent=psutil.virtual_memory().percent,
            disk_io=self._get_disk_io(),
            network_io=self._get_network_io(),
            response_time=response_time,
            throughput=throughput
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def _get_disk_io(self) -> Dict[str, float]:
        """Get disk I/O statistics"""
        disk_io = psutil.disk_io_counters()
        return {
            "read_bytes": disk_io.read_bytes,
            "write_bytes": disk_io.write_bytes,
            "read_count": disk_io.read_count,
            "write_count": disk_io.write_count
        }
    
    def _get_network_io(self) -> Dict[str, float]:
        """Get network I/O statistics"""
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }
    
    def analyze_performance(self) -> Dict[str, any]:
        """Analyze performance trends"""
        if len(self.metrics_history) < 10:
            return {"error": "Insufficient data"}
        
        recent_metrics = self.metrics_history[-10:]
        
        avg_response_time = sum(m.response_time for m in recent_metrics) / len(recent_metrics)
        avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
        
        return {
            "avg_response_time": avg_response_time,
            "avg_cpu_usage": avg_cpu,
            "avg_memory_usage": avg_memory,
            "trend": self._calculate_trend(recent_metrics)
        }
    
    def _calculate_trend(self, metrics: List[PerformanceMetrics]) -> str:
        """Calculate performance trend"""
        if len(metrics) < 2:
            return "stable"
        
        first_half = metrics[:len(metrics)//2]
        second_half = metrics[len(metrics)//2:]
        
        first_avg = sum(m.response_time for m in first_half) / len(first_half)
        second_avg = sum(m.response_time for m in second_half) / len(second_half)
        
        if second_avg > first_avg * 1.1:
            return "degrading"
        elif second_avg < first_avg * 0.9:
            return "improving"
        else:
            return "stable"
```

### SLO/SLI Management

#### Service Level Objectives
```python
# SLO/SLI implementation
from dataclasses import dataclass
from typing import List, Dict
import time

@dataclass
class SLO:
    name: str
    target: float  # Target percentage (e.g., 99.9)
    measurement_window: int  # Window in seconds
    error_budget: float  # Error budget percentage

@dataclass
class SLI:
    name: str
    good_events: int
    total_events: int
    timestamp: float

class SLOManager:
    def __init__(self):
        self.slos: List[SLO] = []
        self.sli_data: List[SLI] = []
    
    def add_slo(self, name: str, target: float, window: int):
        """Add a new SLO"""
        slo = SLO(
            name=name,
            target=target,
            measurement_window=window,
            error_budget=100 - target
        )
        self.slos.append(slo)
    
    def record_sli(self, name: str, success: bool):
        """Record an SLI measurement"""
        sli = SLI(
            name=name,
            good_events=1 if success else 0,
            total_events=1,
            timestamp=time.time()
        )
        self.sli_data.append(sli)
    
    def calculate_slo_health(self, slo_name: str) -> Dict[str, any]:
        """Calculate current SLO health"""
        slo = next((s for s in self.slos if s.name == slo_name), None)
        if not slo:
            return {"error": "SLO not found"}
        
        # Get data within measurement window
        cutoff_time = time.time() - slo.measurement_window
        relevant_data = [s for s in self.sli_data 
                        if s.name == slo_name and s.timestamp > cutoff_time]
        
        if not relevant_data:
            return {"error": "No data in measurement window"}
        
        total_good = sum(s.good_events for s in relevant_data)
        total_events = sum(s.total_events for s in relevant_data)
        
        if total_events == 0:
            return {"error": "No events recorded"}
        
        current_sli = (total_good / total_events) * 100
        error_budget_remaining = current_sli - slo.target
        
        return {
            "slo_name": slo_name,
            "target": slo.target,
            "current_sli": current_sli,
            "error_budget_remaining": error_budget_remaining,
            "status": "healthy" if current_sli >= slo.target else "unhealthy",
            "measurement_window": slo.measurement_window
        }
    
    def get_error_budget_burn_rate(self, slo_name: str) -> float:
        """Calculate error budget burn rate"""
        slo = next((s for s in self.slos if s.name == slo_name), None)
        if not slo:
            return 0.0
        
        # Calculate burn rate over last hour vs last 24 hours
        one_hour_ago = time.time() - 3600
        one_day_ago = time.time() - 86400
        
        hourly_data = [s for s in self.sli_data 
                      if s.name == slo_name and s.timestamp > one_hour_ago]
        daily_data = [s for s in self.sli_data 
                     if s.name == slo_name and s.timestamp > one_day_ago]
        
        if not hourly_data or not daily_data:
            return 0.0
        
        hourly_failure_rate = 1 - (sum(s.good_events for s in hourly_data) / 
                                  sum(s.total_events for s in hourly_data))
        daily_failure_rate = 1 - (sum(s.good_events for s in daily_data) / 
                                 sum(s.total_events for s in daily_data))
        
        if daily_failure_rate == 0:
            return 0.0
        
        return hourly_failure_rate / daily_failure_rate
```

#### SLO Configuration Examples
```yaml
# SLO configuration for different services
slo_configs:
  api_latency:
    name: "API Response Time"
    target: 99.9
    measurement_window: 3600  # 1 hour
    sli_type: "latency"
    thresholds:
      p50: 100ms
      p95: 500ms
      p99: 1000ms
  
  availability:
    name: "Service Availability"
    target: 99.95
    measurement_window: 86400  # 24 hours
    sli_type: "availability"
    health_check_endpoint: "/health"
  
  throughput:
    name: "Request Throughput"
    target: 99.0
    measurement_window: 300  # 5 minutes
    sli_type: "throughput"
    min_requests_per_second: 1000
```

### Capacity Planning & Cost Forecasting

#### Capacity Planning Framework
```python
# Capacity planning and forecasting
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class CapacityRequirement:
    cpu_cores: float
    memory_gb: float
    storage_gb: float
    network_mbps: float
    cost_per_hour: float

class CapacityPlanner:
    def __init__(self):
        self.historical_usage: List[Dict] = []
        self.growth_rates: Dict[str, float] = {}
    
    def add_usage_data(self, timestamp: float, usage: Dict[str, float]):
        """Add historical usage data"""
        self.historical_usage.append({
            "timestamp": timestamp,
            "usage": usage
        })
    
    def calculate_growth_rate(self, metric: str, days: int = 30) -> float:
        """Calculate growth rate for a specific metric"""
        if len(self.historical_usage) < 2:
            return 0.0
        
        # Get data from last N days
        cutoff_time = time.time() - (days * 86400)
        recent_data = [h for h in self.historical_usage 
                      if h["timestamp"] > cutoff_time]
        
        if len(recent_data) < 2:
            return 0.0
        
        # Sort by timestamp
        recent_data.sort(key=lambda x: x["timestamp"])
        
        # Calculate growth rate
        initial_value = recent_data[0]["usage"].get(metric, 0)
        final_value = recent_data[-1]["usage"].get(metric, 0)
        
        if initial_value == 0:
            return 0.0
        
        time_diff_days = (recent_data[-1]["timestamp"] - recent_data[0]["timestamp"]) / 86400
        
        # Annual growth rate
        growth_rate = ((final_value / initial_value) ** (365 / time_diff_days)) - 1
        return growth_rate
    
    def forecast_capacity(self, metric: str, months_ahead: int) -> float:
        """Forecast capacity needs X months ahead"""
        current_usage = self.historical_usage[-1]["usage"].get(metric, 0)
        growth_rate = self.growth_rates.get(metric, self.calculate_growth_rate(metric))
        
        # Compound growth
        months = months_ahead
        forecasted_usage = current_usage * ((1 + growth_rate) ** (months / 12))
        
        return forecasted_usage
    
    def calculate_cost_forecast(self, months_ahead: int) -> Dict[str, float]:
        """Calculate cost forecast for different resources"""
        cpu_forecast = self.forecast_capacity("cpu_cores", months_ahead)
        memory_forecast = self.forecast_capacity("memory_gb", months_ahead)
        storage_forecast = self.forecast_capacity("storage_gb", months_ahead)
        
        # AWS pricing (example)
        cpu_cost_per_hour = 0.0416  # t3.medium
        memory_cost_per_hour = 0.0056  # per GB
        storage_cost_per_month = 0.023  # per GB
        
        monthly_cpu_cost = cpu_forecast * cpu_cost_per_hour * 730  # hours per month
        monthly_memory_cost = memory_forecast * memory_cost_per_hour * 730
        monthly_storage_cost = storage_forecast * storage_cost_per_month
        
        total_monthly_cost = monthly_cpu_cost + monthly_memory_cost + monthly_storage_cost
        
        return {
            "cpu_cost": monthly_cpu_cost,
            "memory_cost": monthly_memory_cost,
            "storage_cost": monthly_storage_cost,
            "total_cost": total_monthly_cost,
            "forecast_months": months_ahead
        }
    
    def optimize_costs(self, target_cost: float) -> Dict[str, any]:
        """Find cost optimization opportunities"""
        current_monthly_cost = self.calculate_cost_forecast(0)["total_cost"]
        
        if current_monthly_cost <= target_cost:
            return {"status": "within_budget", "current_cost": current_monthly_cost}
        
        # Find optimization opportunities
        optimizations = []
        
        # Reserved instances (30% savings)
        reserved_savings = current_monthly_cost * 0.3
        optimizations.append({
            "type": "reserved_instances",
            "savings": reserved_savings,
            "implementation": "Purchase 1-year reserved instances"
        })
        
        # Spot instances for non-critical workloads (50% savings on 20% of instances)
        spot_savings = current_monthly_cost * 0.2 * 0.5
        optimizations.append({
            "type": "spot_instances",
            "savings": spot_savings,
            "implementation": "Use spot instances for batch processing"
        })
        
        # Storage optimization (20% savings)
        storage_savings = self.calculate_cost_forecast(0)["storage_cost"] * 0.2
        optimizations.append({
            "type": "storage_optimization",
            "savings": storage_savings,
            "implementation": "Implement lifecycle policies and compression"
        })
        
        total_potential_savings = sum(o["savings"] for o in optimizations)
        optimized_cost = current_monthly_cost - total_potential_savings
        
        return {
            "current_cost": current_monthly_cost,
            "target_cost": target_cost,
            "optimizations": optimizations,
            "total_savings": total_potential_savings,
            "optimized_cost": optimized_cost,
            "within_budget": optimized_cost <= target_cost
        }
```

---

# Security & Compliance

## Security & Compliance

## 1. HIPAA Compliance

### Protected Health Information (PHI)
- **Definition**: Individually identifiable health information
- **Examples**: Names, addresses, dates, medical records, insurance info
- **Storage**: Must be encrypted at rest and in transit

### Business Associate Agreement (BAA)
- **Required**: When sharing PHI with third-party services
- **Coverage**: Data processing, storage, transmission
- **Penalties**: Up to $50,000 per violation

### Technical Safeguards
- **Access Control**: Unique user identification, automatic logoff
- **Audit Controls**: Record and examine access to PHI
- **Integrity**: Ensure PHI is not altered or destroyed
- **Transmission Security**: Encrypt PHI in transit

### Physical Safeguards
- **Facility Access**: Control physical access to facilities
- **Workstation Security**: Secure workstations and devices
- **Media Controls**: Control access to media containing PHI

---

## 2. Security Patterns

### Authentication
- **Multi-Factor Authentication (MFA)**: Something you know, have, are
- **OAuth 2.0**: Authorization framework for third-party access
- **JWT Tokens**: Stateless authentication with expiration
- **Session Management**: Secure session creation and termination

### Authorization
- **Role-Based Access Control (RBAC)**: Assign permissions to roles
- **Attribute-Based Access Control (ABAC)**: Dynamic access based on attributes
- **Principle of Least Privilege**: Minimum access necessary
- **Just-In-Time Access**: Temporary elevated permissions

### Encryption
- **At Rest**: AES-256 for stored data
- **In Transit**: TLS 1.3 for network communication
- **Key Management**: Hardware Security Modules (HSM)
- **Data Classification**: Different encryption levels for different data types

---

## 3. Common Security Vulnerabilities

### OWASP Top 10
1. **Injection**: SQL, NoSQL, OS command injection
2. **Broken Authentication**: Weak passwords, session fixation
3. **Sensitive Data Exposure**: Unencrypted data, weak algorithms
4. **XML External Entities**: XXE attacks on XML processors
5. **Broken Access Control**: Insecure direct object references
6. **Security Misconfiguration**: Default settings, unnecessary features
7. **Cross-Site Scripting (XSS)**: Stored, reflected, DOM-based
8. **Insecure Deserialization**: Object injection attacks
9. **Using Components with Known Vulnerabilities**: Outdated libraries
10. **Insufficient Logging & Monitoring**: Lack of security visibility

### Prevention Strategies
- **Input Validation**: Sanitize all user inputs
- **Output Encoding**: Encode data before sending to browser
- **Security Headers**: CSP, HSTS, X-Frame-Options
- **Regular Updates**: Keep dependencies and systems updated

---

## 4. Security Implementation Examples

### Secure Password Storage
```python
import bcrypt
import secrets

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def generate_secure_token():
    return secrets.token_urlsafe(32)
```

### JWT Implementation
```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"

def create_token(user_id, expires_in=3600):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
```

### Rate Limiting
```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id):
        now = time.time()
        client_requests = self.requests[client_id]
        
        # Remove old requests outside window
        client_requests[:] = [req_time for req_time in client_requests 
                            if now - req_time < self.window_seconds]
        
        if len(client_requests) >= self.max_requests:
            return False
        
        client_requests.append(now)
        return True

# Usage
limiter = RateLimiter(max_requests=100, window_seconds=60)
if limiter.is_allowed("user123"):
    # Process request
    pass
else:
    # Rate limit exceeded
    pass
```

---

## 5. HTTPS & Transport Layer Security

### How HTTPS Works
HTTPS (HTTP Secure) combines HTTP with TLS/SSL encryption to provide:
- **Confidentiality**: Data is encrypted and cannot be read by interceptors
- **Integrity**: Data cannot be modified without detection
- **Authentication**: Verifies the server's identity

### TLS Handshake Process
```
1. Client Hello
   ├── Supported TLS versions
   ├── Supported cipher suites
   ├── Random number
   └── Session ID (if resuming)

2. Server Hello
   ├── Chosen TLS version
   ├── Chosen cipher suite
   ├── Random number
   ├── Session ID
   └── Digital certificate

3. Certificate Verification
   ├── Client verifies server certificate
   ├── Checks certificate chain
   └── Validates domain name

4. Key Exchange
   ├── Client generates pre-master secret
   ├── Encrypts with server's public key
   └── Both sides derive master secret

5. Finished
   ├── Both sides verify handshake
   ├── Switch to encrypted communication
   └── Application data exchange begins
```

### SSL/TLS Configuration
```nginx
# Nginx HTTPS configuration
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # SSL certificate and key
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/ssl/certs/chain.crt;
}
```

### Certificate Management
```bash
# Generate private key
openssl genrsa -out private.key 2048

# Generate CSR (Certificate Signing Request)
openssl req -new -key private.key -out request.csr

# Generate self-signed certificate (for testing)
openssl req -x509 -new -nodes -key private.key -sha256 -days 365 -out certificate.crt

# Check certificate details
openssl x509 -in certificate.crt -text -noout

# Convert between formats
openssl x509 -in certificate.crt -outform DER -out certificate.der
```

---

## 6. Essential Security Libraries & Tools

### Python Security Libraries
```python
# Cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Secure random generation
import secrets
import os

# Password hashing
import bcrypt
import passlib.hash

# JWT handling
import PyJWT

# Input validation
import validators
import bleach

# Security headers
from flask_talisman import Talisman
```

### Security Headers Implementation
```python
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

# Configure security headers
Talisman(app,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
        'font-src': "'self'",
        'connect-src': "'self'",
        'frame-ancestors': "'none'"
    },
    force_https=True,
    strict_transport_security=True,
    session_cookie_secure=True
)

@app.route('/')
def index():
    return 'Secure Flask App'
```

### Input Sanitization
```python
import bleach
import validators
from urllib.parse import urlparse

def sanitize_html(html_content):
    """Remove potentially dangerous HTML"""
    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li']
    allowed_attributes = {}
    
    return bleach.clean(html_content, 
                        tags=allowed_tags, 
                        attributes=allowed_attributes,
                        strip=True)

def validate_url(url):
    """Validate and sanitize URLs"""
    if not validators.url(url):
        return None
    
    parsed = urlparse(url)
    if parsed.scheme not in ['http', 'https']:
        return None
    
    return url

def sanitize_filename(filename):
    """Remove dangerous characters from filenames"""
    import re
    # Remove or replace dangerous characters
    safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return safe_filename[:255]  # Limit length
```

### Secure File Upload
```python
import os
import hashlib
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_file_upload(file, upload_folder):
    if file and allowed_file(file.filename):
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Generate unique filename to prevent conflicts
        file_hash = hashlib.md5(file.read()).hexdigest()
        file.seek(0)  # Reset file pointer
        
        # Create safe filename with hash
        safe_filename = f"{file_hash}_{filename}"
        filepath = os.path.join(upload_folder, safe_filename)
        
        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            raise ValueError("File too large")
        
        # Save file
        file.save(filepath)
        return safe_filename
    
    raise ValueError("Invalid file type or no file provided")
```

---

## 7. Security Best Practices

### Development Security
- **Secure by Default**: Deny access unless explicitly allowed
- **Input Validation**: Validate and sanitize all inputs
- **Output Encoding**: Encode data before sending to clients
- **Error Handling**: Don't expose sensitive information in errors
- **Logging**: Log security events without sensitive data

### Production Security
- **Regular Updates**: Keep systems and dependencies updated
- **Access Control**: Implement least privilege access
- **Monitoring**: Monitor for suspicious activities
- **Backup Security**: Encrypt backups and test restoration
- **Incident Response**: Have a plan for security incidents

### Security Testing
- **Static Analysis**: Use tools like Bandit, Semgrep
- **Dynamic Testing**: Regular penetration testing
- **Dependency Scanning**: Check for known vulnerabilities
- **Code Reviews**: Security-focused code reviews
- **Automated Testing**: Security tests in CI/CD pipeline

### Compliance Checklist
- [ ] Data encryption at rest and in transit
- [ ] Access controls and authentication
- [ ] Audit logging and monitoring
- [ ] Regular security assessments
- [ ] Employee security training
- [ ] Incident response procedures
- [ ] Data backup and recovery
- [ ] Vendor security assessments
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.JWTError:
        raise Exception("Invalid token")
```

### Rate Limiting
```python
import redis
import time

class RateLimiter:
    def __init__(self, redis_client, max_requests, window_seconds):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    def is_allowed(self, key):
        current = int(time.time())
        window_start = current - self.window_seconds
        
        # Remove expired entries
        self.redis.zremrangebyscore(key, 0, window_start)
        
        # Count current requests
        current_requests = self.redis.zcard(key)
        
        if current_requests < self.max_requests:
            self.redis.zadd(key, {current: current})
            self.redis.expire(key, self.window_seconds)
            return True
        
        return False
```

---

## 5. Compliance Checklists

### HIPAA Technical Safeguards
- [ ] Unique user identification implemented
- [ ] Automatic logoff configured
- [ ] Encryption at rest enabled
- [ ] Encryption in transit enabled
- [ ] Audit logging configured
- [ ] Access controls implemented
- [ ] Integrity controls in place

### HIPAA Audit Preparation & Process
**What HIPAA Auditors Look For:**

1. **Administrative Safeguards**
   - [ ] Security officer designated and trained
   - [ ] Workforce security policies documented
   - [ ] Information access management procedures
   - [ ] Security incident procedures documented
   - [ ] Contingency plan tested annually
   - [ ] Business associate agreements (BAAs) in place

2. **Physical Safeguards**
   - [ ] Facility access controls implemented
   - [ ] Workstation use policies documented
   - [ ] Workstation security measures in place
   - [ ] Device and media controls established
   - [ ] Media disposal procedures documented

3. **Technical Safeguards**
   - [ ] Access control implementation verified
   - [ ] Audit logs enabled and monitored
   - [ ] Integrity controls implemented
   - [ ] Person/entity authentication verified
   - [ ] Transmission security measures in place

**Common HIPAA Compliance Gaps:**
- Missing or outdated BAAs with vendors
- Inadequate audit logging and monitoring
- Insufficient encryption key management
- Lack of regular security assessments
- Missing incident response documentation
- Incomplete workforce training records

**Audit Preparation Checklist:**
- [ ] Review all policies and procedures
- [ ] Verify BAA compliance with vendors
- [ ] Test backup and recovery procedures
- [ ] Review access control logs
- [ ] Verify encryption implementation
- [ ] Prepare workforce training records
- [ ] Review incident response procedures
- [ ] Test contingency plan procedures

### Security Algorithm Deep Dive

#### JWT Signing Algorithms Comparison

**HS256 (HMAC with SHA-256)**
- **Type**: Symmetric (same key for signing and verification)
- **Security**: High when using strong secret keys
- **Use Case**: Single-party applications, internal services
- **Pros**: Fast, simple key management
- **Cons**: Key must be shared securely, can't verify origin

**RS256 (RSA with SHA-256)**
- **Type**: Asymmetric (public/private key pair)
- **Security**: Very high, industry standard
- **Use Case**: Multi-party applications, public APIs
- **Pros**: Can verify token origin, private key never shared
- **Cons**: Slower than HS256, more complex key management

**ES256 (ECDSA with SHA-256)**
- **Type**: Asymmetric (elliptic curve)
- **Security**: Very high, smaller key sizes
- **Use Case**: Resource-constrained environments
- **Pros**: Fast verification, small key sizes
- **Cons**: More complex implementation, newer standard

**Algorithm Selection Guide:**
```python
# For internal services (single organization)
ALGORITHM = "HS256"  # Use strong secret key (32+ bytes)

# For public APIs or multi-tenant systems
ALGORITHM = "RS256"  # Use RSA key pair

# For IoT or mobile applications
ALGORITHM = "ES256"  # Use ECDSA for efficiency

# Implementation example with algorithm selection
def create_token_with_algorithm(data: dict, algorithm: str = "HS256"):
    if algorithm == "HS256":
        return jwt.encode(data, SECRET_KEY, algorithm=algorithm)
    elif algorithm == "RS256":
        return jwt.encode(data, PRIVATE_KEY, algorithm=algorithm)
    elif algorithm == "ES256":
        return jwt.encode(data, ECDSA_PRIVATE_KEY, algorithm=algorithm)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
```

#### Encryption Key Management Best Practices

**Key Rotation Strategy:**
- **HS256**: Rotate secret keys every 90 days
- **RS256/ES256**: Rotate private keys every 1-2 years
- **Public keys**: Can be published and shared freely

**Key Storage Security:**
```python
# Secure key storage examples
import os
from cryptography.fernet import Fernet

# Environment variable (for development)
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

# AWS KMS (for production)
import boto3
kms = boto3.client('kms')
response = kms.decrypt(CiphertextBlob=encrypted_key)
SECRET_KEY = response['Plaintext']

# HashiCorp Vault (enterprise)
import hvac
client = hvac.Client(url='https://vault.example.com')
SECRET_KEY = client.secrets.kv.v2.read_secret_version(path='jwt-secret')['data']['data']['key']
```

### General Security Checklist
- [ ] MFA enabled for all users
- [ ] Regular security training conducted
- [ ] Vulnerability scanning scheduled
- [ ] Incident response plan documented
- [ ] Backup and recovery tested
- [ ] Security monitoring active
- [ ] Access reviews conducted quarterly

### Data Protection Checklist
- [ ] Data classification completed
- [ ] Encryption policies defined
- [ ] Key management procedures documented
- [ ] Data retention policies established
- [ ] Privacy impact assessments completed
- [ ] Consent mechanisms implemented
- [ ] Data breach response plan ready

---

## 6. Security Monitoring

### Log Management
- **Centralized Logging**: Aggregate logs from all systems
- **Log Analysis**: Use SIEM tools for correlation
- **Retention Policies**: Keep logs for compliance requirements
- **Access Controls**: Restrict log access to security team

### Incident Response
- **Detection**: Automated alerts for suspicious activity
- **Response**: Documented procedures for different incident types
- **Recovery**: Steps to restore normal operations
- **Post-Incident**: Lessons learned and process improvements

### Security Metrics
- **Mean Time to Detection (MTTD)**: How quickly threats are identified
- **Mean Time to Response (MTTR)**: How quickly threats are contained
- **False Positive Rate**: Accuracy of security alerts
- **Vulnerability Remediation Time**: Speed of patch deployment

---

## 7. Cloud Security

### AWS Security Best Practices
- **IAM**: Use least privilege, enable MFA
- **VPC**: Isolate resources, use security groups
- **Encryption**: Enable encryption for S3, RDS, EBS
- **Monitoring**: Use CloudTrail, CloudWatch, GuardDuty

### Azure Security Best Practices
- **Azure AD**: Implement conditional access policies
- **Network Security**: Use NSGs, Azure Firewall
- **Data Protection**: Enable encryption, use Key Vault
- **Monitoring**: Use Azure Security Center, Sentinel

### GCP Security Best Practices
- **IAM**: Use custom roles, enable MFA
- **VPC**: Use firewall rules, enable flow logs
- **Encryption**: Enable customer-managed encryption keys
- **Monitoring**: Use Security Command Center

---

## 8. Security Tools

### Static Analysis
- **SonarQube**: Code quality and security analysis
- **Snyk**: Dependency vulnerability scanning
- **Bandit**: Python security linter
- **ESLint**: JavaScript security rules

### Dynamic Analysis
- **OWASP ZAP**: Web application security testing
- **Burp Suite**: Web application security testing
- **Nmap**: Network security scanning
- **Metasploit**: Penetration testing framework

### Monitoring Tools
- **ELK Stack**: Log aggregation and analysis
- **Splunk**: Security information and event management
- **Wireshark**: Network protocol analyzer
- **Snort**: Intrusion detection system

---

## 9. Security Training

### Developer Security
- **Secure Coding**: Input validation, output encoding
- **Authentication**: Secure session management
- **Authorization**: Access control implementation
- **Data Protection**: Encryption and key management

### Operations Security
- **System Hardening**: Remove unnecessary services
- **Patch Management**: Regular security updates
- **Network Security**: Firewall configuration
- **Incident Response**: Security event handling

### Compliance Training
- **HIPAA Requirements**: PHI protection guidelines
- **Data Privacy**: GDPR, CCPA compliance
- **Security Policies**: Company security procedures
- **Reporting Procedures**: Security incident reporting

---

# Quick Reference & Cheat Sheets

## Comprehensive Cheat Sheet

## 1) Load Balancing

### What to choose & why

| Strategy           | How it works                         | Pros                            | Cons                          | When to use                      |
| ------------------ | ------------------------------------ | ------------------------------- | ----------------------------- | -------------------------------- |
| Round Robin        | Rotate across backends               | Simple                          | Ignores load differences      | Homogeneous stateless apps       |
| Weighted RR        | Like RR but with weights             | Skews toward stronger nodes     | Manual tuning                 | Mixed instance sizes             |
| Least Connections  | Pick server with fewest active conns | Adapts to variable request time | Needs connection tracking     | Long-lived/variable requests     |
| IP Hash            | Hash(client IP) → server             | Sticky by client                | Poorly balances NAT’d clients | Session affinity without cookies |
| Header/Cookie Hash | Hash on header/cookie                | Fine-grained stickiness         | Requires header/cookie        | Stateful session shards          |
| Consistent Hash    | Hash(key) on ring                    | Minimal reshuffle on scale      | Requires key choice           | Caches, sharded stores           |
| Anycast + LB       | Route to nearest POP                 | Low latency                     | Network expertise             | Global edges (CDN/API edge)      |

### Health checks & routing

- **Liveness** (process up) vs **readiness** (can serve traffic).
- Graceful drain on deploys; slow-start newly added instances.

---

## 2) Caching Tiers (quick recap + design tips)

- **Where:** client → CDN → edge/API gateway → app → Redis/memcached → DB.
- **Patterns:** cache-aside (lazy), read-through, write-through, write-back.
- **Invalidation:** TTLs, versioned keys (`user:123:v42`), pub/sub invalidations.
- **Avoid stampedes:** single-flight locks, randomized TTLs, early refresh.

---

## 3) Consistent Hashing (for caches/shards)

**Idea:** Place servers on a hash ring; `node = first_server_clockwise(hash(key))`.
**Why:** Adding/removing a server only remaps a small slice of keys.
**Tips:** Use **virtual nodes** (many tokens per server) for smoother balance.

**Pseudocode**

```
# ring: sorted list of (token, server)
# tokens: hash(server_id + vnode_index)

function lookup(key):
    # hash key onto ring
    h = hash(key)
    # find first token >= h (wrap if needed)
    s = ring.lower_bound(h) or ring[0]
    return s.server
```

---

## 4) Queues & Pub/Sub

### Concepts

- **Queue (point-to-point):** workers pull; each message to one consumer.
- **Pub/Sub (fan-out):** topics; multiple subscribers receive messages.
- **Ordering:** per-partition FIFO (Kafka); SQS FIFO queues.
- **Consumer groups:** scale horizontally; each partition to one consumer in the group.
- **Backpressure:** control concurrency; rate limit producers; DLQ for poison pills.

### Delivery semantics

| Semantics      | What it means                | Typical systems             | Design requirement       |
| -------------- | ---------------------------- | --------------------------- | ------------------------ |
| At-most-once   | May drop messages, no dupes  | UDP-like, rare for business | Accept loss              |
| At-least-once  | No loss, possible duplicates | SQS std, Kafka              | **Idempotent** consumers |
| Exactly-once\* | No loss, no duplicates       | Kafka EOS (within scopes)   | Careful txn boundaries   |

\*Exactly-once is contextual; end-to-end often reduces to **at-least-once + idempotency**.

**Idempotency pattern**

- Deterministic **idempotency key** (e.g., order_id).
- Store processed keys; ignore repeats.

**Retry/backoff (pseudocode)**

```
retries = 0
delay = base
while retries < max_retries:
    ok = call()
    if ok: return OK
    sleep(delay)
    delay = min(delay * 2, max_delay)  # exponential backoff + cap
    retries += 1
return FAIL
```

---

## 5) Eventual Consistency

- **Definition:** replicas converge if no new writes occur.
- **Read models:** read-repair on access; async background anti-entropy.
- **Client strategies:** **read-your-writes**, **monotonic reads**, **session consistency** where supported.
- **Write conflicts:** timestamps + last-write-wins, vector clocks, or CRDTs.

---

## 6) SLI / SLO / SLA

- **SLI** (indicator): measured metric (e.g., request success rate, p95 latency).
- **SLO** (objective): target for SLI (e.g., **99.9%** success over 30 days).
- **SLA** (agreement): external contract; includes penalties/credits.

**Error budget**

- Budget = 1 − SLO. Example: 99.9% monthly → \~43.2 minutes budget.
- Spend budget on launches; pause risky changes when burning too fast.

**Burn-rate alerts (example)**

- Fast burn: 2% of budget in 1 hour → page now.
- Slow burn: 5% of budget in 6 hours → ticket & investigate.

**Useful SLIs**

- Availability: `2xx+3xx / total`.
- Latency: % of requests under threshold (p90/p95/p99).
- Quality: error rate of critical transactions.
- Saturation: CPU, memory, queue depth.

---

## 7) Reliability Guards

**Circuit breaker (pseudocode)**

```
state = CLOSED
failures = 0
last_open = -inf

function call():
    if state == OPEN and now < last_open + cool_down:
        return FAIL_FAST
    if state == HALF_OPEN:
        allow_only_small_probe_rate()

    ok = downstream()
    if ok:
        if state == HALF_OPEN: state = CLOSED; failures = 0
        else: failures = 0
        return OK
    else:
        failures += 1
        if failures >= threshold:
            state = OPEN
            last_open = now
        return FAIL
```

**Bulkheads:** isolate pools; one noisy neighbor can’t drain all threads/connections.
**Timeouts:** every remote call needs a timeout + retry policy.
**Dead-letter queues:** capture poisoned messages.

---

# Final Cheat Sheet — 1 Page

## A) Cross-Structure Operations (Python)

| Operation       | list                                 | dict                                | set                          | deque                           | heapq                       |               |
| --------------- | ------------------------------------ | ----------------------------------- | ---------------------------- | ------------------------------- | --------------------------- | ------------- |
| `len(x)`        | ✓                                    | ✓                                   | ✓                            | ✓                               | ✓ (len of list)             |               |
| Membership `in` | O(n)                                 | O(1) avg                            | O(1) avg                     | O(n)                            | —                           |               |
| Add             | `.append(x)` / `.insert(i,x)`        | `d[k]=v`                            | `.add(x)`                    | `.append(x)` / `.appendleft(x)` | `heappush(h,x)`             |               |
| Remove          | `.remove(x)` / `.pop()` / `del a[i]` | `del d[k]` / `.pop(k)`              | `.remove(x)` / `.discard(x)` | `.popleft()` / `.pop()`         | `heappop(h)`                |               |
| Iterate         | `for v in a`                         | `for k,v in d.items()`              | `for v in s`                 | `for v in q`                    | `for v in h` (unsorted)     |               |
| Sort            | `.sort()` / `sorted(a)`              | `sorted(d.items())`                 | `sorted(s)`                  | convert → list                  | heaps are partially ordered |               |
| Special         | slicing, `.reverse()`                | `.keys() .values() .items() .get()` | set ops \`                   | & - ^\`                         | O(1) ends                   | min at `h[0]` |

## B) Big-O Quick Table

| Structure      | Access   | Search   | Insert   | Delete   |
| -------------- | -------- | -------- | -------- | -------- |
| Array/list     | O(1)     | O(n)     | O(n)     | O(n)     |
| Dict           | —        | O(1) avg | O(1) avg | O(1) avg |
| Set            | —        | O(1) avg | O(1) avg | O(1) avg |
| Heap           | —        | O(n)     | O(log n) | O(log n) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) |

## C) Algorithm Skeletons (minimal)

**Recursion template**

```python
def solve(x):
    # base case(s)
    # combine results from smaller subproblems
    return result
```

**DFS (graph)**

```python
def dfs(u):
    if u in seen: return
    seen.add(u)
    for v in G[u]:
        dfs(v)
```

**BFS (graph)**

```python
from collections import deque
def bfs(s):
    q, seen = deque([s]), {s}
    while q:
        u = q.popleft()
        for v in G[u]:
            if v not in seen:
                seen.add(v); q.append(v)
```

**Binary search (index or insert position)**

```python
def bsearch(a, t):
    l, r = 0, len(a)-1
    while l <= r:
        m = (l+r)//2
        if a[m]==t: return m
        if a[m]<t: l = m+1
        else: r = m-1
    return l  # insert position
```

**Sliding window (no repeats)**

```python
def longest(s):
    pos, L, best = {}, 0, 0
    for R,ch in enumerate(s):
        if ch in pos and pos[ch] >= L: L = pos[ch]+1
        pos[ch] = R
        best = max(best, R-L+1)
    return best
```

**Dijkstra (min distances)**

```python
import heapq
def dijkstra(G, s):
    dist = {s:0}; pq = [(0,s)]
    while pq:
        d,u = heapq.heappop(pq)
        if d != dist.get(u, float('inf')): continue
        for v,w in G[u]:
            nd = d + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd; heapq.heappush(pq, (nd,v))
    return dist
```

**DP template**

```python
# define state dp[...] and base cases
# fill in dependency order using transitions
return answer_state
```

## D) Python Interview Reminders

- **Strings are immutable**; use `''.join(parts)` for concatenation in loops.
- **List slicing makes a copy**: `a[i:j]` is O(k).
- Use **`deque`** for O(1) queue ops; avoid `pop(0)` on lists.
- `heapq` is a **min-heap**; for max-heap push negatives.
- Sorting is **Timsort** (stable, O(n log n)).
- Don’t use **mutable defaults** in function params; use `None` then set.

---
