"""day_data_094.py — Exhaustive architecture data specification for Day 94.

Covers Logs, Traces, and Profiling:
1. Cloud Logging: log router, log sinks (BigQuery, Cloud Storage, Pub/Sub), log buckets, exclusions, log-based metrics, retention policies, and Log Analytics (BigQuery-linked SQL).
2. Cloud Trace, Cloud Profiler, and Error Reporting: distributed request tracing, sampling rate trade-offs, continuous low-overhead CPU/heap/contention profiling, automated exception grouping.
3. OpenTelemetry (OTel) instrumentation: W3C traceparent context propagation across HTTP/gRPC boundaries, trace-log correlation via trace_id injection, and OTel Cloud Exporters.
Follows PAGE_AUTHORING_CONTRACT.md with hands-on, verifiable exercises.
"""

DAY_NUM = 94

DATA = {
    "day": 94,
    "part1_intro": (
        "Day 94 shifts observability from aggregate time-series metrics to high-fidelity transaction telemetry: structured logging, "
        "distributed tracing, continuous runtime profiling, and exception aggregation. While metrics show that a service is failing, "
        "logs and traces isolate exactly why, where, and for which customer request the failure occurred. In high-throughput distributed "
        "systems, naive logging causes exorbitant storage bills and noisy query timeouts, while un-traced asynchronous messaging chains "
        "turn debugging into guesswork. Today's curriculum constructs an enterprise logging and tracing architecture using Google Cloud "
        "Logging routers, cost-saving exclusion filters, BigQuery-backed Log Analytics, Cloud Trace with continuous Cloud Profiler, and "
        "vendor-neutral OpenTelemetry instrumentation linking distributed spans to structured JSON logs."
    ),
    "exit_summary": (
        "Engineered a production Logs, Traces, and Profiling telemetry architecture: implemented Cloud Logging log router sinks and cost-optimized "
        "exclusion filters with Log Analytics SQL analytics; configured Cloud Trace and continuous Cloud Profiler to capture distributed latency "
        "bottlenecks and heap allocations; deployed an OpenTelemetry W3C trace context interceptor with automated trace-log correlation in structured JSON."
    ),
    "part2_intro": (
        "Deep application observability requires correlating three distinct execution signals: structured log events, distributed trace spans, "
        "and runtime CPU/memory profiles. The sections below analyze the architectural mechanics of the Google Cloud Log Router, distributed "
        "trace context propagation, continuous profiling overhead bounds, and OpenTelemetry instrumentation pipelines."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Observability Primitive</th>
      <th>GCP Service / Engine</th>
      <th>Data Ingestion &amp; Storage Mechanics</th>
      <th>Retention &amp; Query Interface</th>
      <th>Key Architectural Trade-off / Cost Boundary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Structured Logs</strong></td>
      <td>Cloud Logging (Log Router &amp; Log Buckets)</td>
      <td>Streaming JSON ingestion via Ops Agent / Logging API to regional Log Buckets</td>
      <td>30 days standard (configurable up to 3650 days); Logs Explorer &amp; SQL via Log Analytics</td>
      <td>$0.50/GiB after free allocation; requires exclusion filters to drop health checks and repetitive debug chatter</td>
    </tr>
    <tr>
      <td><strong>Log Analytical Warehouse</strong></td>
      <td>Log Analytics (BigQuery-linked)</td>
      <td>Zero-ETL automated synchronization between regional Log Buckets and BigQuery schemas</td>
      <td>Matches Log Bucket retention; standard BigQuery SQL dialect querying `_AllLogs` views</td>
      <td>Requires linked dataset creation; queries incur BigQuery compute slot costs or on-demand scan fees</td>
    </tr>
    <tr>
      <td><strong>Distributed Traces</strong></td>
      <td>Cloud Trace</td>
      <td>Span collection via OpenTelemetry Trace Exporter / Cloud Trace API</td>
      <td>30 days rolling window; Cloud Trace UI and latency distribution histograms</td>
      <td>Sampling rate trade-off: 100% trace capture causes extreme billing; rate-limiting / probabilistic sampling mandatory</td>
    </tr>
    <tr>
      <td><strong>Continuous Profiling</strong></td>
      <td>Cloud Profiler</td>
      <td>Statistical sampling via in-process C++/Go/Java/NodeJS/Python runtime agents</td>
      <td>30 days rolling; flame graphs for CPU, wall-time, heap allocations, and lock contention</td>
      <td>Negligible CPU overhead (<1%) and minimal network egress; cannot capture individual request traces (aggregate only)</td>
    </tr>
    <tr>
      <td><strong>Exception Grouping</strong></td>
      <td>Error Reporting</td>
      <td>Automated regex matching on structured JSON logs containing stack traces or Error Reporting API</td>
      <td>30 days rolling; automated notification channels and resolution status tracking</td>
      <td>Requires standard exception formats or explicit `serviceContext`; unhandled panics without stack traces are missed</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Unified Telemetry Architecture: Logging, Tracing, Profiling, and Error Reporting",
        "desc": "Flow diagram showing client request ingress, trace context injection, OpenTelemetry span extraction, structured log emission, and storage sinks.",
        "caption": "Figure 94.1: Unified transaction telemetry pipeline across Cloud Trace, Cloud Logging Router, BigQuery Log Analytics, and Cloud Profiler.",
        "nodes": [
            ("1. Ingress Request", "W3C traceparent injected"),
            ("2. App Service Span", "OTel SDK traces & profiles"),
            ("3. Log Router Sinks", "Filtered to Storage/BigQuery"),
            ("4. Unified Correlation", "Trace ID links logs & flamegraph"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Cloud Logging: Log Router, Sinks, Exclusions, and Log Analytics",
            "overview": (
                "Google Cloud Logging decouples log generation from log storage through an event routing pipeline known as the Log Router. "
                "Every service, VM, container, and audit log emitted in a Google Cloud organization flows through the Log Router, which evaluates "
                "inclusion and exclusion filters in real time before routing logs to regional Log Buckets, Cloud Storage for archival, BigQuery "
                "for deep analysis, or Pub/Sub for SIEM integration. Log Analytics links log buckets to BigQuery, enabling relational SQL queries "
                "over streaming semi-structured JSON payloads without custom ingestion pipelines."
            ),
            "preview": (
                "An unconfigured log router ingests gigabytes of repetitive load balancer health checks, triggering thousands of dollars in billing overages. "
                "Proper routing with exclusion filters and BigQuery Log Analytics eliminates noise while preserving compliance and audit trails."
            ),
            "technical": (
                "### 1. Log Router Mechanics and Sink Topology\n"
                "- **Processing Sequence:** When an application or infrastructure component writes a log entry, it arrives at the Log Router. "
                "The router checks two layers of rules: **Exclusion Filters** and **Sink Destinations**.\n"
                "- **Exclusion Filters:** Discard high-volume, low-value logs (e.g. `httpRequest.status = 200 AND httpRequest.requestUrl =~ '/healthz'`) "
                "prior to storage, preventing ingestion charges while allowing sample percentages (e.g. keep 1% of healthy requests for baseline analysis).\n"
                "- **Sinks:** Define the target destination for matching logs:\n"
                "  - **Log Bucket (Default):** Regional, encrypted storage inside Cloud Logging with retention from 1 to 3650 days.\n"
                "  - **BigQuery:** Streams structured logs into BigQuery partitioned tables for enterprise analytical correlation.\n"
                "  - **Cloud Storage:** Cost-effective long-term cold archive for regulatory compliance (e.g., 7-year WORM storage).\n"
                "  - **Pub/Sub:** Low-latency event streaming to third-party SIEM platforms (Splunk, Datadog, Chronicle).\n\n"
                "### 2. Log Analytics and BigQuery Linking\n"
                "- **BigQuery-Linked Buckets:** Upgrading a Log Bucket to use Log Analytics provisions a linked BigQuery dataset. SREs can write "
                "standard SQL queries joining log records with customer tables or cost allocation datasets.\n"
                "- **JSON Parsing in SQL:** Structured log payloads stored in `json_payload` can be extracted using BigQuery JSON operators:\n"
                "  `SELECT JSON_VALUE(json_payload.order_id) AS order_id, count(*) FROM `project_id.region_id.bucket_id._AllLogs` GROUP BY 1`.\n\n"
                "### 3. Log-Based Metrics\n"
                "- **Counter Metrics:** Count log entries matching a filter (e.g., counting HTTP 500 errors to create Cloud Monitoring alerts).\n"
                "- **Distribution Metrics:** Extract numerical values from JSON fields (e.g., parsing payload sizes or payment processing latencies) "
                "into Cloud Monitoring distribution histograms for SLO calculation."
            ),
            "questions": [
                "How do Log Router exclusion filters prevent runaway Cloud Logging ingestion costs without blinding operational dashboards?",
                "What architectural trade-offs govern routing logs to BigQuery via Log Router sinks versus enabling Log Analytics on Log Buckets?",
                "Why should log-based metrics be restricted to bounded extractors rather than arbitrary high-cardinality regex fields?",
            ],
            "reference": "https://docs.cloud.google.com/logging/docs/routing/overview",
            "reference_label": "Google Cloud Logging: Log Router, sinks, exclusion filters, and Log Analytics configuration",
            "scenario": {
                "symptom": (
                    "Brightloaf's monthly Cloud Logging invoice reached $42,000 for a single billing cycle. Over 85% of total log volume consisted "
                    "of redundant Kubernetes kubelet probes and Cloud Load Balancer HTTP 200 `/healthz` polling logs occurring every 2 seconds across 300 pods."
                ),
                "constraints": (
                    "Must drop 95% of routine health-check traffic to bring ingestion under $2,000/month while preserving 100% of HTTP 5xx errors "
                    "and 1% of successful probes for latency baseline audits."
                ),
                "evidence": (
                    "Log Router inspection revealed `_Default` sink was ingesting 450 GiB/day. A breakdown by `logName` identified `cloudaudit.googleapis.com` "
                    "and `requests` logs dominated by user-agent `GoogleHC/1.0`."
                ),
                "diagnostic_steps": [
                    "Query Cloud Logging usage metrics `logging.googleapis.com/billing/bytes_ingested` grouped by `resource_type` and `log_id`.",
                    "Analyze Logs Explorer sample queries to isolate repetitive probe request patterns.",
                    "Audit existing Log Router sinks and verify whether exclusion rules exist on the `_Default` bucket sink.",
                ],
                "root": (
                    "Missing Log Router exclusion rules allowed uncompressed, high-frequency internal health-check transactions to be ingested "
                    "and billed at full price into standard retention storage."
                ),
                "fix": (
                    "Configure an exclusion filter on the `_Default` log sink matching `httpRequest.userAgent =~ 'GoogleHC/.*' AND httpRequest.status = 200` "
                    "with a 99% drop rate (1% sampling). Deploy a Log Analytics linked dataset to query remaining logs via BigQuery SQL."
                ),
                "verify": (
                    "Check `logging.googleapis.com/billing/bytes_ingested` after applying exclusion; verify daily ingestion falls from 450 GiB/day to 22 GiB/day "
                    "while synthetic error logs continue to appear in Logs Explorer."
                ),
                "residual": (
                    "Exclusion filters permanently discard un-sampled matching logs prior to ingestion; dropped logs cannot be retrieved retroactively for historical investigations."
                ),
                "diagram": (
                    "High-volume health probes",
                    "Unfiltered log router",
                    "Storage billing explosion",
                    "Exclusion filter applied",
                    "Controlled ingestion cost"
                )
            },
            "lab": {
                "name": "Cloud Logging Router Architecture, Cost Exclusion Filters, and Log Analytics SQL",
                "goal": "Author a production Cloud Logging sink configuration with exclusion rules and execute SQL queries against Log Analytics.",
                "expected": "A validated Cloud Logging sink manifest, an executable Python log generator, and a tested BigQuery Log Analytics SQL script.",
                "mode": "tabletop analysis & shell/SQL synthesis",
                "prereq": "Understanding of Google Cloud Logging filters and JSON structures.",
                "preflight": "Review gcloud logging sink CLI syntax and BigQuery SQL dialect.",
                "steps": [
                    "Author the Cloud Logging Router sink specification with cost-saving exclusion filters:\n\n```sh\ncat <<'EOF' > day-094-topic-01-log-sink.json\n{\n  \"name\": \"brightloaf-compliance-sink\",\n  \"destination\": \"storage.googleapis.com/brightloaf-audit-logs-cold-vault\",\n  \"filter\": \"severity >= WARNING OR protoPayload.methodName =~ '.*(delete|patch|update).*'\",\n  \"description\": \"Archive security-sensitive audit and error logs to cold storage for 7-year retention\",\n  \"exclusions\": [\n    {\n      \"name\": \"drop-k8s-health-checks\",\n      \"description\": \"Drop 99% of routine load balancer and kubelet health checks\",\n      \"filter\": \"httpRequest.userAgent =~ 'GoogleHC/.*' AND httpRequest.status = 200\",\n      \"disabled\": false\n    },\n    {\n      \"name\": \"drop-routine-readiness\",\n      \"description\": \"Discard all readiness endpoint queries\",\n      \"filter\": \"httpRequest.requestUrl =~ '.*/readyz$' AND httpRequest.status = 200\",\n      \"disabled\": false\n    }\n  ]\n}\nEOF\ncat day-094-topic-01-log-sink.json\n```",
                    "Author an automated Python simulation modeling log ingestion filtering and calculating exact dollar savings:\n\n```sh\ncat <<'EOF' > simulate_log_routing.py\n# Simulation of Log Router exclusion evaluation and cost reduction\n\nraw_events = [\n    {\"type\": \"health\", \"ua\": \"GoogleHC/1.0\", \"status\": 200, \"size_bytes\": 450},\n    {\"type\": \"health\", \"ua\": \"GoogleHC/1.0\", \"status\": 200, \"size_bytes\": 450},\n    {\"type\": \"health\", \"ua\": \"GoogleHC/1.0\", \"status\": 500, \"size_bytes\": 720},\n    {\"type\": \"order\", \"ua\": \"Mozilla/5.0\", \"status\": 200, \"size_bytes\": 1200},\n    {\"type\": \"order\", \"ua\": \"Mozilla/5.0\", \"status\": 503, \"size_bytes\": 1500},\n    {\"type\": \"audit\", \"ua\": \"gcloud/450\", \"status\": 200, \"size_bytes\": 2800}\n]\n\ndef route_log(entry):\n    # Exclusion Rule 1: Drop routine health checks (200 OK)\n    if entry.get(\"ua\", \"\").startswith(\"GoogleHC/\") and entry.get(\"status\") == 200:\n        return False, \"EXCLUDED: drop-k8s-health-checks\"\n    return True, \"INGESTED to Log Bucket\"\n\ningested_bytes = 0\nexcluded_bytes = 0\n\nfor log in raw_events:\n    keep, action = route_log(log)\n    if keep:\n        ingested_bytes += log[\"size_bytes\"]\n    else:\n        excluded_bytes += log[\"size_bytes\"]\n\nprint(f\"Raw Total Bytes:     {ingested_bytes + excluded_bytes} bytes\")\nprint(f\"Ingested Bytes:      {ingested_bytes} bytes\")\nprint(f\"Excluded Bytes:      {excluded_bytes} bytes\")\nprint(f\"Storage Reduction:   {(excluded_bytes / (ingested_bytes + excluded_bytes)) * 100:.1f}%\")\nassert excluded_bytes == 900, \"Simulation failed: health checks not excluded correctly!\"\nprint(\"PASS: Log Router exclusion simulation validated.\")\nEOF\npython3 simulate_log_routing.py\n```",
                    "Author a production BigQuery Log Analytics SQL script querying structured application error patterns:\n\n```sh\ncat <<'EOF' > day-094-topic-01-log-analytics.sql\n-- Query Log Analytics linked dataset to find top error clusters and latency percentiles\nSELECT\n  JSON_VALUE(json_payload.service) AS microservice,\n  JSON_VALUE(json_payload.error_code) AS error_code,\n  COUNT(*) AS error_occurrences,\n  ROUND(AVG(CAST(JSON_VALUE(json_payload.duration_ms) AS FLOAT64)), 2) AS avg_duration_ms,\n  ARRAY_AGG(DISTINCT JSON_VALUE(json_payload.trace_id) IGNORE NULLS LIMIT 3) AS sample_trace_ids\nFROM\n  `brightloaf-prod.us_central1.brightloaf_app_logs._AllLogs`\nWHERE\n  timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)\n  AND severity IN ('ERROR', 'CRITICAL')\nGROUP BY\n  1, 2\nORDER BY\n  error_occurrences DESC\nLIMIT 10;\nEOF\ncat day-094-topic-01-log-analytics.sql\n```",
                    "Review all output artifacts and confirm that the exclusion filter JSON, routing simulation, and Log Analytics SQL script are syntactically valid."
                ],
                "verification": "The log router JSON defines both destination and exclusion rules, the Python simulation passes assertions, and the BigQuery SQL accurately parses JSON payload fields.",
                "trouble": "Ensure BigQuery SQL uses the backticked table format `project.location.bucket._AllLogs` when querying Log Analytics linked datasets.",
                "cleanup": "Retain `day-094-topic-01-log-sink.json` and `day-094-topic-01-log-analytics.sql` as exit evidence artifacts.",
                "accept": "Completed Log Router configuration and verified Log Analytics SQL script. File: `day-094-topic-01-log-analytics.md`.",
                "file": "day-094-topic-01-log-analytics.md"
            }
        },
        {
            "key": "topic-02",
            "title": "Cloud Trace, Cloud Profiler, and Error Reporting",
            "overview": (
                "Cloud Trace provides distributed latency analysis across microservice boundaries, visualizing request timelines through nested "
                "waterfall span graphs. Cloud Profiler operates continuously in production with less than 1% CPU overhead, statistically sampling "
                "runtime call stacks to generate flame graphs identifying CPU hotspots, memory leak allocations, and thread synchronization bottlenecks. "
                "Error Reporting automatically aggregates runtime stack traces and unhandled exceptions into deduplicated problem groups, "
                "linking incident tickets directly to the code line responsible."
            ),
            "preview": (
                "A checkout request experiences an intermittent 4-second delay, but individual component metrics show normal CPU and memory utilization. "
                "Cloud Trace and Cloud Profiler reveal downstream thread contention and un-indexed database lock waits that metrics completely obscure."
            ),
            "technical": (
                "### 1. Distributed Tracing Mechanics (Cloud Trace)\n"
                "- **Span Hierarchy:** A Trace represents an end-to-end user transaction composed of one or more Spans. Each span records a named "
                "operation, start and end timestamps, status codes, and key-value attributes.\n"
                "- **Sampling Rate Strategies:** In high-volume systems (e.g. 100,000 requests/sec), capturing 100% of traces incurs massive network "
                "and storage overhead. Architects implement **Head-based Probabilistic Sampling** (e.g., sample 1 out of 1000 requests at the API Gateway) "
                "or **Adaptive/Tail-based Sampling** (always sample requests resulting in HTTP 5xx or exceeding a latency threshold such as 2.0 seconds).\n\n"
                "### 2. Low-Overhead Continuous Profiling (Cloud Profiler)\n"
                "- **Statistical Sampling:** Unlike intrusive debuggers that alter program timing, Cloud Profiler uses statistical OS timers "
                "(`SIGPROF` interrupts) to capture call stacks at random 10ms intervals over a 10-second sampling window once every minute.\n"
                "- **Profile Types:**\n"
                "  - **CPU Time:** Identifies functions consuming the most processor cycles.\n"
                "  - **Wall Time:** Identifies functions blocked on I/O, database locks, or network calls.\n"
                "  - **Heap Allocations:** Pinpoints functions allocating the most RAM (critical for preventing Kubernetes OOMKilled events).\n"
                "  - **Contention / Mutex:** Identifies lock serialization bottlenecks in multi-threaded runtimes.\n\n"
                "### 3. Error Reporting Exception Aggregation\n"
                "- **Grouping Algorithm:** Error Reporting parses stack traces and groups errors by top-level calling function and exception type, "
                "preventing thousands of identical crashes from producing thousands of individual alert notifications.\n"
                "- **Context Binding:** Automatically extracts HTTP request method, URL, user agent, and release version when formatted in "
                "Google Cloud's structured `ReportedErrorEvent` schema."
            ),
            "questions": [
                "Why is continuous statistical profiling architecturally superior to ad-hoc APM agent profiling in production environments?",
                "What sampling strategy ensures that rare, high-latency tail events are captured in Cloud Trace without overpaying for trace storage?",
                "How does Error Reporting correlate grouped exception signatures with specific Git release versions?",
            ],
            "reference": "https://docs.cloud.google.com/trace/docs/overview",
            "reference_label": "Google Cloud Trace, Cloud Profiler, and Error Reporting production architecture",
            "scenario": {
                "symptom": (
                    "Brightloaf's checkout service suffered an unexplained P99 latency degradation from 180ms to 4,200ms following a microservice refactoring, "
                    "yet GKE cluster CPU utilization remained below 25%."
                ),
                "constraints": (
                    "Must diagnose the bottleneck without taking down production nodes or running invasive debugging sessions that degrade customer throughput."
                ),
                "evidence": (
                    "Cloud Trace waterfall diagrams showed the `OrderProcessing` span took 4,100ms, with 95% of the time spent in a nested child span "
                    "named `InventoryDeduction`. Cloud Profiler flame graphs revealed 98% of wall-time in `InventoryDeduction` was spent in `threading.Lock.acquire()`."
                ),
                "diagnostic_steps": [
                    "Open Cloud Trace Explorer and filter transactions where `latency > 3s`.",
                    "Inspect the waterfall breakdown of the slowest trace to identify which child span consumed the bulk of the duration.",
                    "Open Cloud Profiler and switch the profile view to 'Wall Time' and 'Contention' for the `checkout-service` deployment.",
                ],
                "root": (
                    "Lock contention: a developer had introduced a global in-memory Python mutex around the inventory stock check rather than using "
                    "optimistic locking in Spanner/Cloud SQL, causing all concurrent checkout threads to serialize behind a single locked resource."
                ),
                "fix": (
                    "Replace the in-memory global mutex with fine-grained per-SKU distributed lock tokens or database-level row-level version checks. "
                    "Deploy Cloud Profiler continuous profiling in staging to verify lock wait time drops to near zero."
                ),
                "verify": (
                    "Inspect Cloud Trace P99 latency distribution histogram post-fix; confirm P99 returns to <200ms and Cloud Profiler contention flame graphs clear."
                ),
                "residual": (
                    "Cloud Trace sampling may miss transient 1-in-10,000 latency spikes unless adaptive tail-based sampling is configured at the ingress layer."
                ),
                "diagram": (
                    "Refactored checkout release",
                    "Global thread lock added",
                    "P99 latency spikes to 4.2s",
                    "Profiler isolates mutex lock",
                    "P99 latency restored <200ms"
                )
            },
            "lab": {
                "name": "Cloud Trace Waterfall Analysis and Cloud Profiler Flame Graph Synthesis",
                "goal": "Instrument a Python microservice with OpenTelemetry distributed tracing and analyze latency waterfall spans and lock contention.",
                "expected": "A runnable Python distributed service simulator emitting correlated trace spans and a flame-graph diagnostic analysis document.",
                "mode": "local script execution & tabletop analysis",
                "prereq": "Understanding of distributed tracing spans and thread contention.",
                "preflight": "Ensure Python 3 standard library is accessible; no cloud credentials required.",
                "steps": [
                    "Author an executable Python script simulating distributed trace span generation with injected lock contention:\n\n```sh\ncat <<'EOF' > trace_profiler_sim.py\n# Simulation of Distributed Tracing Spans and Wall-Time Contention\nimport time\nimport json\nimport uuid\nimport threading\n\n# Global lock to demonstrate contention bottleneck\nINVENTORY_LOCK = threading.Lock()\n\ndef simulate_checkout_transaction(order_id, trace_id, simulate_contention=True):\n    trace_record = {\n        \"trace_id\": trace_id,\n        \"root_span\": \"CheckoutOrder\",\n        \"order_id\": order_id,\n        \"spans\": []\n    }\n    \n    start_total = time.time()\n    \n    # Span 1: Ingress Authentication\n    s1_start = time.time()\n    time.sleep(0.02) # 20ms auth check\n    trace_record[\"spans\"].append({\n        \"name\": \"AuthenticateToken\",\n        \"duration_ms\": round((time.time() - s1_start) * 1000, 2),\n        \"status\": \"OK\"\n    })\n    \n    # Span 2: Inventory Allocation (Contention Bottleneck)\n    s2_start = time.time()\n    if simulate_contention:\n        with INVENTORY_LOCK:\n            time.sleep(0.15) # 150ms serialized lock wait\n    else:\n        time.sleep(0.01) # 10ms non-blocking check\n        \n    trace_record[\"spans\"].append({\n        \"name\": \"InventoryAllocation\",\n        \"duration_ms\": round((time.time() - s2_start) * 1000, 2),\n        \"status\": \"OK\",\n        \"contention_flag\": simulate_contention\n    })\n    \n    # Span 3: Payment Gateway Charge\n    s3_start = time.time()\n    time.sleep(0.05) # 50ms external API call\n    trace_record[\"spans\"].append({\n        \"name\": \"PaymentCharge\",\n        \"duration_ms\": round((time.time() - s3_start) * 1000, 2),\n        \"status\": \"OK\"\n    })\n    \n    total_duration = round((time.time() - start_total) * 1000, 2)\n    trace_record[\"total_duration_ms\"] = total_duration\n    return trace_record\n\n# Run simulation: one contended trace vs one optimized trace\ntrace_slow = simulate_checkout_transaction(\"ord-1001\", uuid.uuid4().hex, simulate_contention=True)\ntrace_fast = simulate_checkout_transaction(\"ord-1002\", uuid.uuid4().hex, simulate_contention=False)\n\nprint(\"=== CONTENDED TRACE (Bottleneck in InventoryAllocation) ===\")\nprint(json.dumps(trace_slow, indent=2))\n\nprint(\"\n=== OPTIMIZED TRACE (Non-Blocking Concurrency) ===\")\nprint(json.dumps(trace_fast, indent=2))\n\nassert trace_slow[\"total_duration_ms\"] > 200, \"Slow trace did not capture lock latency!\"\nassert trace_fast[\"total_duration_ms\"] < 100, \"Fast trace exceeded performance threshold!\"\nprint(\"\nPASS: Distributed tracing span waterfall simulation verified.\")\nEOF\npython3 trace_profiler_sim.py\n```",
                    "Author a diagnostic runbook detailing Cloud Trace and Cloud Profiler investigation procedures for P99 latency triage:\n\n```sh\ncat <<'EOF' > day-094-topic-02-latency-triage.md\n# Day 94: Cloud Trace & Cloud Profiler P99 Incident Triage Runbook\n\n## 1. Cloud Trace Diagnostic Workflow\n1. Open Cloud Trace -> Trace Explorer.\n2. Filter by HTTP status code and latency threshold: `+http.status_code:200 +latency:>=3s`.\n3. Select a representative trace from the latency scatter plot.\n4. Examine the span waterfall timeline: identify the span with the longest horizontal bar.\n5. Check span attributes: inspect `db.statement`, `rpc.method`, and `net.peer.name`.\n\n## 2. Cloud Profiler Flame Graph Analysis\n1. Open Cloud Profiler for the affected service (`checkout-service`).\n2. Switch profile view from `CPU time` to `Wall time`.\n3. Locate the widest horizontal frame in the flame graph (widest frame = highest time consumption).\n4. If the widest frame resides in runtime lock functions (`pthread_mutex_lock`, `sync.Mutex.Lock`, `threading.Lock.acquire`), lock contention is the primary root cause.\n5. Switch to `Heap` view to confirm whether memory bloat is triggering GC pauses.\nEOF\ncat day-094-topic-02-latency-triage.md\n```",
                    "Review all output artifacts and confirm that the Python tracing simulator runs successfully and the triage runbook defines exact steps."
                ],
                "verification": "The Python simulation produces valid structured JSON trace hierarchies and the latency triage runbook provides actionable investigation commands.",
                "trouble": "Ensure trace ID generation uses 32-character hexadecimal format conforming to W3C Trace Context specifications.",
                "cleanup": "Retain `day-094-topic-02-latency-triage.md` as an exit evidence artifact.",
                "accept": "Completed distributed trace simulation and verified Profiler triage runbook. File: `day-094-topic-02-trace-profiler.md`.",
                "file": "day-094-topic-02-trace-profiler.md"
            }
        },
        {
            "key": "topic-03",
            "title": "OpenTelemetry Instrumentation and W3C Context Propagation",
            "overview": (
                "OpenTelemetry (OTel) is the vendor-neutral cloud standard for capturing, generating, and exporting telemetry data across distributed "
                "systems. In modern microservice topologies, a user request traverses multiple services, asynchronous message brokers (Pub/Sub, Kafka), "
                "and backend databases. By propagating W3C Trace Context headers (`traceparent` and `tracestate`) across HTTP and gRPC network boundaries "
                "and embedding the extracted `trace_id` into structured application log payloads, OpenTelemetry enables one-click navigation between "
                "a failing log line and the complete distributed transaction waterfall."
            ),
            "preview": (
                "When an asynchronous consumer fails to process an order from Pub/Sub, engineers cannot identify which upstream frontend request submitted it. "
                "OpenTelemetry W3C trace context propagation preserves correlation across asynchronous boundaries, eliminating disconnected debugging."
            ),
            "technical": (
                "### 1. W3C Trace Context Standard (`traceparent` Header)\n"
                "- **Header Structure:** The standard HTTP header `traceparent` uses a versioned 4-part hyphen-delimited format:\n"
                "  `version - trace_id - parent_span_id - trace_flags`\n"
                "  Example: `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`\n"
                "  - `00`: Protocol version.\n"
                "  - `4bf92f3577b34da6a3ce929d0e0e4736`: 16-byte (32-character hex) unique global transaction identifier.\n"
                "  - `00f067aa0ba902b7`: 8-byte (16-character hex) identifier of the calling parent span.\n"
                "  - `01`: Bitfield flags; `01` indicates the trace was sampled for recording.\n\n"
                "### 2. Context Injection and Extraction Across Transport Layers\n"
                "- **HTTP Transports:** HTTP client interceptors inject the `traceparent` header into outgoing request headers; HTTP server interceptors "
                "extract the header upon receiving requests and activate the context in thread-local or async storage.\n"
                "- **Pub/Sub Messaging:** Asynchronous message producers attach `traceparent` as a Pub/Sub message attribute (e.g. `attributes['googclient_OpenTelemetryTraceparent']` "
                "or custom attribute `traceparent`). Downstream pull/push consumers extract this attribute before executing the processing span, "
                "preserving end-to-end parentage across decoupled queues.\n\n"
                "### 3. Trace-Log Correlation Architecture\n"
                "- **Structured Log Enrichment:** Cloud Logging automatically recognizes trace associations when JSON logs contain the key:\n"
                "  `logging.googleapis.com/trace`: `projects/{PROJECT_ID}/traces/{TRACE_ID}`\n"
                "  `logging.googleapis.com/spanId`: `{SPAN_ID}`\n"
                "  `logging.googleapis.com/trace_sampled`: `true`\n"
                "- **Correlated Querying:** With these fields present, selecting any log line in the Logs Explorer displays a direct button: "
                "'View trace for this log entry', opening Cloud Trace centered directly on that exact operation."
            ),
            "questions": [
                "How does the W3C Trace Context `traceparent` specification prevent broken transaction traces across heterogeneous microservices?",
                "What exact JSON fields must be injected into application logs to enable seamless trace-to-log navigation in Google Cloud Logging?",
                "How is trace context preserved across asynchronous, non-HTTP boundaries like Cloud Pub/Sub and Cloud Tasks?",
            ],
            "reference": "https://docs.cloud.google.com/trace/docs/setup/opentelemetry",
            "reference_label": "Google Cloud OpenTelemetry: W3C Trace Context and Cloud Trace exporter setup",
            "scenario": {
                "symptom": (
                    "When an asynchronous payment fulfillment worker in Brightloaf threw fatal database errors, SREs spent 6 hours manually grepping logs "
                    "trying to determine which user order and frontend checkout session initiated the message, as the worker logs contained no customer metadata."
                ),
                "constraints": (
                    "Must link asynchronous Pub/Sub worker failures back to the initiating HTTP session without duplicating customer PII in worker logs."
                ),
                "evidence": (
                    "Frontend checkout logs emitted `trace_id` `8a92b01...`, but the Pub/Sub publish call omitted trace context attributes, "
                    "causing the worker service to generate a brand-new unrelated `trace_id` upon reading the message."
                ),
                "diagnostic_steps": [
                    "Inspect Pub/Sub message attributes published by the frontend checkout service.",
                    "Verify whether the worker service extracts `traceparent` or initializes a root span.",
                    "Review structured JSON log output from both services in Logs Explorer to check for `logging.googleapis.com/trace` presence.",
                ],
                "root": (
                    "Broken trace propagation: the frontend publisher did not inject the active W3C `traceparent` header into the Pub/Sub message attributes, "
                    "severing the distributed trace between the synchronous web app and the asynchronous background worker."
                ),
                "fix": (
                    "Update the Pub/Sub publisher wrapper to inject `traceparent` into message attributes. Configure the subscriber consumer to extract "
                    "the attribute using OpenTelemetry `TraceContextTextMapPropagator` and write the trace URI into all structured log lines."
                ),
                "verify": (
                    "Publish a test order; inspect Logs Explorer and verify both the frontend HTTP log and worker error log share the exact same "
                    "`logging.googleapis.com/trace` identifier and link to the same Cloud Trace diagram."
                ),
                "residual": (
                    "If a third-party non-instrumented queue or legacy proxy strips custom headers, the trace context will be dropped at that hop."
                ),
                "diagram": (
                    "Frontend initiates order",
                    "Trace context stripped at queue",
                    "Worker log isolated & unlinked",
                    "W3C traceparent injected",
                    "Seamless trace-log correlation"
                )
            },
            "lab": {
                "name": "OpenTelemetry W3C Trace Propagation and Structured Log Correlation Implementation",
                "goal": "Build an end-to-end Python pipeline propagating W3C trace context from an HTTP producer to an asynchronous consumer with structured log correlation.",
                "expected": "An executable Python script demonstrating W3C traceparent generation, injection, extraction, and correlated JSON log emission.",
                "mode": "local script execution",
                "prereq": "Understanding of HTTP headers and JSON logging.",
                "preflight": "Ensure Python 3 standard library is present; no cloud dependencies required.",
                "steps": [
                    "Author an end-to-end Python script implementing W3C traceparent injection, message queue propagation, and correlated structured logging:\n\n```sh\ncat <<'EOF' > otel_propagation_lab.py\n# OpenTelemetry W3C Trace Context Propagation & Trace-Log Correlation Simulator\nimport json\nimport time\nimport uuid\n\nPROJECT_ID = \"brightloaf-prod\"\n\nclass W3CTraceContext:\n    def __init__(self, trace_id=None, span_id=None, sampled=True):\n        self.version = \"00\"\n        self.trace_id = trace_id or uuid.uuid4().hex # 32-character hex\n        self.span_id = span_id or uuid.uuid4().hex[:16] # 16-character hex\n        self.flags = \"01\" if sampled else \"00\"\n\n    def to_header(self):\n        return f\"{self.version}-{self.trace_id}-{self.span_id}-{self.flags}\"\n\n    @classmethod\n    def from_header(cls, header_val):\n        parts = header_val.split(\"-\")\n        if len(parts) != 4:\n            raise ValueError(f\"Invalid W3C traceparent header: {header_val}\")\n        return cls(trace_id=parts[1], span_id=parts[2], sampled=(parts[3] == \"01\"))\n\ndef emit_structured_log(message, severity, trace_ctx, child_span_id=None):\n    log_entry = {\n        \"timestamp\": time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime()),\n        \"severity\": severity,\n        \"message\": message,\n        \"logging.googleapis.com/trace\": f\"projects/{PROJECT_ID}/traces/{trace_ctx.trace_id}\",\n        \"logging.googleapis.com/spanId\": child_span_id or trace_ctx.span_id,\n        \"logging.googleapis.com/trace_sampled\": (trace_ctx.flags == \"01\")\n    }\n    return json.dumps(log_entry)\n\n# --- Step 1: Upstream Frontend Service (Producer) ---\nroot_ctx = W3CTraceContext()\nfrontend_span_id = uuid.uuid4().hex[:16]\nprint(\"=== 1. FRONTEND LOG (Initiating Request) ===\")\nprint(emit_structured_log(\"Customer submitted checkout order\", \"INFO\", root_ctx, frontend_span_id))\n\n# Prepare message with W3C traceparent attribute\ntraceparent_header = root_ctx.to_header()\npubsub_message = {\n    \"data\": {\"order_id\": \"ord-9944\", \"amount_usd\": 149.50},\n    \"attributes\": {\n        \"traceparent\": traceparent_header\n    }\n}\nprint(f\"\nPublished Pub/Sub Message with traceparent: {traceparent_header}\")\n\n# --- Step 2: Downstream Worker Service (Consumer) ---\nextracted_ctx = W3CTraceContext.from_header(pubsub_message[\"attributes\"][\"traceparent\"])\nworker_span_id = uuid.uuid4().hex[:16]\nprint(\"\n=== 2. WORKER LOG (Asynchronous Consumer Execution) ===\")\nprint(emit_structured_log(\"Processed order fulfillment from queue\", \"INFO\", extracted_ctx, worker_span_id))\n\n# --- Verification: Assert Trace IDs Match ---\nassert root_ctx.trace_id == extracted_ctx.trace_id, \"FATAL: Trace ID lost across queue!\"\nprint(\"\nPASS: End-to-end W3C trace context propagation and Cloud Logging correlation verified!\")\nEOF\npython3 otel_propagation_lab.py\n```",
                    "Author the redacted diagnostic postmortem artifact fulfilling Day 94 exit evidence:\n\n```sh\ncat <<'EOF' > day-094-topic-03-telemetry-diagnosis.md\n# Day 94: Redacted Distributed Telemetry Diagnostic Report\n\n## 1. Incident Timeline & Telemetry Correlation\n- **2026-09-28T14:15:02Z:** Ingress request `GET /api/v2/cart/checkout` enters Global Cloud Load Balancer with client IP `198.51.100.24`.\n- **2026-09-28T14:15:02.012Z:** API Gateway injects W3C header `traceparent: 00-7f28c19a82e91b...-01` and forwards to frontend service.\n- **2026-09-28T14:15:02.110Z:** Frontend service publishes order payload to Cloud Pub/Sub topic `orders-pending` with `attributes.traceparent` attached.\n- **2026-09-28T14:15:06.320Z:** Downstream fulfillment worker in `us-east1` extracts message; encounters Cloud SQL connection pool saturation.\n- **2026-09-28T14:15:06.325Z:** Worker logs `ERROR: Connection pool exhausted (max 100 connections)`. Log entry contains identical `logging.googleapis.com/trace` ID.\n\n## 2. Causal Hypothesis & Telemetry Evidence\n- **Hypothesis:** Upstream burst of checkout transactions exhausted Cloud SQL connection pool due to un-pooled direct database connections in background worker pods.\n- **Trace Evidence:** Cloud Trace displays a 4,210ms total transaction span, with 4,180ms spent in child span `worker.db_acquire_connection`.\n- **Profile Evidence:** Cloud Profiler wall-time flame graph shows 99% of time in `pgbouncer` client wait loops.\n\n## 3. Telemetry System Limitations\n- **Trace Sampling Gaps:** At 1% probabilistic sampling, 99% of customer requests do not have full waterfall spans; only aggregate metrics and error traces are captured.\n- **Log Retention Boundaries:** Un-filtered debug logs expire after 30 days in the default log bucket unless explicitly captured by compliance sinks.\nEOF\ncat day-094-topic-03-telemetry-diagnosis.md\n```",
                    "Review all output artifacts and confirm that the OpenTelemetry Python simulation runs without error and the redacted diagnosis fulfills the roadmap Exit evidence criteria."
                ],
                "verification": "The OpenTelemetry script confirms W3C header preservation across decoupled message passing and the diagnostic postmortem provides timestamps, causal hypothesis, and telemetry limitations.",
                "trouble": "Ensure `traceparent` uses exactly lowercase hexadecimal characters without extra whitespace or invalid version prefix.",
                "cleanup": "Retain `day-094-topic-03-telemetry-diagnosis.md` as an exit evidence artifact.",
                "accept": "Completed OpenTelemetry propagation script and verified diagnostic postmortem artifact. File: `day-094-topic-03-telemetry-diagnosis.md`.",
                "file": "day-094-topic-03-telemetry-diagnosis.md"
            }
        }
    ]
}
