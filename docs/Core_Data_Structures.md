---
title: Core Data Structures
---

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
