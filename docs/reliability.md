---
title: Reliability Engineering
---

# Reliability Engineering

Reliability engineering combines **observability**, **chaos engineering**, and **load testing** to build systems that are not only performant but also resilient and observable under stress.

---

## 1. Observability (The Three Pillars)

### Metrics
- **Prometheus** → pull-based metrics collection, best with Kubernetes
- **Datadog** → SaaS monitoring platform with agents and integrations
- **CloudWatch Metrics** → AWS-native, integrates with alarms
- **Azure Monitor, GCP Monitoring** → cloud-native equivalents

### Logs
- **CloudWatch Logs** → AWS log storage and queries
- **Splunk** → enterprise log aggregation and search
- **ELK Stack** (Elasticsearch + Logstash + Kibana) → open-source stack
- **Loki** → log aggregation, pairs with Prometheus
- **New Relic Logs** → SaaS, correlated with APM traces

### Traces
- **OpenTelemetry** → vendor-neutral standard, instrument once, export anywhere
- **Jaeger** → CNCF tracing tool
- **Zipkin** → lightweight tracer
- **Datadog APM** → integrated metrics/logs/traces
- **AWS X-Ray** → request tracing in AWS stack

### Visualization
- **Grafana** → dashboards and visualization for time-series metrics
- **Key Concepts**: panels, templating, alerting, plugins
- **Best Practices**: organize by team/service, show SLOs, keep simple

---

## 2. Chaos Engineering & Resiliency

### Principles
- **Define steady state** → measurable normal condition (e.g., "95% of requests < 200ms")
- **Hypothesize** → predict what should happen under failure
- **Inject faults** → simulate failure in controlled way
- **Observe** → measure whether steady state holds
- **Minimize blast radius** → start in staging or small slice of prod
- **Automate rollback** → make failure reversible

### Common Faults to Simulate
- **Compute**: kill random VM/pod, simulate resource starvation
- **Network**: latency injection, packet loss, partition a service
- **Storage**: I/O throttling, disk full
- **Dependencies**: force external API to error or slow
- **Region failure**: simulate cloud AZ/region outage

### Tools & Ecosystem
- **Service-level**: Gremlin, AWS FIS, Chaos Monkey
- **Kubernetes-native**: Chaos Mesh, LitmusChaos, Steadybit
- **Pipeline-integrated**: Harness, Argo Rollouts + chaos hooks

### Resiliency Patterns
- **Circuit breakers**: prevent cascading failures
- **Retries with backoff**: exponential backoff + jitter
- **Bulkheads**: partition threadpools/connection pools
- **Fallbacks**: return degraded response instead of full failure
- **Idempotency**: required under retries/at-least-once messaging

---

## 3. Load Testing & Performance

### Types of Performance Tests
- **Load Testing**: verify system behavior under expected load
- **Stress Testing**: find system limits and breaking points
- **Spike Testing**: sudden load increases to test resilience
- **Endurance Testing**: long-running tests to find memory leaks
- **Scalability Testing**: measure performance as load increases

### Key Metrics
- **Response Time**: P50, P90, P95, P99 percentiles
- **Throughput**: requests per second (RPS)
- **Error Rate**: percentage of failed requests
- **Resource Utilization**: CPU, memory, disk, network
- **Concurrent Users**: number of simultaneous users

### Load Testing Tools
- **JMeter**: open source, extensible, distributed testing
- **Gatling**: Scala-based, high-performance, real-time reports
- **K6**: JavaScript, cloud-native, real-time metrics

---

## 4. Internet Fundamentals & Communication Protocols

### OSI 7-Layer Model
```
Layer 7: Application    - HTTP, HTTPS, FTP, SMTP, DNS
Layer 6: Presentation  - SSL/TLS, data formatting
Layer 5: Session      - NetBIOS, RPC, SQL
Layer 4: Transport    - TCP, UDP
Layer 3: Network      - IP, ICMP, routing
Layer 2: Data Link    - Ethernet, MAC addresses
Layer 1: Physical     - Cables, wireless, hardware
```

### Transport Layer Protocols

#### TCP (Transmission Control Protocol)
- **Connection-oriented**: establishes connection before data transfer
- **Reliable delivery**: guarantees data arrives in order
- **Flow control**: prevents overwhelming receiver
- **Error checking**: detects and retransmits lost packets
- **Use cases**: HTTP, HTTPS, FTP, SSH, database connections

```python
# TCP Socket Example
import socket

# Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)

while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024)
    client_socket.send(b"Hello from TCP server")
    client_socket.close()

# Client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))
client_socket.send(b"Hello server")
response = client_socket.recv(1024)
client_socket.close()
```

#### UDP (User Datagram Protocol)
- **Connectionless**: no connection establishment
- **Unreliable**: no guarantee of delivery or order
- **Fast**: minimal overhead, no connection setup
- **No flow control**: can overwhelm receiver
- **Use cases**: DNS, DHCP, streaming video, gaming, real-time data

```python
# UDP Socket Example
import socket

# Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8080))

while True:
    data, addr = server_socket.recvfrom(1024)
    server_socket.sendto(b"Hello from UDP server", addr)

# Client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(b"Hello server", ('localhost', 8080))
response, addr = client_socket.recvfrom(1024)
client_socket.close()
```

### Application Layer Protocols

#### HTTP/HTTPS
- **HTTP**: stateless, request-response protocol
- **HTTPS**: HTTP over TLS/SSL for encryption
- **Methods**: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- **Status codes**: 2xx (success), 3xx (redirect), 4xx (client error), 5xx (server error)

```python
# HTTP Client Example
import requests

# GET request
response = requests.get('https://api.example.com/users')
users = response.json()

# POST request
new_user = {'name': 'John', 'email': 'john@example.com'}
response = requests.post('https://api.example.com/users', json=new_user)

# With authentication
headers = {'Authorization': 'Bearer token123'}
response = requests.get('https://api.example.com/profile', headers=headers)
```

#### gRPC
- **High-performance**: uses HTTP/2 and Protocol Buffers
- **Strong typing**: interface-first design with code generation
- **Bidirectional streaming**: supports real-time communication
- **Use cases**: microservices, real-time APIs, mobile apps

```protobuf
// user.proto
syntax = "proto3";

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc CreateUser(CreateUserRequest) returns (User);
  rpc StreamUsers(StreamUsersRequest) returns (stream User);
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
}

message GetUserRequest {
  string user_id = 1;
}
```

```python
# gRPC Server Example
import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

class UserServicer(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        # Fetch user logic
        return user_pb2.User(
            id=request.user_id,
            name="John Doe",
            email="john@example.com"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

# gRPC Client Example
import grpc
import user_pb2
import user_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = user_pb2_grpc.UserServiceStub(channel)

request = user_pb2.GetUserRequest(user_id="123")
response = stub.GetUser(request)
print(f"User: {response.name}")
```

#### Apache Kafka
- **Distributed streaming platform**: handles high-throughput, fault-tolerant messaging
- **Pub-sub model**: producers publish to topics, consumers subscribe
- **Partitioning**: topics divided into partitions for scalability
- **Use cases**: log aggregation, stream processing, event sourcing, real-time analytics

```python
# Kafka Producer Example
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send message to topic
producer.send('user-events', {
    'event_type': 'user_created',
    'user_id': '123',
    'timestamp': '2024-01-01T00:00:00Z'
})

producer.flush()

# Kafka Consumer Example
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='user-processor'
)

for message in consumer:
    event = message.value
    print(f"Processing event: {event['event_type']} for user {event['user_id']}")
```

### Protocol Comparison

| Protocol | Reliability | Performance | Use Case | Complexity |
|----------|-------------|-------------|----------|------------|
| **TCP** | ✅ Guaranteed | 🟡 Medium | Reliable data transfer | Low |
| **UDP** | ❌ Best effort | 🟢 High | Real-time, streaming | Low |
| **HTTP** | ✅ Reliable | 🟡 Medium | Web APIs, browsers | Low |
| **gRPC** | ✅ Reliable | 🟢 High | Microservices, streaming | Medium |
| **Kafka** | ✅ Reliable | 🟢 High | Event streaming, logs | High |

### Network Security Fundamentals

#### TLS/SSL Handshake
```
1. Client Hello: Supported ciphers, random number
2. Server Hello: Chosen cipher, random number, certificate
3. Key Exchange: Generate shared secret
4. Finished: Verify handshake integrity
```

#### Firewall Rules
```bash
# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow SSH from specific IP
iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 22 -j ACCEPT

# Block all other incoming
iptables -A INPUT -j DROP
```

#### Network Monitoring
```python
# Network connectivity check
import socket
import subprocess

def check_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def ping_host(host):
    try:
        subprocess.run(['ping', '-c', '1', host], 
                      capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Usage
print(f"Database accessible: {check_port('db.example.com', 5432)}")
print(f"API accessible: {check_port('api.example.com', 443)}")
print(f"Host reachable: {ping_host('example.com')}")
```

---

## 5. Putting It All Together

### Reliability Workflow
1. **Establish Baseline**: Use observability to understand normal system behavior
2. **Define SLOs**: Set service level objectives (availability, latency, error rate)
3. **Load Test**: Verify performance under expected and peak load
4. **Chaos Test**: Inject failures to validate resilience
5. **Monitor & Alert**: Use observability to detect issues during chaos
6. **Iterate**: Improve system based on findings

### Example: E-commerce System Reliability
```
Baseline SLOs:
- 99.9% availability
- P95 latency < 200ms
- Error rate < 1%

Load Testing:
- Simulate Black Friday traffic (10x normal)
- Monitor resource utilization
- Identify bottlenecks

Chaos Testing:
- Kill random database replicas
- Inject network latency
- Simulate payment service failure

Observability:
- Real-time dashboards during tests
- Alert on SLO violations
- Trace request flows to identify issues
```

---

## 5. Practical Examples

### JMeter Load Test with Prometheus Monitoring
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="API Load Test">
      <elementProp name="TestPlan.arguments" elementType="Arguments">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <stringProp name="TestPlan.comments"></stringProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="User Group">
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">10</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">100</stringProp>
        <stringProp name="ThreadGroup.ramp_time">10</stringProp>
        <boolProp name="ThreadGroup.scheduler">false</boolProp>
        <stringProp name="ThreadGroup.duration"></stringProp>
        <stringProp name="ThreadGroup.delay"></stringProp>
      </ThreadGroup>
      <hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="API Request">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
            <collectionProp name="Arguments.arguments"/>
          </elementProp>
          <stringProp name="HTTPSampler.domain">api.example.com</stringProp>
          <stringProp name="HTTPSampler.port">443</stringProp>
          <stringProp name="HTTPSampler.protocol">https</stringProp>
          <stringProp name="HTTPSampler.path">/api/users</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
        </HTTPSamplerProxy>
        <hashTree>
          <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="Response Assertion">
            <collectionProp name="Asserion.test_strings">
              <stringProp name="49586">200</stringProp>
            </collectionProp>
            <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
            <boolProp name="Assertion.assume_success">false</boolProp>
            <intProp name="Assertion.test_type">8</intProp>
          </ResponseAssertion>
          <hashTree/>
        </hashTree>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

### Prometheus Alerting Rules for Load Tests
```yaml
groups:
  - name: load_test.rules
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{job="api",code=~"5.."}[5m]) / rate(http_requests_total{job="api"}[5m]) > 0.05
        for: 10m
        labels: { severity: critical }
        annotations:
          summary: "High 5xx error rate during load test"
          description: ">5% 5xx over 10m"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="api"}[5m])) > 0.5
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "High P95 latency during load test"
          description: "P95 > 500ms for 5m"

      - alert: HighCPU
        expr: avg(rate(container_cpu_usage_seconds_total{container!="",pod=~"api.*"}[5m])) > 0.8
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "High CPU usage during load test"
          description: "CPU > 80% for 5m"
```

### Chaos Experiment with Monitoring
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: pod-kill-with-monitoring
spec:
  appinfo:
    appns: default
    applabel: app=api-service
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
            - name: FORCE
              value: "false"
          monitor:
            - name: "prometheus"
              url: "http://prometheus:9090"
              queries:
                - name: "error_rate"
                  query: 'rate(http_requests_total{job="api",code=~"5.."}[5m])'
                - name: "latency_p95"
                  query: 'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="api"}[5m]))'
```

---

## 6. Reliability Metrics & SLOs

### Service Level Objectives (SLOs)
- **Availability**: 99.9% uptime (allows ~43 minutes downtime/month)
- **Latency**: P95 < 200ms, P99 < 500ms
- **Error Rate**: < 1% for critical endpoints
- **Throughput**: handle expected peak load + 50% buffer

### Error Budgets
- **Budget = 1 - SLO** (e.g., 99.9% → 0.1% = 43 minutes/month)
- **Burn Rate Alerts**:
  - Fast burn: 2% of budget in 1 hour → page immediately
  - Slow burn: 5% of budget in 6 hours → investigate

### Reliability Scorecard
```
System: E-commerce API
Availability: 99.95% (target: 99.9%) ✅
Latency P95: 180ms (target: <200ms) ✅
Error Rate: 0.8% (target: <1%) ✅
Throughput: 1500 RPS (target: 1000 RPS) ✅

Reliability Grade: A
```

---

## 7. Reliability Testing Schedule

### Daily
- **Health Checks**: automated health checks on all services
- **Metrics Review**: quick review of key metrics and trends

### Weekly
- **Load Testing**: run baseline load tests
- **Chaos Experiments**: small-scale chaos experiments
- **SLO Review**: analyze SLO performance and trends

### Monthly
- **Comprehensive Load Testing**: full system load testing
- **Chaos Day**: coordinated chaos experiments across teams
- **Reliability Review**: comprehensive reliability assessment

### Quarterly
- **Disaster Recovery**: test full disaster recovery procedures
- **Capacity Planning**: review and update capacity plans
- **Tool Evaluation**: assess and update reliability tools

---

## 8. Tools Integration

### Prometheus + Grafana + AlertManager
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

scrape_configs:
  - job_name: 'api-service'
    static_configs:
      - targets: ['api-service:8080']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

### Load Testing in CI/CD
```yaml
# .github/workflows/reliability-test.yml
name: Reliability Testing
on: [push, pull_request]

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Load Test
        run: |
          k6 run load-test.js
        env:
          K6_PROMETHEUS_RW_SERVER_URL: ${{ secrets.PROMETHEUS_URL }}

  chaos-test:
    runs-on: ubuntu-latest
    needs: load-test
    steps:
      - uses: actions/checkout@v3
      - name: Run Chaos Experiment
        run: |
          kubectl apply -f chaos-experiment.yaml
          # Wait and monitor
          kubectl delete -f chaos-experiment.yaml
```

---

## 9. Best Practices

### Observability
- **Instrument Everything**: metrics, logs, and traces for all services
- **Correlate Data**: link metrics, logs, and traces with correlation IDs
- **Set Meaningful Alerts**: alert on symptoms, not causes
- **Document Runbooks**: clear procedures for common issues

### Chaos Engineering
- **Start Small**: begin with simple experiments in non-critical environments
- **Automate Rollback**: ensure experiments can be stopped quickly
- **Measure Impact**: quantify the effect of chaos experiments
- **Learn and Improve**: use findings to improve system resilience

### Load Testing
- **Test Realistic Scenarios**: simulate actual user behavior
- **Monitor During Tests**: observe system behavior under load
- **Test Failure Scenarios**: verify system behavior when components fail
- **Document Baselines**: establish performance baselines for comparison

---

## 10. Common Reliability Patterns

### Circuit Breaker
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            raise e
```

### Retry with Exponential Backoff
```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
```

### Health Check Endpoint
```python
from flask import Flask, jsonify
import psutil
import redis

app = Flask(__name__)

@app.route('/health')
def health_check():
    health_status = {
        'status': 'healthy',
        'timestamp': time.time(),
        'checks': {}
    }
    
    # Check CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    health_status['checks']['cpu'] = {
        'status': 'healthy' if cpu_percent < 80 else 'unhealthy',
        'value': cpu_percent
    }
    
    # Check memory usage
    memory_percent = psutil.virtual_memory().percent
    health_status['checks']['memory'] = {
        'status': 'healthy' if memory_percent < 90 else 'unhealthy',
        'value': memory_percent
    }
    
    # Check Redis connection
    try:
        redis_client = redis.Redis(host='localhost', port=6379)
        redis_client.ping()
        health_status['checks']['redis'] = {'status': 'healthy'}
    except:
        health_status['checks']['redis'] = {'status': 'unhealthy'}
    
    # Overall status
    all_healthy = all(check['status'] == 'healthy' for check in health_status['checks'].values())
    health_status['status'] = 'healthy' if all_healthy else 'unhealthy'
    
    return jsonify(health_status), 200 if all_healthy else 503
```

---

## 11. Reliability Checklist

### Pre-Production
- [ ] SLOs defined and documented
- [ ] Monitoring and alerting configured
- [ ] Load testing completed
- [ ] Chaos experiments planned
- [ ] Runbooks documented
- [ ] Rollback procedures tested

### Production
- [ ] Real-time monitoring active
- [ ] Alerts configured and tested
- [ ] Incident response team ready
- [ ] Backup and recovery tested
- [ ] Performance baselines established
- [ ] Reliability metrics tracked

### Continuous Improvement
- [ ] Regular reliability reviews scheduled
- [ ] Post-incident analysis conducted
- [ ] SLOs updated based on findings
- [ ] New chaos experiments planned
- [ ] Tools and processes evaluated
- [ ] Team training conducted

---

*Reliability engineering is not a one-time effort but a continuous process of building, testing, and improving system resilience.*
