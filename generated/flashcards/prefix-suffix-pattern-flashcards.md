# Prefix / Suffix Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for: Prefix / Suffix Pattern

**Back:** Key indicators:
• Range queries on arrays
• Subarray sum problems
• Need cumulative information
• "Subarray sum equals k"
• "Product of array except self"
• "Running sum" or "cumulative sum"


## Card 2

**Front:** Give examples of Prefix / Suffix Pattern problems

**Back:** Common examples:
• Subarray Sum Equals K (prefix sum + hash map)
• Product of Array Except Self (prefix + suffix)
• Maximum Subarray (Kadane's algorithm)
• Range Sum Query (prefix sum array)
• Contiguous Array (prefix sum for balance)


## Card 3

**Front:** Implement subarray_sum_equals_k using Prefix / Suffix Pattern

**Back:** ```python
# Subarray Sum Equals K using prefix sum
def subarray_sum_equals_k(nums, k):
    prefix_sum = {0: 1}  # sum: count
    current_sum = 0
    count = 0
    
    for num in nums:
        current_sum += num
        
        # If current_sum - k exists, we found a subarray
        if current_sum - k in prefix_sum:
            count += prefix_sum[current_sum - k]
        
        # Update prefix_sum count
        prefix_sum[current_sum] = prefix_sum.get(current_sum, 0) + 1
    
    return count
```


## Card 4

**Front:** What is the time/space complexity of Prefix / Suffix Pattern?

**Back:** O(n) time, O(n) space for prefix sum array/hash map

