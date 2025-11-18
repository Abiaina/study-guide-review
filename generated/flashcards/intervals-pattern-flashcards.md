# Intervals Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for: Intervals Pattern

**Back:** Key indicators:
• Working with start/end times or ranges
• Merging overlapping intervals
• Scheduling / maximizing non-overlapping tasks
• Checking conflicts or gaps


## Card 2

**Front:** Give examples of Intervals Pattern problems

**Back:** Common examples:
• Merge Intervals
• Non-overlapping Intervals
• Meeting Rooms I & II
• Employee Free Time


## Card 3

**Front:** Implement merge_intervals using Intervals Pattern

**Back:** ```python
intervals.sort(key=lambda x: x[0])
merged = [intervals[0]]

for start, end in intervals[1:]:
    last_end = merged[-1][1]
    if start <= last_end:  # overlap
        merged[-1][1] = max(last_end, end)
    else:
        merged.append([start, end])
```


## Card 4

**Front:** What is the time/space complexity of Intervals Pattern?

**Back:** O(n log n) time for sorting, O(n) space for result

