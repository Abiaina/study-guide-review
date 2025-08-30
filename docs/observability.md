---
title: Observability
---

---

# Observability

Observability is often broken into the **three pillars**: **Logs, Metrics, Traces**. A modern system usually combines all three.

---

## 1. Metrics

- **Prometheus** → pull-based metrics collection. Best with Kubernetes.
- **Datadog** → SaaS monitoring platform (agents on hosts, integrations).
- **CloudWatch Metrics** → AWS-native; integrates with alarms.
- **Azure Monitor, GCP Monitoring** → cloud-native equivalents.

---

## 2. Visualization

### Grafana

- **Purpose:** dashboards and visualization for time-series metrics.
- **Sources:** can use Prometheus, InfluxDB, Elasticsearch, CloudWatch, Loki, and more.
- **Key Concepts:**

  - **Dashboards**: panels (graphs, tables, gauges).
  - **Templating**: variables (e.g., `$cluster`, `$namespace`).
  - **Alerting**: integrated alerts since Grafana 8, can trigger Slack/PagerDuty/etc.
  - **Plugins**: extend to new data sources.

- **Best Practices:**

  - Organize dashboards per _team_ or _service_.
  - Show SLOs: latency (p95, p99), error rate, request throughput.
  - Keep dashboards simple — 6–8 panels max per view.
  - Use _provisioning_ (`dashboards/` directory with JSON + `grafana.ini`).

**Example: Prometheus query in Grafana panel**

```
rate(http_requests_total{job="api",status=~"5.."}[5m])
```

This would plot the 5xx error rate.

---

## 3. Logs

- **CloudWatch Logs** → AWS log storage/queries.
- **Splunk** → enterprise log aggregation/search.
- **ELK (Elasticsearch + Logstash + Kibana)** → open-source stack.
- **Loki (Grafana Labs)** → log aggregation, pairs with Prometheus.
- **New Relic Logs** → SaaS, correlated with APM traces.

---

## 4. Traces

- **OpenTelemetry** → vendor-neutral standard; instrument once, export anywhere.
- **Jaeger** → CNCF tracing tool.
- **Zipkin** → lightweight tracer.
- **Datadog APM** → integrated metrics/logs/traces.
- **AWS X-Ray** → request tracing in AWS stack.

---

## 5. Putting It Together

- **Metrics**: numeric signals → detect anomalies.
- **Logs**: detailed context → debug failures.
- **Traces**: request path → diagnose latency & dependencies.

**Example Workflow**

1. Alert triggers: `p95 latency > 500ms` in Grafana.
2. Jump into logs (Splunk/Loki) for error details.
3. Trace with Jaeger/X-Ray to see which microservice caused the bottleneck.
