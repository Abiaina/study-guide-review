---
title: System Design Problems
---

# System Design Problems

## **🔧 System Design Fundamentals**

*Reference: Grokking the System Design Interview*

Before diving into specific problems, let's understand the fundamental concepts, definitions, and patterns that appear throughout system design interviews.

---

### **📊 Performance Metrics & Definitions**

**Throughput (QPS/RPS)**
- **Definition**: Number of requests/queries processed per second
- **QPS**: Queries Per Second
- **RPS**: Requests Per Second
- **Example**: 1000 QPS = 1000 requests/second
- **Measurement**: Total requests / time window
- **Scaling**: Increase throughput by adding servers or optimizing code

**Latency**
- **Definition**: Time taken for a request to complete (end-to-end)
- **P50 (Median)**: 50% of requests complete in this time or less
- **P95**: 95% of requests complete in this time or less (typical SLA target)
- **P99**: 99% of requests complete in this time or less (worst-case planning)
- **P99.9**: 99.9% of requests complete in this time or less (extreme cases)
- **Example**: P95 latency of 200ms means 95% of requests complete in ≤200ms
- **Why Percentiles Matter**: Average can hide outliers; percentiles show real user experience

**Availability**
- **Definition**: Percentage of time system is operational and accessible
- **99% (Two 9s)**: 87.6 hours downtime/year (~3.65 days)
- **99.9% (Three 9s)**: 8.76 hours downtime/year
- **99.99% (Four 9s)**: 52.56 minutes downtime/year
- **99.999% (Five 9s)**: 5.26 minutes downtime/year
- **Calculation**: (Total time - Downtime) / Total time × 100
- **SLA vs SLO**: SLA is contract with penalties; SLO is internal target

**Error Rate**
- **Definition**: Percentage of requests that fail or return errors
- **Calculation**: Failed requests / Total requests × 100
- **Target**: <0.1% for most systems, <0.01% for critical systems
- **4xx Errors**: Client errors (bad request, not found, unauthorized)
- **5xx Errors**: Server errors (internal error, service unavailable)
- **Monitoring**: Track error rate over time, set up alerts for spikes

**Capacity Planning**
- **Peak Load**: Maximum expected traffic (e.g., Black Friday)
- **Average Load**: Normal traffic levels
- **Headroom**: Extra capacity above peak (typically 20-30%)
- **Example**: If peak is 10K QPS, plan for 13K QPS capacity

---

### **📈 Scalability Deep Dive**

**Horizontal Scaling (Scale Out)**
- **Definition**: Add more servers/nodes to handle increased load
- **Example**: Add 10 more web servers to handle 10x traffic
- **Pros**: 
  - Can scale almost infinitely
  - Fault tolerant (one server fails, others continue)
  - Cost-effective (commodity hardware)
- **Cons**: 
  - Requires load balancing
  - Data consistency challenges
  - Network communication overhead
- **When to Use**: Stateless services, distributed systems

**Vertical Scaling (Scale Up)**
- **Definition**: Add more resources (CPU, RAM, storage) to existing servers
- **Example**: Upgrade server from 8GB to 32GB RAM, 4 cores to 16 cores
- **Pros**: 
  - Simple, no architectural changes
  - No load balancing needed
  - Lower latency (no network hops)
- **Cons**: 
  - Limited by hardware maximums
  - Single point of failure
  - Expensive (high-end hardware)
  - Downtime during upgrades
- **When to Use**: Small to medium scale, single-server applications

**Stateful vs Stateless Services**

**Stateless Services**
- **Definition**: Server doesn't store client state between requests
- **Each Request**: Contains all information needed to process it
- **Example**: REST APIs, stateless web servers
- **Pros**: 
  - Easy horizontal scaling (any server can handle any request)
  - Simple load balancing
  - Fault tolerant (server dies, no state lost)
- **Cons**: 
  - Client must send all data each time
  - Can't maintain sessions server-side
- **Solution for Sessions**: Store in external store (Redis, database)

**Stateful Services**
- **Definition**: Server maintains client state (sessions, connections, data)
- **Example**: WebSocket servers, in-memory caches, database connections
- **Pros**: 
  - Faster (no need to fetch state)
  - Can maintain persistent connections
- **Cons**: 
  - Harder to scale horizontally
  - State lost if server crashes
  - Requires sticky sessions or state replication
- **Solutions**: 
  - Sticky sessions (route same client to same server)
  - External state store (Redis, database)
  - State replication across servers

**Scaling Bottlenecks**
- **Database**: Often the bottleneck; use read replicas, caching, sharding
- **Network**: Bandwidth limits, latency issues
- **CPU**: Compute-intensive operations
- **Memory**: Large datasets, caching
- **I/O**: Disk reads/writes, network I/O
- **Identify**: Use monitoring to find bottlenecks, optimize accordingly

---

### **⚖️ Load Balancing**

**What is Load Balancing?**
- **Definition**: Distribute incoming requests across multiple servers
- **Purpose**: Improve availability, scalability, performance
- **Location**: Can be at DNS, network, or application layer

**Load Balancing Algorithms**

**Round Robin**
- **How**: Rotate requests evenly across servers (1→2→3→1→2→3...)
- **Pros**: Simple, fair distribution
- **Cons**: Ignores server load differences, doesn't account for request complexity
- **Use Case**: Homogeneous servers, similar request processing times

**Weighted Round Robin**
- **How**: Like round robin but with server capacity weights
- **Example**: Server A (weight 3), Server B (weight 1) → A gets 3 requests for every 1 to B
- **Pros**: Accounts for server capacity differences
- **Cons**: Requires manual weight configuration
- **Use Case**: Mixed server sizes (some more powerful than others)

**Least Connections**
- **How**: Route to server with fewest active connections
- **Pros**: Adapts to variable request processing times
- **Cons**: Requires connection tracking, may not account for connection duration
- **Use Case**: Long-lived connections, variable request processing times

**IP Hash**
- **How**: Hash(client IP) → server assignment
- **Pros**: Sticky sessions (same client → same server), simple
- **Cons**: Poorly balances NAT'd clients (many clients share IP), uneven if IPs not random
- **Use Case**: Session affinity without cookies

**Header/Cookie Hash**
- **How**: Hash on specific header or cookie value
- **Pros**: Fine-grained stickiness, better than IP hash
- **Cons**: Requires header/cookie presence
- **Use Case**: Stateful session shards, user-based routing

**Consistent Hashing**
- **How**: Hash(key) on ring, route to first server clockwise
- **Pros**: Minimal reshuffle when servers added/removed (only affected keys remap)
- **Cons**: Requires key choice, uneven distribution with few nodes
- **Solution**: Virtual nodes (each physical server has multiple virtual nodes on ring)
- **Use Case**: Distributed caches, sharded databases, CDN

**Health Checks**
- **Liveness Probe**: Is the server process running? (Can I connect?)
- **Readiness Probe**: Can the server handle traffic? (Is it healthy enough?)
- **Graceful Shutdown**: Drain existing connections before stopping server
- **Slow Start**: Gradually increase traffic to newly added servers
- **Failure Detection**: Remove unhealthy servers from rotation

**Session Affinity (Sticky Sessions)**
- **Problem**: User logged in on Server A, next request goes to Server B (session lost)
- **Solution**: Route same user to same server
- **Methods**: 
  - IP Hash (simple but imperfect)
  - Cookie-based (more reliable)
  - Application-level routing
- **Trade-off**: Reduces load distribution flexibility, harder to scale

---

### **💾 Caching Strategies**

**Why Cache?**
- **Reduce Latency**: Serve data from fast memory instead of slow database
- **Reduce Load**: Fewer database queries = less database load
- **Improve Availability**: Serve cached data even if database is down
- **Cost Savings**: Reduce database costs, bandwidth costs

**Cache-Aside (Lazy Loading)**
- **Flow**: 
  1. App checks cache
  2. If hit: return cached data
  3. If miss: fetch from database, store in cache, return data
- **Pros**: 
  - Simple to implement
  - Cache failures don't break application
  - Only cache frequently accessed data
- **Cons**: 
  - Cache miss penalty (two round trips: cache + DB)
  - Potential stale data (cache not updated on DB write)
  - Race conditions possible (two requests miss cache simultaneously)
- **Use Case**: General purpose, most common pattern

**Read-Through**
- **Flow**: 
  1. App requests data from cache
  2. Cache checks if data exists
  3. If miss: cache fetches from database, stores, returns
  4. App doesn't know about database
- **Pros**: 
  - App doesn't need database logic
  - Consistent data (cache handles DB interaction)
  - Simpler application code
- **Cons**: 
  - Cache must know database schema
  - Cache becomes more complex
- **Use Case**: When cache can abstract database complexity

**Write-Through**
- **Flow**: 
  1. App writes to cache
  2. Cache immediately writes to database
  3. Both must succeed
- **Pros**: 
  - Cache always fresh (no stale data)
  - Data durability (written to DB)
- **Cons**: 
  - Write latency (both cache and DB must complete)
  - Write failures affect both cache and DB
- **Use Case**: When data freshness is critical

**Write-Back (Write-Behind)**
- **Flow**: 
  1. App writes to cache
  2. Cache returns success immediately
  3. Cache writes to database asynchronously (later)
- **Pros**: 
  - Fast writes (no DB wait)
  - Can batch multiple writes
- **Cons**: 
  - Risk of data loss if cache fails before DB write
  - Potential inconsistency (cache has data DB doesn't)
  - Complex failure handling
- **Use Case**: High write throughput, can tolerate some data loss

**Refresh-Ahead**
- **Flow**: 
  1. Cache proactively refreshes data before expiration
  2. Background job refreshes popular items
- **Pros**: 
  - Reduces cache misses
  - Better user experience (data always fresh)
- **Cons**: 
  - Wastes resources refreshing unused data
  - More complex implementation
- **Use Case**: Predictable access patterns, critical data

**Cache Invalidation Strategies**

**TTL (Time To Live)**
- **How**: Set expiration time on cached data
- **Pros**: Simple, automatic cleanup
- **Cons**: Data may be stale before expiration
- **Use Case**: Data that changes infrequently

**Versioned Keys**
- **How**: Use versioned keys like `user:123:v42`
- **Invalidation**: Increment version to invalidate
- **Pros**: Explicit control, can track versions
- **Cons**: Need to track versions, more complex
- **Use Case**: When you need explicit invalidation

**Pub/Sub Invalidation**
- **How**: Publish invalidation events when data changes
- **Pros**: Real-time invalidation, decoupled
- **Cons**: Requires pub/sub infrastructure
- **Use Case**: Distributed systems, real-time updates

**Write-Through Invalidation**
- **How**: Update cache when writing to database
- **Pros**: Cache always fresh
- **Cons**: Write latency, both must succeed

**Cache Patterns**
- **Cache-Aside**: Most common, app manages cache
- **Read-Through**: Cache manages DB reads
- **Write-Through**: Cache writes to DB synchronously
- **Write-Back**: Cache writes to DB asynchronously
- **Refresh-Ahead**: Proactive cache refresh

---

### **🗄️ Database Scaling**

**Replication**

**What is Replication?**
- **Definition**: Copying data from one database to another
- **Purpose**: High availability, read scaling, disaster recovery
- **Types**: Master-Slave, Master-Master, Synchronous, Asynchronous

**Master-Slave (Primary-Replica)**
- **How**: 
  - One master handles all writes
  - Multiple replicas handle reads
  - Master replicates changes to replicas
- **Pros**: 
  - Read scaling (multiple read replicas)
  - High availability (replica can become master if master fails)
  - Disaster recovery (replicas in different regions)
- **Cons**: 
  - Replication lag (replicas may be slightly behind)
  - Master is single point of failure for writes
  - Eventual consistency on reads
- **Use Case**: Read-heavy workloads, need read scaling

**Master-Master (Multi-Leader)**
- **How**: 
  - Multiple masters can handle writes
  - Masters replicate to each other
- **Pros**: 
  - Write scaling (multiple write masters)
  - Fault tolerance (if one master fails, others continue)
- **Cons**: 
  - Conflict resolution needed (same data written to different masters)
  - More complex
  - Eventual consistency
- **Use Case**: Multi-region deployments, write scaling

**Synchronous Replication**
- **How**: Master waits for replica confirmation before returning success
- **Pros**: Strong consistency (replicas always in sync)
- **Cons**: Higher latency (must wait for replica), lower availability (if replica down, write fails)
- **Use Case**: When consistency is critical (financial systems)

**Asynchronous Replication**
- **How**: Master returns success immediately, replicates later
- **Pros**: Lower latency, higher availability
- **Cons**: Replication lag, potential data loss if master fails before replication
- **Use Case**: When performance is more important than immediate consistency

**Read Replicas**
- **Purpose**: Scale read-heavy workloads
- **Example**: 1 write master, 5 read replicas = 5x read capacity
- **Trade-off**: Read replicas may have stale data (replication lag)
- **Use Case**: Analytics, reporting, read-heavy applications

**Sharding (Horizontal Partitioning)**

**What is Sharding?**
- **Definition**: Horizontal partitioning of data across multiple databases
- **Purpose**: Scale database beyond single server capacity
- **Problem it Solves**: Single database can't handle all data or traffic

**Sharding Strategies**

**Range-Based Sharding**
- **How**: Shard by ID ranges
  - Shard 1: IDs 1-1,000,000
  - Shard 2: IDs 1,000,001-2,000,000
  - Shard 3: IDs 2,000,001-3,000,000
- **Pros**: 
  - Easy range queries (all data in one shard)
  - Simple to understand
- **Cons**: 
  - Hot shards (uneven distribution)
  - Hard to rebalance
- **Use Case**: Time-series data, sequential IDs

**Hash-Based Sharding**
- **How**: Shard by hash(key) % num_shards
  - Example: hash(user_id) % 4 → determines shard
- **Pros**: 
  - Even distribution (if hash function is good)
  - Predictable shard assignment
- **Cons**: 
  - Hard to do range queries (data spread across shards)
  - Rebalancing requires moving lots of data
- **Use Case**: User data, evenly distributed data

**Directory-Based Sharding**
- **How**: Lookup table maps key → shard
  - Example: `shard_map[user_id] = shard_number`
- **Pros**: 
  - Flexible (easy to change shard assignment)
  - Easy to rebalance
- **Cons**: 
  - Single point of failure (lookup table)
  - Lookup overhead (extra query)
- **Use Case**: When flexibility is important, complex sharding rules

**Sharding Challenges**

**Cross-Shard Queries**
- **Problem**: Querying data across multiple shards is expensive
- **Solution**: 
  - Avoid cross-shard queries when possible
  - Pre-aggregate data
  - Use separate analytics database
- **Example**: "Get all users in US" requires querying all shards

**Transactions**
- **Problem**: Transactions across shards are complex
- **Solution**: 
  - Use distributed transactions (2PC - Two-Phase Commit)
  - Use Saga pattern (compensating transactions)
  - Design to avoid cross-shard transactions
- **Example**: Transfer money between users on different shards

**Rebalancing**
- **Problem**: Moving data when adding/removing shards
- **Solution**: 
  - Consistent hashing (minimal data movement)
  - Gradual migration (move data in background)
  - Use directory-based sharding for flexibility

**Hot Shards**
- **Problem**: Some shards get more traffic than others
- **Solution**: 
  - Better sharding key selection
  - Split hot shards
  - Use consistent hashing with virtual nodes

**Consistent Hashing**
- **What**: Hashing technique that minimizes redistribution when nodes added/removed
- **Problem it Solves**: Traditional hashing requires remapping all keys when nodes change
- **How it Works**:
  1. Map nodes and keys to a hash ring (0 to 2^32-1)
  2. Key belongs to first node clockwise from its hash
  3. When node added: Only keys between previous node and new node remap
  4. When node removed: Keys remap to next node clockwise
- **Virtual Nodes**: Each physical node has multiple virtual nodes on ring for even distribution
- **Use Cases**: Distributed caching, load balancing, database sharding

---

### **🏗️ Architecture Patterns**

**Microservices vs Monolith**

**Monolith**
- **Definition**: Single application, single database, single deployment
- **Pros**: 
  - Simple to develop and deploy
  - Easy to test (everything in one place)
  - No network latency between components
  - ACID transactions across all data
- **Cons**: 
  - Hard to scale (must scale entire application)
  - Technology lock-in (one tech stack)
  - Single point of failure
  - Hard for large teams (everyone works on same codebase)

**Microservices**
- **Definition**: Application split into small, independent services
- **Each Service**: Own database, own deployment, communicates via APIs
- **Pros**: 
  - Independent scaling (scale services independently)
  - Technology diversity (use different tech stacks per service)
  - Fault isolation (failure in one service doesn't bring down entire system)
  - Team autonomy (different teams own different services)
  - Easier to understand (smaller codebases)
- **Cons**: 
  - Complexity (more moving parts, harder to debug)
  - Network latency (inter-service communication overhead)
  - Data consistency (harder to maintain consistency across services)
  - Deployment complexity (need orchestration like Kubernetes)
  - Distributed transactions (complex, often avoided)
- **When to Use**: 
  - Large teams
  - Different scaling requirements per service
  - Need technology diversity
  - Services can be independently deployed

**Service Communication**

**Synchronous Communication**
- **HTTP/REST**: Request-response, simple, widely supported
- **gRPC**: Binary protocol, faster, type-safe, streaming support
- **Pros**: Simple, request-response pattern
- **Cons**: Tight coupling, blocking calls, cascading failures
- **Use Case**: When you need immediate response

**Asynchronous Communication**
- **Message Queues**: Kafka, RabbitMQ, SQS
- **Event-Driven**: Services publish/subscribe to events
- **Pros**: Loose coupling, better fault tolerance, can handle bursts
- **Cons**: Eventual consistency, harder to debug, message ordering
- **Use Case**: When you can tolerate eventual consistency, need to decouple services

**API Gateway**

**What is an API Gateway?**
- **Definition**: Single entry point for all client requests to microservices
- **Purpose**: Route requests, handle cross-cutting concerns
- **Analogy**: Front door to your microservices architecture

**API Gateway Responsibilities**
- **Routing**: Route requests to appropriate microservice
- **Authentication/Authorization**: Verify user identity and permissions
- **Rate Limiting**: Limit requests per user/IP
- **Request/Response Transformation**: Modify requests/responses
- **Load Balancing**: Distribute requests across service instances
- **Monitoring**: Logging, metrics collection
- **Protocol Translation**: HTTP → gRPC, etc.
- **API Versioning**: Handle multiple API versions
- **Caching**: Cache responses to reduce backend load

**Benefits**
- **Single Entry Point**: Clients only know about gateway
- **Centralized Security**: Auth logic in one place
- **Service Abstraction**: Hide internal service structure
- **Cross-Cutting Concerns**: Handle logging, rate limiting centrally
- **Simplified Client**: Clients don't need to know about multiple services

**Examples**: AWS API Gateway, Kong, Zuul, Envoy

**Circuit Breaker Pattern**

**What is a Circuit Breaker?**
- **Definition**: Design pattern that prevents cascading failures
- **Analogy**: Like electrical circuit breaker - stops current flow when overloaded

**States**
- **Closed**: Normal operation, requests pass through
- **Open**: Failing, requests fail fast (don't call downstream)
- **Half-Open**: Testing if service recovered, allow limited requests

**How it Works**
1. Monitor failure rate or error count
2. If failures exceed threshold → Open circuit
3. After timeout → Half-Open (test with limited requests)
4. If test succeeds → Closed, if fails → Open again

**Benefits**
- **Prevent Cascading Failures**: Stop calling failing service
- **Fast Failure**: Fail fast instead of waiting for timeout
- **Automatic Recovery**: Test if service recovered
- **Resource Protection**: Don't waste resources on failing calls

**Use Cases**
- **External API Calls**: Don't call failing third-party API
- **Database Calls**: Don't query failing database
- **Microservice Calls**: Don't call failing microservice

**Implementation Example**
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = None
    
    def call(self, func):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise CircuitBreakerOpenError()
        
        try:
            result = func()
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            raise e
```

**CQRS (Command Query Responsibility Segregation)**

**What is CQRS?**
- **Definition**: Separate read and write models - use different models for reading and writing data
- **Core Idea**: Commands (writes) and Queries (reads) are fundamentally different operations
- **Professional Use**: Used in production systems for scalability and performance

**Why CQRS?**
- **Different Scaling Needs**: Reads often outnumber writes (100:1 or more)
- **Different Data Shapes**: Write model optimized for writes, read model optimized for reads
- **Performance**: Optimize each model independently
- **Complexity**: Write model can be complex (normalized), read model can be simple (denormalized)

**How it Works**

**Command Side (Write Model)**
- **Purpose**: Handle writes, business logic, validation
- **Structure**: Normalized, ACID transactions, complex relationships
- **Example**: User registration, order creation, payment processing
- **Storage**: Primary database (source of truth)
- **Characteristics**: 
  - Strong consistency
  - Complex validation
  - Business rules enforcement

**Query Side (Read Model)**
- **Purpose**: Handle reads, optimized for querying
- **Structure**: Denormalized, flattened, pre-computed views
- **Example**: User profile display, order history, dashboard data
- **Storage**: Read-optimized database, cache, materialized views
- **Characteristics**: 
  - Optimized for reads
  - Can be eventually consistent
  - Pre-aggregated data

**Synchronization**
- **Event Sourcing**: Write model publishes events, read model subscribes
- **Change Data Capture (CDC)**: Capture database changes, update read model
- **Dual Write**: Write to both models (simpler but risk of inconsistency)
- **Eventual Consistency**: Read model may be slightly behind write model

**CQRS Architecture Example**
```text
User Registration (Command)
  ↓
Write Model (Normalized DB)
  ↓
Publish Event: UserCreated
  ↓
Read Model (Denormalized DB/Cache)
  ↓
User Profile Query (Optimized Read)
```

**When to Use CQRS**
- ✅ **Read/Write Ratio**: Much more reads than writes
- ✅ **Different Data Shapes**: Write and read need different structures
- ✅ **Performance**: Need to optimize reads and writes independently
- ✅ **Scalability**: Need to scale reads separately from writes
- ✅ **Complex Business Logic**: Write model has complex rules
- ❌ **Simple CRUD**: Overkill for simple applications
- ❌ **Strong Consistency Required**: If reads must be immediately consistent

**Benefits**
- **Independent Scaling**: Scale read and write models separately
- **Performance**: Optimize each model for its purpose
- **Flexibility**: Can use different databases for reads and writes
- **Complexity Management**: Separate concerns, easier to reason about

**Challenges**
- **Complexity**: More moving parts, event synchronization
- **Eventual Consistency**: Reads may be slightly stale
- **Event Handling**: Need reliable event processing
- **Debugging**: Harder to debug across models

**Real-World Example**
```python
# Command Side (Write Model)
class UserCommandHandler:
    def create_user(self, user_data):
        """ Validate, business logic """
        user = User.create(user_data)
        db.session.commit()
        
        """ Publish event """
        event_bus.publish(UserCreatedEvent(
            user_id=user.id,
            email=user.email,
            created_at=user.created_at
        ))
        return user

# Query Side (Read Model)
class UserQueryHandler:
    def get_user_profile(self, user_id):
        """ Read from optimized read model """
        return user_read_db.get_user_profile(user_id)

# Event Handler (Syncs read model)
class UserCreatedEventHandler:
    def handle(self, event):
        """ Update read model with denormalized data """
        user_read_db.create_user_profile(
            user_id=event.user_id,
            email=event.email,
            display_name=event.email.split('@')[0],  # Pre-computed
            created_at=event.created_at
        )
```

**CQRS + Event Sourcing**
- **Event Sourcing**: Store events as source of truth, rebuild state from events
- **Combination**: CQRS for separation, Event Sourcing for audit trail
- **Benefits**: Complete audit trail, time travel, replay events

---

### **🌐 CDN (Content Delivery Network)**

**What is a CDN?**
- **Definition**: Distributed network of servers that cache content close to users
- **Purpose**: Reduce latency, reduce origin server load, improve availability
- **How it Works**: Cache content at edge locations worldwide

**How CDN Works**
1. User requests content (e.g., `example.com/image.jpg`)
2. DNS routes to nearest CDN edge server
3. Edge server checks cache
4. **Cache Hit**: Return immediately (fast!)
5. **Cache Miss**: Fetch from origin server, cache it, return to user
6. Subsequent requests served from cache

**CDN Architecture**
```text
User (New York)
  ↓
CDN Edge Server (New York) ← Cache Hit (Fast!)
  ↓ (Cache Miss)
Origin Server (California) ← Slower, but only on miss
```

**CDN Use Cases**
- **Static Assets**: Images, CSS, JavaScript files
- **Video Streaming**: Video files, live streams
- **API Responses**: Cached API responses (with appropriate TTL)
- **Global Distribution**: Serve content from multiple geographic locations
- **DDoS Protection**: CDN can absorb attacks

**CDN Benefits**
- **Lower Latency**: Content served from nearby edge server (10-50ms vs 200-500ms)
- **Reduced Load**: Origin server handles fewer requests
- **Better Availability**: CDN can serve cached content even if origin is down
- **Cost Savings**: Reduced bandwidth costs, reduced origin server costs
- **Scalability**: CDN handles traffic spikes automatically

**CDN Caching**
- **TTL**: How long content stays in CDN cache
- **Cache-Control Headers**: HTTP headers control caching behavior
  - `Cache-Control: public, max-age=3600` (cache for 1 hour)
  - `Cache-Control: no-cache` (always validate with origin)
- **Cache Invalidation**: Purge cache when content updates
- **Cache Keys**: URL-based (different URLs = different cache entries)

**CDN Providers**
- **CloudFront** (AWS)
- **Cloudflare**
- **Fastly**
- **Akamai**
- **Azure CDN**

---

### **🚦 Rate Limiting Algorithms**

**What is Rate Limiting?**
- **Definition**: Limit number of requests a user/IP can make in a time window
- **Purpose**: Prevent abuse, protect resources, ensure fair usage
- **Example**: 100 requests per minute per user

**Token Bucket**
- **How it Works**: 
  - Bucket has capacity (max tokens, e.g., 100)
  - Tokens refill at fixed rate (e.g., 10 tokens/second)
  - Request consumes 1 token
  - If bucket empty, request rejected
- **Pros**: 
  - Allows bursts (if bucket has tokens)
  - Smooth rate limiting
  - Natural throttling
- **Cons**: 
  - More complex to implement
  - Need to track tokens and refill rate
- **Use Case**: When you want to allow bursts but limit average rate

**Leaky Bucket**
- **How it Works**:
  - Bucket has capacity
  - Requests added to bucket
  - Requests processed at fixed rate (leak, e.g., 10 requests/second)
  - If bucket full, request rejected
- **Pros**: 
  - Smooth output rate
  - No bursts
- **Cons**: 
  - No burst allowance
  - Requests may wait in bucket
- **Use Case**: When you need smooth, constant output rate

**Fixed Window**
- **How it Works**:
  - Count requests in time window (e.g., per minute)
  - Reset counter at window boundary
  - If count > limit, reject
- **Pros**: 
  - Simple to implement
  - Low memory (just a counter)
- **Cons**: 
  - Burst at window boundaries (user can make 100 requests at 00:00:59 and 100 at 00:01:00)
  - Not smooth
- **Use Case**: Simple rate limiting, can tolerate boundary bursts

**Sliding Window**
- **How it Works**:
  - Track requests in sliding time window
  - Count requests in last N seconds (e.g., last 60 seconds)
  - If count > limit, reject
- **Implementation**: 
  - Use circular buffer or sorted list of timestamps
  - Remove old requests outside window
- **Pros**: 
  - Smooth rate limiting
  - No burst issues
  - More accurate
- **Cons**: 
  - More memory intensive (store timestamps)
  - More complex to implement
- **Use Case**: When you need accurate, smooth rate limiting

**Sliding Window Log**
- **How it Works**: Store timestamp of each request, count requests in window
- **Pros**: Most accurate
- **Cons**: High memory usage (store all timestamps)

**Sliding Window Counter**
- **How it Works**: Divide window into smaller sub-windows, approximate count
- **Pros**: Lower memory than log, more accurate than fixed window
- **Cons**: Slight approximation

**Rate Limiting Implementation Example**
```python
import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}  # user_id -> deque of timestamps
    
    def is_allowed(self, user_id):
        now = time.time()
        
        if user_id not in self.requests:
            self.requests[user_id] = deque()
        
        """ Remove old requests outside window """
        user_requests = self.requests[user_id]
        while user_requests and user_requests[0] < now - self.window_seconds:
            user_requests.popleft()
        
        """ Check if under limit """
        if len(user_requests) < self.max_requests:
            user_requests.append(now)
            return True
        return False
```

---

## **🔧 Core System Design Concepts**

Before diving into specific problems, let's understand the fundamental concepts that appear throughout system design interviews.

---

### **🌐 WebSockets vs HTTP**

**WebSockets**
- **What**: Full-duplex communication channel over a single TCP connection
- **When to use**: Real-time applications (chat, gaming, live updates)
- **Benefits**: 
  - Persistent connection (no need to reconnect)
  - Bidirectional communication (client ↔ server)
  - Lower latency than HTTP polling
- **Drawbacks**: 
  - More complex to implement
  - Connection management overhead
  - Firewall/proxy issues

**HTTP (REST)**
- **What**: Request-response protocol, stateless
- **When to use**: CRUD operations, API endpoints, traditional web apps
- **Benefits**: 
  - Simple, stateless, cacheable
  - Works everywhere (browsers, mobile, APIs)
  - Easy to scale horizontally
- **Drawbacks**: 
  - Higher latency for real-time updates
  - Server can't push to client
  - Overhead of repeated connections

**Decision Framework**:
- Use **WebSockets** for: Real-time updates, bidirectional communication, low latency
- Use **HTTP** for: CRUD operations, stateless APIs, simple request-response

---

### **🔢 Base62 vs Base64 Encoding**

**Base62 Encoding**
- **What**: Uses 62 characters: A-Z, a-z, 0-9 (no special characters)
- **When to use**: URL shorteners, human-readable IDs, file names
- **Benefits**: 
  - URL-safe (no encoding needed)
  - Human-readable and memorable
  - Shorter than Base64 for same data
- **Example**: `abc123` instead of `YWJjMTIz`

**Base64 Encoding**
- **What**: Uses 64 characters: A-Z, a-z, 0-9, +, / (with padding =)
- **When to use**: Binary data in text, email attachments, API responses
- **Benefits**: 
  - Standard encoding for binary data
  - Efficient for data transfer
  - Widely supported
- **Drawbacks**: 
  - Not URL-safe (requires encoding)
  - Padding characters can cause issues

**Why Base62 for URLs?**
- **URL Safety**: No special characters that need encoding
- **Human Readable**: Easier to type and remember
- **Shorter**: More compact representation
- **No Padding**: Clean URLs without = characters

---

### **⏰ TTL (Time To Live)**

**What is TTL?**
- **Definition**: How long data should be considered valid before expiring
- **Purpose**: Automatic cleanup, cache invalidation, data freshness

**Common TTL Use Cases**:
1. **Cache Expiration**: Redis keys, CDN content
2. **Session Management**: User sessions, authentication tokens
3. **Rate Limiting**: Reset counters after time window
4. **Data Freshness**: Stale data cleanup, temporary data

**TTL Strategies**:
- **Fixed TTL**: Same expiration for all items
- **Variable TTL**: Different expiration based on data type
- **Sliding TTL**: Reset timer on access
- **Exponential TTL**: Increase expiration with usage

**Example Implementation**:
```markdown
# Redis TTL example
redis.setex("user_session:123", 3600, session_data)  # Expires in 1 hour
redis.expire("cache_key", 300)  # Set TTL to 5 minutes
```

---

### **📨 Message Brokers**

**What is a Message Broker?**
- **Definition**: Middleware that handles communication between different parts of a system
- **Purpose**: Decouple services, handle async processing, ensure message delivery

**Popular Message Brokers**:

**Apache Kafka**
- **Use Case**: High-throughput event streaming, log aggregation
- **Benefits**: 
  - Extremely high throughput (millions of messages/second)
  - Persistent storage, fault-tolerant
  - Horizontal scaling
- **Drawbacks**: 
  - Complex setup, overkill for simple use cases
  - Higher latency than in-memory solutions

**RabbitMQ**
- **Use Case**: Traditional message queuing, complex routing
- **Benefits**: 
  - Rich routing capabilities
  - Easy to set up and use
  - Good for complex workflows
- **Drawbacks**: 
  - Lower throughput than Kafka
  - Less suitable for event streaming

**Redis Pub/Sub**
- **Use Case**: Simple real-time messaging, notifications
- **Benefits**: 
  - Simple to implement
  - Low latency
  - Good for real-time features
- **Drawbacks**: 
  - No persistence
  - No guaranteed delivery
  - Limited scalability

**When to Use Each**:
- **Kafka**: High-volume event streaming, data pipelines
- **RabbitMQ**: Complex message routing, reliable delivery
- **Redis**: Simple real-time features, notifications

---

### **🖥️ Server vs Client Architecture**

**Client-Server Model**:
```text
Client (Browser/Mobile) ←→ Server (Backend)
```

**Server Responsibilities**:
- **Business Logic**: Core application logic, data processing
- **Data Storage**: Database operations, file management
- **Authentication**: User verification, session management
- **API Endpoints**: REST/GraphQL interfaces
- **Security**: Input validation, rate limiting, authorization

**Client Responsibilities**:
- **User Interface**: UI rendering, user interactions
- **Data Display**: Presenting server data to users
- **Local State**: Form data, temporary storage
- **Network Requests**: API calls to server
- **Offline Handling**: Local caching, offline functionality

**Modern Variations**:
- **Single Page Application (SPA)**: Client handles routing, server provides APIs
- **Progressive Web App (PWA)**: Client can work offline, sync when online
- **Microservices**: Multiple specialized servers, client aggregates data

---

### **🔴 Redis (Remote Dictionary Server)**

**What is Redis?**
- **Definition**: In-memory data structure store, often used as cache
- **Key Feature**: Data stored in RAM for extremely fast access

**Redis Data Structures**:
1. **Strings**: Simple key-value pairs
```text
   redis.set("user:123", "John Doe")
   redis.get("user:123")  # Returns "John Doe"
```

2. **Hashes**: Field-value pairs within a key
```text
   redis.hset("user:123", "name", "John")
   redis.hset("user:123", "age", "30")
   redis.hgetall("user:123")  # Returns {"name": "John", "age": "30"}
```

3. **Lists**: Ordered collections
```text
   redis.lpush("queue", "task1")
   redis.rpop("queue")  # Returns "task1"
```

4. **Sets**: Unordered unique collections
```text
   redis.sadd("online_users", "user1")
   redis.sismember("online_users", "user1")  # Returns True
```

5. **Sorted Sets**: Ordered collections with scores
```text
   redis.zadd("leaderboard", {"player1": 100, "player2": 200})
   redis.zrevrange("leaderboard", 0, -1)  # Returns ["player2", "player1"]
```

**Redis Use Cases**:
- **Caching**: Store frequently accessed data
- **Session Storage**: User sessions, authentication
- **Rate Limiting**: Track request counts
- **Real-time Features**: Pub/Sub, live counters
- **Leaderboards**: Sorted sets for rankings

**Redis Trade-offs**:
- **Pros**: Extremely fast, rich data structures, persistence options
- **Cons**: Memory cost, single-threaded, limited by RAM size

---

### **🔒 Distributed Locks**

**What is a Distributed Lock?**
- **Definition**: Mechanism to ensure only one process can access a resource across multiple servers
- **Problem**: In distributed systems, multiple servers might try to access the same resource simultaneously

**Why Distributed Locks?**
- **Resource Contention**: Prevent multiple processes from modifying the same data
- **Race Conditions**: Ensure atomic operations across servers
- **Data Consistency**: Maintain integrity in distributed environments

**Implementation Strategies**:

**Redis-based Locks**:
```python
import redis
import time

def acquire_lock(lock_name, acquire_timeout=10, lock_timeout=10):
    """Acquire a distributed lock using Redis"""
    end = time.time() + acquire_timeout
    lock_value = str(time.time())
    
    while time.time() < end:
        if redis.set(lock_name, lock_value, ex=lock_timeout, nx=True):
            return lock_value
        time.sleep(0.001)
    return False

def release_lock(lock_name, lock_value):
    """Release a distributed lock"""
    script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    return redis.eval(script, 1, lock_name, lock_value)
```

**Zookeeper-based Locks**:
- **Use Case**: Complex coordination, leader election
- **Benefits**: Strong consistency, automatic cleanup
- **Drawbacks**: Higher latency, more complex setup

**Database-based Locks**:
- **Use Case**: Simple scenarios, when Redis isn't available
- **Benefits**: ACID guarantees, existing infrastructure
- **Drawbacks**: Higher latency, database load

**Lock Properties**:
- **Exclusivity**: Only one process holds the lock
- **Timeout**: Automatic expiration to prevent deadlocks
- **Reentrancy**: Same process can re-acquire lock
- **Fairness**: FIFO ordering of lock requests

---

### **🏗️ System Design Principles**

**1. Scalability**
- **Horizontal**: Add more servers (scale out)
- **Vertical**: Add more resources to existing servers (scale up)
- **Load Balancing**: Distribute traffic across multiple servers

**2. Availability**
- **Redundancy**: Multiple copies of critical components
- **Failover**: Automatic switching to backup systems
- **Health Checks**: Monitor system health and respond to failures

**3. Consistency**
- **Strong Consistency**: All reads see the latest write
- **Eventual Consistency**: Reads may see stale data temporarily
- **CAP Theorem**: Choose 2 out of 3: Consistency, Availability, Partition Tolerance

**4. Performance**
- **Latency**: Response time for individual requests
- **Throughput**: Number of requests handled per second
- **Caching**: Store frequently accessed data in fast storage

**5. Security**
- **Authentication**: Verify user identity
- **Authorization**: Control access to resources
- **Input Validation**: Prevent malicious input
- **Rate Limiting**: Prevent abuse

---

## 1. URL Shortener

**Requirements**
- Shorten long URLs to 6-8 character codes
- Redirect short URLs to original URLs
- Track click analytics
- Handle 100M+ URLs, 1000+ requests/second

**Design**
- **Short URL Generation**: Hash(long URL) → base62 encoding
- **Storage**: Redis for hot URLs, PostgreSQL for persistence
- **Database Schema**:
```text
  urls (id, short_code, long_url, user_id, created_at, expires_at)
  clicks (id, short_code, ip, user_agent, timestamp, referrer)
```
- **Key Decisions**: Use hash-based generation (not sequential), TTL for unused URLs

**Trade-offs**
- Hash collisions: Use longer codes or collision resolution
- Analytics: Real-time vs batch processing
- Storage: Keep all URLs vs TTL expiration

---

## 2. Chat Application

**Requirements**
- Real-time messaging between users
- Group chats, direct messages
- Message persistence
- Online/offline status
- Handle 1M+ concurrent users

**Design**
- **Real-time**: WebSocket connections, message broker (Redis Pub/Sub)
- **Storage**: Messages in PostgreSQL, user status in Redis
- **Scaling**: Shard by user_id, use read replicas
- **Architecture**:
```text
  Client → Load Balancer → WebSocket Server → Message Broker → Storage
```

**Trade-offs**
- Message ordering: Global vs per-chat ordering
- Persistence: All messages vs recent only
- Real-time: WebSocket vs Server-Sent Events vs Long Polling

---

## 3. Rate Limiter

**Requirements**
- Limit requests per user/IP
- Support different rate limits (per second, minute, hour)
- Handle distributed systems
- Configurable limits per endpoint

**Design**
- **Token Bucket**: Refill tokens at fixed rate, consume per request
- **Sliding Window**: Track requests in time windows
- **Implementation**: Redis with TTL, distributed locks
- **Storage**: Redis for counters, PostgreSQL for configuration

**Trade-offs**
- Accuracy: Fixed vs sliding windows
- Storage: In-memory vs distributed
- Granularity: Per-user vs per-IP vs per-endpoint

---

## 4. News Feed

**Requirements**
- Personalized feed for each user
- Real-time updates
- Handle 10M+ users, 1000+ posts/second
- Support different content types

**Design**
- **Fan-out on Write**: Pre-compute feeds when posts are created
- **Storage**: User feeds in Redis, posts in PostgreSQL
- **Scoring**: Time decay + engagement metrics
- **Architecture**:
```text
  Post → Fan-out Workers → User Feed Stores → Aggregation → Client
```

**Trade-offs**
- Fan-out: Write vs Read (write for normal users, read for celebrities)
- Feed generation: Real-time vs batch
- Storage: Keep all posts vs TTL expiration

---

## 5. File Storage System

**Requirements**
- Store files up to 1GB
- Support multiple file types
- Handle 1000+ uploads/second
- Global distribution
- Backup and redundancy

**Design**
- **Storage**: Object storage (S3), CDN for distribution
- **Metadata**: PostgreSQL for file info, Redis for caching
- **Upload**: Chunked uploads, resume capability
- **Architecture**:
```text
  Client → Load Balancer → Upload Service → Object Storage → CDN
```

**Trade-offs**
- Consistency: Strong vs eventual
- Storage: Hot vs cold storage tiers
- Backup: Synchronous vs asynchronous replication

---

## 6. Ride Hailing System

**Requirements**
- Match riders with drivers
- Real-time location tracking
- Handle 100K+ concurrent rides
- Support surge pricing
- Payment processing

**Design**
- **Matching**: Geospatial indexing (R-tree), real-time location updates
- **Storage**: PostgreSQL for rides, Redis for active sessions
- **Scaling**: Shard by geographic regions
- **Architecture**:
```text
  Location Updates → Matching Engine → Driver Assignment → Payment
```

**Trade-offs**
- Matching: Real-time vs batch processing
- Location: GPS accuracy vs battery life
- Pricing: Dynamic vs fixed pricing

---

## 7. Notification System

**Requirements**
- Send notifications via email, SMS, push
- Support different notification types
- Handle 1M+ notifications/hour
- Delivery tracking
- Template management

**Design**
- **Queue**: Message broker (RabbitMQ/Kafka) for async processing
- **Templates**: Jinja2/Mustache for dynamic content
- **Delivery**: Multiple providers for redundancy
- **Storage**: PostgreSQL for templates, Redis for delivery status

**Trade-offs**
- Delivery: Synchronous vs asynchronous
- Providers: Single vs multiple for redundancy
- Templates: Dynamic vs static generation

---

## 8. Real-time Analytics

**Requirements**
- Track user events in real-time
- Support complex aggregations
- Handle 100K+ events/second
- Low-latency queries
- Historical data retention

**Design**
- **Streaming**: Apache Kafka for event ingestion
- **Processing**: Apache Flink/Spark for real-time aggregation
- **Storage**: Time-series database (InfluxDB), data warehouse
- **Architecture**:
```text
  Events → Kafka → Stream Processor → Real-time Store → Query API
```

**Trade-offs**
- Latency: Real-time vs near-real-time
- Storage: Raw events vs pre-aggregated
- Processing: Stream vs batch processing

---

## 9. Feature Flags

**Requirements**
- Enable/disable features dynamically
- Support A/B testing
- Handle 10M+ requests/second
- Real-time configuration updates
- Audit trail

**Design**
- **Storage**: Redis for fast lookups, PostgreSQL for configuration
- **Distribution**: Pub/Sub for real-time updates
- **Evaluation**: Client-side vs server-side evaluation
- **Architecture**:
```text
  Config Changes → Pub/Sub → Feature Service → Client Evaluation
```

**Trade-offs**
- Evaluation: Client vs server-side
- Storage: In-memory vs distributed
- Updates: Real-time vs eventual consistency

---

## 10. Video Streaming Platform

**Requirements**
- Stream videos in multiple qualities
- Support live and on-demand content
- Handle 1M+ concurrent viewers
- Global distribution
- Content recommendation

**Design**
- **Encoding**: Multiple bitrates, adaptive streaming (HLS/DASH)
- **Storage**: Object storage for video files, CDN for distribution
- **Streaming**: Edge servers, adaptive bitrate selection
- **Architecture**:
```text
  Video Upload → Encoding → Storage → CDN → Client Player
```

**Trade-offs**
- Quality: Multiple bitrates vs single quality
- Storage: Hot vs cold storage
- Distribution: Global vs regional CDNs

---

## 11. Search Autocomplete

**Requirements**
- Suggest search terms as user types
- Support multiple languages
- Handle 10K+ requests/second
- Fast response (<100ms)
- Personalized suggestions

**Design**
- **Data Structure**: Trie for prefix matching
- **Storage**: In-memory for fast access, Redis for persistence
- **Scoring**: Frequency + recency + personalization
- **Architecture**:
```text
  Query → Trie Lookup → Scoring → Personalization → Response
```

**Trade-offs**
- Accuracy: Global vs personalized suggestions
- Storage: In-memory vs distributed
- Updates: Real-time vs batch updates

---

## 12. API Gateway

**Requirements**
- Route requests to appropriate services
- Handle authentication/authorization
- Rate limiting and throttling
- Request/response transformation
- Load balancing

**Design**
- **Routing**: Path-based routing, service discovery
- **Security**: JWT validation, API key management
- **Scaling**: Horizontal scaling, health checks
- **Architecture**:
```text
  Client → API Gateway → Authentication → Rate Limiter → Service Router
```

**Trade-offs**
- Security: Centralized vs distributed
- Routing: Static vs dynamic configuration
- Scaling: Monolithic vs microservices

---

## Common Patterns & Snippets

### Idempotent Endpoint
```python
def process_request(request_id, data):
    if processed(request_id):
        return get_stored_result(request_id)
    
    result = execute_business_logic(data)
    store_result(request_id, result)
    return result
```

### Retry with Jitter
```python
import random
import time

def retry_with_jitter(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
```

### Outbox Pattern
```python
def process_order(order_data):
    with transaction():
        """ Business logic """
        order = create_order(order_data)
        
        """ Store event in outbox """
        outbox_event = OutboxEvent(
            event_type="order_created",
            payload=order.to_dict(),
            status="pending"
        )
        db.session.add(outbox_event)
        db.session.commit()

# Background worker processes outbox
def process_outbox():
    events = OutboxEvent.query.filter_by(status="pending").limit(100)
    for event in events:
        publish_event(event.payload)
        event.status = "sent"
        db.session.commit()
```

---

## Design Decision Framework

### 1. Functional Requirements
- What does the system need to do?
- What are the input/output formats?
- What are the business rules?

### 2. Non-Functional Requirements
- **Scalability**: How many users/requests?
- **Performance**: Response time, throughput?
- **Availability**: Uptime requirements?
- **Consistency**: Data consistency needs?

### 3. Constraints
- **Technical**: Technology stack, team expertise
- **Business**: Budget, timeline, compliance
- **Operational**: Monitoring, maintenance, support

### 4. Trade-offs Analysis
- **Performance vs Scalability**: Optimize for speed vs growth
- **Consistency vs Availability**: CAP theorem choices
- **Complexity vs Maintainability**: Simple vs robust solutions

### 5. Estimation
- **Storage**: Data size, growth rate
- **Bandwidth**: Request/response sizes
- **Compute**: CPU/memory requirements
- **Cost**: Infrastructure and operational costs
