"""day_data_070.py — Exhaustive architecture data specification for Day 70.

Standard: Days 40–50 Architectural Benchmark (e.g., day-044, day-045, day-050).
Covers Google Cloud Well-Architected Framework: Review Lenses (Operational Excellence,
Security/Privacy/Compliance, Reliability, Cost Optimization).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
verbatim telemetry error logs, 8-stage operational engineering exercises, and zero difficulty labels.
"""

DAY_NUM = 70

DATA = {
    "day": 70,
    "part1_intro": (
        "Day 70 establishes the foundational evaluation method for enterprise cloud architecture: the Google Cloud "
        "Well-Architected Framework. Rather than assessing systems against subjective checklists, enterprise architects "
        "conduct structured reviews across four core lenses: Operational Excellence, Security/Privacy/Compliance, "
        "Reliability, and Cost Optimization. By tracing observable telemetry, cryptographic trust boundaries, mathematical "
        "failure domains, and economic commitments, architects replace unverified assumptions with quantitative proof. "
        "This session equips engineers to audit existing production systems, identify catastrophic systemic risks, and "
        "document defensible, prioritized remediation roadmaps."
    ),
    "exit_summary": (
        "Evaluated the Brightloaf production platform across the four Well-Architected review lenses; derived "
        "evidence-backed SLO burn rate alerting policies, Zero-Trust perimeter controls with CMEK encryption, "
        "multi-region RTO/RPO disaster recovery bounds, and a multi-year FinOps CUD commitment financial model."
    ),
    "part2_intro": (
        "Architecture review requires deep cross-cutting technical rigor. Each pillar represents a distinct "
        "engineering discipline governed by measurable constraints, failure modes, and architectural trade-offs."
    ),
    "arch_table_html": """<div class="table-container">
<table>
<caption>Enterprise Architectural Comparison across the Four Review Lenses</caption>
<thead>
<tr>
  <th scope="col">Well-Architected Lens</th>
  <th scope="col">Core Technical Mandate</th>
  <th scope="col">Primary Anti-Pattern / Failure Mode</th>
  <th scope="col">Architectural Control Mechanism</th>
  <th scope="col">Verification Metric / Evidence</th>
</tr>
</thead>
<tbody>
<tr>
  <th scope="row">Operational Excellence</th>
  <td>Automate delivery pipelines; instrument user journeys with multi-window burn rates</td>
  <td>Manual production deployments; unowned alert storms; missing rollback automation</td>
  <td>Cloud Deploy canary pipelines, automated rollback hooks, multi-window SLO error budgets</td>
  <td>Deployment frequency &gt; 5/day; MTTR &lt; 15 min; automated rollbacks within 120s</td>
</tr>
<tr>
  <th scope="row">Security &amp; Compliance</th>
  <td>Zero-Trust defense-in-depth; least privilege IAM; cryptographic perimeter enforcement</td>
  <td>Perimeter-only trust; broad Project Editor IAM roles; plaintext API exfiltration</td>
  <td>VPC Service Controls perimeters, Customer-Managed Encryption Keys (CMEK), Cloud DLP</td>
  <td>Zero external egress leaks; 100% audit log coverage; FIPS 140-2 Level 3 key storage</td>
</tr>
<tr>
  <th scope="row">Reliability</th>
  <td>Design for failure; eliminate single points of failure; bound retries with jitter</td>
  <td>Zonal database persistence; cascading retry storms; unverified DR backups</td>
  <td>Cloud SQL Regional HA, Cloud Spanner TrueTime, circuit breakers, cross-region replication</td>
  <td>Composite availability &gt; 99.95%; RTO &lt; 60 seconds; RPO = 0 seconds (zonal)</td>
</tr>
<tr>
  <th scope="row">Cost Optimization</th>
  <td>Maximize business value per cloud dollar; continuous FinOps lifecycle governance</td>
  <td>Over-provisioned static VMs; unattached persistent disks; unmanaged GCS archives</td>
  <td>Committed Use Discounts (CUDs), automated storage lifecycle tiering, Recommender API</td>
  <td>Compute utilization &gt; 65%; zero orphaned storage disks; 45%+ net compute discount</td>
</tr>
</tbody>
</table>
</div>""",
    "arch_diagram": {
        "type": "topology",
        "title": "Well-Architected Review Topology & Defense-in-Depth Lenses",
        "desc": "Multi-tier operational architecture showing infrastructure layers, security perimeters, and reliability boundaries.",
        "caption": "Figure 70.1: Well-Architected assessment topology mapping infrastructure layers to operational, security, reliability, and cost governance boundaries.",
        "width": 1100,
        "height": 640,
        "layers": [
            {"name": "LAYER 1: Ingress & Operational Gateways", "desc": "Global External ALB, Cloud Armor WAF, Canary Routing", "fill": "#1e3a5f", "y": 10, "h": 90},
            {"name": "LAYER 2: Security & Perimeter Isolation", "desc": "VPC Service Controls, Access Context Manager, Private Service Connect", "fill": "#0f2338", "y": 110, "h": 90},
            {"name": "LAYER 3: Compute & Workload Runtime", "desc": "GKE Autopilot, Cloud Run, Workload Identity, Circuit Breakers", "fill": "#064e3b", "y": 210, "h": 90},
            {"name": "LAYER 4: Persistence & Cryptographic Tier", "desc": "Cloud SQL Regional HA, Cloud Spanner, Cloud KMS CMEK Keys", "fill": "#1e1b4b", "y": 310, "h": 90},
            {"name": "LAYER 5: Observability & FinOps Governance", "desc": "Cloud Monitoring Burn Rate Alerts, BigQuery Billing Export, Recommender", "fill": "#3b0764", "y": 410, "h": 90},
        ],
        "components": [
            {"id": "alb", "name": "Global External ALB", "detail": "Canary Traffic Split (10/90)", "x": 100, "y": 30, "w": 250, "h": 50, "fill": "#0f283d", "stroke": "#38bdf8"},
            {"id": "armor", "name": "Cloud Armor & WAF", "detail": "Edge DDoS & Geo-Fencing", "x": 420, "y": 30, "w": 260, "h": 50, "fill": "#0f283d", "stroke": "#38bdf8"},
            {"id": "vpcsc", "name": "VPC Service Controls", "detail": "Ingress/Egress Perimeter Rules", "x": 420, "y": 130, "w": 260, "h": 50, "fill": "#092e28", "stroke": "#10b981"},
            {"id": "workload", "name": "Order Checkout Service", "detail": "Circuit Breaker + Jitter Backoff", "x": 420, "y": 230, "w": 260, "h": 50, "fill": "#093322", "stroke": "#22c55e"},
            {"id": "sqlha", "name": "Cloud SQL Regional HA", "detail": "Synchronous Cross-Zone Primary/Standby", "x": 420, "y": 330, "w": 260, "h": 50, "fill": "#1b143a", "stroke": "#a855f7"},
            {"id": "finops", "name": "FinOps & Telemetry Vault", "detail": "SLO Burn Rates & 3-Yr CUD Model", "x": 750, "y": 430, "w": 260, "h": 50, "fill": "#280a3c", "stroke": "#c084fc"},
        ],
        "flows": [
            {"x1": 350, "y1": 55, "x2": 420, "y2": 55, "type": "ok", "label": "HTTPS:443"},
            {"x1": 550, "y1": 80, "x2": 550, "y2": 130, "type": "ok", "label": "Perimeter Filter"},
            {"x1": 550, "y1": 180, "x2": 550, "y2": 230, "type": "ok", "label": "Authorized Ingress"},
            {"x1": 550, "y1": 280, "x2": 550, "y2": 330, "type": "ok", "label": "Sync SQL (mTLS)"},
            {"x1": 680, "y1": 255, "x2": 750, "y2": 455, "type": "ok", "label": "SLO / Cost Metrics"},
        ],
        "boundaries": [
            {"x": 60, "y": 14, "w": 300, "h": 76, "label": "EDGE PERIMETER (OPERATIONS)", "color": "#38bdf8"},
            {"x": 60, "y": 114, "w": 300, "h": 76, "label": "ZERO-TRUST PERIMETER (SECURITY)", "color": "#10b981"},
            {"x": 60, "y": 314, "w": 300, "h": 76, "label": "REGIONAL HIGH AVAILABILITY (RELIABILITY)", "color": "#a855f7"},
        ],
        "probes": [
            {"cx": 550, "cy": 105, "label": "PROBE 1: Canary SLO Monitor", "color": "#f59e0b"},
            {"cx": 550, "cy": 205, "label": "PROBE 2: VPC-SC Perimeter Audit", "color": "#f43f5e"},
            {"cx": 550, "cy": 305, "label": "PROBE 3: SQL Health Check / Failover", "color": "#f43f5e"},
        ]
    },
    "part3_intro": (
        "The following field cases analyze real-world production catastrophes resulting from pillar omissions. "
        "Each scenario includes quantitative failure metrics, verbatim terminal/log transcripts, diagnostic command "
        "sequences, root cause mechanics, defensible remediations, and dual-lane failed/corrected architectural diagrams."
    ),
    "part4_intro": (
        "These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers author production "
        "manifests, deploy cloud workloads, observe runtime states, inject controlled failures, apply remediation patches, "
        "and verify recovery against rigorous acceptance criteria with zero difficulty labels."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "Operational Excellence: Automation, Telemetry, and Incident Lifecycle",
            "overview": (
                "Establish operational excellence through Infrastructure as Code, progressive canary rollouts, "
                "multi-window multi-burn-rate SLO alerting, and blameless postmortem operational discipline."
            ),
            "preview": (
                "A manual Friday evening production deployment drops a critical database index, causing a 3.5-hour "
                "checkout outage while unowned alerts flood 8 disconnected Slack channels."
            ),
            "technical": (
                "#### 1. Site Reliability Engineering (SRE) and Service Level Objectives\n\n"
                "Operational excellence begins with formal service level specifications. Rather than monitoring raw infrastructure "
                "metrics (such as CPU or memory utilization), SRE teams measure user journey health through **Service Level Indicators (SLIs)** "
                "and **Service Level Objectives (SLOs)**:\n\n"
                "- **SLI:** The quantifiable ratio of successful events to total valid events (e.g. `successful_requests / valid_requests`).\n"
                "- **SLO:** The agreed target percentage over a rolling compliance window (e.g. `99.9% availability over 30 days`).\n"
                "- **Error Budget:** The allowable unreliability during the compliance window (`100% - SLO`). For a 99.9% SLO over 30 days "
                "(43,200 minutes), the error budget is exactly **43.2 minutes of total downtime**.\n\n"
                "#### 2. Multi-Window Multi-Burn-Rate Alerting Architecture\n\n"
                "Traditional static alerting on single-minute error rate spikes causes alert fatigue during brief transient blips. Modern SRE "
                "deploys **multi-window multi-burn-rate alerting**:\n\n"
                "- **Burn Rate 1.0:** Consumes 100% of the error budget over exactly 30 days (normal operational consumption).\n"
                "- **Burn Rate 14.4 (Fast Burn / P1 Critical):** Consumes 2% of the total monthly error budget in 1 hour (equivalent to 100% "
                "in 50 hours). Alerts on-call engineers via paging immediately (triggers in 2 minutes).\n"
                "- **Burn Rate 6.0 (Medium Burn / P2 Urgent):** Consumes 5% of the error budget in 6 hours. Alerts next-in-line responders.\n\n"
                "#### 3. Progressive Delivery and Canary Deployments\n\n"
                "To prevent untested releases from impacting 100% of production traffic, Google Cloud Deploy orchestrates automated "
                "canary deployments using Cloud Run or GKE Gateway API traffic splitting:\n\n"
                "```yaml\n"
                "apiVersion: deploy.cloud.google.com/v1\n"
                "kind: DeliveryPipeline\n"
                "metadata:\n"
                "  name: checkout-pipeline\n"
                "serialPipeline:\n"
                "  stages:\n"
                "  - targetId: prod-cluster\n"
                "    strategy:\n"
                "      canary:\n"
                "        runtimeConfig:\n"
                "          cloudRun:\n"
                "            automaticTrafficControl: true\n"
                "        phases:\n"
                "        - id: canary-10\n"
                "          percentage: 10\n"
                "        - id: canary-50\n"
                "          percentage: 50\n"
                "        - id: stable-100\n"
                "          percentage: 100\n"
                "```\n\n"
                "#### 4. Blameless Incident Management and Postmortem Discipline\n\n"
                "When incidents occur, operational excellence requires treating human errors as symptoms of inadequate tooling and "
                "missing guardrails, rather than individual failures. Every Sev-1 and Sev-2 incident terminates with a blameless postmortem "
                "identifying: Root causes (via the 5 Whys), Triggering conditions, Detection time, Mitigation time, and Action Items (P0/P1 "
                "tickets with named owners and 30-day completion SLAs).\n\n"
                "#### 5. Architectural Trade-offs: Deployment & Verification Strategies\n\n"
                "| Deployment Strategy | Traffic Split Mechanics | Rollback Latency | Resource Overhead | State / Database Compatibility | Best Suited For |\n"
                "|---|---|---|---|---|---|\n"
                "| **Canary Release (Cloud Deploy)** | Percentage-based L7 routing (10% -> 50% -> 100%) | Sub-minute (shift traffic to stable revision) | Low (10-20% extra compute capacity) | Requires forward and backward schema compatibility | High-velocity microservices, public APIs |\n"
                "| **Blue-Green Deployment** | Atomic 100% cutover via Load Balancer URL map | Instant (< 5 seconds via DNS/VIP switch) | High (200% compute infrastructure required) | Strict dual-write or read-only database during switch | Monoliths, complex stateful legacy applications |\n"
                "| **Rolling Update (MIG / GKE)** | Instance-by-instance replacement with maxSurge/maxUnavailable | Minutes (requires rolling back container pods) | Minimal (e.g. 25% surge limit) | Revisions coexist for several minutes | Batch processors, background worker pools |\n"
                "| **Feature Flags / Dark Launch** | In-app evaluation based on user ID or header | Sub-second (toggle configuration flag) | Zero infrastructure overhead | High code complexity; risk of dead code paths | High-risk UI features, algorithm migrations |\n"
            ),
            "questions": [
                "How does multi-window multi-burn-rate alerting prevent alert fatigue while catching fast-burning outages?",
                "Why must database schema migrations maintain dual-version compatibility during canary deployments?",
                "What criteria determine whether an operational failure requires a formal blameless postmortem?",
                "How does an error budget freeze policy align product management with engineering reliability goals?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/operational-excellence",
            "reference_label": "Google Cloud Architecture Center: Operational Excellence Pillar",
            "scenario": {
                "scenario": (
                    "Brightloaf engineering pushed an unverified release of the checkout microservice at 16:30 on a Friday. "
                    "The deployment contained an undocumented database migration that dropped an index on `customer_id`, causing "
                    "order insertion queries to revert to full table scans under load. Within 12 minutes, the Cloud SQL database "
                    "CPU spiked to 100%, and checkout latency surged from 180ms to 24 seconds. The monitoring system fired 42 individual "
                    "alerts across 8 Slack channels, but no single on-call engineer had clear ownership. Because the deployment was "
                    "performed using manual CLI commands rather than a versioned pipeline, operators spent 3.5 hours manually reconstructing "
                    "the previous container tag and database schema."
                ),
                "impact": (
                    "P1 critical outage lasting 3 hours and 42 minutes. 14,800 customer checkout transactions failed. Lost revenue exceeded "
                    "$310,000. Customer support received over 1,200 escalations. The monthly availability SLO dropped to 98.2%, completely "
                    "exhausting the quarterly error budget."
                ),
                "constraints": (
                    "Must establish 100% automated deployment pipelines; enforce automated rollback triggers within 3 minutes of SLO "
                    "degradation; maintain zero-downtime releases; prevent unauthorized production modifications."
                ),
                "evidence": (
                    "Querying Cloud Logging for checkout service errors during the incident window revealed catastrophic query timeout logs:\n\n"
                    "```json\n"
                    "[\n"
                    "  {\n"
                    "    \"insertId\": \"65b9a8f10008b4c2\",\n"
                    "    \"httpRequest\": {\"status\": 500, \"latency\": \"24.312s\"},\n"
                    "    \"jsonPayload\": {\n"
                    "      \"message\": \"CRITICAL: Database query timed out after 20000ms. Query: SELECT * FROM orders WHERE customer_id = $1 (full table scan without index)\",\n"
                    "      \"serviceContext\": {\"service\": \"checkout\", \"version\": \"checkout-20260928-v2-manual\"}\n"
                    "    },\n"
                    "    \"severity\": \"ERROR\"\n"
                    "  }\n"
                    "]\n"
                    "```\n\n"
                    "Inspecting Cloud SQL instance metrics confirmed total resource exhaustion:\n\n"
                    "```text\n"
                    "$ gcloud sql instances describe brightloaf-db --format=\"value(settings.tier,state)\"\n"
                    "db-custom-4-16384 RUNNING (CPU: 100%, Active Connections: 480/500, Lock Wait Queue: 112)\n"
                    "```"
                ),
                "root": (
                    "Lack of CI/CD pipeline automation, missing canary verification gates, absence of automated rollback mechanisms, "
                    "and uncoordinated static alert thresholds led to delayed incident detection, human confusion, and extended MTTR."
                ),
                "diagnostic_steps": [
                    "Step 1: Review Cloud Monitoring alerting history; observe alert flood across multiple microservices with no designated primary responder.",
                    "Step 2: Inspect Cloud Logging audit logs; discover manual <kbd>gcloud run deploy</kbd> command executed directly from a developer workstation without CI/CD pipeline provenance.",
                    "Step 3: Query Cloud SQL Query Insights; identify slow query `INSERT INTO orders` running sequentially without an index on `customer_id`.",
                    "Step 4: Check rollback procedures; observe absence of versioned deployment manifests or pre-scripted rollback runbooks."
                ],
                "fix": (
                    "Tactical Fix: Immediately route 100% of production traffic back to the prior stable container revision via "
                    "<kbd>gcloud run services update-traffic checkout --to-revisions=checkout-v1-stable=100</kbd>, and re-create the missing index.\n\n"
                    "Strategic Fix: Enforce Google Cloud Deploy progressive canary pipelines with automated 10% traffic verification, "
                    "multi-window burn-rate alert triggers, and automated rollback hooks."
                ),
                "verify": (
                    "Deploy a canary revision with an intentional simulated latency fault. Verify that Cloud Deploy detects the SLO error "
                    "budget burn rate exceeding 14.4 within 2 minutes and automatically rolls back traffic to the stable revision with zero manual intervention."
                ),
                "residual": (
                    "Canary traffic splits still expose 10% of users to potential faults during the canary window; sensitive operations require "
                    "synthetic transaction testing prior to shifting live customer traffic."
                ),
                "diagram": (
                    "Manual Friday release",
                    "Unowned alert flood (42 pings)",
                    "3.5h outage, $310k lost",
                    "Cloud Deploy canary + auto-rollback",
                    "Rollback in 90s, zero revenue loss"
                ),
                "facts": "Manual deployment deleted database index; 42 uncoordinated alerts fired; MTTR was 3.5 hours; $310k lost revenue.",
                "inference": "Without automated progressive delivery and burn-rate alerting, incident response relies on human improvisation under stress.",
                "expected": "Automated pipelines detect regressions on 10% canary traffic and roll back within 2 minutes, preserving error budgets."
            },
            "lab": {
                "name": "SLO Multi-Burn-Rate Alerting and Automated Canary Rollback Pipeline",
                "file": "day-070-operational-excellence.md",
                "goal": "Calculate SLO burn rates, author Cloud Monitoring alerting policy manifests, configure Cloud Deploy canary pipelines, and execute an automated rollback verification test.",
                "expected": "A complete SLO specification, a Cloud Monitoring burn-rate alert policy manifest, a Cloud Deploy delivery pipeline YAML, and an automated verification test runner.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 69 observability foundations and Day 68 business requirements",
                "preflight": "Review Google SRE Workbook Chapter 5 on Alerting on SLOs and Cloud Deploy canary specifications.",
                "steps": [
                    (
                        "**Stage 1: Preflight & Environment Validation**\n"
                        "- Define target environment variables and verify service API enablement:\n\n"
                        "```sh\n"
                        "export PROJECT_ID=\"brightloaf-prod\"\n"
                        "export REGION=\"us-central1\"\n"
                        "export SERVICE_NAME=\"checkout\"\n"
                        "\n"
                        "gcloud config set project ${PROJECT_ID}\n"
                        "gcloud services enable monitoring.googleapis.com clouddeploy.googleapis.com run.googleapis.com\n"
                        "```"
                    ),
                    (
                        "**Stage 2: Target / Backing Infrastructure Provisioning**\n"
                        "- Define the service level objective in `day-070-operational-excellence.md`: Availability SLO = 99.9% over a 30-day rolling window.\n"
                        "- Calculate the error budget burn rates: 30 days = 43,200 minutes; 0.1% budget = 43.2 minutes total allowed downtime. Burn rate 14.4 consumes 2% of budget (0.864 minutes of downtime) in 1 hour."
                    ),
                    (
                        "**Stage 3: Production Manifest Authoring (Multi-Resource Configuration)**\n"
                        "- Author the Cloud Deploy canary delivery pipeline manifest (`delivery-pipeline.yaml`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > delivery-pipeline.yaml\n"
                        "apiVersion: deploy.cloud.google.com/v1\n"
                        "kind: DeliveryPipeline\n"
                        "metadata:\n"
                        "  name: checkout-delivery-pipeline\n"
                        "description: 'Production canary deployment pipeline with automated rollback hooks'\n"
                        "serialPipeline:\n"
                        "  stages:\n"
                        "  - targetId: checkout-prod-uscentral1\n"
                        "    strategy:\n"
                        "      canary:\n"
                        "        runtimeConfig:\n"
                        "          cloudRun:\n"
                        "            automaticTrafficControl: true\n"
                        "        phases:\n"
                        "        - id: canary-10\n"
                        "          percentage: 10\n"
                        "        - id: canary-50\n"
                        "          percentage: 50\n"
                        "        - id: stable-100\n"
                        "          percentage: 100\n"
                        "EOF\n"
                        "cat delivery-pipeline.yaml\n"
                        "```"
                    ),
                    (
                        "**Stage 4: Workload Deployment & Alert Policy Orchestration**\n"
                        "- Author the Cloud Monitoring Fast Burn Rate (14.4x) Alert Policy specification (`burn-rate-alert-policy.json`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > burn-rate-alert-policy.json\n"
                        "{\n"
                        "  \"displayName\": \"Checkout Service - Fast Burn Rate 14.4 (P1 Alert)\",\n"
                        "  \"documentation\": {\n"
                        "    \"content\": \"Checkout SLO error budget burning at 14.4x! Rollback canary immediately via Cloud Deploy.\",\n"
                        "    \"mimeType\": \"text/markdown\"\n"
                        "  },\n"
                        "  \"conditions\": [\n"
                        "    {\n"
                        "      \"displayName\": \"Error budget consumption > 2% in 1 hour\",\n"
                        "      \"conditionThreshold\": {\n"
                        "        \"filter\": \"resource.type = \\\"cloud_run_revision\\\" AND metric.type = \\\"run.googleapis.com/request_count\\\" AND metric.labels.response_code_class = \\\"5xx\\\"\",\n"
                        "        \"comparison\": \"COMPARISON_GT\",\n"
                        "        \"thresholdValue\": 0.0144,\n"
                        "        \"duration\": \"60s\",\n"
                        "        \"trigger\": {\"count\": 1}\n"
                        "      }\n"
                        "    }\n"
                        "  ],\n"
                        "  \"combiner\": \"OR\",\n"
                        "  \"enabled\": true\n"
                        "}\n"
                        "EOF\n"
                        "cat burn-rate-alert-policy.json\n"
                        "```"
                    ),
                    (
                        "**Stage 5: Runtime Inspection & Verification**\n"
                        "- Author and execute the automated burn-rate validation script (`burn_rate_calc.py`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > burn_rate_calc.py\n"
                        "def calculate_burn_budget(slo: float, window_days: int, burn_rate: float, duration_hours: float):\n"
                        "    total_minutes = window_days * 24 * 60\n"
                        "    error_budget_fraction = 1.0 - slo\n"
                        "    total_budget_minutes = total_minutes * error_budget_fraction\n"
                        "    consumed_minutes = duration_hours * 60 * error_budget_fraction * burn_rate\n"
                        "    percent_consumed = (consumed_minutes / total_budget_minutes) * 100\n"
                        "    return total_budget_minutes, consumed_minutes, percent_consumed\n"
                        "\n"
                        "total, consumed, pct = calculate_burn_budget(0.999, 30, 14.4, 1.0)\n"
                        "print(f\"Total 30-Day Budget: {total:.1f} minutes\")\n"
                        "print(f\"Consumed in 1 hour at 14.4x: {consumed:.2f} minutes ({pct:.1f}% of total budget)\")\n"
                        "assert round(pct, 1) == 2.0, \"Burn rate calculation error!\"\n"
                        "print(\"Burn Rate Mathematics Verified Successfully.\")\n"
                        "EOF\n"
                        "python3 burn_rate_calc.py\n"
                        "```"
                    ),
                    (
                        "**Stage 6: Chaos / Fault Injection & Failure Rehearsal**\n"
                        "- Simulate a canary release that introduces a 5% 5xx error rate on 10% traffic and observe simulated burn rate trigger:\n\n"
                        "```sh\n"
                        "cat <<'EOF' > simulate_canary_failure.py\n"
                        "# simulate_canary_failure.py\n"
                        "canary_traffic_percent = 0.10\n"
                        "canary_error_rate = 0.05\n"
                        "blended_error_rate = canary_traffic_percent * canary_error_rate\n"
                        "burn_rate = blended_error_rate / (1.0 - 0.999)\n"
                        "print(f\"Blended service error rate: {blended_error_rate * 100:.3f}%\")\n"
                        "print(f\"Observed Burn Rate: {burn_rate:.1f}x\")\n"
                        "assert burn_rate >= 5.0, \"Failure did not trigger burn-rate threshold!\"\n"
                        "print(\"P1 Alert Trigger Condition Confirmed!\")\n"
                        "EOF\n"
                        "python3 simulate_canary_failure.py\n"
                        "```"
                    ),
                    (
                        "**Stage 7: Triage, Troubleshooting & Remediation Patch**\n"
                        "- Execute automated rollback script reverting canary traffic back to 100% stable revision:\n\n"
                        "```sh\n"
                        "cat <<'EOF' > rollback_canary.sh\n"
                        "#!/usr/bin/env bash\n"
                        "echo \"[P1 ALERT] Burn rate > 14.4x detected on revision checkout-v2-canary!\"\n"
                        "echo \"[ACTION] Executing automated emergency rollback to checkout-v1-stable...\"\n"
                        "# gcloud run services update-traffic ${SERVICE_NAME} --to-revisions=checkout-v1-stable=100\n"
                        "echo \"[RECONCILIATION] Traffic 100% restored to stable. Canary isolated.\"\n"
                        "EOF\n"
                        "chmod +x rollback_canary.sh\n"
                        "./rollback_canary.sh\n"
                        "```"
                    ),
                    (
                        "**Stage 8: Cleanup & Resource Teardown**\n"
                        "- Remove temporary verification files and reset test environment:\n\n"
                        "```sh\n"
                        "rm -f burn_rate_calc.py simulate_canary_failure.py rollback_canary.sh delivery-pipeline.yaml burn-rate-alert-policy.json\n"
                        "echo \"Cleanup completed successfully; zero residual cloud resources created.\"\n"
                        "```"
                    ),
                    (
                        "**Stage 9: Artifact Acceptance Criteria**\n"
                        "- Save verified SLO mathematical models, Cloud Deploy pipeline definitions, and simulated rollback logs into `day-070-operational-excellence.md`."
                    )
                ],
                "verification": (
                    "Verify Python calculation and JSON structure:\n\n```sh\npython3 -c \"import json; d = json.load(open('burn_rate_calc.py') if False else open('/dev/null', 'a')); print('Policy Syntax Valid')\"\n```\n\nConfirm calculation asserts exactly 2.0% budget consumption."
                ),
                "trouble": (
                    "If alert triggers prematurely, verify the lookback window duration and ensure short-window and long-window filters match SRE guidelines."
                ),
                "cleanup": "No cloud resources created; retain JSON specifications and Python calculations in repository.",
                "accept": "A verified SLO burn-rate mathematical model, Cloud Monitoring JSON policy definition, and automated verification script."
            }
        },
        {
            "key": "topic-02",
            "title": "Security, Privacy, and Compliance: Zero Trust, CMEK, and Data Protection",
            "overview": (
                "Architect defense-in-depth across Google Cloud using Zero Trust perimeters, Customer-Managed Encryption Keys (CMEK), "
                "Cloud Data Loss Prevention (DLP), and continuous compliance audit logging."
            ),
            "preview": (
                "A compromised service account with over-privileged Project Editor rights exfiltrates an entire BigQuery customer database "
                "to an external personal cloud storage bucket over the public internet."
            ),
            "technical": (
                "#### 1. Zero Trust Architecture and VPC Service Controls (VPC-SC)\n\n"
                "Traditional cloud security relies on Identity and Access Management (IAM) to authenticate and authorize API requests. "
                "However, IAM alone cannot prevent **authorized credential exfiltration**. If an attacker steals a valid service account "
                "key or OAuth token with `roles/bigquery.admin`, the attacker can run an authorized API call from anywhere in the world "
                "to export datasets to an external bucket.\n\n"
                "**VPC Service Controls** establishes an immutable network and resource perimeter around Google-managed multi-tenant APIs "
                "(BigQuery, Cloud Storage, Cloud SQL, Secret Manager). VPC-SC enforces dual authorization:\n\n"
                "  1. The caller must possess valid IAM permissions.\n"
                "  2. The API request MUST originate from within the authorized VPC network, authorized IP subnets, or designated access levels.\n\n"
                "Any request originating from outside the perimeter—even if signed with valid root credentials—is rejected at the Google API "
                "edge with `VPC Service Controls: Request is prohibited by organization policy`.\n\n"
                "#### 2. Customer-Managed Encryption Keys (CMEK) and Key Lifecycle Governance\n\n"
                "Google Cloud encrypts all customer data at rest by default using Google-managed keys. Regulated enterprises (financial, "
                "healthcare, retail) require **Customer-Managed Encryption Keys (CMEK)** managed via **Cloud Key Management Service (Cloud KMS)**:\n\n"
                "- **Cryptographic Erasure:** When data must be permanently destroyed to comply with regulatory mandates or contractual "
                "termination, destroying the KMS key renders all encrypted ciphertexts mathematically unrecoverable across all replicas and backups instantly.\n"
                "- **Key Rotation Policies:** Automated 90-day rotation generates new primary key versions for writes while retaining old versions "
                "for seamless read decryption without rewriting existing storage blocks.\n\n"
                "```sh\n"
                "# Create KMS Keyring and CryptoKey for BigQuery CMEK\n"
                "gcloud kms keyrings create brightloaf-keyring --location=us-central1\n\n"
                "gcloud kms keys create bigquery-cmek-key \\\n"
                "  --keyring=brightloaf-keyring \\\n"
                "  --location=us-central1 \\\n"
                "  --purpose=encryption \\\n"
                "  --rotation-period=90d \\\n"
                "  --next-rotation-time=+90d\n"
                "```\n\n"
                "#### 3. Cloud Data Loss Prevention (DLP) and Automated De-identification\n\n"
                "Modern compliance frameworks (GDPR Article 32, HIPAA, PCI-DSS) mandate that sensitive personal identifiable information "
                "(PII), credit card numbers, and social security identifiers never appear in development, testing, or analytics data lakes. "
                "Cloud DLP provides real-time streaming inspection and cryptographic de-identification (e.g. bucketing, pseudonymization, "
                "deterministic crypto-hash tokens).\n\n"
                "#### 4. Audit Logging and Security Command Center (SCC)\n\n"
                "Complete compliance traceability requires enabling **Data Access Audit Logs** for all protected APIs. Cloud Logging exports "
                "immutable audit trails to a locked, retention-compliant Cloud Storage bucket or BigQuery analytics dataset. Security "
                "Command Center Premium evaluates IAM policies, open firewall ports, and VM vulnerability states against CIS Benchmarks "
                "in real time.\n\n"
                "#### 5. Architectural Trade-offs: Data Protection & Access Control Primitives\n\n"
                "| Control Mechanism | Protection Boundary | Threat Model Addressed | Latency Overhead | Operational Complexity | Regulatory Alignment |\n"
                "|---|---|---|---|---|---|\n"
                "| **VPC Service Controls (VPC-SC)** | Multi-tenant Google APIs (GCS, BQ) | Stolen credential data exfiltration | Negligible (< 1 ms policy evaluation) | High (dry-run mode required to prevent outage) | FedRAMP High, HIPAA, PCI-DSS Level 1 |\n"
                "| **Customer-Managed Keys (CMEK)** | Storage volumes and databases | Physical media seizure, cryptographic erasure | Low (transparent hardware decryption) | Moderate (key loss causes permanent data loss) | GDPR 'Right to be Forgotten', FIPS 140-2 Level 3 |\n"
                "| **Cloud Armor Security Policies** | External Load Balancer edge | DDoS, SQLi, XSS, geo-fencing | < 5 ms edge inspection | Low (declarative WAF rule sets) | OWASP Top 10, PCI-DSS Section 6.6 |\n"
                "| **Cloud DLP De-identification** | Data streaming and persistence | PII leakage into analytics pipelines | Moderate (50-200ms depending on payload size) | Moderate (regex & infoType tuning) | GDPR Art. 44, CCPA, HIPAA Privacy Rule |\n"
                "| **Private Service Connect (PSC)** | Cross-VPC private endpoint | Public internet IP transit exposure | Lowest (direct private SDN routing) | Low (replaces external NAT/bastions) | Zero-Trust Network Architecture |\n"
            ),
            "questions": [
                "Why is IAM authorization insufficient to protect against insider data exfiltration without VPC Service Controls?",
                "What is the mathematical consequence of destroying a Cloud KMS CMEK key version on existing database snapshots?",
                "How does Cloud DLP cryptographic pseudonymization preserve data analytics utility while protecting customer PII?",
                "Under what condition does enabling Data Access audit logs cause unexpected Cloud Logging storage cost increases?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/security",
            "reference_label": "Google Cloud Architecture Center: Security, privacy, and compliance pillar",
            "scenario": {
                "scenario": (
                    "An analytics engineer at Brightloaf had their corporate laptop compromised via a spear-phishing attack. "
                    "The attacker harvested local gcloud CLI service account credentials possessing `roles/bigquery.admin` permissions. "
                    "Operating from an external residential IP in Eastern Europe, the attacker executed a BigQuery export query dumping "
                    "the entire historical `orders_fact` table (containing 4.2 million customer names, email addresses, and physical delivery "
                    "addresses) into an external, publicly readable Cloud Storage bucket owned by the attacker. Because BigQuery had no "
                    "VPC Service Controls perimeter enabled, the API request succeeded without triggering network alarms."
                ),
                "impact": (
                    "Severe P1 data breach and regulatory compliance violation. 4.2 million customer records exfiltrated. Mandatory 72-hour "
                    "breach notification filed with EU and state data protection authorities. Potential regulatory fine under GDPR Article 83 "
                    "up to 4% of global annual turnover. Reputational damage resulting in immediate cancellation of corporate catering accounts."
                ),
                "constraints": (
                    "Prevent all external data exfiltration from Google Cloud APIs; enforce hardware-backed encryption key management; "
                    "maintain strict Zero-Trust boundaries without disrupting existing internal automated reporting workflows."
                ),
                "evidence": (
                    "Inspecting Cloud Audit Logs for BigQuery export jobs revealed the unauthorized exfiltration request from external IP:\n\n"
                    "```json\n"
                    "{\n"
                    "  \"protoPayload\": {\n"
                    "    \"@type\": \"type.googleapis.com/google.cloud.audit.AuditLog\",\n"
                    "    \"authenticationInfo\": {\n"
                    "      \"principalEmail\": \"brightloaf-analytics@brightloaf-prod.iam.gserviceaccount.com\"\n"
                    "    },\n"
                    "    \"requestMetadata\": {\n"
                    "      \"callerIp\": \"194.26.29.112\",\n"
                    "      \"callerSuppliedUserAgent\": \"google-cloud-sdk gcloud/460.0.0\"\n"
                    "    },\n"
                    "    \"serviceName\": \"bigquery.googleapis.com\",\n"
                    "    \"methodName\": \"google.cloud.bigquery.v2.JobService.InsertJob\",\n"
                    "    \"status\": {\"code\": 0, \"message\": \"OK\"},\n"
                    "    \"serviceData\": {\n"
                    "      \"jobInsertRequest\": {\n"
                    "        \"resource\": {\n"
                    "          \"jobConfiguration\": {\n"
                    "            \"extract\": {\n"
                    "              \"destinationUris\": [\"gs://attacker-owned-bucket-eu/exfil/*.csv\"],\n"
                    "              \"sourceTable\": {\"projectId\": \"brightloaf-prod\", \"datasetId\": \"production_analytics\", \"tableId\": \"orders_fact\"}\n"
                    "            }\n"
                    "          }\n"
                    "        }\n"
                    "      }\n"
                    "    }\n"
                    "  }\n"
                    "}\n"
                    "```\n\n"
                    "Confirming Access Context Manager policy state:\n\n"
                    "```text\n"
                    "$ gcloud access-context-manager perimeters list --policy=10492817294\n"
                    "Listed 0 items. (No VPC Service Controls perimeters active for BigQuery or Cloud Storage)\n"
                    "```"
                ),
                "root": (
                    "Absence of VPC Service Controls allowed authorized IAM credentials to execute API data exports from the public internet. "
                    "Over-privileged IAM role grants violated least privilege, and un-audited service account keys enabled persistence outside corporate networks."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect Cloud Audit Logs filtering by `methodName = \"google.cloud.bigquery.v2.JobService.InsertJob\"`; discover bulk export job initiated from an unrecognized external IP.",
                    "Step 2: Check VPC Service Controls configuration in Access Context Manager; observe zero perimeters configured around BigQuery or Cloud Storage.",
                    "Step 3: Review IAM policy bindings for the compromised service account; discover broad `roles/bigquery.admin` granted at the project level instead of dataset-scoped viewer permissions.",
                    "Step 4: Check BigQuery table encryption; observe tables encrypted using standard Google-managed keys rather than customer-controlled keys."
                ],
                "fix": (
                    "Tactical Fix: Immediately revoke the compromised service account keys, disable the service account, and deploy a VPC-SC "
                    "perimeter around BigQuery and Cloud Storage.\n\n"
                    "Strategic Fix: Provision Cloud KMS CMEK keys for all BigQuery datasets, configure Cloud DLP automated PII masking pipelines, "
                    "and enforce organization-level constraint `constraints/iam.disableServiceAccountKeyCreation`."
                ),
                "verify": (
                    "Attempt to execute a BigQuery export command from an external IP using a valid service account credential. Verify the API "
                    "call is blocked immediately with an HTTP 403 VPC Service Controls violation error logged in Cloud Audit Logs."
                ),
                "residual": (
                    "VPC Service Controls perimeters require careful ingress/egress rule maintenance when integrating with third-party SaaS "
                    "platforms; any misconfigured rule can disrupt legitimate business data ingestion."
                ),
                "diagram": (
                    "Compromised SA credentials",
                    "Exfiltrate BQ over public internet",
                    "4.2M records leaked, GDPR P1",
                    "Enforce VPC-SC & CMEK encryption",
                    "Zero egress, 403 blocked at API edge"
                ),
                "facts": "Stolen service account exported 4.2M customer rows to external bucket; BigQuery was outside VPC-SC; IAM alone failed to stop exfiltration.",
                "inference": "IAM authenticates identity but cannot verify network provenance; VPC Service Controls is required to prevent data exfiltration.",
                "expected": "VPC-SC blocks all requests originating outside the corporate perimeter regardless of credential validity."
            },
            "lab": {
                "name": "Zero-Trust Perimeter, CMEK Encryption, and DLP De-identification Pipeline",
                "file": "day-070-security-compliance.md",
                "goal": "Author Access Context Manager VPC Service Controls manifests, deploy Cloud KMS CMEK keys, configure Cloud DLP cryptographic masking, and execute an exfiltration block test.",
                "expected": "An Access Context Manager perimeter specification, Cloud KMS CLI provisioning commands, a verified Cloud DLP JSON config, and an exfiltration audit runner.",
                "mode": "offline architecture specification, shell scripting, and configuration design; no cloud resources billed",
                "prereq": "Day 69 IAM policies and Day 68 compliance constraints",
                "preflight": "Review VPC Service Controls documentation, Access Context Manager YAML syntax, and Cloud KMS key access permissions.",
                "steps": [
                    (
                        "**Stage 1: Preflight & Environment Validation**\n"
                        "- Set target variables and verify security and encryption API enablement:\n\n"
                        "```sh\n"
                        "export PROJECT_ID=\"brightloaf-prod\"\n"
                        "export REGION=\"us-central1\"\n"
                        "export KEYRING_NAME=\"brightloaf-security-kr\"\n"
                        "export KEY_NAME=\"brightloaf-bq-cmek\"\n"
                        "\n"
                        "gcloud config set project ${PROJECT_ID}\n"
                        "gcloud services enable accesscontextmanager.googleapis.com cloudkms.googleapis.com dlp.googleapis.com bigquery.googleapis.com\n"
                        "```"
                    ),
                    (
                        "**Stage 2: Target / Backing Infrastructure Provisioning**\n"
                        "- Provision the Cloud KMS Keyring and CryptoKey with automated 90-day key rotation:\n\n"
                        "```sh\n"
                        "# 1. Create regional KMS Keyring\n"
                        "gcloud kms keyrings create ${KEYRING_NAME} --location=${REGION}\n"
                        "\n"
                        "# 2. Create CryptoKey for BigQuery CMEK\n"
                        "gcloud kms keys create ${KEY_NAME} \\\n"
                        "  --location=${REGION} \\\n"
                        "  --keyring=${KEYRING_NAME} \\\n"
                        "  --purpose=encryption \\\n"
                        "  --rotation-period=90d \\\n"
                        "  --next-rotation-time=+90d\n"
                        "```"
                    ),
                    (
                        "**Stage 3: Production Manifest Authoring (VPC-SC Perimeter YAML)**\n"
                        "- Author the declarative Access Context Manager VPC Service Controls perimeter definition (`vpc-sc-perimeter.yaml`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > vpc-sc-perimeter.yaml\n"
                        "- name: accessPolicies/10492817294/servicePerimeters/brightloaf_secure_perimeter\n"
                        "  title: Brightloaf Secure Data Perimeter\n"
                        "  description: Encloses BigQuery and Cloud Storage to block unauthorized external egress\n"
                        "  perimeterType: PERIMETER_TYPE_REGULAR\n"
                        "  status:\n"
                        "    resources:\n"
                        "    - projects/10492817294\n"
                        "    restrictedServices:\n"
                        "    - bigquery.googleapis.com\n"
                        "    - storage.googleapis.com\n"
                        "    accessLevels: []\n"
                        "    vpcAccessibleServices:\n"
                        "      enableRestriction: true\n"
                        "      allowedServices:\n"
                        "      - bigquery.googleapis.com\n"
                        "      - storage.googleapis.com\n"
                        "EOF\n"
                        "cat vpc-sc-perimeter.yaml\n"
                        "```"
                    ),
                    (
                        "**Stage 4: Workload Deployment & IAM Service Agent Binding**\n"
                        "- Author and bind KMS Encrypter/Decrypter permissions to the BigQuery service agent:\n\n"
                        "```sh\n"
                        "# Retrieve BigQuery service agent identity\n"
                        "BQ_SA=\"serviceAccount:bq-10492817294@bigquery-encryption.iam.gserviceaccount.com\"\n"
                        "\n"
                        "# Grant CMEK encryption role to BigQuery service agent\n"
                        "gcloud kms keys add-iam-policy-binding ${KEY_NAME} \\\n"
                        "  --location=${REGION} \\\n"
                        "  --keyring=${KEYRING_NAME} \\\n"
                        "  --member=\"${BQ_SA}\" \\\n"
                        "  --role=\"roles/cloudkms.cryptoKeyEncrypterDecrypter\"\n"
                        "```"
                    ),
                    (
                        "**Stage 5: Runtime Inspection & Cloud DLP De-identification Configuration**\n"
                        "- Author the Cloud DLP cryptographic masking configuration (`dlp-deid-config.json`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > dlp-deid-config.json\n"
                        "{\n"
                        "  \"deidentifyConfig\": {\n"
                        "    \"infoTypeTransformations\": {\n"
                        "      \"transformations\": [\n"
                        "        {\n"
                        "          \"infoTypes\": [{\"name\": \"EMAIL_ADDRESS\"}, {\"name\": \"PHONE_NUMBER\"}],\n"
                        "          \"primitiveTransformation\": {\n"
                        "            \"characterMaskConfig\": {\n"
                        "              \"maskingCharacter\": \"*\",\n"
                        "              \"numberToMask\": 4,\n"
                        "              \"reverseOrder\": true\n"
                        "            }\n"
                        "          }\n"
                        "        }\n"
                        "      ]\n"
                        "    }\n"
                        "  }\n"
                        "}\n"
                        "EOF\n"
                        "cat dlp-deid-config.json\n"
                        "```"
                    ),
                    (
                        "**Stage 6: Chaos / Fault Injection & Unauthorized Egress Rehearsal**\n"
                        "- Write an automated verification script simulating an unauthorized external export attempt (`verify_exfil_block.py`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > verify_exfil_block.py\n"
                        "import json\n"
                        "\n"
                        "# Validate DLP Configuration\n"
                        "with open('dlp-deid-config.json') as f:\n"
                        "    dlp_cfg = json.load(f)\n"
                        "info_types = [x['name'] for x in dlp_cfg['deidentifyConfig']['infoTypeTransformations']['transformations'][0]['infoTypes']]\n"
                        "assert 'EMAIL_ADDRESS' in info_types and 'PHONE_NUMBER' in info_types\n"
                        "print('PASS 1: Cloud DLP InfoType Masking Schema Validated.')\n"
                        "\n"
                        "# Emulate VPC Service Controls evaluation\n"
                        "def evaluate_vpc_sc(caller_ip, is_in_perimeter, service):\n"
                        "    if not is_in_perimeter:\n"
                        "        return {'status': 403, 'error': 'VPC_SC_PROHIBITED_BY_POLICY'}\n"
                        "    return {'status': 200, 'error': None}\n"
                        "\n"
                        "result = evaluate_vpc_sc('194.26.29.112', False, 'bigquery.googleapis.com')\n"
                        "assert result['status'] == 403, 'Exfiltration was not blocked!'\n"
                        "print(f\"PASS 2: External egress from 194.26.29.112 blocked with {result['error']}.\")\n"
                        "EOF\n"
                        "python3 verify_exfil_block.py\n"
                        "```"
                    ),
                    (
                        "**Stage 7: Triage, Troubleshooting & Remediation Patch**\n"
                        "- Inspect Access Context Manager dry-run violation logs and verify perimeter policy syntax:\n\n"
                        "```sh\n"
                        "python3 -c \"import yaml; p = yaml.safe_load(open('vpc-sc-perimeter.yaml')); print('Perimeter verified for resources:', p[0]['status']['resources'])\"\n"
                        "```"
                    ),
                    (
                        "**Stage 8: Cleanup & Resource Teardown**\n"
                        "- Remove temporary configuration files and restore directory baseline:\n\n"
                        "```sh\n"
                        "rm -f vpc-sc-perimeter.yaml dlp-deid-config.json verify_exfil_block.py\n"
                        "echo \"Security and compliance lab artifacts cleared; zero cloud spend.\"\n"
                        "```"
                    ),
                    (
                        "**Stage 9: Artifact Acceptance Criteria**\n"
                        "- Save verified VPC-SC perimeter specifications, Cloud KMS CMEK rotation parameters, and Cloud DLP de-identification configs into `day-070-security-compliance.md`."
                    )
                ],
                "verification": (
                    "Verify Cloud DLP JSON configuration:\n\n```sh\npython3 -c \"import json; d = json.load(open('dlp-deid-config.json')); print('DLP Config Validated: InfoTypes =', [x['name'] for x in d['deidentifyConfig']['infoTypeTransformations']['transformations'][0]['infoTypes']])\"\n```\n\nConfirm output lists `['EMAIL_ADDRESS', 'PHONE_NUMBER']`."
                ),
                "trouble": (
                    "If BigQuery queries fail with CMEK errors, inspect KMS IAM bindings to ensure the BigQuery service agent possesses `roles/cloudkms.cryptoKeyEncrypterDecrypter`."
                ),
                "cleanup": "No cloud resources created; retain configuration files in local repository.",
                "accept": "A validated VPC-SC perimeter policy, Cloud KMS CMEK deployment script, and working Cloud DLP de-identification schema."
            }
        },
        {
            "key": "topic-03",
            "title": "Reliability: High Availability, Fault Tolerance, and Disaster Recovery",
            "overview": (
                "Design resilient cloud platforms achieving 99.99% availability. Implement cross-zone redundancy, "
                "multi-region disaster recovery, circuit breakers, and automated health probing."
            ),
            "preview": (
                "A regional host failure isolates a single-zone Cloud SQL database; without Regional HA or cross-region "
                "read replicas, the checkout platform suffers a 5.3-hour outage and loses 14 hours of orders."
            ),
            "technical": (
                "#### 1. High Availability Math and Multi-Zone Redundancy\n\n"
                "In cloud infrastructure, availability is governed by mathematical series and parallel probability models. "
                "For components in series, total availability is the product of individual availabilities (`A_total = A_1 * A_2 * A_3`). "
                "If compute (99.9%), database (99.95%), and cache (99.9%) are in series, overall availability is `99.9% * 99.95% * 99.9% = 99.75%` "
                "(over 1.8 hours of downtime per month).\n\n"
                "To exceed 99.95%, architects introduce **parallel redundancy** (`A_parallel = 1 - (1 - A)^N`):\n\n"
                "- Deploying stateless compute across 3 availability zones in a Managed Instance Group increases compute availability to 99.999%.\n"
                "- Regional Cloud SQL provides synchronous replication across two zones with automatic sub-60-second failover.\n\n"
                "#### 2. Cascading Failure Prevention: Circuit Breakers and Jittered Backoff\n\n"
                "When a downstream service degrades, callers that retry aggressively cause a **retry storm** that drives system "
                "utilization to 100%, converting a minor slowdown into total collapse. Resilient architectures mandate two patterns:\n\n"
                "  1. **Full Jitter Exponential Backoff:** `sleep = random(0, min(max_backoff, base * 2 ^ attempt))`. Jitter disperses "
                "retry waves evenly across time, eliminating synchronized resonance.\n"
                "  2. **Circuit Breakers:** If the failure rate exceeds 50% over a 10-second rolling window, the circuit breaker **trips open**, "
                "immediately failing fast with HTTP 503 or returning cached fallback data without touching the downstream service.\n\n"
                "#### 3. Disaster Recovery RTO and RPO Archetypes\n\n"
                "Disaster recovery planning evaluates two non-negotiable parameters:\n\n"
                "- **Recovery Time Objective (RTO):** Maximum allowable duration the business can tolerate being offline.\n"
                "- **Recovery Point Objective (RPO):** Maximum allowable data loss measured in time (e.g. 5 minutes of lost transactions).\n\n"
                "```sh\n"
                "# Promote Cloud SQL cross-region replica during regional disaster\n"
                "gcloud sql instances promote-replica brightloaf-db-replica-eu \\\n"
                "  --quiet\n"
                "```\n\n"
                "#### 4. Chaos Engineering and Failure Injection Testing\n\n"
                "Reliability is a hypothesis until validated under real failure conditions. Chaos engineering proactively injects "
                "faults into staging and production: terminating random VM instances, injecting 500ms network latency via Linux `tc` "
                "(traffic control), and partitioning database subnets to verify that automated failover mechanisms function within SLO bounds.\n\n"
                "#### 5. Architectural Trade-offs: High Availability & DR Topologies\n\n"
                "| Topology Pattern | RTO Target | RPO Target | Cost Multiplier | Data Consistency Model | Failover Complexity |\n"
                "|---|---|---|---|---|---|\n"
                "| **Cold Standby (Backup & Restore)** | 4 – 24 hours | 1 – 24 hours | 1.1x (storage backups only) | Eventual (as of last backup) | High (manual infrastructure recreation) |\n"
                "| **Warm Standby (Pilot Light)** | 30 – 60 minutes | < 15 minutes | 1.4x (minimal idle compute + replicated DB) | Asynchronous replication lag | Moderate (scale up compute, promote replica) |\n"
                "| **Hot Standby (Active-Passive)** | < 2 minutes | < 5 seconds | 1.9x (full compute capacity running idle) | Asynchronous cross-region replication | Low (automated Load Balancer health rerouting) |\n"
                "| **Active-Active (Multi-Region Spanner)** | < 1 second (Instant) | Zero (0 seconds) | 2.5x – 3.5x (distributed consensus nodes) | External consistency (TrueTime synchrony) | None (automatic multi-region traffic routing) |\n"
            ),
            "questions": [
                "Why does multiplying component availabilities in series reduce overall system uptime?",
                "How does full jitter exponential backoff prevent retry storms during downstream service recovery?",
                "What is the operational trade-off between synchronous cross-region replication and transaction write latency?",
                "Why must chaos engineering tests be executed during normal working hours with on-call engineers present?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/reliability",
            "reference_label": "Google Cloud Architecture Center: Reliability pillar",
            "scenario": {
                "scenario": (
                    "Brightloaf operated its primary ordering database on a single-zone Cloud SQL instance in `us-central1-a`. "
                    "At 14:15 UTC, an unexpected hardware failure in the underlying host server crashed the database VM. Because the database "
                    "was configured with standalone Zonal availability rather than Regional High Availability, Google Cloud automated failover "
                    "could not occur. Compute Engine instances in zones b and c were unable to connect, exhausting their local connection pools. "
                    "Operators were forced to execute a manual point-in-time restore from a Cloud Storage backup taken at midnight, resulting "
                    "in over 14 hours of permanently lost order records."
                ),
                "impact": (
                    "Catastrophic P1 business outage lasting 5 hours and 18 minutes. Complete data loss of 3,420 settled customer orders "
                    "worth $145,000. Customer trust severely damaged; credit card chargebacks and compensation vouchers cost an additional $65,000. "
                    "Breach of contractual 99.95% merchant availability SLA."
                ),
                "constraints": (
                    "Enforce zero single-zone points of failure; guarantee RTO < 60 seconds for zonal outages; achieve RPO = 0 seconds "
                    "(zero data loss) within the primary operating region."
                ),
                "evidence": (
                    "Inspecting Compute Engine instance application logs during the database failure revealed client connection exhaustion:\n\n"
                    "```text\n"
                    "$ gcloud logging read 'resource.type=\"gce_instance\" AND textPayload=~\"database connection\"' --limit=3\n"
                    "2026-09-28T14:15:32Z order-service-mig-w4m1 app: ERROR [DBPool] Connection refused to 10.128.0.45:5432 (timeout 5000ms)\n"
                    "2026-09-28T14:15:35Z order-service-mig-w4m1 app: FATAL [DBPool] Connection pool exhausted (max 100/100). All worker threads blocked.\n"
                    "2026-09-28T14:15:38Z order-service-mig-k9z2 app: CRITICAL [HTTP] Upstream 504 Gateway Timeout returned to client.\n"
                    "```\n\n"
                    "Checking Cloud SQL instance configuration:\n\n"
                    "```yaml\n"
                    "$ gcloud sql instances describe brightloaf-orders-db --format=\"yaml(settings.availabilityType,state)\"\n"
                    "settings:\n"
                    "  availabilityType: ZONAL\n"
                    "state: FAILED\n"
                    "```"
                ),
                "root": (
                    "Single-zone database deployment created a single point of failure. Failure to enable Regional HA and point-in-time recovery "
                    "prevented automatic failover and forced reliance on stale daily backups."
                ),
                "diagnostic_steps": [
                    "Step 1: Check Cloud SQL instance configuration in Cloud Console; confirm `availabilityType: ZONAL` is enabled instead of `REGIONAL`.",
                    "Step 2: Inspect Cloud Monitoring timeline; observe immediate drop to zero database connections and simultaneous spike in VM connection timeouts.",
                    "Step 3: Review database backup metadata; discover automated backups occur only once every 24 hours without continuous transaction log archiving.",
                    "Step 4: Audit client microservice database retry logic; observe static 1-second retry loops without backoff or circuit breakers."
                ],
                "fix": (
                    "Tactical Fix: Immediately restore the latest valid transaction log snapshot and upgrade the Cloud SQL instance "
                    "to `--availability-type=REGIONAL` with synchronous standby in zone `b`.\n\n"
                    "Strategic Fix: Implement client-side circuit breakers with full jitter exponential backoff in all microservices, "
                    "and provision an asynchronous cross-region read replica in `us-east4`."
                ),
                "verify": (
                    "Initiate a simulated Cloud SQL failover via the CLI (<kbd>gcloud sql instances failover</kbd>). Verify that the standby instance "
                    "assumes primary leadership within 45 seconds, zero data transactions are lost, and application error rates recover automatically."
                ),
                "residual": (
                    "Regional HA failovers require clients to re-establish dropped TCP connections; connection pools must implement resilient "
                    "reconnection retry loops to prevent application crashes during the 45-second switchover."
                ),
                "diagram": (
                    "Single-zone host failure",
                    "No standby replica in zone B",
                    "5h downtime, 14h data lost",
                    "Regional HA + cross-zone failover",
                    "Sub-45s failover, zero data loss"
                ),
                "facts": "Zonal Cloud SQL instance failed; manual restore took 5h; 14 hours of orders permanently lost; RPO breached.",
                "inference": "Zonal persistence violates high availability mandates; regional HA is required for zero-data-loss durability.",
                "expected": "Regional Cloud SQL synchronously replicates to zone B and fails over automatically in under 60 seconds."
            },
            "lab": {
                "name": "Reliability Sizing and Chaos Engineering Circuit Breaker Simulation",
                "file": "day-070-reliability.md",
                "goal": "Calculate availability series math, author Cloud SQL Regional HA configuration, implement a Python circuit breaker with exponential jittered backoff, and verify failover metrics.",
                "expected": "A complete reliability calculation document, a Cloud SQL Regional HA upgrade script, an executable Python circuit breaker test runner, and failover verification commands.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 69 reliability basics and Day 68 SLA targets",
                "preflight": "Review Cloud SQL Regional HA architecture and Netflix Hystrix circuit breaker patterns.",
                "steps": [
                    (
                        "**Stage 1: Preflight & Environment Validation**\n"
                        "- Set target variables and calculate composite availability math:\n\n"
                        "```sh\n"
                        "export PROJECT_ID=\"brightloaf-prod\"\n"
                        "export REGION=\"us-central1\"\n"
                        "export DB_INSTANCE=\"brightloaf-orders-db\"\n"
                        "\n"
                        "# Calculate composite series availability: ALB (99.99%) * Compute (99.9%) * SQL (99.95%)\n"
                        "python3 -c \"print('Composite Series Availability:', f'{0.9999 * 0.999 * 0.9995 * 100:.3f}%')\"\n"
                        "```"
                    ),
                    (
                        "**Stage 2: Target / Backing Infrastructure Provisioning**\n"
                        "- Author the gcloud command upgrading Cloud SQL to Regional High Availability with automated backups:\n\n"
                        "```sh\n"
                        "cat <<'EOF' > upgrade_db_ha.sh\n"
                        "#!/usr/bin/env bash\n"
                        "# Upgrade Cloud SQL instance to Regional High Availability\n"
                        "echo \"Upgrading ${DB_INSTANCE} to REGIONAL HA...\"\n"
                        "# gcloud sql instances patch ${DB_INSTANCE} \\\n"
                        "#   --availability-type=REGIONAL \\\n"
                        "#   --backup-start-time=02:00 \\\n"
                        "#   --enable-bin-log \\\n"
                        "#   --retained-backups-count=14\n"
                        "echo \"Regional HA configuration specified: Primary zone us-central1-a, Standby zone us-central1-b.\"\n"
                        "EOF\n"
                        "chmod +x upgrade_db_ha.sh\n"
                        "./upgrade_db_ha.sh\n"
                        "```"
                    ),
                    (
                        "**Stage 3: Production Manifest Authoring (Client Connection Pool Config)**\n"
                        "- Author resilient database connection pool configuration with health checks (`db_pool.yaml`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > db_pool.yaml\n"
                        "database_pool:\n"
                        "  max_connections: 50\n"
                        "  min_idle_connections: 10\n"
                        "  connection_timeout_ms: 3000\n"
                        "  max_lifetime_ms: 1800000\n"
                        "  idle_timeout_ms: 600000\n"
                        "  validation_query: 'SELECT 1'\n"
                        "  circuit_breaker:\n"
                        "    failure_threshold_percent: 50\n"
                        "    sliding_window_seconds: 10\n"
                        "    wait_duration_in_open_seconds: 5\n"
                        "EOF\n"
                        "cat db_pool.yaml\n"
                        "```"
                    ),
                    (
                        "**Stage 4: Workload Deployment & Circuit Breaker Authoring**\n"
                        "- Author an executable Python circuit breaker implementing full jitter exponential backoff (`circuit_breaker_sim.py`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > circuit_breaker_sim.py\n"
                        "import time\n"
                        "import random\n"
                        "\n"
                        "class CircuitBreaker:\n"
                        "    def __init__(self, failure_threshold=3, recovery_time=1.0):\n"
                        "        self.failure_threshold = failure_threshold\n"
                        "        self.recovery_time = recovery_time\n"
                        "        self.failure_count = 0\n"
                        "        self.state = 'CLOSED'\n"
                        "        self.last_failure_time = 0\n"
                        "\n"
                        "    def call(self, success: bool):\n"
                        "        now = time.time()\n"
                        "        if self.state == 'OPEN':\n"
                        "            if now - self.last_failure_time > self.recovery_time:\n"
                        "                self.state = 'HALF-OPEN'\n"
                        "            else:\n"
                        "                return 'SHORT_CIRCUITED_503'\n"
                        "        \n"
                        "        if success:\n"
                        "            self.failure_count = 0\n"
                        "            self.state = 'CLOSED'\n"
                        "            return 'SUCCESS_200'\n"
                        "        else:\n"
                        "            self.failure_count += 1\n"
                        "            self.last_failure_time = now\n"
                        "            if self.failure_count >= self.failure_threshold:\n"
                        "                self.state = 'OPEN'\n"
                        "            return 'FAILED_500'\n"
                        "\n"
                        "cb = CircuitBreaker(failure_threshold=2, recovery_time=0.4)\n"
                        "assert cb.call(True) == 'SUCCESS_200'\n"
                        "print('1. Baseline normal operation: 200 OK')\n"
                        "EOF\n"
                        "python3 circuit_breaker_sim.py\n"
                        "```"
                    ),
                    (
                        "**Stage 5: Runtime Inspection & Verification**\n"
                        "- Test initial circuit breaker state transitions:\n\n"
                        "```sh\n"
                        "python3 -c \"import circuit_breaker_sim; print('Initial state: CLOSED')\"\n"
                        "```"
                    ),
                    (
                        "**Stage 6: Chaos / Fault Injection & Failure Rehearsal**\n"
                        "- Simulate downstream database outage and observe circuit breaker tripping:\n\n"
                        "```sh\n"
                        "cat <<'EOF' >> circuit_breaker_sim.py\n"
                        "# Inject consecutive failures to trip circuit\n"
                        "assert cb.call(False) == 'FAILED_500'\n"
                        "assert cb.call(False) == 'FAILED_500'\n"
                        "assert cb.call(True) == 'SHORT_CIRCUITED_503'  # Circuit tripped open\n"
                        "print('2. Injected failure: Circuit tripped to OPEN state (503 fast-fail)')\n"
                        "\n"
                        "# Wait for recovery timeout to verify half-open transition\n"
                        "time.sleep(0.5)\n"
                        "assert cb.call(True) == 'SUCCESS_200'  # Recovered\n"
                        "print('3. Downstream recovered: Circuit transitioned to CLOSED')\n"
                        "print('Circuit Breaker Mechanics Verified Successfully.')\n"
                        "EOF\n"
                        "python3 circuit_breaker_sim.py\n"
                        "```"
                    ),
                    (
                        "**Stage 7: Triage, Troubleshooting & Remediation Patch**\n"
                        "- Add exponential jittered backoff calculation to prevent synchronized retry waves:\n\n"
                        "```sh\n"
                        "cat <<'EOF' > backoff_jitter_calc.py\n"
                        "import random\n"
                        "def full_jitter_backoff(attempt, base_delay=0.1, max_delay=5.0):\n"
                        "    temp = min(max_delay, base_delay * (2 ** attempt))\n"
                        "    return random.uniform(0, temp)\n"
                        "\n"
                        "delays = [full_jitter_backoff(i) for i in range(5)]\n"
                        "print('Simulated retry delays with full jitter:', [f'{d:.3f}s' for d in delays])\n"
                        "EOF\n"
                        "python3 backoff_jitter_calc.py\n"
                        "```"
                    ),
                    (
                        "**Stage 8: Cleanup & Resource Teardown**\n"
                        "- Remove temporary reliability test files:\n\n"
                        "```sh\n"
                        "rm -f upgrade_db_ha.sh db_pool.yaml circuit_breaker_sim.py backoff_jitter_calc.py\n"
                        "echo \"Reliability test suite cleaned up successfully.\"\n"
                        "```"
                    ),
                    (
                        "**Stage 9: Artifact Acceptance Criteria**\n"
                        "- Document verified composite availability math, Cloud SQL Regional HA failover scripts, and working Python circuit breaker code in `day-070-reliability.md`."
                    )
                ],
                "verification": (
                    "Run circuit breaker automated test:\n\n```sh\npython3 -c \"import circuit_breaker_sim; print('Reliability Circuit Breaker Test Passed')\"\n```\n\nConfirm output displays `Reliability Circuit Breaker Test Passed`."
                ),
                "trouble": (
                    "If circuit breaker fails to close after recovery timeout, verify timestamp difference logic in the half-open state transition."
                ),
                "cleanup": "No cloud resources created; retain scripts and configuration templates in local repository.",
                "accept": "A verified availability mathematical model, Cloud SQL Regional HA command specification, and working Python circuit breaker script."
            }
        },
        {
            "key": "topic-04",
            "title": "Cost Optimization: FinOps Governance, Committed Use Discounts, and Storage Lifecycle",
            "overview": (
                "Implement FinOps practices on Google Cloud. Master cost allocation tagging, Committed Use Discounts (CUDs), "
                "Cloud Storage automated lifecycle tiers, and compute right-sizing with Recommender API."
            ),
            "preview": (
                "An organization's monthly cloud bill unexpectedly doubles to $85,000 due to unattached persistent disks, "
                "over-provisioned VMs running at 8% CPU, and multi-terabyte analytics datasets stored without compression or lifecycle rules."
            ),
            "technical": (
                "#### 1. The FinOps Lifecycle and Cost Allocation Architecture\n\n"
                "Cloud financial management (FinOps) replaces centralized annual budgeting with continuous iterative cost optimization "
                "divided into three phases: **Inform**, **Optimize**, and **Operate**:\n\n"
                "- **Inform (Cost Transparency):** Workloads cannot be optimized without granular cost attribution. Google Cloud enforces "
                "**Labeling and Tagging Policies** across all billable resources (`environment: prod`, `cost_center: 1042`, `service: checkout`, "
                "`owner: team-alpha`). Cloud Billing export streams raw billing data directly into BigQuery every hour.\n"
                "- **Optimize (Rate and Usage Reduction):** Right-sizing underutilized instances and committing to baseline usage.\n"
                "- **Operate (Continuous Governance):** Setting automated budget alerts, anomaly detection thresholds, and executive dashboards.\n\n"
                "#### 2. Committed Use Discounts (CUDs): Spend-Based vs. Resource-Based\n\n"
                "Google Cloud offers substantial discounts (up to 57% for 3-year commitments) in exchange for committed usage:\n\n"
                "  1. **Resource-Based CUDs:** Tied to specific machine series (e.g. N2, C2) and specific regions. Ideal for steady-state, "
                "predictable infrastructure running 24/7 (such as primary database instances).\n"
                "  2. **Flexible Spend-Based CUDs:** Committed dollar spend per hour across compute engines (Compute Engine, Google Kubernetes "
                "Engine, Cloud Run) regardless of machine series, region, or operating system. Maximizes architectural flexibility during migrations.\n\n"
                "#### 3. Storage Lifecycle Management and Coldline/Archive Migration\n\n"
                "Storing historical media, database backups, and raw log files in Cloud Storage Standard tier indefinitely is a massive "
                "budget drain ($0.020/GB/month vs $0.0012/GB/month in Archive). Automated **Object Lifecycle Management** rules migrate data "
                "transparently based on object age:\n\n"
                "```json\n"
                "{\n"
                "  \"rule\": [\n"
                "    {\n"
                "      \"action\": {\"type\": \"SetStorageClass\", \"storageClass\": \"NEARLINE\"},\n"
                "      \"condition\": {\"age\": 30, \"matchesPrefix\": [\"backups/\"]}\n"
                "    },\n"
                "    {\n"
                "      \"action\": {\"type\": \"SetStorageClass\", \"storageClass\": \"ARCHIVE\"},\n"
                "      \"condition\": {\"age\": 90, \"matchesPrefix\": [\"backups/\"]}\n"
                "    },\n"
                "    {\n"
                "      \"action\": {\"type\": \"Delete\"},\n"
                "      \"condition\": {\"age\": 365, \"matchesPrefix\": [\"backups/\"]}\n"
                "    }\n"
                "  ]\n"
                "}\n"
                "```\n\n"
                "#### 4. Active Right-Sizing with Recommender API\n\n"
                "Compute Engine VM instances frequently run at an average CPU utilization of 5% to 12% because developers size machines "
                "for hypothetical peaks. Google Cloud Recommender analyzes 14-day CPU and memory utilization percentiles and emits actionable "
                "downsizing recommendations (e.g. downsize `n2-standard-8` to `n2-standard-4`), reducing VM compute spend by 50% without risk.\n\n"
                "#### 5. Architectural Trade-offs: Compute & Storage Cost Levers\n\n"
                "| Cost Optimization Lever | Discount Potential | Commitment Duration | Workload Risk | Architectural Flexibility | Best Suited For |\n"
                "|---|---|---|---|---|---|\n"
                "| **Resource-Based CUDs** | Up to 57% | 1 or 3 Years | Zero workload risk | Low (locked to region & VM family) | Steady-state databases, persistent Kafka brokers |\n"
                "| **Flexible Spend-Based CUDs** | Up to 46% | 1 or 3 Years | Zero workload risk | Highest (cross-region, cross-service) | Mixed microservices, Cloud Run, GKE fleets |\n"
                "| **Spot VMs (Preemptible)** | 60% – 91% | None (On-demand) | High (can be preempted with 30s notice) | Moderate | Stateless batch processing, ML training, CI/CD runners |\n"
                "| **Storage Lifecycle Rules** | 80% – 94% | None | Early deletion fees if retrieved < 90d | High | Historical backups, audit logs, raw IoT archives |\n"
                "| **BigQuery Autoscaling Slots** | 30% – 50% | None | Potential query throttling if ceiling set low | High | Variable query workloads, daily batch ETL transforms |\n"
            ),
            "questions": [
                "What is the difference between Resource-Based CUDs and Flexible Spend-Based CUDs?",
                "How do early deletion fees affect the cost equation when migrating objects to Coldline or Archive storage?",
                "Why must FinOps cost allocation labels be enforced via CI/CD policies rather than manual entry?",
                "Under what workload conditions are Spot VMs dangerous for production batch processing?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/cost-optimization",
            "reference_label": "Google Cloud Architecture Center: Cost optimization pillar",
            "scenario": {
                "scenario": (
                    "Brightloaf experienced rapid growth following an international brand campaign, expanding its cloud footprint "
                    "across multiple development and production environments. Six months post-launch, the CFO received a monthly cloud bill "
                    "exceeding $84,000—more than 220% over budget. An audit revealed that 45 developers had provisioned `n2-standard-16` "
                    "development VMs that remained running 24/7 at 4% average CPU utilization. Over 180 unattached Persistent Disks from deleted "
                    "test clusters were quietly billing $4,200/month in SSD storage. Furthermore, all database snapshots and media archives "
                    "were stored in Standard Cloud Storage without lifecycle archival policies."
                ),
                "impact": (
                    "Severe budget overrun of $48,000/month ($576,000 annualized waste). Department head discretionary budgets frozen. "
                    "Mandatory emergency FinOps audit demanded by the board of directors. Unplanned resource cleanup consumed 120 senior "
                    "engineering hours."
                ),
                "constraints": (
                    "Reduce monthly cloud expenditure by at least 40% within 45 days; preserve developer productivity; maintain full production "
                    "performance and disaster recovery capabilities."
                ),
                "evidence": (
                    "Querying Cloud Billing BigQuery export revealed massive compute overspend without discounts and idle disk accumulation:\n\n"
                    "```text\n"
                    "$ bq query --use_legacy_sql=false '\n"
                    "  SELECT\n"
                    "    service.description AS service_name,\n"
                    "    ROUND(SUM(cost), 2) AS total_cost,\n"
                    "    ROUND(SUM(cost) - SUM(IFNULL(credits.amount, 0)), 2) AS net_cost\n"
                    "  FROM `brightloaf-billing.billing_export.gcp_billing_export_v1_012345`\n"
                    "  WHERE _PARTITIONDATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)\n"
                    "  GROUP BY 1 ORDER BY 2 DESC LIMIT 3'\n"
                    "+-------------------------+------------+------------+\n"
                    "| service_name            | total_cost | net_cost   |\n"
                    "+-------------------------+------------+------------+\n"
                    "| Compute Engine          | 54210.45   | 54210.45   |  (0% CUD discount applied)\n"
                    "| Cloud Storage           | 18450.20   | 18450.20   |  (140 TB unmanaged Standard tier)\n"
                    "| Cloud SQL               |  8920.10   |  8920.10   |\n"
                    "+-------------------------+------------+------------+\n"
                    "```\n\n"
                    "Listing unattached orphaned disks:\n\n"
                    "```text\n"
                    "$ gcloud compute disks list --filter=\"-users:*\" --format=\"table(name,sizeGb,type,zone)\" | head -n 4\n"
                    "NAME                    SIZE_GB  TYPE         ZONE\n"
                    "test-k8s-node-disk-01   200      pd-ssd       us-central1-a  (ORPHANED - $34/mo)\n"
                    "test-k8s-node-disk-02   200      pd-ssd       us-central1-a  (ORPHANED - $34/mo)\n"
                    "dev-temp-build-disk     500      pd-ssd       us-central1-b  (ORPHANED - $85/mo)\n"
                    "```"
                ),
                "root": (
                    "Lack of cost governance, missing automated cleanup policies for orphaned disks, absence of instance right-sizing, "
                    "and failure to leverage Committed Use Discounts or automated storage tiering resulted in compounding financial waste."
                ),
                "diagnostic_steps": [
                    "Step 1: Export Cloud Billing data to BigQuery; execute SQL grouping costs by `service.description` and `labels.environment`; discover non-production environments account for 62% of total spend.",
                    "Step 2: Run gcloud asset inventory query identifying all Persistent Disks with status `READY` and zero attached VM instances.",
                    "Step 3: Query Cloud Monitoring CPU metrics for Compute Engine; observe average CPU across 80% of VMs was below 10%.",
                    "Step 4: Inspect Cloud Storage bucket configurations; verify zero lifecycle management rules configured on 140 TB of backup objects."
                ],
                "fix": (
                    "Tactical Fix: Immediately snapshot and purge all unattached persistent disks, saving $4,200/month immediately, and "
                    "attach lifecycle management policies to the 140 TB backup storage bucket.\n\n"
                    "Strategic Fix: Commit to a 3-year Flexible Spend-Based CUD for steady-state baseline compute (saving 46%), and "
                    "deploy automated VM scheduling scripts stopping development instances on evenings and weekends."
                ),
                "verify": (
                    "Review Cloud Billing reports 30 days post-remediation. Confirm total monthly billing drops from $84,000 to $42,500 "
                    "(49.4% savings) while production SLOs and transaction throughput remain completely unaffected."
                ),
                "residual": (
                    "Committed Use Discounts legally obligate the enterprise to pay for committed spend regardless of architectural changes; "
                    "baseline commitments should cover only steady-state predictable minimums (70-80% of floor load)."
                ),
                "diagram": (
                    "Unchecked VM & disk growth",
                    "No CUDs, unattached SSDs",
                    "$84k/month budget blowout (+220%)",
                    "Purge disks, CUD commitment, lifecycle rules",
                    "Bill cut to $42.5k (50% saved)"
                ),
                "facts": "Cloud bill was $84k/month; unattached disks cost $4.2k; dev VMs ran 24/7 at 4% CPU; no lifecycle rules on 140 TB storage.",
                "inference": "Unmanaged cloud resources accumulate compounding financial waste; automated lifecycle and scheduling controls restore fiscal governance.",
                "expected": "FinOps controls cut monthly spend by 50% without impacting application availability or performance."
            },
            "lab": {
                "name": "FinOps Cost Modeling, CUD Calculator, and Automated Storage Lifecycle",
                "file": "day-070-cost-optimization.md",
                "goal": "Build an executable FinOps CUD calculator in Python, author automated Cloud Storage lifecycle manifests, analyze break-even commitment curves, and audit unattached storage volumes.",
                "expected": "A complete cost optimization strategy document, a Cloud Storage lifecycle rule manifest, and an executable Python CUD savings calculator.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 69 cost governance and Day 68 budget constraints",
                "preflight": "Review Google Cloud Pricing Calculator and Committed Use Discount contract terms.",
                "steps": [
                    (
                        "**Stage 1: Preflight & Environment Validation**\n"
                        "- Set target variables and enable cloud billing and recommender APIs:\n\n"
                        "```sh\n"
                        "export PROJECT_ID=\"brightloaf-prod\"\n"
                        "export REGION=\"us-central1\"\n"
                        "export BACKUP_BUCKET=\"gs://brightloaf-prod-backups\"\n"
                        "\n"
                        "gcloud config set project ${PROJECT_ID}\n"
                        "gcloud services enable storage.googleapis.com recommender.googleapis.com\n"
                        "```"
                    ),
                    (
                        "**Stage 2: Target / Backing Infrastructure Provisioning**\n"
                        "- Audit unattached persistent disks using gcloud filter queries:\n\n"
                        "```sh\n"
                        "# Query unattached disks and compute estimated wasted monthly spend\n"
                        "gcloud compute disks list --filter=\"-users:*\" --format=\"table(name,sizeGb,type,zone)\"\n"
                        "```"
                    ),
                    (
                        "**Stage 3: Production Manifest Authoring (GCS Lifecycle Policy JSON)**\n"
                        "- Author declarative Cloud Storage lifecycle configuration (`storage-lifecycle.json`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > storage-lifecycle.json\n"
                        "{\n"
                        "  \"rule\": [\n"
                        "    {\n"
                        "      \"action\": {\"type\": \"SetStorageClass\", \"storageClass\": \"NEARLINE\"},\n"
                        "      \"condition\": {\"age\": 30, \"matchesPrefix\": [\"backups/\"]}\n"
                        "    },\n"
                        "    {\n"
                        "      \"action\": {\"type\": \"SetStorageClass\", \"storageClass\": \"ARCHIVE\"},\n"
                        "      \"condition\": {\"age\": 90, \"matchesPrefix\": [\"backups/\"]}\n"
                        "    },\n"
                        "    {\n"
                        "      \"action\": {\"type\": \"Delete\"},\n"
                        "      \"condition\": {\"age\": 365, \"matchesPrefix\": [\"backups/\"]}\n"
                        "    }\n"
                        "  ]\n"
                        "}\n"
                        "EOF\n"
                        "cat storage-lifecycle.json\n"
                        "```"
                    ),
                    (
                        "**Stage 4: Workload Deployment & Lifecycle Policy Enforcement**\n"
                        "- Apply lifecycle configuration to backup storage bucket:\n\n"
                        "```sh\n"
                        "cat <<'EOF' > apply_lifecycle.sh\n"
                        "#!/usr/bin/env bash\n"
                        "echo \"Applying lifecycle policy to ${BACKUP_BUCKET}...\"\n"
                        "# gcloud storage buckets update ${BACKUP_BUCKET} --lifecycle-file=storage-lifecycle.json\n"
                        "echo \"Lifecycle policy active: 30d Nearline, 90d Archive, 365d Deletion.\"\n"
                        "EOF\n"
                        "chmod +x apply_lifecycle.sh\n"
                        "./apply_lifecycle.sh\n"
                        "```"
                    ),
                    (
                        "**Stage 5: Runtime Inspection & Verification**\n"
                        "- Validate lifecycle JSON syntax using Python:\n\n"
                        "```sh\n"
                        "python3 -c \"import json; d = json.load(open('storage-lifecycle.json')); assert len(d['rule']) == 3; print('Lifecycle JSON schema validated successfully.')\"\n"
                        "```"
                    ),
                    (
                        "**Stage 6: Chaos / Waste Audit Simulation**\n"
                        "- Simulate unattached disk identification and calculate immediate reclamation savings:\n\n"
                        "```sh\n"
                        "cat <<'EOF' > audit_orphaned_disks.py\n"
                        "disks = [\n"
                        "    {'name': 'test-k8s-node-disk-01', 'size_gb': 200, 'type': 'pd-ssd', 'rate': 0.17},\n"
                        "    {'name': 'test-k8s-node-disk-02', 'size_gb': 200, 'type': 'pd-ssd', 'rate': 0.17},\n"
                        "    {'name': 'dev-temp-build-disk', 'size_gb': 500, 'type': 'pd-ssd', 'rate': 0.17}\n"
                        "]\n"
                        "total_monthly_waste = sum(d['size_gb'] * d['rate'] for d in disks)\n"
                        "print(f\"Identified {len(disks)} orphaned disks.\")\n"
                        "print(f\"Monthly wasted spend: ${total_monthly_waste:.2f}\")\n"
                        "print(f\"Annualized wasted spend: ${total_monthly_waste * 12:.2f}\")\n"
                        "assert total_monthly_waste == 153.0\n"
                        "print(\"Orphaned disk cost audit PASSED.\")\n"
                        "EOF\n"
                        "python3 audit_orphaned_disks.py\n"
                        "```"
                    ),
                    (
                        "**Stage 7: Triage, Troubleshooting & FinOps CUD Model Calculation**\n"
                        "- Develop and execute the 3-year Flexible CUD savings financial model (`cud_calculator.py`):\n\n"
                        "```sh\n"
                        "cat <<'EOF' > cud_calculator.py\n"
                        "def calculate_cud_savings(hourly_on_demand_rate: float, discount_percent: float, commitment_months: int):\n"
                        "    hourly_discounted_rate = hourly_on_demand_rate * (1 - discount_percent / 100.0)\n"
                        "    hours_per_month = 730\n"
                        "    monthly_on_demand = hourly_on_demand_rate * hours_per_month\n"
                        "    monthly_cud = hourly_discounted_rate * hours_per_month\n"
                        "    monthly_savings = monthly_on_demand - monthly_cud\n"
                        "    total_savings = monthly_savings * commitment_months\n"
                        "    return monthly_on_demand, monthly_cud, monthly_savings, total_savings\n"
                        "\n"
                        "# Baseline: $50/hour on-demand spend, 3-year Flexible CUD (46% discount)\n"
                        "ondemand, cud, m_save, t_save = calculate_cud_savings(50.0, 46.0, 36)\n"
                        "print(f\"Monthly On-Demand Cost: ${ondemand:,.2f}\")\n"
                        "print(f\"Monthly CUD Cost: ${cud:,.2f}\")\n"
                        "print(f\"Monthly Net Savings: ${m_save:,.2f}\")\n"
                        "print(f\"3-Year Total Savings: ${t_save:,.2f}\")\n"
                        "assert t_save > 500000, 'Savings calculation threshold failed!'\n"
                        "print('FinOps CUD Calculator Validated Successfully.')\n"
                        "EOF\n"
                        "python3 cud_calculator.py\n"
                        "```"
                    ),
                    (
                        "**Stage 8: Cleanup & Resource Teardown**\n"
                        "- Clean up temporary FinOps calculation files:\n\n"
                        "```sh\n"
                        "rm -f storage-lifecycle.json apply_lifecycle.sh audit_orphaned_disks.py cud_calculator.py\n"
                        "echo \"FinOps model artifacts cleared; zero cloud resources billed.\"\n"
                        "```"
                    ),
                    (
                        "**Stage 9: Artifact Acceptance Criteria**\n"
                        "- Record the verified FinOps CUD financial model, Cloud Storage lifecycle rules, and disk audit script in `day-070-cost-optimization.md`."
                    )
                ],
                "verification": (
                    "Run automated CUD calculation test:\n\n```sh\npython3 -c \"import cud_calculator; print('FinOps CUD Test Passed')\"\n```\n\nConfirm output shows 3-year net savings exceeding $500,000."
                ),
                "trouble": (
                    "If lifecycle policies fail to transition objects, verify that bucket does not have retention locks preventing storage class changes."
                ),
                "cleanup": "No cloud resources created; retain JSON policies and calculation scripts in local repository.",
                "accept": "A verified FinOps CUD mathematical calculator, Cloud Storage lifecycle configuration, and cost governance policy document."
            }
        }
    ]
}
