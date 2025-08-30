---
title: Chaos Engineering & Resiliency
---

# Chaos Engineering & Resiliency

## 1. Principles of Chaos Engineering

- **Define steady state** → measurable normal condition (e.g., “95% of requests < 200ms”).
- **Hypothesize** → predict what should happen under a failure.
- **Inject faults** → simulate failure in a controlled way (kill instances, add latency, cut network).
- **Observe** → measure whether steady state holds.
- **Minimize blast radius** → start in staging or a small slice of prod.
- **Automate rollback** → make failure reversible.

---

## 2. Core Practices

- **Game days** → scheduled failure drills with teams.
- **Fault injection testing (FIT)** → deliberate perturbations.
- **Chaos experiments in CI/CD** → inject faults during integration tests.
- **Resiliency KPIs**: MTTR, error budget burn, % of auto-recovered failures.

---

## 3. Common Faults to Simulate

- **Compute**: kill random VM/pod; simulate resource starvation.
- **Network**: latency injection, packet loss, partition a service.
- **Storage**: I/O throttling, disk full.
- **Dependencies**: force external API to error or slow.
- **Region failure**: simulate cloud AZ/region outage.

---

## 4. Tools & Ecosystem

### Service-level chaos

- **Gremlin** → SaaS, rich attacks (CPU, memory, network, shutdown).
- **AWS FIS** (Fault Injection Simulator) → native AWS tool.
- **Chaos Monkey** → Netflix OSS, randomly kills instances.

### Kubernetes-native

- **Chaos Mesh** (CNCF) → CRDs for chaos experiments.
- **LitmusChaos** → declarative chaos workflows.
- **Steadybit** → commercial, visual chaos injection for K8s.

### Pipeline-integrated

- **Harness Chaos Engineering** → tie experiments to CI/CD gates.
- **Argo Rollouts + chaos hooks** → progressive delivery with chaos tests.

---

## 5. Patterns for Resiliency

**Circuit breakers**

- Prevent cascading failures when a dependency is unhealthy.

**Retries with backoff**

- Retry transient failures, but with exponential backoff + jitter.

**Bulkheads**

- Partition threadpools/connection pools → noisy neighbors isolated.

**Fallbacks**

- Return degraded response (cached data, stubbed value) instead of full failure.

**Idempotency**

- Required under retries / at-least-once messaging.

---

## 6. Example Chaos Experiments

**Pod kill experiment (K8s, LitmusChaos)**

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: pod-kill-exp
spec:
  appinfo:
    appns: default
    applabel: app=example-svc
    appkind: deployment
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "60"
```

**Network latency (Gremlin CLI)**

```bash
gremlin attack latency --length 120 --latency 300 --hosts app1
```

**AWS FIS: Terminate random EC2 in ASG**

```json
{
  "description": "Terminate 1 EC2 instance",
  "targets": {
    "Instances": {
      "resourceType": "aws:ec2:instance",
      "resourceTags": { "ChaosTest": "true" }
    }
  },
  "actions": {
    "terminate": {
      "actionId": "aws:ec2:terminate-instances",
      "parameters": { "force": "false" },
      "targets": { "Instances": "Instances" }
    }
  }
}
```

---

## 7. Linking to SLOs

- Chaos is not just for fun → validate your **SLOs** (availability, latency).
- Example: If SLO is 99.9% availability, chaos experiments should show that the system **self-heals** under single-node failure without dropping below that.

---

✅ This now makes the Chaos/Resiliency section just as detailed as the Terraform/Jenkins/Observability sections.

Would you like me to **bundle Chaos Engineering + Observability into the DevOps & Cloud chapter** of your workbook now, or keep them as standalone chapters so they’re easy to flip to during review?

# 📘 Chaos Engineering & Resiliency (Expanded)

## 1. Key Terms

- **Steady state** → a measurable “normal” behavior of the system (baseline SLI/SLO).
- **Fault injection** → intentionally introducing failures to observe resilience.
- **Blast radius** → scope of an experiment (how many users/resources affected). Keep small at first.
- **Game day** → scheduled chaos experiment involving multiple teams, like a fire drill.
- **Resiliency testing** → broader umbrella including load testing, failover drills, chaos experiments.
- **MTBF / MTTR** → mean time between failures / mean time to recovery.
- **Error budget** → the portion of downtime allowed by the SLO.
- **Kill switch / rollback** → a fast way to stop the experiment if it gets risky.
- **Dark launch** → releasing a feature but routing no real users, to test readiness.
- **Canary** → routing a small percentage of users to new code or infra.

---

## 2. Types of Chaos Experiments

**By Layer**

- **Compute** → terminate instances/pods, CPU hog, memory leak, disk pressure.
- **Network** → add latency, drop packets, simulate partitions.
- **Storage** → disk full, I/O throttling, corrupted data blocks.
- **Dependencies** → force upstream API to timeout or return errors.
- **Region/AZ outage** → cut off an entire availability zone or data center.
- **Security/Access** → simulate expired TLS certificates, expired IAM roles.

**By Goal**

- **Availability** → can system self-heal after a node dies?
- **Latency** → does system degrade gracefully under slowness?
- **Correctness** → is data consistent when replicas partition?
- **Scaling** → do autoscalers trigger correctly under load?
- **Recovery** → can we failover quickly? Are runbooks correct?

---

## 3. Classic Experiments & Tools

- **Chaos Monkey (Netflix)** → randomly kill instances in prod.
- **Chaos Gorilla (Netflix)** → simulate AZ outage.
- **Chaos Kong (Netflix)** → simulate entire region outage.
- **Latency injection** (Gremlin, Chaos Mesh, Istio fault injection).
- **Pod delete** (Kubernetes chaos tools).
- **Dependency blackhole** → cut off calls to a downstream system.

---

## 4. Research & Lessons from Old Incidents

Chaos engineering often evolves from **real outages**. Some well-known ones:

- **Netflix (2008–2010)**: Region outages → led to Chaos Monkey/Gorilla/Kong for AZ/region kill testing.
- **Amazon S3 outage (2017)**: Mis-typed command removed too many servers; highlighted “fat-finger” risks and the need for safeguards.
- **Google GCP outage (2019)**: Network misconfig cascaded globally; importance of blast radius control.
- **Dyn DNS DDoS (2016)**: Took down major websites; showed need for dependency chaos and DDoS planning.
- **Facebook global outage (2021)**: BGP misconfig locked out employees; underscored testing of control-plane failures.
- **Ticketmaster–Taylor Swift (2022)**: Presale meltdown under \~14M fans (vs \~1.5M planned) plus bot load; revealed lack of graceful degradation and surge testing.

---

## 5. Mapping Experiments to SLOs

- **SLO: 99.9% availability**
  → Run chaos experiments like _pod kill_ or _node termination_. The system should failover within seconds/minutes, not hours.
- **SLO: p95 latency < 200ms**
  → Run _network latency injection_. See if requests still stay within the budget.
- **SLO: zero data loss**
  → Run _partition experiments_ on DB replicas. Ensure recovery reconciles without missing writes.

---

## 6. Checklist for Running Chaos Experiments

- ✅ Define steady state metric (e.g., error rate, latency).
- ✅ Choose smallest possible blast radius (one pod, one AZ).
- ✅ Run in staging → then canary slice in prod.
- ✅ Automate rollback and alerts.
- ✅ Document findings → update runbooks, add automation.
- ✅ Iterate → chaos is a program, not a one-off.

# Chaos Experiment Workflow

## A) LitmusChaos – Runbook

**Goal:** validate pod self-heal and latency SLOs in a K8s service.

### 1) Preconditions

- Pick **steady state** SLI/SLO (e.g., p95 < 200ms, error rate < 1%).
- **Blast radius**: 1 service, 1 replica, off-peak.
- Enable **rollback**: `kubectl rollout undo`, autoscaler sane, alerts wired.

### 2) Install CRDs (once)

```bash
kubectl apply -f https://litmuschaos.github.io/litmus/litmus-operator-vx.y.z.yaml
```

### 3) Minimal Pod-Kill Experiment

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: pod-kill-example
spec:
  appinfo:
    appns: default
    applabel: app=example-svc
    appkind: deployment
  annotationCheck: "false"
  engineState: active
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION # seconds
              value: "60"
            - name: CHAOS_INTERVAL # seconds between deletions
              value: "10"
            - name: FORCE
              value: "false"
```

### 4) Network Latency (optional)

```yaml
- name: pod-network-latency
  spec:
    components:
      env:
        - name: NETWORK_INTERFACE
          value: eth0
        - name: LATENCY
          value: "300" # ms
        - name: DURATION
          value: "120" # s
```

### 5) Observe & Decide

- During run: track **p95 latency**, **error rate**, **availability**, **restarts**.
- If SLOs breach or alerts fire: **kill switch** → `kubectl delete chaosengine pod-kill-example`.

### 6) After Action

- Record **findings**, update **runbooks** and **autoscaling/limits**, add **alerts** if gaps found.
- Schedule a higher-confidence rerun (e.g., include a small canary % in prod).

---

## B) AWS FIS – Runbook

**Goal:** terminate a single EC2 in an ASG with guardrails.

### 1) Preconditions

- IAM role for FIS with least privilege.
- **Stop condition**: CloudWatch alarm (e.g., `High5xx`).
- Known **ASG tag** to target only chaos-safe instances.

### 2) FIS Template (JSON)

```json
{
  "description": "Terminate one EC2 in chaos-safe ASG",
  "targets": {
    "Instances": {
      "resourceType": "aws:ec2:instance",
      "resourceTags": { "ChaosSafe": "true" },
      "selectionMode": "COUNT(1)"
    }
  },
  "actions": {
    "terminateOne": {
      "actionId": "aws:ec2:terminate-instances",
      "parameters": { "force": "false" },
      "targets": { "Instances": "Instances" }
    }
  },
  "stopConditions": [
    {
      "source": "aws:cloudwatch:alarm",
      "value": "arn:aws:cloudwatch:...:alarm/High5xx"
    }
  ],
  "roleArn": "arn:aws:iam::123456789012:role/FISExecutionRole"
}
```

### 3) Execute + Rollback

- Start via console/CLI. Watch SLOs and alarm state.
- Ensure ASG replaces instance; rollback if SLO burn accelerates.

### 4) Findings

- Did traffic rebalance? Were health checks/ELB drain working?
- Tune **grace periods**, **readiness probes**, **retry budgets**.

---

# System Design Deep Dives

## 1) Storage Scaling Patterns

### Event Sourcing

- **What**: store immutable **events**, reconstruct state by replay.
- **Why**: perfect audit trail, time travel, pub/sub projections.
- **Tradeoffs**: read models must be **materialized**; rebuild & snapshots.

**Command handler (pseudocode)**

```
# validate command against current aggregate
load events for aggregateId
state = fold(events)
newEvents = decide(state, command)
append newEvents atomically to event_log
publish newEvents to projection bus
```

**Snapshotting**

```
# every N events, store snapshot(state)
if count(events_since_last_snapshot) > N:
    write snapshot(aggregateId, state, last_event_id)
```

### CQRS (Command Query Responsibility Segregation)

- **Writes**: normalized, transactional.
- **Reads**: precomputed **projections** (denormalized for queries).
- **Consistency**: often **eventual**; expose “last updated” to clients.

**Projection updater (pseudocode)**

```
# on each event
for e in stream:
    # update read model optimized for queries
    apply(e, read_store)
```

### Materialized Views

- **What**: precomputed aggregates/tables.
- **Sources**: CDC (Debezium), stream jobs (Flink/Spark), triggers.
- **Ops**: rebuild plan, TTLs, backfill tooling.

### Outbox Pattern

- Ensure **atomic** DB write + event publish.

```
# in the same DB txn:
insert business_row(...)
insert outbox(event_id, payload, status='NEW')

# outbox relay:
loop:
  rows = select * from outbox where status='NEW' limit 100
  for r in rows:
    publish(r.payload)
    update outbox set status='SENT' where event_id=r.event_id
```

### Sagas (Distributed Transactions)

- **Choreography**: services react to events.
- **Orchestration**: central coordinator drives steps.

**Order saga (orchestrated)**

```
create order(PENDING)
reserve inventory -> OK?
  no -> cancel order
authorize payment -> OK?
  no -> release inventory, cancel order
capture payment, mark order CONFIRMED
```

---

## 2) Real-World Design Walkthroughs

### A) Twitter Timeline

**Requirements**

- Post tweet; follow; home timeline; user timeline; like/retweet; search.
- Low latency reads; huge fan-out; anti-abuse/rate limiting.

**Core choices**

- **Fan-out on write** (push to followers’ timelines) for normal users; **fan-out on read** for celebrities.
- **Write path**: Tweet → Kafka → Fanout workers → per-user timeline store (Cassandra/Redis).
- **Read path**: Timeline service reads from cache, paginates by time ID.
- **Search**: index tweet text/hashtags in Elasticsearch/OpenSearch.
- **Hot keys**: shard by user id; use consistent hashing + virtual nodes.

**APIs**

```
POST /tweets {user_id, text, media_ids[]}
GET  /users/{id}/timeline?cursor=...
POST /follow {follower_id, followee_id}
```

**Idempotency**

```
# Header: Idempotency-Key for tweet create
if exists(request_id): return stored_result
else: execute & store(request_id, result)
```

**SLOs**

- P99 timeline read < 200ms, write acknowledged < 150ms.

---

### B) YouTube-like Video Platform

**Pipeline**

- Chunked upload → virus scan → metadata store → **transcoding** (worker fleet) → multi-bitrate variants → store in **object storage** → **CDN** distribution.
- Metadata (Postgres/Spanner): title, user, tags, captions.
- Streaming: HLS/DASH manifests; signed URLs.

**Components**

- **Upload service** (auth, pre-signed URLs).
- **Transcode service** (queue + workers; FFmpeg).
- **Catalog service** (search/index).
- **Watch service** (serves manifests, enforces geo/rights).
- **Analytics** (view counts; exactly-once via stream dedupe or idempotency).

**Cache/CDN**

- Hot variants at edge; origin shield; cache-key includes **bitrate** and **codec**.

**SLOs**

- Upload success rate, time to first frame (TTFF), rebuffer ratio.

---

### C) E-commerce Checkout

**Services**

- Cart, Inventory, Order, Payment, Shipping, Notification, Pricing/Promotions, Fraud.

**Flow (saga)**

```
create order PENDING
reserve inventory -> OK?
  no -> FAIL_OUT_OF_STOCK
authorize payment -> OK?
  no -> release inventory; FAIL_PAYMENT
confirm order; capture payment; emit events
```

**Idempotent endpoints**

```
# request_id from client
if processed(request_id): return stored_result
else:
  execute
  record(request_id, result)
  return result
```

**Inventory reservation**

- Soft-reserve with TTL; on timeout or cancel, release.

**Payment**

- Auth then capture on ship; handle **chargebacks** and retries.

**Data**

- OLTP DB for orders; event stream to create **materialized views** (user order history, storefront availability).

**SLOs**

- Checkout P99 < 300ms (pre-payment); payment callback < 5s; order consistency visible < 1s.

---

## Quick Decision Cues (Interview Soundbites)

- **Fanout write vs read**: write is cheaper for average users; switch to read for celebrity hot paths.
- **Exactly-once** ≈ **at-least-once + idempotency** with a durable key.
- **Sagas over 2PC**: better availability and operability across microservices.
- **Event sourcing** if you need audit/time-travel; otherwise **outbox + CDC** often simpler.
- **Materialized views** to meet read SLOs; accept eventual consistency.

---

# Chaos Experiment Workflow

## A) LitmusChaos – Runbook

**Goal:** validate pod self-heal and latency SLOs in a K8s service.

### 1) Preconditions

- Pick **steady state** SLI/SLO (e.g., p95 < 200ms, error rate < 1%).
- **Blast radius**: 1 service, 1 replica, off-peak.
- Enable **rollback**: `kubectl rollout undo`, autoscaler sane, alerts wired.

### 2) Install CRDs (once)

```bash
kubectl apply -f https://litmuschaos.github.io/litmus/litmus-operator-vx.y.z.yaml
```

### 3) Minimal Pod-Kill Experiment

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: pod-kill-example
spec:
  appinfo:
    appns: default
    applabel: app=example-svc
    appkind: deployment
  annotationCheck: "false"
  engineState: active
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "60"
            - name: CHAOS_INTERVAL
              value: "10"
```

### 4) Network Latency (optional)

```yaml
- name: pod-network-latency
  spec:
    components:
      env:
        - name: LATENCY
          value: "300" # ms
        - name: DURATION
          value: "120" # s
```

### 5) Observe & Decide

- Track **latency, error rate, availability**.
- Kill switch if error budget burns too fast.

---

## B) Gremlin / Steadybit Runbook

### Gremlin

- **Philosophy:** “simple, controlled chaos.”
- **Installation:** lightweight agent on hosts or containers.
- **Scenarios:** CPU spike, memory hog, shutdown, network latency/loss.

**Example – Inject Latency**

```bash
# Add 300ms latency for 60s
gremlin attack latency \
  --length 60 \
  --latency 300 \
  --hosts app1
```

**Example – Kill Pod**

```bash
gremlin attack shutdown \
  --length 30 \
  --target "app=example-svc" \
  --namespace default
```

### Steadybit

- **Philosophy:** chaos as part of CI/CD.
- **Interface:** UI-driven + CLI + APIs.
- **Scenarios:** K8s pod kill, AWS AZ outage, latency injection, dependency failure.
- **Integration:** works with Jenkins, GitLab CI, ArgoCD.

**Example – Pod Termination (CLI)**

```bash
steadybit experiments run pod-delete \
  --selector "app=example-svc" \
  --duration 30s \
  --namespace default
```

**Example – Latency Injection**

```bash
steadybit experiments run pod-network-latency \
  --selector "app=example-svc" \
  --latency 300ms \
  --duration 60s
```

---

## Chaos Tools Comparison

| Tool            | Environment              | Fault Types                                   | Strengths                                                        | Limitations                                |
| --------------- | ------------------------ | --------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------ |
| **LitmusChaos** | Kubernetes-native        | Pod kill, network latency/loss, disk, node    | Open source, declarative (CRDs), integrates with GitOps          | K8s only; YAML-heavy configs               |
| **Gremlin**     | Hosts, containers, cloud | CPU/memory hogs, shutdown, latency, blackhole | SaaS, mature UI, fine-grained blast radius, strong agent library | Paid at scale; agent install required      |
| **Steadybit**   | K8s, cloud, CI/CD        | Pod kill, AWS/AZ failures, network chaos      | CI/CD integration, visual workflow builder, commercial support   | Paid; smaller OSS ecosystem vs LitmusChaos |
