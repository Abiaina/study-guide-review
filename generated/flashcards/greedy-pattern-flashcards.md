# Greedy Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for: Greedy Pattern

**Back:** Key indicators:
• Make locally optimal choice at each step
• Problems involving intervals, scheduling, or optimization
• "Maximum non-overlapping intervals"
• "Jump game" problems
• "Minimum coins" or "activity selection"
• Can prove greedy choice leads to global optimum


## Card 2

**Front:** Give examples of Greedy Pattern problems

**Back:** Common examples:
• Interval Scheduling (max non-overlapping intervals)
• Jump Game I & II
• Gas Station
• Meeting Rooms
• Minimum Number of Arrows to Burst Balloons
• Assign Cookies


## Card 3

**Front:** Implement max_non_overlapping_intervals using Greedy Pattern

**Back:** ```python
# Maximum Non-Overlapping Intervals
def max_non_overlapping(intervals):
    # Sort by end time (greedy: pick earliest finishing)
    intervals.sort(key=lambda x: x[1])
    
    count = 0
    last_end = float('-inf')
    
    for start, end in intervals:
        # If doesn't overlap with last taken
        if start >= last_end:
            count += 1
            last_end = end
    
    return count
```


## Card 4

**Front:** What is the time/space complexity of Greedy Pattern?

**Back:** O(n log n) time for sorting, O(1) or O(n) space depending on problem

