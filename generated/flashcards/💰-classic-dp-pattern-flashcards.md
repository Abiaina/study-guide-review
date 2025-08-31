# 💰 Classic DP Pattern Flashcards

Generated for interview preparation


## Card 1

**Front:** Identify the algorithm pattern for: 💰 Classic DP Pattern

**Back:** Key indicators:
• "Maximum/minimum value"
• "Count ways to do something"
• "Longest increasing subsequence"
• "Coin change"
• "Climbing stairs"


## Card 2

**Front:** Give examples of 💰 Classic DP Pattern problems

**Back:** Common examples:



## Card 3

**Front:** Implement coin_change using 💰 Classic DP Pattern

**Back:** ```python
# Coin Change - Minimum coins needed
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```


## Card 4

**Front:** What is the time/space complexity of 💰 Classic DP Pattern?

**Back:** Varies by implementation

