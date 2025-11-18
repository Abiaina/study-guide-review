# Fast & Slow Pointers Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for: Fast & Slow Pointers Pattern

**Back:** Key indicators:
• Linked list problems
• Find middle of linked list
• Detect cycle in linked list
• Find k-th node from end
• Two pointers moving at different speeds (1 step vs 2 steps)


## Card 2

**Front:** Give examples of Fast & Slow Pointers Pattern problems

**Back:** Common examples:
• Find middle of linked list
• Detect cycle in linked list
• Remove nth node from end
• Palindrome linked list
• Find cycle start node


## Card 3

**Front:** Implement find_middle and has_cycle using Fast & Slow Pointers Pattern

**Back:** ```python
# Find middle of linked list
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next          # Move 1 step
        fast = fast.next.next     # Move 2 steps
    return slow

# Detect cycle in linked list
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:          # Cycle detected
            return True
    return False
```


## Card 4

**Front:** What is the time/space complexity of Fast & Slow Pointers Pattern?

**Back:** O(n) time, O(1) space - single pass through linked list

