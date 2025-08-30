---
title: System Design Problems
---

# System Design Problems

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
