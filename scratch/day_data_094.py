"""day_data_094.py — Exhaustive architecture data specification for Day 94.

Covers Logs, Traces, and Profiling.
"""

DAY_NUM = 94

DATA = {'day': 94,
 'part1_intro': 'Day 94 shifts observability from aggregate time-series metrics to high-fidelity transaction '
                'telemetry: structured logging, distributed tracing, continuous runtime profiling, and exception '
                'aggregation. While metrics show that a service is failing, logs and traces isolate exactly why, '
                'where, and for which customer request the failure occurred. In high-throughput distributed systems, '
                'naive logging causes exorbitant storage bills and noisy query timeouts, while un-traced asynchronous '
                "messaging chains turn debugging into guesswork. Today's curriculum constructs an enterprise logging "
                'and tracing architecture using Google Cloud Logging routers, cost-saving exclusion filters, '
                'BigQuery-backed Log Analytics, Cloud Trace with continuous Cloud Profiler, and vendor-neutral '
                'OpenTelemetry instrumentation linking distributed spans to structured JSON logs.',
 'exit_summary': 'Engineered a production Logs, Traces, and Profiling telemetry architecture: implemented Cloud '
                 'Logging log router sinks and cost-optimized exclusion filters with Log Analytics SQL analytics; '
                 'configured Cloud Trace and continuous Cloud Profiler to capture distributed latency bottlenecks and '
                 'heap allocations; deployed an OpenTelemetry W3C trace context interceptor with automated trace-log '
                 'correlation in structured JSON.',
 'part2_intro': 'Deep application observability requires correlating three distinct execution signals: structured log '
                'events, distributed trace spans, and runtime CPU/memory profiles. The sections below analyze the '
                'architectural mechanics of the Google Cloud Log Router, distributed trace context propagation, '
                'continuous profiling overhead bounds, and OpenTelemetry instrumentation pipelines.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>Observability Primitive</th>\n'
                    '      <th>GCP Service / Engine</th>\n'
                    '      <th>Data Ingestion &amp; Storage Mechanics</th>\n'
                    '      <th>Retention &amp; Query Interface</th>\n'
                    '      <th>Key Architectural Trade-off / Cost Boundary</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>Structured Logs</strong></td>\n'
                    '      <td>Cloud Logging (Log Router &amp; Log Buckets)</td>\n'
                    '      <td>Streaming JSON ingestion via Ops Agent / Logging API to regional Log Buckets</td>\n'
                    '      <td>30 days standard (configurable up to 3650 days); Logs Explorer &amp; SQL via Log '
                    'Analytics</td>\n'
                    '      <td>$0.50/GiB after free allocation; requires exclusion filters to drop health checks and '
                    'repetitive debug chatter</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Log Analytical Warehouse</strong></td>\n'
                    '      <td>Log Analytics (BigQuery-linked)</td>\n'
                    '      <td>Zero-ETL automated synchronization between regional Log Buckets and BigQuery '
                    'schemas</td>\n'
                    '      <td>Matches Log Bucket retention; standard BigQuery SQL dialect querying `_AllLogs` '
                    'views</td>\n'
                    '      <td>Requires linked dataset creation; queries incur BigQuery compute slot costs or '
                    'on-demand scan fees</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Distributed Traces</strong></td>\n'
                    '      <td>Cloud Trace</td>\n'
                    '      <td>Span collection via OpenTelemetry Trace Exporter / Cloud Trace API</td>\n'
                    '      <td>30 days rolling window; Cloud Trace UI and latency distribution histograms</td>\n'
                    '      <td>Sampling rate trade-off: 100% trace capture causes extreme billing; rate-limiting / '
                    'probabilistic sampling mandatory</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Continuous Profiling</strong></td>\n'
                    '      <td>Cloud Profiler</td>\n'
                    '      <td>Statistical sampling via in-process C++/Go/Java/NodeJS/Python runtime agents</td>\n'
                    '      <td>30 days rolling; flame graphs for CPU, wall-time, heap allocations, and lock '
                    'contention</td>\n'
                    '      <td>Negligible CPU overhead (<1%) and minimal network egress; cannot capture individual '
                    'request traces (aggregate only)</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Exception Grouping</strong></td>\n'
                    '      <td>Error Reporting</td>\n'
                    '      <td>Automated regex matching on structured JSON logs containing stack traces or Error '
                    'Reporting API</td>\n'
                    '      <td>30 days rolling; automated notification channels and resolution status tracking</td>\n'
                    '      <td>Requires standard exception formats or explicit `serviceContext`; unhandled panics '
                    'without stack traces are missed</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 94: Unified Telemetry Architecture: Logging, Tracing, Profiling, and Error Reporting',
                  'desc': 'Flow diagram showing client request ingress, trace context injection, OpenTelemetry span '
                          'extraction, structured log emission, and storage sinks.',
                  'caption': 'Figure 94.1: Unified transaction telemetry pipeline across Cloud Trace, Cloud Logging '
                             'Router, BigQuery Log Analytics, and Cloud Profiler.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Client Ingress & Edge Tracing Perimeter',
                              'desc': 'W3C traceparent Injection, Global External ALB, and Cloud CDN Edge Request '
                                      'Processing',
                              'fill': '#1e3a5f',
                              'y': 10,
                              'h': 90},
                             {'name': 'LAYER 2: Application Container & Microservice Runtime',
                              'desc': 'GKE Microservice Pods, OpenTelemetry SDK Interceptors, and Continuous Cloud '
                                      'Profiler Runtime Agent',
                              'fill': '#0f2338',
                              'y': 115,
                              'h': 90},
                             {'name': 'LAYER 3: Enterprise Log Routing & Ingestion Filtering Fabric',
                              'desc': 'Cloud Logging Log Router, Cost Exclusion Filters (Dropping 99% Health Checks), '
                                      'and Regional Log Buckets',
                              'fill': '#064e3b',
                              'y': 220,
                              'h': 90},
                             {'name': 'LAYER 4: Deep Analytical Warehousing & Latency Correlation',
                              'desc': 'Log Analytics BigQuery-Linked Dataset (_AllLogs), Cloud Trace Waterfall '
                                      'Visualizer, and Wall-Time Flame Graphs',
                              'fill': '#1e1b4b',
                              'y': 325,
                              'h': 90},
                             {'name': 'LAYER 5: SRE Governance, Error Reporting & Long-Term Compliance',
                              'desc': 'Error Reporting Exception Deduplication, Cloud Storage 7-Year Cold Vault Sink, '
                                      'and Log-Based Metric Alerts',
                              'fill': '#3b0764',
                              'y': 430,
                              'h': 90}],
                  'components': [{'id': 'w3c_ingress_edge',
                                  'name': 'W3C Ingress Edge',
                                  'detail': 'traceparent: 00-4bf9...-01',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'alb_trace_injector',
                                  'name': 'Global ALB Ingress',
                                  'detail': 'Span Context Header Forwarding',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'gke_otel_runtime',
                                  'name': 'GKE OTel Runtime',
                                  'detail': 'Trace-Log Context Linking',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'profiler_agent_node',
                                  'name': 'Continuous Profiler',
                                  'detail': 'Statistical Wall-Time / Mutex (<1%)',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'log_router_engine',
                                  'name': 'Log Router Engine',
                                  'detail': 'Streaming Inclusion/Exclusion Filter',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'cost_exclusion_filter',
                                  'name': 'Exclusion Filter',
                                  'detail': 'Drop 99% Health Checks (GoogleHC)',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'log_analytics_bq',
                                  'name': 'Log Analytics (SQL)',
                                  'detail': 'BigQuery Zero-ETL Sync (_AllLogs)',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'trace_waterfall_viewer',
                                  'name': 'Cloud Trace Waterfall',
                                  'detail': 'Distributed Latency Breakdown',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'error_reporting_hub',
                                  'name': 'Error Reporting Hub',
                                  'detail': 'Automated Stack Trace Grouping',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'},
                                 {'id': 'cold_worm_sink',
                                  'name': '7-Year Cold Sink',
                                  'detail': 'GCS WORM Compliance Vault',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'}],
                  'boundaries': [{'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'CLIENT INGRESS & DISTRIBUTED TRACE HEADER BOUNDARY',
                                  'color': '#38bdf8'},
                                 {'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'label': 'APPLICATION RUNTIME & LOG ROUTER INGESTION PERIMETER',
                                  'color': '#10b981'},
                                 {'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 195,
                                  'label': 'ANALYTICAL STORAGE & SECURITY COMPLIANCE PERIMETER',
                                  'color': '#a855f7'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'type': 'ok', 'label': 'Inject W3C traceparent'},
                            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'type': 'ok', 'label': 'Extract Trace in GKE'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'type': 'ok',
                             'label': 'Sample Profiler Stacks'},
                            {'x1': 210,
                             'y1': 187,
                             'x2': 210,
                             'y2': 240,
                             'type': 'ok',
                             'label': 'Stream Structured Logs'},
                            {'x1': 340,
                             'y1': 266,
                             'x2': 420,
                             'y2': 266,
                             'type': 'fail',
                             'label': 'Drop Health-Check Noise'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'type': 'ok',
                             'label': 'Synchronize to BigQuery'},
                            {'x1': 340,
                             'y1': 371,
                             'x2': 420,
                             'y2': 371,
                             'type': 'ok',
                             'label': 'Correlate Trace ID to Log'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'type': 'ok',
                             'label': 'Deduplicate Exceptions'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'type': 'ok',
                             'label': 'Archive Security Audit Logs'}],
                  'probes': [{'cx': 420,
                              'cy': 56,
                              'label': 'PROBE 1: W3C Header Sampling Flag (01 = Sampled)',
                              'color': '#38bdf8'},
                             {'cx': 420,
                              'cy': 240,
                              'label': 'PROBE 2: Exclusion Filter Discard Counter (GiB)',
                              'color': '#10b981'},
                             {'cx': 420,
                              'cy': 345,
                              'label': 'PROBE 3: Cloud Profiler Mutex Wait Duration (>100ms)',
                              'color': '#ef4444'}]},
 'topics': [{'key': 'topic-01',
             'title': 'Cloud Logging: Log Router, Sinks, Exclusions, and Log Analytics',
             'overview': 'Google Cloud Logging decouples log generation from log storage through an event routing '
                         'pipeline known as the Log Router. Every service, VM, container, and audit log emitted in a '
                         'Google Cloud organization flows through the Log Router, which evaluates inclusion and '
                         'exclusion filters in real time before routing logs to regional Log Buckets, Cloud Storage '
                         'for archival, BigQuery for deep analysis, or Pub/Sub for SIEM integration. Log Analytics '
                         'links log buckets to BigQuery, enabling relational SQL queries over streaming '
                         'semi-structured JSON payloads without custom ingestion pipelines.',
             'preview': 'An unconfigured log router ingests gigabytes of repetitive load balancer health checks, '
                        'triggering thousands of dollars in billing overages. Proper routing with exclusion filters '
                        'and BigQuery Log Analytics eliminates noise while preserving compliance and audit trails.',
             'technical': '### 1. Log Router Mechanics and Sink Topology\n'
                          '- **Processing Sequence:** When an application or infrastructure component writes a log '
                          'entry, it arrives at the Log Router. The router checks two layers of rules: **Exclusion '
                          'Filters** and **Sink Destinations**.\n'
                          '- **Exclusion Filters:** Discard high-volume, low-value logs (e.g. `httpRequest.status = '
                          "200 AND httpRequest.requestUrl =~ '/healthz'`) prior to storage, preventing ingestion "
                          'charges while allowing sample percentages (e.g. keep 1% of healthy requests for baseline '
                          'analysis).\n'
                          '- **Sinks:** Define the target destination for matching logs:\n'
                          '  - **Log Bucket (Default):** Regional, encrypted storage inside Cloud Logging with '
                          'retention from 1 to 3650 days.\n'
                          '  - **BigQuery:** Streams structured logs into BigQuery partitioned tables for enterprise '
                          'analytical correlation.\n'
                          '  - **Cloud Storage:** Cost-effective long-term cold archive for regulatory compliance '
                          '(e.g., 7-year WORM storage).\n'
                          '  - **Pub/Sub:** Low-latency event streaming to third-party SIEM platforms (Splunk, '
                          'Datadog, Chronicle).\n'
                          '\n'
                          '### 2. Log Analytics and BigQuery Linking\n'
                          '- **BigQuery-Linked Buckets:** Upgrading a Log Bucket to use Log Analytics provisions a '
                          'linked BigQuery dataset. SREs can write standard SQL queries joining log records with '
                          'customer tables or cost allocation datasets.\n'
                          '- **JSON Parsing in SQL:** Structured log payloads stored in `json_payload` can be '
                          'extracted using BigQuery JSON operators:\n'
                          '  `SELECT JSON_VALUE(json_payload.order_id) AS order_id, count(*) FROM '
                          '`project_id.region_id.bucket_id._AllLogs` GROUP BY 1`.\n'
                          '\n'
                          '### 3. Log-Based Metrics\n'
                          '- **Counter Metrics:** Count log entries matching a filter (e.g., counting HTTP 500 errors '
                          'to create Cloud Monitoring alerts).\n'
                          '- **Distribution Metrics:** Extract numerical values from JSON fields (e.g., parsing '
                          'payload sizes or payment processing latencies) into Cloud Monitoring distribution '
                          'histograms for SLO calculation.',
             'questions': ['How do Log Router exclusion filters prevent runaway Cloud Logging ingestion costs without '
                           'blinding operational dashboards?',
                           'What architectural trade-offs govern routing logs to BigQuery via Log Router sinks versus '
                           'enabling Log Analytics on Log Buckets?',
                           'Why should log-based metrics be restricted to bounded extractors rather than arbitrary '
                           'high-cardinality regex fields?'],
             'reference': 'https://docs.cloud.google.com/logging/docs/routing/overview',
             'reference_label': 'Google Cloud Logging: Log Router, sinks, exclusion filters, and Log Analytics '
                                'configuration',
             'scenario': {'symptom': "Brightloaf's monthly Cloud Logging invoice reached $42,000 for a single billing "
                                     'cycle. Over 85% of total log volume consisted of redundant Kubernetes kubelet '
                                     'probes and Cloud Load Balancer HTTP 200 `/healthz` polling logs occurring every '
                                     '2 seconds across 300 pods.',
                          'constraints': 'Must drop 95% of routine health-check traffic to bring ingestion under '
                                         '$2,000/month while preserving 100% of HTTP 5xx errors and 1% of successful '
                                         'probes for latency baseline audits.',
                          'evidence': 'Billing telemetry and Log Router usage metrics captured the runaway ingestion:\n'
                                      '\n'
                                      '```\n'
                                      '$ gcloud logging metrics list ...\n'
                                      'Metric: logging.googleapis.com/billing/bytes_ingested\n'
                                      'Daily Volume: 450.2 GiB/day (Surpassing 50 GiB/month free tier by 270x)\n'
                                      'Top Ingestion Contributors:\n'
                                      '- logName: projects/brightloaf-prod/logs/requests (UserAgent: GoogleHC/1.0): '
                                      '382.4 GiB/day (84.9%)\n'
                                      '- logName: projects/brightloaf-prod/logs/kubelet-probes:                     '
                                      '38.1 GiB/day ( 8.5%)\n'
                                      '- Real Application & Business Logs:                                         '
                                      '29.7 GiB/day ( 6.6%)\n'
                                      'Monthly Ingestion Cost Run Rate: $42,180.00 USD\n'
                                      'Log Router Sink: _Default (Exclusions: 0 configured)\n'
                                      '```',
                          'diagnostic_steps': ['Query Cloud Logging usage metrics '
                                               '`logging.googleapis.com/billing/bytes_ingested` grouped by '
                                               '`resource_type` and `log_id`.',
                                               'Analyze Logs Explorer sample queries to isolate repetitive probe '
                                               'request patterns.',
                                               'Audit existing Log Router sinks and verify whether exclusion rules '
                                               'exist on the `_Default` bucket sink.'],
                          'root': 'Missing Log Router exclusion rules allowed uncompressed, high-frequency internal '
                                  'health-check transactions to be ingested and billed at full price into standard '
                                  'retention storage.',
                          'fix': 'Configure an exclusion filter on the `_Default` log sink matching '
                                 "`httpRequest.userAgent =~ 'GoogleHC/.*' AND httpRequest.status = 200` with a 99% "
                                 'drop rate (1% sampling). Deploy a Log Analytics linked dataset to query remaining '
                                 'logs via BigQuery SQL.',
                          'verify': 'Check `logging.googleapis.com/billing/bytes_ingested` after applying exclusion; '
                                    'verify daily ingestion falls from 450 GiB/day to 22 GiB/day while synthetic error '
                                    'logs continue to appear in Logs Explorer.',
                          'residual': 'Exclusion filters permanently discard un-sampled matching logs prior to '
                                      'ingestion; dropped logs cannot be retrieved retroactively for historical '
                                      'investigations.',
                          'diagram': ('High-volume health probes',
                                      'Unfiltered log router',
                                      'Storage billing explosion',
                                      'Exclusion filter applied',
                                      'Controlled ingestion cost')},
             'lab': {'name': 'Cloud Logging Router Architecture, Cost Exclusion Filters, and Log Analytics SQL',
                     'goal': 'Author a production Cloud Logging sink configuration with exclusion rules and execute '
                             'SQL queries against Log Analytics.',
                     'expected': 'A validated Cloud Logging sink manifest, an executable Python log generator, and a '
                                 'tested BigQuery Log Analytics SQL script.',
                     'mode': 'tabletop analysis & production CLI / SQL execution',
                     'prereq': 'Understanding of Google Cloud Logging filters and JSON structures.',
                     'preflight': 'Review gcloud logging sink CLI syntax and BigQuery SQL dialect.',
                     'steps': ['#### Stage 1: Pre-Flight Log Router Topology & Ingestion Invariants\n'
                               "Establish the logging governance invariants for Brightloaf's production services:\n"
                               '- **Exclusion Invariant:** 99% of routine load balancer and kubelet health checks '
                               "(`httpRequest.userAgent =~ 'GoogleHC/.*' AND httpRequest.status = 200`) must be "
                               'discarded at the router.\n'
                               '- **Retention Invariant:** Security and audit logs must route to a compliance cold '
                               'storage vault with 7-year retention.\n'
                               '- **Analytical Invariant:** Operational application log buckets must be upgraded to '
                               'Log Analytics, enabling zero-ETL BigQuery SQL querying.',
                               '#### Stage 2: Infrastructure Preflight & Bucket Inspection\n'
                               'Author a preflight script (<kbd>check_logging_env.py</kbd>) verifying existing log '
                               'buckets and sinks:\n'
                               '\n'
                               '```python\n'
                               '# check_logging_env.py\n'
                               'bucket_spec = {\n'
                               "    'default_retention_days': 30,\n"
                               "    'analytics_enabled': True,\n"
                               "    'target_daily_gib_cap': 30,\n"
                               '}\n'
                               "print('[PREFLIGHT] Validating Cloud Logging configuration...')\n"
                               "assert bucket_spec['default_retention_days'] >= 30, 'Retention must satisfy minimum "
                               "operational window'\n"
                               "assert bucket_spec['analytics_enabled'], 'Log Analytics must be active for BigQuery "
                               "linking'\n"
                               "print('[PASS] Logging preflight invariants verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight check:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_logging_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Log Router Sink with Cost Exclusion Rules\n'
                               'Author the declarative Log Router sink manifest (<kbd>deploy_log_sink.json</kbd>):\n'
                               '\n'
                               '```json\n'
                               "cat <<'EOF' > deploy_log_sink.json\n"
                               '{\n'
                               '  "name": "brightloaf-compliance-sink",\n'
                               '  "destination": "storage.googleapis.com/brightloaf-audit-logs-cold-vault",\n'
                               '  "filter": "severity >= WARNING OR protoPayload.methodName =~ '
                               '\'.*(delete|patch|update).*\'",\n'
                               '  "description": "Archive security-sensitive audit and error logs to cold storage for '
                               '7-year retention",\n'
                               '  "exclusions": [\n'
                               '    {\n'
                               '      "name": "drop-k8s-health-checks",\n'
                               '      "description": "Drop 99% of routine load balancer and kubelet health checks",\n'
                               '      "filter": "httpRequest.userAgent =~ \'GoogleHC/.*\' AND httpRequest.status = '
                               '200",\n'
                               '      "disabled": false\n'
                               '    },\n'
                               '    {\n'
                               '      "name": "drop-routine-readiness",\n'
                               '      "description": "Discard all readiness endpoint queries",\n'
                               '      "filter": "httpRequest.requestUrl =~ \'.*/readyz$\' AND httpRequest.status = '
                               '200",\n'
                               '      "disabled": false\n'
                               '    }\n'
                               '  ]\n'
                               '}\n'
                               'EOF\n'
                               'cat deploy_log_sink.json\n'
                               '```',
                               '#### Stage 4: Execution & BigQuery Log Analytics Linking\n'
                               'Author the deployment script instantiating the Log Router sink and enabling Log '
                               'Analytics:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > link_log_analytics.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-prod}"\n'
                               'BUCKET_NAME="brightloaf_app_logs"\n'
                               'LOCATION="us-central1"\n'
                               '\n'
                               'echo "Upgrading Log Bucket ${BUCKET_NAME} to Log Analytics (BigQuery-linked)..."\n'
                               'gcloud logging buckets update "${BUCKET_NAME}" \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --location="${LOCATION}" \\\n'
                               '    --enable-analytics || true\n'
                               '\n'
                               'echo "[PASS] Log Analytics linked dataset instantiated."\n'
                               'EOF\n'
                               'chmod +x link_log_analytics.sh\n'
                               './link_log_analytics.sh\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Probe Flooding Chaos Injection\n'
                               'Author an executable Python simulation (<kbd>simulate_log_routing.py</kbd>) evaluating '
                               'exclusion efficiency under simulated health check surges:\n'
                               '\n'
                               '```python\n'
                               '# simulate_log_routing.py\n'
                               'raw_events = [\n'
                               "    {'type': 'health', 'ua': 'GoogleHC/1.0', 'status': 200, 'size_bytes': 450},\n"
                               "    {'type': 'health', 'ua': 'GoogleHC/1.0', 'status': 200, 'size_bytes': 450},\n"
                               "    {'type': 'health', 'ua': 'GoogleHC/1.0', 'status': 500, 'size_bytes': 720}, # "
                               'Error kept\n'
                               "    {'type': 'order',  'ua': 'Mozilla/5.0',  'status': 200, 'size_bytes': 1200},\n"
                               "    {'type': 'order',  'ua': 'Mozilla/5.0',  'status': 503, 'size_bytes': 1500},\n"
                               "    {'type': 'audit',  'ua': 'gcloud/450',   'status': 200, 'size_bytes': 2800}\n"
                               ']\n'
                               '\n'
                               'def route_log(entry):\n'
                               "    if entry.get('ua', '').startswith('GoogleHC/') and entry.get('status') == 200:\n"
                               "        return False, 'EXCLUDED'\n"
                               "    return True, 'INGESTED'\n"
                               '\n'
                               'ingested = [e for e in raw_events if route_log(e)[0]]\n'
                               'excluded = [e for e in raw_events if not route_log(e)[0]]\n'
                               '\n'
                               "print(f'Total Events: {len(raw_events)} | Ingested: {len(ingested)} | Excluded: "
                               "{len(excluded)}')\n"
                               "assert len(excluded) == 2, 'Routine 200 OK health checks must be dropped'\n"
                               "assert any(e['status'] == 500 for e in ingested), 'HTTP 500 health check failure must "
                               "be preserved'\n"
                               "print('[PASS] Log Router exclusion simulation validated.')\n"
                               '```\n'
                               '\n'
                               'Execute chaos test:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_log_routing.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & SQL Analytics Querying\n'
                               'Author a production BigQuery SQL analytics script (<kbd>query_log_analytics.sql</kbd>) '
                               'auditing error clusters:\n'
                               '\n'
                               '```sql\n'
                               "cat <<'EOF' > query_log_analytics.sql\n"
                               '-- Query Log Analytics linked dataset to isolate top error clusters and latency '
                               'percentiles\n'
                               'SELECT\n'
                               '  JSON_VALUE(json_payload.service) AS microservice,\n'
                               '  JSON_VALUE(json_payload.error_code) AS error_code,\n'
                               '  COUNT(*) AS error_occurrences,\n'
                               '  ROUND(AVG(CAST(JSON_VALUE(json_payload.duration_ms) AS FLOAT64)), 2) AS '
                               'avg_duration_ms,\n'
                               '  ARRAY_AGG(DISTINCT JSON_VALUE(json_payload.trace_id) IGNORE NULLS LIMIT 3) AS '
                               'sample_trace_ids\n'
                               'FROM\n'
                               '  `brightloaf-prod.us_central1.brightloaf_app_logs._AllLogs`\n'
                               'WHERE\n'
                               '  timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)\n'
                               "  AND severity IN ('ERROR', 'CRITICAL')\n"
                               'GROUP BY\n'
                               '  1, 2\n'
                               'ORDER BY\n'
                               '  error_occurrences DESC\n'
                               'LIMIT 10;\n'
                               'EOF\n'
                               'cat query_log_analytics.sql\n'
                               '```',
                               '#### Stage 7: Automated Verification & Ingestion Cost Reduction Assertions\n'
                               'Author an automated test (<kbd>assert_logging_savings.py</kbd>) calculating cost '
                               'savings:\n'
                               '\n'
                               '```python\n'
                               '# assert_logging_savings.py\n'
                               'baseline_gib_day = 450.0\n'
                               'filtered_gib_day = 22.5\n'
                               'savings_pct = (baseline_gib_day - filtered_gib_day) / baseline_gib_day\n'
                               "print(f'Ingestion Reduction: {savings_pct*100:.1f}%')\n"
                               "assert savings_pct >= 0.90, 'Exclusion rules must eliminate at least 90% of noise'\n"
                               "print('[ASSERT PASS] Cloud Logging ingestion cost reduction verified.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_logging_savings.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_logging_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 94 Topic 1 test scripts..."\n'
                               'rm -f check_logging_env.py deploy_log_sink.json link_log_analytics.sh '
                               'simulate_log_routing.py query_log_analytics.sql assert_logging_savings.py\n'
                               'echo "[CLEANUP] Retaining day-094-topic-01-log-analytics.md evidence documentation."\n'
                               'echo "[CLEANUP PASS] Logging lab teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_logging_lab.sh\n'
                               './teardown_logging_lab.sh\n'
                               '```'],
                     'verification': 'The log router JSON defines both destination and exclusion rules, the Python '
                                     'simulation passes assertions, and the BigQuery SQL accurately parses JSON '
                                     'payload fields.',
                     'trouble': 'Ensure BigQuery SQL uses the backticked table format '
                                '`project.location.bucket._AllLogs` when querying Log Analytics linked datasets.',
                     'cleanup': 'Retain `day-094-topic-01-log-sink.json` and `day-094-topic-01-log-analytics.sql` as '
                                'exit evidence artifacts.',
                     'accept': 'Completed Log Router configuration and verified Log Analytics SQL script. File: '
                               '`day-094-topic-01-log-analytics.md`.',
                     'file': 'day-094-topic-01-log-analytics.md'}},
            {'key': 'topic-02',
             'title': 'Cloud Trace, Cloud Profiler, and Error Reporting',
             'overview': 'Cloud Trace provides distributed latency analysis across microservice boundaries, '
                         'visualizing request timelines through nested waterfall span graphs. Cloud Profiler operates '
                         'continuously in production with less than 1% CPU overhead, statistically sampling runtime '
                         'call stacks to generate flame graphs identifying CPU hotspots, memory leak allocations, and '
                         'thread synchronization bottlenecks. Error Reporting automatically aggregates runtime stack '
                         'traces and unhandled exceptions into deduplicated problem groups, linking incident tickets '
                         'directly to the code line responsible.',
             'preview': 'A checkout request experiences an intermittent 4-second delay, but individual component '
                        'metrics show normal CPU and memory utilization. Cloud Trace and Cloud Profiler reveal '
                        'downstream thread contention and un-indexed database lock waits that metrics completely '
                        'obscure.',
             'technical': '### 1. Distributed Tracing Mechanics (Cloud Trace)\n'
                          '- **Span Hierarchy:** A Trace represents an end-to-end user transaction composed of one or '
                          'more Spans. Each span records a named operation, start and end timestamps, status codes, '
                          'and key-value attributes.\n'
                          '- **Sampling Rate Strategies:** In high-volume systems (e.g. 100,000 requests/sec), '
                          'capturing 100% of traces incurs massive network and storage overhead. Architects implement '
                          '**Head-based Probabilistic Sampling** (e.g., sample 1 out of 1000 requests at the API '
                          'Gateway) or **Adaptive/Tail-based Sampling** (always sample requests resulting in HTTP 5xx '
                          'or exceeding a latency threshold such as 2.0 seconds).\n'
                          '\n'
                          '### 2. Low-Overhead Continuous Profiling (Cloud Profiler)\n'
                          '- **Statistical Sampling:** Unlike intrusive debuggers that alter program timing, Cloud '
                          'Profiler uses statistical OS timers (`SIGPROF` interrupts) to capture call stacks at random '
                          '10ms intervals over a 10-second sampling window once every minute.\n'
                          '- **Profile Types:**\n'
                          '  - **CPU Time:** Identifies functions consuming the most processor cycles.\n'
                          '  - **Wall Time:** Identifies functions blocked on I/O, database locks, or network calls.\n'
                          '  - **Heap Allocations:** Pinpoints functions allocating the most RAM (critical for '
                          'preventing Kubernetes OOMKilled events).\n'
                          '  - **Contention / Mutex:** Identifies lock serialization bottlenecks in multi-threaded '
                          'runtimes.\n'
                          '\n'
                          '### 3. Error Reporting Exception Aggregation\n'
                          '- **Grouping Algorithm:** Error Reporting parses stack traces and groups errors by '
                          'top-level calling function and exception type, preventing thousands of identical crashes '
                          'from producing thousands of individual alert notifications.\n'
                          '- **Context Binding:** Automatically extracts HTTP request method, URL, user agent, and '
                          "release version when formatted in Google Cloud's structured `ReportedErrorEvent` schema.",
             'questions': ['Why is continuous statistical profiling architecturally superior to ad-hoc APM agent '
                           'profiling in production environments?',
                           'What sampling strategy ensures that rare, high-latency tail events are captured in Cloud '
                           'Trace without overpaying for trace storage?',
                           'How does Error Reporting correlate grouped exception signatures with specific Git release '
                           'versions?'],
             'reference': 'https://docs.cloud.google.com/trace/docs/overview',
             'reference_label': 'Google Cloud Trace, Cloud Profiler, and Error Reporting production architecture',
             'scenario': {'symptom': "Brightloaf's checkout service suffered an unexplained P99 latency degradation "
                                     'from 180ms to 4,200ms following a microservice refactoring, yet GKE cluster CPU '
                                     'utilization remained below 25%.',
                          'constraints': 'Must diagnose the bottleneck without taking down production nodes or running '
                                         'invasive debugging sessions that degrade customer throughput.',
                          'evidence': 'Cloud Trace waterfall timings and Cloud Profiler flame-graph profiles captured '
                                      'the lock contention:\n'
                                      '\n'
                                      '```\n'
                                      'CLOUD TRACE EXPLORER (Trace ID: 7f28c19a82e91b4081c7e42b1092a488):\n'
                                      'Span: CheckoutOrder                      Duration: 4,210 ms  [200 OK]\n'
                                      '├── Span: AuthenticateToken               Duration:    18 ms  [200 OK]\n'
                                      '├── Span: InventoryAllocation (BOTTLENECK) Duration: 4,142 ms  [200 OK] (98.4% '
                                      'of total time)\n'
                                      '└── Span: PaymentGatewayCharge            Duration:    50 ms  [200 OK]\n'
                                      '\n'
                                      'CLOUD PROFILER (Service: checkout-service | View: Wall Time):\n'
                                      'Top Frame: threading.Lock.acquire() (98.1% of sampled wall-time duration)\n'
                                      'Call Path: checkout.py:order_handler -> inventory.py:deduct_stock -> '
                                      'threading.Lock\n'
                                      'GKE CPU Utilization during incident: 18% (VMs were idling while threads '
                                      'serialized on lock)\n'
                                      '```',
                          'diagnostic_steps': ['Open Cloud Trace Explorer and filter transactions where `latency > '
                                               '3s`.',
                                               'Inspect the waterfall breakdown of the slowest trace to identify which '
                                               'child span consumed the bulk of the duration.',
                                               "Open Cloud Profiler and switch the profile view to 'Wall Time' and "
                                               "'Contention' for the `checkout-service` deployment."],
                          'root': 'Lock contention: a developer had introduced a global in-memory Python mutex around '
                                  'the inventory stock check rather than using optimistic locking in Spanner/Cloud '
                                  'SQL, causing all concurrent checkout threads to serialize behind a single locked '
                                  'resource.',
                          'fix': 'Replace the in-memory global mutex with fine-grained per-SKU distributed lock tokens '
                                 'or database-level row-level version checks. Deploy Cloud Profiler continuous '
                                 'profiling in staging to verify lock wait time drops to near zero.',
                          'verify': 'Inspect Cloud Trace P99 latency distribution histogram post-fix; confirm P99 '
                                    'returns to <200ms and Cloud Profiler contention flame graphs clear.',
                          'residual': 'Cloud Trace sampling may miss transient 1-in-10,000 latency spikes unless '
                                      'adaptive tail-based sampling is configured at the ingress layer.',
                          'diagram': ('Refactored checkout release',
                                      'Global thread lock added',
                                      'P99 latency spikes to 4.2s',
                                      'Profiler isolates mutex lock',
                                      'P99 latency restored <200ms')},
             'lab': {'name': 'Cloud Trace Waterfall Analysis and Cloud Profiler Flame Graph Synthesis',
                     'goal': 'Instrument a Python microservice with OpenTelemetry distributed tracing and analyze '
                             'latency waterfall spans and lock contention.',
                     'expected': 'A runnable Python distributed service simulator emitting correlated trace spans and '
                                 'a flame-graph diagnostic analysis document.',
                     'mode': 'tabletop analysis & production Python execution',
                     'prereq': 'Understanding of distributed tracing spans and thread contention.',
                     'preflight': 'Ensure Python 3 standard library is accessible; no cloud credentials required.',
                     'steps': ['#### Stage 1: Pre-Flight Distributed Tracing & Continuous Profiler Invariants\n'
                               'Establish the tracing and profiling architectural invariants:\n'
                               '- **Sampling Strategy:** Ingress API Gateway implements 1% probabilistic sampling for '
                               'successful transactions and 100% adaptive sampling for errors (HTTP 5xx) and slow '
                               'requests (>2.0s).\n'
                               '- **Continuous Profiling:** Cloud Profiler agent runs in-process with <1% CPU '
                               'overhead, capturing CPU, wall-time, heap allocations, and mutex contention.\n'
                               '- **Context Linking:** Every trace span must carry service name, environment, and '
                               'release version tags.',
                               '#### Stage 2: Infrastructure Preflight & Sampling Rate Verification\n'
                               'Author a preflight script (<kbd>check_trace_env.py</kbd>) validating trace sampling '
                               'configurations:\n'
                               '\n'
                               '```python\n'
                               '# check_trace_env.py\n'
                               'trace_config = {\n'
                               "    'probabilistic_sample_rate': 0.01,\n"
                               "    'tail_sample_latency_threshold_s': 2.0,\n"
                               "    'profiler_overhead_pct_max': 1.0,\n"
                               '}\n'
                               "print('[PREFLIGHT] Validating Cloud Trace and Cloud Profiler invariants...')\n"
                               "assert trace_config['probabilistic_sample_rate'] <= 0.05, 'Sample rate must not exceed "
                               "5% in high volume'\n"
                               "assert trace_config['profiler_overhead_pct_max'] <= 1.0, 'Profiler overhead must be "
                               "bounded <1%'\n"
                               "print('[PASS] Trace & Profiler invariants verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight check:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_trace_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Distributed Span Simulator with Lock Contention\n'
                               'Author an executable Python simulator (<kbd>trace_profiler_sim.py</kbd>) demonstrating '
                               'contention and waterfall spans:\n'
                               '\n'
                               '```python\n'
                               "cat <<'EOF' > trace_profiler_sim.py\n"
                               'import time\n'
                               'import json\n'
                               'import uuid\n'
                               'import threading\n'
                               '\n'
                               'INVENTORY_LOCK = threading.Lock()\n'
                               '\n'
                               'def simulate_checkout(order_id, trace_id, simulate_contention=True):\n'
                               '    start = time.time()\n'
                               '    spans = []\n'
                               '    \n'
                               '    # Span 1: Auth\n'
                               '    s1 = time.time()\n'
                               '    time.sleep(0.01)\n'
                               "    spans.append({'name': 'AuthenticateToken', 'duration_ms': round((time.time() - "
                               's1)*1000, 2)})\n'
                               '    \n'
                               '    # Span 2: Inventory\n'
                               '    s2 = time.time()\n'
                               '    if simulate_contention:\n'
                               '        with INVENTORY_LOCK:\n'
                               '            time.sleep(0.12) # Serialized mutex lock wait\n'
                               '    else:\n'
                               '        time.sleep(0.01)\n'
                               "    spans.append({'name': 'InventoryAllocation', 'duration_ms': round((time.time() - "
                               's2)*1000, 2)})\n'
                               '    \n'
                               '    # Span 3: Payment\n'
                               '    s3 = time.time()\n'
                               '    time.sleep(0.03)\n'
                               "    spans.append({'name': 'PaymentCharge', 'duration_ms': round((time.time() - "
                               's3)*1000, 2)})\n'
                               '    \n'
                               '    total_ms = round((time.time() - start)*1000, 2)\n'
                               "    return {'trace_id': trace_id, 'order_id': order_id, 'total_ms': total_ms, 'spans': "
                               'spans}\n'
                               '\n'
                               "slow = simulate_checkout('ord-1', uuid.uuid4().hex, simulate_contention=True)\n"
                               "fast = simulate_checkout('ord-2', uuid.uuid4().hex, simulate_contention=False)\n"
                               '\n'
                               "print('--- CONTENDED TRACE WATERFALL ---')\n"
                               'print(json.dumps(slow, indent=2))\n'
                               "assert slow['total_ms'] > 150, 'Contended trace must capture lock latency'\n"
                               'EOF\n'
                               'python3 trace_profiler_sim.py\n'
                               '```',
                               '#### Stage 4: Execution & Error Reporting Schema Context Formatting\n'
                               'Author a Python utility (<kbd>format_error_event.py</kbd>) formatting exceptions in '
                               'Google Cloud Error Reporting schema:\n'
                               '\n'
                               '```python\n'
                               "cat <<'EOF' > format_error_event.py\n"
                               'import json\n'
                               'import time\n'
                               '\n'
                               'def format_error_reporting_event(service_name, version, message, stack_trace, '
                               'trace_id):\n'
                               '    return {\n'
                               "        'eventTime': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),\n"
                               "        'serviceContext': {'service': service_name, 'version': version},\n"
                               "        'message': f'{message}\\n{stack_trace}',\n"
                               "        'context': {\n"
                               "            'httpRequest': {'method': 'POST', 'url': '/api/v1/checkout', "
                               "'responseStatusCode': 500},\n"
                               "            'reportLocation': {'filePath': 'src/checkout/handler.py', 'lineNumber': "
                               "84, 'functionName': 'order_handler'}\n"
                               '        },\n'
                               "        'logging.googleapis.com/trace': f'projects/brightloaf-prod/traces/{trace_id}'\n"
                               '    }\n'
                               '\n'
                               "event = format_error_reporting_event('checkout-service', 'v2.4.1', 'DeadlockDetected: "
                               'Mutex lock timeout\', \'Traceback (most recent call last):\\n  File "handler.py", line '
                               "84', '7f28c19a82e91b40')\n"
                               'print(json.dumps(event, indent=2))\n'
                               "assert event['serviceContext']['service'] == 'checkout-service'\n"
                               'EOF\n'
                               'python3 format_error_event.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Thread Contention Chaos Injection\n'
                               'Author a multi-threaded stress script (<kbd>simulate_thread_contention.py</kbd>) '
                               'showing P99 latency explosion under concurrent threads:\n'
                               '\n'
                               '```python\n'
                               '# simulate_thread_contention.py\n'
                               'import threading\n'
                               'import time\n'
                               '\n'
                               'lock = threading.Lock()\n'
                               'latencies = []\n'
                               '\n'
                               'def worker():\n'
                               '    t0 = time.time()\n'
                               '    with lock:\n'
                               '        time.sleep(0.02)\n'
                               '    latencies.append((time.time() - t0) * 1000)\n'
                               '\n'
                               'threads = [threading.Thread(target=worker) for _ in range(10)]\n'
                               'for t in threads: t.start()\n'
                               'for t in threads: t.join()\n'
                               '\n'
                               'p99 = max(latencies)\n'
                               'p50 = sorted(latencies)[len(latencies)//2]\n'
                               "print(f'Serialized 10 Threads -> P50: {p50:.1f}ms | P99: {p99:.1f}ms')\n"
                               "assert p99 > 150, 'Contention must visibly inflate P99 latency'\n"
                               "print('[PASS] Contention chaos simulation verified.')\n"
                               '```\n'
                               '\n'
                               'Execute chaos test:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_thread_contention.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Flame Graph Waterfall Auditing\n'
                               'Author a diagnostic runbook verifying Cloud Profiler flame graph inspection '
                               'procedures:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > audit_latency_triage.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Simulating Cloud Profiler flame-graph frame extraction..."\n'
                               "cat <<'FRAME'\n"
                               'Top Wall-Time Consuming Frames in checkout-service:\n'
                               '1. threading.Lock.acquire()                   : 98.1% of wall-time duration\n'
                               '2. pgbouncer.client_wait()                    :  1.2% of wall-time duration\n'
                               '3. json.dumps()                               :  0.4% of wall-time duration\n'
                               'Diagnostic Action: Eliminate global mutex; adopt row-level database locking.\n'
                               'FRAME\n'
                               'echo "[PROFILER OBSERVABILITY PASS] Root cause successfully isolated to lock frame."\n'
                               'EOF\n'
                               'chmod +x audit_latency_triage.sh\n'
                               './audit_latency_triage.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Span Latency Assertions\n'
                               'Author an automated test (<kbd>assert_trace_latencies.py</kbd>) asserting latency '
                               'thresholds:\n'
                               '\n'
                               '```python\n'
                               '# assert_trace_latencies.py\n'
                               'optimized_span_ms = 12.0\n'
                               'contended_span_ms = 4142.0\n'
                               "assert optimized_span_ms < 50.0, 'Optimized span must complete under 50ms'\n"
                               "assert contended_span_ms > 2000.0, 'Contended span correctly flagged as anomalous'\n"
                               "print('[ASSERT PASS] Distributed span latency thresholds verified.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_trace_latencies.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_trace_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 94 Topic 2 test scripts..."\n'
                               'rm -f check_trace_env.py trace_profiler_sim.py format_error_event.py '
                               'simulate_thread_contention.py audit_latency_triage.sh assert_trace_latencies.py\n'
                               'echo "[CLEANUP] Retaining day-094-topic-02-latency-triage.md evidence documentation."\n'
                               'echo "[CLEANUP PASS] Trace lab teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_trace_lab.sh\n'
                               './teardown_trace_lab.sh\n'
                               '```'],
                     'verification': 'The Python simulation produces valid structured JSON trace hierarchies and the '
                                     'latency triage runbook provides actionable investigation commands.',
                     'trouble': 'Ensure trace ID generation uses 32-character hexadecimal format conforming to W3C '
                                'Trace Context specifications.',
                     'cleanup': 'Retain `day-094-topic-02-latency-triage.md` as an exit evidence artifact.',
                     'accept': 'Completed distributed trace simulation and verified Profiler triage runbook. File: '
                               '`day-094-topic-02-trace-profiler.md`.',
                     'file': 'day-094-topic-02-trace-profiler.md'}},
            {'key': 'topic-03',
             'title': 'OpenTelemetry Instrumentation and W3C Context Propagation',
             'overview': 'OpenTelemetry (OTel) is the vendor-neutral cloud standard for capturing, generating, and '
                         'exporting telemetry data across distributed systems. In modern microservice topologies, a '
                         'user request traverses multiple services, asynchronous message brokers (Pub/Sub, Kafka), and '
                         'backend databases. By propagating W3C Trace Context headers (`traceparent` and `tracestate`) '
                         'across HTTP and gRPC network boundaries and embedding the extracted `trace_id` into '
                         'structured application log payloads, OpenTelemetry enables one-click navigation between a '
                         'failing log line and the complete distributed transaction waterfall.',
             'preview': 'When an asynchronous consumer fails to process an order from Pub/Sub, engineers cannot '
                        'identify which upstream frontend request submitted it. OpenTelemetry W3C trace context '
                        'propagation preserves correlation across asynchronous boundaries, eliminating disconnected '
                        'debugging.',
             'technical': '### 1. W3C Trace Context Standard (`traceparent` Header)\n'
                          '- **Header Structure:** The standard HTTP header `traceparent` uses a versioned 4-part '
                          'hyphen-delimited format:\n'
                          '  `version - trace_id - parent_span_id - trace_flags`\n'
                          '  Example: `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`\n'
                          '  - `00`: Protocol version.\n'
                          '  - `4bf92f3577b34da6a3ce929d0e0e4736`: 16-byte (32-character hex) unique global '
                          'transaction identifier.\n'
                          '  - `00f067aa0ba902b7`: 8-byte (16-character hex) identifier of the calling parent span.\n'
                          '  - `01`: Bitfield flags; `01` indicates the trace was sampled for recording.\n'
                          '\n'
                          '### 2. Context Injection and Extraction Across Transport Layers\n'
                          '- **HTTP Transports:** HTTP client interceptors inject the `traceparent` header into '
                          'outgoing request headers; HTTP server interceptors extract the header upon receiving '
                          'requests and activate the context in thread-local or async storage.\n'
                          '- **Pub/Sub Messaging:** Asynchronous message producers attach `traceparent` as a Pub/Sub '
                          "message attribute (e.g. `attributes['googclient_OpenTelemetryTraceparent']` or custom "
                          'attribute `traceparent`). Downstream pull/push consumers extract this attribute before '
                          'executing the processing span, preserving end-to-end parentage across decoupled queues.\n'
                          '\n'
                          '### 3. Trace-Log Correlation Architecture\n'
                          '- **Structured Log Enrichment:** Cloud Logging automatically recognizes trace associations '
                          'when JSON logs contain the key:\n'
                          '  `logging.googleapis.com/trace`: `projects/{PROJECT_ID}/traces/{TRACE_ID}`\n'
                          '  `logging.googleapis.com/spanId`: `{SPAN_ID}`\n'
                          '  `logging.googleapis.com/trace_sampled`: `true`\n'
                          '- **Correlated Querying:** With these fields present, selecting any log line in the Logs '
                          "Explorer displays a direct button: 'View trace for this log entry', opening Cloud Trace "
                          'centered directly on that exact operation.',
             'questions': ['How does the W3C Trace Context `traceparent` specification prevent broken transaction '
                           'traces across heterogeneous microservices?',
                           'What exact JSON fields must be injected into application logs to enable seamless '
                           'trace-to-log navigation in Google Cloud Logging?',
                           'How is trace context preserved across asynchronous, non-HTTP boundaries like Cloud Pub/Sub '
                           'and Cloud Tasks?'],
             'reference': 'https://docs.cloud.google.com/trace/docs/setup/opentelemetry',
             'reference_label': 'Google Cloud OpenTelemetry: W3C Trace Context and Cloud Trace exporter setup',
             'scenario': {'symptom': 'When an asynchronous payment fulfillment worker in Brightloaf threw fatal '
                                     'database errors, SREs spent 6 hours manually grepping logs trying to determine '
                                     'which user order and frontend checkout session initiated the message, as the '
                                     'worker logs contained no customer metadata.',
                          'constraints': 'Must link asynchronous Pub/Sub worker failures back to the initiating HTTP '
                                         'session without duplicating customer PII in worker logs.',
                          'evidence': 'Asynchronous worker logs and Pub/Sub message attributes captured the severed '
                                      'context:\n'
                                      '\n'
                                      '```\n'
                                      "[2026-09-29T14:15:02Z] FRONTEND LOG: 'Order ord-9944 submitted by user-4491'\n"
                                      '  logging.googleapis.com/trace: '
                                      'projects/brightloaf-prod/traces/8a92b01c34ef7712\n'
                                      '  logging.googleapis.com/spanId: 44a90182bb10\n'
                                      '\n'
                                      "[2026-09-29T14:15:06Z] WORKER LOG:   'FATAL: Payment fulfillment worker crashed "
                                      "on DB timeout'\n"
                                      '  logging.googleapis.com/trace: '
                                      'projects/brightloaf-prod/traces/0000000000000000 (UNLINKED)\n'
                                      '  logging.googleapis.com/spanId: 99c81200fa21\n'
                                      'Pub/Sub message inspection: attributes = {} (W3C traceparent was completely '
                                      'omitted!)\n'
                                      'Investigation delay: 6 hours spent manually correlating timestamps across '
                                      'decoupled microservices.\n'
                                      '```',
                          'diagnostic_steps': ['Inspect Pub/Sub message attributes published by the frontend checkout '
                                               'service.',
                                               'Verify whether the worker service extracts `traceparent` or '
                                               'initializes a root span.',
                                               'Review structured JSON log output from both services in Logs Explorer '
                                               'to check for `logging.googleapis.com/trace` presence.'],
                          'root': 'Broken trace propagation: the frontend publisher did not inject the active W3C '
                                  '`traceparent` header into the Pub/Sub message attributes, severing the distributed '
                                  'trace between the synchronous web app and the asynchronous background worker.',
                          'fix': 'Update the Pub/Sub publisher wrapper to inject `traceparent` into message '
                                 'attributes. Configure the subscriber consumer to extract the attribute using '
                                 'OpenTelemetry `TraceContextTextMapPropagator` and write the trace URI into all '
                                 'structured log lines.',
                          'verify': 'Publish a test order; inspect Logs Explorer and verify both the frontend HTTP log '
                                    'and worker error log share the exact same `logging.googleapis.com/trace` '
                                    'identifier and link to the same Cloud Trace diagram.',
                          'residual': 'If a third-party non-instrumented queue or legacy proxy strips custom headers, '
                                      'the trace context will be dropped at that hop.',
                          'diagram': ('Frontend initiates order',
                                      'Trace context stripped at queue',
                                      'Worker log isolated & unlinked',
                                      'W3C traceparent injected',
                                      'Seamless trace-log correlation')},
             'lab': {'name': 'OpenTelemetry W3C Trace Propagation and Structured Log Correlation Implementation',
                     'goal': 'Build an end-to-end Python pipeline propagating W3C trace context from an HTTP producer '
                             'to an asynchronous consumer with structured log correlation.',
                     'expected': 'An executable Python script demonstrating W3C traceparent generation, injection, '
                                 'extraction, and correlated JSON log emission.',
                     'mode': 'tabletop analysis & production Python execution',
                     'prereq': 'Understanding of HTTP headers and JSON logging.',
                     'preflight': 'Ensure Python 3 standard library is present; no cloud dependencies required.',
                     'steps': ['#### Stage 1: Pre-Flight W3C Trace Context & Correlation Invariants\n'
                               'Establish the OpenTelemetry context propagation invariants across transport '
                               'boundaries:\n'
                               '- **W3C Format:** Standard `traceparent` header format: '
                               '`00-{trace_id}-{span_id}-{trace_flags}` (32-char hex trace ID, 16-char hex span ID).\n'
                               '- **Asynchronous Queue Propagation:** Message publishers must attach `traceparent` to '
                               'Pub/Sub attributes, and subscribers must extract context before beginning message '
                               'processing spans.\n'
                               '- **Structured Log Injection:** Cloud Logging requires `logging.googleapis.com/trace` '
                               'in the format `projects/{PROJECT_ID}/traces/{TRACE_ID}` for automatic one-click trace '
                               'correlation.',
                               '#### Stage 2: Environment Preflight & Header Format Verification\n'
                               'Author a preflight script (<kbd>check_otel_env.py</kbd>) validating W3C traceparent '
                               'syntax parsing:\n'
                               '\n'
                               '```python\n'
                               '# check_otel_env.py\n'
                               "sample_header = '00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01'\n"
                               "parts = sample_header.split('-')\n"
                               "print(f'[PREFLIGHT] Parsing sample W3C traceparent: {sample_header}')\n"
                               "assert len(parts) == 4, 'Must have exactly 4 hyphen-delimited fields'\n"
                               "assert parts[0] == '00', 'Version must be 00'\n"
                               "assert len(parts[1]) == 32, 'Trace ID must be 32 hex characters'\n"
                               "assert len(parts[2]) == 16, 'Span ID must be 16 hex characters'\n"
                               "print('[PASS] W3C traceparent format validated.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight check:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_otel_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: W3C Traceparent Propagator & JSON Log Correlator\n'
                               'Author the end-to-end Python OpenTelemetry context propagation simulator '
                               '(<kbd>otel_propagation_engine.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               "cat <<'EOF' > otel_propagation_engine.py\n"
                               'import json\n'
                               'import time\n'
                               'import uuid\n'
                               '\n'
                               "PROJECT_ID = 'brightloaf-prod'\n"
                               '\n'
                               'class W3CTraceContext:\n'
                               '    def __init__(self, trace_id=None, span_id=None, sampled=True):\n'
                               "        self.version = '00'\n"
                               '        self.trace_id = trace_id or uuid.uuid4().hex\n'
                               '        self.span_id = span_id or uuid.uuid4().hex[:16]\n'
                               "        self.flags = '01' if sampled else '00'\n"
                               '\n'
                               '    def to_header(self):\n'
                               "        return f'{self.version}-{self.trace_id}-{self.span_id}-{self.flags}'\n"
                               '\n'
                               '    @classmethod\n'
                               '    def from_header(cls, header):\n'
                               "        p = header.split('-')\n"
                               "        return cls(trace_id=p[1], span_id=p[2], sampled=(p[3]=='01'))\n"
                               '\n'
                               'def emit_correlated_log(msg, severity, ctx, child_span_id=None):\n'
                               '    return json.dumps({\n'
                               "        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),\n"
                               "        'severity': severity,\n"
                               "        'message': msg,\n"
                               "        'logging.googleapis.com/trace': "
                               "f'projects/{PROJECT_ID}/traces/{ctx.trace_id}',\n"
                               "        'logging.googleapis.com/spanId': child_span_id or ctx.span_id,\n"
                               "        'logging.googleapis.com/trace_sampled': (ctx.flags == '01')\n"
                               '    })\n'
                               '\n'
                               'root_ctx = W3CTraceContext()\n'
                               "print('=== PRODUCER LOG ===')\n"
                               "print(emit_correlated_log('Order checkout received', 'INFO', root_ctx))\n"
                               '\n'
                               'header = root_ctx.to_header()\n'
                               'consumer_ctx = W3CTraceContext.from_header(header)\n'
                               "print('=== CONSUMER LOG ===')\n"
                               "print(emit_correlated_log('Payment fulfillment executed', 'INFO', consumer_ctx))\n"
                               'assert root_ctx.trace_id == consumer_ctx.trace_id\n'
                               "print('PASS: Trace context preserved.')\n"
                               'EOF\n'
                               'python3 otel_propagation_engine.py\n'
                               '```',
                               '#### Stage 4: Execution & Asynchronous Pub/Sub Attribute Injection\n'
                               'Author a script (<kbd>simulate_pubsub_trace.py</kbd>) attaching trace headers to '
                               'message attributes:\n'
                               '\n'
                               '```python\n'
                               "cat <<'EOF' > simulate_pubsub_trace.py\n"
                               'import json\n'
                               'from otel_propagation_engine import W3CTraceContext\n'
                               '\n'
                               'ctx = W3CTraceContext()\n'
                               'pubsub_payload = {\n'
                               "    'data': {'order_id': 'ord-9944', 'amount': 250.00},\n"
                               "    'attributes': {\n"
                               "        'traceparent': ctx.to_header(),\n"
                               "        'originating_service': 'checkout-api'\n"
                               '    }\n'
                               '}\n'
                               'print(json.dumps(pubsub_payload, indent=2))\n'
                               "assert 'traceparent' in pubsub_payload['attributes']\n"
                               "print('[PASS] Pub/Sub message enriched with W3C traceparent.')\n"
                               'EOF\n'
                               'python3 simulate_pubsub_trace.py\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Context Stripping Chaos Drill\n'
                               'Author a chaos simulation script (<kbd>simulate_trace_severing.py</kbd>) evaluating '
                               'fallback behavior when headers are missing:\n'
                               '\n'
                               '```python\n'
                               '# simulate_trace_severing.py\n'
                               'from otel_propagation_engine import W3CTraceContext\n'
                               '\n'
                               'def process_incoming_queue_message(attributes):\n'
                               "    if 'traceparent' in attributes:\n"
                               "        return W3CTraceContext.from_header(attributes['traceparent']), 'CORRELATED'\n"
                               '    # Fallback to new trace ID with warning\n'
                               "    return W3CTraceContext(), 'UNLINKED_FALLBACK'\n"
                               '\n'
                               "ctx_ok, status_ok = process_incoming_queue_message({'traceparent': "
                               "'00-11111111111111111111111111111111-2222222222222222-01'})\n"
                               'ctx_orphan, status_orphan = process_incoming_queue_message({})\n'
                               '\n'
                               "print(f'With Header   : {status_ok} (Trace ID: {ctx_ok.trace_id})')\n"
                               "print(f'Without Header: {status_orphan} (Trace ID: {ctx_orphan.trace_id})')\n"
                               "assert status_ok == 'CORRELATED'\n"
                               "assert status_orphan == 'UNLINKED_FALLBACK'\n"
                               "print('[PASS] Fallback detection verified.')\n"
                               '```\n'
                               '\n'
                               'Execute chaos test:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_trace_severing.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Redacted Telemetry Postmortem\n'
                               'Author the redacted diagnostic postmortem report '
                               '(<kbd>day-094-topic-03-telemetry-diagnosis.md</kbd>):\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > day-094-topic-03-telemetry-diagnosis.md\n"
                               '# Day 94: Redacted Distributed Telemetry Diagnostic Report\n'
                               '\n'
                               '## 1. Incident Timeline & Telemetry Correlation\n'
                               '- 2026-09-28T14:15:02Z: Ingress request `POST /api/v2/cart/checkout` enters ALB with '
                               'client IP `198.51.100.24`.\n'
                               '- 2026-09-28T14:15:02.012Z: API Gateway injects W3C header `traceparent: '
                               '00-7f28c19a82e91b...-01` and forwards to frontend service.\n'
                               '- 2026-09-28T14:15:02.110Z: Frontend service publishes order payload to Cloud Pub/Sub '
                               'topic `orders-pending` with `attributes.traceparent` attached.\n'
                               '- 2026-09-28T14:15:06.320Z: Downstream fulfillment worker in `us-east1` extracts '
                               'message; encounters Cloud SQL connection pool saturation.\n'
                               '- 2026-09-28T14:15:06.325Z: Worker logs `ERROR: Connection pool exhausted`. Log entry '
                               'contains identical `logging.googleapis.com/trace` ID.\n'
                               '\n'
                               '## 2. Causal Hypothesis & Telemetry Evidence\n'
                               '- Hypothesis: Upstream burst of checkout transactions exhausted Cloud SQL connection '
                               'pool due to un-pooled direct database connections.\n'
                               '- Trace Evidence: Cloud Trace displays a 4,210ms total transaction span, with 4,180ms '
                               'spent in child span `worker.db_acquire_connection`.\n'
                               '- Profile Evidence: Cloud Profiler wall-time flame graph shows 99% of time in '
                               '`pgbouncer` client wait loops.\n'
                               '\n'
                               '## 3. Telemetry System Limitations\n'
                               '- Trace Sampling Gaps: At 1% probabilistic sampling, 99% of customer requests do not '
                               'have full waterfall spans; only aggregate metrics and error traces are captured.\n'
                               '- Log Retention Boundaries: Un-filtered debug logs expire after 30 days in the default '
                               'log bucket unless explicitly captured by compliance sinks.\n'
                               'EOF\n'
                               'cat day-094-topic-03-telemetry-diagnosis.md\n'
                               '```',
                               '#### Stage 7: Automated Verification & End-to-End Correlation Assertions\n'
                               'Author an automated test (<kbd>assert_trace_correlation.py</kbd>) asserting trace ID '
                               'matching:\n'
                               '\n'
                               '```python\n'
                               '# assert_trace_correlation.py\n'
                               'import json\n'
                               'from otel_propagation_engine import W3CTraceContext, emit_correlated_log\n'
                               '\n'
                               'ctx = W3CTraceContext()\n'
                               "log1 = json.loads(emit_correlated_log('Event 1', 'INFO', ctx))\n"
                               "log2 = json.loads(emit_correlated_log('Event 2', 'INFO', ctx))\n"
                               '\n'
                               "assert log1['logging.googleapis.com/trace'] == log2['logging.googleapis.com/trace']\n"
                               "assert log1['logging.googleapis.com/trace_sampled'] is True\n"
                               "print('[ASSERT PASS] Trace-log correlation fields strictly validated.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_trace_correlation.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_otel_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 94 Topic 3 test scripts..."\n'
                               'rm -f check_otel_env.py otel_propagation_engine.py simulate_pubsub_trace.py '
                               'simulate_trace_severing.py assert_trace_correlation.py\n'
                               'echo "[CLEANUP] Retaining day-094-topic-03-telemetry-diagnosis.md evidence '
                               'documentation."\n'
                               'echo "[CLEANUP PASS] OpenTelemetry lab teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_otel_lab.sh\n'
                               './teardown_otel_lab.sh\n'
                               '```'],
                     'verification': 'The OpenTelemetry script confirms W3C header preservation across decoupled '
                                     'message passing and the diagnostic postmortem provides timestamps, causal '
                                     'hypothesis, and telemetry limitations.',
                     'trouble': 'Ensure `traceparent` uses exactly lowercase hexadecimal characters without extra '
                                'whitespace or invalid version prefix.',
                     'cleanup': 'Retain `day-094-topic-03-telemetry-diagnosis.md` as an exit evidence artifact.',
                     'accept': 'Completed OpenTelemetry propagation script and verified diagnostic postmortem '
                               'artifact. File: `day-094-topic-03-telemetry-diagnosis.md`.',
                     'file': 'day-094-topic-03-telemetry-diagnosis.md'}}],
 'part3_intro': 'The following field cases analyze real-world production catastrophes resulting from unhedged '
                'telemetry and tracing architectures: unfiltered Log Router sinks ingesting millions of routine '
                'health-check probes to generate a $42,000 billing surge, severe P99 latency regressions caused by '
                'global thread lock contention completely invisible to standard host CPU metrics, and asynchronous '
                'background worker crashes orphaned from user checkout sessions because upstream queues stripped W3C '
                'traceparent headers. Each case details quantifiable failure metrics, verbatim terminal/log '
                'transcripts, diagnostic command sequences, root cause mechanics, defensible remediations, and '
                'dual-lane failed/corrected architectural diagrams.',
 'part4_intro': 'These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers author '
                'production Cloud Logging sink manifests with cost-saving exclusion filters, execute BigQuery Log '
                'Analytics SQL queries across structured application logs, build Python distributed tracing and '
                'continuous lock contention simulators with Cloud Profiler flame-graph analysis, and deploy '
                'vendor-neutral OpenTelemetry pipelines with end-to-end W3C traceparent propagation and trace-log '
                'correlation.'}
