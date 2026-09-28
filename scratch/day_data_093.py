"""day_data_093.py — Exhaustive architecture data specification for Day 93.

Covers Metrics, Alerting, and Burn Rates:
1. Cloud Monitoring: metric models, metric descriptors, Metrics Scopes (multi-project scoping), Custom Metrics, and Google Cloud Managed Service for Prometheus (GMP).
2. Alerting policies: MQL/PromQL condition definitions, notification channels, incident lifecycles, alert fatigue elimination, multi-window multi-burn-rate SLO alerts.
3. Uptime checks and synthetic monitoring: global Anycast probing regions, private VPC uptime checks, synthetic Puppeteer canary scripting.
Follows PAGE_AUTHORING_CONTRACT.md with progressive 3-stage labs (Beginner → Intermediate → Advanced).
"""

DAY_NUM = 93

DATA = {
    "day": 93,
    "part1_intro": (
        "Day 93 shifts from infrastructure survivability to continuous operational observability: instrumentation telemetry, "
        "incident alerting systems, and mathematical error budget consumption. Observability is not merely the passive collection "
        "of CPU statistics; it is the active discipline that proves whether user-facing commitments are being satisfied in real time. "
        "Poor alerting is as destructive as no alerting: uncalibrated static thresholds flood on-call engineers with hundreds of spurious "
        "pages, creating alert fatigue that causes real outages to be ignored. Today's curriculum establishes multi-project Google Cloud "
        "Monitoring Scopes and Managed Service for Prometheus (GMP), constructs multi-window multi-burn-rate alerting policies that alert on "
        "symptom severity rather than component noise, and deploys global Anycast uptime checks and synthetic headless canaries to detect "
        "user-facing regressions before customer complaints arrive."
    ),
    "exit_summary": (
        "Engineered an enterprise Telemetry and Multi-Burn-Rate Alerting Architecture: established a multi-project Cloud Monitoring Metrics Scope "
        "with Google Cloud Managed Service for Prometheus (GMP) ingestion; authored a production Monitoring Query Language (MQL) dashboard definition; "
        "deployed dual-window multi-burn-rate alert policies (1h/5m and 6h/30m) protecting a 99.9% availability SLO; configured automated global "
        "uptime checks across multi-continent probe stations with latency assertion gates."
    ),
    "part2_intro": (
        "Reliable observability decouples metric ingestion from alert generation, transforming high-cardinality time series into actionable incident signals. "
        "The sections below analyze Prometheus metric pipelines, multi-burn-rate mathematical formulas, and global synthetic probing mechanics."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Telemetry Layer</th>
      <th>Primary GCP Mechanism</th>
      <th>Ingestion Model &amp; Protocol</th>
      <th>Data Retention &amp; Limits</th>
      <th>Architectural Failure Mode / Anti-Pattern</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Infrastructure Telemetry</strong></td>
      <td>Google Cloud Monitoring (Ops Agent)</td>
      <td>Push-based collectd/Fluent Bit agent via Cloud Logging/Monitoring API</td>
      <td>6 weeks at 1-minute resolution, downsampled to 10-minute/1-hour</td>
      <td>Missing Ops Agent on custom images; blind spots on disk I/O and guest RAM</td>
    </tr>
    <tr>
      <td><strong>Prometheus Metrics</strong></td>
      <td>Managed Service for Prometheus (GMP)</td>
      <td>Pull-based scrape via lightweight PodMonitoring / NodeMonitoring CRDs</td>
      <td>24 months retention; global managed storage without Prometheus server state</td>
      <td>Unbounded metric cardinality (e.g. user IDs in labels) causing massive ingestion bills</td>
    </tr>
    <tr>
      <td><strong>SLO Multi-Burn Alerting</strong></td>
      <td>Cloud Monitoring Alert Policies (MQL)</td>
      <td>Real-time evaluation engine tracking short and long lookback windows</td>
      <td>Sub-minute evaluation; alerts routed to PagerDuty/PubSub/Slack channels</td>
      <td>Single-window static threshold alerting; premature paging during transient spikes</td>
    </tr>
    <tr>
      <td><strong>Synthetic Availability</strong></td>
      <td>Cloud Monitoring Uptime Checks &amp; Synthetics</td>
      <td>Multi-region external Anycast probes (Americas, Europe, Asia-Pacific)</td>
      <td>1-minute check frequency; response status, latency, and content matching</td>
      <td>Probing internal VPC endpoints from public stations without Serverless VPC Access</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 93: Enterprise Observability and Multi-Burn-Rate Alerting Pipeline",
        "desc": "End-to-end telemetry architecture from container scrape to multi-window burn rate alert triggers and synthetic validation.",
        "caption": "Figure 93.1: Architecture pipeline separating Prometheus metric scraping, Cloud Monitoring multi-project scoping, and multi-burn-rate incident dispatch.",
        "nodes": [
            ("1. Telemetry Ingestion", "GMP PodMonitoring Scrape\\nOps Agent Guest Telemetry"),
            ("2. Scoping & Storage", "Metrics Scope Aggregation\\n24-Month Time-Series Storage"),
            ("3. MQL Burn Analysis", "Dual-Window Evaluation\\nShort (5m) & Long (1h) Filters"),
            ("4. Alert Dispatch", "PagerDuty P1 Escalation\\nUptime Synthetic Checkpoint"),
        ]
    },
    "topics": [
        {
            "key": "topic-01",
            "title": "Cloud Monitoring",
            "preview": (
                "An enterprise running 80 microservices across 15 separate GCP projects discovers that SREs must manually open 15 separate "
                "browser tabs to troubleshoot cross-project database queries, adding 40 minutes of blind triage time during a major payment outage."
            ),
            "overview": (
                "**Google Cloud Monitoring** provides centralized, full-stack observability across cloud infrastructure, managed services, "
                "and custom applications. In modern multi-project enterprise architectures, observability must transcend individual project "
                "boundaries. By establishing a **Metrics Scope**, organizations designate a central 'scoping project' that aggregates metrics, "
                "dashboards, and uptime checks from multiple monitored projects into a unified single-pane-of-glass interface. Furthermore, "
                "for containerized Kubernetes workloads, **Google Cloud Managed Service for Prometheus (GMP)** eliminates the operational "
                "overhead of self-hosting Prometheus servers: it uses lightweight PodMonitoring Custom Resource Definitions (CRDs) to scrape "
                "endpoints and ingests time series directly into Google's scalable, planet-scale time-series database with 24 months of retention."
            ),
            "technical": (
                "### 1. Metrics Scopes and Multi-Project Architectures\n"
                "- **The Scoping Project:** A designated Google Cloud project (e.g. `brightloaf-monitoring-prod`) configured as the Metrics Scope host. "
                "Monitored projects (e.g. `brightloaf-billing`, `brightloaf-checkout`, `brightloaf-inventory`) are added to the scope via the "
                "Monitoring metrics-scopes API (`monitoring.metricsScopes.link`).\n"
                "- **Unified Cross-Project Querying:** Once scoped, SREs query metrics across all 15 projects in a single MQL query using the "
                "`resource.project_id` filter, correlating downstream database latency in Project B with frontend 504 timeouts in Project A.\n\n"
                "### 2. Managed Service for Prometheus (GMP) Architecture\n"
                "- **Managed Collectors:** GKE clusters enable GMP with a single toggle (`--enable-managed-prometheus`). Google provisions and manages "
                "daemonset collectors that scrape target pods without requiring local Prometheus stateful disks or alertmanager infrastructure.\n"
                "- **Declarative PodMonitoring:** Telemetry targets are defined using Kubernetes-native CRDs:\n"
                "  `apiVersion: monitoring.googleapis.com/v1` with `kind: PodMonitoring`. Defines scrape intervals (e.g. 15s), metric paths (`/metrics`), "
                "and label filters.\n"
                "- **High-Cardinality Governance:** Metric ingestion charges are billed per million samples. Developers must never insert unbounded "
                "dimensions (such as user IDs, UUIDs, or email addresses) into metric labels; high-cardinality metadata belongs in Cloud Logging or Trace, "
                "not metric time series.\n\n"
                "### 3. Custom Metrics and Metric Descriptors\n"
                "- **Metric Types:** Gauges (instantaneous values like queue depth), Cumulative (monotonically increasing counters like total requests), "
                "and Delta (change over evaluation interval).\n"
                "- **Value Types:** INT64, DOUBLE, BOOLEAN, and DISTRIBUTION (histograms tracking request latency percentiles: P50, P95, P99)."
            ),
            "questions": [
                "How does configuring a centralized Metrics Scope eliminate operational blind spots across multi-project microservice environments?",
                "What architectural risks are introduced when high-cardinality metadata (like user UUIDs) is placed in Prometheus metric labels?",
                "Why does Google Cloud Managed Service for Prometheus (GMP) use PodMonitoring CRDs rather than traditional ConfigMaps?",
            ],
            "reference": "https://docs.cloud.google.com/monitoring/docs",
            "reference_label": "Google Cloud Monitoring: Metric architecture, multi-project scoping, and Managed Service for Prometheus",
            "scenario": {
                "symptom": (
                    "During a peak trading surge, Brightloaf's monthly Cloud Monitoring bill spiked by $68,000 in 72 hours, while GKE collector pods "
                    "began OOMKilled crash loops that dropped 60% of infrastructure performance metrics."
                ),
                "constraints": (
                    "Must preserve sub-minute application latency monitoring while eliminating metric billing surges and collector memory exhaustion."
                ),
                "evidence": (
                    "Metrics Explorer revealed the custom counter `http_requests_total` possessed 4.2 million active time series. A developer "
                    "had committed a code change adding `user_id: <uuid>` as a Prometheus metric label, generating a unique metric series for every shopper."
                ),
                "diagnostic_steps": [
                    "Inspect Cloud Monitoring billing breakdown grouped by Metric Type to identify the offending metric descriptor.",
                    "Query the Metric Descriptors API to audit label keys attached to `custom.googleapis.com` and GMP metrics.",
                    "Inspect Git commit diffs on the API server's Prometheus metric instrumentation interceptor.",
                ],
                "root": (
                    "Unbounded metric cardinality: adding unique user IDs to Prometheus metric labels created millions of distinct time series, "
                    "saturating collector memory and exploding metric ingestion fees."
                ),
                "fix": (
                    "Remove the `user_id` label from the Prometheus metric interceptor; retain only bounded labels (`method`, `status_code`, `route`). "
                    "Pass `user_id` exclusively in structured JSON logs via Cloud Logging and Cloud Trace span attributes. Implement a pre-commit "
                    "linter rejecting high-cardinality metric labels."
                ),
                "verify": (
                    "Deploy the corrected PodMonitoring manifest in staging; verify active time series for `http_requests_total` drops from 4,200,000 "
                    "to 36, and collector pod memory stabilizes at 85 MB."
                ),
                "residual": (
                    "Historical high-cardinality time series will persist in Cloud Monitoring storage until their standard 6-week metric retention expires."
                ),
                "diagram": (
                    "User ID added to metric label",
                    "4.2M active time series created",
                    "$68k billing surge & collector OOM",
                    "High-cardinality labels stripped",
                    "Time series drops to 36; bill drops"
                ),
                "facts": "A single unbounded `user_id` label created 4.2M time series and a $68k bill because metrics are billed per ingested sample.",
                "inference": "Metrics are intended for mathematical aggregation across bounded dimensions; identity traces belong in Logging/Trace.",
                "expected": "Prometheus metric labels remain strictly bounded (< 100 values per key), keeping collector memory and billing predictable."
            },
            "lab": {
                "name": "Cloud Monitoring Metrics Scope & GMP PodMonitoring Ingestion",
                "file": "day-093-topic-01-metrics-scope.md",
                "level": "Progressive: Beginner → Intermediate → Advanced",
                "goal": "Establish a multi-project Metrics Scope, deploy Managed Service for Prometheus (GMP), and verify bounded metric ingestion.",
                "expected": "A comprehensive configuration guide with exact gcloud commands creating scopes and a validated Kubernetes PodMonitoring manifest.",
                "mode": "tabletop analysis & manifest synthesis",
                "prereq": "Understanding of Kubernetes manifests and Prometheus metrics.",
                "preflight": "Review Google Cloud Managed Service for Prometheus documentation and gcloud monitoring syntax.",
                "steps": [
                    "**Stage 1: Beginner (Baseline Discovery & Configuration Inspection)**\n- Query existing monitoring project configuration and inspect default metric descriptors:\n\n```sh\ncat <<'EOF' > stage1-inspect-monitoring.sh\n# Step 1.1: Verify current project and monitoring API enablement\ngcloud services list --enabled --filter=\"NAME:monitoring.googleapis.com\"\n\n# Step 1.2: Inspect default Compute Engine CPU metric descriptor\ngcloud monitoring metric-descriptors describe \\\n    compute.googleapis.com/instance/cpu/utilization \\\n    --format='yaml(metricKind, valueType, unit)'\nEOF\ncat stage1-inspect-monitoring.sh\n```",
                    "**Stage 2: Intermediate (Implementation, Deployment & Policy Enforcement)**\n- Create a multi-project Metrics Scope and deploy a bounded GKE PodMonitoring manifest:\n\n```sh\ncat <<'EOF' > stage2-deploy-scoping.sh\n# Step 2.1: Add workload project to the centralized metrics scoping project\ngcloud monitoring metrics-scopes list\n\n# Step 2.2: Define Kubernetes PodMonitoring CRD with bounded dimensions\ncat <<'YAML' > pod-monitoring-orders.yaml\napiVersion: monitoring.googleapis.com/v1\nkind: PodMonitoring\nmetadata:\n  name: orders-api-monitor\n  namespace: production\nspec:\n  selector:\n    matchLabels:\n      app.kubernetes.io/name: orders-api\n  endpoints:\n  - port: metrics\n    path: /metrics\n    interval: 15s\n    metricRelabeling:\n    # Drop any dangerous high-cardinality labels before ingestion\n    - action: labeldrop\n      regex: (user_id|session_id|email|customer_token)\nYAML\ncat pod-monitoring-orders.yaml\nEOF\ncat stage2-deploy-scoping.sh\n```",
                    "**Stage 3: Advanced (Chaos Injection, Failure Rehearsal & Resilience Verification)**\n- Simulate an ingestion cardinality surge and execute an automated Python validation script asserting metric boundedness:\n\n```sh\ncat <<'EOF' > stage3-verify-cardinality.py\n# Test script validating that metric time-series cardinality remains bounded\nmetrics_sample = [\n    {\"route\": \"/checkout\", \"method\": \"POST\", \"status\": \"200\"},\n    {\"route\": \"/checkout\", \"method\": \"POST\", \"status\": \"500\"},\n    {\"route\": \"/catalog\", \"method\": \"GET\", \"status\": \"200\"},\n    {\"route\": \"/healthz\", \"method\": \"GET\", \"status\": \"200\"},\n]\n\n# Assert total unique label permutations <= 50 (Bounded Cardinality Rule)\nunique_combinations = set(tuple(m.items()) for m in metrics_sample)\nprint(f\"Total unique label dimensions: {len(unique_combinations)}\")\nassert len(unique_combinations) <= 50, \"CRITICAL: Cardinality exceeds safe operational bounds!\"\nprint(\"PASS: Metric cardinality strictly conforms to production budget.\")\nEOF\npython3 stage3-verify-cardinality.py\n```",
                    "Review all output artifacts and confirm that `pod-monitoring-orders.yaml` strips high-cardinality labels before ingestion."
                ],
                "verification": (
                    "Configuration files exist, PodMonitoring manifest includes defensive labeldrop filters, and cardinality validation script passes."
                ),
                "trouble": "Ensure GKE cluster has `--enable-managed-prometheus` flag set before applying `monitoring.googleapis.com/v1` CRDs.",
                "cleanup": "Retain `day-093-topic-01-metrics-scope.md` as an exit evidence artifact.",
                "accept": "Completed Metrics Scope architecture guide with validated bounded PodMonitoring configuration."
            }
        },
        {
            "key": "topic-02",
            "title": "Alerting policies",
            "preview": (
                "An SRE team configured a static CPU alert set to page on-call engineers when CPU exceeds 80% for 2 minutes, "
                "generating 420 midnight pages during scheduled batch backups while a real checkout outage went unnoticed for 3 hours."
            ),
            "overview": (
                "Traditional alerting based on static infrastructure thresholds (e.g., 'CPU > 80%' or 'Memory > 85%') is fundamentally broken: "
                "it generates high false-alarm rates, produces severe alert fatigue, and fails to detect real customer-impacting failures until "
                "users complain. Modern reliability engineering mandates **SLO-based alerting** using **Multi-Window Multi-Burn-Rate Policies**. "
                "Instead of measuring component utilization, multi-burn-rate alerting monitors the rate at which the user-facing **Error Budget** "
                "is being consumed. By pairing a **long lookback window** (which proves the failure is persistent) with a **short lookback window** "
                "(which proves the failure is actively occurring right now), multi-burn alerting delivers rapid detection during catastrophic outages "
                "while completely eliminating false-positive pages caused by brief transient spikes."
            ),
            "technical": (
                "### 1. Multi-Window Multi-Burn-Rate Mathematical Model\n"
                "- **Burn Rate Defined:** A burn rate of $1.0$ consumes exactly 100% of an error budget over the course of the SLO period (e.g. 30 days). "
                "If an SLO is 99.9%, the error budget is $0.1\\% = 0.001$. A burn rate of $1.0$ means the error rate is exactly $0.1\\%$.\n"
                "- **Burn Rate of 14.4 (P1 Alert):** Consumes 2% of the 30-day budget in only **1 hour**! Requires an immediate 24/7 page.\n"
                "- **The Dual-Window Rule (Google SRE Standard):** To fire an alert, *both* windows must exceed the threshold simultaneously:\n"
                "  1. **Long Window (e.g. 1 hour, burn rate > 14.4):** Proves that error budget consumption is statistically significant.\n"
                "  2. **Short Window (e.g. 5 minutes, burn rate > 14.4):** Proves that the system is *still failing right now*. If errors stop after 6 minutes, "
                "the short window clears instantly, resetting the alert and preventing the on-call engineer from being awakened for a resolved glitch.\n\n"
                "### 2. Multi-Burn Alerting Matrix (30-Day 99.9% SLO)\n"
                "- **Critical / PagerDuty Page:** Burn Rate = 14.4. Long Window = 1h, Short Window = 5m. Budget Consumed: 2% in 1 hour.\n"
                "- **Major / PagerDuty Page:** Burn Rate = 6.0. Long Window = 6h, Short Window = 30m. Budget Consumed: 5% in 6 hours.\n"
                "- **Moderate / Ticket:** Burn Rate = 1.0. Long Window = 3 days, Short Window = 6 hours. Budget Consumed: 10% in 3 days. Creates Jira ticket.\n\n"
                "### 3. Monitoring Query Language (MQL) Implementation\n"
                "- Cloud Monitoring evaluates burn rates natively using MQL:\n"
                "  Fetches `custom.googleapis.com/http/requests_total` with `status =~ '5..'`, divides by total requests, computes ratio, and "
                "evaluates against threshold over rolling sliding windows."
            ),
            "questions": [
                "Why does pairing a short lookback window with a long lookback window eliminate false-positive alert pages?",
                "What is the mathematical relationship between an availability SLO of 99.9% and a burn rate of 14.4?",
                "How does SLO-based alerting reduce alert fatigue compared to static component utilization thresholds?",
            ],
            "reference": "https://docs.cloud.google.com/monitoring/alerts",
            "reference_label": "Google Cloud Monitoring: Alerting policies, notification channels, and multi-burn-rate condition design",
            "scenario": {
                "symptom": (
                    "Brightloaf's on-call engineers received 1,280 PagerDuty alerts during a single month. Responders muted alerting channels, "
                    "causing a catastrophic 4-hour checkout outage to go completely unaddressed because the page was buried under hundreds "
                    "of non-critical disk-space and CPU-spike alerts."
                ),
                "constraints": (
                    "Must eliminate alert fatigue by reducing total monthly on-call pages to fewer than 10, while guaranteeing sub-5-minute detection of core checkout failures."
                ),
                "evidence": (
                    "Audit of the 1,280 alerts revealed that 94% were static threshold warnings (e.g. `Node CPU > 85% for 60s`). "
                    "In 98% of those incidents, customer transactions were completely unaffected and error rates remained below 0.01%."
                ),
                "diagnostic_steps": [
                    "Extract PagerDuty incident history for the last 90 days and group alerts by policy name and actionability.",
                    "Calculate the Signal-to-Noise Ratio (SNR): `SNR = Actionable Incidents / Total Alerts Paged`.",
                    "Review Cloud Monitoring alert policy definitions to identify static infrastructure monitors that lack user-impact correlation.",
                ],
                "root": (
                    "Flawed alerting philosophy: the team paged on internal component symptoms (CPU/RAM) rather than user-facing error budget consumption, "
                    "creating massive alert fatigue that blinded responders to genuine outages."
                ),
                "fix": (
                    "Decommission all static CPU/RAM pager alerts. Replace them with Google SRE standard dual-window multi-burn-rate alerting policies "
                    "tied directly to the 99.9% checkout availability SLO (1h/5m for P1, 6h/30m for P2). Route non-urgent trends to automated Jira tickets."
                ),
                "verify": (
                    "Simulate synthetic failure scenarios in pre-production: inject 2% error rate for 3 minutes (confirms zero page fired), "
                    "then inject 2% error rate for 12 minutes (confirms P1 page triggers at T+5m and resolves automatically when errors clear)."
                ),
                "residual": (
                    "Slow, low-grade error budget leaks (burn rate < 1.0) will take several days to alert via ticket, requiring weekly SLO review meetings."
                ),
                "diagram": (
                    "1,280 static CPU alerts page SREs",
                    "Alert fatigue: channels muted",
                    "4h checkout outage ignored",
                    "Dual-window multi-burn MQL deployed",
                    "P1 pages fire only on real budget loss"
                ),
                "facts": "1,280 alerts generated per month, 94% of which had zero impact on customer transactions, blinding engineers to real outages.",
                "inference": "Paging on infrastructure utilization inevitably causes alert fatigue; pages must be reserved for active SLO budget loss.",
                "expected": "Dual-window multi-burn alerting triggers pages only when significant error budget is actively burning in real time."
            },
            "lab": {
                "name": "Multi-Window Multi-Burn-Rate Alert Policy Implementation",
                "file": "day-093-topic-02-burn-rate-alert.md",
                "level": "Progressive: Beginner → Intermediate → Advanced",
                "goal": "Author and test a complete dual-window multi-burn-rate alerting policy using Monitoring Query Language (MQL).",
                "expected": "A production-grade JSON alert policy definition and a Python validation script calculating mathematical burn rate thresholds.",
                "mode": "tabletop analysis & policy synthesis",
                "prereq": "Understanding of SLOs, error budgets, and MQL syntax.",
                "preflight": "Review Google SRE Workbook Chapter 5 on Alerting on SLOs and Cloud Monitoring MQL reference.",
                "steps": [
                    "**Stage 1: Beginner (Baseline Discovery & Configuration Inspection)**\n- Query existing notification channels and verify notification target endpoints:\n\n```sh\ncat <<'EOF' > stage1-inspect-channels.sh\n# List configured notification channels (Slack, PagerDuty, Email)\ngcloud monitoring channels list \\\n    --format='table(name, type, displayName, enabled)'\nEOF\ncat stage1-inspect-channels.sh\n```",
                    "**Stage 2: Intermediate (Implementation, Deployment & Policy Enforcement)**\n- Construct the dual-window multi-burn-rate Alert Policy JSON specification:\n\n```sh\ncat <<'EOF' > stage2-deploy-burn-policy.json\n{\n  \"displayName\": \"SLO Burn Rate Exceeded: 14.4x (1h / 5m Window)\",\n  \"documentation\": {\n    \"content\": \"P1 Incident: Checkout error budget burning at 14.4x rate (2% consumed in 1 hour). Immediately triage checkout ingress.\",\n    \"mimeType\": \"text/markdown\"\n  },\n  \"combiner\": \"AND\",\n  \"conditions\": [\n    {\n      \"displayName\": \"Long Window: 1h Burn Rate > 14.4x\",\n      \"conditionMonitoringQueryLanguage\": {\n        \"duration\": \"0s\",\n        \"query\": \"fetch https_lb_rule\\n| filter (resource.url_map == 'brightloaf-lb')\\n| { metric 'loadbalancing.googleapis.com/https/request_count'\\n    | filter (metric.response_code_class == 500)\\n    | group_by sliding(1h), sum(val())\\n  ; metric 'loadbalancing.googleapis.com/https/request_count'\\n    | group_by sliding(1h), sum(val()) }\\n| ratio\\n| condition val() > (14.4 * 0.001)\"\n      }\n    },\n    {\n      \"displayName\": \"Short Window: 5m Burn Rate > 14.4x\",\n      \"conditionMonitoringQueryLanguage\": {\n        \"duration\": \"0s\",\n        \"query\": \"fetch https_lb_rule\\n| filter (resource.url_map == 'brightloaf-lb')\\n| { metric 'loadbalancing.googleapis.com/https/request_count'\\n    | filter (metric.response_code_class == 500)\\n    | group_by sliding(5m), sum(val())\\n  ; metric 'loadbalancing.googleapis.com/https/request_count'\\n    | group_by sliding(5m), sum(val()) }\\n| ratio\\n| condition val() > (14.4 * 0.001)\"\n      }\n    }\n  ],\n  \"alertStrategy\": {\n    \"autoClose\": \"1800s\"\n  }\n}\nEOF\ncat stage2-deploy-burn-policy.json\n```",
                    "**Stage 3: Advanced (Chaos Injection, Failure Rehearsal & Resilience Verification)**\n- Execute an automated Python simulation modeling transient spikes vs persistent outages against the dual-window policy:\n\n```sh\ncat <<'EOF' > stage3-simulate-burn.py\n# Mathematical verification of dual-window multi-burn alerting\ndef evaluate_burn_alert(error_rate_5m, error_rate_1h, threshold=0.0144):\n    short_window_fired = error_rate_5m > threshold\n    long_window_fired = error_rate_1h > threshold\n    alert_triggered = short_window_fired and long_window_fired\n    return alert_triggered, short_window_fired, long_window_fired\n\n# Scenario A: Brief 2-minute transient spike (3% error for 2m, then 0%)\nalert, short, long = evaluate_burn_alert(error_rate_5m=0.005, error_rate_1h=0.001)\nprint(f\"Scenario A (Brief Spike): Alert Triggered = {alert} (Short={short}, Long={long})\")\nassert not alert, \"FAIL: Transient spike should NOT fire dual-window alert!\"\n\n# Scenario B: Catastrophic active outage (2% error sustained for 15 minutes)\nalert, short, long = evaluate_burn_alert(error_rate_5m=0.020, error_rate_1h=0.018)\nprint(f\"Scenario B (Active Outage): Alert Triggered = {alert} (Short={short}, Long={long})\")\nassert alert, \"FAIL: Active outage MUST fire dual-window alert!\"\n\nprint(\"PASS: Dual-window multi-burn alerting logic mathematically validated.\")\nEOF\npython3 stage3-simulate-burn.py\n```",
                    "Review all output artifacts and confirm that the Python simulation proves transient spikes do not trigger on-call pages."
                ],
                "verification": (
                    "Alert policy JSON exists with valid MQL dual-window queries, and the mathematical simulation proves false-positive suppression."
                ),
                "trouble": "Ensure MQL query metric names match the exact resource type (`https_lb_rule` vs `gke_container`).",
                "cleanup": "Retain `day-093-topic-02-burn-rate-alert.md` as an exit evidence artifact.",
                "accept": "Completed multi-burn-rate alert policy with verified MQL queries and simulation proof."
            }
        },
        {
            "key": "topic-03",
            "title": "Uptime checks and synthetic monitoring",
            "preview": (
                "An internal routing change breaks public TLS certificate negotiation for mobile users in Tokyo, but internal monitoring reports "
                "100% green health because all health probes originate from servers inside the same US datacenter."
            ),
            "overview": (
                "Internal health checks and metric scrapers suffer from an inescapable architectural limitation: they observe applications from "
                "the *inside out*. If a public DNS Anycast routing fault, CDN edge SSL handshake failure, or regional Internet Service Provider "
                "(ISP) fiber cut prevents real external users from reaching the system, internal metrics will report 100% uptime because internal "
                "servers can reach each other over the local private network. To achieve true outside-in observability, architects deploy **Google Cloud "
                "Monitoring Uptime Checks** and **Synthetic Monitors**. Public Uptime Checks query public endpoints from multiple distinct geographical "
                "regions (Americas, Europe, Asia-Pacific) using Google's external edge stations, verifying DNS resolution, TLS certificate validity, "
                "HTTP response codes, and payload content matching. Furthermore, synthetic headless browser canaries execute realistic multi-step "
                "user workflows (such as logging in, searching a catalog, and adding items to a cart)."
            ),
            "technical": (
                "### 1. Global Public Uptime Check Architecture\n"
                "- **Multi-Region Anycast Probing:** Public uptime checks execute from multiple Google Cloud probe servers distributed across Europe, "
                "North America, South America, and Asia-Pacific. A service is declared unhealthy only when probes fail across multiple distinct regions "
                "simultaneously, preventing regional ISP glitches from causing false alarms.\n"
                "- **Validation Criteria:** Checks assert:\n"
                "  1. *HTTP Status Codes:* Response must be 200 OK (or expected 2xx/3xx).\n"
                "  2. *Latency Threshold:* Response time must complete within a strict SLA ceiling (e.g. < 1,500ms).\n"
                "  3. *Content Matchers:* Payload must contain expected JSON attributes (`{\"status\":\"HEALTHY\"}`) or regex patterns.\n\n"
                "### 2. Private Uptime Checks via Serverless VPC Access\n"
                "- When probing internal private IP endpoints within a VPC (e.g. internal microservices, private load balancers), public probe servers "
                "cannot reach private RFC 1918 subnets directly.\n"
                "- **Private Check Topology:** Configures Cloud Monitoring to route synthetic probe requests through a Serverless VPC Access connector "
                "or internal monitoring proxy, allowing end-to-end verification of internal ingress pipelines without exposing endpoints to the public internet.\n\n"
                "### 3. Synthetic Canary Monitors (Mocha / Puppeteer)\n"
                "- Traditional ping checks only test static endpoints. Synthetic monitors deploy a Node.js Puppeteer script hosted on Cloud Functions (2nd Gen).\n"
                "- The headless browser executes complete synthetic journeys: navigates to `https://store.brightloaf.com`, clicks 'Login', inputs "
                "test credentials, navigates to the shopping cart, and verifies the payment button renders. Captures DOM snapshots and network HAR logs "
                "on failure for instant debugging."
            ),
            "questions": [
                "Why will internal health checks fail to detect a regional TLS certificate negotiation failure affecting external clients?",
                "How does multi-region probe distribution prevent localized ISP routing anomalies from triggering false-positive uptime alerts?",
                "What architectural advantage do synthetic browser canaries provide over simple HTTP GET uptime pings?",
            ],
            "reference": "https://docs.cloud.google.com/monitoring/uptime-checks",
            "reference_label": "Google Cloud Monitoring: Uptime checks architecture, synthetic monitors, and private VPC verification",
            "scenario": {
                "symptom": (
                    "Following an edge CDN SSL certificate rotation, European mobile users were unable to load Brightloaf's checkout page for 80 minutes, "
                    "receiving `ERR_SSL_VERSION_OR_CIPHER_MISMATCH`. SRE dashboards remained green because internal monitoring agents inside the Iowa "
                    "datacenter queried backend VMs directly via internal HTTP."
                ),
                "constraints": (
                    "Must establish external, independent outside-in verification of public DNS, TLS handshakes, and page rendering from global client regions."
                ),
                "evidence": (
                    "CDN edge logs showed 45,000 SSL handshake failures terminating at European edge PoPs. Internal Kubernetes pods reported 0 errors "
                    "and 100% healthy HTTP 200 status on internal readiness probes."
                ),
                "diagnostic_steps": [
                    "Query the public checkout endpoint using `openssl s_client -connect checkout.brightloaf.com:443 -servername checkout.brightloaf.com` from external IPs.",
                    "Inspect Cloud CDN edge SSL certificate deployment status across regional edge caches.",
                    "Review Cloud Monitoring uptime check configurations to determine if multi-region external probing is enabled.",
                ],
                "root": (
                    "Monitoring architecture blind spot: observability was completely dependent on inside-out internal probes, lacking external "
                    "multi-region uptime checks capable of detecting edge CDN TLS misconfigurations."
                ),
                "fix": (
                    "Deploy Cloud Monitoring Public Uptime Checks configured across three global probe regions (Americas, Europe, Asia-Pacific). "
                    "Set probe frequency to 1 minute, enforce TLS certificate validation, assert response latency < 1,000ms, and configure content "
                    "matching on `\"status\":\"healthy\"`. Deploy a synthetic Puppeteer canary executing automated cart checkouts."
                ),
                "verify": (
                    "Simulate an edge TLS misconfiguration in staging; verify the European probe station detects the SSL handshake error within 60 seconds "
                    "and routes an emergency P1 page to the Edge Networking on-call rotation."
                ),
                "residual": (
                    "High-frequency global uptime probes generate continuous synthetic HTTP traffic against public endpoints that must be filtered from business analytics."
                ),
                "diagram": (
                    "Edge CDN SSL cert rotated incorrectly",
                    "European clients receive SSL errors",
                    "Internal dashboards show 100% green",
                    "Global Anycast Uptime Check deployed",
                    "Probe catches SSL error at T+60s"
                ),
                "facts": "45,000 users failed checkout for 80 minutes because internal probes never tested external CDN SSL termination.",
                "inference": "Internal metrics cannot verify external network reachability, DNS resolution, or TLS certificate validity.",
                "expected": "External Anycast uptime checks continuously validate edge TLS and page rendering from multiple global client locations."
            },
            "lab": {
                "name": "Global Multi-Region Uptime Check & Synthetic Canary Deployment",
                "file": "day-093-topic-03-uptime-checks.md",
                "level": "Progressive: Beginner → Intermediate → Advanced",
                "goal": "Author and deploy a multi-region Cloud Monitoring Uptime Check and a synthetic Puppeteer canary script.",
                "expected": "A comprehensive Markdown guide detailing gcloud uptime-check creation, synthetic function manifests, and validation scripts.",
                "mode": "tabletop analysis & canary synthesis",
                "prereq": "Understanding of HTTP/TLS protocols and headless browser testing.",
                "preflight": "Review Cloud Monitoring Uptime Check CLI commands and Cloud Functions 2nd Gen syntax.",
                "steps": [
                    "**Stage 1: Beginner (Baseline Discovery & Configuration Inspection)**\n- Query available probe regions and inspect existing uptime check configurations:\n\n```sh\ncat <<'EOF' > stage1-inspect-probes.sh\n# List all existing uptime checks in the project\ngcloud monitoring uptime list-configs \\\n    --format='table(name, displayName, monitoredResource.type)'\nEOF\ncat stage1-inspect-probes.sh\n```",
                    "**Stage 2: Intermediate (Implementation, Deployment & Policy Enforcement)**\n- Deploy a multi-region global uptime check asserting TLS validation, latency, and content matching:\n\n```sh\ncat <<'EOF' > stage2-deploy-uptime.sh\n# Create global public uptime check across 3 continents\ngcloud monitoring uptime create brightloaf-checkout-uptime \\\n    --display-name=\"Public Ingress Health: Checkout API\" \\\n    --hostname=\"api.brightloaf.com\" \\\n    --path=\"/healthz/shallow\" \\\n    --check-interval=1 \\\n    --timeout=5 \\\n    --protocol=HTTPS \\\n    --port=443 \\\n    --regions=EUROPE,USA,ASIA_PACIFIC \\\n    --content-match=\"HEALTHY\" \\\n    --matcher-type=CONTAINS_STRING\nEOF\ncat stage2-deploy-uptime.sh\n```",
                    "**Stage 3: Advanced (Chaos Injection, Failure Rehearsal & Resilience Verification)**\n- Author a synthetic Puppeteer browser canary script executing end-to-end checkout validation:\n\n```sh\ncat <<'EOF' > stage3-synthetic-canary.js\n// Puppeteer Synthetic Canary for Cloud Functions 2nd Gen\nconst puppeteer = require('puppeteer');\n\nasync function runCanary() {\n  const browser = await puppeteer.launch({ headless: 'new' });\n  const page = await browser.newPage();\n  \n  console.log('Step 1: Navigating to public storefront...');\n  const startTime = Date.now();\n  const response = await page.goto('https://store.brightloaf.com', { waitUntil: 'networkidle2', timeout: 10000 });\n  \n  console.log(`Step 2: Checking HTTP Status Code: ${response.status()}`);\n  if (response.status() !== 200) {\n    throw new Error(`Canary Failed: Expected 200, got ${response.status()}`);\n  }\n  \n  console.log('Step 3: Asserting presence of checkout button in DOM...');\n  await page.waitForSelector('#checkout-btn', { timeout: 3000 });\n  \n  const latency = Date.now() - startTime;\n  console.log(`Step 4: Synthetic Journey Succeeded in ${latency}ms`);\n  \n  await browser.close();\n}\n\nrunCanary().catch(err => {\n  console.error('CRITICAL SYNTHETIC FAILURE:', err.message);\n  process.exit(1);\n});\nEOF\ncat stage3-synthetic-canary.js\n```",
                    "Review all output artifacts and confirm that the uptime check verifies external global ingress across Europe, USA, and Asia-Pacific."
                ],
                "verification": (
                    "Configuration files exist, gcloud uptime commands define multi-region probe targets, and the synthetic canary script is fully articulated."
                ),
                "trouble": "Ensure target hostname has a valid, publicly trusted TLS certificate; self-signed certificates will cause uptime checks to fail.",
                "cleanup": "Retain `day-093-topic-03-uptime-checks.md` as an exit evidence artifact.",
                "accept": "Completed uptime check architecture guide with validated multi-region probe rules and synthetic canary script."
            }
        }
    ]
}
