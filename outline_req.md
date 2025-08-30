
# Detailed Outline for the Study Workbook

## Part 1: Algorithms & Data Structures

**Core Python Structures**

* **Lists (arrays in Python)**:

  * Methods: append, insert, pop, del, slicing, reverse, sort.
  * Complexity table.
  * Example: iterate, add, delete, sort.
* **Strings**:

  * Properties: immutable.
  * Methods: split, join, find, replace, strip.
  * Notes: slicing copies, concatenation cost, Counter for frequency.
* **Dictionaries (hash maps)**:

  * Methods: keys, values, items, get, setdefault, defaultdict, Counter.
  * Examples: add, remove, traverse, “sort” by key/value.
* **Sets**:

  * Methods: add, remove, union, intersection, difference, symmetric diff.
  * Examples: membership test, sorted view, frozenset.

**Other Data Structures**

* **Stacks & Queues**: `list`, `deque`, `queue`, O(1) ops.
* **Heaps/Priority Queues**: `heapq` min-heap, max-heap via negatives, top-K pattern.
* **Trees**:

  * Traversals (pre/in/post/level order).
  * Examples: insert, delete, search in BST.
  * Utilities: max depth, balance check.
* **Graphs**:

  * Adjacency list/matrix.
  * BFS, DFS (templates).
  * Topological sort.

**Algorithm Categories**

* **Sorting**: Quicksort, Mergesort, Heapsort, Timsort (with table).
* **Searching**: Binary search templates (leftmost/rightmost).
* **Sliding Window**: Fixed-size and variable-size templates.
* **Dynamic Programming**: Top-down vs bottom-up; examples (climbing stairs, coin change, edit distance, LIS, knapsack).
* **Greedy**: Interval scheduling, Jump Game II, Kruskal’s MST, Huffman coding.

---

## Part 2: Data Layer

* **CAP theorem** (CA/CP/AP, tunable consistency).
* **ACID vs BASE**.
* **Database types**: relational, key-value, doc store, columnar, graph. Include CAP stance.
* **Indexing strategies**: B-tree, hash, covering, GIN/GiST.
* **Normalization vs Denormalization**.
* **Replication & Sharding**: sync/async, leader-follower, hash/range sharding.
* **Caching**: cache-aside, read/write-through, write-back.
* **Data pipelines for AI/ML**:

  * Raw → staging → clean/normalized → feature store → model training.
  * Streaming vs batch ingestion.
  * Tools: Spark, Kafka, Airflow.

---

## Part 3: DevOps & Cloud

* **Infrastructure as Code**: Terraform multi-resource example (VPC, EC2, S3).
* **CI/CD**: Jenkinsfile example, GitHub Actions, GitLab.
* **Containers**:

  * Docker multi-stage builds, Docker vs Podman vs containerd.
  * Orchestration: Kubernetes manifests (Deployment, Service, Ingress).
* **Observability**:

  * Logs: Splunk, ELK, Loki.
  * Metrics: Prometheus, Datadog, CloudWatch.
  * Traces: OpenTelemetry, Jaeger.
  * Visualization: Grafana.
* **Security & Compliance**:

  * HIPAA rules: PHI/PII definitions, BAA, encryption at rest/in transit, access control, audit logs.
  * Tools: Snyk, Trivy, Vault/Secrets Manager.

---

## Part 4: Chaos Engineering & Resiliency

* **Principles**: steady state, blast radius, rollback, kill switch.
* **Fault types**: compute, network, storage, dependencies, AZ/region.
* **Workflows**: LitmusChaos CRDs, Gremlin CLI, Steadybit CI/CD integration.
* **Historical incidents**: Netflix, AWS S3 2017, GCP 2019, Dyn DNS 2016, Facebook BGP 2021, Ticketmaster–Taylor Swift 2022.
* **Chaos Tools Comparison table**.
* **Resiliency patterns**: circuit breakers, retries with backoff + jitter, bulkheads, fallbacks, idempotency.

---

## Part 5: System Design Appendix

* **Load balancing**: round robin, least connections, consistent hashing.
* **Caching tiers**: client, CDN, app, DB.
* **Queues & Pub/Sub**: delivery semantics (at-least/at-most/exactly once), DLQs, idempotency keys.
* **Eventual consistency**: read-repair, session consistency, CRDTs.
* **SLIs/SLOs/SLAs + error budgets**.
* **Reliability guards**: timeouts, circuit breakers, bulkheads.

---

## Part 6: System Design Deep Dives

* **Storage scaling**: event sourcing, CQRS, materialized views, outbox, sagas.
* **Case studies**:

  * Twitter timeline: fanout read vs write.
  * YouTube: upload → transcode → CDN.
  * E-commerce checkout: cart/inventory/payment saga.

---

## Part 7: System Design Problems

* **12 classic problems**: URL shortener, chat app, rate limiter, newsfeed, file storage, ride hailing, notification system, real-time analytics, feature flags, video streaming, search autocomplete, API gateway.
* **Snippets**: idempotent endpoint, retry with jitter, outbox relay.

---

## Part 8: Final 1-Page Cheat Sheet

* **Cross-structure methods table** (lists, strings, dicts, sets, heaps, queues).
* **Big-O quick table** (insert/delete/lookup by structure).
* **Algorithm skeletons**: recursion, DFS/BFS, binary search, sliding window, Dijkstra, DP template.
* **Python reminders**: strings immutable, slicing makes copy, Timsort is stable, dict/set membership O(1), list insert O(n).
* **Common libraries**:

  * `collections`: Counter, defaultdict, deque.
  * `heapq`, `bisect`.
  * `functools`: lru\_cache.
  * `itertools`: combinations, permutations, product.

---