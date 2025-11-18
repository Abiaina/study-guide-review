# Hash Map / Frequency Tracking Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for: Hash Map / Frequency Tracking Pattern

**Back:** Key indicators:
• Need fast lookup or counting
• Problems involve checking existence
• Counting frequency
• Prefix sums with a map
• Grouping items


## Card 2

**Front:** Give examples of Hash Map / Frequency Tracking Pattern problems

**Back:** Common examples:
• Two Sum
• Subarray Sum Equals K (prefix sum + map)
• Group Anagrams
• Longest Substring Without Repeating Characters (map for last seen index)


## Card 3

**Front:** Implement frequency tracking using Hash Map / Frequency Tracking Pattern

**Back:** ```python
freq = {}
for x in nums:
    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1

# Example: check duplicates
if freq[x] > 1:
    # do something
```


## Card 4

**Front:** What is the time/space complexity of Hash Map / Frequency Tracking Pattern?

**Back:** O(n) time, O(n) space for frequency counting; O(1) average lookup time

