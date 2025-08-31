# Algorithm Flashcards - Anki Format

Generated for interview preparation


# Algorithm Flashcards - 🔍 Two Pointers Pattern

## Card 1: Identify the algorithm pattern for: 🔍 Two Pointers...

**Front:**
Identify the algorithm pattern for: 🔍 Two Pointers Pattern

**Back:**
Key indicators:
• "Find two numbers that sum to target"
• "Remove duplicates from sorted array"
• "Check if string is palindrome"
• "Merge two sorted arrays"
• "Container with most water"

---


# Algorithm Flashcards - 🔍 Two Pointers Pattern

## Card 2: Give examples of 🔍 Two Pointers Pattern problems...

**Front:**
Give examples of 🔍 Two Pointers Pattern problems

**Back:**
Common examples:


---


# Algorithm Flashcards - 🔍 Two Pointers Pattern

## Card 3: Implement two_sum_sorted using 🔍 Two Pointers Patt...

**Front:**
Implement two_sum_sorted using 🔍 Two Pointers Pattern

**Back:**
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

---


# Algorithm Flashcards - 🔍 Two Pointers Pattern

## Card 4: What is the time/space complexity of 🔍 Two Pointer...

**Front:**
What is the time/space complexity of 🔍 Two Pointers Pattern?

**Back:**
Varies by implementation

---


# Algorithm Flashcards - 🪟 Sliding Window Pattern

## Card 5: Identify the algorithm pattern for: 🪟 Sliding Wind...

**Front:**
Identify the algorithm pattern for: 🪟 Sliding Window Pattern

**Back:**
Key indicators:
• "Find longest substring without repeating characters"
• "Maximum sum subarray of size k"
• "Minimum window substring"
• "Longest substring with at most k distinct characters"
• "Find all anagrams in a string"

---


# Algorithm Flashcards - 🪟 Sliding Window Pattern

## Card 6: Give examples of 🪟 Sliding Window Pattern problems...

**Front:**
Give examples of 🪟 Sliding Window Pattern problems

**Back:**
Common examples:


---


# Algorithm Flashcards - 🪟 Sliding Window Pattern

## Card 7: Implement length_of_longest_substring using 🪟 Slid...

**Front:**
Implement length_of_longest_substring using 🪟 Sliding Window Pattern

**Back:**
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

---


# Algorithm Flashcards - 🪟 Sliding Window Pattern

## Card 8: What is the time/space complexity of 🪟 Sliding Win...

**Front:**
What is the time/space complexity of 🪟 Sliding Window Pattern?

**Back:**
Varies by implementation

---


# Algorithm Flashcards - 🔢 Binary Search Pattern

## Card 9: Identify the algorithm pattern for: 🔢 Binary Searc...

**Front:**
Identify the algorithm pattern for: 🔢 Binary Search Pattern

**Back:**
Key indicators:
• "Find element in sorted array"
• "Find first/last occurrence"
• "Find minimum/maximum capacity"
• "Search in rotated sorted array"
• "Find peak element"

---


# Algorithm Flashcards - 🔢 Binary Search Pattern

## Card 10: Give examples of 🔢 Binary Search Pattern problems...

**Front:**
Give examples of 🔢 Binary Search Pattern problems

**Back:**
Common examples:


---


# Algorithm Flashcards - 🔢 Binary Search Pattern

## Card 11: Implement ship_within_days using 🔢 Binary Search P...

**Front:**
Implement ship_within_days using 🔢 Binary Search Pattern

**Back:**
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


# Algorithm Flashcards - 🔢 Binary Search Pattern

## Card 12: What is the time/space complexity of 🔢 Binary Sear...

**Front:**
What is the time/space complexity of 🔢 Binary Search Pattern?

**Back:**
Varies by implementation

---


# Algorithm Flashcards - 🌳 Tree Traversal Pattern

## Card 13: Identify the algorithm pattern for: 🌳 Tree Travers...

**Front:**
Identify the algorithm pattern for: 🌳 Tree Traversal Pattern

**Back:**
Key indicators:
• "Inorder/preorder/postorder traversal"
• "Level order traversal"
• "Validate binary search tree"
• "Serialize/deserialize tree"
• "Find lowest common ancestor"

---


# Algorithm Flashcards - 🌳 Tree Traversal Pattern

## Card 14: Give examples of 🌳 Tree Traversal Pattern problems...

**Front:**
Give examples of 🌳 Tree Traversal Pattern problems

**Back:**
Common examples:


---


# Algorithm Flashcards - 🌳 Tree Traversal Pattern

## Card 15: Implement is_valid_bst using 🌳 Tree Traversal Patt...

**Front:**
Implement is_valid_bst using 🌳 Tree Traversal Pattern

**Back:**
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

---


# Algorithm Flashcards - 🌳 Tree Traversal Pattern

## Card 16: What is the time/space complexity of 🌳 Tree Traver...

**Front:**
What is the time/space complexity of 🌳 Tree Traversal Pattern?

**Back:**
Varies by implementation

---


# Algorithm Flashcards - 🕸️ Graph Traversal Pattern

## Card 17: Identify the algorithm pattern for: 🕸️ Graph Trave...

**Front:**
Identify the algorithm pattern for: 🕸️ Graph Traversal Pattern

**Back:**
Key indicators:
• "Find shortest path"
• "Detect cycle in graph"
• "Topological sort"
• "Number of islands"
• "Clone graph"

---


# Algorithm Flashcards - 🕸️ Graph Traversal Pattern

## Card 18: Give examples of 🕸️ Graph Traversal Pattern proble...

**Front:**
Give examples of 🕸️ Graph Traversal Pattern problems

**Back:**
Common examples:


---


# Algorithm Flashcards - 🕸️ Graph Traversal Pattern

## Card 19: Implement has_cycle using 🕸️ Graph Traversal Patte...

**Front:**
Implement has_cycle using 🕸️ Graph Traversal Pattern

**Back:**
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


# Algorithm Flashcards - 🕸️ Graph Traversal Pattern

## Card 20: What is the time/space complexity of 🕸️ Graph Trav...

**Front:**
What is the time/space complexity of 🕸️ Graph Traversal Pattern?

**Back:**
Varies by implementation

---


# Algorithm Flashcards - 💰 Classic DP Pattern

## Card 21: Identify the algorithm pattern for: 💰 Classic DP P...

**Front:**
Identify the algorithm pattern for: 💰 Classic DP Pattern

**Back:**
Key indicators:
• "Maximum/minimum value"
• "Count ways to do something"
• "Longest increasing subsequence"
• "Coin change"
• "Climbing stairs"

---


# Algorithm Flashcards - 💰 Classic DP Pattern

## Card 22: Give examples of 💰 Classic DP Pattern problems...

**Front:**
Give examples of 💰 Classic DP Pattern problems

**Back:**
Common examples:


---


# Algorithm Flashcards - 💰 Classic DP Pattern

## Card 23: Implement coin_change using 💰 Classic DP Pattern...

**Front:**
Implement coin_change using 💰 Classic DP Pattern

**Back:**
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

---


# Algorithm Flashcards - 💰 Classic DP Pattern

## Card 24: What is the time/space complexity of 💰 Classic DP ...

**Front:**
What is the time/space complexity of 💰 Classic DP Pattern?

**Back:**
Varies by implementation

---


# Algorithm Flashcards - 🎒 Knapsack Pattern

## Card 25: Identify the algorithm pattern for: 🎒 Knapsack Pat...

**Front:**
Identify the algorithm pattern for: 🎒 Knapsack Pattern

**Back:**
Key indicators:
• "Select items with weight/value constraints"
• "Partition equal subset sum"
• "Target sum"
• "0/1 knapsack"
• "Unbounded knapsack"

---


# Algorithm Flashcards - 🎒 Knapsack Pattern

## Card 26: Give examples of 🎒 Knapsack Pattern problems...

**Front:**
Give examples of 🎒 Knapsack Pattern problems

**Back:**
Common examples:


---


# Algorithm Flashcards - 🎒 Knapsack Pattern

## Card 27: Implement can_partition using 🎒 Knapsack Pattern...

**Front:**
Implement can_partition using 🎒 Knapsack Pattern

**Back:**
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


# Algorithm Flashcards - 🎒 Knapsack Pattern

## Card 28: What is the time/space complexity of 🎒 Knapsack Pa...

**Front:**
What is the time/space complexity of 🎒 Knapsack Pattern?

**Back:**
Varies by implementation

---


# Algorithm Flashcards - 📊 Heap Pattern

## Card 29: Identify the algorithm pattern for: 📊 Heap Pattern...

**Front:**
Identify the algorithm pattern for: 📊 Heap Pattern

**Back:**
Key indicators:
• "Find k
• th largest/smallest element"
• "Merge k sorted lists"
• "Top k frequent elements"
• "Median of data stream"
• "Sliding window median"

---


# Algorithm Flashcards - 📊 Heap Pattern

## Card 30: Give examples of 📊 Heap Pattern problems...

**Front:**
Give examples of 📊 Heap Pattern problems

**Back:**
Common examples:


---


# Algorithm Flashcards - 📊 Heap Pattern

## Card 31: Implement find_kth_largest using 📊 Heap Pattern...

**Front:**
Implement find_kth_largest using 📊 Heap Pattern

**Back:**
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


# Algorithm Flashcards - 📊 Heap Pattern

## Card 32: What is the time/space complexity of 📊 Heap Patter...

**Front:**
What is the time/space complexity of 📊 Heap Pattern?

**Back:**
Varies by implementation

---


# Algorithm Flashcards - 🔄 Backtracking Pattern

## Card 33: Identify the algorithm pattern for: 🔄 Backtracking...

**Front:**
Identify the algorithm pattern for: 🔄 Backtracking Pattern

**Back:**
Key indicators:
• "Generate all combinations"
• "Find all permutations"
• "N
• queens problem"
• "Sudoku solver"
• "Word search"

---


# Algorithm Flashcards - 🔄 Backtracking Pattern

## Card 34: Give examples of 🔄 Backtracking Pattern problems...

**Front:**
Give examples of 🔄 Backtracking Pattern problems

**Back:**
Common examples:


---


# Algorithm Flashcards - 🔄 Backtracking Pattern

## Card 35: Implement permute using 🔄 Backtracking Pattern...

**Front:**
Implement permute using 🔄 Backtracking Pattern

**Back:**
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


# Algorithm Flashcards - 🔄 Backtracking Pattern

## Card 36: What is the time/space complexity of 🔄 Backtrackin...

**Front:**
What is the time/space complexity of 🔄 Backtracking Pattern?

**Back:**
Varies by implementation

---


# Algorithm Flashcards - 🎯 Problem Type → Algorithm Pattern

## Card 37: What is the time/space complexity of 🎯 Problem Typ...

**Front:**
What is the time/space complexity of 🎯 Problem Type → Algorithm Pattern?

**Back:**
Varies by implementation

---


# Algorithm Flashcards - Back Side (Solution Pattern)

## Card 38: What is the time/space complexity of Back Side (So...

**Front:**
What is the time/space complexity of Back Side (Solution Pattern)?

**Back:**
Varies by implementation

---


# Algorithm Flashcards - ⚡ Common Interview Patterns

## Card 39: What is the time/space complexity of ⚡ Common Inte...

**Front:**
What is the time/space complexity of ⚡ Common Interview Patterns?

**Back:**
Varies by implementation

---

