# Monotonic Stack Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for: Monotonic Stack Pattern

**Back:** Key indicators:
• "Next greater element"
• "Next smaller element"
• "Largest rectangle in histogram"
• "Daily temperatures"
• Need to find next/previous element with certain property
• Stack maintains monotonic order (increasing or decreasing)


## Card 2

**Front:** Give examples of Monotonic Stack Pattern problems

**Back:** Common examples:
• Next Greater Element
• Daily Temperatures
• Largest Rectangle in Histogram
• Trapping Rain Water
• Remove K Digits
• Next Greater Element II (circular array)


## Card 3

**Front:** Implement next_greater_element using Monotonic Stack Pattern

**Back:** ```python
# Next Greater Element
def next_greater_element(nums):
    result = [-1] * len(nums)
    stack = []  # Store indices
    
    for i in range(len(nums)):
        # While stack not empty and current > stack top
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result
```


## Card 4

**Front:** What is the time/space complexity of Monotonic Stack Pattern?

**Back:** O(n) time, O(n) space - each element pushed/popped at most once

