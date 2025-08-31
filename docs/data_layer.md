---
title: Data Layer
---

# Data Layer & Databases

## **📚 Database Fundamentals & Definitions**

Before diving into advanced concepts, let's understand the fundamental database types and terminology.

---

### **🗄️ SQL vs NoSQL: What Are They?**

**SQL (Structured Query Language)**
- **What**: Standard language for managing relational databases
- **Definition**: A programming language designed for managing and querying data in relational database management systems (RDBMS)
- **Key Characteristics**: 
  - Structured, tabular data with predefined schemas
  - ACID compliance for data integrity
  - Strong consistency guarantees
  - Complex queries with JOINs and transactions

**NoSQL (Not Only SQL)**
- **What**: Non-relational database systems designed for specific data models
- **Definition**: Database systems that store and retrieve data in non-tabular form, often optimized for specific use cases
- **Key Characteristics**:
  - Flexible schemas that can evolve over time
  - Often sacrifice ACID for performance and scalability
  - Designed for horizontal scaling
  - Specialized for specific data patterns

---

### **🏗️ Database Categories Explained**

#### **1. Relational Databases (SQL)**
**What They Are**: Databases that organize data into tables with rows and columns, where relationships between data are defined by foreign keys.

**Core Concepts**:
- **Tables**: Collections of related data (e.g., users, orders, products)
- **Rows**: Individual records in a table
- **Columns**: Attributes or fields for each record
- **Relationships**: Connections between tables using foreign keys
- **Schema**: The structure that defines tables, columns, and relationships

**Examples**: PostgreSQL, MySQL, Oracle, SQL Server, SQLite

**When to Use**:
- ✅ **Structured data** with clear relationships
- ✅ **ACID compliance** required (banking, financial systems)
- ✅ **Complex queries** with JOINs and aggregations
- ✅ **Data integrity** is critical
- ❌ **Rapid schema changes** needed
- ❌ **Massive horizontal scaling** required

#### **2. Key-Value Stores (NoSQL)**
**What They Are**: Simple databases that store data as key-value pairs, where each key maps to a single value.

**Core Concepts**:
- **Key**: Unique identifier (usually a string)
- **Value**: Data associated with the key (can be simple or complex)
- **No Schema**: Values can be any type without predefined structure
- **Fast Lookups**: O(1) average time complexity for key-based access

**Examples**: Redis, DynamoDB, Riak, Memcached

**When to Use**:
- ✅ **Simple data models** (user sessions, caching)
- ✅ **High-performance lookups** by key
- ✅ **Session storage** and temporary data
- ✅ **Real-time counters** and simple state
- ❌ **Complex queries** or relationships
- ❌ **Data that needs** complex aggregations

#### **3. Document Databases (NoSQL)**
**What They Are**: Databases that store data in flexible, JSON-like documents that can have different structures.

**Core Concepts**:
- **Documents**: Self-contained data units (usually JSON/BSON)
- **Collections**: Groups of related documents
- **Embedded Data**: Related information can be nested within documents
- **Schema Flexibility**: Documents can have different fields and structures

**Examples**: MongoDB, Couchbase, CouchDB, Firestore

**When to Use**:
- ✅ **Flexible schemas** that evolve over time
- ✅ **Hierarchical data** (nested objects, arrays)
- ✅ **Content management** systems
- ✅ **Product catalogs** with varying attributes
- ❌ **Complex transactions** across documents
- ❌ **Data with many relationships** between entities

#### **4. Column-Family Stores (NoSQL)**
**What They Are**: Databases that store data in columns rather than rows, optimized for reading and writing large amounts of data.

**Core Concepts**:
- **Column Families**: Groups of related columns
- **Wide Rows**: Each row can have many columns
- **Column-Oriented**: Data is stored by column, not by row
- **Time-Series Friendly**: Excellent for data that changes over time

**Examples**: Cassandra, HBase, Bigtable, ScyllaDB

**When to Use**:
- ✅ **Time-series data** (logs, metrics, IoT data)
- ✅ **High write throughput** requirements
- ✅ **Analytics and reporting** workloads
- ✅ **Data warehousing** and large-scale storage
- ❌ **Complex transactions** or relationships
- ❌ **Frequent schema changes**

#### **5. Graph Databases (NoSQL)**
**What They Are**: Databases designed to store and query relationships between entities, treating relationships as first-class citizens.

**Core Concepts**:
- **Nodes**: Entities or objects in the graph
- **Edges**: Relationships between nodes
- **Properties**: Attributes stored on both nodes and edges
- **Traversals**: Navigation through connected data

**Examples**: Neo4j, ArangoDB, Amazon Neptune, OrientDB

**When to Use**:
- ✅ **Complex relationships** between entities
- ✅ **Social networks** and recommendation engines
- ✅ **Fraud detection** and network analysis
- ✅ **Knowledge graphs** and semantic search
- ❌ **Simple CRUD operations** without relationships
- ❌ **Traditional reporting** and analytics

#### **6. Search Engines (Specialized NoSQL)**
**What They Are**: Databases optimized for full-text search, complex queries, and text-based analytics.

**Core Concepts**:
- **Inverted Indexes**: Maps terms to documents containing them
- **Text Analysis**: Tokenization, stemming, and language processing
- **Scoring**: Relevance ranking for search results
- **Aggregations**: Complex analytics on search results

**Examples**: Elasticsearch, OpenSearch, Solr, Algolia

**When to Use**:
- ✅ **Full-text search** requirements
- ✅ **Log analysis** and monitoring
- ✅ **Content search** and discovery
- ✅ **Real-time analytics** on text data
- ❌ **Primary data storage** (use as secondary)
- ❌ **ACID transactions** or strong consistency

---

### **🔄 ACID vs BASE: Transaction Models**

#### **ACID (Traditional SQL)**
**Atomicity**: All operations in a transaction succeed or fail together
**Consistency**: Data moves from one valid state to another
**Isolation**: Concurrent transactions don't interfere with each other
**Durability**: Committed changes survive system failures

**Use Cases**: Banking, financial systems, inventory management, any system where data integrity is critical

#### **BASE (Common in NoSQL)**
**Basically Available**: System guarantees availability over consistency
**Soft State**: Data may change over time due to eventual consistency
**Eventual Consistency**: System will become consistent over time if no new updates occur

**Use Cases**: Social media, content management, real-time analytics, systems where availability is more important than immediate consistency

---

### **📊 CAP Theorem: The Fundamental Trade-off**

**What is CAP Theorem?**
In distributed database systems, you can only guarantee **2 out of 3** properties:

1. **Consistency (C)**: All nodes see the same data at the same time
2. **Availability (A)**: Every request receives a response
3. **Partition Tolerance (P)**: System continues operating despite network failures

**Real-World Implications**:
- **CP Systems**: Choose consistency over availability (banking, financial)
- **AP Systems**: Choose availability over consistency (social media, content)
- **CA Systems**: Only possible in single-node systems (not truly distributed)

---

## 1. Key Theoretical Foundations

### **CAP Theorem**

- A distributed database can only guarantee **two** out of three:

  - **Consistency (C):** every read returns the latest write.
  - **Availability (A):** every request receives a response (even if not the latest).
  - **Partition Tolerance (P):** system continues despite dropped/delayed messages.

**Tradeoffs:**

- **CP (Consistency + Partition Tolerance):** strict correctness, lower availability → banking, financial systems.
- **AP (Availability + Partition Tolerance):** eventual consistency, high availability → social media, caching layers.
- **CA (Consistency + Availability):** only realistic in single-node or non-partitioned systems.

---

### **ACID Transactions**

- **Atomicity** → All or nothing (no partial writes).
- **Consistency** → Data moves from one valid state to another.
- **Isolation** → Transactions don’t interfere with each other.
- **Durability** → Committed changes survive crashes.

**Example (Bank Transfer):**

```
begin transaction
    debit Alice $100
    credit Bob $100
commit
```

If the system crashes mid-way, rollback ensures no partial transfer.

---

### **BASE Model** (common in NoSQL)

- **Basically Available:** system guarantees availability.
- **Soft state:** data may change over time (due to eventual consistency).
- **Eventual consistency:** if no updates occur, replicas converge.

---

## 2. Database Types & Design Choices

| Type                 | Example Systems            | Strengths                                             | Limitations                                   | When to Use                                     |
| -------------------- | -------------------------- | ----------------------------------------------------- | --------------------------------------------- | ----------------------------------------------- |
| **Relational (SQL)** | PostgreSQL, MySQL, Oracle  | Strong consistency, ACID, rich queries (SQL, joins)   | Harder to scale horizontally, schema rigidity | Banking, ERP, analytics with strong correctness |
| **Key-Value**        | Redis, DynamoDB, Riak      | Very fast lookups, simple model                       | No joins, limited query flexibility           | Caching, session stores, user profiles          |
| **Document**         | MongoDB, Couchbase         | Flexible schema, hierarchical docs                    | Joins are weak, eventual consistency common   | CMS, product catalogs, flexible JSON data       |
| **Columnar**         | Cassandra, HBase, Bigtable | Wide-column storage, great for writes and time series | Complex setup, weaker joins                   | Logging, time series, IoT data                  |
| **Graph**            | Neo4j, ArangoDB            | Optimized for relationships (edges)                   | Slower for non-graph workloads                | Social networks, recommendation engines         |

---

## 3. Core Database Concepts

### Indexing

- **B-Tree indexes:** balanced, efficient for range queries.
- **Hash indexes:** O(1) lookups but poor for ranges.
- **Covering indexes:** include all queried columns → avoid table lookups.
- **Tradeoff:** faster reads but slower writes (maintaining index).

### Normalization vs Denormalization

- **Normalization:** reduce redundancy (3NF/BCNF), consistent updates, smaller storage.
- **Denormalization:** duplicate data for faster queries, common in OLAP/NoSQL.

### Scaling Approaches

- **Replication:** copies of data for HA/reads.
- **Sharding:** horizontal partitioning across servers.
- **Caching:** use Redis/Memcached to reduce DB load.
- **Event sourcing / CQRS:** separate read vs write models.

---

## 4. Patterns in System Design Interviews

- **Use SQL** when correctness, transactions, and structured queries matter.
- **Use NoSQL (KV/Doc/Column)** when availability, scale, and flexibility matter.
- **Mix approaches:** e.g., use PostgreSQL for core financial records, Redis for session caching, ElasticSearch for logs/queries.

---

| Type                                  | Example Systems                                           | **CAP Posture (typical)**                          | Strengths                                                               | Limitations                                                             | Common Uses                                             |
| ------------------------------------- | --------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------- |
| **Relational (SQL)**                  | PostgreSQL, MySQL (single-node)                           | **CA\***                                           | Strong consistency on a single node, ACID, rich SQL/joins               | Vertical scaling limits; schema rigidity                                | OLTP, finance, ERP, analytics where correctness matters |
| **Relational (clustered/replicated)** | Postgres w/ sync replicas, Galera/MySQL Group Replication | **CP (sync quorum)** / **AP-ish (async replicas)** | ACID with high correctness; can survive node loss with quorum           | May refuse writes under partition (CP); async replicas risk stale reads | High-integrity systems needing HA                       |
| **Key–Value**                         | **DynamoDB**                                              | **AP (tunable)**                                   | Massive scale, predictable latency; eventual or strong reads selectable | Limited querying/joins; modeling discipline needed                      | Caching, user profiles, session stores                  |
|                                       | **Redis (standalone)**                                    | **CA\***                                           | Extremely fast, simple; great cache                                     | Single-node unless clustered; no durability by default                  | Caching, rate limiting, queues                          |
|                                       | **Redis Cluster**                                         | **AP (tunable)**                                   | Scales horizontally, high throughput                                    | Eventual consistency windows; key-hash slotting constraints             | Distributed cache, pub/sub                              |
| **Document**                          | **MongoDB (replica set)**                                 | **CP (tunable)**                                   | Flexible schema (JSON/BSON), rich queries & indexes                     | Cross-document transactions newer/limited by design                     | Content mgmt, product catalogs                          |
| **Wide-Column**                       | **Cassandra**                                             | **AP**                                             | Writes-first design, linear scalability, multi-DC friendly              | Eventual consistency; complex data modeling                             | Time-series, logging, large-scale writes                |
|                                       | **HBase / Bigtable**                                      | **CP**                                             | Strong consistency, huge tables, range scans                            | Operationally heavier; limited ad-hoc queries                           | Analytics backends, large KV/range workloads            |
| **Search**                            | Elasticsearch, OpenSearch                                 | **AP (tunable)**                                   | Full-text search, aggregations, near-real-time                          | Eventual consistency; not a primary source of truth                     | Search, logs, analytics                                 |
| **Graph**                             | Neo4j, ArangoDB                                           | **CA\*** (single-node) / **CP (cluster)**          | Efficient traversals, relationship-heavy queries                        | Not ideal for wide scans/OLAP                                           | Social graphs, recommendations                          |

\* **CA** is only meaningful when there’s effectively **no partition** (e.g., single-node or same-box). In real distributed settings you must pick between **CP** and **AP** under partitions.
**Tunable** = posture can be adjusted (e.g., quorum reads/writes, read/write concerns).

If you want, I can drop this directly into the Data Layer section and keep going with **indexing strategies, normalization vs. denormalization, replication vs. sharding, and caching**—all in the same reference style.

# Indexing Strategies

### What is an index?

A secondary data structure that lets the database find rows **without scanning the whole table**.

### Common Index Types

| Index              | Best For                                                | Notes                                                           |
| ------------------ | ------------------------------------------------------- | --------------------------------------------------------------- |
| **B-Tree**         | Range scans, ordering (`BETWEEN`, `<`, `>`, `ORDER BY`) | Default in most RDBMS; balanced tree keeps O(log n) lookups     |
| **Hash**           | Exact matches (`=`)                                     | No range scans; O(1) average lookups                            |
| **GIN / GIST**     | Full-text, arrays, geo                                  | Postgres: GIN for inverted (contains), GiST for spatial/nearest |
| **Bitmap**         | Low-cardinality columns                                 | Often used in data warehouses for analytics                     |
| **Covering Index** | Query can be answered by the index alone                | Add **included** columns so base table lookup is avoided        |

### General Rules

- Index **what you filter on**, not what you select.
- **Equality first**, then range: compound indexes should match query predicates’ order (e.g., `WHERE a = ? AND b = ? AND c > ?` → index `(a, b, c)`).
- **High cardinality** columns benefit more (e.g., user_id > gender).
- Too many indexes **slow writes** (each insert/update must update indexes).

### SQL Snippets (PostgreSQL-flavored)

```sql
-- B-Tree (default)
CREATE INDEX idx_users_email ON users(email);

-- Composite index (equality, equality, then range)
CREATE INDEX idx_orders_user_date ON orders(user_id, status, created_at);

-- Partial index (only for active rows)
CREATE INDEX idx_active_users_email ON users(email) WHERE is_active = true;

-- Covering index (include extra columns)
CREATE INDEX idx_orders_lookup ON orders(order_id) INCLUDE (total_amount, status);

-- Full-text (GIN)
CREATE INDEX idx_docs_ft ON docs USING GIN (to_tsvector('english', body));
```

**Gotchas**

- **Leading column** matters in composite indexes. Query must use the leftmost parts to benefit.
- **Function indexes** require the query to use the same function (`LOWER(email)`).
- **Selectivity**: Indexes on low-selectivity columns (e.g., boolean) rarely help.

---

# Normalization vs Denormalization

### Normalization (3NF+)

- **Goal:** eliminate redundancy, maintain consistency.
- **Pros:** smaller data, consistent updates, fewer anomalies.
- **Cons:** more joins; sometimes slower reads.

### Denormalization

- **Goal:** speed reads by duplicating/aggregating data.
- **Pros:** fewer joins, faster read queries.
- **Cons:** write complexity; need **fan-out updates** or **background jobs** to keep in sync.

### When to Use

- **OLTP systems** (high write correctness): normalize first; denormalize selectively with materialized views/caches.
- **OLAP / analytics**: star/snowflake schemas, aggressive denormalization for read speed.

**Pattern**: Start normalized → measure → denormalize **targeted hot paths**.

---

# Replication vs Sharding

### Replication (Copy the same data to multiple nodes)

- **Synchronous:** writes wait for replicas → **CP** flavor (lower availability if replicas unreachable, but consistent).
- **Asynchronous:** leader commits and returns → **AP-ish** (stale reads possible).
- **Use for:** high availability (HA), read scaling (read replicas), DR.

**Terms**

- **Leader-Follower** (Primary-Replica)
- **Multi-leader** (conflict resolution needed)
- **Quorum** (R/W majority votes; tunable consistency)

**Example Read Scaling**

- Send writes to **leader**; send heavy reports to **read replicas**.

### Sharding (Horizontal partitioning; split data across nodes)

- **Key-based** (hash user_id) → even distribution, but hard to do cross-shard joins.
- **Range-based** (by date/id range) → easy range scans, risk hot shards.
- **Directory/Lookup** (custom routing service) → flexible, operationally complex.

**When to Shard**

- Dataset won’t fit on a single node / vertical scaling exhausted.
- Single-node write throughput maxed out.

**Cross-shard Challenges**

- **Joins**: push down computations or pre-aggregate.
- **Transactions**: need 2PC/sagas; prefer **idempotent** operations.
- **Rebalancing**: plan for adding shards (consistent hashing helps).

---

# Caching (and Layers)

### Why Cache?

Reduce latency and database load by serving hot data from memory.

### Types of Caches

| Layer                 | Example                  | Pros                   | Cons                          |
| --------------------- | ------------------------ | ---------------------- | ----------------------------- |
| **Client-side**       | Browser cache            | Zero network hops      | Stale control limited         |
| **CDN/Edge**          | CloudFront, Fastly       | Global low-latency     | Purge/invalidation needed     |
| **Application cache** | In-process LRU           | Ultra fast             | Memory pressure; not shared   |
| **Distributed cache** | Redis, Memcached         | Shared across services | Network hop; consistency risk |
| **Database cache**    | Buffer pool, query cache | Transparent            | DB-specific behavior          |

### Caching Strategies

- **Cache-aside (lazy):** app reads cache, on miss load DB then write cache.

  - Simple; stale possible until TTL expires.

- **Write-through:** write to cache and DB simultaneously.

  - Safer reads; writes slower.

- **Write-back:** write to cache, flush to DB later.

  - Fast writes; risk data loss without durability.

- **Read-through:** cache sits in front of DB transparently.

  - Managed by cache layer/provider.

### Redis Patterns

```python
# Cache-aside (pseudo/Python)
value = redis.get(key)
if value is None:
    value = db.read(key)
    redis.setex(key, ttl_seconds, serialize(value))
return value
```

**Invalidation**

- TTLs on keys, **versioned keys** (`user:123:v42`) to avoid thundering herds.
- **Pub/Sub** or **streams** to broadcast invalidations on updates.

**Gotchas**

- **Stale reads** (eventual consistency).
- **Hot keys** (use sharding or probabilistic caching).
- **Stampede**: use **singleflight**/locks or **randomized TTL** to spread expiries.

---

# Putting It Together — Quick Decision Guide

- **Need strict correctness & joins?** Start with **PostgreSQL** (normalized).
- **Read-heavy & scale-out?** Add **read replicas** (async replication).
- **Global latency?** Add **CDN/edge** and regional **caches** (Redis).
- **Write throughput wall / dataset too large?** **Shard** by user or time.
- **Slow queries?** Add **indexes** (B-Tree for ranges; composite for equality+range; GIN for text/arrays).
- **Analytics?** Denormalize into **warehouse** (star schema) or use **columnar** stores.

---

If you want, I can now fold these sections into your master document and then move on to the **DevOps & Cloud** chapter (Terraform/IaC with CLI & examples, AWS/Azure/GCP core services, CI/CD including Jenkins, Observability with CloudWatch/Splunk/New Relic, Chaos Engineering tools, Containers beyond Docker, Security/HIPAA).
