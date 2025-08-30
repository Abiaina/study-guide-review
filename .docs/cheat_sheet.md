---
title: Cheat Sheet
---

# System Design Appendix

## 1) Load Balancing

### What to choose & why

| Strategy           | How it works                         | Pros                            | Cons                          | When to use                      |
| ------------------ | ------------------------------------ | ------------------------------- | ----------------------------- | -------------------------------- |
| Round Robin        | Rotate across backends               | Simple                          | Ignores load differences      | Homogeneous stateless apps       |
| Weighted RR        | Like RR but with weights             | Skews toward stronger nodes     | Manual tuning                 | Mixed instance sizes             |
| Least Connections  | Pick server with fewest active conns | Adapts to variable request time | Needs connection tracking     | Long-lived/variable requests     |
| IP Hash            | Hash(client IP) → server             | Sticky by client                | Poorly balances NAT’d clients | Session affinity without cookies |
| Header/Cookie Hash | Hash on header/cookie                | Fine-grained stickiness         | Requires header/cookie        | Stateful session shards          |
| Consistent Hash    | Hash(key) on ring                    | Minimal reshuffle on scale      | Requires key choice           | Caches, sharded stores           |
| Anycast + LB       | Route to nearest POP                 | Low latency                     | Network expertise             | Global edges (CDN/API edge)      |

### Health checks & routing

- **Liveness** (process up) vs **readiness** (can serve traffic).
- Graceful drain on deploys; slow-start newly added instances.

---

## 2) Caching Tiers (quick recap + design tips)

- **Where:** client → CDN → edge/API gateway → app → Redis/memcached → DB.
- **Patterns:** cache-aside (lazy), read-through, write-through, write-back.
- **Invalidation:** TTLs, versioned keys (`user:123:v42`), pub/sub invalidations.
- **Avoid stampedes:** single-flight locks, randomized TTLs, early refresh.

---

## 3) Consistent Hashing (for caches/shards)

**Idea:** Place servers on a hash ring; `node = first_server_clockwise(hash(key))`.
**Why:** Adding/removing a server only remaps a small slice of keys.
**Tips:** Use **virtual nodes** (many tokens per server) for smoother balance.

**Pseudocode**

```
# ring: sorted list of (token, server)
# tokens: hash(server_id + vnode_index)

function lookup(key):
    # hash key onto ring
    h = hash(key)
    # find first token >= h (wrap if needed)
    s = ring.lower_bound(h) or ring[0]
    return s.server
```

---

## 4) Queues & Pub/Sub

### Concepts

- **Queue (point-to-point):** workers pull; each message to one consumer.
- **Pub/Sub (fan-out):** topics; multiple subscribers receive messages.
- **Ordering:** per-partition FIFO (Kafka); SQS FIFO queues.
- **Consumer groups:** scale horizontally; each partition to one consumer in the group.
- **Backpressure:** control concurrency; rate limit producers; DLQ for poison pills.

### Delivery semantics

| Semantics      | What it means                | Typical systems             | Design requirement       |
| -------------- | ---------------------------- | --------------------------- | ------------------------ |
| At-most-once   | May drop messages, no dupes  | UDP-like, rare for business | Accept loss              |
| At-least-once  | No loss, possible duplicates | SQS std, Kafka              | **Idempotent** consumers |
| Exactly-once\* | No loss, no duplicates       | Kafka EOS (within scopes)   | Careful txn boundaries   |

\*Exactly-once is contextual; end-to-end often reduces to **at-least-once + idempotency**.

**Idempotency pattern**

- Deterministic **idempotency key** (e.g., order_id).
- Store processed keys; ignore repeats.

**Retry/backoff (pseudocode)**

```
retries = 0
delay = base
while retries < max_retries:
    ok = call()
    if ok: return OK
    sleep(delay)
    delay = min(delay * 2, max_delay)  # exponential backoff + cap
    retries += 1
return FAIL
```

---

## 5) Eventual Consistency

- **Definition:** replicas converge if no new writes occur.
- **Read models:** read-repair on access; async background anti-entropy.
- **Client strategies:** **read-your-writes**, **monotonic reads**, **session consistency** where supported.
- **Write conflicts:** timestamps + last-write-wins, vector clocks, or CRDTs.

---

## 6) SLI / SLO / SLA

- **SLI** (indicator): measured metric (e.g., request success rate, p95 latency).
- **SLO** (objective): target for SLI (e.g., **99.9%** success over 30 days).
- **SLA** (agreement): external contract; includes penalties/credits.

**Error budget**

- Budget = 1 − SLO. Example: 99.9% monthly → \~43.2 minutes budget.
- Spend budget on launches; pause risky changes when burning too fast.

**Burn-rate alerts (example)**

- Fast burn: 2% of budget in 1 hour → page now.
- Slow burn: 5% of budget in 6 hours → ticket & investigate.

**Useful SLIs**

- Availability: `2xx+3xx / total`.
- Latency: % of requests under threshold (p90/p95/p99).
- Quality: error rate of critical transactions.
- Saturation: CPU, memory, queue depth.

---

## 7) Reliability Guards

**Circuit breaker (pseudocode)**

```
state = CLOSED
failures = 0
last_open = -inf

function call():
    if state == OPEN and now < last_open + cool_down:
        return FAIL_FAST
    if state == HALF_OPEN:
        allow_only_small_probe_rate()

    ok = downstream()
    if ok:
        if state == HALF_OPEN: state = CLOSED; failures = 0
        else: failures = 0
        return OK
    else:
        failures += 1
        if failures >= threshold:
            state = OPEN
            last_open = now
        return FAIL
```

**Bulkheads:** isolate pools; one noisy neighbor can’t drain all threads/connections.
**Timeouts:** every remote call needs a timeout + retry policy.
**Dead-letter queues:** capture poisoned messages.

---

# Final Cheat Sheet — 1 Page

## A) Cross-Structure Operations (Python)

| Operation       | list                                 | dict                                | set                          | deque                           | heapq                       |               |
| --------------- | ------------------------------------ | ----------------------------------- | ---------------------------- | ------------------------------- | --------------------------- | ------------- |
| `len(x)`        | ✓                                    | ✓                                   | ✓                            | ✓                               | ✓ (len of list)             |               |
| Membership `in` | O(n)                                 | O(1) avg                            | O(1) avg                     | O(n)                            | —                           |               |
| Add             | `.append(x)` / `.insert(i,x)`        | `d[k]=v`                            | `.add(x)`                    | `.append(x)` / `.appendleft(x)` | `heappush(h,x)`             |               |
| Remove          | `.remove(x)` / `.pop()` / `del a[i]` | `del d[k]` / `.pop(k)`              | `.remove(x)` / `.discard(x)` | `.popleft()` / `.pop()`         | `heappop(h)`                |               |
| Iterate         | `for v in a`                         | `for k,v in d.items()`              | `for v in s`                 | `for v in q`                    | `for v in h` (unsorted)     |               |
| Sort            | `.sort()` / `sorted(a)`              | `sorted(d.items())`                 | `sorted(s)`                  | convert → list                  | heaps are partially ordered |               |
| Special         | slicing, `.reverse()`                | `.keys() .values() .items() .get()` | set ops \`                   | & - ^\`                         | O(1) ends                   | min at `h[0]` |

## B) Big-O Quick Table

| Structure      | Access   | Search   | Insert   | Delete   |
| -------------- | -------- | -------- | -------- | -------- |
| Array/list     | O(1)     | O(n)     | O(n)     | O(n)     |
| Dict           | —        | O(1) avg | O(1) avg | O(1) avg |
| Set            | —        | O(1) avg | O(1) avg | O(1) avg |
| Heap           | —        | O(n)     | O(log n) | O(log n) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) |

## C) Algorithm Skeletons (minimal)

**Recursion template**

```python
def solve(x):
    # base case(s)
    # combine results from smaller subproblems
    return result
```

**DFS (graph)**

```python
def dfs(u):
    if u in seen: return
    seen.add(u)
    for v in G[u]:
        dfs(v)
```

**BFS (graph)**

```python
from collections import deque
def bfs(s):
    q, seen = deque([s]), {s}
    while q:
        u = q.popleft()
        for v in G[u]:
            if v not in seen:
                seen.add(v); q.append(v)
```

**Binary search (index or insert position)**

```python
def bsearch(a, t):
    l, r = 0, len(a)-1
    while l <= r:
        m = (l+r)//2
        if a[m]==t: return m
        if a[m]<t: l = m+1
        else: r = m-1
    return l  # insert position
```

**Sliding window (no repeats)**

```python
def longest(s):
    pos, L, best = {}, 0, 0
    for R,ch in enumerate(s):
        if ch in pos and pos[ch] >= L: L = pos[ch]+1
        pos[ch] = R
        best = max(best, R-L+1)
    return best
```

**Dijkstra (min distances)**

```python
import heapq
def dijkstra(G, s):
    dist = {s:0}; pq = [(0,s)]
    while pq:
        d,u = heapq.heappop(pq)
        if d != dist.get(u, float('inf')): continue
        for v,w in G[u]:
            nd = d + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd; heapq.heappush(pq, (nd,v))
    return dist
```

**DP template**

```python
# define state dp[...] and base cases
# fill in dependency order using transitions
return answer_state
```

## D) Python Interview Reminders

- **Strings are immutable**; use `''.join(parts)` for concatenation in loops.
- **List slicing makes a copy**: `a[i:j]` is O(k).
- Use **`deque`** for O(1) queue ops; avoid `pop(0)` on lists.
- `heapq` is a **min-heap**; for max-heap push negatives.
- Sorting is **Timsort** (stable, O(n log n)).
- Don’t use **mutable defaults** in function params; use `None` then set.
