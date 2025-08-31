---
title: Searching Algorithms
---

# Searching Algorithms

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

- O(log n). Requires sorted data.

**Pseudocode**

```
binary_search(arr, target):
    left = 0
    right = len(arr)-1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: left = mid + 1
        else: right = mid - 1
    return -1
```

**Python**

```python
def binary_search(arr, target):
    left, right = 0, len(arr)-1
    while left <= right:
        mid = (left + right)//2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
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
