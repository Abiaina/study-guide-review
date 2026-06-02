#  Sliding Window Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for:  Sliding Window Pattern

**Back:** Key indicators:
• "Find longest substring without repeating characters"
• "Maximum sum subarray of size k"
• "Minimum window substring"
• "Longest substring with at most k distinct characters"
• "Find all anagrams in a string"


## Card 2

**Front:** Give examples of  Sliding Window Pattern problems

**Back:** Common examples:



## Card 3

**Front:** Implement length_of_longest_substring using  Sliding Window Pattern

**Back:** ```python
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


## Card 4

**Front:** What is the time/space complexity of  Sliding Window Pattern?

**Back:** Varies by implementation

