---
title: Performance Testing & Optimization
---

# Performance Testing & Optimization

## 1. Load Testing Fundamentals

### Types of Performance Tests
- **Load Testing**: Verify system behavior under expected load
- **Stress Testing**: Find system limits and breaking points
- **Spike Testing**: Sudden load increases to test resilience
- **Endurance Testing**: Long-running tests to find memory leaks
- **Scalability Testing**: Measure performance as load increases

### Key Metrics
- **Response Time**: P50, P90, P95, P99 percentiles
- **Throughput**: Requests per second (RPS)
- **Error Rate**: Percentage of failed requests
- **Resource Utilization**: CPU, memory, disk, network
- **Concurrent Users**: Number of simultaneous users

---

## 2. Load Testing Tools

### JMeter
- **Open Source**: Free, extensible testing tool
- **Features**: HTTP, JDBC, LDAP, JMS testing
- **Reporting**: HTML reports with graphs and statistics
- **Distributed Testing**: Multiple machines for high load

### Gatling
- **Scala-based**: High-performance load testing
- **Real-time Reports**: Live monitoring during tests
- **Code-based**: Tests written in Scala/Java
- **CI/CD Integration**: Easy automation integration

### K6
- **JavaScript**: Tests written in modern JavaScript
- **Cloud-native**: Built for modern architectures
- **Real-time Metrics**: Live monitoring and alerting
- **Extensible**: Plugin system for custom protocols

---

## 3. JMeter Examples

### Basic HTTP Request Test
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

### JMeter CLI Commands
```bash
# Run test plan
jmeter -n -t test_plan.jmx -l results.jtl

# Run with properties file
jmeter -n -t test_plan.jmx -p user.properties -l results.jtl

# Generate HTML report
jmeter -n -t test_plan.jmx -l results.jtl -e -o report/

# Run distributed test
jmeter -n -t test_plan.jmx -R server1,server2,server3 -l results.jtl
```

---

## 4. Gatling Examples

### Basic HTTP Test
```scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class BasicSimulation extends Simulation {
  val httpProtocol = http
    .baseUrl("https://api.example.com")
    .acceptHeader("application/json")
    .userAgentHeader("Gatling/Performance Test")

  val scn = scenario("API Load Test")
    .exec(http("Get Users")
      .get("/api/users")
      .check(status.is(200))
      .check(jsonPath("$.users").exists))
    .pause(1)

  setUp(
    scn.inject(
      rampUsers(100).during(10.seconds),
      constantUsersPerSec(50).during(30.seconds)
    ).protocols(httpProtocol)
  )
}
```

### Advanced Test with Authentication
```scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class AuthenticatedSimulation extends Simulation {
  val httpProtocol = http
    .baseUrl("https://api.example.com")
    .acceptHeader("application/json")
    .contentTypeHeader("application/json")

  val login = exec(http("Login")
    .post("/api/auth/login")
    .body(StringBody("""{"username": "testuser", "password": "testpass"}"""))
    .check(status.is(200))
    .check(jsonPath("$.token").saveAs("authToken")))

  val authenticatedRequest = exec(http("Authenticated Request")
    .get("/api/protected")
    .header("Authorization", "Bearer ${authToken}")
    .check(status.is(200)))

  val scn = scenario("Authenticated API Test")
    .exec(login)
    .exec(authenticatedRequest)
    .pause(2)

  setUp(
    scn.inject(
      rampUsers(50).during(10.seconds),
      constantUsersPerSec(25).during(60.seconds)
    ).protocols(httpProtocol)
  )
}
```

---

## 5. K6 Examples

### Basic HTTP Test
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 }, // Ramp up
    { duration: '1m', target: 20 },  // Stay at 20 users
    { duration: '30s', target: 0 },  // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
    http_req_failed: ['rate<0.1'],    // Error rate must be below 10%
  },
};

export default function () {
  const response = http.get('https://api.example.com/users');
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}
```

### Advanced Test with Custom Metrics
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const responseTime = new Trend('response_time');

export const options = {
  vus: 100,
  duration: '5m',
  thresholds: {
    errors: ['rate<0.1'],
    response_time: ['p(95)<500'],
  },
};

export default function () {
  const start = Date.now();
  const response = http.get('https://api.example.com/users');
  const end = Date.now();
  
  const duration = end - start;
  responseTime.add(duration);
  
  const success = check(response, {
    'status is 200': (r) => r.status === 200,
    'response has users': (r) => r.json('users').length > 0,
  });
  
  errorRate.add(!success);
  sleep(1);
}
```

---

## 6. Performance Optimization

### Database Optimization
- **Indexing**: Create indexes on frequently queried columns
- **Query Optimization**: Use EXPLAIN to analyze query plans
- **Connection Pooling**: Reuse database connections
- **Read Replicas**: Distribute read load across multiple databases

### Application Optimization
- **Caching**: Implement Redis/Memcached for frequently accessed data
- **Async Processing**: Use message queues for non-critical operations
- **Connection Pooling**: Reuse HTTP connections
- **Resource Management**: Properly close connections and resources

### Infrastructure Optimization
- **Load Balancing**: Distribute traffic across multiple servers
- **Auto-scaling**: Automatically scale based on load
- **CDN**: Use content delivery networks for static content
- **Monitoring**: Implement comprehensive monitoring and alerting

---

## 7. Performance Monitoring

### Application Performance Monitoring (APM)
- **New Relic**: Full-stack application monitoring
- **Datadog**: Infrastructure and application monitoring
- **AppDynamics**: Business transaction monitoring
- **Dynatrace**: AI-powered monitoring and optimization

### Key Metrics to Monitor
- **Response Time**: P50, P90, P95, P99 percentiles
- **Throughput**: Requests per second
- **Error Rate**: Percentage of failed requests
- **Resource Utilization**: CPU, memory, disk, network
- **Business Metrics**: User engagement, conversion rates

### Alerting and Thresholds
- **Response Time**: Alert when P95 > 500ms
- **Error Rate**: Alert when error rate > 5%
- **Resource Usage**: Alert when CPU > 80% or memory > 90%
- **Business Impact**: Alert when key business metrics degrade

---

## 8. Capacity Planning

### Load Estimation
- **Current Load**: Measure existing system performance
- **Growth Projections**: Estimate future load based on business growth
- **Peak Load**: Identify peak usage patterns and requirements
- **Seasonal Variations**: Account for seasonal traffic patterns

### Resource Planning
- **CPU Requirements**: Calculate CPU needs based on load
- **Memory Requirements**: Estimate memory usage patterns
- **Storage Requirements**: Plan for data growth and retention
- **Network Requirements**: Estimate bandwidth and latency needs

### Scaling Strategies
- **Vertical Scaling**: Increase resources on existing servers
- **Horizontal Scaling**: Add more servers to distribute load
- **Auto-scaling**: Automatically scale based on load
- **Load Balancing**: Distribute traffic across multiple servers

---

## 9. Performance Testing Best Practices

### Test Environment
- **Production-like**: Use environment similar to production
- **Data Volume**: Use realistic data volumes
- **Network Conditions**: Test with realistic network latency
- **Monitoring**: Implement comprehensive monitoring during tests

### Test Execution
- **Baseline**: Establish performance baseline before changes
- **Incremental**: Test with increasing load to find breaking points
- **Regression**: Run performance tests after each deployment
- **Documentation**: Document test results and findings

### Analysis and Reporting
- **Metrics Collection**: Collect comprehensive performance metrics
- **Trend Analysis**: Analyze performance trends over time
- **Root Cause Analysis**: Investigate performance issues thoroughly
- **Action Items**: Create actionable items for performance improvements

---

## 10. Common Performance Issues

### Memory Leaks
- **Symptoms**: Increasing memory usage over time
- **Causes**: Unclosed connections, circular references
- **Solutions**: Proper resource cleanup, memory profiling

### Database Bottlenecks
- **Symptoms**: Slow query response times
- **Causes**: Missing indexes, inefficient queries
- **Solutions**: Query optimization, indexing, read replicas

### Network Latency
- **Symptoms**: High response times, timeouts
- **Causes**: Geographic distance, network congestion
- **Solutions**: CDN, edge computing, connection pooling

### Resource Contention
- **Symptoms**: High CPU/memory usage, slow response
- **Causes**: Insufficient resources, inefficient algorithms
- **Solutions**: Resource scaling, algorithm optimization
