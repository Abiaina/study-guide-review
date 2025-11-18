# Greedy Threshold Tracking Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for: Greedy Threshold Tracking Pattern

**Back:** Key indicators:
• "Increasing triplet subsequence"
• Track multiple thresholds or candidates
• Need to find sequence with specific ordering
• "Longest increasing subsequence" variants
• Maintain multiple potential candidates
• Greedy selection with threshold tracking


## Card 2

**Front:** Give examples of Greedy Threshold Tracking Pattern problems

**Back:** Common examples:
• Increasing Triplet Subsequence
• Longest Increasing Subsequence (O(n log n) variant)
• Russian Doll Envelopes
• Maximum Length of Pair Chain
• Wiggle Subsequence


## Card 3

**Front:** Implement increasing_triplet using Greedy Threshold Tracking Pattern

**Back:** ```python
# Increasing Triplet Subsequence
def increasing_triplet(nums):
    first = second = float('inf')
    
    for num in nums:
        if num <= first:
            first = num          # Update smallest
        elif num <= second:
            second = num          # Update second smallest
        else:
            return True           # Found third > second
    
    return False
```


## Card 4

**Front:** What is the time/space complexity of Greedy Threshold Tracking Pattern?

**Back:** O(n) time, O(1) or O(k) space where k is number of thresholds tracked

