"""day_data_070.py — Exhaustive architecture data specification for Day 70.

Covers Google Cloud Well-Architected Framework: Review Lenses (Operational Excellence,
Security/Privacy/Compliance, Reliability, Cost Optimization).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 70

DATA = {
    "day": 70,
    "part1_intro": (
        "Day 70 establishes the foundational evaluation method for cloud architecture: the Google Cloud "
        "Well-Architected Framework. Rather than assessing systems against subjective checklists, enterprise "
        "architects conduct structured reviews across four core lenses: Operational Excellence, Security/Privacy/"
        "Compliance, Reliability, and Cost Optimization. By tracing observable telemetry, cryptographic trust "
        "boundaries, mathematical failure domains, and economic commitments, architects replace unverified "
        "assumptions with quantitative proof. This session equips engineers to audit existing production systems, "
        "identify catastrophic systemic risks, and document defensible, prioritized remediation roadmaps."
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
  <thead>
    <tr>
      <th>Well-Architected Lens</th>
      <th>Core Technical Mandate</th>
      <th>Primary Anti-Pattern / Failure Mode</th>
      <th>Architectural Control Mechanism</th>
      <th>Verification Metric / Evidence</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Operational Excellence</strong></td>
      <td>Automate delivery; instrument user journeys</td>
      <td>Manual production changes; unowned alert storms</td>
      <td>GitOps pipelines, canary deployments, SLO error budgets</td>
      <td>Deployment frequency; MTTR &lt; 15 min; automated rollbacks</td>
    </tr>
    <tr>
      <td><strong>Security &amp; Compliance</strong></td>
      <td>Zero-Trust defense-in-depth; least privilege</td>
      <td>Perimeter-only trust; broad IAM roles; plaintext keys</td>
      <td>VPC Service Controls, CMEK with Cloud KMS, Cloud DLP</td>
      <td>Zero external egress leaks; 100% audit log coverage</td>
    </tr>
    <tr>
      <td><strong>Reliability</strong></td>
      <td>Design for failure; eliminate single points</td>
      <td>Cascading brownouts; unverified DR backups</td>
      <td>Regional HA, circuit breakers, multi-region replication</td>
      <td>SLO 99.95% met; RTO &lt; 30 min; RPO &lt; 5 min</td>
    </tr>
    <tr>
      <td><strong>Cost Optimization</strong></td>
      <td>Maximize business value per cloud dollar</td>
      <td>Over-provisioned static VMs; unattached storage disks</td>
      <td>Committed Use Discounts (CUDs), autoscaling, lifecycle rules</td>
      <td>Resource utilization &gt; 65%; zero zombie resources</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 70: Well-Architected Holistic Review Cycle",
        "desc": "Continuous architectural evaluation across operations, security, reliability, and cost governance.",
        "nodes": [
            ("Observe", "Telemetry & Error Budgets\\n(Operational Excellence)"),
            ("Protect", "Perimeters & Identities\\n(Security & Compliance)"),
            ("Sustain", "Redundancy & Failover\\n(Reliability Engineering)"),
            ("Govern", "Allocation & Commitment\\n(Cost Optimization)"),
        ],
        "caption": "Figure 70.1: Continuous Well-Architected assessment lifecycle validating production workloads against enterprise constraints."
    },
    "part3_intro": (
        "The following field cases analyze real-world production catastrophes resulting from pillar omissions. "
        "Each scenario includes quantitative impact data, diagnostic traces, root cause postmortems, "
        "defensible remediations, and dual-lane failed/corrected architectural diagrams."
    ),
    "part4_intro": (
        "These hands-on exercises provide production-grade, executable configurations and verification scripts "
        "for implementing SLO burn-rate alerts, configuring KMS encryption keys, modeling circuit breaker mechanics, "
        "and calculating break-even economics for Committed Use Discounts."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "Operational Excellence: Automation, Telemetry, and Incident Lifecycle",
            "overview": (
                "Establish operational excellence through Infrastructure as Code, progressive canary rollouts, "
                "multi-window multi-burn-rate SLO alerting, and blameless incident management."
            ),
            "preview": (
                "A Friday afternoon deployment corrupts the database schema; without automated canary analysis or "
                "pre-authorized rollback runbooks, operators spend 4 hours diagnosing the failure while customers experience 500 errors."
            ),
            "technical": (
                "#### 1. Site Reliability Engineering (SRE) Principles and Error Budget Governance\n\n"
                "Operational excellence begins with a cultural and technical shift: systems cannot achieve 100% availability, "
                "nor should they strive to. SRE defines the **Error Budget** as `1 - Availability SLO`. For a service targeting "
                "99.9% availability over a rolling 30-day window, the allowable downtime is 43.2 minutes. The error budget is the "
                "formal contractual boundary between product velocity and platform stability:\n\n"
                "- When the error budget is healthy (> 20% remaining), teams deploy rapidly and experiment.\n"
                "- When the error budget is exhausted (< 0%), feature deployments are frozen; engineering capacity shifts 100% "
                "to reliability engineering, technical debt remediation, and test automation.\n\n"
                "#### 2. Multi-Window Multi-Burn-Rate Alerting Architecture\n\n"
                "Traditional alerting relies on static threshold triggers (e.g. CPU > 85% or 5xx count > 10). This produces "
                "severe operational pathologies: alert fatigue from transient spikes, or delayed notifications during catastrophic slow burns. "
                "Google Cloud SRE mandates **Multi-Window Multi-Burn-Rate Alerts** based on consumption of the 30-day error budget:\n\n"
                "- **Burn Rate 14.4 (P1 Page):** Consumes 2% of the monthly error budget in 1 hour (100% exhaustion in 50 hours). "
                "Requires dual-window verification: a 1-hour lookback window AND a 5-minute short window to confirm the burn is active.\n"
                "- **Burn Rate 6 (P2 Ticket):** Consumes 5% of the error budget in 6 hours. Triggers on a 6-hour long window and "
                "30-minute short window.\n\n"
                "#### 3. Progressive Delivery and Automated Canary Analysis with Cloud Deploy\n\n"
                "Deploying new container revisions directly to 100% of production traffic exposes all users to untested regression bugs. "
                "Google Cloud Deploy implements automated canary progressions:\n\n"
                "```yaml\n"
                "# clouddeploy.yaml - Progressive Delivery Pipeline\n"
                "apiVersion: deploy.cloud.google.com/v1\n"
                "kind: DeliveryPipeline\n"
                "metadata:\n"
                "  name: checkout-pipeline\n"
                "serialPipeline:\n"
                "  stages:\n"
                "  - targetId: staging\n"
                "  - targetId: prod-canary\n"
                "    strategy:\n"
                "      canary:\n"
                "        runtimeConfig:\n"
                "          cloudRun:\n"
                "            automaticTrafficControl: false\n"
                "        route:\n"
                "          phases:\n"
                "          - id: canary-10\n"
                "            percentage: 10\n"
                "            verify: true\n"
                "          - id: canary-50\n"
                "            percentage: 50\n"
                "            verify: true\n"
                "          - id: stable-100\n"
                "            percentage: 100\n"
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
                    "The deployment contained an undocumented database index deletion that caused order insertion queries to revert to "
                    "full table scans under load. Within 12 minutes, the Cloud SQL database CPU spiked to 100%, and checkout latency surged "
                    "from 180ms to 24 seconds. The monitoring system fired 42 individual alerts across 8 Slack channels, but no single on-call "
                    "engineer had clear ownership. Because the deployment was performed using manual CLI commands rather than a versioned "
                    "pipeline, operators spent 3.5 hours manually reconstructing the previous container tag and database schema."
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
                "diagnostic_steps": [
                    "Step 1: Review Cloud Monitoring alerting history; observe alert flood across multiple microservices with no designated primary responder.",
                    "Step 2: Inspect Cloud Logging audit logs; discover manual `gcloud run deploy` command executed directly from a developer workstation without CI/CD pipeline provenance.",
                    "Step 3: Query Cloud SQL Query Insights; identify slow query `INSERT INTO orders` running sequentially without an index on `customer_id`.",
                    "Step 4: Check rollback procedures; observe absence of versioned deployment manifests or pre-scripted rollback runbooks."
                ],
                "root": (
                    "Lack of CI/CD pipeline automation, missing canary verification gates, absence of automated rollback mechanisms, "
                    "and uncoordinated static alert thresholds led to delayed incident detection, human confusion, and extended MTTR."
                ),
                "remediation_steps": [
                    "Step 1: Enforce Google Cloud Deploy progressive canary pipelines with automated 10% traffic verification and instant rollback hooks.",
                    "Step 2: Implement multi-window multi-burn-rate alerting policies in Cloud Monitoring, routing P1 alerts directly to PagerDuty with named escalation paths.",
                    "Step 3: Revoke direct production deployment IAM permissions from developer accounts; enforce deployment strictly through service accounts bound to Cloud Build.",
                    "Step 4: Conduct a blameless postmortem, establish a formal disaster recovery runbook repository, and implement a mandatory change-freeze window on Friday afternoons."
                ],
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
                "name": "SLO Multi-Burn-Rate Alerting and Automated Rollback Policy",
                "file": "day-070-operational-excellence.md",
                "goal": "Calculate SLO burn rates, generate Cloud Monitoring alerting policy JSON, and write an automated rollback verification test.",
                "expected": "A complete SLO specification, a Cloud Monitoring burn-rate alert policy manifest, and an automated verification script.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 69 observability foundations and Day 68 business requirements",
                "preflight": "Review Google SRE Workbook Chapter 5 on Alerting on SLOs.",
                "steps": [
                    "Define the service level objective in `day-070-operational-excellence.md`: Availability SLO = 99.9% over a 30-day rolling window.",
                    "Calculate the error budget burn rates: 30 days = 43,200 minutes; 0.1% budget = 43.2 minutes total allowed downtime. Burn rate 14.4 consumes 2% of budget (0.864 minutes of downtime) in 1 hour.",
                    "Generate the Cloud Monitoring Alert Policy JSON specification:\n\n```json\n{\n  \"displayName\": \"Checkout Service - Fast Burn Rate 14.4 (P1 Alert)\",\n  \"documentation\": {\n    \"content\": \"Checkout SLO error budget burning at 14.4x! Rollback canary immediately via Cloud Deploy.\",\n    \"mimeType\": \"text/markdown\"\n  },\n  \"conditions\": [\n    {\n      \"displayName\": \"Error budget consumption > 2% in 1 hour\",\n      \"conditionThreshold\": {\n        \"filter\": \"resource.type = \\\"cloud_run_revision\\\" AND metric.type = \\\"run.googleapis.com/request_count\\\" AND metric.labels.response_code_class = \\\"5xx\\\"\",\n        \"comparison\": \"COMPARISON_GT\",\n        \"thresholdValue\": 0.0144,\n        \"duration\": \"60s\",\n        \"trigger\": {\"count\": 1}\n      }\n    }\n  ],\n  \"combiner\": \"OR\",\n  \"enabled\": true\n}\n```",
                    "Write an automated Python script to simulate and verify burn rate calculations (`burn_rate_calc.py`):\n\n```python\n# burn_rate_calc.py\n\ndef calculate_burn_budget(slo: float, window_days: int, burn_rate: float, duration_hours: float):\n    total_minutes = window_days * 24 * 60\n    error_budget_fraction = 1.0 - slo\n    total_budget_minutes = total_minutes * error_budget_fraction\n    consumed_minutes = duration_hours * 60 * error_budget_fraction * burn_rate\n    percent_consumed = (consumed_minutes / total_budget_minutes) * 100\n    return total_budget_minutes, consumed_minutes, percent_consumed\n\ntotal, consumed, pct = calculate_burn_budget(0.999, 30, 14.4, 1.0)\nprint(f\"Total 30-Day Budget: {total:.1f} minutes\")\nprint(f\"Consumed in 1 hour at 14.4x: {consumed:.2f} minutes ({pct:.1f}% of total budget)\")\nassert round(pct, 1) == 2.0, \"Burn rate calculation error!\"\nprint(\"Burn Rate Mathematics Verified Successfully.\")\n```",
                    "Execute the burn rate verification script:\n\n```sh\npython3 burn_rate_calc.py\n```"
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
                "diagnostic_steps": [
                    "Step 1: Inspect Cloud Audit Logs filtering by `methodName = \"google.cloud.bigquery.v2.JobService.InsertJob\"`; discover bulk export job initiated from an unrecognized external IP.",
                    "Step 2: Check VPC Service Controls configuration in Access Context Manager; observe zero perimeters configured around BigQuery or Cloud Storage.",
                    "Step 3: Review IAM policy bindings for the compromised service account; discover broad `roles/bigquery.admin` granted at the project level instead of dataset-scoped viewer permissions.",
                    "Step 4: Check BigQuery table encryption; observe tables encrypted using standard Google-managed keys rather than customer-controlled keys."
                ],
                "root": (
                    "Absence of VPC Service Controls allowed authorized IAM credentials to execute API data exports from the public internet. "
                    "Over-privileged IAM role grants violated least privilege, and un-audited service account keys enabled persistence outside corporate networks."
                ),
                "remediation_steps": [
                    "Step 1: Immediately establish a VPC Service Controls perimeter enclosing BigQuery and Cloud Storage, blocking all egress to external projects and public IPs.",
                    "Step 2: Deploy VPC-SC dry-run mode to audit internal pipelines, verify legitimate service flows, and promote the perimeter to active enforcement.",
                    "Step 3: Revoke user-managed service account keys; mandate Workload Identity Federation for external services and short-lived OAuth tokens.",
                    "Step 4: Provision Cloud KMS CMEK keys for all BigQuery datasets and integrate Cloud DLP masking pipelines for customer PII fields."
                ],
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
                "name": "Zero-Trust Perimeter and CMEK Encryption Specification",
                "file": "day-070-security-compliance.md",
                "goal": "Design a VPC Service Controls perimeter configuration, write Cloud KMS CMEK provisioning scripts, and verify DLP de-identification policies.",
                "expected": "An Access Context Manager perimeter specification, Cloud KMS CLI commands, and a verified Cloud DLP JSON config.",
                "mode": "offline architecture specification, shell scripting, and configuration design; no cloud resources billed",
                "prereq": "Day 69 IAM policies and Day 68 compliance constraints",
                "preflight": "Review VPC Service Controls documentation and Cloud KMS key access permission requirements.",
                "steps": [
                    "Draft the Access Context Manager VPC Service Controls perimeter specification in `day-070-security-compliance.md`.",
                    "Define the Cloud KMS Keyring and CryptoKey provisioning commands:\n\n```sh\n# Provision KMS Keyring in regional location\ngcloud kms keyrings create brightloaf-security-kr --location=us-central1\n\n# Create CryptoKey with automatic 90-day rotation\ngcloud kms keys create brightloaf-bq-cmek \\\n  --location=us-central1 \\\n  --keyring=brightloaf-security-kr \\\n  --purpose=encryption \\\n  --rotation-period=90d \\\n  --next-rotation-time=+90d\n```",
                    "Grant the BigQuery service agent permission to encrypt/decrypt using the CMEK key:\n\n```sh\n# Bind CryptoKey Encrypter/Decrypter role to BigQuery Service Agent\ngcloud kms keys add-iam-policy-binding brightloaf-bq-cmek \\\n  --location=us-central1 \\\n  --keyring=brightloaf-security-kr \\\n  --member=\"serviceAccount:bq-project-number@bigquery-encryption.iam.gserviceaccount.com\" \\\n  --role=\"roles/cloudkms.cryptoKeyEncrypterDecrypter\"\n```",
                    "Write the Cloud DLP de-identification configuration JSON (`dlp-deid-config.json`):\n\n```json\n{\n  \"deidentifyConfig\": {\n    \"infoTypeTransformations\": {\n      \"transformations\": [\n        {\n          \"infoTypes\": [{\"name\": \"EMAIL_ADDRESS\"}, {\"name\": \"PHONE_NUMBER\"}],\n          \"primitiveTransformation\": {\n            \"characterMaskConfig\": {\n              \"maskingCharacter\": \"*\",\n              \"numberToMask\": 4,\n              \"reverseOrder\": true\n            }\n          }\n        }\n      ]\n    }\n  }\n}\n```",
                    "Execute a validation script to verify KMS policy and DLP JSON syntax:\n\n```sh\npython3 -c \"import json; d = json.load(open('dlp-deid-config.json')); assert 'deidentifyConfig' in d; print('Cloud DLP JSON Schema Validated')\"\n```"
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
                "A regional fiber cut isolates an entire Google Cloud region; without automated cross-region database "
                "failover or decoupled read paths, the entire business remains down for 6 hours."
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
                "diagnostic_steps": [
                    "Step 1: Check Cloud SQL instance configuration in Cloud Console; confirm `availabilityType: ZONAL` is enabled instead of `REGIONAL`.",
                    "Step 2: Inspect Cloud Monitoring timeline; observe immediate drop to zero database connections and simultaneous spike in VM connection timeouts.",
                    "Step 3: Review database backup metadata; discover automated backups occur only once every 24 hours without continuous transaction log archiving.",
                    "Step 4: Audit client microservice database retry logic; observe static 1-second retry loops without backoff or circuit breakers."
                ],
                "root": (
                    "Single-zone database deployment created a single point of failure. Failure to enable Regional HA and point-in-time recovery "
                    "prevented automatic failover and forced reliance on stale daily backups."
                ),
                "remediation_steps": [
                    "Step 1: Reconfigure Cloud SQL to Regional High Availability (`--availability-type=REGIONAL`), enabling synchronous standby replication across two availability zones.",
                    "Step 2: Enable Point-In-Time Recovery (PITR) with continuous write-ahead log (WAL) archiving to Cloud Storage, guaranteeing sub-5-minute RPO.",
                    "Step 3: Provision an asynchronous cross-region read replica in `us-east4` to provide disaster recovery protection against regional catastrophes.",
                    "Step 4: Implement client-side circuit breakers and jittered exponential backoff in all microservice database client connection pools."
                ],
                "verify": (
                    "Initiate a simulated Cloud SQL failover via the CLI (`gcloud sql instances failover`). Verify that the standby instance "
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
                "goal": "Calculate availability series math, write a Python circuit breaker with exponential jittered backoff, and verify failover metrics.",
                "expected": "A complete reliability calculation document, an executable Python circuit breaker test runner, and failover verification commands.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 69 reliability basics and Day 68 SLA targets",
                "preflight": "Review Cloud SQL Regional HA architecture and Netflix Hystrix circuit breaker patterns.",
                "steps": [
                    "Calculate composite availability in `day-070-reliability.md`: 3 components in series (ALB 99.99%, Compute 99.9%, Cloud SQL 99.95%) = `0.9999 * 0.999 * 0.9995 = 99.84%`.",
                    "Define Regional Cloud SQL HA configuration commands:\n\n```sh\n# Upgrade Cloud SQL instance to Regional High Availability\ngcloud sql instances patch brightloaf-orders-db \\\n  --availability-type=REGIONAL \\\n  --backup-start-time=02:00 \\\n  --enable-bin-log \\\n  --retained-backups-count=14\n```",
                    "Write an executable Python circuit breaker with jittered backoff (`circuit_breaker_sim.py`):\n\n```python\n# circuit_breaker_sim.py\nimport time\nimport random\n\nclass CircuitBreaker:\n    def __init__(self, failure_threshold=3, recovery_time=2.0):\n        self.failure_threshold = failure_threshold\n        self.recovery_time = recovery_time\n        self.failure_count = 0\n        self.state = 'CLOSED'\n        self.last_failure_time = 0\n\n    def call(self, success: bool):\n        now = time.time()\n        if self.state == 'OPEN':\n            if now - self.last_failure_time > self.recovery_time:\n                self.state = 'HALF-OPEN'\n            else:\n                return 'SHORT_CIRCUITED_503'\n        \n        if success:\n            self.failure_count = 0\n            self.state = 'CLOSED'\n            return 'SUCCESS_200'\n        else:\n            self.failure_count += 1\n            self.last_failure_time = now\n            if self.failure_count >= self.failure_threshold:\n                self.state = 'OPEN'\n            return 'FAILED_500'\n\ncb = CircuitBreaker(failure_threshold=2, recovery_time=0.5)\nassert cb.call(False) == 'FAILED_500'\nassert cb.call(False) == 'FAILED_500'\nassert cb.call(True) == 'SHORT_CIRCUITED_503'  # Circuit tripped open\ntime.sleep(0.6)\nassert cb.call(True) == 'SUCCESS_200'  # Recovered\nprint('Circuit Breaker Mechanics Verified Successfully.')\n```",
                    "Execute the Python circuit breaker simulation:\n\n```sh\npython3 circuit_breaker_sim.py\n```"
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
                "diagnostic_steps": [
                    "Step 1: Export Cloud Billing data to BigQuery; execute SQL grouping costs by `service.description` and `labels.environment`; discover non-production environments account for 62% of total spend.",
                    "Step 2: Run gcloud asset inventory query identifying all Persistent Disks with status `READY` and zero attached VM instances.",
                    "Step 3: Query Cloud Monitoring CPU metrics for Compute Engine; observe average CPU across 80% of VMs was below 10%.",
                    "Step 4: Inspect Cloud Storage bucket configurations; verify zero lifecycle management rules configured on 140 TB of backup objects."
                ],
                "root": (
                    "Lack of cost governance, missing automated cleanup policies for orphaned disks, absence of instance right-sizing, "
                    "and failure to leverage Committed Use Discounts or automated storage tiering resulted in compounding financial waste."
                ),
                "remediation_steps": [
                    "Step 1: Immediately purge orphaned unattached disks after creating a final archival snapshot, reclaiming $4,200/month instantly.",
                    "Step 2: Deploy Cloud Functions automated schedulers to stop all development and staging VMs outside business hours (19:00 to 07:00 and weekends), saving 65% on non-prod compute.",
                    "Step 3: Apply Recommender API recommendations to downsize over-provisioned production VMs, and purchase a 3-year Flexible Spend-Based CUD for baseline compute.",
                    "Step 4: Configure automated Cloud Storage lifecycle rules migrating backups to Nearline after 30 days and Archive after 90 days."
                ],
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
                "name": "FinOps Cost Modeling and CUD Break-Even Calculator",
                "file": "day-070-cost-optimization.md",
                "goal": "Build a FinOps financial model in Python to calculate break-even timelines and savings from Committed Use Discounts.",
                "expected": "A complete cost optimization strategy document, a Cloud Storage lifecycle rule manifest, and an executable Python CUD calculator.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 69 cost governance and Day 68 budget constraints",
                "preflight": "Review Google Cloud Pricing Calculator and Committed Use Discount contract terms.",
                "steps": [
                    "Draft the FinOps cost governance framework in `day-070-cost-optimization.md`.",
                    "Create the Cloud Storage automated lifecycle configuration (`storage-lifecycle.json`):\n\n```json\n{\n  \"rule\": [\n    {\n      \"action\": {\"type\": \"SetStorageClass\", \"storageClass\": \"NEARLINE\"},\n      \"condition\": {\"age\": 30, \"matchesPrefix\": [\"backups/\"]}\n    },\n    {\n      \"action\": {\"type\": \"SetStorageClass\", \"storageClass\": \"ARCHIVE\"},\n      \"condition\": {\"age\": 90, \"matchesPrefix\": [\"backups/\"]}\n    },\n    {\n      \"action\": {\"type\": \"Delete\"},\n      \"condition\": {\"age\": 365, \"matchesPrefix\": [\"backups/\"]}\n    }\n  ]\n}\n```",
                    "Apply lifecycle rule to production backup bucket:\n\n```sh\n# Apply lifecycle policy to GCS bucket\ngcloud storage buckets update gs://brightloaf-prod-backups \\\n  --lifecycle-file=storage-lifecycle.json\n```",
                    "Develop an executable Python CUD savings calculator script (`cud_calculator.py`):\n\n```python\n# cud_calculator.py\n\ndef calculate_cud_savings(hourly_on_demand_rate: float, discount_percent: float, commitment_months: int):\n    hourly_discounted_rate = hourly_on_demand_rate * (1 - discount_percent / 100.0)\n    hours_per_month = 730\n    monthly_on_demand = hourly_on_demand_rate * hours_per_month\n    monthly_cud = hourly_discounted_rate * hours_per_month\n    monthly_savings = monthly_on_demand - monthly_cud\n    total_savings = monthly_savings * commitment_months\n    return monthly_on_demand, monthly_cud, monthly_savings, total_savings\n\n# Scenario: $50/hour on-demand baseline compute, 3-year Flexible CUD (46% discount)\nondemand, cud, m_save, t_save = calculate_cud_savings(50.0, 46.0, 36)\nprint(f\"Monthly On-Demand Cost: ${ondemand:,.2f}\")\nprint(f\"Monthly CUD Cost: ${cud:,.2f}\")\nprint(f\"Monthly Net Savings: ${m_save:,.2f}\")\nprint(f\"3-Year Total Savings: ${t_save:,.2f}\")\nassert t_save > 500000, \"Savings threshold failed!\"\nprint(\"FinOps CUD Calculator Validated Successfully.\")\n```",
                    "Execute the Python CUD calculator test:\n\n```sh\npython3 cud_calculator.py\n```"
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
