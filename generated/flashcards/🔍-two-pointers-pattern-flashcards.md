# 🔍 Two Pointers Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for: 🔍 Two Pointers Pattern

**Back:** Key indicators:
• "Find two numbers that sum to target"
• "Remove duplicates from sorted array"
• "Check if string is palindrome"
• "Merge two sorted arrays"
• "Container with most water"


## Card 2

**Front:** Give examples of 🔍 Two Pointers Pattern problems

**Back:** Common examples:



## Card 3

**Front:** Implement two_sum_sorted using 🔍 Two Pointers Pattern

**Back:** ```python
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


## Card 4

**Front:** What is the time/space complexity of 🔍 Two Pointers Pattern?

**Back:** Varies by implementation

