# 📊 Heap Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for: 📊 Heap Pattern

**Back:** Key indicators:
• "Find k
• th largest/smallest element"
• "Merge k sorted lists"
• "Top k frequent elements"
• "Median of data stream"
• "Sliding window median"


## Card 2

**Front:** Give examples of 📊 Heap Pattern problems

**Back:** Common examples:



## Card 3

**Front:** Implement find_kth_largest using 📊 Heap Pattern

**Back:** ```python
# Find K-th Largest Element
def find_kth_largest(nums, k):
    import heapq
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    
    return heap[0]
```


## Card 4

**Front:** What is the time/space complexity of 📊 Heap Pattern?

**Back:** Varies by implementation

