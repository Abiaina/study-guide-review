#  Graph Traversal Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for:  Graph Traversal Pattern

**Back:** Key indicators:
• "Find shortest path"
• "Detect cycle in graph"
• "Topological sort"
• "Number of islands"
• "Clone graph"


## Card 2

**Front:** Give examples of  Graph Traversal Pattern problems

**Back:** Common examples:



## Card 3

**Front:** Implement has_cycle using  Graph Traversal Pattern

**Back:** ```python
# Detect cycle in directed graph
def has_cycle(graph):
    visited = set()
    rec_stack = set()
    
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(node)
        return False
    
    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    return False
```


## Card 4

**Front:** What is the time/space complexity of  Graph Traversal Pattern?

**Back:** Varies by implementation

