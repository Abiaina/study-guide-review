---
title: System Design Problems
---

# System Design Problems

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
```python
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
```
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
   ```python
   redis.set("user:123", "John Doe")
   redis.get("user:123")  # Returns "John Doe"
   ```

2. **Hashes**: Field-value pairs within a key
   ```python
   redis.hset("user:123", "name", "John")
   redis.hset("user:123", "age", "30")
   redis.hgetall("user:123")  # Returns {"name": "John", "age": "30"}
   ```

3. **Lists**: Ordered collections
   ```python
   redis.lpush("queue", "task1")
   redis.rpop("queue")  # Returns "task1"
   ```

4. **Sets**: Unordered unique collections
   ```python
   redis.sadd("online_users", "user1")
   redis.sismember("online_users", "user1")  # Returns True
   ```

5. **Sorted Sets**: Ordered collections with scores
   ```python
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
  ```sql
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
  ```
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
  ```
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
  ```
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
  ```
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
  ```
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
  ```
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
  ```
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
  ```
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
  ```
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
        # Business logic
        order = create_order(order_data)
        
        # Store event in outbox
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
