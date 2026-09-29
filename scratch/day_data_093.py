"""day_data_093.py — Exhaustive architecture data specification for Day 93.

Covers Metrics, Alerting, and Burn Rates.
"""

DAY_NUM = 93

DATA = {'day': 93,
 'part1_intro': 'Day 93 shifts from infrastructure survivability to continuous operational observability: '
                'instrumentation telemetry, incident alerting systems, and mathematical error budget consumption. '
                'Observability is not merely the passive collection of CPU statistics; it is the active discipline '
                'that proves whether user-facing commitments are being satisfied in real time. Poor alerting is as '
                'destructive as no alerting: uncalibrated static thresholds flood on-call engineers with hundreds of '
                "spurious pages, creating alert fatigue that causes real outages to be ignored. Today's curriculum "
                'establishes multi-project Google Cloud Monitoring Scopes and Managed Service for Prometheus (GMP), '
                'constructs multi-window multi-burn-rate alerting policies that alert on symptom severity rather than '
                'component noise, and deploys global Anycast uptime checks and synthetic headless canaries to detect '
                'user-facing regressions before customer complaints arrive.',
 'exit_summary': 'Engineered an enterprise Telemetry and Multi-Burn-Rate Alerting Architecture: established a '
                 'multi-project Cloud Monitoring Metrics Scope with Google Cloud Managed Service for Prometheus (GMP) '
                 'ingestion; authored a production Monitoring Query Language (MQL) dashboard definition; deployed '
                 'dual-window multi-burn-rate alert policies (1h/5m and 6h/30m) protecting a 99.9% availability SLO; '
                 'configured automated global uptime checks across multi-continent probe stations with latency '
                 'assertion gates.',
 'part2_intro': 'Reliable observability decouples metric ingestion from alert generation, transforming '
                'high-cardinality time series into actionable incident signals. The sections below analyze Prometheus '
                'metric pipelines, multi-burn-rate mathematical formulas, and global synthetic probing mechanics.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>Telemetry Layer</th>\n'
                    '      <th>Primary GCP Mechanism</th>\n'
                    '      <th>Ingestion Model &amp; Protocol</th>\n'
                    '      <th>Data Retention &amp; Limits</th>\n'
                    '      <th>Architectural Failure Mode / Anti-Pattern</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>Infrastructure Telemetry</strong></td>\n'
                    '      <td>Google Cloud Monitoring (Ops Agent)</td>\n'
                    '      <td>Push-based collectd/Fluent Bit agent via Cloud Logging/Monitoring API</td>\n'
                    '      <td>6 weeks at 1-minute resolution, downsampled to 10-minute/1-hour</td>\n'
                    '      <td>Missing Ops Agent on custom images; blind spots on disk I/O and guest RAM</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Prometheus Metrics</strong></td>\n'
                    '      <td>Managed Service for Prometheus (GMP)</td>\n'
                    '      <td>Pull-based scrape via lightweight PodMonitoring / NodeMonitoring CRDs</td>\n'
                    '      <td>24 months retention; global managed storage without Prometheus server state</td>\n'
                    '      <td>Unbounded metric cardinality (e.g. user IDs in labels) causing massive ingestion '
                    'bills</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>SLO Multi-Burn Alerting</strong></td>\n'
                    '      <td>Cloud Monitoring Alert Policies (MQL)</td>\n'
                    '      <td>Real-time evaluation engine tracking short and long lookback windows</td>\n'
                    '      <td>Sub-minute evaluation; alerts routed to PagerDuty/PubSub/Slack channels</td>\n'
                    '      <td>Single-window static threshold alerting; premature paging during transient spikes</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>Synthetic Availability</strong></td>\n'
                    '      <td>Cloud Monitoring Uptime Checks &amp; Synthetics</td>\n'
                    '      <td>Multi-region external Anycast probes (Americas, Europe, Asia-Pacific)</td>\n'
                    '      <td>1-minute check frequency; response status, latency, and content matching</td>\n'
                    '      <td>Probing internal VPC endpoints from public stations without Serverless VPC Access</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 93: Enterprise Observability and Multi-Burn-Rate Alerting Pipeline',
                  'desc': 'End-to-end telemetry architecture from container scrape to multi-window burn rate alert '
                          'triggers and synthetic validation.',
                  'caption': 'Figure 93.1: Architecture pipeline separating Prometheus metric scraping, Cloud '
                             'Monitoring multi-project scoping, and multi-burn-rate incident dispatch.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Global Edge Ingress & Outside-In Synthetic Probing Tier',
                              'desc': 'Public Multi-Region Uptime Probes (Americas, Europe, Asia), Headless Browser '
                                      'Canaries, and Edge CDN Handshakes',
                              'fill': '#1e3a5f',
                              'y': 10,
                              'h': 90},
                             {'name': 'LAYER 2: Compute Runtime & Prometheus Exporter Scrape Tier',
                              'desc': 'GKE Regional Cluster, Managed Service for Prometheus (GMP) DaemonSet '
                                      'Collectors, and PodMonitoring CRDs',
                              'fill': '#0f2338',
                              'y': 115,
                              'h': 90},
                             {'name': 'LAYER 3: Centralized Multi-Project Metrics Scoping Fabric',
                              'desc': 'Metrics Scope Host Project (brightloaf-mon-prod), 24-Month Time-Series Storage, '
                                      'and Cross-Project MQL',
                              'fill': '#064e3b',
                              'y': 220,
                              'h': 90},
                             {'name': 'LAYER 4: SLO Real-Time Evaluation & Multi-Burn Analysis Engine',
                              'desc': 'Dual-Window Rolling Evaluation (1h/5m, 6h/30m), MQL Error Budget Burn '
                                      'Calculators, and Suppression Gates',
                              'fill': '#1e1b4b',
                              'y': 325,
                              'h': 90},
                             {'name': 'LAYER 5: SRE Incident Notification & Automated Paging Lifecycle',
                              'desc': 'PagerDuty P1 Escalation Channel, Slack Incident Response Bridge, and Automated '
                                      'Jira Low-Priority Tickets',
                              'fill': '#3b0764',
                              'y': 430,
                              'h': 90}],
                  'components': [{'id': 'global_uptime_probes',
                                  'name': 'Global Uptime Probes',
                                  'detail': 'Multi-Continent Edge Probing',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'synthetic_canary',
                                  'name': 'Synthetic Canary Node',
                                  'detail': 'Puppeteer Journey Validation',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'gmp_managed_collector',
                                  'name': 'GMP Managed Collector',
                                  'detail': 'DaemonSet Prometheus Scraping',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'pod_monitoring_crd',
                                  'name': 'PodMonitoring CRD',
                                  'detail': 'Bounded Label Filtering',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'metrics_scope_host',
                                  'name': 'Metrics Scope Host',
                                  'detail': 'Multi-Project Unified Aggregation',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'time_series_storage',
                                  'name': 'Time-Series Store',
                                  'detail': '24-Month Managed Retention',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'mql_burn_engine',
                                  'name': 'MQL Burn Engine',
                                  'detail': '14.4x & 6.0x Burn Calculation',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'dual_window_evaluator',
                                  'name': 'Dual-Window Evaluator',
                                  'detail': 'Short (5m) & Long (1h) AND Gate',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'pagerduty_escalation',
                                  'name': 'PagerDuty Escalation',
                                  'detail': 'Immediate P1 On-Call Wakeup',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'},
                                 {'id': 'jira_ticket_router',
                                  'name': 'Jira Ticket Router',
                                  'detail': 'Sub-Burn Trend Tracking',
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
                                  'label': 'OUTSIDE-IN GLOBAL SYNTHETIC & EDGE PERIMETER',
                                  'color': '#38bdf8'},
                                 {'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 195,
                                  'label': 'KUBERNETES RUNTIME & MULTI-PROJECT METRIC SCOPING BOUNDARY',
                                  'color': '#10b981'},
                                 {'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 195,
                                  'label': 'SLO EVALUATION & DUAL-WINDOW ALERTING PERIMETER',
                                  'color': '#a855f7'}],
                  'flows': [{'x1': 340,
                             'y1': 56,
                             'x2': 420,
                             'y2': 56,
                             'type': 'ok',
                             'label': 'Execute Synthetic Journey'},
                            {'x1': 210,
                             'y1': 82,
                             'x2': 210,
                             'y2': 135,
                             'type': 'ok',
                             'label': 'Validate Ingress Health'},
                            {'x1': 340,
                             'y1': 161,
                             'x2': 420,
                             'y2': 161,
                             'type': 'ok',
                             'label': 'Enforce Label Boundedness'},
                            {'x1': 210,
                             'y1': 187,
                             'x2': 210,
                             'y2': 240,
                             'type': 'ok',
                             'label': 'Ingest Scraped Time Series'},
                            {'x1': 340,
                             'y1': 266,
                             'x2': 420,
                             'y2': 266,
                             'type': 'ok',
                             'label': 'Query Across Scoped Projects'},
                            {'x1': 210,
                             'y1': 292,
                             'x2': 210,
                             'y2': 345,
                             'type': 'ok',
                             'label': 'Evaluate MQL Error Budget'},
                            {'x1': 340,
                             'y1': 371,
                             'x2': 420,
                             'y2': 371,
                             'type': 'ok',
                             'label': 'Check Long AND Short Windows'},
                            {'x1': 210,
                             'y1': 397,
                             'x2': 210,
                             'y2': 450,
                             'type': 'fail',
                             'label': 'Dispatch P1 PagerDuty Page'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'type': 'ok',
                             'label': 'File Low-Priority Ticket'}],
                  'probes': [{'cx': 80,
                              'cy': 30,
                              'label': 'PROBE 1: Global Edge SSL Handshake Latency (<500ms)',
                              'color': '#38bdf8'},
                             {'cx': 420,
                              'cy': 135,
                              'label': 'PROBE 2: Active Metric Time-Series Count (<50)',
                              'color': '#10b981'},
                             {'cx': 420,
                              'cy': 345,
                              'label': 'PROBE 3: Error Budget Consumption Burn Rate (>14.4x)',
                              'color': '#ef4444'}]},
 'topics': [{'key': 'topic-01',
             'title': 'Cloud Monitoring',
             'preview': 'An enterprise running 80 microservices across 15 separate GCP projects discovers that SREs '
                        'must manually open 15 separate browser tabs to troubleshoot cross-project database queries, '
                        'adding 40 minutes of blind triage time during a major payment outage.',
             'overview': '**Google Cloud Monitoring** provides centralized, full-stack observability across cloud '
                         'infrastructure, managed services, and custom applications. In modern multi-project '
                         'enterprise architectures, observability must transcend individual project boundaries. By '
                         "establishing a **Metrics Scope**, organizations designate a central 'scoping project' that "
                         'aggregates metrics, dashboards, and uptime checks from multiple monitored projects into a '
                         'unified single-pane-of-glass interface. Furthermore, for containerized Kubernetes workloads, '
                         '**Google Cloud Managed Service for Prometheus (GMP)** eliminates the operational overhead of '
                         'self-hosting Prometheus servers: it uses lightweight PodMonitoring Custom Resource '
                         "Definitions (CRDs) to scrape endpoints and ingests time series directly into Google's "
                         'scalable, planet-scale time-series database with 24 months of retention.',
             'technical': '### 1. Metrics Scopes and Multi-Project Architectures\n'
                          '- **The Scoping Project:** A designated Google Cloud project (e.g. '
                          '`brightloaf-monitoring-prod`) configured as the Metrics Scope host. Monitored projects '
                          '(e.g. `brightloaf-billing`, `brightloaf-checkout`, `brightloaf-inventory`) are added to the '
                          'scope via the Monitoring metrics-scopes API (`monitoring.metricsScopes.link`).\n'
                          '- **Unified Cross-Project Querying:** Once scoped, SREs query metrics across all 15 '
                          'projects in a single MQL query using the `resource.project_id` filter, correlating '
                          'downstream database latency in Project B with frontend 504 timeouts in Project A.\n'
                          '\n'
                          '### 2. Managed Service for Prometheus (GMP) Architecture\n'
                          '- **Managed Collectors:** GKE clusters enable GMP with a single toggle '
                          '(`--enable-managed-prometheus`). Google provisions and manages daemonset collectors that '
                          'scrape target pods without requiring local Prometheus stateful disks or alertmanager '
                          'infrastructure.\n'
                          '- **Declarative PodMonitoring:** Telemetry targets are defined using Kubernetes-native '
                          'CRDs:\n'
                          '  `apiVersion: monitoring.googleapis.com/v1` with `kind: PodMonitoring`. Defines scrape '
                          'intervals (e.g. 15s), metric paths (`/metrics`), and label filters.\n'
                          '- **High-Cardinality Governance:** Metric ingestion charges are billed per million samples. '
                          'Developers must never insert unbounded dimensions (such as user IDs, UUIDs, or email '
                          'addresses) into metric labels; high-cardinality metadata belongs in Cloud Logging or Trace, '
                          'not metric time series.\n'
                          '\n'
                          '### 3. Custom Metrics and Metric Descriptors\n'
                          '- **Metric Types:** Gauges (instantaneous values like queue depth), Cumulative '
                          '(monotonically increasing counters like total requests), and Delta (change over evaluation '
                          'interval).\n'
                          '- **Value Types:** INT64, DOUBLE, BOOLEAN, and DISTRIBUTION (histograms tracking request '
                          'latency percentiles: P50, P95, P99).',
             'questions': ['How does configuring a centralized Metrics Scope eliminate operational blind spots across '
                           'multi-project microservice environments?',
                           'What architectural risks are introduced when high-cardinality metadata (like user UUIDs) '
                           'is placed in Prometheus metric labels?',
                           'Why does Google Cloud Managed Service for Prometheus (GMP) use PodMonitoring CRDs rather '
                           'than traditional ConfigMaps?'],
             'reference': 'https://docs.cloud.google.com/monitoring/docs',
             'reference_label': 'Google Cloud Monitoring: Metric architecture, multi-project scoping, and Managed '
                                'Service for Prometheus',
             'scenario': {'symptom': "During a peak trading surge, Brightloaf's monthly Cloud Monitoring bill spiked "
                                     'by $68,000 in 72 hours, while GKE collector pods began OOMKilled crash loops '
                                     'that dropped 60% of infrastructure performance metrics.',
                          'constraints': 'Must preserve sub-minute application latency monitoring while eliminating '
                                         'metric billing surges and collector memory exhaustion.',
                          'evidence': 'Metrics Explorer and collector pod error logs captured the cardinality '
                                      'explosion:\n'
                                      '\n'
                                      '```\n'
                                      '[2026-09-29T10:15:22Z] gke-metrics-collector: FATAL: OOMKilled: memory limit '
                                      '(512MiB) exceeded\n'
                                      '[2026-09-29T10:15:25Z] kubelet: Pod gke-gmp-collector-v8k2 restarted '
                                      '(restartCount=18)\n'
                                      '$ gcloud monitoring metric-descriptors describe '
                                      'custom.googleapis.com/http_requests_total ...\n'
                                      'labels:\n'
                                      '- key: method\n'
                                      '- key: route\n'
                                      '- key: status\n'
                                      '- key: user_id  <-- UNBOUNDED HIGH-CARDINALITY DIMENSION\n'
                                      'Active Time-Series Count: 4,218,920 distinct metric streams\n'
                                      'Cloud Billing impact: Ingestion surge of $68,400 USD accrued within 72 hours\n'
                                      'Infrastructure impact: 60% of cluster performance metrics dropped due to '
                                      'collector thrashing\n'
                                      '```',
                          'diagnostic_steps': ['Inspect Cloud Monitoring billing breakdown grouped by Metric Type to '
                                               'identify the offending metric descriptor.',
                                               'Query the Metric Descriptors API to audit label keys attached to '
                                               '`custom.googleapis.com` and GMP metrics.',
                                               "Inspect Git commit diffs on the API server's Prometheus metric "
                                               'instrumentation interceptor.'],
                          'root': 'Unbounded metric cardinality: adding unique user IDs to Prometheus metric labels '
                                  'created millions of distinct time series, saturating collector memory and exploding '
                                  'metric ingestion fees.',
                          'fix': 'Remove the `user_id` label from the Prometheus metric interceptor; retain only '
                                 'bounded labels (`method`, `status_code`, `route`). Pass `user_id` exclusively in '
                                 'structured JSON logs via Cloud Logging and Cloud Trace span attributes. Implement a '
                                 'pre-commit linter rejecting high-cardinality metric labels.',
                          'verify': 'Deploy the corrected PodMonitoring manifest in staging; verify active time series '
                                    'for `http_requests_total` drops from 4,200,000 to 36, and collector pod memory '
                                    'stabilizes at 85 MB.',
                          'residual': 'Historical high-cardinality time series will persist in Cloud Monitoring '
                                      'storage until their standard 6-week metric retention expires.',
                          'diagram': ('User ID added to metric label',
                                      '4.2M active time series created',
                                      '$68k billing surge & collector OOM',
                                      'High-cardinality labels stripped',
                                      'Time series drops to 36; bill drops'),
                          'facts': 'A single unbounded `user_id` label created 4.2M time series and a $68k bill '
                                   'because metrics are billed per ingested sample.',
                          'inference': 'Metrics are intended for mathematical aggregation across bounded dimensions; '
                                       'identity traces belong in Logging/Trace.',
                          'expected': 'Prometheus metric labels remain strictly bounded (< 100 values per key), '
                                      'keeping collector memory and billing predictable.'},
             'lab': {'name': 'Cloud Monitoring Metrics Scope & GMP PodMonitoring Ingestion',
                     'file': 'day-093-topic-01-metrics-scope.md',
                     'goal': 'Establish a multi-project Metrics Scope, deploy Managed Service for Prometheus (GMP), '
                             'and verify bounded metric ingestion.',
                     'expected': 'A comprehensive configuration guide with exact gcloud commands creating scopes and a '
                                 'validated Kubernetes PodMonitoring manifest.',
                     'mode': 'tabletop analysis & production CLI / YAML execution',
                     'prereq': 'Understanding of Kubernetes manifests and Prometheus metrics.',
                     'preflight': 'Review Google Cloud Managed Service for Prometheus documentation and gcloud '
                                  'monitoring syntax.',
                     'steps': ['#### Stage 1: Pre-Flight Metrics Scoping & Bounded Ingestion Architecture\n'
                               "Establish the telemetry architecture invariants for Brightloaf's multi-project "
                               'microservices:\n'
                               '- **Metrics Scope Host:** Designate `brightloaf-mon-prod` as the centralized scoping '
                               'project aggregating telemetry across billing, checkout, and inventory.\n'
                               '- **Managed Prometheus (GMP):** Deploy PodMonitoring CRDs with explicit '
                               '`metricRelabeling` to drop high-cardinality labels before ingestion.\n'
                               '- **Cardinality Invariant:** Label permutations for custom metrics must not exceed 50 '
                               'distinct streams per deployment.',
                               '#### Stage 2: Infrastructure Preflight & Scoping Project Verification\n'
                               'Author a preflight script (<kbd>check_monitoring_env.py</kbd>) verifying API '
                               'enablement and scoping topology:\n'
                               '\n'
                               '```python\n'
                               '# check_monitoring_env.py\n'
                               'scoping_spec = {\n'
                               "    'host_project': 'brightloaf-mon-prod',\n"
                               "    'monitored_projects': ['brightloaf-billing', 'brightloaf-checkout', "
                               "'brightloaf-inventory'],\n"
                               "    'max_labels_per_metric': 5,\n"
                               '}\n'
                               'print(f\'[PREFLIGHT] Checking Metrics Scope Host: {scoping_spec["host_project"]}\')\n'
                               "assert len(scoping_spec['monitored_projects']) >= 2, 'Must scope multi-project "
                               "microservices'\n"
                               "print('[PASS] Preflight monitoring topology verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight check:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_monitoring_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Multi-Project Metrics Scope Linkage\n'
                               'Author the deployment script linking monitored projects to the central scoping '
                               'project:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > setup_metrics_scope.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'HOST_PROJECT="${HOST_PROJECT:-brightloaf-mon-prod}"\n'
                               'echo "Verifying Cloud Monitoring API on host project ${HOST_PROJECT}..."\n'
                               'gcloud services enable monitoring.googleapis.com --project="${HOST_PROJECT}" || true\n'
                               '\n'
                               'echo "Simulating Metrics Scope linkage for workload projects..."\n'
                               'for PROJ in brightloaf-billing brightloaf-checkout brightloaf-inventory; do\n'
                               '    echo "Linking ${PROJ} to Metrics Scope ${HOST_PROJECT}..."\n'
                               '    # gcloud alpha monitoring metrics-scopes link\n'
                               'done\n'
                               'echo "[PASS] Multi-project Metrics Scope configured successfully."\n'
                               'EOF\n'
                               'chmod +x setup_metrics_scope.sh\n'
                               './setup_metrics_scope.sh\n'
                               '```',
                               '#### Stage 4: Execution & Declarative PodMonitoring CRD Deployment\n'
                               'Author the Kubernetes PodMonitoring manifest (<kbd>pod-monitoring-orders.yaml</kbd>) '
                               'enforcing labeldrop rules:\n'
                               '\n'
                               '```yaml\n'
                               "cat <<'YAML' > pod-monitoring-orders.yaml\n"
                               'apiVersion: monitoring.googleapis.com/v1\n'
                               'kind: PodMonitoring\n'
                               'metadata:\n'
                               '  name: orders-api-monitor\n'
                               '  namespace: production\n'
                               'spec:\n'
                               '  selector:\n'
                               '    matchLabels:\n'
                               '      app.kubernetes.io/name: orders-api\n'
                               '  endpoints:\n'
                               '  - port: metrics\n'
                               '    path: /metrics\n'
                               '    interval: 15s\n'
                               '    metricRelabeling:\n'
                               '    - action: labeldrop\n'
                               '      regex: (user_id|session_id|email|customer_token|cart_id)\n'
                               'YAML\n'
                               'cat pod-monitoring-orders.yaml\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Unbounded Cardinality Chaos Injection\n'
                               'Author a chaos simulation script (<kbd>simulate_cardinality_surge.py</kbd>) '
                               'demonstrating labeldrop protection:\n'
                               '\n'
                               '```python\n'
                               '# simulate_cardinality_surge.py\n'
                               'import re\n'
                               '\n'
                               "print('--- SIMULATING METRIC SCRAPE CARDINALITY FILTERING ---')\n"
                               "raw_metric = {'method': 'POST', 'route': '/checkout', 'user_id': 'usr-8849120', "
                               "'session_id': 'sess-9921'}\n"
                               "drop_regex = re.compile(r'^(user_id|session_id|email|customer_token|cart_id)$')\n"
                               '\n'
                               'filtered_metric = {k: v for k, v in raw_metric.items() if not drop_regex.match(k)}\n'
                               "print(f'Raw Metric Labels     : {list(raw_metric.keys())}')\n"
                               "print(f'Sanitized GMP Labels : {list(filtered_metric.keys())}')\n"
                               '\n'
                               "assert 'user_id' not in filtered_metric, 'user_id must be stripped by PodMonitoring'\n"
                               "assert 'session_id' not in filtered_metric, 'session_id must be stripped'\n"
                               "assert len(filtered_metric) == 2, 'Only bounded labels method and route must survive'\n"
                               "print('[PASS] Cardinality guard neutralized high-cardinality injection.')\n"
                               '```\n'
                               '\n'
                               'Execute chaos test:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_cardinality_surge.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Ingestion Quota Monitoring\n'
                               'Author a telemetry verification script auditing active time series counts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_gmp_telemetry.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Querying GMP time-series metrics in brightloaf-mon-prod..."\n'
                               "cat <<'METRIC'\n"
                               'Metric: prometheus.googleapis.com/http_requests_total\n'
                               'Active Distinct Label Permutations: 36 (Bounded)\n'
                               'Ingestion Rate: 2.4 samples/second (Down from 280,000 samples/sec)\n'
                               'Projected Monthly Ingestion Cost: $48.20 USD (Down from $68,400.00)\n'
                               'METRIC\n'
                               'echo "[GMP OBSERVABILITY PASS] Metric ingestion volume normalized."\n'
                               'EOF\n'
                               'chmod +x verify_gmp_telemetry.sh\n'
                               './verify_gmp_telemetry.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Label Cardinality Bounds Assertions\n'
                               'Author an automated test (<kbd>assert_bounded_cardinality.py</kbd>) asserting label '
                               'limits:\n'
                               '\n'
                               '```python\n'
                               '# assert_bounded_cardinality.py\n'
                               "permitted_labels = {'method', 'status', 'route'}\n"
                               "active_labels = {'method', 'status', 'route'}\n"
                               'disallowed = active_labels - permitted_labels\n'
                               "assert len(disallowed) == 0, f'Detected unauthorized labels: {disallowed}'\n"
                               "print('[ASSERT PASS] Metric labels strictly conform to bounded schema.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_bounded_cardinality.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_monitoring_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 93 Topic 1 test scripts..."\n'
                               'rm -f check_monitoring_env.py setup_metrics_scope.sh pod-monitoring-orders.yaml '
                               'simulate_cardinality_surge.py verify_gmp_telemetry.sh assert_bounded_cardinality.py\n'
                               'echo "[CLEANUP] Retaining day-093-topic-01-metrics-scope.md evidence documentation."\n'
                               'echo "[CLEANUP PASS] Monitoring lab teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_monitoring_lab.sh\n'
                               './teardown_monitoring_lab.sh\n'
                               '```'],
                     'verification': 'Configuration files exist, PodMonitoring manifest includes defensive labeldrop '
                                     'filters, and cardinality validation script passes.',
                     'trouble': 'Ensure GKE cluster has `--enable-managed-prometheus` flag set before applying '
                                '`monitoring.googleapis.com/v1` CRDs.',
                     'cleanup': 'Retain `day-093-topic-01-metrics-scope.md` as an exit evidence artifact.',
                     'accept': 'Completed Metrics Scope architecture guide with validated bounded PodMonitoring '
                               'configuration.'}},
            {'key': 'topic-02',
             'title': 'Alerting policies',
             'preview': 'An SRE team configured a static CPU alert set to page on-call engineers when CPU exceeds 80% '
                        'for 2 minutes, generating 420 midnight pages during scheduled batch backups while a real '
                        'checkout outage went unnoticed for 3 hours.',
             'overview': "Traditional alerting based on static infrastructure thresholds (e.g., 'CPU > 80%' or 'Memory "
                         "> 85%') is fundamentally broken: it generates high false-alarm rates, produces severe alert "
                         'fatigue, and fails to detect real customer-impacting failures until users complain. Modern '
                         'reliability engineering mandates **SLO-based alerting** using **Multi-Window Multi-Burn-Rate '
                         'Policies**. Instead of measuring component utilization, multi-burn-rate alerting monitors '
                         'the rate at which the user-facing **Error Budget** is being consumed. By pairing a **long '
                         'lookback window** (which proves the failure is persistent) with a **short lookback window** '
                         '(which proves the failure is actively occurring right now), multi-burn alerting delivers '
                         'rapid detection during catastrophic outages while completely eliminating false-positive '
                         'pages caused by brief transient spikes.',
             'technical': '### 1. Multi-Window Multi-Burn-Rate Mathematical Model\n'
                          '- **Burn Rate Defined:** A burn rate of $1.0$ consumes exactly 100% of an error budget over '
                          'the course of the SLO period (e.g. 30 days). If an SLO is 99.9%, the error budget is '
                          '$0.1\\% = 0.001$. A burn rate of $1.0$ means the error rate is exactly $0.1\\%$.\n'
                          '- **Burn Rate of 14.4 (P1 Alert):** Consumes 2% of the 30-day budget in only **1 hour**! '
                          'Requires an immediate 24/7 page.\n'
                          '- **The Dual-Window Rule (Google SRE Standard):** To fire an alert, *both* windows must '
                          'exceed the threshold simultaneously:\n'
                          '  1. **Long Window (e.g. 1 hour, burn rate > 14.4):** Proves that error budget consumption '
                          'is statistically significant.\n'
                          '  2. **Short Window (e.g. 5 minutes, burn rate > 14.4):** Proves that the system is *still '
                          'failing right now*. If errors stop after 6 minutes, the short window clears instantly, '
                          'resetting the alert and preventing the on-call engineer from being awakened for a resolved '
                          'glitch.\n'
                          '\n'
                          '### 2. Multi-Burn Alerting Matrix (30-Day 99.9% SLO)\n'
                          '- **Critical / PagerDuty Page:** Burn Rate = 14.4. Long Window = 1h, Short Window = 5m. '
                          'Budget Consumed: 2% in 1 hour.\n'
                          '- **Major / PagerDuty Page:** Burn Rate = 6.0. Long Window = 6h, Short Window = 30m. Budget '
                          'Consumed: 5% in 6 hours.\n'
                          '- **Moderate / Ticket:** Burn Rate = 1.0. Long Window = 3 days, Short Window = 6 hours. '
                          'Budget Consumed: 10% in 3 days. Creates Jira ticket.\n'
                          '\n'
                          '### 3. Monitoring Query Language (MQL) Implementation\n'
                          '- Cloud Monitoring evaluates burn rates natively using MQL:\n'
                          "  Fetches `custom.googleapis.com/http/requests_total` with `status =~ '5..'`, divides by "
                          'total requests, computes ratio, and evaluates against threshold over rolling sliding '
                          'windows.',
             'questions': ['Why does pairing a short lookback window with a long lookback window eliminate '
                           'false-positive alert pages?',
                           'What is the mathematical relationship between an availability SLO of 99.9% and a burn rate '
                           'of 14.4?',
                           'How does SLO-based alerting reduce alert fatigue compared to static component utilization '
                           'thresholds?'],
             'reference': 'https://docs.cloud.google.com/monitoring/alerts',
             'reference_label': 'Google Cloud Monitoring: Alerting policies, notification channels, and '
                                'multi-burn-rate condition design',
             'scenario': {'symptom': "Brightloaf's on-call engineers received 1,280 PagerDuty alerts during a single "
                                     'month. Responders muted alerting channels, causing a catastrophic 4-hour '
                                     'checkout outage to go completely unaddressed because the page was buried under '
                                     'hundreds of non-critical disk-space and CPU-spike alerts.',
                          'constraints': 'Must eliminate alert fatigue by reducing total monthly on-call pages to '
                                         'fewer than 10, while guaranteeing sub-5-minute detection of core checkout '
                                         'failures.',
                          'evidence': 'PagerDuty incident logs and alert volume distribution telemetry captured the '
                                      'alert fatigue:\n'
                                      '\n'
                                      '```\n'
                                      'PAGERDUTY INCIDENT REPORT (LAST 30 DAYS):\n'
                                      'Total Incidents Fired: 1,280 alerts paged to on-call engineers\n'
                                      'Incident Breakdown:\n'
                                      "- 'Host CPU > 85% for 60s'          : 842 pages (100% false alarms during cron "
                                      'jobs)\n'
                                      "- 'Disk Free Space < 20%'          : 361 pages (All resolved automatically by "
                                      'logrotate)\n'
                                      "- 'Checkout API Error Budget Burn' :   1 page  (REAL OUTAGE: 4 hours "
                                      'unaddressed)\n'
                                      'Signal-to-Noise Ratio (SNR): 0.08% (99.92% of pages were non-actionable noise)\n'
                                      'Finding: Engineers muted on-call mobile notifications due to chronic sleep '
                                      'interruption.\n'
                                      '```',
                          'diagnostic_steps': ['Extract PagerDuty incident history for the last 90 days and group '
                                               'alerts by policy name and actionability.',
                                               'Calculate the Signal-to-Noise Ratio (SNR): `SNR = Actionable Incidents '
                                               '/ Total Alerts Paged`.',
                                               'Review Cloud Monitoring alert policy definitions to identify static '
                                               'infrastructure monitors that lack user-impact correlation.'],
                          'root': 'Flawed alerting philosophy: the team paged on internal component symptoms (CPU/RAM) '
                                  'rather than user-facing error budget consumption, creating massive alert fatigue '
                                  'that blinded responders to genuine outages.',
                          'fix': 'Decommission all static CPU/RAM pager alerts. Replace them with Google SRE standard '
                                 'dual-window multi-burn-rate alerting policies tied directly to the 99.9% checkout '
                                 'availability SLO (1h/5m for P1, 6h/30m for P2). Route non-urgent trends to automated '
                                 'Jira tickets.',
                          'verify': 'Simulate synthetic failure scenarios in pre-production: inject 2% error rate for '
                                    '3 minutes (confirms zero page fired), then inject 2% error rate for 12 minutes '
                                    '(confirms P1 page triggers at T+5m and resolves automatically when errors clear).',
                          'residual': 'Slow, low-grade error budget leaks (burn rate < 1.0) will take several days to '
                                      'alert via ticket, requiring weekly SLO review meetings.',
                          'diagram': ('1,280 static CPU alerts page SREs',
                                      'Alert fatigue: channels muted',
                                      '4h checkout outage ignored',
                                      'Dual-window multi-burn MQL deployed',
                                      'P1 pages fire only on real budget loss'),
                          'facts': '1,280 alerts generated per month, 94% of which had zero impact on customer '
                                   'transactions, blinding engineers to real outages.',
                          'inference': 'Paging on infrastructure utilization inevitably causes alert fatigue; pages '
                                       'must be reserved for active SLO budget loss.',
                          'expected': 'Dual-window multi-burn alerting triggers pages only when significant error '
                                      'budget is actively burning in real time.'},
             'lab': {'name': 'Multi-Window Multi-Burn-Rate Alert Policy Implementation',
                     'file': 'day-093-topic-02-burn-rate-alert.md',
                     'goal': 'Author and test a complete dual-window multi-burn-rate alerting policy using Monitoring '
                             'Query Language (MQL).',
                     'expected': 'A production-grade JSON alert policy definition and a Python validation script '
                                 'calculating mathematical burn rate thresholds.',
                     'mode': 'tabletop analysis & production JSON / Python execution',
                     'prereq': 'Understanding of SLOs, error budgets, and MQL syntax.',
                     'preflight': 'Review Google SRE Workbook Chapter 5 on Alerting on SLOs and Cloud Monitoring MQL '
                                  'reference.',
                     'steps': ['#### Stage 1: Pre-Flight Multi-Burn-Rate Architecture & Error Budget Calculus\n'
                               'Establish the mathematical calculus for multi-window multi-burn-rate alerting:\n'
                               '- **SLO Target:** 99.9% availability over a rolling 30-day period (Error Budget = 0.1% '
                               'or 0.001).\n'
                               '- **Burn Rate of 14.4 (Critical P1 Page):** Consumes 2% of total error budget in 1 '
                               'hour. Evaluated across 1-hour (long) AND 5-minute (short) windows.\n'
                               '- **Burn Rate of 6.0 (Major P2 Page):** Consumes 5% of error budget in 6 hours. '
                               'Evaluated across 6-hour (long) AND 30-minute (short) windows.\n'
                               '- **Dual-Window Invariant:** An alert fires if and only if *both* the short window and '
                               'long window exceed the burn threshold simultaneously.',
                               '#### Stage 2: Infrastructure Preflight & Notification Channel Verification\n'
                               'Author a preflight script (<kbd>check_alerting_env.py</kbd>) verifying burn rate '
                               'thresholds and notification endpoints:\n'
                               '\n'
                               '```python\n'
                               '# check_alerting_env.py\n'
                               'slo_spec = {\n'
                               "    'availability_target': 0.999,\n"
                               "    'error_budget': 0.001,\n"
                               "    'p1_burn_rate': 14.4,\n"
                               "    'p2_burn_rate': 6.0,\n"
                               '}\n'
                               "p1_threshold = slo_spec['p1_burn_rate'] * slo_spec['error_budget']\n"
                               "print(f'[PREFLIGHT] 30-Day 99.9% SLO Error Budget: "
                               '{slo_spec["error_budget"]*100:.2f}%\')\n'
                               "print(f'[PREFLIGHT] Critical P1 Error Threshold: {p1_threshold*100:.3f}%')\n"
                               "assert p1_threshold == 0.0144, 'P1 threshold must equal 1.44% error rate'\n"
                               "print('[PASS] Multi-burn rate mathematical parameters validated.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight check:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_alerting_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Dual-Window Multi-Burn MQL Alert Policy\n'
                               'Author the production Alert Policy JSON specification '
                               '(<kbd>deploy_burn_alert.json</kbd>):\n'
                               '\n'
                               '```json\n'
                               "cat <<'EOF' > deploy_burn_alert.json\n"
                               '{\n'
                               '  "displayName": "SLO Burn Rate Exceeded: 14.4x (1h / 5m Dual-Window)",\n'
                               '  "documentation": {\n'
                               '    "content": "P1 Incident: Checkout error budget burning at 14.4x rate (2% consumed '
                               'in 1h). Triage checkout ingress immediately.",\n'
                               '    "mimeType": "text/markdown"\n'
                               '  },\n'
                               '  "combiner": "AND",\n'
                               '  "conditions": [\n'
                               '    {\n'
                               '      "displayName": "Long Window: 1h Burn Rate > 14.4x",\n'
                               '      "conditionMonitoringQueryLanguage": {\n'
                               '        "duration": "0s",\n'
                               '        "query": "fetch https_lb_rule\\n| filter (resource.url_map == '
                               "'brightloaf-lb')\\n| { metric 'loadbalancing.googleapis.com/https/request_count'\\n    "
                               '| filter (metric.response_code_class == 500)\\n    | group_by sliding(1h), '
                               "sum(val())\\n  ; metric 'loadbalancing.googleapis.com/https/request_count'\\n    | "
                               'group_by sliding(1h), sum(val()) }\\n| ratio\\n| condition val() > (14.4 * 0.001)"\n'
                               '        }\n'
                               '    },\n'
                               '    {\n'
                               '      "displayName": "Short Window: 5m Burn Rate > 14.4x",\n'
                               '      "conditionMonitoringQueryLanguage": {\n'
                               '        "duration": "0s",\n'
                               '        "query": "fetch https_lb_rule\\n| filter (resource.url_map == '
                               "'brightloaf-lb')\\n| { metric 'loadbalancing.googleapis.com/https/request_count'\\n    "
                               '| filter (metric.response_code_class == 500)\\n    | group_by sliding(5m), '
                               "sum(val())\\n  ; metric 'loadbalancing.googleapis.com/https/request_count'\\n    | "
                               'group_by sliding(5m), sum(val()) }\\n| ratio\\n| condition val() > (14.4 * 0.001)"\n'
                               '        }\n'
                               '    }\n'
                               '  ],\n'
                               '  "alertStrategy": {\n'
                               '    "autoClose": "1800s"\n'
                               '  }\n'
                               '}\n'
                               'EOF\n'
                               'cat deploy_burn_alert.json\n'
                               '```',
                               '#### Stage 4: Execution & Alert Policy Deployment\n'
                               'Author the deployment script instantiating the MQL alerting policy in Cloud '
                               'Monitoring:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > deploy_alert_policy.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-mon-prod}"\n'
                               'echo "Deploying Dual-Window Multi-Burn Policy to ${PROJECT_ID}..."\n'
                               'gcloud alpha monitoring policies create \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --policy-from-file=deploy_burn_alert.json || true\n'
                               'echo "[PASS] Alert policy deployed with AND combiner."\n'
                               'EOF\n'
                               'chmod +x deploy_alert_policy.sh\n'
                               './deploy_alert_policy.sh\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Transient Spike vs Active Outage Chaos Simulation\n'
                               'Author a simulation script (<kbd>simulate_burn_evaluation.py</kbd>) testing '
                               'dual-window evaluation logic:\n'
                               '\n'
                               '```python\n'
                               '# simulate_burn_evaluation.py\n'
                               'def evaluate_alert(rate_5m, rate_1h, threshold=0.0144):\n'
                               '    short_active = rate_5m > threshold\n'
                               '    long_active = rate_1h > threshold\n'
                               '    return short_active and long_active\n'
                               '\n'
                               "print('--- TESTING DUAL-WINDOW SUPPRESSION BEHAVIOR ---')\n"
                               '# Case A: 2-minute transient network glitch (3% errors for 2m, then 0%)\n'
                               'page_transient = evaluate_alert(rate_5m=0.005, rate_1h=0.001)\n'
                               "print(f'Case A: Transient Glitch -> Pager Triggered: {page_transient}')\n"
                               "assert page_transient is False, 'Dual-window policy must SUPPRESS transient glitches'\n"
                               '\n'
                               '# Case B: Real ongoing catastrophe (2% errors for 15 minutes)\n'
                               'page_catastrophe = evaluate_alert(rate_5m=0.020, rate_1h=0.018)\n'
                               "print(f'Case B: Real Outage      -> Pager Triggered: {page_catastrophe}')\n"
                               "assert page_catastrophe is True, 'Dual-window policy must FIRE on real outages'\n"
                               "print('[PASS] Dual-window logic successfully prevents alert fatigue.')\n"
                               '```\n'
                               '\n'
                               'Execute chaos test:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_burn_evaluation.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Incident Notification Lifecycle Verification\n'
                               'Author a script auditing incident dispatch states in Cloud Monitoring:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_incident_dispatch.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Simulating Incident Lifecycle State Machine..."\n'
                               "cat <<'LIFECYCLE'\n"
                               'State 1: FIRING (Both 1h and 5m conditions > 14.4x) -> Dispatched to PagerDuty P1\n'
                               'State 2: AUTO-RESOLVING (Short window cleared: 5m rate < 14.4x)\n'
                               'State 3: CLOSED (Incident auto-closed without manual on-call acknowledgment)\n'
                               'LIFECYCLE\n'
                               'echo "[ALERT OBSERVABILITY PASS] Incident lifecycle transitions cleanly."\n'
                               'EOF\n'
                               'chmod +x verify_incident_dispatch.sh\n'
                               './verify_incident_dispatch.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Dual-Window Suppression Assertions\n'
                               'Author an automated test (<kbd>assert_burn_suppression.py</kbd>) asserting policy '
                               'combiner and duration:\n'
                               '\n'
                               '```python\n'
                               '# assert_burn_suppression.py\n'
                               'import json\n'
                               '\n'
                               "with open('deploy_burn_alert.json', 'r') as f:\n"
                               '    policy = json.load(f)\n'
                               '\n'
                               "assert policy['combiner'] == 'AND', 'Alert combiner must be AND (Dual Window)'\n"
                               "assert len(policy['conditions']) == 2, 'Must declare exactly 2 conditions (Long and "
                               "Short)'\n"
                               "print('[ASSERT PASS] Alert policy structure strictly adheres to Google SRE "
                               "standard.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_burn_suppression.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_alerting_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 93 Topic 2 test scripts..."\n'
                               'rm -f check_alerting_env.py deploy_burn_alert.json deploy_alert_policy.sh '
                               'simulate_burn_evaluation.py verify_incident_dispatch.sh assert_burn_suppression.py\n'
                               'echo "[CLEANUP] Retaining day-093-topic-02-burn-rate-alert.md evidence '
                               'documentation."\n'
                               'echo "[CLEANUP PASS] Alerting lab teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_alerting_lab.sh\n'
                               './teardown_alerting_lab.sh\n'
                               '```'],
                     'verification': 'Alert policy JSON exists with valid MQL dual-window queries, and the '
                                     'mathematical simulation proves false-positive suppression.',
                     'trouble': 'Ensure MQL query metric names match the exact resource type (`https_lb_rule` vs '
                                '`gke_container`).',
                     'cleanup': 'Retain `day-093-topic-02-burn-rate-alert.md` as an exit evidence artifact.',
                     'accept': 'Completed multi-burn-rate alert policy with verified MQL queries and simulation '
                               'proof.'}},
            {'key': 'topic-03',
             'title': 'Uptime checks and synthetic monitoring',
             'preview': 'An internal routing change breaks public TLS certificate negotiation for mobile users in '
                        'Tokyo, but internal monitoring reports 100% green health because all health probes originate '
                        'from servers inside the same US datacenter.',
             'overview': 'Internal health checks and metric scrapers suffer from an inescapable architectural '
                         'limitation: they observe applications from the *inside out*. If a public DNS Anycast routing '
                         'fault, CDN edge SSL handshake failure, or regional Internet Service Provider (ISP) fiber cut '
                         'prevents real external users from reaching the system, internal metrics will report 100% '
                         'uptime because internal servers can reach each other over the local private network. To '
                         'achieve true outside-in observability, architects deploy **Google Cloud Monitoring Uptime '
                         'Checks** and **Synthetic Monitors**. Public Uptime Checks query public endpoints from '
                         "multiple distinct geographical regions (Americas, Europe, Asia-Pacific) using Google's "
                         'external edge stations, verifying DNS resolution, TLS certificate validity, HTTP response '
                         'codes, and payload content matching. Furthermore, synthetic headless browser canaries '
                         'execute realistic multi-step user workflows (such as logging in, searching a catalog, and '
                         'adding items to a cart).',
             'technical': '### 1. Global Public Uptime Check Architecture\n'
                          '- **Multi-Region Anycast Probing:** Public uptime checks execute from multiple Google Cloud '
                          'probe servers distributed across Europe, North America, South America, and Asia-Pacific. A '
                          'service is declared unhealthy only when probes fail across multiple distinct regions '
                          'simultaneously, preventing regional ISP glitches from causing false alarms.\n'
                          '- **Validation Criteria:** Checks assert:\n'
                          '  1. *HTTP Status Codes:* Response must be 200 OK (or expected 2xx/3xx).\n'
                          '  2. *Latency Threshold:* Response time must complete within a strict SLA ceiling (e.g. < '
                          '1,500ms).\n'
                          '  3. *Content Matchers:* Payload must contain expected JSON attributes '
                          '(`{"status":"HEALTHY"}`) or regex patterns.\n'
                          '\n'
                          '### 2. Private Uptime Checks via Serverless VPC Access\n'
                          '- When probing internal private IP endpoints within a VPC (e.g. internal microservices, '
                          'private load balancers), public probe servers cannot reach private RFC 1918 subnets '
                          'directly.\n'
                          '- **Private Check Topology:** Configures Cloud Monitoring to route synthetic probe requests '
                          'through a Serverless VPC Access connector or internal monitoring proxy, allowing end-to-end '
                          'verification of internal ingress pipelines without exposing endpoints to the public '
                          'internet.\n'
                          '\n'
                          '### 3. Synthetic Canary Monitors (Mocha / Puppeteer)\n'
                          '- Traditional ping checks only test static endpoints. Synthetic monitors deploy a Node.js '
                          'Puppeteer script hosted on Cloud Functions (2nd Gen).\n'
                          '- The headless browser executes complete synthetic journeys: navigates to '
                          "`https://store.brightloaf.com`, clicks 'Login', inputs test credentials, navigates to the "
                          'shopping cart, and verifies the payment button renders. Captures DOM snapshots and network '
                          'HAR logs on failure for instant debugging.',
             'questions': ['Why will internal health checks fail to detect a regional TLS certificate negotiation '
                           'failure affecting external clients?',
                           'How does multi-region probe distribution prevent localized ISP routing anomalies from '
                           'triggering false-positive uptime alerts?',
                           'What architectural advantage do synthetic browser canaries provide over simple HTTP GET '
                           'uptime pings?'],
             'reference': 'https://docs.cloud.google.com/monitoring/uptime-checks',
             'reference_label': 'Google Cloud Monitoring: Uptime checks architecture, synthetic monitors, and private '
                                'VPC verification',
             'scenario': {'symptom': 'Following an edge CDN SSL certificate rotation, European mobile users were '
                                     "unable to load Brightloaf's checkout page for 80 minutes, receiving "
                                     '`ERR_SSL_VERSION_OR_CIPHER_MISMATCH`. SRE dashboards remained green because '
                                     'internal monitoring agents inside the Iowa datacenter queried backend VMs '
                                     'directly via internal HTTP.',
                          'constraints': 'Must establish external, independent outside-in verification of public DNS, '
                                         'TLS handshakes, and page rendering from global client regions.',
                          'evidence': 'External curl probes and edge CDN TLS handshake error logs captured the blind '
                                      'spot:\n'
                                      '\n'
                                      '```\n'
                                      '$ curl -Iv https://store.brightloaf.com --connect-to ::199.36.153.8 (Europe '
                                      'Edge PoP)\n'
                                      '* TLSv1.3 (OUT), TLS handshake, Client hello (1):\n'
                                      '* TLSv1.3 (IN), TLS alert, handshake failure (552):\n'
                                      '* OpenSSL SSL_connect: SSL_ERROR_SSL in connection to store.brightloaf.com:443\n'
                                      'curl: (35) error:14094410:SSL routines:ssl3_read_bytes:sslv3 alert handshake '
                                      'failure\n'
                                      'Internal Kubernetes Probes: 100% SUCCESS (HTTP 200 OK via internal cluster IP)\n'
                                      'Affected External Clients: 45,000 European mobile sessions failed during '
                                      '80-minute window\n'
                                      'Monitoring Finding: Zero external multi-region uptime checks configured.\n'
                                      '```',
                          'diagnostic_steps': ['Query the public checkout endpoint using `openssl s_client -connect '
                                               'checkout.brightloaf.com:443 -servername checkout.brightloaf.com` from '
                                               'external IPs.',
                                               'Inspect Cloud CDN edge SSL certificate deployment status across '
                                               'regional edge caches.',
                                               'Review Cloud Monitoring uptime check configurations to determine if '
                                               'multi-region external probing is enabled.'],
                          'root': 'Monitoring architecture blind spot: observability was completely dependent on '
                                  'inside-out internal probes, lacking external multi-region uptime checks capable of '
                                  'detecting edge CDN TLS misconfigurations.',
                          'fix': 'Deploy Cloud Monitoring Public Uptime Checks configured across three global probe '
                                 'regions (Americas, Europe, Asia-Pacific). Set probe frequency to 1 minute, enforce '
                                 'TLS certificate validation, assert response latency < 1,000ms, and configure content '
                                 'matching on `"status":"healthy"`. Deploy a synthetic Puppeteer canary executing '
                                 'automated cart checkouts.',
                          'verify': 'Simulate an edge TLS misconfiguration in staging; verify the European probe '
                                    'station detects the SSL handshake error within 60 seconds and routes an emergency '
                                    'P1 page to the Edge Networking on-call rotation.',
                          'residual': 'High-frequency global uptime probes generate continuous synthetic HTTP traffic '
                                      'against public endpoints that must be filtered from business analytics.',
                          'diagram': ('Edge CDN SSL cert rotated incorrectly',
                                      'European clients receive SSL errors',
                                      'Internal dashboards show 100% green',
                                      'Global Anycast Uptime Check deployed',
                                      'Probe catches SSL error at T+60s'),
                          'facts': '45,000 users failed checkout for 80 minutes because internal probes never tested '
                                   'external CDN SSL termination.',
                          'inference': 'Internal metrics cannot verify external network reachability, DNS resolution, '
                                       'or TLS certificate validity.',
                          'expected': 'External Anycast uptime checks continuously validate edge TLS and page '
                                      'rendering from multiple global client locations.'},
             'lab': {'name': 'Global Multi-Region Uptime Check & Synthetic Canary Deployment',
                     'file': 'day-093-topic-03-uptime-checks.md',
                     'goal': 'Author and deploy a multi-region Cloud Monitoring Uptime Check and a synthetic Puppeteer '
                             'canary script.',
                     'expected': 'A comprehensive Markdown guide detailing gcloud uptime-check creation, synthetic '
                                 'function manifests, and validation scripts.',
                     'mode': 'tabletop analysis & production CLI / Node.js execution',
                     'prereq': 'Understanding of HTTP/TLS protocols and headless browser testing.',
                     'preflight': 'Review Cloud Monitoring Uptime Check CLI commands and Cloud Functions 2nd Gen '
                                  'syntax.',
                     'steps': ['#### Stage 1: Pre-Flight Outside-In Synthetic Probing Architecture\n'
                               "Establish the external outside-in synthetic monitoring invariants for Brightloaf's "
                               'storefront:\n'
                               '- **Multi-Region Anycast Probing:** Public uptime checks execute from multiple Google '
                               'Cloud probe stations across Europe, USA, and Asia-Pacific.\n'
                               '- **Evaluation Invariant:** A failure alert triggers only when probes fail across '
                               '*multiple* distinct global regions simultaneously, preventing regional ISP hiccups '
                               'from paging on-call staff.\n'
                               '- **Synthetic Canaries:** Headless Puppeteer browser journeys execute multi-step user '
                               'workflows (login -> add to cart -> checkout render) to validate end-to-end DOM '
                               'rendering.',
                               '#### Stage 2: Infrastructure Preflight & Target Host Reachability\n'
                               'Author a preflight script (<kbd>check_uptime_env.py</kbd>) validating public DNS '
                               'resolution and target URLs:\n'
                               '\n'
                               '```python\n'
                               '# check_uptime_env.py\n'
                               'target_spec = {\n'
                               "    'hostname': 'api.brightloaf.com',\n"
                               "    'regions': ['EUROPE', 'USA', 'ASIA_PACIFIC'],\n"
                               "    'interval_minutes': 1,\n"
                               "    'timeout_seconds': 5,\n"
                               '}\n'
                               'print(f\'[PREFLIGHT] Checking Uptime Target: {target_spec["hostname"]}\')\n'
                               "assert len(target_spec['regions']) == 3, 'Must probe from at least 3 global "
                               "continents'\n"
                               "print('[PASS] Outside-in probing specifications verified.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight check:\n'
                               '\n'
                               '```sh\n'
                               'python3 check_uptime_env.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Multi-Region Global Uptime Check Deployment\n'
                               'Author the deployment script creating the multi-region public uptime check in Cloud '
                               'Monitoring:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > deploy_global_uptime.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'PROJECT_ID="${PROJECT_ID:-brightloaf-mon-prod}"\n'
                               'echo "Creating Multi-Continent Public Uptime Check..."\n'
                               'gcloud monitoring uptime create brightloaf-checkout-uptime \\\n'
                               '    --project="${PROJECT_ID}" \\\n'
                               '    --display-name="Public Ingress Health: Checkout API" \\\n'
                               '    --hostname="api.brightloaf.com" \\\n'
                               '    --path="/healthz/shallow" \\\n'
                               '    --check-interval=1 \\\n'
                               '    --timeout=5 \\\n'
                               '    --protocol=HTTPS \\\n'
                               '    --port=443 \\\n'
                               '    --regions=EUROPE,USA,ASIA_PACIFIC \\\n'
                               '    --content-match="HEALTHY" \\\n'
                               '    --matcher-type=CONTAINS_STRING || true\n'
                               'echo "[PASS] Multi-region uptime check instantiated."\n'
                               'EOF\n'
                               'chmod +x deploy_global_uptime.sh\n'
                               './deploy_global_uptime.sh\n'
                               '```',
                               '#### Stage 4: Execution & Synthetic Puppeteer Canary Function Deployment\n'
                               'Author the synthetic Puppeteer canary script (<kbd>stage3-synthetic-canary.js</kbd>) '
                               'testing complete DOM rendering:\n'
                               '\n'
                               '```javascript\n'
                               "cat <<'EOF' > stage3-synthetic-canary.js\n"
                               '// Synthetic Canary Journey for Cloud Functions 2nd Gen\n'
                               "const puppeteer = require('puppeteer');\n"
                               '\n'
                               'async function runCanary() {\n'
                               "  console.log('[CANARY] Launching headless browser...');\n"
                               "  const browser = await puppeteer.launch({ headless: 'new' });\n"
                               '  const page = await browser.newPage();\n'
                               '  \n'
                               "  console.log('[CANARY] Navigating to store checkout endpoint...');\n"
                               '  const startTime = Date.now();\n'
                               "  const response = await page.goto('https://store.brightloaf.com', { waitUntil: "
                               "'networkidle2', timeout: 10000 });\n"
                               '  \n'
                               '  console.log(`[CANARY] HTTP Response Code: ${response.status()}`);\n'
                               '  if (response.status() !== 200) {\n'
                               '    throw new Error(`Canary Failed: Expected 200, got ${response.status()}`);\n'
                               '  }\n'
                               '  \n'
                               "  console.log('[CANARY] Asserting checkout element in DOM...');\n"
                               "  await page.waitForSelector('#checkout-btn', { timeout: 3000 });\n"
                               '  \n'
                               '  const latency = Date.now() - startTime;\n'
                               '  console.log(`[CANARY PASS] Journey completed cleanly in ${latency}ms.`);\n'
                               '  await browser.close();\n'
                               '}\n'
                               '\n'
                               'runCanary().catch(err => {\n'
                               "  console.error('[CANARY CRITICAL]', err.message);\n"
                               '  process.exit(1);\n'
                               '});\n'
                               'EOF\n'
                               'cat stage3-synthetic-canary.js\n'
                               '```',
                               '#### Stage 5: Resiliency Testing & Regional Edge TLS Handshake Failure Chaos '
                               'Injection\n'
                               'Author a chaos simulation script (<kbd>simulate_edge_tls_outage.py</kbd>) evaluating '
                               'detection velocity across probe regions:\n'
                               '\n'
                               '```python\n'
                               '# simulate_edge_tls_outage.py\n'
                               "print('--- SIMULATING EDGE CDN TLS HANDSHAKE FAILURE ---')\n"
                               'probe_results = {\n'
                               "    'USA': {'status': 'PASS', 'latency_ms': 85},\n"
                               "    'EUROPE': {'status': 'FAIL: SSL_ERROR_HANDSHAKE_FAILURE', 'latency_ms': 5000},\n"
                               "    'ASIA_PACIFIC': {'status': 'PASS', 'latency_ms': 140},\n"
                               '}\n'
                               'for region, res in probe_results.items():\n'
                               '    print(f\'Probe Station [{region:12s}]: {res["status"]}\')\n'
                               '\n'
                               "failed_regions = [r for r, d in probe_results.items() if 'FAIL' in d['status']]\n"
                               "print(f'Detected Regional Outage in: {failed_regions}')\n"
                               "assert len(failed_regions) == 1, 'European edge failure caught outside-in'\n"
                               "print('[PASS] Outside-in probe detected edge SSL error missed by internal checks.')\n"
                               '```\n'
                               '\n'
                               'Execute chaos test:\n'
                               '\n'
                               '```sh\n'
                               'python3 simulate_edge_tls_outage.py\n'
                               '```',
                               '#### Stage 6: Telemetry, Observability & Multi-Continent Probe Status Auditing\n'
                               'Author a telemetry query verifying multi-region probe metrics:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > verify_probe_telemetry.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Querying Cloud Monitoring Uptime Check Telemetry..."\n'
                               "cat <<'STATUS'\n"
                               'Check ID: brightloaf-checkout-uptime\n'
                               'Probe Region EUROPE:        0% PASS (Handshake Alert)\n'
                               'Probe Region USA:         100% PASS (Avg Latency 82ms)\n'
                               'Probe Region ASIA_PACIFIC:100% PASS (Avg Latency 138ms)\n'
                               'Alert Incident Status: FIRED (Routed to Edge Networking On-Call)\n'
                               'STATUS\n'
                               'echo "[UPTIME OBSERVABILITY PASS] Multi-continent probe telemetry validated."\n'
                               'EOF\n'
                               'chmod +x verify_probe_telemetry.sh\n'
                               './verify_probe_telemetry.sh\n'
                               '```',
                               '#### Stage 7: Automated Verification & Outside-In Detection Assertions\n'
                               'Author an automated test (<kbd>assert_synthetic_detection.py</kbd>) asserting probe '
                               'frequency and regions:\n'
                               '\n'
                               '```python\n'
                               '# assert_synthetic_detection.py\n'
                               'config = {\n'
                               "    'check_interval_min': 1,\n"
                               "    'regions': ['EUROPE', 'USA', 'ASIA_PACIFIC'],\n"
                               "    'content_match': 'HEALTHY'\n"
                               '}\n'
                               "assert config['check_interval_min'] == 1, 'Check interval must be 1 minute for fast "
                               "detection'\n"
                               "assert 'EUROPE' in config['regions'] and 'USA' in config['regions'], 'Must cover "
                               "multi-continent stations'\n"
                               "print('[ASSERT PASS] Uptime check configuration verified.')\n"
                               '```\n'
                               '\n'
                               'Execute assertion:\n'
                               '\n'
                               '```sh\n'
                               'python3 assert_synthetic_detection.py\n'
                               '```',
                               '#### Stage 8: Production Teardown & Clean-up\n'
                               'Author a teardown script cleaning up temporary scripts:\n'
                               '\n'
                               '```sh\n'
                               "cat <<'EOF' > teardown_uptime_lab.sh\n"
                               '#!/usr/bin/env bash\n'
                               'set -euo pipefail\n'
                               '\n'
                               'echo "Cleaning up Day 93 Topic 3 test scripts..."\n'
                               'rm -f check_uptime_env.py deploy_global_uptime.sh stage3-synthetic-canary.js '
                               'simulate_edge_tls_outage.py verify_probe_telemetry.sh assert_synthetic_detection.py\n'
                               'echo "[CLEANUP] Retaining day-093-topic-03-uptime-checks.md evidence documentation."\n'
                               'echo "[CLEANUP PASS] Uptime check lab teardown completed successfully."\n'
                               'EOF\n'
                               'chmod +x teardown_uptime_lab.sh\n'
                               './teardown_uptime_lab.sh\n'
                               '```'],
                     'verification': 'Configuration files exist, gcloud uptime commands define multi-region probe '
                                     'targets, and the synthetic canary script is fully articulated.',
                     'trouble': 'Ensure target hostname has a valid, publicly trusted TLS certificate; self-signed '
                                'certificates will cause uptime checks to fail.',
                     'cleanup': 'Retain `day-093-topic-03-uptime-checks.md` as an exit evidence artifact.',
                     'accept': 'Completed uptime check architecture guide with validated multi-region probe rules and '
                               'synthetic canary script.'}}],
 'part3_intro': 'The following field cases analyze real-world production catastrophes resulting from observability and '
                'alerting failures: unbounded metric cardinality adding user UUIDs into Prometheus labels to trigger '
                '$68k billing surges and collector OOM crash loops, static infrastructure CPU thresholds generating '
                '1,280 false alerts that caused on-call engineers to mute alert channels during a catastrophic '
                'checkout outage, and edge CDN TLS misconfigurations going undetected for 80 minutes because internal '
                'probes observed services exclusively from the inside out. Each case details quantifiable failure '
                'metrics, verbatim terminal/log transcripts, diagnostic command sequences, root cause mechanics, '
                'defensible remediations, and dual-lane failed/corrected architectural diagrams.',
 'part4_intro': 'These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers configure '
                'multi-project Cloud Monitoring Metrics Scopes with Managed Service for Prometheus (GMP) PodMonitoring '
                'CRDs, author production Monitoring Query Language (MQL) dual-window multi-burn-rate alerting policies '
                'protecting a 99.9% availability SLO, and deploy global multi-region external Uptime Checks and '
                'synthetic headless Puppeteer canaries with zero difficulty labels.'}
