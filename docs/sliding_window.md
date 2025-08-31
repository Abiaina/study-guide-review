---
title: Sliding Window Algorithms
---

# Sliding Window Algorithms

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
