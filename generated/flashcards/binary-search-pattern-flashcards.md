#  Binary Search Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for:  Binary Search Pattern

**Back:** Key indicators:
• "Find element in sorted array"
• "Find first/last occurrence"
• "Find minimum/maximum capacity"
• "Search in rotated sorted array"
• "Find peak element"


## Card 2

**Front:** Give examples of  Binary Search Pattern problems

**Back:** Common examples:



## Card 3

**Front:** Implement ship_within_days using  Binary Search Pattern

**Back:** ```python
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


## Card 4

**Front:** What is the time/space complexity of  Binary Search Pattern?

**Back:** Varies by implementation

