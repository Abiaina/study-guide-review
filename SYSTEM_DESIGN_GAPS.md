# System Design Section - Missing Key Definitions & Concepts

## Critical Missing Definitions

### 1. **Fundamental System Design Metrics** (Partially Missing)

**Current Status:**
- ✅ Latency and Throughput mentioned briefly
- ⚠️ Not deeply explained with examples
- ❌ QPS (Queries Per Second) not defined
- ❌ P95/P99 latency not explained
- ❌ Error rate not defined
- ❌ Availability percentage (99.9%, 99.99%) not explained

**What's Missing:**
```markdown
### System Performance Metrics

**Throughput (QPS/RPS)**
- **Definition**: Number of requests/queries processed per second
- **Example**: 1000 QPS = 1000 requests/second
- **Measurement**: Total requests / time window

**Latency**
- **Definition**: Time taken for a request to complete
- **P50 (Median)**: 50% of requests complete in this time
- **P95**: 95% of requests complete in this time (typical SLA target)
- **P99**: 99% of requests complete in this time (worst-case planning)
- **Example**: P95 latency of 200ms means 95% of requests complete in ≤200ms

**Availability**
- **Definition**: Percentage of time system is operational
- **99.9% (Three 9s)**: 8.76 hours downtime/year
- **99.99% (Four 9s)**: 52.56 minutes downtime/year
- **99.999% (Five 9s)**: 5.26 minutes downtime/year

**Error Rate**
- **Definition**: Percentage of requests that fail
- **Calculation**: Failed requests / Total requests
- **Target**: <0.1% for most systems
```

### 2. **Scalability Definitions** (Too Brief)

**Current Status:**
- ✅ Horizontal vs Vertical mentioned
- ❌ Not explained with examples
- ❌ Scaling bottlenecks not discussed
- ❌ Stateful vs Stateless not explained

**What's Missing:**
```markdown
### Scalability Deep Dive

**Horizontal Scaling (Scale Out)**
- **Definition**: Add more servers/nodes to handle increased load
- **Example**: Add 10 more web servers to handle 10x traffic
- **Pros**: Can scale almost infinitely, fault tolerant
- **Cons**: Requires load balancing, data consistency challenges

**Vertical Scaling (Scale Up)**
- **Definition**: Add more resources (CPU, RAM) to existing servers
- **Example**: Upgrade server from 8GB to 32GB RAM
- **Pros**: Simple, no architectural changes
- **Cons**: Limited by hardware, single point of failure

**Stateful vs Stateless**
- **Stateless**: Server doesn't store client state between requests
  - Example: REST APIs, can scale horizontally easily
- **Stateful**: Server maintains client state (sessions, connections)
  - Example: WebSocket servers, harder to scale
  - Solution: Use sticky sessions or external state store (Redis)
```

### 3. **Load Balancing** (Mentioned but Not Explained)

**Current Status:**
- ✅ Mentioned in principles
- ✅ Detailed in cheat_sheet.md
- ❌ Not explained in system_design.md main content
- ❌ Health checks not explained
- ❌ Session affinity not explained

**What's Missing:**
```markdown
### Load Balancing

**What is Load Balancing?**
- **Definition**: Distribute incoming requests across multiple servers
- **Purpose**: Improve availability, scalability, performance

**Load Balancing Algorithms**
- **Round Robin**: Rotate requests evenly
- **Weighted Round Robin**: Rotate with server capacity weights
- **Least Connections**: Route to server with fewest active connections
- **IP Hash**: Route based on client IP (session affinity)
- **Consistent Hashing**: Minimal redistribution when servers added/removed

**Health Checks**
- **Liveness Probe**: Is the server process running?
- **Readiness Probe**: Can the server handle traffic?
- **Graceful Shutdown**: Drain connections before stopping

**Session Affinity (Sticky Sessions)**
- **Problem**: User logged in on Server A, next request goes to Server B
- **Solution**: Route same user to same server (IP hash or cookie-based)
- **Trade-off**: Reduces load distribution flexibility
```

### 4. **Caching Strategies** (Mentioned but Not Detailed)

**Current Status:**
- ✅ Redis explained
- ✅ Caching mentioned in principles
- ✅ Patterns in cheat_sheet.md
- ❌ Not explained in system_design.md
- ❌ Cache invalidation strategies not detailed
- ❌ Cache-aside vs Read-through vs Write-through not explained

**What's Missing:**
```markdown
### Caching Strategies

**Cache-Aside (Lazy Loading)**
- **Flow**: App checks cache → miss → fetch from DB → store in cache
- **Pros**: Simple, cache failures don't break app
- **Cons**: Cache miss penalty, potential stale data

**Read-Through**
- **Flow**: App requests cache → cache fetches from DB if miss
- **Pros**: App doesn't know about DB, consistent data
- **Cons**: Cache must know DB schema

**Write-Through**
- **Flow**: Write to cache and DB simultaneously
- **Pros**: Cache always fresh
- **Cons**: Write latency (both must succeed)

**Write-Back (Write-Behind)**
- **Flow**: Write to cache immediately, DB write async
- **Pros**: Fast writes
- **Cons**: Risk of data loss if cache fails before DB write

**Cache Invalidation**
- **TTL**: Time-based expiration
- **Versioned Keys**: `user:123:v42` - invalidate by incrementing version
- **Pub/Sub**: Publish invalidation events
- **Write-Through**: Always update cache on write
```

### 5. **Database Sharding** (Not in system_design.md)

**Current Status:**
- ✅ Covered in data_layer.md
- ❌ Not in system_design.md
- ❌ Sharding strategies not explained in context of system design

**What's Missing:**
```markdown
### Database Sharding

**What is Sharding?**
- **Definition**: Horizontal partitioning of data across multiple databases
- **Purpose**: Scale database beyond single server capacity

**Sharding Strategies**
- **Range-based**: Shard by ID ranges (1-1M → Shard1, 1M-2M → Shard2)
  - Pros: Easy range queries
  - Cons: Hot shards, uneven distribution
- **Hash-based**: Shard by hash(user_id) % num_shards
  - Pros: Even distribution
  - Cons: Hard to do range queries
- **Directory-based**: Lookup table maps key → shard
  - Pros: Flexible, easy to rebalance
  - Cons: Single point of failure, lookup overhead

**Sharding Challenges**
- **Cross-shard queries**: Expensive, avoid if possible
- **Transactions**: Need distributed transactions (2PC) or avoid
- **Rebalancing**: Moving data when adding/removing shards
- **Hot shards**: Uneven load distribution
```

### 6. **Database Replication** (Not in system_design.md)

**Current Status:**
- ✅ Covered in data_layer.md
- ❌ Not in system_design.md
- ❌ Read replicas not explained in system design context

**What's Missing:**
```markdown
### Database Replication

**What is Replication?**
- **Definition**: Copying data from one database to another
- **Purpose**: High availability, read scaling, disaster recovery

**Replication Types**
- **Master-Slave (Primary-Replica)**: One write master, multiple read replicas
  - Writes → Master, Reads → Replicas
  - Replication lag: Replicas may be slightly behind
- **Master-Master (Multi-Leader)**: Multiple write masters
  - Pros: Write scaling, fault tolerance
  - Cons: Conflict resolution needed
- **Synchronous**: Wait for replica confirmation (strong consistency)
- **Asynchronous**: Don't wait (better performance, eventual consistency)

**Read Replicas**
- **Use Case**: Scale read-heavy workloads
- **Example**: 1 write master, 5 read replicas = 5x read capacity
- **Trade-off**: Read replicas may have stale data (replication lag)
```

### 7. **CDN (Content Delivery Network)** (Mentioned but Not Explained)

**Current Status:**
- ✅ Mentioned in problems (File Storage, Video Streaming)
- ❌ Not explained as a concept
- ❌ How CDN works not explained
- ❌ Edge caching not explained

**What's Missing:**
```markdown
### CDN (Content Delivery Network)

**What is a CDN?**
- **Definition**: Distributed network of servers that cache content close to users
- **Purpose**: Reduce latency, reduce origin server load

**How CDN Works**
1. User requests content (e.g., image.jpg)
2. Request routed to nearest CDN edge server
3. If cached (cache hit): Return immediately
4. If not cached (cache miss): Fetch from origin, cache, return

**CDN Use Cases**
- **Static Assets**: Images, CSS, JavaScript files
- **Video Streaming**: Video files, live streams
- **API Responses**: Cached API responses (with appropriate TTL)
- **Global Distribution**: Serve content from multiple geographic locations

**CDN Benefits**
- **Lower Latency**: Content served from nearby edge server
- **Reduced Load**: Origin server handles fewer requests
- **Better Availability**: CDN can serve cached content even if origin is down
- **Cost Savings**: Reduced bandwidth costs

**CDN Caching**
- **TTL**: How long content stays in CDN cache
- **Cache Invalidation**: Purge cache when content updates
- **Cache-Control Headers**: HTTP headers control caching behavior
```

### 8. **Microservices Architecture** (Mentioned but Not Explained)

**Current Status:**
- ✅ Mentioned briefly in "Modern Variations"
- ❌ Not explained as a concept
- ❌ Pros/cons not detailed
- ❌ Service communication not explained

**What's Missing:**
```markdown
### Microservices Architecture

**What are Microservices?**
- **Definition**: Architecture where application is split into small, independent services
- **Each Service**: Own database, own deployment, communicates via APIs

**Microservices vs Monolith**
- **Monolith**: Single application, single database, single deployment
- **Microservices**: Multiple services, multiple databases, independent deployments

**Pros of Microservices**
- **Independent Scaling**: Scale services independently
- **Technology Diversity**: Use different tech stacks per service
- **Fault Isolation**: Failure in one service doesn't bring down entire system
- **Team Autonomy**: Different teams own different services

**Cons of Microservices**
- **Complexity**: More moving parts, harder to debug
- **Network Latency**: Inter-service communication overhead
- **Data Consistency**: Harder to maintain consistency across services
- **Deployment Complexity**: Need orchestration (Kubernetes, etc.)

**Service Communication**
- **Synchronous**: HTTP/REST, gRPC (request-response)
- **Asynchronous**: Message queues (Kafka, RabbitMQ) (event-driven)
```

### 9. **API Gateway** (Has Problem but Not Explained as Concept)

**Current Status:**
- ✅ Problem #12 covers API Gateway
- ❌ Not explained as a fundamental concept
- ❌ Benefits not detailed

**What's Missing:**
```markdown
### API Gateway

**What is an API Gateway?**
- **Definition**: Single entry point for all client requests to microservices
- **Purpose**: Route requests, handle cross-cutting concerns

**API Gateway Responsibilities**
- **Routing**: Route requests to appropriate microservice
- **Authentication/Authorization**: Verify user identity and permissions
- **Rate Limiting**: Limit requests per user/IP
- **Request/Response Transformation**: Modify requests/responses
- **Load Balancing**: Distribute requests across service instances
- **Monitoring**: Logging, metrics collection
- **Protocol Translation**: HTTP → gRPC, etc.

**Benefits**
- **Single Entry Point**: Clients only know about gateway
- **Centralized Security**: Auth logic in one place
- **Service Abstraction**: Hide internal service structure
- **Cross-Cutting Concerns**: Handle logging, rate limiting centrally
```

### 10. **Rate Limiting Algorithms** (Has Problem but Algorithms Not Detailed)

**Current Status:**
- ✅ Problem #3 covers Rate Limiter
- ❌ Algorithms not explained in detail
- ❌ Token bucket vs Sliding window not explained

**What's Missing:**
```markdown
### Rate Limiting Algorithms

**Token Bucket**
- **How it works**: 
  - Bucket has capacity (max tokens)
  - Tokens refill at fixed rate (e.g., 10 tokens/second)
  - Request consumes 1 token
  - If bucket empty, request rejected
- **Pros**: Allows bursts, smooth rate limiting
- **Cons**: More complex to implement

**Leaky Bucket**
- **How it works**:
  - Bucket has capacity
  - Requests added to bucket
  - Requests processed at fixed rate (leak)
  - If bucket full, request rejected
- **Pros**: Smooth output rate
- **Cons**: No burst allowance

**Fixed Window**
- **How it works**:
  - Count requests in time window (e.g., per minute)
  - Reset counter at window boundary
  - If count > limit, reject
- **Pros**: Simple to implement
- **Cons**: Burst at window boundaries

**Sliding Window**
- **How it works**:
  - Track requests in sliding time window
  - Count requests in last N seconds
  - If count > limit, reject
- **Pros**: Smooth rate limiting, no burst issues
- **Cons**: More memory intensive
```

### 11. **Consistent Hashing** (In Cheat Sheet but Not Explained)

**Current Status:**
- ✅ Mentioned in cheat_sheet.md
- ❌ Not explained in system_design.md
- ❌ Virtual nodes not explained

**What's Missing:**
```markdown
### Consistent Hashing

**What is Consistent Hashing?**
- **Definition**: Hashing technique that minimizes redistribution when nodes added/removed
- **Problem it solves**: Traditional hashing requires remapping all keys when nodes change

**How it Works**
1. Map nodes and keys to a hash ring (0 to 2^32-1)
2. Key belongs to first node clockwise from its hash
3. When node added: Only keys between previous node and new node remap
4. When node removed: Keys remap to next node clockwise

**Virtual Nodes**
- **Problem**: Uneven distribution with few nodes
- **Solution**: Each physical node has multiple virtual nodes on ring
- **Benefit**: More even distribution, easier rebalancing

**Use Cases**
- **Distributed Caching**: Redis cluster, Memcached
- **Load Balancing**: Consistent hash load balancer
- **Database Sharding**: Shard assignment
```

### 12. **Circuit Breaker Pattern** (In Cheat Sheet but Not in system_design.md)

**Current Status:**
- ✅ Detailed in cheat_sheet.md
- ❌ Not in system_design.md
- ❌ Not explained as a concept

**What's Missing:**
```markdown
### Circuit Breaker Pattern

**What is a Circuit Breaker?**
- **Definition**: Design pattern that prevents cascading failures
- **Analogy**: Like electrical circuit breaker - stops current flow when overloaded

**States**
- **Closed**: Normal operation, requests pass through
- **Open**: Failing, requests fail fast (don't call downstream)
- **Half-Open**: Testing if service recovered, allow limited requests

**How it Works**
1. Monitor failure rate
2. If failures exceed threshold → Open circuit
3. After timeout → Half-Open (test with limited requests)
4. If test succeeds → Closed, if fails → Open again

**Benefits**
- **Prevent Cascading Failures**: Stop calling failing service
- **Fast Failure**: Fail fast instead of waiting for timeout
- **Automatic Recovery**: Test if service recovered

**Use Cases**
- **External API Calls**: Don't call failing third-party API
- **Database Calls**: Don't query failing database
- **Microservice Calls**: Don't call failing microservice
```

### 13. **Other Missing Concepts**

**Event-Driven Architecture**
- ❌ Not explained
- ❌ Event sourcing mentioned but not explained
- ❌ CQRS mentioned but not explained

**Database Concepts**
- ❌ Connection pooling not mentioned
- ❌ Database indexing strategies not in system_design.md
- ❌ Query optimization not mentioned

**Distributed Systems**
- ❌ Leader election mentioned but not explained
- ❌ Quorum mentioned but not explained
- ❌ Vector clocks not mentioned
- ❌ Gossip protocol not mentioned

**Data Structures for System Design**
- ❌ Bloom filters not mentioned (useful for caching, deduplication)
- ❌ Geohashing mentioned but not explained (ride hailing problem)

**API Design**
- ❌ API versioning not mentioned
- ❌ REST vs GraphQL vs gRPC not compared in system_design.md

**Monitoring & Observability**
- ❌ Distributed tracing not mentioned
- ❌ Log aggregation not mentioned
- ❌ Metrics collection not mentioned

---

## Recommendations

### High Priority (Add to system_design.md)

1. **Add "System Design Fundamentals" section** at the beginning with:
   - Performance metrics (QPS, latency percentiles, availability)
   - Scalability definitions (horizontal/vertical, stateful/stateless)
   - Load balancing (algorithms, health checks, session affinity)
   - Caching strategies (cache-aside, read-through, write-through, invalidation)

2. **Add "Database Scaling" section**:
   - Replication (master-slave, read replicas)
   - Sharding (strategies, challenges)
   - Consistent hashing

3. **Add "Architecture Patterns" section**:
   - Microservices vs Monolith
   - API Gateway
   - Circuit Breaker
   - Event-Driven Architecture

4. **Add "Rate Limiting" section**:
   - Token bucket, leaky bucket, fixed window, sliding window algorithms

5. **Add "CDN" section**:
   - What it is, how it works, use cases, caching

### Medium Priority

6. **Add "Distributed Systems Concepts"**:
   - Leader election
   - Quorum
   - Vector clocks (brief)

7. **Add "Data Structures for System Design"**:
   - Bloom filters
   - Geohashing

8. **Add "API Design"**:
   - REST vs GraphQL vs gRPC comparison
   - API versioning strategies

### Low Priority

9. **Add "Monitoring & Observability"**:
   - Distributed tracing
   - Log aggregation
   - Metrics collection

---

## Summary

The system_design.md file has **excellent problem coverage** (12 problems) but is **missing fundamental definitions and concepts** that are essential for system design interviews. The content exists in other files (cheat_sheet.md, data_layer.md) but should be consolidated and explained in the system design section for completeness.

**Key Missing Areas:**
1. Fundamental metrics and definitions
2. Scalability deep dive
3. Load balancing details
4. Caching strategies
5. Database scaling (replication, sharding)
6. Architecture patterns (microservices, API gateway, circuit breaker)
7. Rate limiting algorithms
8. CDN explanation
9. Consistent hashing
10. Event-driven architecture

**Recommendation**: Add a comprehensive "System Design Fundamentals" section at the beginning of system_design.md covering all these concepts before the problem solutions.

