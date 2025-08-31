#  Knapsack Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for:  Knapsack Pattern

**Back:** Key indicators:
• "Select items with weight/value constraints"
• "Partition equal subset sum"
• "Target sum"
• "0/1 knapsack"
• "Unbounded knapsack"


## Card 2

**Front:** Give examples of  Knapsack Pattern problems

**Back:** Common examples:



## Card 3

**Front:** Implement can_partition using  Knapsack Pattern

**Back:** ```python
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


## Card 4

**Front:** What is the time/space complexity of  Knapsack Pattern?

**Back:** Varies by implementation

